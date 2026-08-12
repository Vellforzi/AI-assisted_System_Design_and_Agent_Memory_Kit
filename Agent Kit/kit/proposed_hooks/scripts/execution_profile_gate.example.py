#!/usr/bin/env python3
"""Execution profile gate (example).

R1-R4 mutating work must name mode, task class, and path zone. Zero or
several equal matches is a deny. See ../README.md.
"""
from __future__ import annotations

import json
import re
import sys

PLAYBOOK = "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"
NEEDLE = re.compile(
    r"(/apply|/stage|/map-apply|risk_tier\s*:\s*R[1-4])",
    re.I,
)


def deny(code: str, why: str, required: str) -> int:
    print(
        json.dumps(
            {
                "continue": False,
                "permission": "deny",
                "violationCode": code,
                "whyBlocked": why,
                "requiredNextResponse": required,
                "allowedNextActions": ["add Execution Profile Gate block", "answer-only"],
                "forbiddenNextActions": ["mutate without a unique route"],
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
    blob = json.dumps(data)
    if not NEEDLE.search(blob):
        print(json.dumps({"continue": True, "permission": "allow"}))
        return 0
    if not re.search(r"execution profile gate|execution_profile_gate", blob, re.I):
        return deny(
            "MISSING_EXECUTION_PROFILE_GATE",
            "R1-R4 mutating work has no Execution Profile Gate.",
            "Name mode, task class, path zone, toolchain, and write lock; resolve exactly one route.",
        )
    print(json.dumps({"continue": True, "permission": "allow"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
