#!/usr/bin/env python3
"""Guard owner prompts for intent/scope and inject generic AMK reminders."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

prompt = str(data.get("prompt", ""))
low = prompt.lower()
PLAYBOOK = "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"


def block_payload(code, why, required_next_response, allowed_next_actions, forbidden_next_actions):
    return {
        "decision": "block",
        "violation_code": code,
        "why_blocked": why,
        "reason": why,
        "required_next_response": required_next_response,
        "allowed_next_actions": allowed_next_actions,
        "forbidden_next_actions": forbidden_next_actions,
        "playbook": PLAYBOOK,
    }

changing_intent = bool(re.search(
    r"\b(/apply|/map-apply|edit|modify|update|write|delete|remove|rename|move|refactor|fix|implement|apply|change|create file|rewrite)\b",
    low,
))
project_map_intent = "project map" in low or "/map-apply" in low
has_scope = "scope:" in low or "allowed:" in low or "allowed paths:" in low
explicit_answer_only = any(x in low for x in ["/answer", "answer only", "read-only", "analyze only", "plan only"])

if changing_intent and not explicit_answer_only and not has_scope:
    print(json.dumps(block_payload(
        "MISSING_APPLY_SCOPE",
        "Changing action requested without explicit scope.",
        (
            "Blocked: changing work was requested without an explicit scope. I need Mode, "
            "Allowed, Forbidden, Evidence to read, Stop condition, and Verification before editing or executing."
        ),
        ["ask owner for a task contract", "answer/analyze without mutation"],
        ["edit files", "run mutating commands", "infer scope from prior chat"],
    )))
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
            "Agent Memory Kit reminder: default intent is answer-only; platform summaries are non-authoritative. "
            "Use only current owner scope, repository instructions, Project Map core files, active task evidence, "
            "and current tool output. /answer and /analyze may read/search within scope, but they do not authorize "
            "mutations or side effects."
        )
    }
}))
