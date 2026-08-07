# Documentation Governance Adoption and Rollback Guide

Status: optional guidance; inactive until explicit owner adoption

## Before adoption

Adopt this module only when the target project needs an explicit policy for
current documentation, active requirements, immutable records, and ephemeral
work state. It is an addition to, not a replacement for,
`secondary_memory_governance/`. Keep the baseline source-authority and
mutation rules in force: operational sources and current owner instructions
remain authoritative, while `docs/project_map/` remains secondary navigation.

This Kit is language-agnostic and does not require Python. The optional
`tools/documentation_governance.py` helper is a dependency-free Python 3
convenience tool for adopters who choose to run its checks; it is not a core
Kit dependency, runtime component, or required adoption step.

Before changing the target project, an owner should approve the local scope,
the zone mapping, the local policy owner, the review path, and whether checks
remain report-only or become locally enforced. Review
[README.md](README.md), [INTEGRATION_DECISION.md](INTEGRATION_DECISION.md), and
[WORK_MODEL_MAPPING.md](WORK_MODEL_MAPPING.md) with the target project's
operational sources.

## Adopt deliberately

1. Copy or locally reference only the needed policy, templates, and optional
   check configuration. Do not replace the project's existing instructions,
   source-authority policy, or documentation structure wholesale.
2. Map local locations to `docs/`, `specs/active/`, `specs/archive/`,
   `docs/adr/`, and `.work/`; document any intentional local equivalents.
   Preserve immutable records and use linked successors for later decisions or
   requirements.
3. If using generated projections, identify their sole generator and add
   unambiguous paired markers only to files whose generated regions are
   locally approved. Keep `.work/<change-id>/TASKS.md` as the sole
   operational-status authority; projections may route readers to it but must
   not duplicate status.
4. If choosing the optional Python helper, run `init` once in the target
   project, review the created `.documentation-governance.json`, then run
   `check` before enabling any automation. `check` is read-only. Use `fix`
   only after review; it changes only text inside existing paired markers.
5. Keep enforcement report-only until the owner has reviewed findings and
   explicitly chosen a project-local enforcement policy. Hooks, CI examples,
   MkDocs configuration, and the optional `just` templates are examples, not
   installation requirements. Merge the documentation recipes into the
   project's existing `justfile`; preserve its real `check-contracts`,
   `check-context`, and `check-work` targets. The template deliberately does
   not provide dummy replacements for project-specific gates.

## Validate adoption

Record the local owner decision and verify that:

- Project Map summaries are still secondary to operational docs, code, tests,
  active requirements, and current owner instructions.
- Current requirements are not presented as proof of current runtime behavior.
- Archived specifications and ADRs are preserved rather than silently edited.
- Durable facts originating in `.work/` have an explicit reviewed promotion.
- Every generated block has one named generator and an identified source of
  change.
- Optional tooling can be removed without changing core Kit behavior.

## Roll back safely

An owner may stop using this module at any time. First disable any local hook,
CI job, site build, or task runner entry that invokes it. Retain project
documentation and immutable history; the module does not authorize deleting
or rewriting them.

Then remove only the local configuration, markers, templates, and automation
that were added specifically for this integration. Before removing generated
markers, preserve any useful generated text as ordinary human-owned
documentation or regenerate it from its authoritative source. Do not delete
`.work/` material solely to roll back this module; follow the project's normal
retention policy. Finally, rerun the project's baseline governance checks to
confirm that `secondary_memory_governance/` remains intact and that no
navigation points to removed optional tooling.
