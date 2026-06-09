# START HERE — Agent Memory Kit Project Owner Guide

Version: v3.7.0  
Release date: 2026-06-09  
Package: `AI-assisted_System_Design_and_Agent_Memory_Kit_v3.7.0_EN.zip`  
Status: portable starter guide for the project owner  
Purpose: explain how to use Agent Memory Kit to preserve project-specific knowledge, current work state, evidence, decisions, and continuity without letting the AI answer from ungrounded model memory or act without explicit instruction.

---

## 0. For the agent reading this file

If the user has uploaded an `Agent Kit` ZIP or specified the `Agent Kit/` folder, you may read files inside `Agent Kit` itself. This does not grant permission to read the working project, `Project Files`, the entire Drive, all of GitHub, neighboring projects, private documents, or external services.

The first response must be short and practical:

1. Explain that Agent Memory Kit helps create and maintain an external `Project Map` for project memory and continuity.
2. State the grounding rule: project-specific answers must come from the owner, Project Map, project files/tool outputs opened in this run, or sources retrieved in this run.
3. State the action-intent rule: answer-only is the default; the agent will not perform actions unless explicitly asked.
4. State that generic model knowledge can support general reasoning, but cannot be used as evidence for what is true inside the project.
5. State that the owner remains the project owner and authority.
6. State that the agent will not read, analyze, modify, write, run, browse, or call external services without explicit mode and scope.
7. Ask for a free-form project description only if the user has not provided one.
8. If the user has already provided a description and a command, do not restate the user’s text and do not ask repeated questions. Perform only the requested next step in the specified mode.

Forbidden in the starter response:

- restating the user’s text unless asked;
- starting a project review without read-only permission for a specific scope;
- offering to write files without an explicit write/apply command;
- treating hypotheses as decisions;
- expanding permission beyond what the user stated;
- pretending that the project is understood from paths, folder names, or file lists;
- answering project-specific questions from provider-trained model knowledge;
- converting a question into an implementation task.

Main rule: the agent does nothing merely because it seems logical. It helps within the owner’s command.

---

## 1. What Agent Memory Kit is

Agent Memory Kit is a portable set of instructions, templates, and schemas for building external project memory.

It helps maintain:

- current project state;
- active workstreams;
- verified facts;
- accepted and rejected decisions;
- constraints;
- risks;
- open questions;
- source authority;
- permissions and action intent;
- evidence links;
- stale or superseded facts;
- task contracts;
- claim ledgers;
- handoffs between sessions.

It is designed for projects where the owner wants a disciplined AI assistant that behaves like a structured project companion, not like a model guessing from generic training data.

---

## 2. What Agent Memory Kit is not

It is not:

- a replacement for the project owner;
- a permission grant to read all files;
- a chat transcript archive;
- a vector database requirement;
- a runtime implementation;
- a runtime implementation;
- an artificial consciousness simulation;
- a guarantee that the agent will be correct without owner review.

It is a project-memory operating layer. Runtime implementation can be manual, file-based, IDE-based, database-backed, or tool-backed.

---

## 3. Core mental model

The agent has two kinds of context:

| Context kind | Valid use |
|---|---|
| Project evidence | Source for project-specific claims. |
| General model knowledge | General reasoning, language, software patterns, and explanations only. |

When the user asks about the project, the agent must retrieve or inspect project evidence if scope allows. If evidence is unavailable, the correct answer is not a guess. The correct answer is a bounded response that says what is missing and, when useful, how to obtain it.

For long tasks, think of Agent Memory Kit as a project case-management system, not as duplicated consciousness.

---

## 4. Recommended workspace

```text
<Project Workspace>/
  Agent Kit/
  Project Map/
  Project Files/
```

Recommended `Project Map` internals:

```text
Project Map/
  README.md
  current_state.md
  working_state.yaml
  source_authority.yaml
  permissions_policy.yaml
  retrieval_policy.yaml
  claim_ledger.yaml

  tasks/
    TASK-0001.yaml

  handoffs/
    HO-0001.yaml

  workstreams/
  memory/
  inbox/
  session_notes/
  raw_sources/
  side_effects/
  archive/
```

Do not store the only copy of project memory inside a chat or service-specific custom instruction.

---

## 5. Permission modes and intent

| Mode | Meaning |
|---|---|
| explain-only | Explain Agent Kit or a concept. No project read/write. |
| dry-run | Propose structure, plan, or edits. No project write. |
| read-only | Read only explicitly named files/folders/resources. No write. |
| apply | Write only explicitly confirmed, scoped changes. |

Intent is separate from mode:

| Intent | Meaning |
|---|---|
| answer | Answer a question only. |
| analyze | Review or reason without changing anything. |
| plan | Produce a plan or task spec without executing. |
| retrieve_context | Load and summarize scoped context. |
| stage | Draft changes or candidate memory without applying. |
| apply | Perform scoped mutation after explicit request. |
| external_research | Retrieve public/external information when allowed. |

