#!/usr/bin/env python3
"""Block Project Map writes unless the owner explicitly allows them."""
import json
import os
import sys
from pathlib import Path

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

tool = str(data.get("tool_name", ""))
tool_input = data.get("tool_input") or {}
blob = json.dumps(tool_input, ensure_ascii=False).lower()
cwd = Path(data.get("cwd") or os.getcwd())

allow = os.getenv("ALLOW_PROJECT_MAP_WRITE", "").lower() in {"1", "true", "yes"}
allow = allow or (cwd / ".codex" / "ALLOW_PROJECT_MAP_WRITE").exists()

touches_project_map = "project map" in blob or "project_map" in blob or "working_state.yaml" in blob or "source_authority.yaml" in blob
edit_tool = tool.lower() in {"apply_patch", "edit", "write", "bash"}

if edit_tool and touches_project_map and not allow:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Project Map write blocked. Use /map-apply with explicit owner approval, "
                "or create .codex/ALLOW_PROJECT_MAP_WRITE for this controlled run."
            )
        }
    }))
    sys.exit(0)

print(json.dumps({}))
