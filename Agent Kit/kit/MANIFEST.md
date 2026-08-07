# AI-assisted System Design and Agent Memory Kit v5.0.0 — Manifest

Package file: `AI-assisted_System_Design_and_Agent_Memory_Kit_v5.0.0_EN.zip`

Package purpose: portable starter guide and memory operating layer for using AI agents with owner-controlled projects. Agent Memory Kit helps build a Project Map through structured, meaningful, interconnected duplication of project information supplied or verified by the owner.

---

## Top-level files

- `README.md` — concise repository/package README.
- `START_HERE.md` — package router and first entry point.
- `RELEASE_NOTES_v5.0.0.md` — what changed in this release.
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
- `Agent Kit/kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md` — operational protocol for memory intake, grounded answers, memory updates, checkpoints, verification, and eval usage.
- `Agent Kit/kit/PROJECT_MEMORY_STORAGE_GUIDE.md` — storage architecture: current state, working state, policies, tasks, claims, handoffs, memory cards, indexes, evals, raw sources, archive.
- `Agent Kit/kit/PLAIN_LANGUAGE_GLOSSARY.md` — simple explanations for common terms.
- `Agent Kit/kit/POSITIONING_AND_ALTERNATIVES.md` — comparison with provider memory, repo instruction files, memory frameworks, vector stores, and autonomous runtimes.

## v5.0 contract and workflow files

- `project_artifact_contract_v2/` — closed Draft 2020-12 schemas, examples, and semantic fixture corpus for Project Artifact Contract V2.
- `tools/project_artifact_contract_v2_oracle.py` — dependency-free structural and cross-contract oracle, including DAG/frontier and activation checks.
- `tools/workflow_projection_helper.py` — report-only work frontier, capability status, and triage readiness projections.
- `WORK_ITEM_GRAPH_TEMPLATE.yaml`, `PLAN_CHALLENGE_TEMPLATE.yaml`, `REVIEW_RECEIPT_TEMPLATE.yaml`, `EXPLORATION_MAP_TEMPLATE.yaml`, `TRIAGE_LEDGER_TEMPLATE.yaml`, `DESIGN_PROBE_TEMPLATE.yaml`, `CAPABILITY_REGISTRY_TEMPLATE.yaml`, `DOMAIN_LANGUAGE_TEMPLATE.yaml` — conditionally activated workflow artifacts.
- `MIGRATION_v4_TO_v5.md` and `tools/migrate_v4_artifact.py` — read-only reviewed migration proposal.

## Preserved v4 contract and governance files

- `project_artifact_contract_v1/` — closed Draft 2020-12 schemas, valid/invalid examples, and fixture corpus.
- `tools/project_artifact_contract_oracle.py` — dependency-free structural and semantic oracle.
- `COMMITMENT_LEDGER_TEMPLATE.yaml`, `MEMORY_DELTA_TEMPLATE.yaml`, `SIDE_EFFECT_RECEIPT_TEMPLATE.yaml`, `VERIFICATION_RECEIPT_TEMPLATE.yaml` — reality-gated artifact templates.
- `ARTIFACT_DESCRIPTOR_TEMPLATE.yaml`, `ARTIFACT_EXCERPT_TEMPLATE.yaml` — progressive-disclosure projections.
- `CONTEXT_BUDGET_POLICY_TEMPLATE.yaml` and `tools/context_budget_audit.py` — report-only context budget checks.
- `MIGRATION_v3.8_TO_v4.0.md` and `tools/migrate_v38_artifact.py` — read-only migration proposal workflow.
- `optional_integrations/workflow_evals_mocked_tools/` — deterministic recorded-trace evaluation.
- `optional_integrations/tool_capability_governance/` — fail-closed capability manifest reporting.
- `optional_integrations/policy_canary/` — offline canary validation without live traffic.

---

## Secondary-memory governance baseline

