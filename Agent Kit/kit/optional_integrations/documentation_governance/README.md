# Documentation Governance (optional)

Status: optional integration; inactive until explicit owner adoption
Runtime impact: none
Authority: documentation-placement and review policy only; subordinate to the
adopting project's operational sources and to the Kit's
`secondary_memory_governance/` baseline

## Purpose

This module supplies a compact, adoptable policy for separating current
knowledge, current requirements, immutable history, and temporary execution
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
| `.work/` | Ephemeral execution state | An explicitly activated change process for task-local notes and resumable context. It is non-authoritative for product facts and requires deliberate promotion before informing durable documentation. |

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
4. Promote durable facts from activated `.work/` only through an explicit,
   reviewed update to the appropriate `docs/` or `specs/active/` source.
5. Preserve archive and ADR records as historical evidence; create a linked
   successor when a decision or requirement changes.

## Temporary-work activation

Create `.work/<change-id>/` only when at least one observable need applies:
resumable multi-session work, coordination among multiple executors, more than
three independently verifiable slices, high-risk acceptance, or a requested
audit trail. It is not a default task folder for routine single-session work.

When this process is activated, `TASKS.md` is the sole authority for that
change's operational task status. The minimal folder may contain only
`TASKS.md` and `ACCEPTANCE.md`; add `PLAN.md`, `DEVIATIONS.md`, or `artifacts/`
only when their specific purpose is needed. Outside an activated `.work`
process, task status remains in the adopting project's existing operational
system.

## Reference Lab: generated blocks

Generated-block patterns and generators are Reference Lab examples outside the
normal policy install path. If an owner separately evaluates one, apply the
following ownership rule:

A generated block must have one named authoritative generator and a stable
marker or equivalent local convention. The generator owns the block's content;
human edits inside it are not durable unless the generator's source is updated
and regeneration is explicitly performed. Surrounding prose remains
human-owned unless the project declares otherwise.

Do not treat generated output as a separate authority. The source data and the
operational source it represents remain authoritative. A failed or unavailable
generation is a review signal, not permission to overwrite the block manually.

## Metadata and Reference Lab material

Use [docs_metadata_policy.json](docs_metadata_policy.json) for optional,
additive, role-specific metadata rules. Choose fields only when they suit the
document's role; no universal frontmatter shape is required. `last_verified`
records when the document's relevant claims were last checked against its
required evidence; it is not a freshness guarantee, a replacement for
evidence, or a mandatory field on every document.

Use [checks_registry.json](checks_registry.json) as the stable registry for
the report-only checker kept as a Reference Lab example. Stable check IDs allow
an adopter to evaluate or automate local reporting without making this module
a runtime dependency. Broader authority questions such as whether prose
matches code or whether archived history was improperly rewritten remain
policy-review concerns; the local CLI does not claim to prove them.

Hooks, CI variants, MkDocs, just recipes, fixtures, generators, and full
pilots are also Reference Lab examples. They remain available for a separately
owned evaluation or integration decision, but are outside the normal policy
install path and add no enforcement by their presence.

## Lifecycle engine for mature corpora

Repositories with observable navigation drift, mixed active/history corpora,
or materially growing full-scan cost may separately adopt the portable
[`engine/`](engine/) implementation. It adds four explicit lifecycle states,
exactly-one classification, Git index and merge-base snapshots, active/history
body selection, successor and moved-path invariants, expiring exceptions, and
finding-delta gates.

This is a higher-cost Reference Lab profile, not an upgrade silently applied to
Core, Standard, or Workflow. Lifecycle is independent from authority: the
zones above still determine how a document may be used, while the lifecycle
registry determines whether it is current, supporting, historical, or
superseded. Adoption starts with a repository-specific inventory and
report-only pilot; another project's paths, counts, entrypoints, exceptions,
and baseline values are never defaults.

The engine includes an Orchestrator `DocumentationGovernancePolicyV1`
template. Orchestrator owns task scoping and execution of required gates; the
repository-owned engine remains the oracle that detects prohibited findings.

## Adoption boundary

Keep the Kit's source-authority and mutation rules intact. This optional module
does not require a language policy, a branching model, or a fixed number of
frontmatter fields. It changes no runtime behavior until an owner explicitly
adopts a local policy and implementation.
