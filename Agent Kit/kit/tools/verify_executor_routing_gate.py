#!/usr/bin/env python3
"""Verify Executor Routing Gate blocks in task contracts/bootstrap artifacts.

This helper is file-read-only. It can be used by reviewers, hooks, or release
checks to ensure non-trivial contracts include the required routing gate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "recommended_executor",
    "confidence",
    "why_this_executor",
    "why_not_default_executor",
    "evidence_used",
    "escalation_trigger",
    "stop_or_owner_gate",
)

VALID_CONFIDENCE = {"high", "medium", "low"}
VIOLATION_MISSING = "EXECUTOR_ROUTING_GATE_MISSING"
VIOLATION_MALFORMED = "EXECUTOR_ROUTING_GATE_MALFORMED"

EXCLUDED_SUFFIXES = (
    ".result.md",
    ".handoff.md",
    ".log.md",
    ".validation.json",
)
EXCLUDED_FILENAMES = {"orchestration_log.jsonl"}
EXCLUDED_DIR_MARKERS = ("/reports/", "/inventory/", "/generated/", "/gpt/")

GATE_HEADER_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?Executor Routing Gate\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

FIELD_RE = re.compile(
    r"^\s*(recommended_executor|confidence|why_this_executor|why_not_default_executor|"
    r"evidence_used|escalation_trigger|stop_or_owner_gate)\s*:\s*(.*)$",
    re.IGNORECASE,
)


def norm_posix(path: str | Path) -> str:
    return str(path).replace("\\", "/").lstrip("./")


def is_excluded_path(path: str | Path, *, strict: bool = False) -> bool:
    rel = norm_posix(path)
    name = Path(rel).name
    if name in EXCLUDED_FILENAMES:
        return True
    if any(rel.endswith(suffix) for suffix in EXCLUDED_SUFFIXES):
        return True
    if strict:
        return False
    low = rel.lower()
    return any(marker in low for marker in EXCLUDED_DIR_MARKERS)


def is_check_target(path: str | Path, *, strict: bool = False) -> bool:
    rel = norm_posix(path)
    if is_excluded_path(rel, strict=strict):
        return False
    if rel.endswith(".cursor-bootstrap"):
        return True
    if "/agent-tools/tasks/" in rel or rel.startswith("agent-tools/tasks/"):
        return rel.endswith(".md")
    if "/tasks/" in rel or rel.startswith("tasks/"):
        return rel.endswith((".md", ".yaml", ".yml"))
    return False


def _section_end_line(lines: list[str], start_idx: int) -> int:
    start_line = lines[start_idx]
    heading = re.match(r"^(#{1,6})\s+", start_line)
    start_level = len(heading.group(1)) if heading else 0
    for idx in range(start_idx + 1, len(lines)):
        next_heading = re.match(r"^(#{1,6})\s+", lines[idx])
        if not next_heading:
            continue
        if start_level == 0 or len(next_heading.group(1)) <= start_level:
            return idx
    return len(lines)


def parse_executor_routing_gate(content: str) -> dict[str, Any]:
    lines = (content or "").splitlines()
    start_idx = None
    for idx, line in enumerate(lines):
        if GATE_HEADER_RE.match(line):
            start_idx = idx
            break
    if start_idx is None:
        return {
            "present": False,
            "fields": {},
            "missing_fields": list(REQUIRED_FIELDS),
            "malformed_fields": [],
            "reason": "Executor Routing Gate section not found",
            "valid": False,
        }

    section_lines = lines[start_idx + 1 : _section_end_line(lines, start_idx)]
    fields: dict[str, str] = {}
    current_field = ""
    for raw in section_lines:
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("```"):
            continue
        match = FIELD_RE.match(line)
        if match:
            current_field = match.group(1).lower()
            fields[current_field] = match.group(2).strip()
            continue
        if current_field and re.match(r"^\s*-\s+", line):
            item = re.sub(r"^\s*-\s+", "", line).strip()
            if item:
                prev = fields.get(current_field, "")
                fields[current_field] = f"{prev}\n{item}".strip() if prev else item
            continue
        if current_field and line.startswith((" ", "\t")) and not FIELD_RE.match(line):
            extra = line.strip()
            if extra:
                prev = fields.get(current_field, "")
                fields[current_field] = f"{prev} {extra}".strip() if prev else extra

    missing = [field for field in REQUIRED_FIELDS if not fields.get(field, "").strip()]
    malformed: list[str] = []
    confidence = fields.get("confidence", "").strip().lower()
    if confidence and confidence not in VALID_CONFIDENCE:
        malformed.append(f"confidence must be one of {sorted(VALID_CONFIDENCE)}")
    reason = f"missing fields: {', '.join(missing)}" if missing else "; ".join(malformed)
    return {
        "present": True,
        "fields": fields,
        "missing_fields": missing,
        "malformed_fields": malformed,
        "reason": reason,
        "valid": not missing and not malformed,
    }


def validate_content(path: str | Path, content: str, *, strict: bool = False) -> dict[str, Any] | None:
    rel = norm_posix(path)
    if not is_check_target(rel, strict=strict):
        return None
    parsed = parse_executor_routing_gate(content)
    if parsed["valid"]:
        return None
    code = VIOLATION_MISSING if parsed["missing_fields"] or not parsed["present"] else VIOLATION_MALFORMED
    return {
        "path": rel,
        "reason": parsed["reason"] or "Executor Routing Gate block is missing or incomplete",
        "missing_fields": parsed["missing_fields"],
        "malformed_fields": parsed.get("malformed_fields", []),
        "violation_code": code,
    }


def validate_file(path: Path, *, strict: bool = False) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return {
            "path": norm_posix(path),
            "reason": "file not found",
            "missing_fields": list(REQUIRED_FIELDS),
            "malformed_fields": [],
            "violation_code": VIOLATION_MISSING,
        }
    return validate_content(path, path.read_text(encoding="utf-8", errors="replace"), strict=strict)


def collect_paths(paths: list[str], *, strict: bool = False) -> list[Path]:
    collected: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            collected.extend(candidate for candidate in sorted(path.rglob("*")) if candidate.is_file())
        elif path.is_file():
            collected.append(path)
    dedup: dict[str, Path] = {}
    for item in collected:
        if is_check_target(item, strict=strict):
            dedup[norm_posix(item)] = item
    return list(dedup.values())


def validate_paths(paths: list[str], *, strict: bool = False) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    checked: list[str] = []
    for path in collect_paths(paths, strict=strict):
        checked.append(norm_posix(path))
        failure = validate_file(path, strict=strict)
        if failure:
            failures.append(failure)
    return {"status": "pass" if not failures else "fail", "checked": checked, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Executor Routing Gate blocks.")
    parser.add_argument("--path", action="append", default=[], help="File or directory to check")
    parser.add_argument("--stdin", action="store_true", help="Read content from stdin; requires one --path logical name")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--strict", action="store_true", help="Validate stricter path classes")
    args = parser.parse_args()

    if args.stdin:
        if len(args.path) != 1:
            print("ERROR: --stdin requires exactly one --path logical name", file=sys.stderr)
            return 2
        failure = validate_content(args.path[0], sys.stdin.read(), strict=args.strict)
        result = {"status": "pass" if failure is None else "fail", "checked": [args.path[0]], "failures": [] if failure is None else [failure]}
    else:
        if not args.path:
            print("ERROR: at least one --path is required", file=sys.stderr)
            return 2
        result = validate_paths(args.path, strict=args.strict)

    if args.json:
        print(json.dumps(result, indent=2))
    elif result["status"] == "pass":
        print("PASS: Executor Routing Gate checks passed")
    else:
        print("FAIL: Executor Routing Gate checks failed")
        for failure in result["failures"]:
            print(f"- {failure['path']}: {failure['reason']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
