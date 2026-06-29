# Source Of Truth Hierarchy

Status: Active repository navigation rule
Last aligned: <YYYY-MM-DD>
Audience: owner, AI/Codex sessions, future API-agent work
Runtime impact: none
Authority: repository source-of-truth hierarchy for documentation authority and retrieval priority

---

## Purpose

This document defines:

- which documents are operational source-of-truth;
- which docs are navigation indexes;
- which docs are historical, research, proposal, or archive context;
- which docs AI/Codex should use first.

Goal:

- reduce documentation drift;
- reduce duplicated planning;
- reduce stale context;
- reduce AI confusion;
- make context selection reproducible.

---

## Main Rule

```text
Repository operational docs, code, tests, specs, issues, and current owner
instructions are project truth.

Project Map is secondary memory and navigation unless this document says
otherwise.
```

If a document affects implementation, architecture, runtime behavior, safety,
permissions, task decomposition, validation workflow, or AI/Codex behavior, it
belongs in repository Markdown or tracked project files.

---

## Documentation Reachability Rule

Do not create an active repository documentation file unless the same change
adds an inbound reference to that file from an already discoverable repository
doc.

Valid inbound reference targets include:

- `AGENTS.md`;
- `README.md`;
- `docs/NEXT_STEPS.md`;
- this file;
- a relevant operational source-of-truth doc;
- a relevant layer index;
- a relevant parent `README.md`.

Directory traversal, search-only discovery, or "the file exists in Git" is not
enough.

---

## Authority Tiers

### Tier 1 - Primary Operational Docs

Use these first:

```text
AGENTS.md
docs/NEXT_STEPS.md
docs/source_of_truth_hierarchy.md
docs/context_packs/current_status.md
<project-specific roadmap/status/spec entrypoints>
```

These define current priority, source authority, action boundaries, and current
operational state.

### Tier 2 - Secondary Navigation Indexes

Use these secondary, lower-authority indexes to avoid reading scattered docs
unnecessarily:

```text
README.md
docs/project_map/context_index.yaml  # secondary lower-authority navigation
docs/validation/README.md
docs/research/README.md
docs/specs/README.md
docs/architecture/README.md
```

Indexes route agents. They do not override Tier 1 docs.

### Tier 3 - Layer-Specific Specs

Use relevant specs after the task profile is known:

```text
docs/specs/**
docs/architecture/**
docs/validation/**
```

Specs define bounded implementation behavior only for their layer.

### Tier 4 - Knowledge And Research

Research and knowledge files are context, evidence, hypotheses, or accepted
syntheses. They are not implementation authority until promoted into a Tier 1
or Tier 3 source through reviewed scope.

Evidence can prove why a state changed, but it is not the primary carrier for
what a fresh agent should do next. When evidence changes the active next step,
current phase, required read set, or roadmap/spec direction, promote the compact
state into `docs/NEXT_STEPS.md`, `docs/context_packs/current_status.md`, and
the relevant roadmap/status/spec entrypoint in the same scoped task.

### Tier 5 - Project Map

Project Map preserves owner memory, navigation metadata, working state, risks,
open questions, handoff notes, and drift markers.

It does not override operational docs.

### Archive

Archive docs are historical context only. They must not remain linked as active
implementation instructions.

---

## AI/Codex Navigation Order

At the start of a non-trivial task:

1. Read `AGENTS.md`.
2. Read `docs/NEXT_STEPS.md`.
3. Read `docs/source_of_truth_hierarchy.md`.
4. Read `docs/context_packs/current_status.md`.
5. Apply the task-local scope gate in `docs/context_governance_rules.md`.
6. Use secondary `docs/project_map/context_index.yaml` or the local context
   helper for bounded read-set selection when context routing is in scope.
7. Read only task-specific docs, code, tests, specs, or Project Map policy
   files.

Do not read the whole repository, Project Map, archive, research corpus, local
data, raw logs, local databases, secrets, or environment files by default.

---

## Anti-Drift Rule

Do not maintain the same operational rule in multiple active docs. Prefer one
canonical source plus links.

When source authority, priority, or active boundaries change:

1. update the canonical operational doc;
2. update the closest navigation index;
3. update compact current status when handoff context changed;
4. update `docs/NEXT_STEPS.md` when the next safe action changed;
5. report Project Map drift unless memory-update scope is explicit.
