# Solo Owner Workflow Guide

Status: practical workflow guide  
Purpose: help one project owner use Agent Memory Kit with high control, local IDE agents, and research-focused chat assistants.

---

## 1. Recommended operating model

Use two roles:

1. **Research and analysis assistant** — used for thinking, comparison, architecture, audits, external research, and drafting instructions.
2. **Implementation agent** — used inside the local project workspace to read files and apply owner-approved changes.

For many owners this maps naturally to:

- ChatGPT Pro or another research assistant for analysis;
- Cursor or another IDE agent for repository work.

The research assistant should not be treated as having live project truth unless you upload or retrieve the evidence. The implementation agent should not be allowed to improvise beyond the Project Map and task contract.

---

## 2. Daily loop

A controlled solo loop:

```text
1. Ask / analyze / plan.
2. Retrieve only the Project Map context needed.
3. Decide the next small task.
4. Give the implementation agent a scoped task.
5. Review the diff/output.
6. Decide whether the work was significant.
7. Update or propose Project Map updates: current_state, working_state, decisions, facts, open questions.
8. Run or propose a small eval when instructions, memory policy, model/client, permissions, or repeated failures changed.
```

The owner remains the scheduler, reviewer, and final source of intent.

---

## 3. Modes to use deliberately

### Answer mode

Use for:

- understanding;
- project questions;
- risk analysis;
- architecture discussion;
- deciding whether a task is worth doing.

No mutation.

### Plan mode

Use for:

- breaking work into safe chunks;
- drafting Cursor tasks;
- choosing files to inspect;
- designing verification.

No mutation.

### Apply mode

Use only after the owner gives:

- task ID or clear goal;
- target paths;
- allowed actions;
- forbidden actions;
- verification command or review method;
- expected output.

---

## 4. Recommended Cursor-style task format

Use a compact task block:

```text
Task: <one goal>
Mode: apply
Project Map refs: <current_state, task, decisions, facts>
Scope: <paths>
Allowed: <read/edit/test commands>
Forbidden: <db writes, deploy, secrets, unrelated files>
Expected result: <specific artifact or diff>
Verification: <tests or manual checks>
After work: summarize changed files, verification, significant-work status, proposed Project Map updates, handoff need, and eval trigger. Do not update Project Map unless explicitly asked.
```

This keeps control with the owner and reduces broad autonomous wandering.

---

## 5. When to use ChatGPT vs local IDE agent

Use research chat for:

- comparing options;
- summarizing external research;
- designing memory schemas;
- writing prompts and task specs;
- reviewing output from Cursor;
- deciding architecture direction.

Use local IDE agent for:

- reading actual repository files;
- editing code;
- running tests;
- producing diffs;
- updating docs after approval.

Do not ask the research chat to invent repository facts. Upload evidence or ask the IDE agent to gather it.

---

## 6. Memory maintenance cadence

At the end of meaningful sessions, use `SIGNIFICANT_WORK_AND_CHECKPOINTS.md`. Then:

- update `Project Map/current_state.md`;
- update `Project Map/working_state.yaml`;
- add or revise memory cards only for durable facts/decisions/constraints;
- record open questions;
- record side-effect receipts for actions already taken;
- create a handoff if the next session should continue cleanly.

Do not save every conversation. Save what affects future work.

---

## 7. Practical rule for long-running agents

Do not use long-running autonomous agents until the project passes this threshold:

- Project Map exists and is current;
- active workstreams are indexed;
- source authority is known;
- the implementation agent can resume from working_state without the previous chat;
- eval smoke tests pass;
- owner is comfortable reviewing proposed changes quickly.

Before that threshold, use short tasks and explicit gates.


---

## 8. If you forget evals

A file-first kit cannot force evals to run by itself.

Mitigation:

- require the agent to report `Eval trigger: yes/no` after significant work;
- run the checklist helper after instruction or policy changes;
- convert repeated failures into eval cases;
- keep the smoke suite small enough that running it is not annoying.

For a solo owner, the best default is not full automatic grading. The best default is a visible trigger that reminds the owner when a check is needed.
