#!/usr/bin/env python3
"""Deny dangerous shell commands before execution."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

tool = str(data.get("tool_name", ""))
tool_input = data.get("tool_input") or {}
command = str(tool_input.get("command", tool_input))
low = command.lower()

patterns = [
    r"\bgit\s+push\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\b",
    r"\brm\s+-rf\b",
    r"\bdel\s+/[fsq]\b",
    r"\bdrop\s+database\b",
    r"\bdrop\s+table\b",
    r"\btruncate\s+table\b",
    r"\balter\s+table\b",
    r"\bdelete\s+from\b",
    r"\bupdate\s+\w+\s+set\b",
    r"\binsert\s+into\b",
    r"\bpsql\b",
    r"\balembic\s+upgrade\b",
    r"\bdocker\s+compose\s+down\b",
    r"\bdocker\s+system\s+prune\b",
    r"\bkubectl\s+delete\b",
]

if tool.lower() in {"bash", "shell"} and any(re.search(p, low) for p in patterns):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Blocked by Agent Memory Kit: dangerous command requires explicit owner approval, "
                "a task contract, and a safer execution plan."
            )
        }
    }))
    sys.exit(0)

print(json.dumps({}))
