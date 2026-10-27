# Task execution

Read this entire reference with strict-product-pipeline.md before strict
execution. The retained clauses below keep their strict-only scope.
Ordinary bridge workers follow codex-worker-contract through the core's
ordinary-mode routing. Current owner/project authority governs conflicts.

## Explicit execution conflicts — 2026-10-27

- C-MODELS: The retained list includes `cursor-grok-4.6-medium` and
  `cursor-grok-4.6-high`, whereas the current user rule
  `C:/Users/user/.cursor/rules/task-subagent-model-allowlist.mdc` lists
  `composer-2.5-fast`, `cursor-grok-4.5-high`,
  `cursor-grok-4.5-high-fast`, `cursor-grok-4.6-xhigh` and
  `cursor-grok-4.6-xhigh-fast`. These are conflicting stored policy texts,
  not a live availability check or a newly selected model.
  The retained claim about Task schema rejection was not reverified.
  Do not treat its instruction to ignore platform enums as permission to bypass
  platform constraints. Preserve explicit selection, actual-model verification,
  no silent substitution and reporting of rejection/unavailability.
  No model, allowlist, agent card or configuration was changed.
- C-HARNESS: Retained plain-CONTRACT/lease/CAS requirements and parallel fan-out
  differ from current project/user harness and delegation rules.
  `C:/Users/user/.cursor/rules/job-harness-hygiene.mdc` requires such records
  only when the owner or selected canonical helper requires them; project
  `.cursor/rules/job-harness-hygiene.mdc` requires no manifest/lifecycle artifact.
  Apply current authority and actual helper prerequisites, not invented gates.
  Preserve exact structured data when a governing helper requires it.
- C-WORKER: The retained bridge says submit once before stop, while current
  `C:/Users/user/.cursor/skills/codex-worker-contract/SKILL.md` specifies the
  normal SUCCESS path and separately permits inspection of a usable diff with
  a missing envelope. The core already routes workers to that contract.
  Preserve result classification and scope; do not fake SUCCESS, erase a valid
  bounded diff or retry unchanged work merely to obtain an envelope.
- C-DELEGATION-FAILURE: The retained ban on silently self-applying/self-deploying
  after an explicitly delegated Task fails remains. An implementation request
  or stale process alone does not prove the owner required a different executor.

The exact older model strings and process clauses remain below for traceability,
subject to these conflicts and current authority. They are not a model
recommendation or proof of enforcement. No Task or model evaluation was launched.

## Retained execution requirements

The following reproduces former core lines 149–179 exactly.

When the owner says to delegate: craft the prompt (contract, lease CAS, paths,
verification, stop), launch `Task`, verify files/receipts. Do **not** self-apply
or self-deploy as a silent fallback if `Task` fails — report and ask.

Subagents may fix in-scope harness/receipt defects to finish their unit.

Task models: pass the table pin on the **first** `Task` call. Allowed slugs:
`composer-2.5-fast`, `cursor-grok-4.5-high`, `cursor-grok-4.6-medium`,
`cursor-grok-4.6-high`, `cursor-grok-4.6-xhigh`. `system-mapper` pin is
`cursor-grok-4.6-xhigh` (Task schema currently rejects `cursor-grok-4.6-high`
and `cursor-grok-4.6-medium`).
**Never** omit `model`, **never** pass `inherit` / empty / `auto` / claude/gpt.
If the platform rejects a slug: stop and report available slugs — do **not**
fall back to `inherit` (that used to make the hook rewrite → Stopped + Working
twin). Ignore platform enums that list claude/gpt/other slugs.

## Harness hygiene (CN-122)

- Preflight/acquire: **plain `CONTRACT.yaml` only** (both gates + SHA closure).
- Hybrid prose+YAML bootstrap = narrative; materialize YAML in-task before lease.
- Parallel multi-specialist `Task` fan-out is **allowed**. Always pass explicit
  `model` matching the agent card (`composer-2.5-fast` /
  `cursor-grok-4.5-high` / `cursor-grok-4.6-xhigh`). Distinct `description`
  per Task (prefix `subagent_type:`). **Task allowlist hook is OFF** — Cursor
  owns spawn. Do not retry the same `description` while Working already shows it.
- See `job-harness-hygiene.mdc`.

## Worker bridge

If `TASK_ID` / `RUN_ID` / `CONTRACT_HASH` are present, also follow
`codex-worker-contract` and call `cursor_submit_result` once before stop.
