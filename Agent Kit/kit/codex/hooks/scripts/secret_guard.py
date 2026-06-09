#!/usr/bin/env python3
"""Block obvious secret access patterns."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

tool_input = data.get("tool_input") or {}
blob = json.dumps(tool_input, ensure_ascii=False).lower()

patterns = [
    r"\.env(\.|$|\s)",
    r"id_rsa",
    r"private[_-]?key",
    r"secrets?\.(json|yaml|yml|toml)",
    r"credentials?\.(json|yaml|yml|toml)",
    r"access[_-]?token",
    r"api[_-]?key",
    r"password",
]

if any(re.search(p, blob) for p in patterns):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Potential secret access blocked by Agent Memory Kit. Do not read or expose secrets. "
                "Ask the owner for a sanitized value or use documented secret references only."
            )
        }
    }))
    sys.exit(0)

print(json.dumps({}))
