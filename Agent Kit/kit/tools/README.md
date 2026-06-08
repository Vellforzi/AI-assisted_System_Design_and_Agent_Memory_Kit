# Agent Memory Kit Tools

This folder contains optional helper scripts. They are not required to use the kit.

## `run_eval_checklist.py`

Creates a local eval run folder and Markdown checklist from `eval_suite/core_behavior_eval_cases.yaml`.

It does not call a model API and does not grade automatically. It helps the owner start and record a manual or semi-automated eval run.

Example:

```bash
python3 "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Project Map/eval_suite/core_behavior_eval_cases.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```
