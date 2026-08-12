# Cursor Integration Pack

This folder contains copy-pasteable building blocks for using Agent Memory Kit in Cursor.

It is intentionally split into small files so the owner can install only what is needed.

---

## Contents

```text
cursor/
  README.md
  COMMAND_VOCABULARY.md
  CURSOR_OWNER_CONTROLLED_DEFAULTS.md

  rules/
    agent_memory_core.mdc
    project_map_authority.mdc
    platform_context_compaction_boundary.mdc
    option_profit_safety.mdc
    context_advisor_preflight.mdc

  settings/
    owner_controlled_profile.yaml
    option_profit_current_profile.yaml

  context/
    .cursorignore.safe-default

  commands/
    answer.md
    analyze.md
    plan.md
    apply.md
    checkpoint.md
    handoff.md
    map-delta.md
    map-apply.md
    recover.md
    eval-smoke.md
    failure-case.md
    inventory.md
    context-advisor.md
    settings.md
    scope.md
    fuel.md
    safe-apply.md

  skills/
    memory_compiler_skill.md
    checkpoint_builder_skill.md
    handoff_builder_skill.md
    eval_case_builder_skill.md
    source_authority_audit_skill.md
    context_recovery_skill.md

  subagents/
    README.md
    api_auditor.md
    scraper_auditor.md
    mt_auditor.md
    db_schema_auditor.md
    docs_drift_auditor.md
    memory_auditor.md
    implementation_writer.md
    independent_reviewer.md
    coverage_mapper.md
    runtime_forensic.md
    native_builder.md
    artifact_deployer.md
    cheap_explorer.md

  hooks/
    README.md
    hooks.json.example
    scripts/
      block_secrets.py
      block_db_writes.py
      block_git_danger.py
      scope_guard.py
      project_map_write_guard.py
```

---

## Install order

1. Install only the core Rules first.
2. Add Commands for common workflows.
3. Add Skills for longer procedures.
4. Add Hooks only after testing them locally.
5. Add Subagents later, preferably read-only first. Treat
   `subagents/` as proposed functions with limits, not a required roster.
   See `../PROPOSED_SPECIALIST_FUNCTIONS.md`.

---

## Minimal recommended setup

Rules:

- `agent_memory_core.mdc`
- `platform_context_compaction_boundary.mdc`
- `option_profit_safety.mdc`
- `context_advisor_preflight.mdc`

Commands:

- `/context-advisor`
- `/settings`
- `/scope`
- `/fuel`
- `/safe-apply`
- `/answer`
- `/plan`
- `/apply`
- `/checkpoint`
- `/handoff`
- `/map-apply`
- `/recover`
- `/eval-smoke`
- `/settings-audit`
- `/cursorignore-audit`

Hooks:

- secret scan;
- git danger guard;
- DB write guard;
- scope guard;
- Project Map write guard.

---

## Important limitation

Rules and commands guide the model. Hooks and external tooling provide stronger technical checks. Agent Memory Kit itself is a file-based operating contract; it is not a security sandbox.


## Settings profile

Use `CURSOR_OWNER_CONTROLLED_DEFAULTS.md` and `settings/owner_controlled_profile.yaml` as the default Cursor Agent settings profile.

Key defaults:

- Run Mode must not be `Run Everything`; use Auto-review or stricter.
- Usage Summary should be visible, preferably Always.
- Auto-Approve Mode Transitions should be off.
- Auto-Accept Web Search should be off.
- Browser, MCP, file deletion, and external-file protections should be on.
- Auto Format on Agent Finish should be off.
- Hierarchical Cursor Ignore should be enabled only after `.cursorignore` is verified.


## Context Advisor

Install `rules/context_advisor_preflight.mdc` when you want Cursor to warn about insufficient scope, overbroad context, wrong Max/IDE context settings, or unsafe apply gates before work starts.

Use `/context-advisor`, `/settings`, `/scope`, `/fuel`, and `/safe-apply` as on-demand commands. These commands analyze only; they do not authorize mutation.
