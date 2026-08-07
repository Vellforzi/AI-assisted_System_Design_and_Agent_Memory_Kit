# Agent Memory Kit Tools

This folder contains helper scripts. They are optional for the general kit, but
the repo-centric context governance baseline uses the context helper and
documentation harness when a project wants repo-centric secondary-memory local checks.

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

## `context_contract_v1_oracle.py`

Validates the language-independent Context Contract V1 schemas, examples, and
canonical smoke corpus. It reuses `context_governance_helper.py` to parse the
existing context-selection smoke ids and reads the existing retrieval policy
for lifecycle exclusions. It uses only the Python standard library and does
not start a service or persist context.

```bash
python3 "Agent Kit/kit/tools/context_contract_v1_oracle.py" --format json
```

See `secondary_memory_governance/context_contract_v1/README.md` for Python and
TypeScript adapter guidance.

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

## Optional integration tools

The ChatGPT Project sources generator is intentionally outside this `tools/`
folder:

```text
Agent Kit/kit/optional_integrations/chatgpt_project_sources/generate_chatgpt_project_sources.py
```

It is an export workflow for owners who use ChatGPT Project, not part of the
core repo-centric governance helper set.

## v4 dependency-free helpers

- `project_artifact_contract_oracle.py` validates strict schemas, examples, and cross-contract invariants.
- `context_budget_audit.py` reports source/token budgets and caller-supplied baseline growth without retaining history.
- `migrate_v38_artifact.py` prints a conservative v4 proposal and never overwrites a v3.8 source.
- `generate_checksums.py` verifies `SHA256SUMS.txt` by default; `--write` explicitly regenerates it while excluding caches and the checksum file itself.

## v5 dependency-free helpers

- `project_artifact_contract_v2_oracle.py` validates V2 schemas plus DAG/frontier, workflow activation, owner, evidence, isolation, and lifecycle invariants.
- `workflow_projection_helper.py` reports work/exploration frontiers, current capability status, and triage readiness; it never selects, activates, or persists work.
- `migrate_v4_artifact.py` prints a conservative reviewed v5 proposal and never changes the v4 source.
