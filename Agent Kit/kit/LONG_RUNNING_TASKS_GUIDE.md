# Long-Running Tasks Without Simulating Consciousness

Status: design guide
Purpose: show how to support longer agent work through explicit task state, evidence, permissions, and handoff artifacts instead of trying to imitate human consciousness.

---

## 1. Core framing

Do not design a giant artificial consciousness.

Design a **project case-management system**:

| Human analogy | Agent Memory Kit artifact |
|---|---|
| What the person knows is true | verified Project Map memory |
| What the person is working on now | Working State and active task contract |
| What the person is allowed to do | Permissions Policy and Action Intent Contract |
| What the person must not forget | constraints, risks, side-effect receipts, open questions |
| What the person would hand to a colleague | clean-slate handoff packet |
| What the person must prove before claiming | claim ledger and evidence refs |

The agent does not need a consciousness graph. It needs a small, current, evidence-bearing working set and safe transitions between steps.

---

## 2. Long-running task architecture

A robust long task uses these artifacts:

1. `source_authority.yaml` — decides which evidence wins.
2. `permissions_policy.yaml` — decides what actions are allowed.
3. `retrieval_policy.yaml` — decides what context is loaded for each profile.
4. `tasks/TASK-xxxx.yaml` — defines the current task contract.
5. `working_state.yaml` — tracks cursor, refs, blockers, checkpoint, and receipts.
6. `claim_ledger.yaml` — checks claims before final answer.
7. `handoffs/HO-xxxx.yaml` — allows clean-slate continuation.
8. `side_effects/receipts.yaml` — prevents duplicate external actions.

These are simpler and safer than a single huge memory structure.

---

## 3. Operating loop

For long tasks, use this loop:

```text
1. classify intent
2. check permission mode and scope
3. load task contract
4. hydrate minimal context by retrieval profile
5. execute only the allowed step
6. record claims and evidence
7. check final answer gate
8. update working state or propose memory delta only if allowed
9. create handoff if the task is not complete
```

The loop can run many times, but each step remains bounded.

---

## 4. Preventing unsupported project claims

The goal is not to make hallucination metaphysically impossible. The practical goal is to make unsupported project claims **invalid outputs**.

A project claim can appear in final output only if it is one of:

- supported by valid project evidence;
- explicitly labeled as an inference;
- explicitly listed as missing evidence;
- explicitly listed as a conflict;
- framed as a proposal, not a fact.

Unsupported project claims must be removed or downgraded before final output.

---

## 5. External research in long tasks

External research is useful, but it must stay in its lane.

Allowed:

- researching libraries;
- checking public documentation;
- comparing technical methods;
- finding domain techniques;
- studying market or regulatory background.

Not allowed:

- using web research to infer the current project implementation;
- treating a public pattern as proof that the project uses it;
- filling missing project facts with plausible generic knowledge.

Store external research as `research_output`, `procedure`, or decision input. Promote it to project fact only after project evidence or owner approval.

---

## 6. Clean-slate continuation

Do not rely on a very long chat being compressed forever.

When a task crosses a context boundary, create a handoff packet that a new run can read without the old transcript.

A good handoff contains:

- active task;
- checkpoint;
- current best state;
- must-read refs;
- next safe step;
- completed actions;
- unsafe-to-repeat actions;
- open questions;
- unresolved claims;
- required receipt checks.

This is closer to professional case notes than to consciousness.

---

## 7. Stop conditions

A long-running agent should stop and return a bounded answer when:

- evidence is missing and scope does not allow retrieval;
- the next step is mutating but not explicitly approved;
- source authority conflict is unresolved;
- claim gate fails;
- side-effect receipt is ambiguous;
- the task contract is missing a done definition;
- external research is needed but not allowed;
- the owner decision is required.

Stopping with a precise next step is correct behavior. Continuing by guessing is failure.
