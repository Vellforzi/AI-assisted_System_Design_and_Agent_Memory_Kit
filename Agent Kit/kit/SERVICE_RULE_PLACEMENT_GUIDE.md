# Service Rule Placement Guide

Status: portable guide  
Purpose: help place Agent Memory Kit rules in AI services without turning service instructions into the only source of project truth.

---

## 1. Placement principle

Put stable operating rules in service-level instructions.

Put project-specific facts in `Project Map/`.

Do not store the only copy of project truth in a service prompt, custom instruction, memory feature, or hidden assistant setting.

---

## 2. Runtime-core rule snippet

Use a short version of this in service-level instructions when possible:

```text
Use Agent Memory Kit rules for project work.
For project-specific claims, use only current user input, Project Map memory, project files/tool outputs opened in this run, or valid external sources retrieved in this run. Do not use provider-trained model knowledge as evidence for the user's project. If evidence is missing, say so, retrieve it if allowed, or ask one minimal clarification. Mark non-obvious reasoning as inference. Do not write durable memory from unsupported claims. Read the smallest sufficient memory context; do not load the whole project by default.

Answer-only is the default intent. If the user asks a question, requests analysis, asks for a review, or asks what should be done, answer or propose only. Do not write, edit, run commands, browse externally, update memory, commit, push, deploy, send messages, or perform other side effects unless the user explicitly asks for that action with target, mode, and scope. Permission mode does not imply action intent.
```

---

## 3. What belongs in Project Map, not service rules

- current project facts;
- routes, modules, schemas, endpoints, tables;
- business rules;
- owner decisions;
- constraints;
- workstream state;
- active task contracts;
- source authority;
- permissions policy;
- claim ledgers;
- handoff packets;
- side-effect receipts.

---

## 4. What belongs in service rules

- always apply grounding contract;
- answer-only default intent;
- no project facts from model memory;
- no side effects without explicit action request;
- ask for scope before reading project materials;
- propose before writing if mode is not apply;
- preserve secrets and credentials;
- use Project Map for continuity.

---

## 5. Avoid service-specific lock-in

The Project Map should remain readable outside any single provider.

Prefer Markdown and YAML for durable memory. If a service provides native memory, use it only as a recall aid or pointer layer, not as the only project memory.


---

## 6. Repository instruction files

For coding agents, place a short repository-level instruction file near the project root when the tool supports it, for example:

- `AGENTS.md`;
- `.cursor/rules/*.mdc`;
- `CLAUDE.md`;
- service-specific project rules.

Keep these files short. They should point to the Project Map and summarize the invariant operating rules. They should not duplicate the full Project Map or the full Agent Kit.

Recommended contents:

1. project name and root layout;
2. where the Project Map lives;
3. source-of-truth order;
4. answer-only default intent;
5. no project facts from model memory;
6. no side effects without explicit apply intent;
7. read-only default for audits and analysis;
8. required docs or memory updates after implementation.

Use `AGENT_INSTRUCTION_FILES_GUIDE.md`, `AGENTS.md_TEMPLATE.md`, and `CURSOR_RULE_TEMPLATE.mdc` as starters.
