# Agent Memory Kit eval suite — v3.10.0

Status: authoritative kit eval suite for v3.10.0 when located under `Agent Kit/kit/eval_suite`.

Project Map mirror: `Project Map/eval_suite` is a synced mirror only when `manifest.yaml`, `eval_trigger_policy.yaml`, `run_eval_checklist.py`, and case IDs match the kit suite. If parity fails, mark the Project Map mirror as `stale_mirror` and do not grade from it as current truth.

v3.10.0 adds:

- `gpt_project_sources`:
  - local, config-driven ChatGPT Project sources manifest workflow;
  - `generate_chatgpt_project_sources.py` stdlib generator;
  - compact Project Instructions and operating contract templates;
  - owner manually updates ChatGPT Project sources in UI (no UI automation);
  - eval case `AMK-GPS-001`.

v3.9.6 baseline coverage retained:

- `shell_reliability_gate` and `model_setting_label_fidelity`;
- `context_compaction_control`;
- platform/generated summaries are non-authoritative hints;
- agent-created summaries/compaction are owner-gated unless inside an approved checkpoint/update task.

Authoritative files:

- `manifest.yaml`
- `eval_trigger_policy.yaml`
- `run_eval_checklist.py`
- `cases/*.yaml`

Legacy files from older eval-suite schemas must not drive smoke selection.
