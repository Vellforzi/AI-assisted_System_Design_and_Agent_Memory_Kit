# Agent Memory Kit eval suite — v3.9.4

This directory is part of the v3.9.4 micro-patch: eval parity, live Cursor
integration adoption, and model escalation trigger wording.

## Authority rule

`Agent Kit/kit/eval_suite` is the canonical kit eval suite. `Project Map/eval_suite`
is allowed to be a synced mirror only when all of the following match:

- `manifest.yaml:suite_id`
- `manifest.yaml:kit_version`
- case ids and required schema fields
- `eval_trigger_policy.yaml:kit_version`
- smoke categories required by `eval_trigger_policy.yaml`

If any of those drift, `Project Map/eval_suite` must be marked as `stale_mirror`
and must not be used as authoritative current grading input.

## v3.9.4 smoke categories

Smoke categories are not hardcoded in `run_eval_checklist.py`. They are read from
`eval_trigger_policy.yaml`.

Required v3.9.4 categories:

- `context_advisor`
- `cursor_integration`
- `eval_suite_sync`
- `model_escalation`

## Required case schema

Every active case must include:

- `id`
- `suite_id`
- `kit_version`
- `schema_version`
- `category`
- `title`
- `severity`
- `fixture`
- `grading`

## Static smoke command

```bash
python "Project Map/eval_suite/run_eval_checklist.py" \
  --root "Project Map/eval_suite" \
  --format markdown
```

For JSON output:

```bash
python "Project Map/eval_suite/run_eval_checklist.py" \
  --root "Project Map/eval_suite" \
  --format json
```

## Stale mirror marker

If Project Map is not synced to kit, set the manifest authority state to:

```yaml
authority:
  project_map_authority_state: stale_mirror
```

and add a visible README notice that this directory is not authoritative.
