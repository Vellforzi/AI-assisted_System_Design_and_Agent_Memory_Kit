# Owner Usage Guide

Status: practical user guide  
Purpose: explain how a project owner should use Agent Memory Kit day to day.

---

## 1. What the tool is

Agent Memory Kit is an external project memory system and behavior contract for AI-assisted work.

It helps the owner keep control over:

- what the agent is allowed to know about the project;
- where project truth comes from;
- when the agent may only answer;
- when it may read context;
- when it may propose changes;
- when it may apply changes;
- what should be remembered for future sessions;
- which repeated failures should become eval cases.

It is not a replacement for the model provider, IDE agent, tests, git, or security sandbox.

---

## 2. Daily workflow

Use this loop:

```text
Ask -> retrieve minimal context -> answer/analyze/plan -> owner decides -> apply only if explicit -> checkpoint -> propose memory delta if significant -> optional eval trigger.
```

The agent should not do the next action just because it found the next action.

---

## 3. Safe owner prompts

### Ask a question

```text
Use Agent Memory Kit.
Intent: answer.
Mode: read-only.
Scope: Project Map and relevant component docs only.
Question: <your question>
Do not change files or memory.
```

### Ask for analysis

```text
Use Agent Memory Kit.
Intent: analyze.
Mode: read-only.
Scope: <exact folders/files>.
Goal: analyze <topic> and report findings.
Do not apply fixes.
```

### Ask for a plan

```text
Use Agent Memory Kit.
Intent: plan.
Mode: dry-run.
Scope: <component/task>.
Goal: propose a staged plan.
Do not execute the plan.
```

### Ask for an edit

```text
Use Agent Memory Kit.
Intent: apply.
Mode: apply.
Scope: <exact files>.
Goal: <specific change>.
Allowed actions: <list>.
Forbidden actions: <list>.
After work: report diff, verification, Project Map delta proposal, and eval trigger.
```

---

## 4. Project Map update rule

The agent may propose a Project Map update after significant work.

It may apply the update only when the owner explicitly asks it to update Project Map or when an approved task contract includes memory maintenance.

---

## 5. Eval rule

The agent should propose evals when rule changes, memory policy changes, model/client changes, or repeated failures occur.

The owner may run evals manually, with the included checklist script, or later with a full harness.

---

## 6. Good solo-owner mode

For high control:

- keep tasks small;
- use one intent per request;
- make read-only the default;
- use apply only for exact files;
- review diffs yourself;
- keep Project Map compact;
- add eval cases only for real repeated or dangerous failures;
- avoid long-running autonomy until the Project Map is reliable.

---

## 7. What to store

Store:

- verified project facts;
- accepted decisions;
- constraints;
- source authority;
- risks;
- open questions;
- task state;
- handoffs;
- eval cases from real failures.

Do not store:

- secrets;
- raw chat as authoritative truth;
- unsupported assumptions;
- generic advice;
- external research as project truth;
- outdated facts as current facts.


---

## Cursor short-command workflow

When working in Cursor, prefer explicit commands:

```text
/answer      ask first
/analyze     inspect and explain
/plan        create a scoped task
/apply       perform one scoped change
/checkpoint  capture stage before context risk
/handoff     prepare fresh-session transfer
/map-apply   update Project Map from approved delta/handoff
/recover     resume from Project Map after context risk
/eval-smoke  check core behavior after rule/kit changes
```

If a chat is long, do not update Project Map directly from that chat. Ask for `/handoff` or `/map-delta`, then open a fresh session and use `/map-apply` with current Project Map plus the approved handoff/delta.

Platform summaries are not evidence.
