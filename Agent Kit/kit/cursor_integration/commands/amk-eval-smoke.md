# /amk-eval-smoke

Run static AMK eval-smoke audit.

Mode: read-only by default. Do not auto-grade with a live harness unless the owner explicitly asks and the harness exists.

Suggested command:

```bash
python "Project Map/eval_suite/run_eval_checklist.py" --root "Project Map/eval_suite" --format markdown
```

Checks:

1. `manifest.yaml` and `eval_trigger_policy.yaml` must report the same `suite_id` and `kit_version`.
2. `run_eval_checklist.py` must read smoke categories from `eval_trigger_policy.yaml`, not a hardcoded category list.
3. Required smoke categories must include policy coverage for context advisor and Cursor integration.
4. Active cases must include `severity`, `fixture`, and `grading`.
5. `Project Map/eval_suite` must be synced to the kit or explicitly marked stale mirror.

Output: findings, evidence paths/lines, verification commands, and proposed Project Map delta only if durable facts changed.
