# Repo-Centric Context Governance Baseline

Status: reusable baseline package
Purpose: reproduce the stockanalyst-style AI working behavior in any
repo-centric project without copying adopter-specific domain facts.

This package is the default Agent Memory Kit behavior for existing projects
that already have or can add operational repository docs.

Canonical rule:

```text
Project Map summarizes and navigates.
Operational docs, code, tests, specs, issues, and current owner instructions win.
```

The baseline combines:

- secondary Project Map memory;
- operational source-of-truth hierarchy;
- task-local scope gate;
- machine-readable `context_index.yaml`;
- bounded read-set selection;
- retrieval receipts;
- context-selection smoke cases;
- report-only documentation harness checks;
- high-risk context exclusions for data, logs, local databases, secrets, and
  raw external-system payloads.

This is one behavior, not two modes. Projects may simplify pieces only when
they deliberately do not need stockanalyst-style reproducibility.

---

## Target Project Layout

Copy or adapt these files into the target project:

```text
<Project Root>/
  AGENTS.md
  .codexignore
  docs/
    NEXT_STEPS.md
    source_of_truth_hierarchy.md
    context_governance_rules.md
    context_packs/
      current_status.md
    research/
      README.md
    validation/
      README.md
    project_map/
      README.md
      context_index.yaml
      current_map.md
      source_authority.yaml
      permissions_policy.yaml
      retrieval_policy.yaml
      retrieval_scoring_policy.yaml
      memory_lifecycle_policy.yaml
      tool_output_reference_template.yaml
      working_state.yaml
      memory_quality_review_bar.md
      eval_suite/
        manual_smoke_cases.yaml
        context_selection_smoke_cases.yaml
    rules/
      ai_development_rules.md
      codex_prompt_rules.md
  scripts/
    ai_context_helper.py
    documentation_harness.py
```

Use `.cursorignore` only if Cursor is used.

The baseline does not require:

```text
memory/
.agent-memory/
runtime memory
task tree
handoff tree
replacement AGENTS.md
vector DB
MCP server
background capture
```

---

## Package File Responsibilities

`AGENTS_SNIPPET.md`

- patch for the existing project-specific `AGENTS.md`;
- adds task-local scope, startup context, skipped-by-default context, and
  reporting requirements;
- must not replace the project's own instruction file.

`next_steps_template.md`

- template for `docs/NEXT_STEPS.md`;
- records the active priority, explicit non-goals, startup handoff, open
  questions, and next checks.

`current_status_template.md`

- template for `docs/context_packs/current_status.md`;
- gives fresh sessions a compact operational status summary without becoming
  higher authority than current owner instructions, code, or specs.

`source_of_truth_hierarchy_template.md`

- template for `docs/source_of_truth_hierarchy.md`;
- defines authority tiers, reachability rules, navigation order, Project Map
  secondary status, and archive/research limits.

`context_governance_rules_template.md`

- template for `docs/context_governance_rules.md`;
- defines task-local scope gate, minimal retrieval discipline, docs lifecycle,
  link lifecycle, session-context promotion, and Project Map boundaries.

`context_index.yaml`

- template for `docs/project_map/context_index.yaml`;
- routes agents to conservative P0/P1 read sets by task profile;
- marks trigger-only and high-risk context;
- does not grant source authority or mutation permission.

`context_selection_smoke_cases.yaml`

- template for
  `docs/project_map/eval_suite/context_selection_smoke_cases.yaml`;
- verifies startup, docs-only, review, Project Map update, and research read
  sets;
- fails when required indexed files are missing from the installed project;
- should be extended with domain-specific forbidden paths and boundaries.

`project_map_readme_template.md`

- template for `docs/project_map/README.md`;
- states Project Map secondary-memory role, file responsibilities, and update
  rules.

`source_authority.yaml`

- records source-of-truth order;
- states that Project Map is secondary memory;
- defines conflict behavior;
- gates external research promotion into project facts.

`permissions_policy.yaml`

- records default answer-only intent;
- allows scoped read-only coding-agent exploration;
- separates answer/analyze/review/plan from apply/mutation;
- labels runtime capability as enforced, advisory, unknown, or absent.

`retrieval_policy.yaml`

- keeps context intake small;
- requires operational source-of-truth before relying on Project Map;
- prevents whole-repo and whole-Project-Map loading by default;
- labels stale Project Map content as context, not truth.

`retrieval_scoring_policy.yaml`