- `Agent Kit/kit/secondary_memory_governance/README.md` - single repo-centric secondary-memory governance baseline for existing projects.
- `Agent Kit/kit/secondary_memory_governance/AGENTS_SNIPPET.md` - project `AGENTS.md` snippet for task-local scope, startup read order, skipped context, mutation rules, next-step promotion, and reporting.
- `Agent Kit/kit/secondary_memory_governance/next_steps_template.md` - active task navigation template for `docs/NEXT_STEPS.md`, including current next safe step and evidence/read-set refs.
- `Agent Kit/kit/secondary_memory_governance/current_status_template.md` - compact current-status and next-step context pack template for fresh sessions.
- `Agent Kit/kit/secondary_memory_governance/source_of_truth_hierarchy_template.md` - operational source-of-truth hierarchy template with evidence boundary and next-step promotion rules.
- `Agent Kit/kit/secondary_memory_governance/context_governance_rules_template.md` - task-local scope, minimal retrieval, docs lifecycle, session-context promotion, and next-step impact promotion template.
- `Agent Kit/kit/secondary_memory_governance/project_map_readme_template.md` - secondary Project Map entrypoint template.
- `Agent Kit/kit/secondary_memory_governance/context_index.yaml` - machine-readable context index template for task-profile read sets.
- `Agent Kit/kit/secondary_memory_governance/context_selection_smoke_cases.yaml` - copyable smoke-case suite for context-selection checks.
- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/README.md` - Context Contract V1 ownership, portability, and Python/TypeScript adapter guide.
- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/schemas/` - standalone Draft 2020-12 schemas for `ContextRequestV1`, `ContextBundleV1`, and `ContextReceiptV1`.
- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/examples/` - valid and invalid payload examples for all three V1 contracts.
- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/fixtures/context-contract-v1-smoke.json` - canonical cross-language fixture oracle for over/under retrieval, forbidden paths, and stale authority.
- `Agent Kit/kit/secondary_memory_governance/codex_prompt_rules_template.md` - bounded Codex prompt contract template with receipt and handoff update requirements.
- `Agent Kit/kit/secondary_memory_governance/ai_development_rules_template.md` - AI workflow rule template for scoped reads, mutation gates, conflict handling, and next-step promotion.
- `Agent Kit/kit/secondary_memory_governance/research_readme_template.md` - research navigation template that keeps research as evidence/context until promotion.
- `Agent Kit/kit/secondary_memory_governance/validation_readme_template.md` - validation navigation template for checks and evidence boundaries.
- `Agent Kit/kit/secondary_memory_governance/source_authority.yaml` - source authority policy where Project Map is secondary memory, operational docs win, and next-step-critical evidence must be promoted.
- `Agent Kit/kit/secondary_memory_governance/permissions_policy.yaml` - action-intent, scoped read-only exploration, mutation gates, and enforcement labels.
- `Agent Kit/kit/secondary_memory_governance/retrieval_policy.yaml` - smallest evidence-bearing retrieval policy for secondary memory.
- `Agent Kit/kit/secondary_memory_governance/retrieval_scoring_policy.yaml` - hard-gated retrieval scoring policy for secondary memory.
- `Agent Kit/kit/secondary_memory_governance/memory_lifecycle_policy.yaml` - candidate-first lifecycle, stale suppression, episodic event, and tool-use lesson rules.
- `Agent Kit/kit/secondary_memory_governance/tool_output_reference_template.yaml` - compact reference template for long tool outputs.
- `Agent Kit/kit/secondary_memory_governance/working_state.yaml` - compact replay root for fresh sessions.
- `Agent Kit/kit/secondary_memory_governance/current_map_template.md` - secondary owner-memory map template.
- `Agent Kit/kit/secondary_memory_governance/manual_smoke_cases.yaml` - manual portable governance smoke cases for the repo-centric baseline.
- `Agent Kit/kit/secondary_memory_governance/PASS_3_VERIFICATION_RECEIPT.md` - verification receipt that concrete adopter profiles are not bundled in the reusable overlay.
- `Agent Kit/kit/secondary_memory_governance/memory_quality_review_bar.md` - review bar for memory, retrieval, permission, and governance changes.
- `Agent Kit/kit/secondary_memory_governance/.codexignore_TEMPLATE` - Codex context-hygiene template, not a security boundary.
- `Agent Kit/kit/secondary_memory_governance/.cursorignore_TEMPLATE` - optional Cursor context-hygiene template, not a security boundary.

---

## Optional integrations

- `Agent Kit/kit/optional_integrations/README.md` - index for optional modules that sit outside the core governance baseline.
- `Agent Kit/kit/optional_integrations/chatgpt_project_sources/README.md` - local ChatGPT Project source export workflow.
- `Agent Kit/kit/optional_integrations/chatgpt_project_sources/generate_chatgpt_project_sources.py` - stdlib generator for context packs, source manifests, TODOs, and checksums.
- `Agent Kit/kit/optional_integrations/chatgpt_project_sources/CHATGPT_PROJECT_SOURCES.config.template.json` - project config template for the generator.
- `Agent Kit/kit/optional_integrations/chatgpt_project_sources/PROJECT_AI_BRIEF.template.md` - compact project brief source template.
- `Agent Kit/kit/optional_integrations/chatgpt_project_sources/PROJECT_GPT_OPERATING_CONTRACT.template.md` - ChatGPT Project read-only operating contract template.
- `Agent Kit/kit/optional_integrations/chatgpt_project_sources/GPT_PROJECT_INSTRUCTIONS_COMPACT.template.md` - compact ChatGPT Project Instructions source template.
- `Agent Kit/kit/optional_integrations/chatgpt_project_sources/chatgpt_project_sources_policy.md` - safety and manifest policy for ChatGPT Project sources.
- `Agent Kit/kit/optional_integrations/cost_model_routing/README.md` - optional cost/model routing guide.
- `Agent Kit/kit/optional_integrations/cursor_settings/README.md` - optional Cursor settings integration guide.

