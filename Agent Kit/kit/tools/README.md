# Agent Memory Kit Tools

This folder contains optional helper scripts. They are not required to use the kit.

## `verify_executor_routing_gate.py`

Checks non-trivial task contracts and bootstrap artifacts for a complete
Executor Routing Gate.

Example:

```bash
python "Agent Kit/kit/tools/verify_executor_routing_gate.py" \
  --path "agent-tools/tasks/example/TASK-contract.md" --json
```

## `run_eval_checklist.py`

Creates a local eval run folder and Markdown checklist from the v3.11.0 manifest
suite or a legacy embedded cases YAML file.

Requires Python with PyYAML available.

Smoke mode reads required categories from `eval_suite/eval_trigger_policy.yaml`
and validates each required category's `min_cases` count. It must not maintain a
separate hardcoded smoke-category list.

Legacy embedded suites use the historical smoke categories plus critical cases
unless `--policy` is supplied explicitly.

Examples:

```bash
python "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Agent Kit/kit/eval_suite/manifest.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```

Validate smoke policy without writing a checklist:

```bash
python "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Agent Kit/kit/eval_suite/manifest.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke \
  --validate-only \
  --format json
```

Legacy embedded suite example:

```bash
python3 "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Agent Kit/kit/eval_suite/core_behavior_eval_cases.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```

It does not call a model API and does not grade automatically. It helps the owner start and record a manual or semi-automated eval run.


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

## v3.11.1 ContextAdvisor model routing flags

`context_advisor_preflight.py` accepts optional flags for dated provider/model routing checks:

```bash
python3 Agent\ Kit/kit/tools/context_advisor_preflight.py \
  --intent analyze \
  --have project_map_core,source_authority,memory_relevant \
  --surface chatgpt_desktop_codex \
  --settings-requested \
  --provider-snapshot-date 2026-07-10 \
  --provider-snapshot-current \
  --model-display-label "GPT-5.6-Terra" \
  --model-config-slug gpt-5.6-terra \
  --reasoning-effort medium
```

Use `--reasoning-effort`, `--delegation-mode`, `--independent-subscopes`,
`--subscope-stop-conditions`, and `--fuel-justification` to validate Max/Ultra
semantics. Use `--fast-mode` and `--fast-credit-multiplier` to expose the
GPT-5.6 public-doc/local-cache conflict and reject unsupported fixed multipliers.

`chatgpt_desktop_codex` is current for ChatGPT desktop Codex. `codex_app` is a
compatibility alias; `codex_ide`, `codex_cli`, and `codex_web` are distinct
current clients. Compact owner advice contains only surface/model/reasoning/speed.
Exact Cursor GPT-5.6 advice is rejected while the bundled Cursor snapshot is
stale and no current Cursor evidence exists.

## `generate_chatgpt_project_sources.py`

Generates a local ChatGPT Project sources manifest, deterministic context pack, and owner TODO.

- Config-driven (`CHATGPT_PROJECT_SOURCES.config.json` in the project)
- Stdlib only; no network; no ChatGPT UI automation
- Default minimal required sources; `--include-optional` for granular files
- See `CHATGPT_PROJECT_SOURCES_WORKFLOW.md`

Example (project):

```bash
python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config CHATGPT_PROJECT_SOURCES.config.json \
  --write --check
```

Package fixture self-test:

```bash
python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config "Agent Kit/kit/tools/fixtures/gpt_project_sources_minimal/config.json" \
  --write --check
```


### v3.9.3 surface/mode preflight flags

`context_advisor_preflight.py` supports `--surface`, `--cursor-mode`, `--independent-subscopes`, and `--pursue-goal` to gate Cursor/Codex/ChatGPT surface routing, Multitask, and Codex goal-style autonomy.
