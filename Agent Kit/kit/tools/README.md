# Agent Memory Kit Tools

This folder contains helper scripts. They are optional for the general kit, but
the repo-centric context governance baseline uses the context helper and
documentation harness when a project wants stockanalyst-style local checks.

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

## `context_governance_helper.py`

Reference implementation for the `secondary_memory_governance/` repo-centric
context governance baseline.

Copy it into a target project as:

```text
scripts/ai_context_helper.py
```

It reads `docs/project_map/context_index.yaml` and can produce:

- deterministic task-profile read sets;
- retrieval receipts;
- read-only API-agent context bundles;
- context-selection smoke-check reports.

Smoke-check reports validate both selection behavior and that selected/required
read-set files exist in the installed project.

Examples:

```bash
python3 "Agent Kit/kit/tools/context_governance_helper.py" \
  --root "<Project Root>" \
  read-set \
  --profile startup \
  --format json

python3 "Agent Kit/kit/tools/context_governance_helper.py" \
  --root "<Project Root>" \
  smoke-check \
  --format json
```

The helper is read-only and uses only the Python standard library.

## `documentation_harness.py`

Reference report-only harness for the `secondary_memory_governance/`
repo-centric context governance baseline.

Copy it into a target project as:

```text
scripts/documentation_harness.py
```

It scans repository documentation for:

- active-doc metadata;
- inbound reachability;
- unlabeled references to lower-authority docs such as archive, planned,
  proposal, research, or Project Map files.

Example:

```bash
python3 "Agent Kit/kit/tools/documentation_harness.py" \
  --root "<Project Root>" \
  --format json
```

The harness is report-only. It does not edit docs, Project Map, runtime code,
data artifacts, external systems, commits, pushes, or deployments.
