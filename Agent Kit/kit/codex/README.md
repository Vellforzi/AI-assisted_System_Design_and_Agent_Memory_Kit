# Codex Integration Pack

This folder contains templates for using Codex with Agent Memory Kit.

The pack assumes Codex is used as a controlled second agent surface inside or alongside Cursor, not as an uncontrolled autonomous runtime.

## Contents

```text
codex/
  config/
    config.toml.owner-controlled.example
    config.toml.safe-overlay.toml
    custom-instructions.codex.txt
  agents/
    AGENTS.global.example.md
    AGENTS.project.example.md
  skills/
  subagents/
  CODEX_SETTINGS_RECOMMENDATIONS.md
  CODEX_CURSOR_WORKFLOW.md
  CODEX_CONFIG_TOML_TEMPLATES.md
  CODEX_CUSTOM_INSTRUCTIONS.md
```

## Recommended use

Use Codex for read-only audit, review, recovery, independent analysis, or scoped implementation when the selected role profile allows it. Keep Project Map as the durable project-memory source; treat it as project truth only when source authority says so.

## Critical boundary

Codex memory, provider memory, compressed chat history, and platform summaries must not be used as project truth.

## Setup summary

1. Add safe settings to `~/.codex/config.toml`.
2. Put `AGENTS.md` in the project root.
3. Restart Codex after global config changes.

---

## v3.8 additions

Codex integration now includes:

- scope-control templates and helper;
- guidance for `default_permissions` versus old `sandbox_mode` settings;
- workspace selection guidance;
- a default role split: Cursor implements, Codex reviews, GPT researches, Project Map stores memory or truth according to source authority;

See:

- `../SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`
- `../CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`
- `../WORKSPACE_SELECTION_GUIDE.md`
- `../AI_AGENT_ROLE_STACK_GUIDE.md`
- `scope/README.md`

## Ignore files

See `ignore/` for `.codexignore` templates and the Codex ignore boundary guide. Keep `.codexignore` aligned with `.cursorignore` when Cursor and Codex operate on the same project root.
