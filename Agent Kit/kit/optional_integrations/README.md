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

Adopt only the modules that match the project's actual tools.
