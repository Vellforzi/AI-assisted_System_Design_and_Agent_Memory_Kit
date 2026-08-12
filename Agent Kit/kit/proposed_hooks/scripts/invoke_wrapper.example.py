#!/usr/bin/env python3
"""Fail-closed invoke wrapper (example).

Empty stdout or a crash is a deny, not a pass. Copy into the adopting
project and point hooks.json at this file. See ../README.md.
"""
from __future__ import annotations

import json
import subprocess
import sys

PLAYBOOK = "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"


def deny(code: str, why: str, required: str) -> int:
    print(
        json.dumps(
            {
                "continue": False,
                "permission": "deny",
                "violationCode": code,
                "whyBlocked": why,
                "requiredNextResponse": required,
                "allowedNextActions": ["repair hook", "retry"],
                "forbiddenNextActions": ["treat empty stdout as pass", "bypass failClosed"],
                "playbook": PLAYBOOK,
            },
            ensure_ascii=False,
        )
    )
    return 2


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return deny(
            "HOOK_WRAPPER_NO_EVENT",
            "Invoke wrapper received no event name.",
            "Pass the hook event as argv[1], then the inner command.",
        )
    inner = argv[2:]
    if not inner:
        return deny(
            "HOOK_WRAPPER_NO_INNER",
            "Invoke wrapper has no inner guard command.",
            "Configure hooks.json to call this wrapper with an inner script.",
        )
    try:
        proc = subprocess.run(inner, capture_output=True, text=True, check=False)
    except OSError as exc:
        return deny(
            "HOOK_WRAPPER_SPAWN_FAILED",
            f"Inner hook failed to start: {exc}",
            "Verify the registered interpreter and inner script path.",
        )
    out = (proc.stdout or "").strip()
    if proc.returncode == 0 and not out:
        return deny(
            "HOOK_EMPTY_STDOUT",
            "Blocking hook returned success with empty stdout.",
            "Repair the inner hook to emit a JSON verdict; do not treat silence as pass.",
        )
    if out:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return proc.returncode if proc.returncode != 0 else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
