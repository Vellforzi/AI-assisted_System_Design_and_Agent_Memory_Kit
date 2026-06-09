# START HERE — AI-assisted System Design and Agent Memory Kit

Version: v3.5.0  
Release date: 2026-06-09  
Package: `AI-assisted_System_Design_and_Agent_Memory_Kit_v3.5.0_EN.zip`  
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

For project-specific claims, the model is only an execution engine. The valid project context comes from the owner, the Project Map, project files, tool outputs, and sources explicitly retrieved in the current run.

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

For any project-specific answer, the agent may use only:

1. the current user message;
2. Project Map memory;
3. project files or tool outputs opened in the current run;
4. external sources explicitly retrieved in the current run and valid for the claim type.

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

---

## Existing project versus new project

For an existing project with code and docs:

1. read `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`;
2. create a minimal Project Map;
3. run read-only inventory;
4. define source authority;
5. seed memory from verified facts only;
6. run eval smoke before trusting the setup.

For a new empty project:

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

## What changed in v3.5.0

This release strengthens the memory layer around:

- significant-work detection;
- checkpoint timing;
- Project Map update proposals;
- eval automation levels and triggers;
- optional checklist-assisted eval runs;
- new-project adoption;
- owner usage prompts;
- public positioning versus alternative memory approaches;
- simple terminology support.

See `RELEASE_NOTES_v3.5.0.md` for details.


---

## Cursor Integration Pack

For Cursor setup, read:

1. `Agent Kit/kit/CURSOR_INTEGRATION_OWNER_GUIDE.md`
2. `Agent Kit/kit/cursor/README.md`
3. `Agent Kit/kit/cursor/COMMAND_VOCABULARY.md`
4. `Agent Kit/kit/cursor/rules/`
5. `Agent Kit/kit/cursor/commands/`

Start with Rules and Commands. Add Hooks and Subagents after the core workflow is stable.
