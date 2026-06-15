# Existing Project Governance Overlay Guide

Status: practical baseline for active repo-centric projects
Purpose: add Agent Kit governance to an existing project without replacing its
current documentation, runtime behavior, or project-specific agent rules.

Use this guide when the project already has useful operational docs such as
`AGENTS.md`, roadmap/status docs, source-of-truth hierarchy, context packs,
layer-specific specs, issues, or tests.

The default system for this class of project is:

```text
Reusable Secondary-Memory Governance System
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

## 2. Target Overlay

Install only the governance overlay unless the owner explicitly requests more.

```text
<Project Root>/
  AGENTS.md
  .codexignore
  docs/
    project_map/
      README.md
      current_map.md
      source_authority.yaml
      permissions_policy.yaml
      retrieval_policy.yaml
      working_state.yaml
      eval_suite/
        manual_smoke_cases.yaml
```

Optional only if Cursor is used:

```text
.cursorignore
```

Do not install these as part of the baseline overlay:

```text
memory/
.agent-memory/
runtime memory
full eval harness
task tree
handoff tree
replacement AGENTS.md
```

---

## 3. Required Files

Copy or adapt these files from `secondary_memory_governance/`:

```text
source_authority.yaml
permissions_policy.yaml
retrieval_policy.yaml
working_state.yaml
manual_smoke_cases.yaml
.codexignore_TEMPLATE
.cursorignore_TEMPLATE
AGENTS_SNIPPET.md
```

Create or update `docs/project_map/README.md` so it states:

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

The overlay is installed correctly when a fresh agent can:

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

Stop after these criteria are met unless the owner explicitly requests a larger
memory/runtime system.
