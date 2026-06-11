#!/usr/bin/env python3
"""Generate ChatGPT Project source manifest and context pack (Agent Memory Kit).

Stdlib only. Config-driven. No network. No ChatGPT UI automation.

Example:
  python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \\
    --config CHATGPT_PROJECT_SOURCES.config.json --write --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FORBIDDEN_PATTERNS = [
    r"\.env\b",
    r"\.cursor/mcp\.env",
    r"secrets",
    r"credentials",
    r"archive/releases",
    r"\.git\b",
    r"canvases",
    r"agent-transcripts",
    r"runtime",
    r"\.zip\b",
]
FORBIDDEN_SHA_RE = re.compile(r"\.sha256\b(?!.*CHATGPT_PROJECT_SOURCES\.sha256)")
HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
FIELD_RE = re.compile(r"^\s*[-*]\s*\*\*(?P<label>[^:*]+):\*\*\s*(?P<value>.*)$")
GENERATOR_ID = "Agent Kit/kit/tools/generate_chatgpt_project_sources.py"

EXPLICIT_EXCLUSIONS = [
    "Previous kit release archives — not GPT sources by default",
    "Secrets: .env, credential stores, MCP env files",
    "Runtime evidence: agent-transcripts, canvases, IDE runtime folders",
    ".git/, *.zip, unrelated code trees unless task-scoped",
]


@dataclass
class ProjectConfig:
    root: Path
    output_dir: Path
    instructions_compact: Path
    worklog: Path
    context_input_paths: list[Path]
    memory_index: Path
    current_state: Path
    working_state: Path
    source_authority: Path
    checkpoint_heading: str
    repo_routing_boundary: str
    required_sources: list[tuple[str, str]]
    optional_sources: list[tuple[str, str]]
    config_path: Path

    @property
    def out_context_md(self) -> Path:
        return self.output_dir / "GPT_CONTEXT_PACK.md"

    @property
    def out_context_json(self) -> Path:
        return self.output_dir / "GPT_CONTEXT_PACK.json"

    @property
    def out_todo(self) -> Path:
        return self.output_dir / "CHATGPT_PROJECT_SOURCES_TODO.md"

    @property
    def out_manifest(self) -> Path:
        return self.output_dir / "CHATGPT_PROJECT_SOURCES_MANIFEST.json"

    @property
    def out_sha256(self) -> Path:
        return self.output_dir / "CHATGPT_PROJECT_SOURCES.sha256"


@dataclass
class FileMeta:
    path: str
    rel: Path
    purpose: str
    required: bool
    destination: str
    exists: bool = False
    sha256: str | None = None
    size_bytes: int | None = None
    mtime_iso: str | None = None
    action: str = "MISSING"
    previous_sha256: str | None = None


@dataclass
class MemoryEntry:
    entry_id: str
    class_name: str
    status: str
    title: str
    last_verified_at: str
    source_file: str


def load_config(config_path: Path, project_root_override: Path | None) -> ProjectConfig:
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    base = project_root_override or (config_path.parent / raw.get("project_root", "."))
    root = base.resolve()

    def p(key: str) -> Path:
        return (root / raw[key]).resolve()

    def rel(path: Path) -> str:
        return path.relative_to(root).as_posix()

    output_dir = (root / raw["output_dir"]).resolve()
    required = [(item["path"], item["purpose"]) for item in raw.get("required_sources", [])]
    optional = [(item["path"], item["purpose"]) for item in raw.get("optional_sources", [])]
    context_inputs = [(root / rel_path).resolve() for rel_path in raw.get("context_pack_inputs", [])]

    return ProjectConfig(
        root=root,
        output_dir=output_dir,
        instructions_compact=p("instructions_compact_path"),
        worklog=p("worklog_path"),
        context_input_paths=context_inputs,
        memory_index=p("memory_index_path"),
        current_state=p("current_state_path"),
        working_state=p("working_state_path"),
        source_authority=p("source_authority_path"),
        checkpoint_heading=raw.get("checkpoint_heading", "## Checkpoint"),
        repo_routing_boundary=raw.get(
            "repo_routing_boundary",
            "Separate package repository from project mirror.",
        ),
        required_sources=required,
        optional_sources=optional,
        config_path=config_path.resolve(),
    )


def rel_posix(cfg: ProjectConfig, path: Path) -> str:
    return path.relative_to(cfg.root).as_posix()


def is_forbidden_path(path_str: str) -> bool:
    normalized = path_str.replace("\\", "/")
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True
    if FORBIDDEN_SHA_RE.search(normalized):
        return True
    return False


def sha256_file(path: Path) -> tuple[str, int, str]:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    stat = path.stat()
    mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).replace(microsecond=0).isoformat()
    return digest.hexdigest(), stat.st_size, mtime


def source_latest_mtime(paths: list[Path]) -> str | None:
    mtimes = [p.stat().st_mtime for p in paths if p.is_file()]
    if not mtimes:
        return None
    return datetime.fromtimestamp(max(mtimes), tz=timezone.utc).replace(microsecond=0).isoformat()


def run_generated_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def short_sha(sha: str | None) -> str:
    return "—" if not sha else sha[:12]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip().strip('"').strip("'")
    return value


def parse_memory_index(text: str) -> list[MemoryEntry]:
    entries: list[MemoryEntry] = []
    for block in re.split(r"\n(?=- id: )", text):
        if not block.strip().startswith("- id:"):
            continue
        entry_id = re.search(r"- id:\s*(\S+)", block)
        if not entry_id:
            continue
        class_m = re.search(r"class:\s*(\S+)", block)
        status_m = re.search(r"status:\s*(\S+)", block)
        title_m = re.search(r"title:\s*(.+)", block)
        verified_m = re.search(r"last_verified_at:\s*['\"]?([^'\"\n]+)", block)
        source_m = re.search(r"source_file:\s*(\S+)", block)
        entries.append(
            MemoryEntry(
                entry_id=entry_id.group(1),
                class_name=class_m.group(1) if class_m else "",
                status=status_m.group(1) if status_m else "",
                title=title_m.group(1).strip() if title_m else "",
                last_verified_at=verified_m.group(1).strip() if verified_m else "",
                source_file=source_m.group(1) if source_m else "",
            )
        )
    return entries


def pick_current_ids(
    entries: list[MemoryEntry],
    *,
    classes: set[str],
    source_files: set[str] | None = None,
    limit: int = 10,
) -> list[str]:
    filtered = [
        e
        for e in entries
        if e.status == "current" and e.class_name in classes
        and (source_files is None or e.source_file in source_files)
    ]
    filtered.sort(key=lambda e: (e.last_verified_at, e.entry_id), reverse=True)
    return [e.entry_id for e in filtered[:limit]]


def extract_checkpoint(current_state: str, heading: str) -> str:
    token = heading.lstrip("#").strip()
    if token not in current_state:
        return "missing evidence"
    section = current_state.split(heading, 1)[1].split("\n## ", 1)[0].strip()
    return "\n".join(line.strip() for line in section.splitlines() if line.strip())[:2000]


def extract_workstreams(working_state: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for match in re.finditer(
        r"- id:\s*([^\n]+)\n\s+status:\s*(\S+)\n\s+path:\s*([^\n]+)",
        working_state,
    ):
        rows.append(
            {
                "id": match.group(1).strip(),
                "status": match.group(2).strip(),
                "path": match.group(3).strip(),
            }
        )
    return rows


def _parse_current_task(working_state: str) -> dict[str, str | None]:
    block_match = re.search(r"current_task:\s*\n((?:\s+.+\n?)+)", working_state)
    block = block_match.group(1) if block_match else working_state
    task_id = re.search(r"^\s+id:\s*(\S+)", block, re.MULTILINE)
    summary = re.search(r"^\s+summary:\s*(.+)$", block, re.MULTILINE)
    summary_value = summary.group(1).strip().strip('"').strip("'") if summary else None
    return {
        "id": task_id.group(1) if task_id else None,
        "summary": summary_value,
    }


def parse_top_worklog_entry(text: str) -> dict[str, str] | None:
    current: dict[str, str] | None = None
    body_lines: list[str] = []
    for line in text.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            if current is not None and "priority" in current:
                current["body"] = "\n".join(body_lines).strip()
                return current
            current = {"title": heading.group("title").strip()}
            body_lines = []
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line)
        if field:
            label = field.group("label").strip().lower()
            if label in {"id", "priority", "status", "notes"}:
                current[label] = field.group("value").strip()
        else:
            body_lines.append(line)
    if current is not None and "priority" in current:
        current["body"] = "\n".join(body_lines).strip()
        return current
    return None


def build_context_pack_payload(cfg: ProjectConfig) -> dict[str, Any]:
    current_state = read_text(cfg.current_state)
    working_state = read_text(cfg.working_state)
    source_authority = read_text(cfg.source_authority)
    memory_index = read_text(cfg.memory_index)
    entries = parse_memory_index(memory_index)
    worklog_entry = None
    if cfg.worklog.is_file():
        worklog_entry = parse_top_worklog_entry(read_text(cfg.worklog))

    amk_state: dict[str, Any] = {
        "schema_version": yaml_scalar(working_state, "schema_version"),
        "kit_version": re.search(r"kit_version:\s*[\"']?([^\"'\n]+)", working_state),
        "map_schema_version": re.search(r"map_schema_version:\s*[\"']?([^\"'\n]+)", working_state),
        "replay_checkpoint_id": re.search(r"checkpoint_id:\s*(\S+)", working_state),
    }
    kit_from_state = re.search(r"Agent Memory Kit\s*\*\*([^*]+)\*\*", current_state)
    for key in ("kit_version", "replay_checkpoint_id", "map_schema_version"):
        match = amk_state[key]
        if hasattr(match, "group"):
            amk_state[key] = match.group(1).strip().strip('"').strip("'")
        elif key == "kit_version" and kit_from_state:
            amk_state[key] = kit_from_state.group(1).strip()
        else:
            amk_state[key] = None

    return {
        "source_latest_mtime": source_latest_mtime(cfg.context_input_paths),
        "checkpoint": extract_checkpoint(current_state, cfg.checkpoint_heading),
        "amk_state": amk_state,
        "repo_routing_boundary": cfg.repo_routing_boundary,
        "source_authority_summary": {
            "core_rule": yaml_scalar(source_authority, "core_rule"),
            "top_ranks": re.findall(r"- rank:\s*(\d+)\n\s+id:\s*(\S+)", source_authority)[:4],
        },
        "current_task": _parse_current_task(working_state),
        "memory_ids": {
            "facts_current": pick_current_ids(entries, classes={"fact_current"}, source_files={"facts.yaml"}),
            "decisions_current": pick_current_ids(
                entries, classes={"accepted_decision"}, source_files={"decisions.yaml"}
            ),
            "constraints_current": pick_current_ids(
                entries, classes={"constraint"}, source_files={"constraints.yaml"}
            ),
            "risks_current": pick_current_ids(entries, classes={"risk"}, source_files={"risks.yaml"}),
        },
        "active_workstreams": extract_workstreams(working_state),
        "top_worklog_entry": worklog_entry,
        "explicit_exclusions": EXPLICIT_EXCLUSIONS,
    }


def render_context_pack_md(payload: dict[str, Any]) -> str:
    lines = [
        "# GPT Context Pack (generated)",
        "",
        f"> **source_latest_mtime:** {payload.get('source_latest_mtime')} (UTC, max of input files)",
        "",
        "## Checkpoint",
        "",
        payload["checkpoint"],
        "",
        "## AMK adopted state",
        "",
        f"- schema_version: `{payload['amk_state'].get('schema_version')}`",
        f"- kit_version: `{payload['amk_state'].get('kit_version')}`",
        f"- map_schema_version: `{payload['amk_state'].get('map_schema_version')}`",
        f"- replay_checkpoint_id: `{payload['amk_state'].get('replay_checkpoint_id')}`",
        "",
        "## Repo routing boundary",
        "",
        payload["repo_routing_boundary"],
        "",
        "## Source authority summary",
        "",
        f"- core_rule: {payload['source_authority_summary'].get('core_rule')}",
        "- top authority ranks:",
    ]
    for rank, auth_id in payload["source_authority_summary"].get("top_ranks", []):
        lines.append(f"  - {rank}: `{auth_id}`")
    lines.extend(
        [
            "",
            "## current_task",
            "",
            f"- id: `{payload['current_task'].get('id')}`",
            f"- summary: {payload['current_task'].get('summary')}",
            "",
            "## Current memory IDs (from index scan)",
            "",
        ]
    )
    for key, label in (
        ("facts_current", "Facts"),
        ("decisions_current", "Decisions"),
        ("constraints_current", "Constraints"),
        ("risks_current", "Risks"),
    ):
        ids = payload["memory_ids"].get(key, [])
        lines.extend([f"### {label}", "", ", ".join(f"`{i}`" for i in ids) if ids else "_none_", ""])
    lines.extend(["## Active workstreams", ""])
    for ws in payload["active_workstreams"]:
        lines.append(f"- `{ws['id']}` ({ws['status']}): `{ws['path']}`")
    lines.extend(["", "## Top WORKLOG entry only", ""])
    entry = payload.get("top_worklog_entry")
    if entry:
        lines.append(f"### {entry.get('title', 'untitled')}")
        lines.append("")
        for key in ("id", "priority", "status", "notes"):
            if entry.get(key):
                lines.append(f"- **{key}:** {entry[key]}")
        if entry.get("body"):
            lines.extend(["", entry["body"][:1200]])
    else:
        lines.append("_No WORKLOG entry parsed._")
    lines.extend(["", "## Explicit exclusions", ""])
    lines.extend(f"- {item}" for item in payload["explicit_exclusions"])
    lines.append("")
    return "\n".join(lines)


def collect_desired_sources(cfg: ProjectConfig, include_optional: bool) -> list[FileMeta]:
    items: list[FileMeta] = []
    for path_str, purpose in cfg.required_sources:
        items.append(
            FileMeta(
                path=path_str,
                rel=(cfg.root / Path(path_str)),
                purpose=purpose,
                required=True,
                destination="project_source",
            )
        )
    if include_optional:
        for path_str, purpose in cfg.optional_sources:
            rel = cfg.root / Path(path_str)
            if rel.is_file():
                items.append(
                    FileMeta(
                        path=path_str,
                        rel=rel,
                        purpose=purpose,
                        required=False,
                        destination="project_source",
                    )
                )
    return items


def compute_actions(items: list[FileMeta], prev_map: dict[str, str]) -> None:
    current_paths = {item.path for item in items}
    for item in items:
        item.previous_sha256 = prev_map.get(item.path)
        if not item.exists:
            item.action = "MISSING"
        elif item.path not in prev_map:
            item.action = "ADD"
        elif item.sha256 == item.previous_sha256:
            item.action = "KEEP"
        else:
            item.action = "UPDATE"
    for path in sorted(set(prev_map) - current_paths):
        items.append(
            FileMeta(
                path=path,
                rel=Path(path),
                purpose="Previously tracked; no longer in desired set",
                required=False,
                destination="project_source",
                action="REMOVE",
                previous_sha256=prev_map[path],
            )
        )


def project_instructions_meta(cfg: ProjectConfig, previous_sha: str | None) -> dict[str, Any]:
    path = rel_posix(cfg, cfg.instructions_compact)
    ui_note = (
        "Copy this file manually into ChatGPT Project Instructions; "
        "generator cannot verify UI state."
    )
    if cfg.instructions_compact.is_file():
        sha, size, mtime = sha256_file(cfg.instructions_compact)
        action = "ADD" if previous_sha is None else "KEEP" if previous_sha == sha else "UPDATE"
        return {
            "status": "present",
            "path": path,
            "destination": "project_instructions",
            "required": False,
            "sha256": sha,
            "size_bytes": size,
            "mtime_iso": mtime,
            "purpose": "Compact ChatGPT Project Instructions (copy manually into UI)",
            "action": action,
            "previous_sha256": previous_sha,
            "ui_note": ui_note,
        }
    return {
        "status": "missing",
        "path": path,
        "destination": "project_instructions",
        "required": False,
        "sha256": None,
        "size_bytes": None,
        "mtime_iso": None,
        "purpose": "Compact ChatGPT Project Instructions (copy manually into UI)",
        "action": "MISSING",
        "previous_sha256": previous_sha,
        "ui_note": ui_note,
        "note": f"{path} not present in project",
    }


def _action_table(rows: list[FileMeta]) -> list[str]:
    out = [
        "| Action | File | Purpose | SHA256 (short) | Size |",
        "|--------|------|---------|----------------|------|",
    ]
    for row in rows:
        out.append(
            f"| {row.action} | `{row.path}` | {row.purpose} | "
            f"`{short_sha(row.sha256)}` | {row.size_bytes or '—'} |"
        )
    return out


def render_todo_md(
    run_meta: dict[str, Any],
    items: list[FileMeta],
    instructions: dict[str, Any],
    *,
    include_optional: bool,
) -> str:
    required_items = [i for i in items if i.required and i.action != "REMOVE"]
    optional_items = [i for i in items if not i.required and i.action != "REMOVE"]
    removed_items = [i for i in items if i.action == "REMOVE"]
    lines = [
        "# ChatGPT Project Sources — owner TODO",
        "",
        "Upload or update these files in your **ChatGPT Project** sources.",
        "",
        "> Actions are relative to the **previous local manifest**, not verified against the ChatGPT UI.",
        "> Previous kit release archives are not sources by default.",
        "",
        f"**manifest_generated_at:** {run_meta['generated_at']} (UTC)",
        f"**source_set:** {'minimal + optional granular' if include_optional else 'minimal required only'}",
        "",
        "## Project Instructions",
        "",
        instructions.get("ui_note", ""),
        "",
    ]
    if instructions.get("status") == "present":
        lines.append(
            f"- Tracked file: `{instructions['path']}` — manifest action **{instructions['action']}** "
            f"(sha `{short_sha(instructions.get('sha256'))}`)"
        )
        lines.append("- Paste the `text` block from that file into ChatGPT Project Instructions UI.")
    else:
        lines.append(f"- Tracked file missing: `{instructions['path']}`")
    lines.extend(["", "## Minimal project sources (required)", ""])
    lines.extend(_action_table(sorted(required_items, key=lambda i: i.path)) if required_items else ["_none_", ""])
    for section, pred in (
        ("ADD", lambda i: i.action == "ADD" and i.required),
        ("UPDATE", lambda i: i.action == "UPDATE" and i.required),
        ("KEEP", lambda i: i.action == "KEEP" and i.required),
        ("MISSING", lambda i: i.action == "MISSING" and i.required),
    ):
        rows = [i for i in items if pred(i)]
        lines.extend([f"### Required — {section}", ""])
        lines.extend(_action_table(sorted(rows, key=lambda i: i.path)) if rows else ["_none_", ""])
    if include_optional:
        lines.extend(
            [
                "## Optional granular sources",
                "",
                "Included because `--include-optional` was used.",
                "",
            ]
        )
        lines.extend(
            _action_table(sorted(optional_items, key=lambda i: i.path))
            if optional_items
            else ["_none present on disk_", ""]
        )
    lines.extend(["## REMOVE (from previous manifest)", ""])
    lines.extend(
        _action_table(sorted(removed_items, key=lambda i: i.path)) if removed_items else ["_none_", ""]
    )
    lines.extend(["## DO NOT UPLOAD", ""])
    lines.extend(f"- paths matching `{p}`" for p in FORBIDDEN_PATTERNS)
    lines.extend(["- `*.sha256` except generated `CHATGPT_PROJECT_SOURCES.sha256`", ""])
    return "\n".join(lines)


def write_outputs(cfg: ProjectConfig, include_optional: bool) -> dict[str, Any]:
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    payload = build_context_pack_payload(cfg)
    cfg.out_context_md.write_text(render_context_pack_md(payload), encoding="utf-8")
    cfg.out_context_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    previous = {}
    if cfg.out_manifest.is_file():
        previous = json.loads(read_text(cfg.out_manifest))
    prev_map = {
        item["path"]: item["sha256"]
        for item in previous.get("sources", [])
        if item.get("path") and item.get("sha256")
    }
    prev_instr = (previous.get("project_instructions") or {}).get("sha256")
    instructions = project_instructions_meta(cfg, prev_instr)

    items = collect_desired_sources(cfg, include_optional)
    for item in items:
        if item.rel.is_file():
            item.exists = True
            item.sha256, item.size_bytes, item.mtime_iso = sha256_file(item.rel)
    compute_actions(items, prev_map)

    run_meta = {"generated_at": run_generated_at()}
    manifest = {
        "generated_at": run_meta["generated_at"],
        "source_set": "minimal+optional" if include_optional else "minimal",
        "generator": GENERATOR_ID,
        "config_path": rel_posix(cfg, cfg.config_path),
        "project_instructions": instructions,
        "sources": [
            {
                "path": i.path,
                "destination": i.destination,
                "required": i.required,
                "sha256": i.sha256,
                "size_bytes": i.size_bytes,
                "mtime_iso": i.mtime_iso,
                "purpose": i.purpose,
                "action": i.action,
                "previous_sha256": i.previous_sha256,
            }
            for i in sorted(items, key=lambda x: x.path)
        ],
    }
    cfg.out_manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cfg.out_todo.write_text(
        render_todo_md(run_meta, items, instructions, include_optional=include_optional),
        encoding="utf-8",
    )
    sha_lines = []
    if instructions.get("sha256"):
        sha_lines.append(f"{instructions['sha256']}  {instructions['path']}")
    for item in sorted(items, key=lambda i: i.path):
        if item.exists and item.sha256 and item.action != "REMOVE":
            sha_lines.append(f"{item.sha256}  {item.path}")
    cfg.out_sha256.write_text("\n".join(sha_lines) + ("\n" if sha_lines else ""), encoding="utf-8")
    return {"run_meta": run_meta, "items": items, "instructions": instructions, "payload": payload}


def check_outputs(cfg: ProjectConfig) -> int:
    errors: list[str] = []
    outputs = [
        cfg.out_context_md,
        cfg.out_context_json,
        cfg.out_todo,
        cfg.out_manifest,
        cfg.out_sha256,
    ]
    for path in outputs:
        if not path.is_file():
            errors.append(f"missing output: {rel_posix(cfg, path)}")
    for path in outputs:
        if path.suffix == ".json" and path.is_file():
            json.loads(read_text(path))
    for path_str, _ in cfg.required_sources:
        if not (cfg.root / path_str).is_file():
            errors.append(f"missing required source: {path_str}")
    if cfg.out_manifest.is_file():
        manifest = json.loads(read_text(cfg.out_manifest))
        paths = [s.get("path", "") for s in manifest.get("sources", [])]
        instr = manifest.get("project_instructions") or {}
        if instr.get("path"):
            paths.append(instr["path"])
        for path in paths:
            if is_forbidden_path(path):
                errors.append(f"forbidden tracked path: {path}")
    if errors:
        for err in errors:
            print(f"CHECK FAIL: {err}")
        return 1
    print("CHECK OK")
    return 0


def summarize(result: dict[str, Any], cfg: ProjectConfig) -> None:
    actions: dict[str, int] = {}
    missing = []
    for item in result["items"]:
        actions[item.action] = actions.get(item.action, 0) + 1
        if item.action == "MISSING" and item.required:
            missing.append(item.path)
    content_actions = {
        i.action for i in result["items"] if i.action in {"ADD", "UPDATE", "REMOVE", "MISSING"}
    }
    instr = result["instructions"].get("action")
    print("SUMMARY")
    print(f"  manifest_generated_at: {result['run_meta']['generated_at']}")
    print(f"  required_sources: {sum(1 for i in result['items'] if i.required and i.action != 'REMOVE')}")
    print(f"  actions: {actions}")
    print(f"  missing required: {missing or 'none'}")
    print(f"  instructions: {result['instructions'].get('status')} / {instr}")
    print(f"  chatgpt_source_update_needed: {bool(content_actions) or instr in {'ADD', 'UPDATE', 'MISSING'}}")
    print(f"  todo: {rel_posix(cfg, cfg.out_todo)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to CHATGPT_PROJECT_SOURCES.config.json")
    parser.add_argument("--project-root", help="Override project root")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--include-optional", action="store_true")
    parser.add_argument("--no-optional", action="store_true")
    args = parser.parse_args()
    if not args.write and not args.check:
        parser.error("specify --write and/or --check")

    cfg = load_config(Path(args.config), Path(args.project_root) if args.project_root else None)
    include_optional = args.include_optional and not args.no_optional
    result = None
    if args.write:
        result = write_outputs(cfg, include_optional)
        summarize(result, cfg)
    if args.check:
        return check_outputs(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
