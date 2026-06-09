# Working State and Replay Guide

Status: portable integration guide  
Purpose: define Working State as the compact replay root for continuing or recovering long-running project work.

---

## 1. Definition

Working State is not long-term memory.

Working State is compact control state that lets an agent resume or recover work without rereading the whole chat or project.

It stores references, cursors, obligations, blockers, checkpoints, and safety receipts. It should not store large payloads.

---

## 2. Recommended file

```text
Project Map/working_state.yaml
```

---

## 3. Minimal schema

```yaml
schema_version: 3.3.0
project_id: example-project
active_workstream: WS-0001
active_task: TASK-0003
profile: resume
branch: main
checkpoint:
  id: CKPT-0007
  created_at: "2026-06-08T12:00:00Z"
  compatible_with_schema: "3.3.0"
  summary: "Short checkpoint summary."

cursor:
  current_step: "Implement route contract draft"
  next_step: "Owner review"
  last_completed_step: "Read source authority and active workstream"

mandatory_refs:
  memory: [DEC-0001, FACT-0002, CON-0001]
  files: []
  raw_sources: []

obligations:
  - id: OBL-0001
    text: "Do not edit repo files; provide Cursor task only."
    source_ref: DEC-0001
    status: active

blockers:
  - id: BLK-0001
    text: "Owner has not approved apply mode."
    status: active

pending_actions:
  - id: ACT-0001
    type: owner_review
    status: pending
    idempotency_key: null

side_effect_guard:
  required: true
  receipts_to_check: [SE-0001]

notes:
  compact: "Keep this file short. Put detail in workstream or memory cards."
```

---

## 4. Replay algorithm

When resuming:

1. Load `working_state.yaml`.
2. Check schema compatibility.
3. Load active workstream.
4. Load mandatory refs.
5. Check side-effect receipts.
6. Hydrate additional context using `resume` profile only if needed.
7. Continue from `cursor.next_step`.
8. Update Working State or propose a delta at the end.

---

## 5. Recovery algorithm

When state is incomplete or inconsistent:

1. Switch to `recover` retrieval profile.
2. Load the latest checkpoint and workstream history.
3. Load side-effect receipts before repeating any action.
4. Load raw sources only when reconstruction requires them.
5. Mark uncertain reconstruction as inference.
6. Create a new checkpoint after owner confirmation or safe reconstruction.

---

## 6. Branch and fork rules

Each branch should have:

- branch ID;
- parent checkpoint;
- allowed shared memory;
- branch-local memory;
- merge decision if accepted.

A branch must not read future facts or decisions from another branch unless the owner explicitly merges them.

---

## 7. Side-effect receipts

Use receipts for actions that should not be repeated accidentally.

Examples:

- file write;
- database write;
- email/message sent;
- deployment;
- payment/purchase;
- external ticket creation;
- destructive command.

Receipt example:

```yaml
id: SE-0001
type: file_write
status: completed
idempotency_key: "write:docs/WORKLOG.md:2026-06-08T12:00Z"
performed_at: "2026-06-08T12:03:00Z"
scope: "docs/WORKLOG.md"
summary: "Updated worklog entry for TASK-0003."
evidence_ref: "tool_output:apply_patch:123"
```

---

## 8. What not to put in Working State

Do not put:

- full transcripts;
- long raw logs;
- large file contents;
- complete research reports;
- duplicated memory card bodies;
- secrets;
- unrelated historical notes.

Store refs instead.


---

## 10. Task contract and handoff integration

Working State should reference, not duplicate, long-task artifacts:

```yaml
active_task_ref: "Project Map/tasks/TASK-0001.yaml"
latest_handoff_ref: "Project Map/handoffs/HO-0001.yaml"
claim_ledger_ref: "Project Map/claim_ledger.yaml"
permissions_policy_ref: "Project Map/permissions_policy.yaml"
source_authority_ref: "Project Map/source_authority.yaml"
retrieval_policy_ref: "Project Map/retrieval_policy.yaml"
```

On resume, load these refs before semantic memory expansion.

On recovery, check handoff and side-effect receipts before continuing.

---

## 11. Intent-safe replay

Replay must not execute pending actions automatically.

Replay restores context and identifies the next safe step. If the next step is mutating, it requires current explicit apply intent and scope from the owner.


---

## Replay after platform compaction

If the host platform may have summarized or truncated the chat, Working State becomes the replay root.

The agent must not use platform summary as project truth. It should load the latest compatible Working State checkpoint, current Project Map state, Source Authority, active task/checkpoint/handoff, and only policy-allowed memory units.

If this is not enough to continue safely, the correct answer is `missing evidence`, not reconstruction from chat recall.
