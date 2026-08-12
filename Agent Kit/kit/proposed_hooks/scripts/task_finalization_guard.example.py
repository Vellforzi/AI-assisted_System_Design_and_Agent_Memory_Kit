#!/usr/bin/env python3
"""Task finalization guard (example).

Stop/complete cannot claim verified delivery from compile or writer
self-PASS alone. See ../README.md.
"""
from __future__ import annotations

import json
import re
import sys

PLAYBOOK = "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"
DONE = re.compile(
    r"\b(verified delivery|SMOKE_PASS|task complete|delivery_candidate)\b",
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
                "allowedNextActions": ["attach named receipts", "report incomplete"],
                "forbiddenNextActions": [
                    "claim done from compile only",
                    "treat writer PASS as owner smoke",
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
    blob = json.dumps(data)
    if not DONE.search(blob):
        print(json.dumps({"continue": True, "permission": "allow"}))
        return 0
    if not re.search(r"(receipt|oracle|owner.smoke|journal_forensic)", blob, re.I):
        return deny(
            "FINALIZATION_WITHOUT_RECEIPT",
            "Completion language without named receipts or oracles.",
            "Bind the named evidence (oracle, hash, forensic, owner smoke) or do not claim done.",
        )
    print(json.dumps({"continue": True, "permission": "allow"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
