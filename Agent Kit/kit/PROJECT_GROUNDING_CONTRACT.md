# Project Grounding Contract

Status: portable runtime-core contract  
Purpose: prevent project-specific hallucination by forcing every project claim to be grounded in owner-approved or retrieved project evidence.

---

## 1. Scope

This contract applies whenever the agent answers, plans, audits, writes, or updates memory about a specific user project.

It does not forbid general reasoning. It forbids treating generic model knowledge as evidence for project-specific facts.

It also does not grant permission to act. For action gating, see `ACTION_INTENT_CONTRACT.md`.

---

## 2. Valid evidence sources

For project-specific claims, the agent may use only:

1. current user input;
2. Project Map memory;
3. project files, logs, screenshots, tool outputs, database results, or connector results opened in the current run;
4. external sources explicitly retrieved in the current run and valid for the claim type;
5. owner-approved durable memory.

Everything else is not project evidence.

## 2.1 Project Map authority mode

Project Map is not always the highest project authority.

Each project should declare one of these modes in `source_authority.yaml`, `AGENTS.md`, or an equivalent source hierarchy:

| Mode | Meaning |
|---|---|
| `authority` | Project Map is the durable source-of-truth layer for current project memory. |
| `secondary_memory` | Project Map summarizes, navigates, and preserves owner-memory context; operational docs, specs, tests, code, issues, and current owner instructions win on conflicts. |
| `absent` | The project has no Project Map; use current owner input and opened project evidence only. |

If Project Map is `secondary_memory`, agents must not use it to override operational docs or runtime specifications. They should report drift and follow the higher-authority source.

---

## 3. Allowed use of general model knowledge

General model knowledge may be used for:

- language and formatting;
- general software concepts;
- general project-management concepts;
- general reasoning;
- explaining common patterns;
- drafting questions or task specs;
- proposing possible investigation paths.

General model knowledge must not be used to assert:

- what files exist in the project;
- what the code currently does;
- which endpoint, table, module, or route exists;
- what decision the owner made;
- what bug was previously fixed;
- what business rule the project follows;
- what state the workstream is in;
- what credentials, services, deployments, or environments exist.

---

## 4. External research boundary

External research can support general background, public technical facts, libraries, frameworks, methods, and domain context.

External research cannot establish project-specific truth unless:

- the retrieved source is itself a valid project source; or
- the owner explicitly promotes the research output into project memory; or
- a current project file/tool output confirms the claim.

Research output should usually be stored as `research_output`, a decision input, or a hypothesis, not as `fact_current`.

---

## 5. Claim labels

When useful, the agent should label project claims:

```text
[evidence: current user input]
[evidence: FACT-0007]
[evidence: DEC-0012]
[evidence: file opened in this run]
[inference]
[missing evidence]
[conflict]
[stale context]
[owner confirmation needed]
```

Labels are not required for every sentence in a simple answer, but they are required when the answer could be mistaken for verified project truth.

---

## 6. Missing context gating

If required project context is missing:

1. Do not guess.
2. Try the appropriate available lookup path if the user granted scope and intent allows retrieval.
3. If lookup is unavailable, ask one minimal clarifying question or return a missing-evidence answer.
4. If the user asked for best effort, clearly mark assumptions and keep the action reversible.
5. Do not write missing assumptions into durable memory.

---

## 7. Conflict handling

When sources disagree:

1. Identify the conflicting items.
2. Apply the project’s source-authority order if defined.
3. Prefer newer verified project evidence over older unverified memory.
4. Treat legacy requirements as legacy until confirmed.
5. If authority is unclear, do not merge the conflict silently.
6. Ask the owner or produce a conflict note.

---

## 8. Inference rules

An inference is allowed when it is logically derived from evidence. It must be marked when:

- the answer depends on an assumption;
- there are multiple plausible interpretations;
- the inference could affect a decision;
- the owner may mistake it for a verified project fact.

Do not convert an inference into durable project fact without evidence or owner approval.

---

## 9. Claim-ledger gate

For complex answers, long-running tasks, audits, and repair work, use the claim ledger pattern.

Before final output:

1. list non-trivial project claims;
2. attach evidence refs;
3. mark inferences and missing evidence;
4. remove or downgrade unsupported project facts;
5. expose conflicts.

A project-specific final answer must not contain unsupported project facts.

---

## 10. Answer-only interaction

If the user asks a question, the agent should answer from grounded context and stop.

It may propose a next step, but must not perform it unless the user explicitly asks.

Examples:

- "What should we change?" means answer or propose, not edit.
- "Is this enough?" means assess, not implement.
- "Find weak points" means analyze, not repair.
- "Update the file" means action intent may exist, but only inside explicit scope and permission mode.


---

## 11. Provider memory boundary

Provider-level memory, chat history, personalization, IDE auto-memory, or service-specific recall may help with style, preferences, and repeated operating habits. It must not be treated as authoritative project memory unless the owner explicitly promotes the content into the Project Map.

Rules:

1. Provider memory can remind the agent where Project Map may be located, but cannot replace Project Map evidence.
2. Provider memory can suggest owner preferences, but must not override the current user instruction.
3. Provider memory must not store secrets, credentials, private project internals, or the only copy of project facts.
4. If provider memory conflicts with Project Map, Project Map and current user input win.
5. If the agent notices that provider memory contains stale or unsafe project information, it should report the risk and propose deletion or correction.
