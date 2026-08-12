#!/usr/bin/env python3
"""Portable structural validator for AMK Execution Profile Gate blocks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


FIELDS = (
    "task_id", "mode", "task_class", "path_zone", "execution_profile",
    "toolchain_profile", "scope_profile", "worktree", "baseline_ref",
    "scope_lease", "source_write_authorization", "canonical_launcher",
    "verification_profile", "stop_or_escalation",
)
HEADER = re.compile(r"^\s*(?:#{1,6}\s*)?Execution Profile Gate\s*:?\s*$", re.I | re.M)
FIELD = re.compile(r"^\s*(" + "|".join(FIELDS) + r")\s*:\s*(.*)$", re.I)


def validate(content: str) -> dict:
    lines = content.splitlines()
    start = next((index for index, line in enumerate(lines) if HEADER.match(line)), None)
    if start is None:
        return {"valid": False, "missing_fields": list(FIELDS), "reason": "gate not found"}
    values = {}
    for line in lines[start + 1:]:
        if re.match(r"^#{1,6}\s+", line):
            break
        match = FIELD.match(line)
        if match:
            values[match.group(1).lower()] = match.group(2).strip()
    missing = [name for name in FIELDS if not values.get(name)]
    malformed = []
    if values.get("baseline_ref") and not re.fullmatch(r"[0-9a-fA-F]{40}", values["baseline_ref"]):
        malformed.append("baseline_ref must be a full 40-character Git object id")
    mode = values.get("mode", "").strip().replace("-", "_").casefold()
    authorization = values.get("source_write_authorization", "").strip().casefold()
    if mode in {"apply", "map_apply"} and not re.search(r"\bowner(?:_|\b)", authorization):
        malformed.append("apply/map_apply source_write_authorization must reference current owner authorization")
    return {"valid": not missing and not malformed, "fields": values, "missing_fields": missing, "malformed": malformed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    content = sys.stdin.read() if args.stdin else Path(args.path).read_text(encoding="utf-8", errors="replace")
    result = validate(content)
    result["path"] = args.path
    result["status"] = "pass" if result["valid"] else "fail"
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["status"].upper())
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
