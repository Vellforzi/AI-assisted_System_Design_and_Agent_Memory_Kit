# START HERE — AI-assisted System Design and Agent Memory Kit

Version: v5.0.0
Release date: 2026-08-07
Package: `AI-assisted_System_Design_and_Agent_Memory_Kit_v5.0.0_EN.zip`
Status: portable project-owner kit for AI-assisted work and grounded project memory

---

## What this package is

This package contains two coordinated layers:

| Layer | Path | Purpose |
|---|---|---|
| AI-assisted System Design | `AI-assisted System Design/` | A method for running a project as an AI-readable engineering system: scoped work, explicit contracts, small implementation chunks, verification, and documentation sync. |
| Agent Memory Kit | `Agent Kit/` | A portable memory operating layer for preserving project meaning, decisions, constraints, current state, evidence, risks, continuity, and agent behavior checks. |

The two layers are related but not identical.

- Use **AI-assisted System Design** when you are designing or improving the project workflow, repository structure, technical delivery process, or implementation protocol.
- Use **Agent Memory Kit** when you need the agent to remember, retrieve, ground, consolidate, continue, or evaluate project-specific work.
- Use both only when the user explicitly asks to connect process design with project memory.

---

## Core idea

Agent Memory Kit is not a chat-history archive and not an artificial consciousness graph. It is a disciplined external memory and case-management system.

Its purpose is to help the owner and AI agents avoid project errors caused by:

- forgetting prior decisions;
- mixing assumptions with verified facts;
- treating old information as current;
- losing the current workstream;
- answering project-specific questions from generic model knowledge;
- doing work when the owner only asked a question;
- rereading too much irrelevant context;
- silently overwriting important project meaning;
- forgetting to add eval cases for repeated failures.

For project-specific claims, the model is only an execution engine. The valid project context comes from the owner, project operational docs, the Project Map according to its declared authority mode, project files, tool outputs, and sources explicitly retrieved in the current run.

---

## First choice for every session

Before work begins, identify the active layer, intent, mode, and scope.

```text
Active layer: Agent Memory Kit / AI-assisted System Design / both.
Intent: answer / analyze / plan / retrieve_context / stage / apply / external_research.
Mode: explain-only / dry-run / read-only / apply.
Scope: <exact folders, files, or Project Map area>.
Goal: <one goal for this session>.
```

If the user has not chosen a layer, the agent should infer the smallest safe layer from the request. If inference is unsafe, ask one minimal clarification.

Answer-only is the default intent. Do not execute, write, update memory, run commands, or call external services unless the owner explicitly asked for that action.

---

## Non-negotiable grounding rule

For any project-specific answer, the agent may use only sources allowed by the
project's `source_authority.yaml` or equivalent source-of-truth hierarchy:

1. the current user message;
2. Project Map memory only in its declared authority role;
3. project files or tool outputs opened in the current run;
4. external sources explicitly retrieved in the current run and valid for the claim type.

If Project Map is `secondary_memory`, it summarizes and navigates; operational
docs, code, tests, specs, issues, and current owner instructions win.

If the evidence is missing, the agent must say so. It must not fill project gaps with provider-trained model knowledge.

General model knowledge may be used for general concepts, general software practice, language, formatting, and reasoning. It must not be used as evidence for what is true inside the owner's project.

---

## Recommended workspace layout

```text
<Project Workspace>/
  Agent Kit/        # this portable tool
  Project Map/      # external memory and continuity state
  Project Files/    # the actual project materials
```

The owner may rename folders. Roles matter more than names.

---

## Start with Agent Memory Kit

Read:

1. `Agent Kit/README.md`
2. `Agent Kit/START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md`
3. `Agent Kit/kit/README.md`
4. `Agent Kit/kit/OWNER_USAGE_GUIDE.md`
5. `Agent Kit/kit/ACTION_INTENT_CONTRACT.md`
6. `Agent Kit/kit/SIGNIFICANT_WORK_AND_CHECKPOINTS.md`
7. `Agent Kit/kit/PROJECT_GROUNDING_CONTRACT.md`
8. `Agent Kit/kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md`
9. `Agent Kit/kit/PROJECT_MEMORY_STORAGE_GUIDE.md`
10. `Agent Kit/kit/EVAL_SUITE_GUIDE.md`
11. `Agent Kit/kit/EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`
12. `Agent Kit/kit/PLAIN_LANGUAGE_GLOSSARY.md`

For existing repo-centric projects that already have operational docs, use the
repo-centric context governance baseline:

1. `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`
2. `Agent Kit/kit/secondary_memory_governance/README.md`
3. `Agent Kit/kit/secondary_memory_governance/source_of_truth_hierarchy_template.md`
4. `Agent Kit/kit/secondary_memory_governance/context_governance_rules_template.md`
5. `Agent Kit/kit/secondary_memory_governance/context_index.yaml`
6. `Agent Kit/kit/secondary_memory_governance/source_authority.yaml`
7. `Agent Kit/kit/secondary_memory_governance/permissions_policy.yaml`
8. `Agent Kit/kit/secondary_memory_governance/retrieval_policy.yaml`
9. `Agent Kit/kit/secondary_memory_governance/working_state.yaml`
10. `Agent Kit/kit/secondary_memory_governance/manual_smoke_cases.yaml`
11. `Agent Kit/kit/secondary_memory_governance/context_selection_smoke_cases.yaml`

---

## Existing Repo-Centric Project

For an existing project with code, docs, and project-specific agent instructions:

1. read `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`;
2. use `Agent Kit/kit/secondary_memory_governance/` as the single baseline package;
3. preserve the existing `AGENTS.md` and operational docs;
4. add source hierarchy, context governance rules, context index, policy YAML, working state, helper scripts, ignore hygiene, and smoke cases;
5. treat Project Map as secondary memory unless the project's authority policy says otherwise;
6. do not add runtime memory, task trees, handoff trees, vector databases, MCP servers, or a replacement `AGENTS.md` unless explicitly requested later.
7. add `Agent Kit/kit/optional_integrations/` modules only when the project uses
   ChatGPT Project sources, cost/model routing guidance, or Cursor settings.

For a new empty project that lacks operational docs:

1. read `Agent Kit/kit/NEW_PROJECT_ADOPTION_GUIDE.md`;
2. create Project Map before implementation;
3. record owner-approved goals, constraints, and non-goals;
4. avoid inventing architecture;
5. run eval smoke after repository instruction files are created.

---

## Start with AI-assisted System Design

Read:

1. `AI-assisted System Design/README.md`
2. `AI-assisted System Design/AI-assisted System Design.md`
3. the project's own `AGENTS.md`, `PROJECT_AI_BRIEF.md`, repository docs, or equivalent if the user explicitly grants read access.

---

## What changed in v3.8.0

This release adds an operational layer for scope control, workspace selection, and multi-agent role separation:

- agent-managed `.codex/ALLOWED_SCOPE.txt` workflows;
- `/scope-set`, `/scope-reset`, and `/workspace-check` command templates;
- Codex permission profile and sandbox explanations;
- Cursor workspace templates for one-root and multi-component projects;
- default role split: Cursor implements, Codex reviews, GPT web chat researches, Project Map stores memory or truth according to source authority;
- eval cases for scope, workspace, permissions, and role orchestration.

See `RELEASE_NOTES_v3.8.0.md` for details.

---

## Cursor Integration Pack

For Cursor setup, read:

1. `Agent Kit/kit/CURSOR_INTEGRATION_OWNER_GUIDE.md`
2. `Agent Kit/kit/cursor/README.md`
3. `Agent Kit/kit/cursor/COMMAND_VOCABULARY.md`
4. `Agent Kit/kit/cursor/rules/`
5. `Agent Kit/kit/cursor/commands/`

Start with Rules and Commands. Add Subagents after the core workflow is stable.

---

## Optional IDE integrations

For Cursor, read:

- `Agent Kit/kit/CURSOR_INTEGRATION_OWNER_GUIDE.md`
- `Agent Kit/kit/cursor/README.md`

For Codex, read:

- `Agent Kit/kit/CODEX_INTEGRATION_OWNER_GUIDE.md`
- `Agent Kit/kit/codex/README.md`
- `Agent Kit/kit/codex/CODEX_SETTINGS_RECOMMENDATIONS.md`

Recommended split:

```text
Cursor = primary local implementation agent
Codex = independent review, audit, recovery, and controlled second executor
Project Map = shared memory boundary; source of truth only when the project's authority policy says so
```

## v3.8 Cursor settings and workspace authority

This release adds an owner-controlled Cursor Agent settings profile, `.cursorignore` guidance, settings audit commands, and the rule that an existing authoritative workspace file must be inspected and used rather than replaced by a generated fallback.

## v3.8.0 focus

v3.8.0 adds Cursor owner-controlled settings, authoritative existing workspace handling, `.cursorignore` / `.codexignore` context-boundary templates, and desktop metadata ignore patterns for Windows/Google Drive projects.

## v5.0.0 focus

Start new installations with Project Artifact Contract V2. Activate workflow artifacts only when `TaskContractV3.workflow_profile`, risk, or task scale requires them. Existing v4 artifacts require a read-only migration proposal and owner review. Context Contract V1 remains compatible. See `RELEASE_NOTES_v5.0.0.md`.
