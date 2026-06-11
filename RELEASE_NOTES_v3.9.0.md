# Agent Memory Kit v3.9.0 - Context Advisor Release

Release date: 2026-06-10
Status: portable project-owner toolkit

This release adds the **Context / Scope / Model Advisor** layer.

The main purpose of v3.9.0 is to reduce two recurring failure modes:

1. The owner under-scopes a task because they cannot know in advance which files, memory units, logs, schemas, or source-authority entries are required.
2. The agent over-scopes a task, loads noisy context, and burns tokens or usage on irrelevant work.

The Context Advisor runs before retrieval/hydration and before heavy agent work. It classifies the task, estimates the required context classes, checks whether the current scope is sufficient, recommends the execution surface/model class/settings, and returns a compact hint only when useful.

---

## Added

- `CONTEXT_SCOPE_MODEL_ADVISOR.md` - the main design and operating guide.
- `CONTEXT_ADVISOR_TEMPLATE.yaml` - project-local template for advisor policy.
- `PROVIDER_CAPABILITY_SNAPSHOT_TEMPLATE.yaml` - template for volatile model/provider capability snapshots.
- `context_advisor/` - machine-readable profile matrix, hint policy, TypeScript contract, example run, and provider snapshot example.
- `tools/context_advisor_preflight.py` - optional local CLI helper that emits compact advisory output from the profile matrix.
- Cursor rule: `cursor/rules/context_advisor_preflight.mdc`.
- Cursor commands: `/context-advisor`, `/settings`, `/scope`, `/fuel`, `/safe-apply`.
- Codex workflow: `codex/workflows/context-advisor.md`.
- Eval cases for scope sufficiency, compact hints, provider snapshot freshness, Max Mode / IDE context defaults, and safe-apply blocking.

---

## Changed

- The retrieval policy docs now describe Context Advisor as the **pre-hydration** layer.
- Working State can reference `context_advisor_trace_ref`, `context_needs_manifest_ref`, and `provider_capability_snapshot_ref` without storing large payloads.
- The memory tool interface includes `memory.advise_context` and `memory.read_provider_capabilities` as conceptual operations.
- Cursor and Codex guides now include on-demand context/settings/fuel checks.
- Start-message templates include compact owner prompts for automatic and on-demand advisor use.
- The eval suite now includes `context_advisor` as a behavior category.

---

## Default advisor behavior

- Silent by default for easy tasks.
- Compact hint for amber/red scope, apply/audit/repair tasks, missing mandatory context, stale provider snapshots, or likely-wrong model/settings.
- Expanded explanation only on direct request: `settings?`, `scope?`, `fuel?`, `why?`, or `safe apply?`.
- Block only when the request involves secrets, unsafe writes, missing owner approval for mutation, ambiguous branch lineage for mutation, or duplicate side-effect risk.

---

## Practical default settings policy

- Max Mode: off first; turn on only when the advisor proves long context is required.
- Include IDE Context: off first; use explicit `@file` / file refs unless exact open files are intentionally scoped.
- Plan Mode: on for multi-file planning, root-cause debugging, audit, and high-risk changes.
- Speed: standard for risky, verification-heavy, or cross-subsystem work.
- Reasoning: medium for bounded local edits; high for cross-subsystem analysis, audit, repair, package updates, and schema/protocol design.

Provider/model capability facts are volatile. Store them as timestamped provider capability snapshots, not as timeless project memory.

---

## Compatibility

v3.9.0 is compatible with v3.8.0 projects. Existing Project Maps do not need immediate migration. To adopt v3.9.0, copy the new advisor files and optionally add advisor refs to `working_state.yaml` and `retrieval_policy.yaml`.
