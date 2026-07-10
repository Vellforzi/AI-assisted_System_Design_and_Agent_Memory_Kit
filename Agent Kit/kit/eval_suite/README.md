# Agent Memory Kit Eval Suite - v3.11.1 Candidate

Status: authoritative working-tree candidate eval suite for v3.11.1 when located under
`Agent Kit/kit/eval_suite`.

This is not release proof. v3.11.1 adds `AMK-ML-002` and `AMK-MR-001` for
GPT-5.6 exact labels/slugs, cost-aware Luna/Terra/Sol routing, Max/Ultra/Cursor
Max separation, Fast source conflict, stale Cursor evidence, cross-surface
availability, and historical snapshot immutability.

Project Map mirror: `Project Map/eval_suite` is a synced mirror only when
`manifest.yaml`, `eval_trigger_policy.yaml`, `../tools/run_eval_checklist.py`, and case
IDs match the kit suite. If parity fails, mark the Project Map mirror as
`stale_mirror` and do not grade from it as current truth.

v3.11.0 adds:

- `executor_routing`: non-trivial task contracts and bootstraps must include an
  evidence-based Executor Routing Gate.
- `windows_encoding_hygiene`: Windows shell, quoting, and encoding-sensitive
  edits must use safe write paths and readback checks.
- `hook_recovery`: hook denials must surface recovery payloads and preserve
  answer/analyze read-only boundaries.
- `connector_side_effects`: connector reads and writes require explicit scoped
  allowance, with draft-first outbound behavior by default.
- `generated_retrieval_evidence`: generated search, cache, and index output
  narrows candidates but cannot establish truth without canonical source
  readback.

v3.10.0 coverage retained:

- `gpt_project_sources`:
  - local, config-driven ChatGPT Project sources manifest workflow;
  - `generate_chatgpt_project_sources.py` stdlib generator;
  - compact Project Instructions and operating contract templates;
  - owner manually updates ChatGPT Project sources in the UI;
  - eval case `AMK-GPS-001`.

v3.9.6 baseline coverage retained:

- `shell_reliability_gate` and `model_setting_label_fidelity`;
- `context_compaction_control`;
- platform/generated summaries are non-authoritative hints;
- agent-created summaries/compaction are owner-gated unless inside an approved
  checkpoint or update task.

Authoritative files:

- `manifest.yaml`
- `eval_trigger_policy.yaml`
- `../tools/run_eval_checklist.py`
- `cases/*.yaml`

The same-directory `eval_suite/run_eval_checklist.py` is a legacy compatibility
helper and is not the manifest-selected v3.11.1 validator.

Smoke selection contract:

- `../tools/run_eval_checklist.py` reads `smoke_policy.categories` from
  `eval_trigger_policy.yaml`. It must not keep an independent hardcoded
  smoke-category list.
- A case counts toward a required category when `case.category` matches or a
  case `tag` matches that category name.
- `eval_suite_sync` is satisfied by `AMK-ESS-001` and may also be reinforced by
  tag overlap on older cases such as `AMK-CA-012`.
- Legacy embedded suites such as `core_behavior_eval_cases.yaml` are supported
  for historical review only. Without an explicit `--policy`, they use the
  historical smoke categories plus critical cases and are not validated against
  the v3.11.0 `min_cases` contract.

Inherited case metadata:

- Manifest-listed cases introduced before v3.11.0 may keep their original
  `suite_id` and `kit_version` fields until a separate metadata normalization
  task is approved.
- Smoke validation still requires schema fields on every listed case and manifest
  versus policy version parity, but it does not fail solely because an inherited
  case file reports an older `suite_id` or `kit_version`.

Legacy files from older eval-suite schemas must not drive v3.11.0 authoritative
smoke selection.
