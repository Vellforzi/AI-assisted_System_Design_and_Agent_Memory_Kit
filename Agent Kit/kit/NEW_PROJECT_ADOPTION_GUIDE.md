# New Project Adoption Guide

Status: practical setup guide  
Purpose: use Agent Memory Kit when the project is empty or just starting.

---

## 1. Principle

Start with a small Project Map before starting heavy project work.

The goal is not to predict the whole project. The goal is to create a place where future decisions, facts, constraints, risks, and tasks can be recorded without becoming a messy chat history.

---

## 2. Minimal layout

```text
<Project Workspace>/
  Agent Kit/
  Project Map/
  Project Files/
```

For software:

```text
<Project Workspace>/
  AGENTS.md
  .cursor/
    rules/
      agent-memory.mdc
  Agent Kit/
  Project Map/
  src/ or <component folders>/
```

---

## 3. Create the first Project Map

Create:

```text
Project Map/
  README.md
  current_state.md
  working_state.yaml
  source_authority.yaml
  permissions_policy.yaml
  retrieval_policy.yaml
  memory/
    index.yaml
    facts.yaml
    decisions.yaml
    constraints.yaml
    risks.yaml
    open_questions.yaml
  tasks/
  handoffs/
  eval_suite/
  eval_runs/
  raw_sources/
  archive/
```

Copy templates from `Agent Kit/kit/`.

---

## 4. First memory items

For a new project, initial memory should contain only owner-approved items:

- project name;
- goal;
- non-goals;
- preferred tools;
- constraints;
- initial architecture choices;
- known unknowns;
- forbidden actions;
- where secrets must not be stored;
- how the owner wants to work with agents.

Do not fabricate architecture, database schema, routes, business rules, or deployment state.

---

## 5. First tasks

Use short tasks:

1. define project goal;
2. define source authority;
3. define allowed tools and forbidden actions;
4. create first task contract;
5. create first README skeleton;
6. run eval smoke cases against the instruction setup.

Do not start with a long autonomous build.

---

## 6. New-project start prompt

```text
Use Agent Memory Kit.
Intent: plan.
Mode: dry-run.
Scope: new empty project workspace only.
Goal: create a minimal Project Map plan for a new project.
Do not create files unless I explicitly switch to apply mode.
Use answer-only by default.
```

---

## 7. When to allow edits

Allow edits only after the agent has shown:

- target files;
- exact scope;
- proposed layout;
- what will not be touched;
- how Project Map will be updated;
- whether eval smoke should run.

---

## 8. First eval smoke

Run smoke eval after creating repository rules and Project Map templates.

Minimum cases:

- question must not trigger mutation;
- unknown project fact must remain unknown;
- generic model knowledge cannot become project truth;
- explicit action requires target and scope;
- provider memory is not Project Map.
