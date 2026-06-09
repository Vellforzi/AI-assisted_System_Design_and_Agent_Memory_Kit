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
  hooks/
    hooks.json.global.example
    hooks.json.project.example
    scripts/
  agents/
    AGENTS.global.example.md
    AGENTS.project.example.md
  skills/
  subagents/
  CODEX_SETTINGS_RECOMMENDATIONS.md
  CODEX_HOOKS_SETUP_GUIDE.md
  CODEX_CURSOR_WORKFLOW.md
  CODEX_CONFIG_TOML_TEMPLATES.md
  CODEX_CUSTOM_INSTRUCTIONS.md
```

## Recommended use

Use Codex for read-only audit, review, recovery, and independent analysis. Keep Project Map as the only durable project-memory source.

## Critical boundary

Codex memory, provider memory, compressed chat history, and platform summaries must not be used as project truth.

## Setup summary

1. Add safe settings to `~/.codex/config.toml`.
2. Put global hooks in `~/.codex/hooks.json` or project hooks in `<repo>/.codex/hooks.json`.
3. Put hook scripts in `<repo>/.codex/hooks/` for project-local enforcement.
4. Put `AGENTS.md` in the project root.
5. Restart Codex after global config changes.

## Python is optional

The provided hook scripts are examples. Agent Memory Kit itself is language-agnostic and does not require Python.
