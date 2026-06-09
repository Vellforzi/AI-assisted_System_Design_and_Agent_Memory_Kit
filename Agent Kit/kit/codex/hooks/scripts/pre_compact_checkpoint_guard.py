#!/usr/bin/env python3
"""Stop automatic Codex compaction until the owner creates a checkpoint or handoff."""
import json
import os
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

trigger = str(data.get("trigger", "")).lower()
allow = os.getenv("ALLOW_CODEX_COMPACT", "").lower() in {"1", "true", "yes"}

if trigger == "auto" and not allow:
    print(json.dumps({
        "continue": False,
        "stopReason": "Automatic context compaction blocked by Agent Memory Kit.",
        "systemMessage": (
            "Automatic compaction was blocked. Create a checkpoint or handoff first. "
            "Do not promote compressed chat history into Project Map. Resume from Project Map, "
            "Working State, Source Authority, and approved task/checkpoint/handoff."
        )
    }))
    sys.exit(0)

print(json.dumps({
    "continue": True,
    "systemMessage": "Manual compaction allowed only if a checkpoint/handoff already exists."
}))
