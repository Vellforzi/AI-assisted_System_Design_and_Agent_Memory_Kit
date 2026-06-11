# AI-assisted System Design and Agent Memory Kit v3.9.3 — Manifest

Package file: `AI-assisted_System_Design_and_Agent_Memory_Kit_v3.9.3_EN.zip`

Package purpose: portable starter guide and memory operating layer for using AI agents with owner-controlled projects. Agent Memory Kit helps build a Project Map through structured, meaningful, interconnected duplication of project information supplied or verified by the owner.

---

## Top-level files

- `README.md` — concise repository/package README.
- `START_HERE.md` — package router and first entry point.
- `RELEASE_NOTES_v3.9.3.md` — what changed in this patch release.
- `RELEASE_NOTES_v3.9.1.md` — what changed in the implicit IDE context patch.
- `RELEASE_NOTES_v3.9.0.md` — what changed in the Context Advisor release.
- `AI-assisted System Design/README.md` — overview of the system-design methodology.
- `AI-assisted System Design/AI-assisted System Design.md` — methodology for operating AI-readable projects.
- `Agent Kit/README.md` — overview of Agent Memory Kit.
- `Agent Kit/START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md` — main human/agent guide for the memory kit.

---

## Agent Kit core files

- `Agent Kit/kit/README.md` — package note and file map.
- `Agent Kit/kit/OWNER_USAGE_GUIDE.md` — day-to-day usage guide for a project owner.
- `Agent Kit/kit/ACTION_INTENT_CONTRACT.md` — answer-only default intent and explicit-action gate.
- `Agent Kit/kit/SIGNIFICANT_WORK_AND_CHECKPOINTS.md` — significant-work triggers, checkpoints, Project Map deltas, and eval triggers.
- `Agent Kit/kit/PROJECT_GROUNDING_CONTRACT.md` — strict evidence contract for project-specific claims.
- `Agent Kit/kit/CONTEXT_SCOPE_MODEL_ADVISOR.md` — pre-hydration advisor for context, scope, model/settings, and fuel.
- `Agent Kit/kit/CURSOR_MODEL_ROUTING_SNAPSHOT.md` — dated Cursor model-routing snapshot and core/optional model policy.
- `Agent Kit/kit/CONTEXT_ADVISOR_TEMPLATE.yaml` — project-local advisor policy template.
- `Agent Kit/kit/PROVIDER_CAPABILITY_SNAPSHOT_TEMPLATE.yaml` — volatile provider/model capability snapshot template.
- `Agent Kit/kit/context_advisor/` — advisor profile matrix, hint policy, TypeScript contract, example run, and provider snapshot example. v3.9.3 adds cost-aware model routing fields and profile defaults.
- `Agent Kit/kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md` — operational protocol for memory intake, grounded answers, memory updates, checkpoints, verification, and eval usage.
- `Agent Kit/kit/PROJECT_MEMORY_STORAGE_GUIDE.md` — storage architecture: current state, working state, policies, tasks, claims, handoffs, memory cards, indexes, evals, raw sources, archive.
- `Agent Kit/kit/PLAIN_LANGUAGE_GLOSSARY.md` — simple explanations for common terms.
- `Agent Kit/kit/POSITIONING_AND_ALTERNATIVES.md` — comparison with provider memory, repo instruction files, memory frameworks, vector stores, and autonomous runtimes.

---

## Templates and schemas

- `Agent Kit/kit/SOURCE_AUTHORITY_TEMPLATE.yaml` — source-authority template.
- `Agent Kit/kit/PERMISSIONS_POLICY_TEMPLATE.yaml` — permissions and action-intent template.
- `Agent Kit/kit/RETRIEVAL_POLICY_TEMPLATE.yaml` — retrieval policy template.
- `Agent Kit/kit/TASK_CONTRACT_TEMPLATE.yaml` — long-running task contract template.
- `Agent Kit/kit/CLAIM_LEDGER_TEMPLATE.yaml` — claim-ledger and final-answer gate template.
- `Agent Kit/kit/HANDOFF_TEMPLATE.yaml` — clean-slate handoff packet template.
- `Agent Kit/kit/MEMORY_SCHEMA_REFERENCE.yaml` — canonical schema reference for durable memory units and Project Map artifacts.
- `Agent Kit/kit/memory_card_examples.yaml` — copyable examples for Project Map memory.

---

## Operating guides

