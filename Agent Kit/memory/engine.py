"""Agent-authored memory. Canonical JSON history; disposable SQLite FTS5 index.

No model, embedding, network, shell, transcript collector or background worker.
Hash/structure checks establish provenance, not the truth of an agent's claim.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sqlite3
import tempfile
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

VERSION = "0.1.1-local"
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_RECORD_BYTES = 48_000
MAX_ITEMS = 5000
STATUSES = {"candidate", "active", "stale", "superseded", "revoked", "rejected"}
KINDS = {"owner_decision", "constraint", "fact", "experience", "failed_approach", "open_question", "task_state"}
ROLES = {"owner_statement", "source", "test", "build", "runtime", "publication", "owner_acceptance"}
ORIGINS = {"owner_statement", "source_observation", "agent_analysis"}
LEVELS = ROLES | {"unverified"}
ID = re.compile(r"[A-Z][A-Z0-9_-]{2,95}\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
SECRET = re.compile(r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{16,}|\b(?:password|api_key|access_token|refresh_token)\s*[=:]\s*[\"']?[^\s\"'<>]{12,}|://[^/\s:]+:[^/\s@]+@)")
ECHO = re.compile(r"(?i)(?:<\s*/?\s*(?:amk_memory_context|memhub_memory_context|memhub_session_notice)\b|amk-derived:[a-f0-9]{64}|om-derived:[a-f0-9]{64})")
STOP = set("the a an is are to of for and or in on with what how why our this that do did we i it my from as be was were have has can should about что как почему это этот эта эти для или при где когда мы я у в на с по из к и а но ли не уже нужно надо его её их он она мне нас наш which does did been".split())


class MemoryError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def fail(code: str, message: str) -> None:
    raise MemoryError(code, message)


def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold().replace("ё", "е")


def words(text: str) -> list[str]:
    # Only the search projection is normalized. Evidence bytes remain unchanged.
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text).replace("_", " ")
    return list(dict.fromkeys(w for w in re.findall(r"[^\W_]+", normalize(text)) if w not in STOP and len(w) > 1))


def safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        fail("unsafe_path", "Use a portable project-relative path")
    parts = PurePosixPath(relative).parts
    if relative.startswith("/") or any(x in {"", ".", ".."} for x in relative.split("/")):
        fail("unsafe_path", "Absolute paths and traversal are forbidden")
    path = root
    for part in parts:
        if part.endswith((" ", ".")) or re.fullmatch(r"(?i)(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?", part) or part == ".git":
            fail("unsafe_path", "Ambiguous Windows path")
        path = path / part
        if path.is_symlink() or (path.exists() and getattr(path.lstat(), "st_file_attributes", 0) & 0x400):
            fail("unsafe_path", "Symlinks and reparse points are not memory paths")
    if not path.resolve().is_relative_to(root.resolve()):
        fail("unsafe_path", "Path escapes project")
    return path


def read_bytes(path: Path, limit: int = MAX_FILE_BYTES) -> bytes:
    if path.stat().st_size > limit:
        fail("size_limit", "Input exceeds the configured safety ceiling")
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        fail("size_limit", "Input grew beyond the safety ceiling")
    return raw


def load_json(path: Path) -> Any:
    try:
        return json.loads(read_bytes(path).decode("utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError):
        fail("invalid_json", "Invalid UTF-8 JSON input")


def atomic_write(path: Path, raw: bytes, expected: str | None) -> None:
    def current() -> str | None:
        return digest(read_bytes(path)) if path.exists() else None
    if current() != expected:
        fail("cas_conflict", "File changed; reread before retrying")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".amk-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if current() != expected:
            fail("cas_conflict", "Concurrent edit before replace")
        os.replace(name, path)
        if read_bytes(path) != raw:
            fail("readback_failed", "Written bytes differ")
    finally:
        Path(name).unlink(missing_ok=True)


@contextmanager
def file_lock(path: Path) -> Iterator[None]:
    """OS-released lock; never break another writer's lock based on age."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        acquired = False
        try:
            if os.name == "nt":
                import msvcrt
                try:
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                except OSError:
                    fail("writer_busy", "Another memory writer is active")
            else:
                import fcntl
                try:
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    fail("writer_busy", "Another memory writer is active")
            acquired = True
            yield
        finally:
            if acquired:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream, fcntl.LOCK_UN)


