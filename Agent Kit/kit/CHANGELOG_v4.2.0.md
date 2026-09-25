# Agent Memory Kit v4.2.0 Changelog

Release source date: 2026-09-25.
Previous published release: `v4.1.0`.

v4.2.0 removes the obsolete assumption that GPT web is permanently read-only
or advisory. Execution surfaces are selected from current live capabilities,
owner authority and task fit.

## Added

- Capability-based execution-surface rule: ChatGPT web, Codex, Cursor and other
  connected agents are first-class surfaces.
- Explicit separation of owner authority from tool availability.
- Repository branch/tag/deployment evidence model: branch push, tag push, build,
  deploy, runtime and owner acceptance are distinct layers.
- Structured-source and generated-view rule for spreadsheets, databases and
  interactive Canvas dashboards.
- Concise-current-state doctrine for Project Map: current files are not task
  archaeology; history stays in Git, memory records and task artifacts.
- Package-release evidence rule requiring matching version, commit, tag and
  verifiable release state.

## Changed

- `portable/core/WORKFLOW.md` routes work by capability instead of product identity.
- `PROJECT_GPT_OPERATING_CONTRACT.template.md` permits any capable surface to
  execute owner-authorized work.
- `SOURCE_AUTHORITY_TEMPLATE.yaml` defines first-class surfaces, branch/tag
  triggers and generated views.
- `EXECUTOR_ROUTING_GATE.md` is no longer a mandatory ceremonial gate and no
  longer assigns repository work exclusively to Cursor/Codex.
- `CONTEXT_SCOPE_MODEL_ADVISOR.md` removes stale provider-specific model clutter
  from the portable rule.
- Expired model snapshots are explicitly historical and cannot define current
  product roles.
- ChatGPT Project Sources policy supports direct connected updates and separates
  tracked source, Drive/Project copy, UI Instructions and Git publication state.

## Preserved

- Current-source grounding and evidence discipline.
- Owner authority and no duplicate approval.
- One-writer rule for overlapping mutable state.
- Separation of source, test, build, publication, deployment, runtime and owner
  acceptance.
- Secret handling and project-specific side-effect boundaries.
- Optional adoption: no particular model, plugin, hook, MCP or folder layout is
  required by the portable core.

## Release proof

This changelog is source metadata, not proof by itself. A completed GitHub release
requires the published main commit, tag `v4.2.0`, and verifiable remote release
state. Those identities must be recorded after the tag/release operation.
