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
Reference Lab convenience tool for adopters who separately choose to run its
checks; it is not a core Kit dependency, runtime component, or required
adoption step.

Before changing the target project, an owner should approve the local scope,
the zone mapping, the local policy owner, the review path, and whether checks
remain report-only or become locally enforced. Review
[README.md](README.md), [INTEGRATION_DECISION.md](INTEGRATION_DECISION.md), and
[WORK_MODEL_MAPPING.md](WORK_MODEL_MAPPING.md) with the target project's
operational sources.

## Adopt deliberately

1. Copy or locally reference only the needed compact policy and, if activated,
   the minimal work template. Do not replace the project's existing instructions,
   source-authority policy, or documentation structure wholesale.
2. Map local locations to `docs/`, `specs/active/`, `specs/archive/`,
   `docs/adr/`, and `.work/`; document any intentional local equivalents.
   Preserve immutable records and use linked successors for later decisions or
   requirements. Select metadata only when it is additive and appropriate to
   that document role.
3. Create `.work/<change-id>/` only for resumable multi-session work, multiple
   executors, more than three independently verifiable slices, high-risk
   acceptance, or an audit trail. When activated, start with `TASKS.md` and
   `ACCEPTANCE.md`; add a plan, deviations log, or artifacts only when needed.
   `TASKS.md` is the sole operational-status authority only for that activated
   change process; projections may route readers to it but must not duplicate
   status.
4. Treat hooks, CI variants, MkDocs configuration, just recipes, fixtures,
   generators, full pilots, and the optional Python checker as Reference Lab
   examples outside normal installation. A separate owner decision must define
   their scope and keep any checks report-only unless the owner later adopts
   local enforcement. If evaluating generated projections, identify their sole
   generator and use locally approved paired markers.
5. Adopt [`engine/`](engine/) only when the repository has an observable need
   for lifecycle enforcement: mixed active and historical corpora,
   reachability drift, superseded documents without reliable successors, or
   recurring scan cost dominated by history. Inventory Git-tracked documents,
   approve entrypoints and authority sources, create repository-specific
   policy/lifecycle/exception registries, and run `check --worktree --fail-on
   never` before enabling a blocking gate.
6. Promote enforcement in stages. First block only newly introduced
   `DOC-REACH-001` through `delta`; then add staged pre-commit and merge-base PR
   checks. Use committed `check --full` for the weekly active scan and
   `check --full --include-history` for the monthly history scan. Never infer
   lifecycle from age or filename, and migrate archives only as an explicit
   `move + lifecycle + moved path + references + validation` change.

## Validate adoption

Record the local owner decision and verify that:

- Project Map summaries are still secondary to operational docs, code, tests,
  active requirements, and current owner instructions.
- Current requirements are not presented as proof of current runtime behavior.
- Archived specifications and ADRs are preserved rather than silently edited.
- Durable facts originating in activated `.work/` have an explicit reviewed
  promotion.
- Any separately adopted generated block has one named generator and an
  identified source of change.
- Optional tooling can be removed without changing core Kit behavior.
- If the lifecycle engine is adopted, staged reports ignore unstaged content,
  every managed document has exactly one lifecycle, every superseded document
  has an existing registered successor, and repeated committed-snapshot JSON
  is identical.

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
