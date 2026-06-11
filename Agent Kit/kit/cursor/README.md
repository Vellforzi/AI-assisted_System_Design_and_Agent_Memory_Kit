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

  skills/
    memory_compiler_skill.md
    checkpoint_builder_skill.md
    handoff_builder_skill.md
    eval_case_builder_skill.md
    source_authority_audit_skill.md
    context_recovery_skill.md

  subagents/
    api_auditor.md
    scraper_auditor.md
    mt_auditor.md
    db_schema_auditor.md
    docs_drift_auditor.md
    memory_auditor.md

```

---

## Install order

1. Install only the core Rules first.
2. Add Commands for common workflows.
3. Add Skills for longer procedures.
4. Add Subagents later, preferably read-only first.

---

## Minimal recommended setup

Rules:

- `agent_memory_core.mdc`
- `platform_context_compaction_boundary.mdc`
- `option_profit_safety.mdc`

Commands:

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

## Important limitation

Rules and commands guide the model. Agent Memory Kit itself is a file-based operating contract; it is not a security sandbox.


## Settings profile

Use `CURSOR_OWNER_CONTROLLED_DEFAULTS.md` and `settings/owner_controlled_profile.yaml` as the default Cursor Agent settings profile.

Key defaults:

- Run Mode must not be `Run Everything`; use Auto-review or stricter.
- Usage Summary should be visible, preferably Always.
- Auto-Approve Mode Transitions should be off.
- Auto-Accept Web Search should be off.
- Browser, file deletion, and external-file protections should be on.
- Auto Format on Agent Finish should be off.
- Hierarchical Cursor Ignore should be enabled only after `.cursorignore` is verified.
