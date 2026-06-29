# Existing Project Context Governance Guide

Status: practical baseline for active repo-centric projects
Purpose: add Agent Kit governance to an existing project without replacing its
current documentation, runtime behavior, or project-specific agent rules.

Use this guide when the project already has useful operational docs such as
`AGENTS.md`, roadmap/status docs, source-of-truth hierarchy, context packs,
layer-specific specs, issues, or tests.

The default system for this class of project is one repo-centric secondary-memory governance behavior:

```text
Repo-Centric Context Governance Baseline
```

Use `secondary_memory_governance/` as the package source.

---

## 1. Adoption Principle

Do not begin by making the agent understand everything.

Begin by making the existing source authority, action intent, retrieval, and
domain boundaries machine-readable.

For mature existing projects, Agent Kit must reinforce the current operating
model. It must not create a parallel source of truth.

Canonical rule:

```text
Project Map summarizes and navigates.
Operational docs, code, tests, specs, issues, and current owner instructions win.
```

---

## 2. Target Baseline

Install the repo-centric context governance baseline. It keeps Project Map as
secondary memory while making context routing, receipts, and documentation
checks reproducible.

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

Optional only if Cursor is used:

```text
.cursorignore
```

Do not install these as part of the baseline:

```text
memory/
.agent-memory/
runtime memory
task tree
handoff tree
vector DB
MCP server
background capture
replacement AGENTS.md
```

---

## 3. Required Files

Copy or adapt these files from `secondary_memory_governance/`:

```text
AGENTS_SNIPPET.md
next_steps_template.md
current_status_template.md
source_of_truth_hierarchy_template.md
context_governance_rules_template.md
project_map_readme_template.md
context_index.yaml
context_selection_smoke_cases.yaml
source_authority.yaml
permissions_policy.yaml
retrieval_policy.yaml
retrieval_scoring_policy.yaml
memory_lifecycle_policy.yaml
tool_output_reference_template.yaml
working_state.yaml
current_map_template.md
memory_quality_review_bar.md
manual_smoke_cases.yaml
ai_development_rules_template.md
codex_prompt_rules_template.md
research_readme_template.md
validation_readme_template.md
.codexignore_TEMPLATE
.cursorignore_TEMPLATE
```

Copy reference tools from `tools/`:

```text
tools/context_governance_helper.py -> scripts/ai_context_helper.py
tools/documentation_harness.py -> scripts/documentation_harness.py
```

Create or update `docs/project_map/README.md` from
`project_map_readme_template.md` so it states:

- Project Map is secondary memory;
- operational docs win;
- policy YAML files are governance/advisory unless runtime enforcement exists;
- Project Map updates require explicit memory-update intent or approved delta;
- after significant work, the agent may propose memory or smoke-case deltas but
  must not apply them without scope.

Patch the existing `AGENTS.md` only with the short snippet. Do not replace a
project-specific `AGENTS.md` with the generic Agent Kit template.

---

## 4. Action Intent

Questions, reviews, analyses, and plans are non-mutating by default.

Allowed by default when needed for the current task:

- answer;
- analyze;
- review;
- plan;
- scoped read-only repository inspection;
- proposed memory delta;
- proposed smoke case.

Not allowed without explicit apply or mutation intent:

- editing files;
- updating Project Map;
- updating policy YAML;
- creating durable memory;
- running external research except for an explicit current-info need;
- committing, pushing, deploying;
- mutating databases, external-system state, credentials, accounts, or runtime
  artifacts.

Coding agents may read relevant local docs, source, and tests for the requested
task. That read-only exploration is normal and should not require a separate
ceremony, but it never authorizes writes.

---

## 5. Policy Versus Enforcement

Always label runtime capability honestly:

```text
enforced
advisory
unknown
absent
```

Rules:

- `.codexignore` is context hygiene, not a security boundary.
- `.cursorignore` is context hygiene, not a security boundary.
- `permissions_policy.yaml` is behavioral policy unless runtime enforces it.
- `ALLOWED_SCOPE.txt` is advisory unless wrapper or runtime checks
  respect it.
- broad local filesystem access must be reported as broad access.

Do not claim that policy files technically block actions unless the runtime has
been verified to enforce them.

---

## 6. Retrieval Loop

At session start, read only:

```text
AGENTS.md
docs/project_map/source_authority.yaml
docs/project_map/permissions_policy.yaml
docs/project_map/retrieval_policy.yaml
docs/project_map/working_state.yaml
```

Then follow the project-specific reading order from `AGENTS.md`.

Before answering:

1. Classify intent.
2. Identify required source authority.
3. Retrieve the smallest evidence-bearing working set.
4. Label missing, stale, or conflicting evidence.
5. Avoid unsupported project claims.

Before editing:

1. Confirm explicit apply request.
2. Confirm target scope.
3. Read relevant source-of-truth docs.
4. Check forbidden directions.
5. Define verification.

---

## 7. Domain-Boundary Smoke Cases

Start with manual smoke cases, not a full eval harness.

The baseline cases should cover:

1. Project Map does not override operational docs.
2. Private or internal context does not become public/user-facing truth.
3. Current status wins over deferred work.
4. Research notes do not directly change runtime behavior.
5. Unapproved autonomous decision behavior is not introduced.
6. Ignore files are context hygiene, not secret protection.
7. Adoption assessment does not trigger full Agent Kit installation.
8. Experimental evidence is not production readiness.
9. External-system mutations require explicit gated scope.
10. Stale Project Map memory cannot override current source-of-truth docs.

Keep these cases manual until repeated failures justify automation.

---

## 8. Acceptance Criteria

The baseline is installed correctly when a fresh agent can:

- identify the current operational priority from operational docs;
- identify deferred tracks as deferred;
- distinguish public, private/internal, validation, research, and experimental
  scopes;
- treat Project Map as secondary memory;
- prefer operational docs on conflict;
- keep questions and reviews non-mutating;
- perform scoped read-only exploration for coding tasks;
- require explicit intent for memory writes;
- keep external research as context until reviewed promotion;
- describe ignore files as context hygiene, not security;
- leave runtime code, external-system behavior, scheduler behavior, and public
  product semantics unchanged;
- use domain-boundary smoke cases to catch the highest-risk agent mistakes.

Run these local checks before considering adoption complete:

```bash
python scripts/ai_context_helper.py read-set --profile startup --format json
python scripts/ai_context_helper.py smoke-check --format json
python scripts/documentation_harness.py --format json
```

These checks reproduce the standalone repo-centric behavior: bounded context,
trigger-only secondary sources, high-risk exclusions, retrieval receipts,
read-only API-agent context shape, and report-only documentation governance.

Stop after these criteria are met unless the owner explicitly requests runtime
memory, task trees, handoff trees, vector databases, MCP servers, background
capture, or other heavier infrastructure.

---

## 9. Optional Integrations

Use optional integrations only after the core baseline passes.

| Need | Module |
|---|---|
| ChatGPT Project should receive a small, reproducible source set | `optional_integrations/chatgpt_project_sources/` |
| Owner wants cost/model/reasoning guidance | `optional_integrations/cost_model_routing/` |
| Cursor is the local implementation surface | `optional_integrations/cursor_settings/` |

These modules must not become required startup context. They are project-tool
adapters around the core baseline.
