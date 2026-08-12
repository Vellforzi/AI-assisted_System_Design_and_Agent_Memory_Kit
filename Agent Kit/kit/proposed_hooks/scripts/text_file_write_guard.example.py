#!/usr/bin/env python3
"""Encoding / host-write guard (example).

Block project text writes through PowerShell Set-Content/Out-File and
direct file-association script launches. That is harness, not product.
See ../README.md.
"""
from __future__ import annotations

import json
import re
import sys

PLAYBOOK = "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"
BAD = re.compile(
    r"("
    r"Set-Content|Add-Content|Out-File|"
    r"\bcmd\s+/c\s+.*\.(py|ps1|cmd|bat)\b|"
    r"(?:^|[;&|])\s*(?:[A-Za-z]:)?[^\s\"']+\.(py|ps1|cmd|bat)(?:\s|$)"
    r")",
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
                "allowedNextActions": [
                    "use the structured editor",
                    "use the registered interpreter with quoted argv",
                ],
                "forbiddenNextActions": [
                    "PowerShell redirection for project files",
                    "file-association launch of scripts",
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
    tool_input = data.get("tool_input") or {}
    command = str(tool_input.get("command") or data.get("command") or "")
    if BAD.search(command):
        return deny(
            "UNSAFE_HOST_WRITE",
            "Command would write or launch via an encoding-unsafe host path.",
            "Use the structured editor or the registered interpreter with structured argv.",
        )
    print(json.dumps({"continue": True, "permission": "allow"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
