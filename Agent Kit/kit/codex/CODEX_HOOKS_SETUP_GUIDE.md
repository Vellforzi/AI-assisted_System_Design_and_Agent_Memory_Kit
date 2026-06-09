# Codex Hooks Setup Guide

Codex hooks are loaded from files, not from UI buttons.

## Hook locations

Use one of these locations:

```text
~/.codex/hooks.json
~/.codex/config.toml
<repo>/.codex/hooks.json
<repo>/.codex/config.toml
```

For project-specific policy, prefer:

```text
<repo>/.codex/hooks.json
<repo>/.codex/hooks/*.py
```

For global personal policy, use:

```text
C:\Users\<user>\.codex\hooks.json
C:\Users\<user>\.codex\hooks\*.py
```

## Enable hooks

In `~/.codex/config.toml`:

```toml
[features]
hooks = true
```

Do not create a second `[features]` table. Merge this key into the existing table.

## Recommended first hooks

Start with:

1. `pre_compact_checkpoint_guard.py` — stops automatic compaction before Codex summarizes the conversation.
2. `user_prompt_scope_guard.py` — blocks changing requests without explicit scope.
3. `dangerous_command_guard.py` — blocks dangerous shell commands.
4. `project_map_write_guard.py` — blocks Project Map writes unless explicitly allowed.

## Project-local setup

Create:

```text
<repo>/.codex/hooks.json
<repo>/.codex/hooks/pre_compact_checkpoint_guard.py
<repo>/.codex/hooks/user_prompt_scope_guard.py
<repo>/.codex/hooks/dangerous_command_guard.py
<repo>/.codex/hooks/project_map_write_guard.py
```

Copy `codex/hooks/hooks.json.project.example` to `<repo>/.codex/hooks.json` and copy scripts from `codex/hooks/scripts/` to `<repo>/.codex/hooks/`.

## Windows note

Use `commandWindows` entries in `hooks.json` for Windows-specific execution.

## Operational boundary

Hooks are guardrails, not a full security boundary. Keep destructive operations behind explicit owner approval, narrow permissions, git review, and CI.
