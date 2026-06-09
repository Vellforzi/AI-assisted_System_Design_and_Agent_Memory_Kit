#!/usr/bin/env python3
"""Warn after compaction that platform summaries are not project truth."""
import json
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

trigger = data.get("trigger", "unknown")
print(json.dumps({
    "continue": False,
    "stopReason": f"Context compaction detected: {trigger}.",
    "systemMessage": (
        "Context compaction has occurred. Treat compressed history as a non-authoritative hint only. "
        "Before continuing, recover from Project Map, working_state.yaml, source_authority.yaml, "
        "active task contract, and approved memory units."
    )
}))
