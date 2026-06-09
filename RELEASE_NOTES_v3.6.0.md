# Agent Memory Kit v3.6.0 — Codex Integration Pack Release

This release adds a Codex Integration Pack for using OpenAI Codex alongside Cursor under the same owner-controlled Project Map and Agent Memory Kit contracts.

## Main additions

- `CODEX_INTEGRATION_OWNER_GUIDE.md`
- `codex/README.md`
- `codex/CODEX_SETTINGS_RECOMMENDATIONS.md`
- `codex/CODEX_CONFIG_TOML_TEMPLATES.md`
- `codex/CODEX_HOOKS_SETUP_GUIDE.md`
- `codex/CODEX_CURSOR_WORKFLOW.md`
- `codex/CODEX_CUSTOM_INSTRUCTIONS.md`
- `codex/config/` templates
- `codex/hooks/` examples and optional scripts
- `codex/agents/` AGENTS.md examples
- `codex/skills/` memory-oriented skills
- `codex/subagents/` read-only review subagent templates

## Policy additions

- Codex is a second controlled agent surface, not a replacement for Project Map.
- Codex memory and platform-generated summaries are non-authoritative hints.
- Auto-compaction should be stopped until a checkpoint or handoff exists.
- Codex should be read-only by default and apply only through explicit task contracts.
- Cursor remains the primary local implementation agent; Codex is best used for review, audit, recovery, alternative design, and narrow scoped apply work.

## Python is optional

The hook scripts are examples. Agent Memory Kit remains language-agnostic and does not require Python.
