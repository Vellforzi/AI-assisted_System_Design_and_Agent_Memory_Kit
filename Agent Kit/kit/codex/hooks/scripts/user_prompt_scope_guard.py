#!/usr/bin/env python3
"""Block changing prompts that do not include explicit scope."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

prompt = str(data.get("prompt", ""))
low = prompt.lower()

changing_intent = bool(re.search(
    r"\b(/apply|/map-apply|edit|modify|update|write|delete|remove|rename|move|refactor|fix|implement|apply|change|create file|rewrite)\b",
    low,
))
project_map_intent = "project map" in low or "/map-apply" in low
has_scope = "scope:" in low or "allowed:" in low or "allowed paths:" in low
explicit_answer_only = any(x in low for x in ["/answer", "answer only", "read-only", "analyze only", "plan only"])

if changing_intent and not explicit_answer_only and not has_scope:
    print(json.dumps({
        "decision": "block",
        "reason": (
            "Changing action requested without explicit scope. Use a task contract with Mode, Scope, "
            "Allowed, Forbidden, and Verification. Questions and analysis do not authorize changes."
        )
    }))
    sys.exit(0)

if project_map_intent and "/map-apply" not in low and "project map delta" not in low and "map-delta" not in low:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "Project Map updates require explicit /map-apply or an owner-approved Project Map delta. "
                "In answer/analyze/plan mode, propose updates only."
            )
        }
    }))
    sys.exit(0)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": (
            "Agent Memory Kit reminder: default intent is answer-only; platform summaries are non-authoritative."
        )
    }
}))
