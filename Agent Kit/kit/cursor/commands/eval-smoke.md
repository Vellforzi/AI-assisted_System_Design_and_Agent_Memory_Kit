# /eval-smoke

Purpose: run or prepare a small behavior check after instruction, rule, kit, workflow, or repeated-failure changes.

Mode: audit
Default mutations: forbidden

If local script execution is allowed, the owner may run:

```bash
python3 "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Project Map/eval_suite/core_behavior_eval_cases.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```

Agent Memory Kit does not require Python. This helper is optional and can be replaced.

If execution is not allowed, prepare a manual checklist from the relevant cases.

Always report:

- cases selected;
- why selected;
- pass/fail/needs owner review;
- failures that should become repair tasks.
