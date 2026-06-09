# Agent Memory Kit v3.7.0 — Scope, Sandbox, and Workspace Control Release

This release strengthens the operational layer around Cursor, Codex, task scope, workspace selection, and owner-controlled multi-agent workflows.

## Main focus

v3.7.0 makes the kit more practical for a solo owner who uses:

```text
Cursor = primary implementation agent
Codex = restricted reviewer/auditor/recovery helper
GPT web chat = research, design, and task specification
Project Map = shared project truth
```

## Added

- `SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`
- `CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`
- `WORKSPACE_SELECTION_GUIDE.md`
- `AI_AGENT_ROLE_STACK_GUIDE.md`
- `HOOK_REQUEST_WORKFLOW.md`
- `HOOK_GENERATION_QUESTIONS.md`
- `HOOK_PACKAGING_GUIDE.md`

## Added to Cursor Integration Pack

- `cursor/workspaces/README.md`
- `cursor/workspaces/OPTION_PROFIT_JOB.code-workspace.example`
- `cursor/workspaces/single-root-project.code-workspace.template`
- `cursor/commands/scope-set.md`
- `cursor/commands/scope-reset.md`
- `cursor/commands/workspace-check.md`

## Added to Codex Integration Pack

- `codex/scope/README.md`
- `codex/scope/ALLOWED_SCOPE.safe-default.txt`
- `codex/scope/ALLOWED_SCOPE.option-profit-default.txt`
- `codex/scope/update_allowed_scope.py`
- `codex/scope/scope_update_request_template.yaml`
- `codex/workflows/scope-set.md`
- `codex/workflows/scope-reset.md`
- `codex/workflows/workspace-check.md`
- `codex/config/config.toml.owner-controlled-v3.7.0.example`

## Updated

- Root `README.md`
- `START_HERE.md`
- `Agent Kit/README.md`
- `Agent Kit/kit/README.md`
- `MANIFEST.md`
- `OWNER_USAGE_GUIDE.md`
- `PROJECT_MEMORY_OPERATING_PROTOCOL.md`
- `AGENTS.md_TEMPLATE.md`
- `CURSOR_INTEGRATION_OWNER_GUIDE.md`
- `CODEX_INTEGRATION_OWNER_GUIDE.md`
- `codex/CODEX_SETTINGS_RECOMMENDATIONS.md`
- `codex/CODEX_CONFIG_TOML_TEMPLATES.md`
- `codex/CODEX_HOOKS_SETUP_GUIDE.md`
- `cursor/COMMAND_VOCABULARY.md`
- `eval_suite/core_behavior_eval_cases.yaml`

## Important behavior changes

### Agent-managed scope files

The owner should not have to manually edit `.codex/ALLOWED_SCOPE.txt` when an approved agent workflow can safely update it.

The agent must still respect explicit action intent:

- no scope update for ordinary questions or analysis;
- no product edits during scope setup;
- no mutation without task contract;
- no broad write scope unless explicitly approved;
- reset scope after task completion.

### Codex permission defaults

Recommended Codex default remains restricted:

```toml
approval_policy = "on-request"
default_permissions = ":read-only"
```

Do not mix `default_permissions` with old `sandbox_mode` / `[sandbox_workspace_write]` settings.

### Workspace selection

For a multi-component project with one Project Map, prefer opening the shared project root as the workspace. Use task scope, hooks, and permission profiles for safety instead of hiding project memory through component-only workspaces.

## Eval additions

Added eval cases for:

- scope file is not manual-only;
- allowed scope is not authorization;
- scope reset after apply;
- Codex sandbox and permission explanation;
- shared root workspace selection;
- role split across Cursor, Codex, GPT web chat, Project Map, and owner.

## Python is not required

Agent Memory Kit remains language-agnostic and file-based. Python scripts are optional helper examples only.
