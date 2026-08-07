# Documentation Governance (optional)

Status: optional integration; inactive until explicit owner adoption
Runtime impact: none
Authority: documentation-placement and review policy only; subordinate to the
adopting project's operational sources and to the Kit's
`secondary_memory_governance/` baseline

## Purpose

This module supplies a compact, adoptable policy for separating current
knowledge, current requirements, immutable history, and short-lived execution
state. It does not install hooks, change runtime behavior, replace the
secondary-memory baseline, or grant write permission.

An owner adopts it by deliberately copying or referencing the policy in the
target project and assigning local owners and checks. Until then it is only
reference material.

## Knowledge zones and authority

| Zone | Knowledge mode | Authority and handling |
| --- | --- | --- |
| `docs/` | Current state | Operational documentation for how the project currently works. Current code, tests, owner instructions, and other operational sources still win when they conflict. |
| `specs/active/` | Current requirements | The current approved requirement set. It governs intended change scope; reconcile it with operational evidence before claiming present runtime behavior. |
| `specs/archive/` | Immutable history | Superseded or completed specifications. Preserve content and identity; do not revise it to reflect later understanding. |
| `docs/adr/` | Immutable history | Accepted decision records. Amend only through a new ADR that supersedes or clarifies the old one; do not silently rewrite accepted history. |
| `.work/` | Ephemeral execution state | Task-local notes, drafts, scratch output, and resumable execution context. It is non-authoritative and must be promoted deliberately before it informs durable documentation. |

`docs/project_map/` (when present) is secondary navigation and memory. It may
summarize, index, and route readers, but it cannot override an operational
source, active spec, code, test, or current owner instruction.

## Conflict and promotion rules

1. Determine the question: present behavior, current requirement, historical
   record, or task-local execution state.
2. Read the matching zone, then verify against higher-authority operational
   evidence where applicable.
3. Report unresolved conflicts; never resolve them by editing history or a
   Project Map summary.
4. Promote durable facts from `.work/` only through an explicit, reviewed
   update to the appropriate `docs/` or `specs/active/` source.
5. Preserve archive and ADR records as historical evidence; create a linked
   successor when a decision or requirement changes.

## Generated blocks

A generated block must have one named authoritative generator and a stable
marker or equivalent local convention. The generator owns the block's content;
human edits inside it are not durable unless the generator's source is updated
and regeneration is explicitly performed. Surrounding prose remains
human-owned unless the project declares otherwise.

Do not treat generated output as a separate authority. The source data and the
operational source it represents remain authoritative. A failed or unavailable
generation is a review signal, not permission to overwrite the block manually.

## Metadata and checks

Use [docs_metadata_policy.json](docs_metadata_policy.json) for optional,
additive metadata rules. `last_verified` records when the document's relevant
claims were last checked against its required evidence; it is not a freshness
guarantee, a replacement for evidence, or a mandatory field on every document.

Use [checks_registry.json](checks_registry.json) as the stable registry of
checks emitted by the optional CLI. Stable check IDs allow an adopter to
automate reporting without making this module a runtime dependency. Broader
authority questions such as whether prose matches code or whether archived
history was improperly rewritten remain policy-review concerns; the local CLI
does not claim to prove them. Checks are report-only unless an owner explicitly
adopts enforcement in that project.

## Adoption boundary

Keep the Kit's source-authority and mutation rules intact. This optional module
does not require a language policy, a branching model, or a fixed number of
frontmatter fields. It changes no runtime behavior until an owner explicitly
adopts a local policy and implementation.
