# Existing Project Adoption Guide

Status: practical migration guide  
Purpose: install Agent Memory Kit into an already active project without freezing development or forcing autonomous long-running agents.

---

## 1. Adoption principle

Do not begin by making the agent understand everything.

Begin by making the project readable enough that the agent can answer and plan safely.

For an existing project, the first goal is not full automation. The first goal is a trustworthy Project Map that prevents repeated re-explanation and blocks unsupported project claims.

---

## 2. Recommended target layout

For a multi-component software project:

```text
<Project Root>/
  AGENTS.md                         # short shared instruction entrypoint
  Project Map/                      # durable project memory
  Agent Kit/                        # copied or vendored toolkit
  Options_api/                      # project component
  Options_scraper/                  # project component
  Options_MT/                       # project component
```

If the project is already on a shared drive, keep the same separation:

```text
Dev Projects/Job/
  Project Map/
  Agent Kit/
  Options_api/
  Options_scraper/
  Options_MT/
```

Do not mix Project Map files into source-code folders unless they are component-scoped instruction files.

---

## 3. Minimum viable Project Map

Create only these files first:

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

Then populate a small first version:

- project identity;
- component map;
- current active task;
- known authoritative docs;
- known unknowns;
- unsafe assumptions;
- owner preferences for agent behavior.

Do not wait until the map is perfect. A small verified map is better than a large invented one.

---

## 4. Suggested component source authority

For a project with API, scraper, and trading-terminal components, use component-specific authority.

Example:

```yaml
components:
  api:
    source_order:
      - "Options_api/app/routes/"
      - "Options_api/app/services/"
      - "Options_api/database/models.py"
      - "docs/ROUTES_REFERENCE.md"
      - "Project Map/memory/"
  scraper:
    source_order:
      - "Options_scraper/app/main.py"
      - "docs/SCRAPER_JOBS.md"
      - "Project Map/memory/"
  metatrader:
    source_order:
      - "Options_MT/"
      - "Project Map/memory/"
  database:
    source_order:
      - "db_sql/04_public_tables.sql"
      - "*/database/models.py"
      - "Project Map/memory/"
```

Treat this as a starter. The owner should adjust actual paths to match the project.

---

## 5. First adoption tasks

Run these as separate owner-controlled tasks:

1. **Inventory only**: agent lists project folders and proposes Project Map skeleton. No edits unless explicitly approved.
2. **Source authority draft**: agent identifies likely authoritative files and marks unknowns.
3. **Current state draft**: agent writes a compact state summary from owner input and verified files.
4. **Component map**: agent creates a small component index: API, scraper, MetaTrader, docs, database.
5. **Memory seed**: agent creates initial decisions/facts/constraints only from evidence.
6. **Significant-work rule**: add the checkpoint/footer rule to AGENTS.md or Cursor rules.
7. **Eval smoke test**: run 5-10 core eval cases before trusting the setup.

Each task should have a clear output and owner review.

---

## 6. What not to do during adoption

Avoid:

- asking the agent to read the entire project without a target;
- letting the agent rewrite README, docs, memory, and code in one task;
- putting large Project Map content into always-loaded rules;
- treating old chat summaries as authoritative facts;
- storing secrets in memory;
- enabling autonomous long-running work before source authority and working state exist.

---

## 7. First root `AGENTS.md`

Use `AGENTS.md_TEMPLATE.md` as the starting point.

The root instruction file should do three things only:

1. identify the Project Map entrypoints;
2. state default answer-only behavior;
3. define read/write gates and component scope.

Keep deep explanations in `Agent Kit/kit/`, not in the always-loaded root instruction.

---

## 8. When adoption is mature enough

The project is ready for heavier agent work when:

- current state is accurate;
- source authority is clear;
- at least the active workstream has verified memory;
- task contracts exist for multi-step work;
- side-effect receipts are used;
- eval smoke tests pass;
- the agent reliably reports Project Map and eval triggers after significant work;
- the owner can start a clean session and the agent can resume from Project Map without chat history.

Only then consider longer semi-autonomous tasks.
