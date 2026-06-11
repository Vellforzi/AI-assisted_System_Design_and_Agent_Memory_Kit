# Agent Memory Kit

Version: v3.9.4

Agent Memory Kit is the project-memory and agent-behavior layer of the package.

It helps a project owner maintain a structured Project Map containing:

- current state;
- working state;
- source authority;
- permissions policy;
- retrieval policy;
- decisions;
- facts;
- constraints;
- risks;
- open questions;
- task contracts;
- handoffs;
- claim ledgers;
- eval cases and eval run notes.

---

## Start here

1. `START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md`
2. `kit/README.md`
3. `kit/OWNER_USAGE_GUIDE.md`
4. `kit/PROJECT_MEMORY_STORAGE_GUIDE.md`
5. `kit/ACTION_INTENT_CONTRACT.md`
6. `kit/SIGNIFICANT_WORK_AND_CHECKPOINTS.md`
7. `kit/EVAL_SUITE_GUIDE.md`
8. `kit/EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`
9. `kit/SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`
10. `kit/WORKSPACE_SELECTION_GUIDE.md`
11. `kit/CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`
12. `kit/AI_AGENT_ROLE_STACK_GUIDE.md`

---

## Default behavior

The agent must answer only unless the owner explicitly asks for a concrete action. Reading memory for context is not the same as permission to modify memory, files, database state, git state, cloud resources, or external systems.

After meaningful work, the agent may propose a Project Map delta and identify whether evals should run. It must not apply memory or rule changes unless the owner explicitly asks.

---

## Use in a repository

Use `kit/AGENT_INSTRUCTION_FILES_GUIDE.md` and `kit/AGENTS.md_TEMPLATE.md` to create a short root instruction file for repository-aware coding agents.

Use `kit/CURSOR_RULE_TEMPLATE.mdc` for Cursor projects.

Do not commit private local preferences, secrets, credentials, raw personal data, or provider-specific session dumps.

---

## Positioning

Agent Memory Kit is useful when the owner wants a visible, editable, portable project memory rather than hidden provider memory or a loose chat summary.

It is not a full agent runtime. It can later be implemented through a memory framework, vector store, knowledge graph, IDE hook, eval harness, or agent platform, but the core value is the operating contract: what counts as project truth, what may be remembered, when the agent may act, and how failures become eval cases.
---

## Cursor, Codex, and GPT role stack

Recommended default:

```text
Cursor = primary implementation agent
Codex = restricted reviewer/auditor/recovery helper
GPT web chat = research, design, and task specs
Project Map = shared project truth
```

Use one shared workspace root when one Project Map governs multiple components. Use task scope and permission gates for safety.



## v3.8 Cursor settings and workspace authority

This release adds an owner-controlled Cursor Agent settings profile, `.cursorignore` guidance, settings audit commands, and the rule that an existing authoritative workspace file must be inspected and used rather than replaced by a generated fallback.

## v3.9.4 focus

Adds eval parity, live Cursor adoption checks, and explicit model-escalation triggers. Start with the lowest sufficient route and escalate only after reporting a concrete trigger (validation failure, schema/router conflict, insufficient context window, missing model control, repeated scoped failure, or task reclassification to audit/repair/protocol design).

## v3.9.4 Cursor provider model snapshot

v3.9.4 keeps dated Cursor model-routing snapshots as volatile capability observations. Exact Cursor model/settings advice must show snapshot date/ref and must not treat provider/model data as permanent project truth.

## v3.9.4

Adds stale-mirror eval-suite authority checks and live `.cursor` adoption guidance for rules and commands.
