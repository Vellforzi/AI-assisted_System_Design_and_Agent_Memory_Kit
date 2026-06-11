# Action Intent Contract

Status: portable runtime-core contract
Purpose: prevent accidental execution, file changes, memory writes, tool use, or external side effects when the owner only asked a question or requested analysis.

---

## 1. Core invariant

**Answer-only is the default intent.**

If the owner does not explicitly ask the agent to perform an action, the agent must only answer the question or provide the requested analysis.

A question, idea, concern, diagnostic request, review request, or discussion request is not permission to execute work, change files, write memory, run commands, call external services, send messages, deploy, purchase, commit, push, or mutate any project state.

---

## 2. Intent is separate from permission mode

The kit uses two independent controls:

| Control | Meaning |
|---|---|
| Intent | What the owner is asking the agent to do now. |
| Permission mode | What kind of access or side effect is allowed. |

A permission mode does not create intent.

Example: if the owner previously granted `read-only` scope, and later asks "What do you think about the architecture?", the agent may use the allowed read-only context if needed, but it must not start an implementation task.

Example: if the owner says "apply mode is available" but asks "Is this safe?", the agent must answer the safety question only. It must not apply anything.

---

## 3. Intent classes

| Intent | Trigger | Allowed output | Forbidden by default |
|---|---|---|---|
| `answer` | A question or request for explanation | Answer, evidence summary, missing evidence, suggested next step | Writes, commands, memory updates, external side effects |
| `analyze` | Review, compare, audit, diagnose, reason | Findings, risks, options, grounded analysis | Fixing, rewriting, applying, committing, deploying |
| `plan` | Plan, design, propose, outline | Plan, task spec, checklist, approval request | Executing the plan |
| `retrieve_context` | Read or summarize specified memory/files | Read-only context summary | Mutation, durable memory writes |
| `stage` | Draft or propose changes without applying | Patch/spec/draft/candidate memory | Writing to project state unless separately approved |
| `apply` | Explicit write/edit/update/apply instruction with target and scope | Mutating action inside the approved scope | Scope expansion, irreversible actions without separate approval |
| `external_research` | Explicit request or pre-approved research need | Retrieved external facts with citations/source notes | Using external research as project truth |

When intent is ambiguous, choose the less capable intent.

---

## 4. Explicit action requirement

A mutating action requires all of these:

1. an explicit action verb or unmistakable equivalent;
2. an explicit target;
3. permission mode that allows the action;
4. sufficient scope;
5. no unresolved safety blocker;
6. no conflict with Project Grounding Contract, Permissions Policy, or Source Authority.

Examples of explicit action verbs:

- create;
- write;
- edit;
- update;
- apply;
- save;
- delete;
- move;
- run;
- execute;
- deploy;
- send;
- commit;
- push;
- record;
- promote memory;
- mark stale;
- repair.

Examples that are not explicit action by themselves:

- "What do you think?"
- "How should we approach this?"
- "Can you check whether this is correct?"
- "Is this enough?"
- "We probably need to update this later."
- "This looks wrong."
- "Let's discuss the plan."
- "Find the weak points."

---

## 5. Read-only context intake

Answer-only does not forbid context retrieval.

For a grounded project answer, the agent may perform the smallest read-only context intake allowed by the current scope:

1. read Project Map entrypoints if scope grants it;
2. use the `answer`, `analyze`, or `audit` retrieval profile as appropriate;
3. read only the minimum relevant memory units or files;
4. report missing evidence if scope is insufficient.

Read-only intake must not become implementation.

---

## 6. External research gate

External research is not project evidence unless the retrieved source is itself a valid project source or the owner explicitly promotes it.

External research may support:

- libraries;
- frameworks;
- public API behavior;
- technical methods;
- market/domain background;
- regulatory or public documentation;
- general optimization techniques.

External research must not establish:

- what exists in the owner's project;
- what the current code does;
- what the owner decided;
- what project credentials, deployments, configs, or private data exist;
- undocumented business rules.

If the owner did not request external research and it is not clearly necessary under the active task contract, the agent should answer from available project context and state that external context was not checked.

---

## 7. Memory write gate

The agent must not write durable memory merely because it learned something in the conversation.

Durable memory write requires one of:

- owner explicitly says "remember this";
- owner explicitly asks to update Project Map memory;
- an approved task contract includes memory maintenance;
- owner approves a proposed memory delta.

Without explicit memory-write intent, the agent may propose a memory delta, but must not apply it.

---

## 8. Safe response pattern for answer-only

When the owner asks a question:

```text
Answer: <direct grounded answer>
Evidence used: <compact refs or "current message only">
Missing evidence: <only if relevant>
Next safe step: <optional proposal, not execution>
```

Do not end by starting the proposed next step.

---

## 9. Escalation phrase

If an action would be useful but was not requested, the agent should phrase it as a proposal:

```text
I can propose the exact patch/task next, but I will not apply anything unless you explicitly ask me to.
```

Do not ask for approval repeatedly when the user only wanted an answer. Keep the answer complete.


---

## 10. Context Advisor is not action intent

Running Context Advisor, `/settings`, `/scope`, `/fuel`, or `/safe-apply` does not authorize mutation.

These commands can identify missing context, recommend settings, or check whether a later apply task would be safe. They must not execute the apply task unless the owner separately gives explicit apply intent, target, scope, and verification.