- requires hard gates before scoring;
- prevents similarity, entity links, or embeddings from overriding authority;
- requires result metadata such as status, evidence refs, authority, freshness,
  and truncation state.

`memory_lifecycle_policy.yaml`

- defines candidate-first durable memory lifecycle rules;
- blocks stale, superseded, rejected, and archived records from normal current
  truth profiles;
- defines candidate inbox, episodic event, and tool-use lesson rules.

`tool_output_reference_template.yaml`

- stores compact references to long tool outputs;
- keeps raw output out of always-loaded memory;
- requires sensitivity and retention metadata.

`working_state.yaml`

- gives fresh sessions a compact replay root;
- points to current operational entrypoints;
- records drift markers;
- must not become a planning document or override operational docs.

`current_map_template.md`

- template for `docs/project_map/current_map.md`;
- records secondary facts, decisions, hypotheses, risks, open questions, and
  drift notes that must be verified against operational sources.

`memory_quality_review_bar.md`

- gives reviewers a strict bar for memory, retrieval, permission, and
  governance changes;
- prevents silent auto-capture, weak source authority, stale truth leakage, and
  evidence-free project claims.

`manual_smoke_cases.yaml`

- protects portable governance and domain-boundary behavior;
- tests agent behavior rather than runtime code.

`codex_prompt_rules_template.md`

- template for bounded Codex prompts with required read set, mutation scope,
  out-of-scope boundaries, checks, and receipt requirements.

`ai_development_rules_template.md`

- template for `docs/rules/ai_development_rules.md`;
- records executable AI workflow boundaries for request classification, scoped
  reads, mutation gates, and conflict handling.

`research_readme_template.md`

- template for `docs/research/README.md`;
- keeps research as evidence/context until reviewed promotion.

`validation_readme_template.md`

- template for `docs/validation/README.md`;
- records local checks and validation evidence boundaries.

`.codexignore_TEMPLATE` and `.cursorignore_TEMPLATE`

- reduce context noise and accidental exposure;
- are context hygiene only, not security boundaries.

Reference scripts:

```text
tools/context_governance_helper.py -> scripts/ai_context_helper.py
tools/documentation_harness.py -> scripts/documentation_harness.py
```

The helper scripts are local, read-only reference implementations. They are not
runtime memory, not security boundaries, and not external services.

---

## Operating Loop

At session start, read the operational startup context from `AGENTS.md`:

```text
AGENTS.md
docs/NEXT_STEPS.md
docs/source_of_truth_hierarchy.md
docs/context_packs/current_status.md
```

Then classify the task and read only task-specific docs, code, tests, specs, or
Project Map policy files.

Before answering:

1. Classify intent.
2. Identify source authority.
3. Apply task-local scope before global backlog fallback.
4. Apply retrieval hard gates before scoring.
5. Retrieve the smallest evidence-bearing working set.
6. Label missing, stale, trigger-only, or conflicting evidence.
7. Avoid unsupported project claims.

Before editing:

1. Confirm explicit apply intent and mutation scope.
2. Confirm target files/layers.
3. Read relevant source-of-truth docs.
4. Check forbidden paths and boundaries.
5. Define verification.
6. Produce a receipt after non-trivial work.

After significant work, the agent may propose a Project Map delta,
working-state update, smoke case, or source-authority repair note. It must not
apply those memory or governance updates unless the task explicitly includes
them.

---

## Acceptance Checks

After installation in a target project:

```bash
python scripts/ai_context_helper.py read-set --profile startup --format json
python scripts/ai_context_helper.py smoke-check --format json
python scripts/documentation_harness.py --format json
```

Pass means:

- all files required by the selected read sets exist in the target project;
- startup context is bounded;
- trigger-only Project Map/research/archive context is skipped by default;
- high-risk context is excluded by default;
- source authority and status metadata are visible;
- documentation harness is report-only;
- runtime, external-system, data, and Project Map scope are not expanded.

These checks prove workflow reproducibility, not product correctness.

---

## Project-Local Profiles

Concrete adopter data belongs in the adopting project, not in this reusable kit.

When adapting this baseline:

- keep project-specific `AGENTS.md`;
- keep operational docs as truth;
- replace all project ids, paths, current priorities, domain boundaries, and
  smoke cases;
- add domain-specific smoke cases for the project risks;
- do not copy project-specific runtime assumptions into unrelated projects or
  back into this reusable kit.
