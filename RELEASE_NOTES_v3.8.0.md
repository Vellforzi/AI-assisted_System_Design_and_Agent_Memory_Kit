# Agent Memory Kit v3.8.0 - Cursor Settings and Ignore Boundary Release

This release adds the Cursor Agent settings layer and ignore-file context-boundary layer that were missing from the previous Cursor/Codex Integration Packs.

The main purpose of v3.8.0 is to make the recommended Cursor configuration explicit, auditable, and aligned with the kit's owner-controlled workflow.

## Highlights

- Adds a Cursor Agent settings profile for owner-controlled projects.
- Adds a machine-readable Cursor settings profile.
- Adds settings audit, `.cursorignore` audit, and `.codexignore` audit command templates.
- Adds `.cursorignore` context-boundary guidance and safe default templates.
- Adds `.codexignore` context-boundary guidance and safe default templates.
- Adds `desktop.ini` ignore patterns for Windows / Google Drive project trees.
- Adds the authoritative existing workspace rule: use the existing project workspace referenced by Project Map or `AGENTS.md`; do not replace it with a generated fallback.
- Adds eval cases for Cursor settings, workspace authority, ignore files, and submodule behavior.

## Added

- `Agent Kit/kit/CURSOR_AGENT_SETTINGS_GUIDE.md`
- `Agent Kit/kit/CURSORIGNORE_AND_CONTEXT_BOUNDARY_GUIDE.md`
- `Agent Kit/kit/CODEXIGNORE_AND_CONTEXT_BOUNDARY_GUIDE.md`
- `Agent Kit/kit/cursor/CURSOR_OWNER_CONTROLLED_DEFAULTS.md`
- `Agent Kit/kit/cursor/settings/owner_controlled_profile.yaml`
- `Agent Kit/kit/cursor/settings/option_profit_current_profile.yaml`
- `Agent Kit/kit/cursor/context/.cursorignore.safe-default`
- `Agent Kit/kit/cursor/context/.cursorignore.option-profit-default`
- `Agent Kit/kit/cursor/commands/settings-audit.md`
- `Agent Kit/kit/cursor/commands/cursorignore-audit.md`
- `Agent Kit/kit/cursor/commands/codexignore-audit.md`
- `Agent Kit/kit/codex/ignore/README.md`
- `Agent Kit/kit/codex/ignore/.codexignore.safe-default`
- `Agent Kit/kit/codex/ignore/.codexignore.option-profit-default`

## Updated

- `Agent Kit/kit/WORKSPACE_SELECTION_GUIDE.md`
- `Agent Kit/kit/CURSOR_INTEGRATION_OWNER_GUIDE.md`
- `Agent Kit/kit/CODEX_INTEGRATION_OWNER_GUIDE.md`
- `Agent Kit/kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md`
- `Agent Kit/kit/AGENTS.md_TEMPLATE.md`
- `Agent Kit/kit/CURSOR_RULE_TEMPLATE.mdc`
- `Agent Kit/kit/cursor/README.md`
- `Agent Kit/kit/cursor/COMMAND_VOCABULARY.md`
- `Agent Kit/kit/cursor/workspaces/README.md`
- `Agent Kit/kit/eval_suite/core_behavior_eval_cases.yaml`
- `Agent Kit/kit/eval_suite/eval_manifest.yaml`
- package README, START_HERE, MANIFEST, and SHA256SUMS

## Recommended Cursor default

Cursor should be treated as the primary local implementation agent, but not as an unrestricted autonomous worker.

Key defaults:

- Run Mode: Auto-review or stricter; not Run Everything.
- Submit with Ctrl + Enter: on.
- Max Tab Count: 5.
- Usage Summary: always visible.
- Auto-Approve Mode Transitions: off.
- Web Search: on, but Auto-Accept Web Search off.
- Web Fetch: on.
- Browser Protection: on.
- File-Deletion Protection: on.
- External-File Protection: on.
- MCP Tools Protection: on where available.
- Auto Format on Agent Finish: off.
- Include Untracked Files in Agent Review: on.
- Include Submodules in Agent Review: off unless `.gitmodules` exists.
- Hierarchical Cursor Ignore: on only after root `.cursorignore` is verified.
- Ignore Symlinks in Cursor Ignore Search: off unless required by project topology.

## Ignore-file boundary

Ignore files reduce context noise. They are not a security boundary.

The recommended root ignore files are:

```text
.cursorignore
.codexignore
```

Both should include:

```text
**/desktop.ini
```

Do not hide Project Map, AGENTS.md, source authority, docs, or active component source files.

## Known boundary

Cursor settings, Codex settings, and ignore files are not substitutes for Project Map, task contracts, source authority, hooks, git review, or owner approval.

Agent Memory Kit remains file-based and language-agnostic. Optional Python helper scripts are examples only.
