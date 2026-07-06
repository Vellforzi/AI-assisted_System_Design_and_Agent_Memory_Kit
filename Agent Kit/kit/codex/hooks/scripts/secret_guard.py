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
event_name = data.get("hook_event_name") or data.get("hookEventName") or "PreToolUse"
PLAYBOOK = "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"

patterns = [
    r"\.env([\.\\/\s'\"\}:]|$)",
    r"id_rsa",
    r"private[_-]?key",
    r"secrets?\.(json|yaml|yml|toml)",
    r"credentials?\.(json|yaml|yml|toml)",
    r"access[_-]?token",
    r"api[_-]?key",
    r"password",
]

if any(re.search(p, blob) for p in patterns):
    why = "Potential secret access matched a blocked pattern."
    required = (
        "Do not read, expose, or reuse secret values. Ask the owner for a sanitized value "
        "or a current-task explicit credential allowance with credential, purpose, target, and action."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Potential secret access blocked by Agent Memory Kit. Do not read or expose secrets. "
                "Ask the owner for a sanitized value or use documented secret references only."
            ),
            "violationCode": "SECRET_ACCESS_BLOCKED",
            "whyBlocked": why,
            "requiredNextResponse": required,
            "allowedNextActions": [
                "ask owner for sanitized value",
                "ask owner for explicit current-task credential allowance",
                "continue without secret access",
            ],
            "forbiddenNextActions": [
                "read secret payloads",
                "print secrets",
                "reuse credentials for a new action without current allowance",
                "broaden secret scope silently",
            ],
            "playbook": PLAYBOOK,
        }
    }))
    sys.exit(0)

print(json.dumps({}))