- `Agent Kit/kit/LONG_RUNNING_TASKS_GUIDE.md` — long-task design without consciousness simulation.
- `Agent Kit/kit/RETRIEVAL_POLICY_PROFILES.md` — retrieval profiles for answer, analyze, plan, resume, recover, fork, audit, and repair.
- `Agent Kit/kit/WORKING_STATE_AND_REPLAY_GUIDE.md` — compact working-state and replay protocol.
- `Agent Kit/kit/MEMORY_COMPILER_GUIDE.md` — session note to durable memory consolidation guide.
- `Agent Kit/kit/MEMORY_TOOL_INTERFACE_CONTRACT.md` — expected behavior for memory tool implementations.
- `Agent Kit/kit/PROVIDER_MEMORY_AND_RUNTIME_BOUNDARY.md` — boundary between Project Map, provider memory, runtime state, and external research.
- `Agent Kit/kit/SERVICE_RULE_PLACEMENT_GUIDE.md` — where to place rules/instructions in AI services.
- `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md` — migration guide for active existing projects.
- `Agent Kit/kit/NEW_PROJECT_ADOPTION_GUIDE.md` — setup guide for empty new projects.
- `Agent Kit/kit/SOLO_OWNER_WORKFLOW_GUIDE.md` — high-control solo-owner workflow.
- `Agent Kit/kit/AGENT_INSTRUCTION_FILES_GUIDE.md` — how to use AGENTS.md, Cursor rules, CLAUDE.md, and similar files.
- `Agent Kit/kit/START_MESSAGE_TEMPLATES.md` — reusable owner prompts.
- `Agent Kit/kit/PROJECT_WORKSPACE_LAYOUT.md` — folder layout reference.
- `Agent Kit/kit/MANUAL_OWNER_REVIEW_CHECKLIST.md` — manual owner review checklist.

---

## Repository instruction templates

- `Agent Kit/kit/AGENTS.md_TEMPLATE.md` — root repository instruction template.
- `Agent Kit/kit/CURSOR_RULE_TEMPLATE.mdc` — Cursor project rule template.
- `Agent Kit/kit/cursor/rules/context_advisor_preflight.mdc` — Cursor rule fragment for Context Advisor preflight.

---

## Eval files

- `Agent Kit/kit/EVAL_SUITE_GUIDE.md` — eval-suite guide.
- `Agent Kit/kit/EVAL_AUTOMATION_AND_TRIGGER_POLICY.md` — eval trigger matrix and automation levels.
- `Agent Kit/kit/eval_suite/README.md` — eval-suite folder guide.
- `Agent Kit/kit/eval_suite/eval_manifest.yaml` — suite metadata and pass gates.
- `Agent Kit/kit/eval_suite/eval_trigger_policy.yaml` — portable trigger policy for eval runs.
- `Agent Kit/kit/eval_suite/core_behavior_eval_cases.yaml` — portable core behavior cases.
- `Agent Kit/kit/eval_suite/grader_rubric.yaml` — deterministic/model/human grading rubric.
- `Agent Kit/kit/eval_suite/eval_run_report_template.yaml` — eval run report template.
- `Agent Kit/kit/eval_suite/eval_trace_template.yaml` — failure trace template.
- `Agent Kit/kit/eval_suite/failure_to_eval_case_template.yaml` — convert real failures into candidate eval cases.

---

## Codex Integration Pack

- `Agent Kit/kit/CODEX_INTEGRATION_OWNER_GUIDE.md` — owner guide for using Codex with Agent Memory Kit and Cursor.
- `Agent Kit/kit/codex/README.md` — Codex integration folder overview.
- `Agent Kit/kit/codex/CODEX_SETTINGS_RECOMMENDATIONS.md` — recommended Codex UI and behavior settings.
- `Agent Kit/kit/codex/CODEX_CONFIG_TOML_TEMPLATES.md` — config placement and merge guidance.
- `Agent Kit/kit/codex/CODEX_HOOKS_SETUP_GUIDE.md` — global and project hook setup guide.
- `Agent Kit/kit/codex/CODEX_CURSOR_WORKFLOW.md` — workflow for Cursor as implementation agent and Codex as reviewer/auditor.
- `Agent Kit/kit/codex/CODEX_CUSTOM_INSTRUCTIONS.md` — short Codex custom instruction block.
- `Agent Kit/kit/codex/config/` — config templates and custom-instruction text.
- `Agent Kit/kit/codex/hooks/` — hook examples and optional scripts.
- `Agent Kit/kit/codex/agents/` — `AGENTS.md` examples.
- `Agent Kit/kit/codex/skills/` — Codex Skills for memory compilation, checkpointing, handoff, recovery, source authority, and eval cases.
- `Agent Kit/kit/codex/subagents/` — read-only review subagent templates.

## Optional tools

