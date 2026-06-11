# Agent Memory Kit eval suite — v3.9.6

Status: authoritative kit eval suite for v3.9.6 when located under `Agent Kit/kit/eval_suite`.

Project Map mirror: `Project Map/eval_suite` is a synced mirror only when `manifest.yaml`, `eval_trigger_policy.yaml`, `run_eval_checklist.py`, and case IDs match the kit suite. If parity fails, mark the Project Map mirror as `stale_mirror` and do not grade from it as current truth.

v3.9.6 keeps `context_compaction_control` and adds:

- `shell_reliability_gate`:
  - health check `echo AMK_SHELL_OK; pwd; git rev-parse HEAD` before shell-dependent PASS/commit;
  - unknown/no-output/no-exit-code is hard failure, not PASS;
  - preferred transport route is Run Mode `Allowlist`, never Run Everything for this recovery path.
- `model_setting_label_fidelity`:
  - model/settings prompts must match exact owner/provider UI labels from dated snapshot/confirmation;
  - no invented combined labels;
  - no contradictory tuple such as `Model: Codex 5.3 High` with `Reasoning: Medium`.

v3.9.5 baseline coverage retained:

- platform/generated summaries are non-authoritative hints;
- agent-created summaries/compaction are owner-gated unless inside an approved checkpoint/update task;
- controlled compaction requires an explicit keep/drop/evidence plan;
- old re-fetchable tool outputs should be cleared or excluded from future context while replay-critical refs and side-effect receipts are retained.

Authoritative files:

- `manifest.yaml`
- `eval_trigger_policy.yaml`
- `run_eval_checklist.py`
- `cases/*.yaml`

Legacy files from older eval-suite schemas must not drive smoke selection.
