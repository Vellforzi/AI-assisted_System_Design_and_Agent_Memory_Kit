# Agent Memory Kit

Version: v3.8.0

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
3. `kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`
4. `kit/secondary_memory_governance/README.md` for existing projects that already have strong operational docs and should be reinforced rather than replaced.
5. `kit/OWNER_USAGE_GUIDE.md`
6. `kit/ACTION_INTENT_CONTRACT.md`
7. `kit/PROJECT_GROUNDING_CONTRACT.md`
8. `kit/EVAL_SUITE_GUIDE.md`
9. `kit/EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`

---

## Default behavior

The agent must answer only unless the owner explicitly asks for a concrete action. Reading memory for context is not the same as permission to modify memory, files, database state, git state, cloud resources, or external systems.

After meaningful work, the agent may propose a Project Map delta and identify whether evals should run. It must not apply memory or rule changes unless the owner explicitly asks.

---

## Use in a repository

Use `kit/secondary_memory_governance/AGENTS_SNIPPET.md` when a mature existing project already has a project-specific `AGENTS.md`.

Use `kit/AGENT_INSTRUCTION_FILES_GUIDE.md` and `kit/AGENTS.md_TEMPLATE.md` only when the project does not already have a suitable root instruction file.

Use `kit/CURSOR_RULE_TEMPLATE.mdc` for Cursor projects.

For mature existing projects, patch the existing instruction file and add the secondary-memory governance overlay instead of replacing the project's current source-of-truth system.

Do not commit private local preferences, secrets, credentials, raw personal data, or provider-specific session dumps.

---

## Positioning

Agent Memory Kit is useful when the owner wants a visible, editable, portable project memory rather than hidden provider memory or a loose chat summary.

It is not a full agent runtime. The core value is the operating contract: what counts as project truth, what may be remembered, when the agent may act, and how failures become eval cases.

For existing repo-centric projects, start with `kit/secondary_memory_governance/`.
---

## Cursor, Codex, and GPT role stack

Recommended default:

```text
Cursor = primary implementation agent
Codex = restricted reviewer/auditor/recovery helper
GPT web chat = research, design, and task specs
Project Map = shared memory boundary, or source of truth only when the project's authority policy says so
```

Use one shared workspace root when one Project Map governs multiple components. Use task scope and permission gates for safety.



## v3.8 Cursor settings and workspace authority

This release adds an owner-controlled Cursor Agent settings profile, `.cursorignore` guidance, settings audit commands, and the rule that an existing authoritative workspace file must be inspected and used rather than replaced by a generated fallback.