- `Agent Kit/kit/tools/README.md` — helper script documentation.
- `Agent Kit/kit/tools/run_eval_checklist.py` — creates a local eval run folder and Markdown checklist from YAML cases.
- `Agent Kit/kit/tools/context_advisor_preflight.py` — optional local CLI helper for compact Context Advisor preflight output.

---

## Publishing and research files

- `Agent Kit/kit/README_AUTHORING_GUIDE.md` — README publishing guide.
- `Agent Kit/kit/GIT_PUBLISHING_GUIDE.md` — safe git publishing and hygiene guide.
- `Agent Kit/kit/RESEARCH_BASIS.md` — sources and design influences for this release.
- `Agent Kit/kit/SHA256SUMS.txt` — checksums for package files.

---

## Permission model

- `explain-only`: explain the kit; no project file read/write.
- `dry-run`: proposal only; no read/write permission by itself.
- `read-only`: read only explicitly named folders/files/resources.
- `apply`: write only explicitly confirmed, scoped changes.

Permission does not imply action intent. A question remains answer-only unless the owner explicitly asks for a mutating action.

---

## Significant-work rule

After meaningful work, the agent should decide whether a checkpoint, handoff, Project Map update proposal, or eval trigger is needed.

The agent may propose these artifacts in non-apply modes. It must not write them without explicit owner approval or an approved task contract.

---

## Eval rule

Use the eval-suite to detect regressions in action intent, grounding, retrieval, memory compilation, side-effect safety, significant-work handling, eval automation, and owner-control behavior.

Evals complement manual owner review; they do not prove correctness.

Evals do not run automatically unless connected to a runner, hook, command, CI workflow, or API harness.

---

## Execution preflight

Before console, shell, server, container, CI, database, deployment, git mutation, or any external side effect, the owner must specify the target environment and approve the action. Missing environment details must not be guessed.

---

## Grounding preflight

Before a project-specific answer, the agent must identify the valid evidence base. If required context is missing, it must not guess. It may ask a minimal clarification or propose a retrieval plan.

---

## Continuation rule

Later sessions should restore from documented `Project Map` / working state / task contract / handoff state. Undocumented chat history is not reliable project state.


---

## Platform context and Cursor integration files

- `Agent Kit/kit/PLATFORM_CONTEXT_COMPACTION_BOUNDARY.md` — rule that platform summaries, compressed chat history, provider memory, and personalization are non-authoritative hints.
- `Agent Kit/kit/CURSOR_INTEGRATION_OWNER_GUIDE.md` — owner-facing guide for configuring Cursor with Rules, Commands, Skills, Subagents, and optional Hooks.
- `Agent Kit/kit/cursor/README.md` — Cursor Integration Pack overview.
- `Agent Kit/kit/cursor/COMMAND_VOCABULARY.md` — command-to-mode mapping and explicit mode block.
- `Agent Kit/kit/cursor/rules/` — short always-on Cursor rule templates.
- `Agent Kit/kit/cursor/commands/` — copy-paste command bodies for common workflows.
- `Agent Kit/kit/cursor/skills/` — reusable procedure templates.
- `Agent Kit/kit/cursor/subagents/` — focused read-only subagent role templates.
- `Agent Kit/kit/cursor/hooks/` — optional hook examples and scripts.

The Python scripts in `cursor/hooks/scripts/` are optional examples. Agent Memory Kit does not require Python.

---

## v3.8 scope, workspace, and role orchestration files

- `Agent Kit/kit/SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md` — agent-managed allowed-scope workflow.
- `Agent Kit/kit/CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md` — plain-language Codex permission and sandbox guide.
- `Agent Kit/kit/WORKSPACE_SELECTION_GUIDE.md` — workspace selection guidance for multi-component projects.
- `Agent Kit/kit/AI_AGENT_ROLE_STACK_GUIDE.md` — default role split across Cursor, Codex, GPT web chat, Project Map, and owner.
- `Agent Kit/kit/HOOK_REQUEST_WORKFLOW.md` — workflow for hook requests.
- `Agent Kit/kit/HOOK_GENERATION_QUESTIONS.md` — minimal questions for hook generation.
- `Agent Kit/kit/HOOK_PACKAGING_GUIDE.md` — packaging rules for project-local hook bundles.
- `Agent Kit/kit/cursor/workspaces/` — Cursor workspace templates.
- `Agent Kit/kit/cursor/commands/scope-set.md` — command template for setting task write scope.
- `Agent Kit/kit/cursor/commands/scope-reset.md` — command template for resetting write scope.
- `Agent Kit/kit/cursor/commands/workspace-check.md` — command template for workspace validation.
- `Agent Kit/kit/codex/scope/` — Codex scope templates and optional helper.
- `Agent Kit/kit/codex/workflows/` — Codex workflow notes for scope and workspace checks.

