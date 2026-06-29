# Context Governance Rules

Status: Active docs-governance rule
Last aligned: <YYYY-MM-DD>
Audience: future AI/Codex sessions and maintainers
Runtime impact: none; governs repository documentation and context promotion only
Authority: docs-governance rule under `docs/source_of_truth_hierarchy.md`

---

## Purpose

This document defines preventive rules for:

- task-local scope selection;
- minimal retrieval discipline;
- documentation file lifecycle;
- link and reachability lifecycle;
- promotion of session context into canonical long-term memory;
- preserving Project Map as secondary memory unless explicitly scoped.

It does not authorize runtime changes, Project Map updates, external-system
mutations, database mutations, commits, pushes, deployments, product launch,
autonomous decisions, or readiness approvals.

---

## Task-Local Scope Gate

Before choosing the current action, apply the explicit scope of the user's
current request.

Task-local scope controls current action selection:

- `docs-only` scope authorizes documentation edits, proposed deltas, and
  documentation checks only.
- `review` scope authorizes read-only inspection and review findings only
  unless the owner explicitly asks for fixes.
- `research` scope authorizes evidence collection, synthesis, and non-runtime
  recommendations only.
- `planning` scope authorizes plans, scope definitions, and proposed deltas
  only.
- `implementation` scope authorizes only the scoped files/layers requested by
  the owner and source-of-truth docs.
- `memory-update` scope authorizes Project Map edits only for the approved
  delta.

The global next step in roadmap, status, Project Map, or handoff docs is a
fallback only when the owner asks to continue implementation or provides no
narrower task-local scope.

A task-local scope can narrow current action. It cannot authorize a scope
expansion that operational docs forbid.

---

## Minimal Retrieval Discipline

After applying the Task-Local Scope Gate, use progressive disclosure rather
than broad context loading.

Rules:

- Read required operational entrypoints first.
- Add only task-specific docs, code, tests, specs, rules, or Project Map policy
  files needed for the current layer and action.
- Treat deep or secondary sources as trigger-only.
- Exclude high-risk context by default: `data/**`, raw logs, local databases,
  `.env*`, secrets, generated artifacts, raw external-system payloads, and
  private identifiers.
- Use secondary `docs/project_map/context_index.yaml` and the local context
  helper for repeatable read-set selection when available.
- Retrieval/search backends may rank only the bounded candidate set after
  task-profile, source-authority, lifecycle/status, and permission filters.

---

## Documentation File Lifecycle

Before creating a documentation file:

1. Identify the file role: operational source-of-truth, layer spec, validation,
   research, knowledge, governance, Project Map, archive, template, or
   evidence.
2. Confirm the file improves implementation, review, validation, onboarding, or
   drift prevention.
3. Add freshness and authority metadata when the file is active:

```text
Status:
Last aligned:
Audience:
Runtime impact:
Authority:
```

4. Add an inbound reference from an already discoverable repository doc in the
   same change.
5. State whether the file is operational, advisory, planning-only, evidence, or
   archive.

Do not create a new active doc only for completeness.

---

## Link Lifecycle

Every active doc link is a retrieval path for future agents.

Rules:

- Add links from stable entrypoints, layer indexes, or parent READMEs.
- Do not rely on directory traversal or search-only discovery for active docs.
- When renaming, moving, archiving, or deleting a doc, update references to the
  old path.
- Do not link archive docs as active source-of-truth.
- If a link points to a planning, proposal, archive, research, or Project Map
  file, label its authority.

Minimum check after touching links:

```bash
rg -n "old_path|new_path" AGENTS.md README.md docs
```

---

## Session Context Promotion

Session context is not durable project truth by default.

Session context includes:

- chat instructions and decisions;
- tool output;
- command output;
- local observations;
- generated summaries;
- proposed deltas;
- temporary task plans.

Promotion requires:

1. explicit owner scope or approved proposed delta;
2. source path, reviewed decision, sanitized artifact reference, or compact
   command/tool output reference;
3. conflict check against operational source-of-truth docs;
4. sensitivity review for secrets, tokens, private data, raw logs, and raw
   external-system payloads;
5. authority label;
6. inbound link if a new doc is created;
7. no scope expansion from tests, replay, sandbox evidence, or docs cleanup;
8. next-step impact check: if the result changes what a future agent should do
   next, update `docs/NEXT_STEPS.md`,
   `docs/context_packs/current_status.md`, and the relevant
   roadmap/status/spec entrypoint in the same reviewed docs-governance or
   implementation scope.

Evidence records are the proof base. They are not the only durable carrier for
next-step-critical state. Do not leave the current next action, completed phase,
required read set, or roadmap/spec direction only in evidence notes, raw tool
output, temporary artifacts, or chat memory.

Never promote raw secrets, tokens, private identifiers, raw logs, or external
payloads into durable memory.

---

## Project Map Boundary

Project Map remains secondary memory and navigation.

For Project Map tasks:

- read Project Map policy files when source authority, permission, retrieval,
  memory lifecycle, or working-state questions are in scope;
- do not update Project Map unless the owner explicitly scopes a memory update
  or approves a proposed Project Map delta;
- if Project Map conflicts with operational docs, follow operational docs and
  report the drift;
- if Project Map content should affect implementation, architecture, safety,
  validation workflow, runtime behavior, or product scope, promote the relevant
  claim into an operational doc or layer spec first.
