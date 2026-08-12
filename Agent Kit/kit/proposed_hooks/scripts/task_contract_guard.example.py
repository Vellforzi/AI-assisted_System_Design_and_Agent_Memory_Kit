#!/usr/bin/env python3
"""Task contract guard (example).

Mutating apply/stage/map-apply needs a plain contract file. A hybrid
prose+YAML paste is narrative only. See ../README.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PLAYBOOK = "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"
MUTATING = ("/apply", "/stage", "/map-apply", "mode: apply", "mode: stage")


def deny(code: str, why: str, required: str) -> int:
    print(
        json.dumps(
            {
                "continue": False,
                "permission": "deny",
                "violationCode": code,
                "whyBlocked": why,
                "requiredNextResponse": required,
                "allowedNextActions": [
                    "materialize CONTRACT.yaml in the same task",
                    "answer/analyze without mutation",
                ],
                "forbiddenNextActions": [
                    "pass a .bootstrap.txt hybrid as --contract",
                    "open a recovery task for hybrid input",
                ],
                "playbook": PLAYBOOK,
            },
            ensure_ascii=False,
        )
    )
    return 2


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    blob = json.dumps(data).lower()
    mutating = any(token in blob for token in MUTATING)
    if not mutating:
        print(json.dumps({"continue": True, "permission": "allow"}))
        return 0
    prompt = str(data.get("prompt") or data.get("user_prompt") or "")
    if ".bootstrap.txt" in prompt.lower() and "contract.yaml" not in prompt.lower():
        return deny(
            "HYBRID_BOOTSTRAP_NOT_CONTRACT",
            "Hybrid prose+YAML bootstrap is narrative only.",
            "Materialize a plain CONTRACT.yaml with both gates in this same task, then retry.",
        )
    print(json.dumps({"continue": True, "permission": "allow"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
