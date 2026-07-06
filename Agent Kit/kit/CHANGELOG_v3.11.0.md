# Agent Memory Kit v3.11.0 - Operational Boundary and Routing Hardening

Release date: 2026-07-05
Status: working-tree implementation ready for owner review; not yet published.

## Purpose

v3.11.0 packages generic improvements developed during real project use without
copying private project state into the public kit.

The release strengthens how agents choose execution surfaces, recover from hook
blocks, handle encoded text safely, treat connector output, and use generated
retrieval helpers.

## Added

- `EXECUTOR_ROUTING_GATE.md` - evidence-based executor/service routing gate for
  non-trivial task contracts, bootstraps, task blocks, and model/service advice.
- `tools/verify_executor_routing_gate.py` - reusable validator for staged
  contracts and bootstrap artifacts.
- `WINDOWS_ENCODING_AND_SHELL_HYGIENE.md` - byte-safe file mutation and readback
  policy for Windows and non-ASCII text.
- `HOOK_RECOVERY_PLAYBOOK.md` - generic recovery-field contract for blocking
  hooks, accepting both snake_case and camelCase payload forms.
- `CODEX_CONNECTOR_POLICY.md` - connector side-effect policy: default forbidden,
  scoped reads, explicit write gates, draft-first outbound messaging, and
  receipts.
- `GENERATED_RETRIEVAL_EVIDENCE_GUIDE.md` - generated search/index output as
  retrieval evidence only, with canonical source re-read before project claims.
- Eval cases:
  - `AMK-ERG-001`
  - `AMK-WIN-001`
  - `AMK-HR-001`
  - `AMK-CONN-001`
  - `AMK-GRE-001`

## Updated

- `TASK_CONTRACT_TEMPLATE.yaml` and `START_MESSAGE_TEMPLATES.md` now include the
  Executor Routing Gate.
- `AGENTS.md_TEMPLATE.md` now includes generic hook recovery, encoding hygiene,
  and executor routing rules.
- Permission/source/retrieval templates include connector and generated
  retrieval boundaries.
- Codex hook examples include richer recovery payloads and sharper read-only
  scope reminders.
- Model/settings guidance now treats provider labels as dated snapshot evidence,
  not current defaults.
- Eval manifest and trigger policy now cover routing, hook recovery, connector
  safety, Windows encoding hygiene, and generated retrieval evidence.

## Non-goals

- No private Project Map payloads.
- No product-specific logs, receipts, release artifacts, database facts, hosting
  state, or credentials.
- No GitHub release, tag, push, ZIP, or publication side effect.
- No current provider/model claim beyond dated-snapshot guidance.

## Version gate

This is a minor release because it adds guides, templates, tooling, and eval
coverage. It does not introduce a breaking memory schema change.
