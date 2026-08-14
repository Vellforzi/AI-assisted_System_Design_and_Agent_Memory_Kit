# Optional Integrations

Status: optional integration index
Last aligned: 2026-08-07
Audience: project owners, AI/Codex sessions, maintainers
Runtime impact: none unless an owner explicitly adopts and runs a module
Authority: optional integration navigation; adoption boundaries are defined by
`../ADOPTION_PROFILES.md`

---

## Role

These modules are advanced, opt-in additions and do not become default
behavior merely by being present in the Kit.

Core is the small, dependency-free documentation baseline described in
[`../ADOPTION_PROFILES.md`](../ADOPTION_PROFILES.md). It uses ordinary project
documentation for grounding, explicit action approval, and durable notes.
The `secondary_memory_governance/` overlay and Python helpers are opt-in
additions; adopt them only when their observable activation triggers apply and
the owner accepts their operating cost.

Optional modules:

- `chatgpt_project_sources/` - local manifest and context-pack generator for
  ChatGPT Project sources.
- `cost_model_routing/` - owner-facing guide for choosing the lowest sufficient
  model/settings class.
- `cursor_settings/` - Cursor Agent settings integration guide.
- `workflow_evals_mocked_tools/` - deterministic validation of recorded mock traces, including v5 reviewer, exploration, and probe boundaries.
- `tool_capability_governance/` - fail-closed, report-only capability risk checks.
- `policy_canary/` - offline canary policy validation without live rollout.
- `documentation_governance/` - owner-adopted compact policy for documentation
  zones, evidence-aware requirements, immutable records, and deliberate
  promotion from temporary work. Its hooks, CI variants, MkDocs, just recipes,
  fixtures, generators, and full pilots are Reference Lab examples outside the
  normal install path. Its `engine/` subdirectory is a separately activated
  lifecycle and Git-snapshot implementation for mature document corpora.

Adopt only the modules that match the project's actual tools.

`documentation_governance/` is not part of
`secondary_memory_governance/` and does not activate by being present. Its
optional checker uses dependency-free Python 3 only if an adopter chooses to
run it; the core Kit itself remains language-agnostic and Python-optional. See
[`documentation_governance/ADOPTION_GUIDE.md`](documentation_governance/ADOPTION_GUIDE.md)
for local adoption and rollback.