class Memory:
    def __init__(self, root: str | Path, config: str = "Project Map/memory.config.json"):
        self.root = Path(root).resolve(strict=True)
        self.config_path = safe_path(self.root, config)
        self.config = load_json(self.config_path)
        if self.config.get("schema_version") != 1 or not self.config.get("project_id"):
            fail("invalid_config", "schema_version=1 and project_id are required")
        self.project_id = self.config["project_id"]
        self.records = safe_path(self.root, self.config["records_dir"])
        self.cache = safe_path(self.root, self.config["cache_dir"])
        if self.records == self.cache or self.records.is_relative_to(self.cache) or self.cache.is_relative_to(self.records):
            fail("invalid_config", "Canonical records and disposable cache must be separate")
        self.branch = self.config.get("default_branch", "main")
        self.writable = self.config.get("write_enabled", False) is True
        self.warnings: list[dict[str, str]] = []
        self._loaded_hashes: dict[str, str] = {}

    def record_path(self, identifier: str) -> Path:
        if not isinstance(identifier, str) or not ID.fullmatch(identifier):
            fail("invalid_id", "Use 3-96 uppercase ASCII letters, digits, dash or underscore")
        return safe_path(self.root, self.records.relative_to(self.root).as_posix() + "/" + identifier + ".json")

    def source(self, relative: str) -> dict[str, Any]:
        lowered = relative.casefold()
        if any(p == ".git" or p.startswith(".env") or p in {"credentials", "secrets"} for p in PurePosixPath(lowered).parts) or "доступы" in lowered:
            fail("secret_path", "Credential sources are not memory evidence")
        p = safe_path(self.root, relative)
        raw = read_bytes(p)
        return {"path": relative, "sha256": digest(raw), "size_bytes": len(raw)}

    def _load(self, identifier: str) -> dict[str, Any] | None:
        p = self.record_path(identifier)
        if not p.exists():
            return None
        raw = read_bytes(p)
        self._loaded_hashes[identifier] = digest(raw)
        value = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(value, dict):
            fail("record_identity", "Record must be an object")
        if value.get("schema_version") != 1 or value.get("project_id") != self.project_id or value.get("id") != identifier:
            fail("record_identity", "Record belongs to another project or schema")
        versions = value.get("versions")
        if not isinstance(versions, list) or not versions:
            fail("invalid_history", "Record history is required")
        previous = None
        operations: set[str] = set()
        for number, row in enumerate(versions, 1):
            core = {k: v for k, v in row.items() if k != "event_sha256"}
            if (row.get("revision") != number or row.get("previous_sha256") != previous
                    or row.get("event_sha256") != digest(encoded(core))
                    or row.get("operation_id") in operations or row.get("status") not in STATUSES):
                fail("invalid_history", "Revision chain is inconsistent; do not repair it by guessing")
            previous = row["event_sha256"]
            operations.add(row["operation_id"])
        return value

    def all_records(self) -> dict[str, dict[str, Any]]:
        paths = sorted(self.records.glob("*.json")) if self.records.exists() else []
        if len(paths) > MAX_ITEMS:
            fail("corpus_limit", "Too many records; narrow the configured corpus")
        return {p.stem: self._load(p.stem) for p in paths}  # type: ignore[misc]

    def _validate(self, record: dict[str, Any]) -> None:
        required = {"id", "kind", "subject", "scope", "branch", "language", "title", "summary", "search_keys", "original", "evidence", "applicability", "verification"}
        optional = {"details", "not_applicable", "relationships", "task"}
        if not isinstance(record, dict) or required - record.keys() or record.keys() - required - optional:
            fail("invalid_record", "Missing or unknown record fields")
        self.record_path(record["id"])
        if len(encoded(record)) > MAX_RECORD_BYTES or SECRET.search(encoded(record).decode()):
            fail("unsafe_record", "Oversized record or likely credential value")
        for key in ["subject", "scope", "branch", "language", "title", "summary", "applicability"]:
            if not isinstance(record[key], str) or not record[key].strip():
                fail("invalid_record", "Required text fields must be nonempty")
        if record["kind"] not in KINDS or record["language"] != self.config.get("record_language", "en"):
            fail("invalid_record", "Unsupported kind or wrong canonical language label")
        keys = record["search_keys"]
        if not isinstance(keys, dict) or set(keys) != {"ru", "en"}:
            fail("invalid_search_keys", "Provide both ru and en search-key arrays")
        for language in keys:
            if not isinstance(keys[language], list) or not 1 <= len(keys[language]) <= 12 or not all(isinstance(k, str) and 0 < len(k) <= 240 for k in keys[language]):
                fail("invalid_search_keys", "Search keys must be bounded strings")
        original = record["original"]
        if not isinstance(original, dict) or set(original) != {"text", "language", "kind", "event_id", "ref"}:
            fail("invalid_origin", "Original wording and addressable origin are required")
        if original["kind"] not in ORIGINS or not all(isinstance(v, str) and v.strip() for v in original.values()):
            fail("invalid_origin", "Recall, translation or empty origin cannot be independent evidence")
        if ECHO.search(normalize(original["text"])):
            fail("derived_echo", "An injected memory block is not new owner evidence")
        if original["language"] not in {"ru", "en", "mixed"}:
            fail("invalid_origin", "Original language must be ru, en or mixed")
        if not isinstance(record["evidence"], list) or not 1 <= len(record["evidence"]) <= 20:
            fail("evidence_required", "Provide 1-20 explicit evidence files")
        for evidence in record["evidence"]:
            if not isinstance(evidence, dict) or set(evidence) != {"path", "sha256", "role", "freshness"}:
                fail("invalid_evidence", "Evidence needs path, SHA-256, role and freshness")
            if not SHA.fullmatch(str(evidence["sha256"])) or evidence["role"] not in ROLES or evidence["freshness"] not in {"required", "historical"}:
                fail("invalid_evidence", "Invalid evidence hash, role or freshness")
            path = safe_path(self.root, evidence["path"])
            if path.is_relative_to(self.records) or path.is_relative_to(self.cache):
                fail("derived_echo", "Memory and its cache are not independent evidence; use revision-bound links")
        if not isinstance(record.get("details", ""), str):
            fail("invalid_record", "details must be text")
        exclusions = record.get("not_applicable", [])
        if not isinstance(exclusions, list) or len(exclusions) > 20 or not all(isinstance(v, str) and 0 < len(v) <= 2000 for v in exclusions):
            fail("invalid_record", "not_applicable must be a bounded list of text")
        relationships = record.get("relationships", [])
        if not isinstance(relationships, list) or len(relationships) > 20:
            fail("invalid_relationship", "relationships must be a bounded list")
        verification = record["verification"]
        if not isinstance(verification, dict) or set(verification) != {"level", "note"} or verification["level"] not in LEVELS or not isinstance(verification["note"], str) or not verification["note"].strip():
            fail("invalid_verification", "State an evidence level and its actual boundary")
        for relation in record.get("relationships", []):
            if not isinstance(relation, dict) or set(relation) != {"id", "revision", "relation"} or relation["relation"] not in {"related", "derived_from"}:
                fail("invalid_relationship", "Use a revision-bound related or derived_from link")
            if relation["id"] == record["id"] or not isinstance(relation["revision"], int) or relation["revision"] < 1:
                fail("invalid_relationship", "Self reference or invalid revision")
        if record["kind"] == "task_state":
            task = record.get("task", {})
            if not isinstance(task, dict):
                fail("invalid_task_state", "task must be an object")
            if set(task) != {"task_id", "baseline_head", "next_action", "unsafe_to_repeat", "state"} or task["state"] not in {"active", "blocked", "completed"}:
                fail("invalid_task_state", "Task identity, evidence-bound state and next action are required")
            if not all(isinstance(task[k], str) and task[k] for k in ["task_id", "baseline_head", "next_action"]) or not isinstance(task["unsafe_to_repeat"], list) or not all(isinstance(v, str) and v.strip() for v in task["unsafe_to_repeat"]):
                fail("invalid_task_state", "Invalid task recovery fields")

    def freshness(self, record: dict[str, Any], records: dict[str, dict[str, Any]], seen: frozenset[str] = frozenset(), *, check_level: bool = True) -> list[dict[str, str]]:
        problems: list[dict[str, str]] = []
        if record["id"] in seen:
            return [{"reason": "dependency_cycle", "ref": record["id"]}]
        seen = seen | {record["id"]}
        for e in record["evidence"]:
            if e["freshness"] != "required":
                continue
            try:
                if self.source(e["path"])["sha256"] != e["sha256"]:
                    problems.append({"reason": "source_changed", "ref": e["path"]})
            except (OSError, MemoryError):
                problems.append({"reason": "source_unavailable", "ref": e["path"]})
        for relation in record.get("relationships", []):
            if relation["relation"] != "derived_from":
                continue
            parent = records.get(relation["id"])
            if not parent:
                problems.append({"reason": "parent_missing", "ref": relation["id"]})
                continue
            head = parent["versions"][-1]
            if head["revision"] != relation["revision"] or head["status"] != "active":
                problems.append({"reason": "parent_revised_or_retired", "ref": relation["id"]})
            elif self.freshness(head["record"], records, seen):
                problems.append({"reason": "parent_stale", "ref": relation["id"]})
        if check_level:
            issue = self._promotion_error(record)
            if issue:
                problems.append({"reason": issue[0], "ref": record["id"]})
        return problems

    @staticmethod
    def _promotion_error(record: dict[str, Any]) -> tuple[str, str] | None:
        # Historical proof may explain the past, never establish a current level.
        roles = {e["role"] for e in record["evidence"] if e["freshness"] == "required"}
        if record["kind"] in {"owner_decision", "constraint"} and (record["original"]["kind"] != "owner_statement" or "owner_statement" not in roles):
            return "owner_evidence_required", "A current owner decision requires a currently bound owner source"
        level = record["verification"]["level"]
        if level != "unverified" and level not in roles:
            return "evidence_level_mismatch", "The stated evidence level needs currently bound evidence of that role"
        if record["kind"] != "open_question" and level == "unverified":
            return "unverified_promotion", "Keep an unsupported claim as a candidate"
        if not roles:
            return "live_evidence_required", "Active records require at least one currently checked origin"
        return None

    def _assert_evidence(self, record: dict[str, Any], records: dict[str, dict[str, Any]], promote: bool) -> None:
        issues = self.freshness(record, records, check_level=False)
        if issues:
            fail("stale_evidence", "Evidence/parent revision changed: " + ", ".join(x["ref"] for x in issues))
        for relation in record.get("relationships", []):
            parent = records.get(relation["id"])
            if not parent or parent["versions"][-1]["revision"] != relation["revision"]:
                fail("stale_relationship", "Reread the related record")
            if parent["versions"][-1]["record"]["branch"] not in {record["branch"], "*"}:
                fail("branch_mismatch", "Cross-branch relationship requires a separately scoped record")
        if not promote:
            return
        issue = self._promotion_error(record)
        if issue:
            fail(*issue)

    def _mutate(self, identifier: str, operation_id: str, expected_revision: int, action: str,
                record: dict[str, Any] | None, status: str, reason: str, successor: str | None = None) -> dict[str, Any]:
        if not self.writable:
            fail("read_only", "Memory writes are not enabled for this project")
        if not isinstance(operation_id, str) or not re.fullmatch(r"[A-Za-z0-9_.:-]{3,160}", operation_id) or expected_revision < 0 or not reason.strip():
            fail("invalid_operation", "Operation ID, expected revision and reason are required")
        request_sha = digest(encoded([identifier, operation_id, expected_revision, action, record, status, reason, successor]))
        lock = safe_path(self.root, self.cache.relative_to(self.root).as_posix() + "/write.lock")
        with file_lock(lock):
            records = self.all_records()
            for doc in records.values():
                for event in doc["versions"]:
                    if event["operation_id"] == operation_id:
                        if doc["id"] != identifier or event["request_sha256"] != request_sha:
                            fail("operation_conflict", "Operation ID reused with different content")
                        return {"ok": True, "duplicate": True, "id": identifier, "accepted_revision": event["revision"], "current_revision": doc["versions"][-1]["revision"]}
            doc = records.get(identifier)
            head = doc["versions"][-1] if doc else None
            revision = head["revision"] if head else 0
            if revision != expected_revision:
                fail("cas_conflict", "Expected revision does not match; reread current record")
            if head and head["status"] in {"revoked", "superseded", "rejected"}:
                fail("retired_record", "Retired records cannot be resurrected; record a new supported decision")
            selected = copy.deepcopy(record if record is not None else (head["record"] if head else {}))
            self._validate(selected)
            if selected["id"] != identifier:
                fail("record_identity", "ID does not match target")
            if head and any(head["record"][k] != selected[k] for k in ["kind", "scope", "subject", "branch"]):
                fail("immutable_identity", "Changing subject/scope/branch requires a new record")
            if action == "stage":
                for other in records.values():
                    if other["id"] == identifier:
                        continue
                    old = other["versions"][-1]["record"]
                    same_origin = old["original"]["event_id"] == selected["original"]["event_id"] and old["original"]["ref"] == selected["original"]["ref"]
                    same_meaning = normalize(old["summary"]).strip() == normalize(selected["summary"]).strip()
                    retired = other["versions"][-1]["status"] in {"revoked", "rejected", "superseded"}
                    same_literal_origin = same_origin and normalize(old["original"]["text"]).strip() == normalize(selected["original"]["text"]).strip()
                    # New evidence may support the same conclusion after retirement;
                    # the old record remains retired. Replaying its origin is not new.
                    if old["scope"] == selected["scope"] and old["branch"] == selected["branch"] and old["subject"] == selected["subject"] and ((same_meaning and not retired) or same_literal_origin):
                        fail("duplicate_or_echo", "Revise/link the existing record instead: " + other["id"])
                self._assert_evidence(selected, records, False)
            elif status == "active":
                if not head or head["status"] not in {"candidate", "stale"}:
                    fail("invalid_transition", "Only a candidate or reverified stale record can be activated")
                self._assert_evidence(selected, records, True)
            elif not head or status not in {"stale", "revoked", "rejected", "superseded"}:
                fail("invalid_transition", "Unsupported lifecycle transition")
            if status == "superseded":
                target = records.get(successor or "")
                if not target or successor == identifier or target["versions"][-1]["status"] != "active":
                    fail("invalid_successor", "Supersession requires another active record")
                replacement = target["versions"][-1]["record"]
                if any(replacement[k] != selected[k] for k in ["scope", "branch", "subject"]):
                    fail("invalid_successor", "Successor must address the same subject, scope and branch")
                self._assert_evidence(replacement, records, True)
            p = self.record_path(identifier)
            expected_file = self._loaded_hashes.get(identifier) if head else None
            event = {"revision": revision + 1, "operation_id": operation_id, "request_sha256": request_sha,
                     "timestamp": datetime.now(timezone.utc).isoformat(), "action": action, "status": status,
                     "reason": reason, "successor": successor, "record": selected,
                     "previous_sha256": head["event_sha256"] if head else None}
            event["event_sha256"] = digest(encoded(event))
            if doc is None:
                doc = {"schema_version": 1, "project_id": self.project_id, "id": identifier, "versions": []}
            doc["versions"].append(event)
            raw = encoded(doc)
            if len(raw) > MAX_FILE_BYTES:
                fail("history_limit", "History ceiling reached; explicit archival design is required")
            atomic_write(p, raw, expected_file)
            self._load(identifier)
            return {"ok": True, "duplicate": False, "id": identifier, "revision": revision + 1,
                    "status": status, "path": p.relative_to(self.root).as_posix(), "sha256": digest(raw)}

    def stage(self, record: dict[str, Any], operation_id: str, expected_revision: int = 0) -> dict[str, Any]:
        return self._mutate(record.get("id", ""), operation_id, expected_revision, "stage", record, "candidate", "Agent-authored candidate; no semantic truth is inferred by the tool")

    def transition(self, identifier: str, status: str, operation_id: str, expected_revision: int, reason: str, successor: str | None = None) -> dict[str, Any]:
        if status not in STATUSES - {"candidate"}:
            fail("invalid_transition", "Use stage to create or revise a candidate")
        return self._mutate(identifier, operation_id, expected_revision, "lifecycle", None, status, reason, successor)

    def read(self, identifier: str, history: bool = False) -> dict[str, Any]:
        records = self.all_records()
        doc = records.get(identifier)
        if not doc:
            fail("not_found", "No record with this ID")
        head = doc["versions"][-1]
        issues = self.freshness(head["record"], records)
        result = {"id": identifier, "project_id": self.project_id, "revision": head["revision"], "status": head["status"],
                  "effective_status": "stale" if issues and head["status"] == "active" else head["status"],
                  "freshness_issues": issues, "record": head["record"], "successor": head["successor"],
                  "content_trust": "UNTRUSTED_EVIDENCE", "semantic_truth_verified_by_tool": False}
        if history:
            result["history"] = doc["versions"]
        return result

    def _corpus(self) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], str]:
        records = self.all_records()
        rows: list[dict[str, Any]] = []
        self.warnings = []
        for identifier, doc in records.items():
            h = doc["versions"][-1]; r = h["record"]
            row = {"id": identifier, "scope": r["scope"], "branch": r["branch"], "status": h["status"],
                   "title": r["title"], "summary": r["summary"], "revision": h["revision"],
                   "evidence_level": r["verification"]["level"], "kind": r["kind"],
                   "path": self.record_path(identifier).relative_to(self.root).as_posix(), "source_hash": h["event_sha256"],
                   "keys": " ".join(k for values in r["search_keys"].values() for k in values),
                   "body": " ".join([r["original"]["text"], r["applicability"], r.get("details", ""), " ".join(r.get("not_applicable", [])), " ".join(e["path"] for e in r["evidence"])]),
                   "origin_kind": r["original"]["kind"]}
            rows.append(row)
        # Explicit document references are search projections, never promoted facts.
        for spec in self.config.get("reference_files", []):
            if set(spec) != {"path", "scope", "status", "branch"} or spec["status"] not in {"reference", "historical"}:
                fail("invalid_config", "Reference documents need an explicit scope/status/branch")
            try:
                source = self.source(spec["path"])
                raw = read_bytes(safe_path(self.root, spec["path"]))
                if digest(raw) != source["sha256"]:
                    fail("source_changed", "Reference changed while indexing")
                text = raw.decode("utf-8-sig")
                if SECRET.search(text):
                    fail("secret_content", "Reference contains a likely credential")
            except (OSError, UnicodeError, MemoryError) as exc:
                self.warnings.append({"path": spec["path"], "reason": getattr(exc, "code", "source_unavailable")})
                continue
            lines = text.splitlines()
            for start in range(0, len(lines), 100):
                part = "\n".join(lines[start:start + 100])
                if len(part) > 24000:
                    self.warnings.append({"path": spec["path"], "reason": "oversized_section_omitted"})
                    continue
                rows.append({"id": "DOC-" + digest(spec["path"].encode())[:12].upper() + "-" + str(start + 1),
                             "title": spec["path"], "summary": part[:900], "keys": "", "body": part,
                             "scope": spec["scope"], "status": spec["status"], "branch": spec["branch"], "kind": "reference",
                             "revision": None, "path": spec["path"], "source_hash": source["sha256"],
                             "lines": [start + 1, min(len(lines), start + 100)], "evidence_level": "unverified", "origin_kind": "reference_document"})
        if len(rows) > MAX_ITEMS:
            fail("corpus_limit", "Explicit corpus exceeds item ceiling")
        fingerprint = digest(encoded([self.config, [(x["id"], x["source_hash"]) for x in rows]]))
        return rows, records, fingerprint

    @staticmethod
    def _database(rows: list[dict[str, Any]], fingerprint: str) -> sqlite3.Connection:
        c = sqlite3.connect(":memory:")
        try:
            c.execute("CREATE TABLE meta(fingerprint TEXT)")
            c.execute("INSERT INTO meta VALUES (?)", (fingerprint,))
            c.execute("CREATE VIRTUAL TABLE search USING fts5(id UNINDEXED, title, aliases, body, tokenize='unicode61')")
            c.executemany("INSERT INTO search VALUES (?,?,?,?)", [(r["id"], " ".join(words(r["title"] + " " + r["id"])), " ".join(words(r["keys"])), " ".join(words(r["summary"] + " " + r["body"]))) for r in rows])
            c.commit()
        except sqlite3.Error:
            c.close()
            fail("fts_unavailable", "This Python SQLite build must provide FTS5")
        return c

    def index(self) -> dict[str, Any]:
        rows, _, fingerprint = self._corpus()
        target = safe_path(self.root, self.cache.relative_to(self.root).as_posix() + "/index.sqlite3")
        with file_lock(safe_path(self.root, self.cache.relative_to(self.root).as_posix() + "/index.lock")):
            c = self._database(rows, fingerprint)
            fd, name = tempfile.mkstemp(prefix=".index-", suffix=".sqlite3", dir=target.parent)
            os.close(fd)
            try:
                out = sqlite3.connect(name)
                try:
                    c.backup(out)
                finally:
                    out.close()
                os.replace(name, target)
            finally:
                c.close()
                Path(name).unlink(missing_ok=True)
        return {"ok": True, "items": len(rows), "fingerprint": fingerprint, "path": target.relative_to(self.root).as_posix(), "warnings": self.warnings, "canonical_records_modified": False}

    def search(self, queries: list[str], *, scope: str | None = None, branch: str | None = None,
               include_history: bool = False, limit: int = 8, offset: int = 0, budget: int = 8000) -> dict[str, Any]:
        if not queries or len(queries) > 6 or any(not isinstance(q, str) or len(q) > 2000 for q in queries) or not 1 <= limit <= 50 or offset < 0 or not 1000 <= budget <= 40000:
            fail("invalid_query", "Use 1-6 short queries, limit 1-50 and budget 1000-40000")
        rows, records, fingerprint = self._corpus()
        terms = list(dict.fromkeys(w for q in queries for w in words(q)))
        raw_terms = set(terms)
        for group in self.config.get("term_aliases", []):
            if not isinstance(group, list) or not all(isinstance(s, str) for s in group):
                fail("invalid_config", "term_aliases must be arrays of strings")
            if any(set(words(alias)) and set(words(alias)) <= raw_terms for alias in group):
                terms.extend(w for alias in group for w in words(alias))
        terms = list(dict.fromkeys(terms))[:60]
        if not terms:
            return {"hits": [], "status": "empty_query", "suggestion": "Use a component, identifier or RU/EN search variant", "warnings": self.warnings}
        db_path = safe_path(self.root, self.cache.relative_to(self.root).as_posix() + "/index.sqlite3")
        c = None; cache_state = "memory_only"
        if db_path.exists():
            try:
                c = sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True)
                if c.execute("SELECT fingerprint FROM meta").fetchone() != (fingerprint,):
                    c.close(); c = None; cache_state = "stale_rebuilt_in_memory"
                else:
                    cache_state = "valid_cache"
            except sqlite3.Error:
                if c:
                    c.close()
                c = None; cache_state = "invalid_rebuilt_in_memory"
        if c is None:
            c = self._database(rows, fingerprint)
        try:
            expression = " OR ".join('"' + t.replace('"', '""') + '"' for t in terms)
            matches = c.execute("SELECT id, bm25(search,0,8,5,1) FROM search WHERE search MATCH ? ORDER BY 2,id", (expression,)).fetchall()
        except sqlite3.Error:
            fail("search_failed", "Index query failed; rebuild the disposable index")
        finally:
            c.close()
        lookup = {r["id"]: r for r in rows}
        found: list[dict[str, Any]] = []
        skipped = {"scope": 0, "branch": 0, "lifecycle": 0, "stale": 0}
        branch = branch or self.branch
        for identifier, score in matches:
            if identifier not in lookup:
                fail("index_corrupt", "Cached index refers to an unknown record; rebuild")
            r = lookup[identifier]
            if scope and not (r["scope"] == scope or r["scope"].startswith(scope + ".")):
                skipped["scope"] += 1; continue
            if r["branch"] not in {branch, "*"}:
                skipped["branch"] += 1; continue
            if not include_history and r["status"] not in {"active", "reference"}:
                skipped["lifecycle"] += 1; continue
            issues = self.freshness(records[identifier]["versions"][-1]["record"], records) if identifier in records else []
            if issues and not include_history:
                skipped["stale"] += 1; continue
            hit = {k: v for k, v in r.items() if k not in {"keys", "body"}}
            hit["effective_status"] = "stale" if issues and r["status"] == "active" else r["status"]
            hit["freshness_issues"] = issues
            hit["canonical_reread_required"] = True
            hit["semantic_truth_verified_by_tool"] = False
            hit["score"] = round(-score, 6)
            exact_id = any(identifier.casefold() == q.strip().casefold() for q in queries)
            hit["exact_identifier"] = exact_id
            found.append(hit)
        found.sort(key=lambda h: (not h["exact_identifier"], -h["score"], h["id"]))
        selected = []; used = 0
        for hit in found[offset:offset + limit]:
            size = len(encoded(hit).decode())
            if used + size > budget:
                break
            selected.append(hit); used += size
        truncated = offset + len(selected) < len(found)
        return {"status": "ok" if selected else ("budget_exhausted" if found[offset:] else "empty"), "project_id": self.project_id,
                "content_trust": "UNTRUSTED_EVIDENCE", "derived_context": True,
                "echo_marker": "amk-derived:" + digest(encoded([fingerprint, queries, offset, [h["id"] for h in selected]])),
                "queries": queries, "expanded_terms": terms, "hits": selected, "eligible_hits": len(found),
                "offset": offset, "next_offset": offset + len(selected) if truncated and selected else None,
                "truncated": truncated, "budget_exhausted": truncated and len(selected) < limit,
                "returned_characters": used, "index": cache_state, "skipped": skipped, "warnings": self.warnings,
                "coverage": "partial" if self.warnings else "complete_for_configured_corpus",
                "empty_is_not_proof_of_absence": True,
                "suggestion": "Use an exact identifier, English/Russian alternatives or explicit historical mode; reopen canonical sources"}

    def audit(self) -> dict[str, Any]:
        records = self.all_records()
        findings = []
        for identifier in records:
            head = records[identifier]["versions"][-1]
            issues = self.freshness(head["record"], records)
            if issues:
                findings.append({"id": identifier, "status": head["status"], "effective_status": "stale" if head["status"] == "active" else head["status"], "issues": issues})
        return {"ok": True, "project_id": self.project_id, "records": len(records), "findings": findings,
                "model_calls": 0, "canonical_records_modified": False, "semantic_truth_verified_by_tool": False}
