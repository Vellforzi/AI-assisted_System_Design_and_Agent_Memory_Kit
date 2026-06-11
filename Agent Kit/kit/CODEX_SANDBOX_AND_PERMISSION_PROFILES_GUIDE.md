# Codex Sandbox and Permission Profiles Guide

This guide explains Codex local permissions in plain operational terms.

## Short answer

For the owner-controlled Agent Memory Kit workflow, do not install a separate sandbox first.

Start with:

```toml
default_permissions = ":read-only"
approval_policy = "on-request"
```

Then restart Codex.

## What this means

`default_permissions` selects the Codex local permission profile used for sandboxed tool calls.

Recommended default:

```toml
default_permissions = ":read-only"
```

This makes Codex a read-only reviewer by default. It can inspect and analyze the project, but changing files should require an explicit owner-approved task and a temporary write-capable workflow.

## Capability check first

Before claiming a workflow is protected, identify the active runtime capability profile:

```text
permission profile: read-only / workspace-write / danger-full-access / unknown
approval prompts: available / unavailable / unknown
scope file enforcement: enforced / advisory / absent / unknown
```

If the environment has broad write access or no approval prompts, report that scope files and policy YAML are advisory unless wrapper or runtime checks enforce them.

## Built-in profiles

Common built-in profiles:

- `:read-only` — safe default for audit, review, analysis, recovery, and planning.
- `:workspace` — allows writes inside active workspace roots; use only for explicit scoped apply tasks.
- `:danger-full-access` — broad local access; do not use for normal project work.

## Do not mix old and new settings

If you use permission profiles, do not also configure the older keys:

```toml
sandbox_mode = "..."
[sandbox_workspace_write]
```

Reason: if old sandbox settings are present, Codex may use those instead of the newer `default_permissions` profile path. Keep the config simple and use one model:

```toml
approval_policy = "on-request"
default_permissions = ":read-only"
```

## What the owner should do if asked about sandbox

The agent should answer:

1. no separate sandbox installation is required for the default controlled workflow;
2. set `default_permissions = ":read-only"` in `~/.codex/config.toml`;
3. ensure `sandbox_mode` and `[sandbox_workspace_write]` are not present unless intentionally using the older configuration path;
4. restart Codex;
5. use `ALLOWED_SCOPE.txt` or equivalent wrapper checks for task-level guardrails;
6. use a write-capable profile only for explicit scoped apply tasks.

## How this helps Agent Memory Kit

Agent Memory Kit is a behavior and memory contract. Permission profiles are a technical boundary.

Recommended stack:

```text
Project Map = project memory/truth according to source authority
Task Contract = permission boundary
Codex default_permissions = local access boundary
ALLOWED_SCOPE.txt = task write whitelist
Owner approval = final authority
```

## For apply tasks

Default remains read-only.

For a write task, the agent should:

1. propose exact write scope;
2. update `ALLOWED_SCOPE.txt` only after approval;
3. ask for the needed write capability if the runtime blocks edits;
4. apply only the approved diff;
5. reset scope after work;
6. report changed files and verification.
