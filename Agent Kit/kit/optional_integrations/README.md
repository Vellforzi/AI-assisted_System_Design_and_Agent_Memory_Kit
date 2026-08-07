# Optional Integrations

Status: optional integration index
Last aligned: 2026-08-07
Audience: project owners, AI/Codex sessions, maintainers
Runtime impact: none unless an owner explicitly adopts and runs a module
Authority: optional integration navigation; subordinate to core `secondary_memory_governance/`

---

## Role

These modules extend the core repo-centric secondary-memory governance baseline
without becoming part of the default behavior.

Core remains:

- `Agent Kit/kit/secondary_memory_governance/`
- `scripts/ai_context_helper.py`
- `scripts/documentation_harness.py`

Optional modules:

- `chatgpt_project_sources/` - local manifest and context-pack generator for
  ChatGPT Project sources.
- `cost_model_routing/` - owner-facing guide for choosing the lowest sufficient
  model/settings class.
- `cursor_settings/` - Cursor Agent settings integration guide.
- `workflow_evals_mocked_tools/` - deterministic validation of recorded mock traces, including v5 reviewer, exploration, and probe boundaries.
- `tool_capability_governance/` - fail-closed, report-only capability risk checks.
- `policy_canary/` - offline canary policy validation without live rollout.
- `documentation_governance/` - owner-adopted policy and optional report-first
  tooling for documentation zones, generated blocks, and review boundaries.

Adopt only the modules that match the project's actual tools.

`documentation_governance/` is not part of
`secondary_memory_governance/` and does not activate by being present. Its
optional checker uses dependency-free Python 3 only if an adopter chooses to
run it; the core Kit itself remains language-agnostic and Python-optional. See
[`documentation_governance/ADOPTION_GUIDE.md`](documentation_governance/ADOPTION_GUIDE.md)
for local adoption and rollback.
