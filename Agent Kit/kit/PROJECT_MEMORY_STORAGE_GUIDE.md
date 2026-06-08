# Project Memory Storage Guide

Status: portable guide  
Purpose: show how to store operational memory, long-term memory, working state, evidence, policies, task contracts, claims, handoffs, and lifecycle metadata without context inflation.

---

## 1. Core principle

Do not store project memory as one growing document or chat transcript.

Store it as:

- compact entrypoints;
- typed memory units;
- indexes;
- working state;
- task contracts;
- source authority;
- permissions policy;
- retrieval policy;
- claim ledger;
- eval suite and eval runs;
- handoffs;
- raw evidence;
- archive.

The agent should usually load:

1. current state;
2. policy files needed for the current intent;
3. working state;
4. active task contract if present;
5. relevant index entries;
6. only the needed memory units;
7. raw sources only when necessary.

---

## 2. Recommended layout

```text
Project Map/
  README.md
  current_state.md
  working_state.yaml
  source_authority.yaml
  permissions_policy.yaml
  retrieval_policy.yaml
  claim_ledger.yaml

  eval_suite/
    eval_manifest.yaml
    eval_trigger_policy.yaml
    core_behavior_eval_cases.yaml
    grader_rubric.yaml
    failure_to_eval_case_template.yaml

  eval_runs/
    EVAL-RUN-0001.yaml
    traces/
      TRACE-0001.yaml

  tasks/
    TASK-0001.yaml

  handoffs/
    HO-0001.yaml

  workstreams/
    WS-0001.md
    WS-0001.history.md
    WS-0001.sources.md

  memory/
    index.yaml
    decisions.yaml
    facts.yaml
    constraints.yaml
    risks.yaml
    open_questions.yaml
    cards/
      DEC-0001.yaml
      FACT-0001.yaml

  inbox/
    owner_requests.md
    raw_observations.md
    candidate_memory.yaml

  session_notes/
    2026-06-08-session.md

  raw_sources/
    chats/
    logs/
    screenshots/
    files/
    tool_outputs/

  side_effects/
    receipts.yaml

  agent_instructions/
    AGENTS.md
    cursor_rule.mdc

  archive/
    superseded/
    stale/
    legacy/
```

This layout is a recommendation, not a mandatory filesystem contract. The owner may adapt names.

---

## 3. Entrypoints

### `README.md`

Explains what the Project Map contains and what to read first.

### `current_state.md`

A short human-readable state file. Suggested length: 20-80 lines.

Should include:

- project identity;
- current phase;
- active workstreams;
- immediate priorities;
- known blockers;
- latest owner decisions;
- where authoritative references live.

### `working_state.yaml`

Machine-readable compact replay root.

Should include:

- current task cursor;
- active workstream;
- active task contract ref;
- checkpoint;
- branch scope;
- obligations;
- blockers;
- pending actions;
- mandatory memory refs;
- side-effect guards and receipts.

### `source_authority.yaml`

Machine-readable source authority order. Use `SOURCE_AUTHORITY_TEMPLATE.yaml` as a starter.

### `permissions_policy.yaml`

Machine-readable permission and intent policy. Use `PERMISSIONS_POLICY_TEMPLATE.yaml` as a starter.

### `retrieval_policy.yaml`

Machine-readable profile rules for context hydration. Use `RETRIEVAL_POLICY_TEMPLATE.yaml` as a starter.

### `claim_ledger.yaml`

Runtime or review artifact that checks claim support before final output. Use `CLAIM_LEDGER_TEMPLATE.yaml` as a starter.

### `eval_suite/`

Portable test cases and trigger policy that check whether the agent follows Project Map rules. Use `EVAL_SUITE_GUIDE.md`, `EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`, and files under `eval_suite/` as starters.

### `eval_runs/`

Run reports and failure traces from manual or automated eval runs. Keep these concise. They are not full chat transcripts.

---

## 4. Long-task artifacts

### `tasks/TASK-xxxx.yaml`

Use task contracts for work that may span sessions, involve multiple steps, need external research, or require strict permission boundaries.

A task contract should define:

- intent;
- permission mode;
- scope;
- goal;
- non-goals;
- allowed and forbidden actions;
- required evidence;
- done definition;
- verification recipe;
- handoff policy.

### `handoffs/HO-xxxx.yaml`

Use handoff packets to continue work in a clean context window.

A handoff should include:

- active task;
- checkpoint;
- current best state;
- must-read refs;
- next safe step;
- completed actions;
- unsafe-to-repeat actions;
- open questions;
- unresolved claims.

---

## 5. Long-term memory classes

Recommended memory classes:

| Class | Meaning |
|---|---|
| `fact_current` | Verified current project fact. |
| `fact_stale` | Previously true or recorded fact that is no longer current or may be outdated. |
| `accepted_decision` | Owner-approved or project-accepted decision. |
| `rejected_decision` | Explicitly rejected option. |
| `constraint` | Persistent limitation or rule. |
| `risk` | Known risk or failure mode. |
| `open_question` | Unresolved question requiring owner or evidence. |
| `hypothesis` | Plausible but unverified claim. |
| `research_output` | External research note, not automatically project truth. |
| `procedure` | Reusable project workflow. |
| `side_effect_receipt` | Record of external action already taken. |
| `eval_case` | Reusable behavior test for the agent/memory system. |
| `eval_result` | Outcome of a specific test run. |
| `eval_trace` | Short failure trace used to diagnose an eval regression. |

---

## 6. Canonical memory unit fields

A durable memory unit should contain:

```yaml
id: FACT-0001
schema_version: 3.3.0
class: fact_current
status: current
review_state: verified
scope: project.component
branch_scope: main
created_at: "2026-06-08"
updated_at: "2026-06-08"
last_verified_at: "2026-06-08"
valid_until: null
confidence: high
authority_rank: 2
title: "Short title"
summary: "One compact statement."
details: "Optional detail."
evidence:
  - kind: project_file
    ref: "path/to/file.ext:line-range or tool output id"
    quote: "Optional short quote."
source_authority:
  kind: project_file
  ref: "path/to/file.ext"
links:
  related: []
  supersedes: []
  superseded_by: []
retrieval_tags: [component, topic]
owner_approved: false
```

---

## 7. Index design

`memory/index.yaml` should be compact and retrieval-oriented.

It should not duplicate full cards. It should include:

- ID;
- class;
- status;
- title;
- summary;
- scope;
- tags;
- last verified date;
- related IDs;
- source authority rank.

---

## 8. Raw sources

Raw sources are evidence, not memory by themselves.

Keep raw sources when they are needed for:

- audit;
- legal or business traceability;
- exact quotation;
- reproduction;
- repair;
- provenance.

Do not put raw source dumps into normal answer context unless required.

---

## 9. Stale and superseded memory

When a new fact replaces an old fact, do not delete the old fact. Mark it as stale or superseded and link both units.

Stale memory can be useful for audit and repair, but it must not appear as current truth in normal answer context.

---

## 10. Policy file priority

When present, the agent should read policy files before deep retrieval:

1. `permissions_policy.yaml` — what the agent may do;
2. `source_authority.yaml` — what evidence wins;
3. `retrieval_policy.yaml` — what memory classes may be loaded for the current intent.

If these files are missing, the agent should use the conservative defaults in this kit and state that project-specific policy is missing.
