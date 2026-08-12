# Execution Profile Gate

Version: 1.0 (Agent Memory Kit v3.12.0)

## Purpose

`Executor Routing Gate` selects the appropriate agent surface. `Execution
Profile Gate` selects how the accepted task is allowed to run. A non-trivial
execution contract needs both.

The deterministic routing key is:

```text
mode + task class + canonical path zone
```

It must resolve to one execution profile, one toolchain profile, one scope
profile, one task output root, and one verification recipe. Missing or
equal-priority matches block execution.

## Required fields

```yaml
Execution Profile Gate:
  task_id: TASK-0001
  mode: apply
  task_class: bounded_repair
  path_zone: project_isolated_worktree
  execution_profile: project_bounded_apply
  toolchain_profile: owner_workstation
  scope_profile: task_exact_apply
  worktree: C:/absolute/path/to/worktree
  baseline_ref: 0123456789abcdef0123456789abcdef01234567
  scope_lease: .agent-runtime/scope-leases/TASK-0001.json
  source_write_authorization: owner_/apply_current_turn
  canonical_launcher: tools/resolve_execution_profile.py
  verification_profile: bounded_apply_full
  stop_or_escalation: stop on non-unique route, baseline drift, CAS conflict, or validation failure
```

## Scope lease

A mutation lease is operational state, not durable memory and not owner
permission by itself. It records task id, worktree, baseline, resolved profiles,
read/write scope, state/version, and a CAS token. Updates and release require
the current token. A compatibility projection may be generated for older scope
guards, but it must be reset with the same lease/CAS receipt.

Generic apply/build profiles expand `contract_declared_exact_paths` only from
machine-readable paths: backtick-wrapped entries under a Markdown `Allowed`,
`Allowed writes`, `Allowed paths`, or `Allowed scope` heading, or
`scope.project_files` / `allowed_write_scope` in a YAML contract. If the
placeholder is required and no paths can be parsed, resolution blocks. Paths
are canonicalized before matching, so `..`, symlink, or junction aliases cannot
inherit a broader allowed zone.

Read-only answer/analyze/plan/review/recover profiles do not grant a source
write lease. Stage and map-delta may write only the active task-output root.
Apply and map-apply require explicit current owner authorization and one unique
profile match.

## Path and toolchain boundaries

- Resolve `..`, symlink, and reparse/junction aliases before case-insensitive
  Windows matching, then use the most specific registered zone.
- Unknown, secure, backup, and ambiguous zones fail closed.
- Use registered executable paths; do not guess from PATH when a proven
  owner-local toolchain exists.
- Product build, DB, deploy, credentials, release, and remote side effects
  retain their separate owner gates.

## Archive provenance

Commit parity requires bytes read from Git commit blobs (for example via
`git cat-file`). A ZIP built from checked-out worktree bytes may receive a
`worktree_parity` verdict only. It must never receive `commit_parity`, even when
the current worktree happens to match, because checkout attributes and EOL
conversion can change bytes.

## Owner-facing model tuple

Execution profiles do not add provider settings. A ChatGPT Codex prompt-time
recommendation contains only supported selectable controls: surface, model,
reasoning/effort, and speed when available. Do not pad it with derived off
states, IDE context, shell, terminal profile, or application configuration.