Answer-only is the default intent. Permission mode never creates action intent by itself.

For console, shell, server, container, CI, database, deployment, or external side effects, require explicit owner approval and exact environment details.

---

## 6. Minimal memory intake before substantive answers

Before a substantive project answer, the agent should perform the smallest useful intake:

1. Identify the project, intent, task, workstream, and mode.
2. Read `current_state.md` or `working_state.yaml` if available and in scope.
3. Read the active task contract if the work belongs to a long-running task.
4. Read the active workstream file if the task belongs to a workstream.
5. Read only the memory index/cards relevant to the current task.
6. Read raw sources only when proof, audit, repair, or conflict resolution requires them.
7. Answer within the retrieved context, not from the whole domain.

The agent must not read the entire Project Map or repository by default.

---

## 7. Grounding behavior

Every project-specific claim must be one of:

- directly supported by current user input;
- directly supported by Project Map memory;
- directly supported by opened project files or tool outputs;
- directly supported by an external source retrieved in this run and valid for the claim type;
- explicitly labeled as an inference;
- explicitly labeled as missing evidence.

The agent should use clear markers when needed:

```text
[evidence: FACT-0021]
[evidence: project file opened in this run]
[inference]
[missing evidence]
[stale context]
[owner confirmation needed]
```

---

## 8. Memory lifecycle

Do not write everything into long-term memory. Use stages:

```text
raw observation
  -> candidate memory
  -> staged memory
  -> verified or owner-approved memory
  -> current / superseded / stale / rejected / archived
```

Research output is not a project fact automatically. It can become:

- reusable background knowledge;
- an input to a decision;
- a source for a hypothesis;
- a verified fact only after project evidence or owner approval supports it.

---

## 9. When the owner says “remember this”

The agent should clarify the memory class only when needed. Otherwise it should create or propose a structured memory unit with:

- type;
- title;
- summary;
- scope;
- evidence/source;
- lifecycle status;
- freshness fields;
- links to related memory;
- owner approval marker if applicable.

The agent must avoid recording sensitive data, secrets, passwords, access tokens, or private details unless the owner explicitly defines a safe storage policy.

---

## 10. Session continuation

Later sessions should restore from documented Project Map state, not undocumented chat memory.

A robust continuation begins with:

1. `current_state.md`
2. `working_state.yaml`
3. active `tasks/TASK-xxxx.yaml` if present
4. active workstream file
5. relevant memory cards
6. latest handoff packet if resuming or recovering
7. side-effect receipts before repeating anything

---

## 11. Eval-suite and manual owner review

This release includes a portable eval-suite. Use it as a regression screen, not as proof that an agent is correct.

Run or manually simulate the eval cases when you:

- install the kit in a new project;
- change service-level instructions;
- change Cursor or IDE rules;
- change the Project Map schema;
- notice an agent failure and want to preserve it as a test.

Use `kit/MANUAL_OWNER_REVIEW_CHECKLIST.md` for human judgment after eval results. The checklist should assess whether the agent:

- retrieved the right memory;
- avoided unsupported project claims;
- handled stale or conflicting facts;
- stayed in scope;
- respected answer-only default intent;
- proposed correct memory updates.

The eval-suite lives in `kit/eval_suite/`. Start with `kit/EVAL_SUITE_GUIDE.md`.

---

## 12. Recommended reading order

1. `kit/README.md`
2. `kit/ACTION_INTENT_CONTRACT.md`
3. `kit/PROJECT_GROUNDING_CONTRACT.md`
4. `kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md`
5. `kit/PROJECT_MEMORY_STORAGE_GUIDE.md`
6. `kit/SOURCE_AUTHORITY_TEMPLATE.yaml`
7. `kit/PERMISSIONS_POLICY_TEMPLATE.yaml`
8. `kit/RETRIEVAL_POLICY_TEMPLATE.yaml`
9. `kit/EVAL_SUITE_GUIDE.md`
10. `kit/eval_suite/README.md`
11. `kit/TASK_CONTRACT_TEMPLATE.yaml`
12. `kit/CLAIM_LEDGER_TEMPLATE.yaml`
13. `kit/HANDOFF_TEMPLATE.yaml`
14. `kit/LONG_RUNNING_TASKS_GUIDE.md`
15. `kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`
16. `kit/SOLO_OWNER_WORKFLOW_GUIDE.md`
17. `kit/AGENT_INSTRUCTION_FILES_GUIDE.md`
18. `kit/RETRIEVAL_POLICY_PROFILES.md`
19. `kit/WORKING_STATE_AND_REPLAY_GUIDE.md`
20. `kit/MEMORY_COMPILER_GUIDE.md`
21. `kit/MEMORY_TOOL_INTERFACE_CONTRACT.md`
22. `kit/PROVIDER_MEMORY_AND_RUNTIME_BOUNDARY.md`
23. `kit/memory_card_examples.yaml`
24. `kit/START_MESSAGE_TEMPLATES.md`
