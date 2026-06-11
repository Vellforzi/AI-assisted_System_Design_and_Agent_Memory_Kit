# Agent Memory Kit eval suite — v3.9.5

Status: authoritative kit eval suite for v3.9.5 when located under `Agent Kit/kit/eval_suite`.

Project Map mirror: `Project Map/eval_suite` is a synced mirror only when `manifest.yaml`, `eval_trigger_policy.yaml`, `run_eval_checklist.py`, and case IDs match the kit suite. If parity fails, mark the Project Map mirror as `stale_mirror` and do not grade from it as current truth.

v3.9.5 adds smoke coverage for `context_compaction_control`:

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
