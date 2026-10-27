# RECOVERY_CAPSULE — $TASK_NAME

```yaml
schema: RECOVERY_CAPSULE_V1
revision: 1
updated_utc: $UPDATED_UTC
phase: $PHASE
status: $STATUS
last_receipt_seq: 1
capsule_max_bytes: $CAPSULE_MAX_BYTES
task_identity_locked: true
causal_proof_required: true
workflow_contract_version: 2
owner_outcome_sha256: $OWNER_OUTCOME_SHA256
acceptance_matrix: $ACCEPTANCE_MATRIX
acceptance_row_ids: [$ACCEPTANCE_ROW_IDS]
active_slice: $ACTIVE_SLICE
last_owner_evidence: $LAST_OWNER_EVIDENCE
inventory_state: WORKING_INVENTORY
inventory_generation: 1
inventory_unresolved_paths: [INITIAL_CAUSAL_MAPPING]
inventory_final_sweep: NOT_RUN
progress_total_rows: $PROGRESS_TOTAL_ROWS
progress_source_implemented: 0
progress_executable_proven: $PROGRESS_EXECUTABLE_PROVEN
progress_runtime_accepted: $PROGRESS_RUNTIME_ACCEPTED
progress_remaining_rows: $PROGRESS_REMAINING_ROWS
active_worker_present: false
active_worker_scope: NONE
active_worker_stopping_condition: NONE
evidence_layer: NONE
source_checks_complete: false
cumulative_regression: NOT_RUN
```

## Authority

1. Current user request.
2. Applicable system/developer instructions and nearest `AGENTS.md`.
3. This capsule and the latest consistent `IMPLEMENTATION_RECEIPTS.jsonl` records.
4. Authoritative plans, current source, and fresh verification evidence.

Conversation summaries, old PASS labels, and memory are hints rather than current proof.

## Immutable owner outcome

$GOAL

## Definition of done

$DONE_ITEMS

## Acceptance matrix and evidence

The row IDs below are the non-shrinking task scope. Their local/runtime status
and evidence kind come from the authoritative matrix; a correction or active
slice may update evidence but cannot silently remove a row.

The same matrix must contain a matching `## Causal proof` row for every ID,
recording the task-specific producer-to-consumer gate path, production
establishment, required order/reset coverage, and anti-vacuity status.

| ID | Local status | Runtime status | Evidence kind |
|---|---|---|---|
$MATRIX_STATE_ROWS

## Active semantic slice

`$ACTIVE_SLICE`

This is the next bounded work priority. It is non-closing and never replaces
the immutable owner outcome or any acceptance row.

## Inventory and incremental progress

- Inventory remains `WORKING_INVENTORY` until every causal path and proof route
  is mapped and one final bounded read-only sweep returns no new gap.
- `INVENTORY_COMPLETE` requires an empty `inventory_unresolved_paths` list and
  `inventory_final_sweep: PASS`.
- Progress counters measure incorporated evidence, never worker waiting or
  review activity.
- Each causal increment records source checks and cumulative regression before
  the next increment begins.

## Scope and current state

- Repository/workspace root: `$REPO_ROOT`
- Task directory: `$TASK_DIR`
- Observed HEAD: `$HEAD`
- Observed branch: `$BRANCH`
- Sole writer: `$WRITER`
- Current write-set: `TO_BE_DEFINED_BEFORE_PRODUCT_WRITES`
- Protected inherited/user delta: `NONE_RECORDED`

Authoritative plans:

$PLAN_ITEMS

## Latest owner evidence

`$LAST_OWNER_EVIDENCE`

Initialization records no owner runtime evidence. Any later owner smoke failure
must mark the affected row `FAILED` and reopen both that row and the task.

## Evidence boundary

- Initialization proves only that recovery state was created.
- No implementation, test, build, deployment, runtime, or acceptance claim is implied.
- Promote `status` only for the exact scope and postimage supported by current evidence.
- Source shape, compilation, deployment, or a finished active slice cannot close
  an unproven behavioral row.
- A pre-seeded prerequisite or downstream-only seam is unit evidence, not proof
  that production established the prerequisite. Missing or incomplete causal
  proof keeps the row and task open.
- Local matrix cells use only `UNPROVEN`, `PROVEN_EXECUTABLE`,
  `PROVEN_JUSTIFIED_SEAM`, or `NOT_REQUIRED`; task/capsule labels do not belong
  in those cells. Any closing task status requires a final successful
  `recovery_tool.py validate` result with the matching closure-allowed field.

## Exact next action

$NEXT_ACTION

## Status vocabulary

- `TASK_OPEN`
- `OWNER_SMOKE_FAIL_REOPENED`
- `SLICE_FIXED_TASK_OPEN`
- `NOT_STARTED`
- `DESIGN_VERIFIED`
- `CODED_UNVERIFIED`
- `TARGETED_VERIFIED`
- `FULL_VERIFIED`
- `DEPLOYED_UNACCEPTED`
- `LOCAL_VERIFIED_AWAITING_OWNER_SMOKE`
- `LOCAL_MATRIX_VERIFIED_AWAITING_OWNER_SMOKE`
- `RUNTIME_ACCEPTED`

Do not use bare `PASS`, `COMPLETE`, `READY`, or `VERIFIED` without exact scope and evidence.

## NORMAL_RECOVERY

1. Read the current user instruction, nearest `AGENTS.md`, and this capsule.
2. Run the bounded recovery snapshot helper.
3. Read only the latest three receipts.
4. Confirm that HEAD/path drift is explained and overlapping files still have one writer.
5. Restore the immutable owner outcome/hash, every row ID with local/runtime
   status, evidence kind, and causal-proof state, phase/status, the non-closing
   active slice, write-set, latest owner evidence, and exact next action.
6. Read only the source hunks, tests, and plan sections required by the active slice.
7. Continue from the exact next action; do not repeat a full audit.

If the latest receipt sequence exceeds `last_receipt_seq`, use `GLOBAL_RECOVERY` before accepting it.

## GLOBAL_RECOVERY

Use only for missing/malformed/oversized state, receipt sequence mismatch, unexplained HEAD/path drift, overlapping writers, contradiction, or ambiguous scope/next action.

1. Freeze writes and capture one bounded snapshot.
2. Re-read the current user request and applicable `AGENTS.md` chain.
3. Reconcile this capsule, latest receipts, name-only/numstat evidence, and only implicated plan/source sections.
4. Preserve unrelated user changes and distinguish inherited delta from current-agent delta.
5. Confirm that the owner-outcome hash and receipt-anchored row IDs did not
   change; an active slice or compaction summary is never authority for either.
   Reconcile causal-proof rows one-for-one with those same row IDs.
6. Append one reconciliation receipt, then replace this capsule coherently.
7. Continue only after identity, scope, writer, evidence boundary, and next
   action agree.

## Update rule

At a stable semantic boundary, append one compact receipt containing the same
`owner_outcome_sha256` and complete `acceptance_row_ids`, then replace this
capsule coherently and advance `last_receipt_seq`. A failed owner smoke first
reopens its row and the task; it can never coexist with a closing status. Do not
append diary history, source, diff bodies, or logs. A sequence, outcome-hash, or
row-anchor mismatch intentionally forces `GLOBAL_RECOVERY`.