- `Agent Kit/kit/CURSOR_AGENT_SETTINGS_GUIDE.md` — recommended Cursor Agent settings for owner-controlled work.
- `Agent Kit/kit/CURSORIGNORE_AND_CONTEXT_BOUNDARY_GUIDE.md` — `.cursorignore` and context-boundary guide.
- `Agent Kit/kit/cursor/CURSOR_OWNER_CONTROLLED_DEFAULTS.md` — readable Cursor settings profile.
- `Agent Kit/kit/cursor/settings/owner_controlled_profile.yaml` — machine-readable Cursor settings profile.
- `Agent Kit/kit/cursor/settings/option_profit_current_profile.yaml` — example project-specific settings profile.
- `Agent Kit/kit/cursor/context/.cursorignore.safe-default` — safe default `.cursorignore` template.
- `Agent Kit/kit/cursor/commands/settings-audit.md` — Cursor settings audit command.
- `Agent Kit/kit/cursor/commands/cursorignore-audit.md` — `.cursorignore` audit command.

---

## v3.8 ignore boundary additions

- `Agent Kit/kit/CODEXIGNORE_AND_CONTEXT_BOUNDARY_GUIDE.md` — `.codexignore` guidance and Codex context-boundary policy.
- `Agent Kit/kit/codex/ignore/README.md` — Codex ignore template guide.
- `Agent Kit/kit/codex/ignore/.codexignore.safe-default` — general `.codexignore` template.
- `Agent Kit/kit/codex/ignore/.codexignore.option-profit-default` — OPTION PROFIT `.codexignore` template.
- `Agent Kit/kit/cursor/context/.cursorignore.option-profit-default` — OPTION PROFIT `.cursorignore` template.
- `Agent Kit/kit/cursor/commands/codexignore-audit.md` — `.codexignore` audit command.

The ignore templates include `**/desktop.ini` for Windows/Google Drive projects.


---

## v3.9.3 cost-aware model routing additions

- `Agent Kit/kit/CONTEXT_SCOPE_MODEL_ADVISOR.md` — lowest-sufficient model rule and premium escalation requirements.
- `Agent Kit/kit/CURSOR_AGENT_SETTINGS_GUIDE.md` — model/reasoning cost ladder.
- `Agent Kit/kit/context_advisor/context_advisor_v1.profile_matrix.json` — cost/capability fields plus `project_map_update` profile.
- `Agent Kit/kit/context_advisor/context_advisor_v1.types.ts` — cost-aware routing contract fields.
- `Agent Kit/kit/tools/context_advisor_preflight.py` — premium/high routing warning flags.
- `Agent Kit/kit/eval_suite/core_behavior_eval_cases.yaml` — `AMK-CA-008` regression case.

## v3.9.3 dated provider/model snapshot additions

- `Agent Kit/kit/context_advisor/cursor_provider_capability_snapshot_2026-06-10.yaml` — owner-observed Cursor model controls plus source refs, collected on 2026-06-10.
- `Agent Kit/kit/context_advisor/cursor_model_routing_matrix.v1.json` — machine-readable model routing matrix for Cursor-agent.
- `Agent Kit/kit/cursor/commands/models.md` — owner command for model-set sufficiency and snapshot freshness.
- `AMK-CA-009` and `AMK-CA-010` — eval cases for dated snapshots and unsupported model-control invention.

### v3.9.3 model/surface routing files

- `Agent Kit/kit/MODEL_SURFACE_ROUTING_SNAPSHOT.md` — dated Cursor/Codex/ChatGPT Pro model and mode routing snapshot.
- `Agent Kit/kit/CURSOR_MODEL_ROUTING_SNAPSHOT.md` — backward-compatible Cursor routing snapshot including Auto/Max boundaries.
- `Agent Kit/kit/context_advisor/provider_surface_routing_snapshot_2026-06-10.yaml` — machine-readable provider/surface/mode snapshot.
- `Agent Kit/kit/context_advisor/cursor_model_routing_matrix.v1.json` — ContextAdvisor cost/model routing matrix.
- `Agent Kit/kit/cursor/commands/ask.md`, `debug.md`, `multitask.md`, `models.md`, `settings.md` — compact commands for mode/settings routing.
- `Agent Kit/kit/codex/workflows/model-routing.md` — Codex IDE extension routing workflow.

- `Agent Kit/kit/context_advisor/execution_surface_routing_matrix.v1.json` — v3.9.3 machine-readable surface/mode routing matrix.
