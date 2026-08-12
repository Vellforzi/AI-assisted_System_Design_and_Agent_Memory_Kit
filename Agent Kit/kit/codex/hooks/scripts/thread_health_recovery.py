#!/usr/bin/env python3
"""CTX-GUARD-V2 thread health telemetry and file-grounded recovery."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import math
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "2.0"
PARSER_VERSION = "jsonl-counts-v1"
TASK_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,20}(?:-[A-Z0-9]{2,32}){2,8}\b")
SIDE_EFFECT_GATES = {"push", "release", "deploy", "db", "database", "credentials", "hosting", "ssh"}
CORE_EVIDENCE = (
    "AGENTS.md",
    "Project Map/current_state.md",
    "Project Map/working_state.yaml",
    "Project Map/source_authority.yaml",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def safe_identifier(value: Any, fallback: str) -> str:
    rendered = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value or "")).strip(".-")
    return (rendered[:96] or fallback)


def find_repo_root(cwd: str | Path | None) -> Path:
    start = Path(cwd or os.getcwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".codex").exists() and (candidate / "Project Map").exists():
            return candidate
    return start


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def lease_token(lease: dict[str, Any]) -> str:
    clean = {key: value for key, value in lease.items() if key != "cas_token"}
    payload = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def git_text(repo: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def analyze_transcript(path_value: Any) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "transcript_unavailable",
        "schema": "unknown",
        "parser_version": PARSER_VERSION,
        "bytes": 0,
        "record_count": 0,
        "turn_count": 0,
        "tool_call_count": 0,
        "tool_output_bytes": 0,
        "tool_output_share": 0.0,
        "approximate_tokens": 0,
        "token_estimator": "bytes_div_4_v1_approximate",
        "task_ids": [],
        "task_switch_count": 0,
        "metrics_partial": True,
    }
    if not path_value:
        return result
    path = Path(str(path_value))
    try:
        size = path.stat().st_size
        stream = path.open("r", encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        result["status"] = "transcript_unreadable"
        return result

    recognized = 0
    records = 0
    turns: set[str] = set()
    fallback_turns = 0
    tools = 0
    tool_bytes = 0
    ordered_tasks: list[str] = []
    known_keys = {"type", "role", "event", "payload", "turn_id", "turnId", "id", "tool_name", "toolName"}
    with stream:
        for raw in stream:
            line = raw.rstrip("\r\n")
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(value, dict):
                continue
            records += 1
            if known_keys.intersection(value):
                recognized += 1
            turn = value.get("turn_id") or value.get("turnId")
            if turn:
                turns.add(safe_identifier(turn, "turn"))
            role = str(value.get("role") or "").lower()
            event_type = str(value.get("type") or value.get("event") or "").lower()
            toolish = "tool" in event_type or role == "tool" or any(
                key in value for key in ("tool_name", "toolName", "tool_input", "toolInput", "tool_response")
            )
            if toolish:
                tools += 1
                tool_bytes += len(raw.encode("utf-8", errors="replace"))
            if role == "user" or event_type in {"user", "user_message", "turn_start"}:
                fallback_turns += 1
            for task_id in TASK_ID_RE.findall(line):
                if not ordered_tasks or ordered_tasks[-1] != task_id:
                    ordered_tasks.append(task_id)

    result.update(
        {
            "status": "recognized_jsonl_v1" if recognized else "transcript_schema_unknown",
            "schema": "jsonl_v1_observed" if recognized else "unknown",
            "bytes": size,
            "record_count": records,
            "turn_count": len(turns) or fallback_turns,
            "tool_call_count": tools,
            "tool_output_bytes": tool_bytes,
            "tool_output_share": round(tool_bytes / size, 6) if size else 0.0,
            "approximate_tokens": math.ceil(size / 4),
            "task_ids": sorted(set(ordered_tasks)),
            "task_switch_count": max(0, len(ordered_tasks) - 1),
            "metrics_partial": not bool(recognized),
        }
    )
    return result


def active_leases(repo: Path) -> list[tuple[Path, dict[str, Any]]]:
    root = repo / ".codex" / "runtime" / "scope_leases"
    rows: list[tuple[Path, dict[str, Any]]] = []
    if not root.exists():
        return rows
    for path in sorted(root.glob("*.json")):
        value = read_json(path)
        if value and value.get("state") == "active":
            rows.append((path, value))
    return rows


def final_events(task_root: Path, task_id: str) -> list[dict[str, Any]]:
    path = task_root / "orchestration_log.jsonl"
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(value, dict)
            and value.get("task_id") == task_id
            and value.get("event") in {"task_completed", "task_blocked"}
        ):
            rows.append(value)
    return rows


def authorization_tuple(receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": receipt.get("task_id"),
        "mode": receipt.get("mode"),
        "baseline_ref": receipt.get("baseline_ref"),
        "worktree": receipt.get("worktree"),
        "allowed_write_scope": receipt.get("allowed_write_scope") or [],
        "forbidden_actions": receipt.get("forbidden_actions") or [],
        "lease_path": receipt.get("lease_path"),
        "expires_on": receipt.get("expires_on"),
    }


def authorization_hash(receipt: dict[str, Any]) -> str:
    payload = json.dumps(
        authorization_tuple(receipt), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return sha256_bytes(payload)


def path_allowed(path: str, patterns: list[str]) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    for raw in patterns:
        pattern = str(raw).replace("\\", "/").lstrip("./")
        if pattern.endswith("/**") and (normalized == pattern[:-3] or normalized.startswith(pattern[:-2])):
            return True
        if normalized == pattern or fnmatch.fnmatchcase(normalized, pattern):
            return True
    return False


def dirty_paths(repo: Path) -> list[str]:
    rows: set[str] = set()
    for args in (("diff", "--name-only"), ("ls-files", "--others", "--exclude-standard")):
        value = git_text(repo, *args)
        if value:
            rows.update(line.replace("\\", "/") for line in value.splitlines() if line.strip())
    return sorted(rows)


def evaluate_recovery(
    repo: Path,
    data: dict[str, Any],
    *,
    event_name: str,
    persist: bool = True,
) -> dict[str, Any]:
    session_id = safe_identifier(data.get("session_id") or data.get("sessionId"), "session-unknown")
    turn_id = safe_identifier(data.get("turn_id") or data.get("turnId"), "turn-unknown")
    trigger = str(data.get("trigger") or "unknown").lower()
    transcript = analyze_transcript(data.get("transcript_path") or data.get("transcriptPath"))
    leases = active_leases(repo)
    head = git_text(repo, "rev-parse", "HEAD")
    coverage = {item: (repo / item).exists() for item in CORE_EVIDENCE}
    summary_quality = str(
        data.get("summary_hint_quality")
        or ("hint_only_uninspected" if event_name == "PostCompact" else "absent")
    )
    requested_action = str(data.get("requested_action") or "").lower()
    verdict = "pass"
    terminal_reason: str | None = None
    active_task: dict[str, Any] = {
        "task_id": None,
        "phase": "read_only_or_unknown",
        "worktree": str(repo).replace("\\", "/"),
        "head": head,
    }
    lease_info: dict[str, Any] = {
        "active_count": len(leases),
        "state": "none" if not leases else "active",
        "cas_validity": "not_applicable" if not leases else "unchecked",
    }
    orchestration = {"final_event_count": 0, "final_event_classification": "none"}
    authorization = {"status": "not_required_read_only", "tuple_sha256_valid": False}
    command_manifest = {"status": "not_required_read_only"}
    out_of_scope: list[str] = []

    if len(leases) > 1:
        verdict = "terminal_stop"
        terminal_reason = "COMPETING_LEASE"
    elif leases:
        lease_path, lease = leases[0]
        task_id = str(lease.get("task_id") or "")
        task_root_rel = str(lease.get("task_output_root") or "")
        task_root = repo / task_root_rel
        active_task.update(
            {
                "task_id": task_id or None,
                "phase": "active_write_task",
                "worktree": lease.get("worktree"),
                "head": head,
            }
        )
        token_valid = bool(lease.get("cas_token")) and lease.get("cas_token") == lease_token(lease)
        lease_info.update(
            {
                "path": lease_path.relative_to(repo).as_posix(),
                "task_id": task_id,
                "baseline_ref": lease.get("baseline_ref"),
                "cas_validity": "pass" if token_valid else "fail",
            }
        )
        if not token_valid:
            verdict, terminal_reason = "terminal_stop", "LEASE_CAS_MISMATCH"
        elif head is None or head != lease.get("baseline_ref"):
            verdict, terminal_reason = "terminal_stop", "BASELINE_MISMATCH"
        elif str(repo).replace("\\", "/").casefold() != str(lease.get("worktree") or "").replace("\\", "/").casefold():
            verdict, terminal_reason = "terminal_stop", "WORKTREE_MISMATCH"
        elif not task_id or not task_root_rel:
            verdict, terminal_reason = "terminal_stop", "ACTIVE_TASK_AMBIGUOUS"
        else:
            finals = final_events(task_root, task_id)
            orchestration = {
                "final_event_count": len(finals),
                "final_event_classification": finals[-1].get("event") if finals else "none",
            }
            if finals:
                verdict, terminal_reason = "terminal_stop", "FINAL_EVENT_EXISTS"
            receipt_path = task_root / "owner_authorization_receipt.json"
            receipt = read_json(receipt_path)
            if receipt is None and verdict == "pass":
                verdict, terminal_reason = "read_only_owner_gate", "AUTHORIZATION_RECEIPT_MISSING"
                authorization = {"status": "missing", "tuple_sha256_valid": False}
            elif receipt is not None:
                expected_hash = str(receipt.get("canonical_authorization_tuple_sha256") or "")
                auth_ok = (
                    receipt.get("task_id") == task_id
                    and receipt.get("mode") == "apply"
                    and receipt.get("baseline_ref") == lease.get("baseline_ref")
                    and str(receipt.get("worktree") or "").replace("\\", "/").casefold()
                    == str(lease.get("worktree") or "").replace("\\", "/").casefold()
                    and receipt.get("lease_path") == lease_path.relative_to(repo).as_posix()
                    and receipt.get("lease_cas_valid_at_issue") is True
                    and receipt.get("lease_snapshot_sha256") == sha256_bytes(lease_path.read_bytes())
                    and receipt.get("raw_owner_prompt_persisted") is False
                    and receipt.get("secret_payload_persisted") is False
                    and expected_hash == authorization_hash(receipt)
                )
                authorization = {
                    "status": "pass" if auth_ok else "mismatch",
                    "tuple_sha256_valid": expected_hash == authorization_hash(receipt),
                    "lease_snapshot_sha256_valid": receipt.get("lease_snapshot_sha256")
                    == sha256_bytes(lease_path.read_bytes()),
                }
                if not auth_ok and verdict == "pass":
                    verdict, terminal_reason = "read_only_owner_gate", "AUTHORIZATION_RECEIPT_MISMATCH"
                allowed = [str(x) for x in receipt.get("allowed_write_scope") or []]
                preexisting = [str(x) for x in receipt.get("preexisting_dirty_paths") or []]
                for path in dirty_paths(repo):
                    # The canonical lease manager temporarily projects this tracked
                    # compatibility file and restores it during CAS release. It is
                    # lease state, not an owner-requested source path.
                    if path == ".codex/ALLOWED_SCOPE.txt":
                        continue
                    if not path_allowed(path, allowed) and not path_allowed(path, preexisting):
                        out_of_scope.append(path)
                if out_of_scope and verdict == "pass":
                    verdict, terminal_reason = "terminal_stop", "OUT_OF_SCOPE_DIFF"
            manifest_path = task_root / "command-manifest.json"
            command_manifest = {"status": "present" if manifest_path.exists() else "missing_optional"}

    if not all(coverage.values()) and verdict == "pass":
        verdict, terminal_reason = "terminal_stop", "RECOVERY_EVIDENCE_INCOMPLETE"
    if requested_action in SIDE_EFFECT_GATES and verdict in {"pass", "pass_with_discarded_hints"}:
        verdict, terminal_reason = "read_only_owner_gate", "FRESH_OWNER_GATE_REQUIRED"
    if summary_quality in {"stale_hint", "conflicting_hint"} and verdict == "pass":
        verdict = "pass_with_discarded_hints"

    receipt_root = repo / ".codex" / "runtime" / "thread_health" / session_id
    prior_count = len(list(receipt_root.glob("*.json"))) if receipt_root.exists() else 0
    provisional = "elevated" if (
        transcript["bytes"] >= 10_000_000
        or prior_count >= 3
        or transcript["task_switch_count"] >= 4
        or transcript["tool_output_share"] >= 0.75
    ) else "normal"
    receipt: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "parser_version": PARSER_VERSION,
        "session_id": session_id,
        "turn_id": turn_id,
        "identifiers_sanitized": True,
        "timestamp": utc_now(),
        "hook_event": event_name,
        "trigger": trigger,
        "model_observation": {
            "value": safe_identifier(data.get("model"), "unknown"),
            "authority": "volatile_observation",
        },
        "transcript": transcript,
        "compaction_count": prior_count + 1,
        "active_context_pressure": {"status": "unknown_unless_surface_supplies_metric"},
        "thread_total_size": {"bytes": transcript["bytes"], "source": transcript["status"]},
        "active_task": active_task,
        "lease": lease_info,
        "orchestration": orchestration,
        "authorization": authorization,
        "command_manifest": command_manifest,
        "recovery_evidence": {
            "required": list(CORE_EVIDENCE),
            "coverage": coverage,
            "coverage_count": sum(1 for value in coverage.values() if value),
            "required_count": len(coverage),
        },
        "summary_hint": {"classification": summary_quality, "authority": "hint_only"},
        "health": {
            "total_transcript_bytes": transcript["bytes"],
            "compaction_count": prior_count + 1,
            "task_switch_count": transcript["task_switch_count"],
            "tool_output_share": transcript["tool_output_share"],
            "authorization_status": authorization["status"],
            "recovery_coverage": sum(1 for value in coverage.values() if value),
            "provisional_class": provisional,
            "thresholds_are_durable_truth": False,
        },
        "out_of_scope_diff_paths": out_of_scope,
        "recovery_integrity": verdict,
        "terminal_stop_reason": terminal_reason,
        "raw_prompt_persisted": False,
        "transcript_payload_persisted": False,
        "tool_output_payload_persisted": False,
        "secret_payload_persisted": False,
    }
    receipt_write = {"status": "skipped"}
    if persist:
        try:
            receipt_root.mkdir(parents=True, exist_ok=True)
            event_id = safe_identifier(
                f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}-{event_name}-{turn_id}",
                "event",
            )
            target = receipt_root / f"{event_id}.json"
            temporary = receipt_root / f".{event_id}.tmp"
            temporary.write_text(
                json.dumps(receipt, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            os.replace(temporary, target)
            receipt_write = {
                "status": "pass",
                "path": target.relative_to(repo).as_posix(),
            }
        except (OSError, ValueError) as exc:
            receipt_write = {"status": "failed", "error_class": type(exc).__name__}
    receipt["receipt_write"] = receipt_write
    return receipt


def run_event(data: dict[str, Any], event_name: str) -> dict[str, Any]:
    repo = find_repo_root(data.get("cwd"))
    receipt = evaluate_recovery(repo, data, event_name=event_name, persist=True)
    verdict = receipt["recovery_integrity"]
    should_continue = verdict in {"pass", "pass_with_discarded_hints"}
    if should_continue:
        message = (
            f"CTX-GUARD-V2 {event_name}: recovery_integrity={verdict}; "
            "compressed summary remains hint_only. Continue from current repository/task evidence."
        )
        return {"continue": True, "systemMessage": message}
    reason = str(receipt.get("terminal_stop_reason") or "RECOVERY_OWNER_GATE")
    return {
        "continue": False,
        "stopReason": f"CTX-GUARD-V2 recovery gate: {reason}.",
        "systemMessage": (
            f"CTX-GUARD-V2 stopped continuation: {reason}. "
            "Do not use compressed history as authority. Reconcile the named file/owner gate before source writes."
        ),
    }
