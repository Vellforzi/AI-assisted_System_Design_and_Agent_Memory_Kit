# Project Memory Operating Protocol

Status: portable global protocol  
Purpose: make every substantive AI answer start from the smallest useful project-memory context and end with grounded, reviewable output.

---

## 1. Core idea

Every project has two primary memory layers and one control layer.

| Layer | Meaning | Examples |
|---|---|---|
| Operational memory | what is happening now | current task, active workstream, blocker, next step, pending owner decision |
| Long-term memory | stable project knowledge | verified facts, accepted decisions, constraints, risks, domain rules, source authority |
| Working State | compact replay control state | cursor, obligations, refs, branch, checkpoint, side-effect receipts |

The owner should not repeatedly explain the same project context. The agent should restore relevant context from Project Map, then answer or act inside the current task.

The agent must not confuse context restoration with permission to act.

---

## 2. First principle: memory is not transcript

Do not store memory as a growing chat log.

Store:

- small linked memory units;
- indexes;
- current state;
- active task contracts;
- active workstream files;
- evidence references;
- lifecycle metadata;
- source authority;
- permissions policy;
- handoff packets;
- eval cases and eval run notes;
- raw sources only where needed.

Raw chat, logs, and transcripts belong in `raw_sources/`, `session_notes/`, or `archive/`. They are not automatically long-term memory.

---

## 3. Action intent first

Before any project work, classify intent:

1. `answer`
2. `analyze`
3. `plan`
4. `retrieve_context`
5. `stage`
6. `apply`
7. `external_research`

Answer-only is the default intent.

If the user asks a question or requests analysis, the agent may produce an answer, analysis, missing-evidence note, or proposed next step. It must not perform mutating actions, write durable memory, run commands, browse externally, send messages, deploy, commit, push, or change files unless the owner explicitly asks for that action.

Permission mode does not imply action intent. `apply` mode only allows execution after the owner asks for a specific action with target and scope.

See `ACTION_INTENT_CONTRACT.md`.

---

## 4. Minimal memory intake

Before a substantive project answer:

1. Identify project, intent, task, workstream, permission mode, and requested output.
2. Load policy entrypoints if available and in scope:
   - `Project Map/source_authority.yaml`
   - `Project Map/permissions_policy.yaml`
   - `Project Map/retrieval_policy.yaml`
3. Load operational entrypoints first:
   - `Project Map/current_state.md`
   - `Project Map/working_state.yaml`
   - active `Project Map/tasks/TASK-xxxx.yaml` if known
   - active workstream file if known.
4. Use the memory index to find relevant long-term units.
5. Load only the memory cards needed for the task.
6. Escalate to raw sources only when proof, conflict resolution, audit, repair, or exact quotation requires it.
7. Narrow the answer to the current task.

Do not read the whole repository, whole Drive, whole Project Map, or whole chat by default.

---

## 5. Grounding contract

For project-specific claims, use only:

- current user input;
- Project Map memory;
- project files or tool outputs opened in the current run;
- external sources retrieved in the current run and valid for the claim type;
- owner-approved durable memory.

If evidence is missing, do not guess. Mark missing evidence or ask for scope to retrieve it.

Generic model knowledge may support general reasoning, but not project truth.

---

## 6. Retrieval profiles

Use the retrieval profile that matches the task:

| Profile | Use when | Default behavior |
|---|---|---|
| `answer` | answering a project question | current verified facts and decisions only; no stale facts as valid context; no mutation |
| `analyze` | reviewing, comparing, diagnosing, or reasoning | read-only findings; no mutation; inference labels where needed |
| `plan` | planning next work | current state, active task, constraints, risks, relevant decisions; no execution |
| `resume` | continuing a task | working state checkpoint, active task contract, active workstream, mandatory refs |
| `recover` | recovering after lost context or failure | working state, recent handoff, side-effect receipts, raw-source escalation if needed |
| `fork` | exploring alternative branch | branch-local state plus shared stable memory; no future branch leakage |
| `audit` | checking correctness | current and stale memory, raw evidence, conflicts, source authority; no mutation by default |
| `repair` | fixing memory/project state | stale, invalidated, conflicting, and raw evidence allowed as repair input; mutation requires apply |

