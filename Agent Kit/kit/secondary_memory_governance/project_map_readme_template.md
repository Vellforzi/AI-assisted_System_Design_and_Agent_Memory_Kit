# Project Map

Status: Active secondary-memory navigation
Last aligned: <YYYY-MM-DD>
Audience: owner, AI/Codex sessions
Runtime impact: none
Authority: secondary navigation index; operational docs and current owner instructions win

---

## Role

This directory is secondary memory and navigation. It summarizes, routes, and
records candidate memory; it does not override operational docs, code, tests,
specs, issues, or current owner instructions.

## Files

- secondary `docs/project_map/context_index.yaml` - machine-readable context routing metadata.
- secondary `docs/project_map/source_authority.yaml` - source-of-truth order and conflict behavior.
- secondary `docs/project_map/permissions_policy.yaml` - advisory action intent and mutation gates.
- secondary `docs/project_map/retrieval_policy.yaml` - smallest evidence-bearing retrieval policy.
- secondary `docs/project_map/retrieval_scoring_policy.yaml` - hard-gated retrieval scoring rules.
- secondary `docs/project_map/memory_lifecycle_policy.yaml` - candidate-first memory lifecycle.
- secondary `docs/project_map/tool_output_reference_template.yaml` - compact references to long tool output.
- secondary `docs/project_map/working_state.yaml` - compact replay pointer for fresh sessions.
- secondary `docs/project_map/current_map.md` - owner-memory and handoff map.
- secondary `docs/project_map/memory_quality_review_bar.md` - review bar for governance changes.
- secondary `docs/project_map/eval_suite/context_selection_smoke_cases.yaml` - context-selection smoke checks.
- secondary `docs/project_map/eval_suite/manual_smoke_cases.yaml` - manual governance smoke cases.

## Update Rule

Update Project Map files only when the task explicitly scopes a memory update,
governance update, or approved proposed delta. Otherwise report proposed changes
without mutating this directory.
