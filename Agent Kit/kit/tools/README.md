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


## `context_advisor_preflight.py`

Runs a local Context Advisor preflight from `context_advisor/context_advisor_v1.profile_matrix.json`.

It does not call a model API, inspect project files, or mutate anything. It emits a compact gate and routing/settings hint.

Example:

```bash
python3 "Agent Kit/kit/tools/context_advisor_preflight.py" \
  --intent apply \
  --have project_map_core,source_authority,active_workstream,progress_logs,tests \
  --scope "Options_api/app/routes/example.py" \
  --owner-ok \
  --verification "pytest"
```

## v3.9.3 ContextAdvisor model routing flags

`context_advisor_preflight.py` accepts optional flags for dated provider/model routing checks:

```bash
python3 Agent\ Kit/kit/tools/context_advisor_preflight.py \
  --intent project_map_update \
  --have project_map_core,source_authority,memory_relevant \
  --settings-requested \
  --provider-snapshot-date 2026-06-10 \
  --model-name "Composer 2.5"
```

Use `--fast-mode`, `--large-context`, `--optional-model`, and `--optional-model-gap` to test routing warnings.


### v3.9.3 surface/mode preflight flags

`context_advisor_preflight.py` supports `--surface`, `--cursor-mode`, `--independent-subscopes`, and `--pursue-goal` to gate Cursor/Codex/ChatGPT surface routing, Multitask, and Codex goal-style autonomy.