See `RETRIEVAL_POLICY_PROFILES.md` and `RETRIEVAL_POLICY_TEMPLATE.yaml`.

---

## 7. Completion contract

Before finalizing:

1. Check intent: did the response stay inside answer/analyze/plan/apply as requested?
2. Check scope: did the answer stay inside the user’s mode and files?
3. Check grounding: are project claims supported, labeled as inference, or marked missing?
4. Check claim gate: did every non-trivial project claim pass the final-answer gate?
5. Check completeness: did the answer satisfy every explicit requirement?
6. Check freshness: did stale or superseded facts get suppressed or labeled?
7. Check conflicts: did contradictions remain visible?
8. Check side effects: no irreversible action without explicit permission.
9. Check memory delta: should any memory update be proposed or staged, not silently applied?

---

## 8. Claim ledger

For complex answers, audits, or long tasks, use a claim ledger.

A claim ledger records:

- claim statement;
- claim type;
- evidence refs;
- source authority rank;
- confidence;
- whether it may appear in final answer;
- whether it must be labeled.

Unsupported project facts must be removed, marked missing evidence, or downgraded to inference/proposal before final output.

See `CLAIM_LEDGER_TEMPLATE.yaml`.

---

## 9. Memory update rules

After significant work, the agent should consider whether a memory delta is needed. Use explicit triggers from `SIGNIFICANT_WORK_AND_CHECKPOINTS.md`; do not rely on vague intuition.

Write or propose memory only when the item is:

- durable beyond the current chat;
- project-specific;
- useful for future retrieval;
- grounded in evidence or owner approval;
- not a secret or unsafe content;
- not merely a temporary conversational detail.

Do not write long-term memory from:

- unsupported assumptions;
- generic advice;
- raw research output not promoted by the owner;
- old facts that may be superseded;
- private credentials or secrets.

Without explicit memory-write intent, propose a memory delta instead of applying it.

---

## 10. Memory lifecycle

Use this lifecycle:

```text
raw_observation
  -> candidate
  -> staged
  -> verified / owner_approved
  -> current / stale / superseded / rejected / archived
```

Recommended fields:

- `status`
- `review_state`
- `created_at`
- `updated_at`
- `last_verified_at`
- `valid_until`
- `confidence`
- `authority_rank`
- `supersedes`
- `superseded_by`
- `evidence`
- `source_authority`
- `retrieval_tags`

---

## 11. Source authority

Projects should define source authority in `Project Map/source_authority.yaml`.

Example order for a software project:

1. current owner instruction;
2. current code/schema/tool output;
3. current Project Map memory;
4. current docs;
5. recent verified logs;
6. legacy requirements, marked legacy;
7. research notes, not automatically facts;
8. chat history, not authoritative unless captured.

When there is no source-authority file, the agent should state that authority is unclear instead of silently choosing.

---

## 12. Stale and superseded facts

A stale fact is not deleted. It is preserved for:

- audit;
- repair;
- historical reasoning;
- avoid-list context;
- explaining why a prior decision changed.

But it must not be used as current project truth in `answer`, `analyze`, `plan`, or `resume` profiles unless explicitly labeled as stale.

---

## 13. Long-running tasks

For tasks that span sessions or many steps, create or use a task contract:

- `Project Map/tasks/TASK-xxxx.yaml`

The task contract should define:

- goal;
- non-goals;
- intent;
- mode;
- scope;
- allowed and forbidden actions;
- required project evidence;
- done definition;
- verification recipe;
- handoff policy.

See `TASK_CONTRACT_TEMPLATE.yaml` and `LONG_RUNNING_TASKS_GUIDE.md`.


---

## 14. Significant work and checkpoints

A task has reached an after-work checkpoint when the answer, analysis, plan, applied change, audit result, failure state, or handoff cursor is stable enough that a future session would lose important context without a note.

The agent should check whether any of these are needed:

- Project Map delta proposal;
- working-state checkpoint;
- handoff packet;
- stale/superseded memory repair;
- eval trigger;
- candidate eval case from a failure.

In answer/analyze/plan modes, the agent may propose these artifacts but must not write them.