---

## Templates and schemas

- `Agent Kit/kit/SOURCE_AUTHORITY_TEMPLATE.yaml` — source-authority template.
- `Agent Kit/kit/PERMISSIONS_POLICY_TEMPLATE.yaml` — permissions and action-intent template.
- `Agent Kit/kit/RETRIEVAL_POLICY_TEMPLATE.yaml` — retrieval policy template.
- `Agent Kit/kit/RETRIEVAL_SCORING_POLICY_TEMPLATE.yaml` — retrieval scoring policy template with hard gates before scoring.
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
- `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md` — baseline guide for adding the repo-centric context governance baseline to active existing projects.
- `Agent Kit/kit/MATURE_EXISTING_PROJECT_ADOPTION_PROFILE.md` — reference profile for strengthening mature projects; concrete baseline package is `secondary_memory_governance/`.
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

---

## Eval files

- `Agent Kit/kit/EVAL_SUITE_GUIDE.md` — eval-suite guide.
- `Agent Kit/kit/EVAL_AUTOMATION_AND_TRIGGER_POLICY.md` — eval trigger matrix and automation levels.
- `Agent Kit/kit/eval_suite/README.md` — eval-suite folder guide.
- `Agent Kit/kit/eval_suite/eval_manifest.yaml` — suite metadata and pass gates.
- `Agent Kit/kit/eval_suite/eval_trigger_policy.yaml` — portable trigger policy for eval runs.
- `Agent Kit/kit/eval_suite/core_behavior_eval_cases.yaml` — portable core behavior cases.
- `Agent Kit/kit/eval_suite/domain_boundary_smoke_cases_template.yaml` — copyable mature-project template for domain-specific boundary smoke cases.
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
- `Agent Kit/kit/codex/CODEX_CURSOR_WORKFLOW.md` — workflow for Cursor as implementation agent and Codex as reviewer/auditor.
- `Agent Kit/kit/codex/CODEX_CUSTOM_INSTRUCTIONS.md` — short Codex custom instruction block.
- `Agent Kit/kit/codex/config/` — config templates and custom-instruction text.
- `Agent Kit/kit/codex/agents/` — `AGENTS.md` examples.
- `Agent Kit/kit/codex/skills/` — Codex Skills for memory compilation, checkpointing, handoff, recovery, source authority, and eval cases.
- `Agent Kit/kit/codex/subagents/` — read-only review subagent templates.

## Optional tools

- `Agent Kit/kit/tools/README.md` — helper script documentation.
- `Agent Kit/kit/tools/run_eval_checklist.py` — creates a local eval run folder and Markdown checklist from YAML cases.
- `Agent Kit/kit/tools/context_governance_helper.py` - read-only reference helper for context-index read sets, receipts, API-agent context bundles, and context smoke checks.
- `Agent Kit/kit/tools/context_contract_v1_oracle.py` - standard-library oracle for V1 schemas, examples, policy fixtures, and legacy smoke-id reuse.
- `Agent Kit/kit/tools/documentation_harness.py` - report-only documentation harness for metadata, reachability, and lower-authority reference checks.

ChatGPT Project source generation lives under
`Agent Kit/kit/optional_integrations/chatgpt_project_sources/` because it is an
export workflow, not a core local helper.

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

Evals do not run automatically unless connected to a runner, command, CI workflow, or API harness.

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
- `Agent Kit/kit/CURSOR_INTEGRATION_OWNER_GUIDE.md` — owner-facing guide for configuring Cursor with Rules, Commands, Skills, and Subagents.
- `Agent Kit/kit/cursor/README.md` — Cursor Integration Pack overview.
- `Agent Kit/kit/cursor/COMMAND_VOCABULARY.md` — command-to-mode mapping and explicit mode block.
- `Agent Kit/kit/cursor/rules/` — short always-on Cursor rule templates.
- `Agent Kit/kit/cursor/commands/` — copy-paste command bodies for common workflows.
- `Agent Kit/kit/cursor/skills/` — reusable procedure templates.
- `Agent Kit/kit/cursor/subagents/` — focused read-only subagent role templates.
---

## v3.8 scope, workspace, and role orchestration files

- `Agent Kit/kit/SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md` — agent-managed allowed-scope workflow.
- `Agent Kit/kit/CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md` — plain-language Codex permission and sandbox guide.
- `Agent Kit/kit/WORKSPACE_SELECTION_GUIDE.md` — workspace selection guidance for multi-component projects.
- `Agent Kit/kit/AI_AGENT_ROLE_STACK_GUIDE.md` — default role split across Cursor, Codex, GPT web chat, Project Map, and owner.
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
