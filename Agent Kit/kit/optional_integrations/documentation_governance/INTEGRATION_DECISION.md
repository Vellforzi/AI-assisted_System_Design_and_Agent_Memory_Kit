# Documentation Governance Integration Decision

Decision: provide documentation-governance guidance as an optional, standalone
module.

Status: accepted for optional adoption
Default activation: off
Runtime behavior: unchanged

## Context

Projects benefit from a consistent distinction between current state, current
requirements, immutable records, and task-local execution material. That
distinction must coexist with the Kit's repo-centric source-authority model:
Project Map is secondary navigation, while operational sources win.

## Decision

The module defines these zones:

- `docs/` is current-state documentation.
- `specs/active/` is the current requirements zone.
- `specs/archive/` and `docs/adr/` are immutable-history zones.
- `.work/` is ephemeral execution state and never becomes durable authority by
  itself.

The explicit zone-to-authority mapping is maintained in
`docs_metadata_policy.json`; the human-readable form is in the README. The
module supplies a stable, report-only check registry and optional metadata
policy, including `last_verified`.

Generated blocks have a single authoritative generator. Their source is the
durable point of change; manually editing generated content does not establish
authority. The project must make block boundaries and generator ownership
identifiable before relying on generated content.

## Consequences

- `docs/project_map/` remains secondary navigation. Its summaries and indexes
  cannot settle conflicts with operational docs, code, tests, active specs, or
  current owner instructions.
- Current requirements may describe intended future behavior; they do not by
  themselves prove current runtime behavior.
- Historical records stay intact. New ADRs or successor specifications carry
  later decisions instead of rewriting the prior record.
- `.work/` may aid execution and recovery but must be explicitly promoted and
  reviewed before it changes a current-state or requirements source.
- Adoption is owner-controlled. The module neither replaces
  `secondary_memory_governance/` nor becomes active by default.

## Non-decisions

This integration intentionally does not prescribe a Russian-only language rule,
feature/development/main branching policy, or exactly two frontmatter fields
for every document. It also does not add runtime hooks, automatic rewrites, or
enforcement without explicit project-level adoption.
