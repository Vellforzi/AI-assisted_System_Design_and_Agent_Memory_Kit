# AI Development Rules

Status: Active AI workflow rule
Last aligned: <YYYY-MM-DD>
Audience: AI/Codex sessions and maintainers
Runtime impact: none; governs repository workflow only
Authority: workflow rule under `docs/source_of_truth_hierarchy.md`

---

## Required Order

1. Classify the current owner request before using backlog, handoff, or memory.
2. Read only the startup context and task-specific sources selected for that
   request.
3. Keep Project Map as secondary memory unless source authority explicitly says
   otherwise.
4. Do not mutate files, runtime state, external systems, data artifacts, commits,
   branches, deployments, or Project Map unless the current task scopes it.
5. Report read sets, skipped trigger-only context, checks, and any proposed
   memory/governance deltas.

## Implementation Boundaries

- Prefer existing project patterns over new abstractions.
- Keep changes inside the requested layer and behavior surface.
- Validate with the smallest meaningful checks for the risk touched.
- Treat generated artifacts, local databases, secrets, logs, archives, proposals,
  and research notes as skipped by default.

## Conflict Rule

When instructions conflict, current owner instructions and operational
source-of-truth docs win over secondary memory and stale handoffs.
