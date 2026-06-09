# Cursor Integration Pack

This folder contains copy-pasteable building blocks for using Agent Memory Kit in Cursor.

It is intentionally split into small files so the owner can install only what is needed.

---

## Contents

```text
cursor/
  README.md
  COMMAND_VOCABULARY.md

  rules/
    agent_memory_core.mdc
    project_map_authority.mdc
    platform_context_compaction_boundary.mdc
    option_profit_safety.mdc

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
5. Add Subagents later, preferably read-only first.

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

Hooks:

- secret scan;
- git danger guard;
- DB write guard;
- scope guard;
- Project Map write guard.

---

## Important limitation

Rules and commands guide the model. Hooks and external tooling provide stronger technical checks. Agent Memory Kit itself is a file-based operating contract; it is not a security sandbox.
