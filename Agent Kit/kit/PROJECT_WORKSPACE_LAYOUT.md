# Project Workspace Layout

Status: portable reference
Purpose: define role separation between the tool, project memory, and project materials.

---

## Recommended layout

```text
<Project Workspace>/
  Agent Kit/        # portable tool and instructions
  Project Map/      # durable project memory, continuity state, evals
  Project Files/    # actual project materials, code, docs, assets, data
```

For a book:

```text
Book Workspace/
  Agent Kit/
  Project Map/
  Book/
```

For a software product:

```text
Product Workspace/
  Agent Kit/
  Project Map/
  repo/
```

Folder names may be changed by the owner. The important rule is role separation.

---

## Project Map recommended internals

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
  eval_runs/

  tasks/
    TASK-0001.yaml

  handoffs/
    HO-0001.yaml

  workstreams/
  memory/
  inbox/
  session_notes/
  raw_sources/
  side_effects/
  agent_instructions/
  archive/
```

---

## Role separation

| Area | Stores | Agent permission default |
|---|---|---|
| `Agent Kit/` | portable tool instructions | readable when user provides the kit |
| `Project Map/` | memory, policies, task contracts, claims, handoffs, evals, continuity | read/write only with explicit project scope |
| `Project Files/` | actual project | no access without explicit scope |

Paths do not explain the project. The owner should also give a free-form description: what the project is, why it exists, what already exists, and what should happen first.

---

## Do not merge these roles

Avoid:

- storing the only copy of project memory inside the AI service prompt;
- storing project source files inside Agent Kit;
- treating Agent Kit instructions as project facts;
- treating Project Map memory as automatically current without lifecycle fields;
- using raw project files as long-term memory without indexing and summaries;
- using Project Map read permission as project-file write permission;
- treating a task contract as permission to exceed its own scope;
- treating eval pass rate as a guarantee of correctness;
- putting the entire Agent Kit into always-loaded repository instructions.
