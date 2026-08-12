# AI-assisted System Design — Method Guide

Version: v3.9.0 (method text). Package: v4.0.0.
Status: portable methodology note
Purpose: help a project owner run a project as an AI-readable engineering system without letting the AI become an ungrounded source of project truth.

---

## 1. Definition

AI-assisted System Design is a way to organize a project so that human intent, project state, technical contracts, implementation work, verification, and documentation remain readable by both humans and AI agents.

The goal is not to make the AI "just write code" or "just generate documents". The goal is to create a controlled operating environment where the agent can help because the project itself exposes clear context, boundaries, and evidence.

---

## 2. Core principles

### 2.1 The owner remains the source of intent

The owner defines:

- what the project is;
- why it exists;
- what matters now;
- what tradeoffs are acceptable;
- what work is allowed;
- what must not be changed.

The agent may analyze, propose, draft, or implement only inside the mode and scope granted by the owner.

### 2.2 The project must become AI-readable

A project becomes AI-readable when it has explicit artifacts such as:

- project brief;
- repository map;
- route/API reference;
- database/schema reference;
- domain notes;
- worklog;
- active task state;
- decisions and constraints;
- risks and open questions;
- verification commands;
- handoff notes.

These artifacts are more reliable than raw chat history.

### 2.3 The agent must not invent project facts

For project-specific claims, the agent must use only:

- the current owner instruction;
- Project Map memory;
- project files or tool outputs opened in the current run;
- external sources retrieved in the current run.

If evidence is missing, the agent must say that evidence is missing. It may propose how to find it, but it must not answer from general model memory.

### 2.4 Small scoped tasks beat broad heroic tasks

AI agents are more reliable when work is split into small units with:

- one goal;
- exact files or folders;
- clear permission mode;
- expected output;
- verification method;
- documentation update target;
- rollback or stop condition.

### 2.5 Manage capability; do not rank model IQ

Unconstrained agents produce plausible junk. That does not prove a model
IQ ceiling. It proves the project has no contour: grounding, answer-only
default, apply gates, behavioral oracles, independent review, and owner
smoke.

The methodology layer and the memory kit are that contour plus a guide for
installing it on Cursor and Codex. Structural unit tests still encode
internals; they are not the primary chain if the owner is not reading
every generated line. See Agent Memory Kit files
`CAPABILITY_MANAGEMENT.md` and `BEHAVIORAL_ORACLES.md`.

---

## 3. Recommended project operating loop

```text
Owner intent
  -> project brief / current task
  -> context intake
  -> scope and mode selection
  -> plan or patch proposal
  -> implementation by the authorized agent
  -> verification
  -> documentation update
  -> memory delta
  -> owner review
```

For a code project, this usually means:

1. Read the project AI brief or agent instructions.
2. Read only the active worklog / active task entry.
3. Read only the relevant domain, route, schema, or service files.
4. Produce a focused decision or task plan.
5. Let the implementation agent make changes only after explicit owner permission.
6. Verify with the project’s own commands.
7. Update docs and memory.

---

## 4. Recommended repository artifacts

```text
repo/
  AGENTS.md or PROJECT_AI_BRIEF.md
  docs/
    WORKLOG.md
    ROUTES_REFERENCE.md
    SCRAPER_JOBS.md
    domains/
    PHASE_GATES.md
  db_sql/
  src/ or app/
  tests/
```

The exact structure depends on the project. The stable rule is that the agent must know where authoritative facts live.

---

## 5. Authority hierarchy

When sources disagree, use a declared source-of-truth hierarchy.

Example for a software product:

1. Current owner instruction.
2. Current production code and schema.
3. Project docs that are explicitly marked current.
4. Worklog and recent verified outputs.
5. Legacy requirements, marked as legacy until confirmed.
6. Research notes, marked as research until promoted.
7. Chat history, never authoritative unless captured into Project Map.

For any project, define the hierarchy in `Project Map/source_authority.yaml` or an equivalent file.

---

## 6. Interaction with Agent Memory Kit

AI-assisted System Design defines how the project should be operated. Agent Memory Kit defines how project knowledge should be remembered and retrieved.

Use Agent Memory Kit when:

- a later session must continue from prior work;
- a decision must be remembered;
- old facts may conflict with new facts;
- the project has multiple workstreams;
- the agent must avoid using generic model knowledge as project truth;
- current state needs to survive context trimming or chat resets.

---

## 7. Completion contract for agents

Before finalizing a substantive answer, the agent should check:

1. Did it stay inside the requested mode and scope?
2. Did it use valid project evidence for project-specific claims?
3. Did it label assumptions, inferences, and missing evidence?
4. Did it avoid unnecessary broad context loading?
5. Did it produce the requested output format?
6. Did it avoid external side effects unless explicitly authorized?
7. Did it identify any memory update that should be proposed or staged?

---

## 8. Anti-patterns

Avoid:

- treating chat history as durable memory;
- asking the same setup questions every session;
- reading the whole repository by default;
- treating file paths or folder names as project understanding;
- turning every task into a full audit;
- promoting research notes to verified project facts automatically;
- mixing old decisions with current decisions without lifecycle fields;
- giving confident project answers without source refs;
- adding process overhead that blocks product progress.

---

## 9. Minimal session template

```text
Active layer: AI-assisted System Design.
Project: <name>.
Mode: explain-only / dry-run / read-only / apply.
Scope: <exact files/folders or none>.
Goal: <one goal>.
Known source-of-truth order: <brief list or Project Map path>.
Expected output: <decision / design / task for implementation agent / docs draft / review>.
```

If the task touches project memory, also load the Agent Memory Kit grounding contract.


---

## Agent action-intent boundary

In AI-assisted system design, distinguish discussion from execution.

A design question, architecture review, or planning request does not authorize repository changes. The agent should produce analysis, decisions, or task specs until the owner explicitly requests implementation with target, mode, and scope.

For multi-step work, prefer explicit task contracts and handoffs over a long implicit chat state.
