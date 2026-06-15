# Reusable Secondary-Memory Governance Overlay

Status: reusable baseline package
Purpose: add a small governance overlay to an existing repo-centric project that
already has operational documentation and project-specific agent instructions.

This package is for projects where the Project Map is useful as navigation and
owner memory, but must not replace stronger operational docs, specs, tests,
code, issues, or current owner instructions.

Canonical rule:

```text
Project Map summarizes and navigates.
Operational docs, code, tests, specs, issues, and current owner instructions win.
```

## What This Package Adds

Copy or adapt only these files:

```text
docs/project_map/
  README.md
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

.codexignore
AGENTS.md snippet
```

Use `.cursorignore` only if Cursor is used.

This package does not require:

```text
memory/
.agent-memory/
runtime memory/tooling
full eval harness
task tree
handoff tree
replacement AGENTS.md
```

## File Responsibilities

`source_authority.yaml`

- records the source-of-truth order;
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
- prevents whole-repo loading by default;
- labels stale Project Map content as context, not truth.

`retrieval_scoring_policy.yaml`

- requires hard gates before scoring;
- prevents similarity or entity matches from overriding source authority;
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
- must not become a planning document.

`memory_quality_review_bar.md`

- gives reviewers a strict bar for memory, retrieval, permission, and governance
  changes;
- prevents silent auto-capture, weak source authority, stale truth leakage, and
  evidence-free project claims.

`manual_smoke_cases.yaml`

- protects against portable governance and domain-boundary agent failures;
- stays lightweight and manual;
- tests agent behavior rather than runtime code.

`.codexignore_TEMPLATE` and `.cursorignore_TEMPLATE`

- reduce context noise and accidental exposure;
- are context hygiene only, not security boundaries.

`AGENTS_SNIPPET.md`

- small patch for an existing project-specific `AGENTS.md`;
- must not replace the project's existing instruction file.

## Operating Loop

At session start, read only the minimum entrypoints:

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
2. Identify source authority.
3. Apply retrieval hard gates before scoring.
4. Retrieve the smallest evidence-bearing working set.
5. Label missing, stale, or conflicting evidence.
6. Claim-check material project assertions.
7. Avoid unsupported project claims.

Before editing:

1. Confirm explicit apply intent.
2. Confirm target scope.
3. Read relevant source-of-truth docs.
4. Check forbidden directions.
5. Define verification.

After significant work, the agent may propose a Project Map delta, working-state
update, smoke case, or source-authority repair note. It must not apply those
memory or governance updates unless the task explicitly includes them.

For memory proposals, use candidate-first behavior. Do not silently promote a
tool result, chat fragment, external research note, or model inference into
current durable memory.

## Project-Local Profiles

Concrete adopter data belongs in the adopting project, not in this reusable kit.
Project-local profiles can be useful as fixtures for that project, but they
must not become portable baseline defaults.

This directory intentionally has no `examples/` or `profiles/` subtree for a
concrete project. Keep downstream project ids, runtime paths, current
priorities, private boundaries, and project-only smoke cases outside this
package.

When creating a project-local profile:

- keep project-specific `AGENTS.md`;
- keep operational docs as truth;
- install Project Map policy as secondary memory unless the target project
  explicitly chooses another authority mode;
- replace all project ids, paths, current priorities, domain boundaries, and
  smoke cases;
- do not copy project-specific runtime assumptions into unrelated projects or
  back into this reusable kit.