Use `SIGNIFICANT_WORK_AND_CHECKPOINTS.md`.
---

## 15. Handoff and replay

When the task remains active, the context window is near limit, or recovery may be needed, create a handoff packet:

- `Project Map/handoffs/HO-xxxx.yaml`

A handoff is optimized for a clean-slate continuation. It should include:

- active task;
- checkpoint;
- current best state;
- must-read refs;
- next safe step;
- completed actions;
- unsafe-to-repeat actions;
- open questions;
- unresolved claims.

See `HANDOFF_TEMPLATE.yaml`.

---

## 16. Side-effect safety

For external actions, file writes, DB changes, deployments, messages, purchases, or destructive operations:

1. Require explicit owner permission and scope.
2. Record the intended action in Working State if the task is long-running.
3. Use an idempotency key where possible.
4. Record a side-effect receipt after completion.
5. On replay/recovery, check receipts before repeating any action.

---

## 17. Response style

A good project answer is:

- grounded;
- scoped;
- intent-correct;
- concise enough to be usable;
- explicit about missing evidence;
- clear about what is fact, inference, or proposal;
- useful for the next action without performing it unless asked.

Avoid long generic explanations when the user asked for a concrete project answer.

---

## Eval-driven review

Use evals when the kit, Project Map, agent instruction files, model, client, or tool permissions change.

The eval-suite should check behavior, not intelligence:

- answer-only default intent;
- no unauthorized mutation;
- missing-evidence handling;
- stale fact suppression;
- source authority conflicts;
- external research boundary;
- side-effect receipts;
- task/handoff replay;
- no whole-project over-retrieval.

Eval results should be stored in `Project Map/eval_runs/`. Failure traces should be short and should not include secrets or hidden reasoning.

A failed eval should usually result in one of four repairs:

1. clarify a root instruction file;
2. fix Project Map source authority or retrieval policy;
3. adjust a memory card lifecycle state;
4. add a more specific eval case so the failure remains visible.

Manual owner review remains valid. Evals are regression alarms, not proof of correctness.

See `EVAL_AUTOMATION_AND_TRIGGER_POLICY.md` for automation levels and trigger policy.



---

## Cursor integration and command vocabulary

When using Cursor, prefer explicit commands or mode blocks over vague natural language.

Recommended commands:

- `/answer` — answer only;
- `/analyze` — analyze only;
- `/plan` — produce a scoped task;
- `/apply` — perform one scoped change;
- `/checkpoint` — propose a checkpoint;
- `/handoff` — create a clean-slate handoff;
- `/map-delta` — propose Project Map changes;
- `/map-apply` — apply approved Project Map changes;
- `/recover` — recover from Project Map and Working State;
- `/eval-smoke` — prepare or run behavior checks;
- `/failure-case` — convert a failure into a candidate eval case;
- `/inventory` — read-only source-authority inventory.

See `CURSOR_INTEGRATION_OWNER_GUIDE.md` and `cursor/`.

---

## Platform summary boundary

The agent must not treat platform-generated summaries or compressed chat history as durable project memory, owner approval, or source authority.

If context compaction is suspected, use recover mode and start from Project Map + Working State + Source Authority + approved handoff/checkpoint.

See `PLATFORM_CONTEXT_COMPACTION_BOUNDARY.md`.

---

## v3.8 scope and workspace operating rules

1. The owner should not have to manually edit scope files if an explicit agent workflow can safely update them.
2. The agent may update scope control files only after explicit owner approval or an approved task contract.
3. Updating scope does not authorize product changes by itself.
4. A multi-component project with one Project Map should normally be opened at the shared root workspace.
5. A component-only workspace is allowed only when the task intentionally does not require Project Map or cross-component context.
6. Codex should default to restricted second-agent behavior: review first, mutate only under explicit scope and approval.


## Authoritative workspace rule

If Project Map, `AGENTS.md`, `current_state`, or source authority references an existing workspace file, treat it as primary. Do not replace it with a generated fallback workspace unless the owner explicitly asks.


## Cursor settings rule

For owner-controlled projects, Cursor must not default to `Run Everything`. Prefer Auto-review or stricter mode with protections on, narrow allowlists, visible usage summary, and explicit apply scope for file changes.
