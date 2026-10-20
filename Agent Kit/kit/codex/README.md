# Codex Integration Pack

This folder contains templates for using Codex clients with Agent Memory Kit.

The current ChatGPT desktop app combines Chat, Work, and Codex. Codex desktop
mode, Codex IDE extension, Codex CLI, and Codex web remain distinct clients.
The pack treats each as a controlled agent surface alongside Cursor.

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

Use Codex for owner-authorized implementation, analysis, review or recovery when
its current tools fit the task. Keep durable project context in the owner-selected
source and verify recalled claims against current files. No fixed client role split
or mandatory intermediary is required.

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

---

## v3.8 additions

Codex integration now includes:

- scope-control templates and helper;
- guidance for `default_permissions` versus old `sandbox_mode` settings;
- workspace selection guidance;
- historical role-split examples, superseded by current capability-based routing;
- hook request workflow for generating project-local hook packages.

See:

- `../SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`
- `../CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`
- `../WORKSPACE_SELECTION_GUIDE.md`
- `../AI_AGENT_ROLE_STACK_GUIDE.md`
- `scope/README.md`

## Ignore files

See `ignore/` for `.codexignore` templates and the Codex ignore boundary guide. Keep `.codexignore` aligned with `.cursorignore` when Cursor and Codex operate on the same project root.

## v3.9.3 model-routing note

For current ChatGPT desktop Codex prompt choices and distinct Codex client
boundaries, see `workflows/model-routing.md`. Prompt recommendations contain
only surface, model, reasoning, and speed; app configuration is documented
separately.


## Optional production quality skills

Adopt the two canonical skills under `../skills/` using
[the quality-pack guide](../PRODUCTION_CODE_CHANGE_GUIDE.md). Version 4.4.0 adds
purpose comments, truthful types, language/version idioms, justified handlers,
owned-resource cleanup and causal-diagnosis references. The communication skill
references the engineering policy rather than duplicating it.

Verify the selected client's supported discovery path and explicit instruction
links. A copied file is not proof that an already-open client loaded it.
Comment language and exact analyzer versions belong to the adopting project.
