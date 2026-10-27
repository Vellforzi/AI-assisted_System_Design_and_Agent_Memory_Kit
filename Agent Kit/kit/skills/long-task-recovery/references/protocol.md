# Locked-task recovery protocol

This reference applies only after locked/strict mode has been selected.
For ordinary continuity, including behavioral work, use ../SKILL.md; no locked
matrix, outcome hash, bind or closure validator is required.
The init command below creates locked state and is not the ordinary entrypoint.

## 1. Purpose and activation

This protocol preserves only the semantic state needed to continue a long task safely after context compaction, restart, or handoff. It is not a substitute for source, tests, or runtime evidence.

Select this locked protocol only for an explicitly selected strict task or a
substantive outcome-driven-task-closure escalation. Duration, multiple phases,
compaction or expected handoff alone select ordinary continuity, not this mode.

## 2. Authority and location

Precedence remains:

1. current user request;
2. applicable system/developer instructions and nearest `AGENTS.md`;
3. current task-local capsule and consistent receipts;
4. authoritative plan and current source/evidence.

Conversation summaries and memory are navigation hints, not proof of completed work.

Use the repository's established task directory. If there is none, use `.codex/tasks/<task-slug>/` within the repository. Keep recovery files beside the task plan when practical. Do not invent an external control directory or modify repository-wide instructions merely to initialize one task.

## 3. Artifacts

### `RECOVERY_CAPSULE.md`

One current snapshot, normally 4–8 KiB and never above 12 KiB unless the user explicitly changes the limit. It contains:

- immutable owner outcome plus a receipt-anchored SHA-256;
- complete acceptance-row IDs and their local/runtime status and evidence kind;
- matching task-specific causal proof for each behavioral row: gate path,
  production establishment, required order/reset coverage, and anti-vacuity;
- current phase and honest task status;
- workflow contract version, inventory lifecycle, numeric progress, evidence
  layer, source-check state, and cumulative-regression state;
- active semantic slice, explicitly non-closing, and sole writer;
- active worker presence, exact scope, and stopping condition;
- current write-set and protected pre-existing changes;
- latest owner evidence, last valid local evidence, and explicit unverified boundary;
- exact next action;
- task-specific `NORMAL_RECOVERY` and `GLOBAL_RECOVERY`.

Do not append a diary or old snapshots. Replace stale fields coherently.

### `IMPLEMENTATION_RECEIPTS.jsonl`

Append-only, one compact JSON object per stable boundary. Required fields:

- `schema`, `seq`, `recorded_utc`, `kind`;
- exact `scope` and scoped `status`;
- unchanged `owner_outcome_sha256` and complete `acceptance_row_ids`;
- concise verification evidence and limitations of the claim;
- `next` action.

Store paths, exit codes, counts, and artifact references. Do not copy full source, diffs, logs, or entire plans. Hash only a protected preimage, unexplained drift, or an irreversible/final boundary; do not repeat a full hash manifest at every checkpoint.

## 4. Initialization

Before `init`, decide:

- task name and concrete goal;
- definition of done;
- an acceptance matrix with a machine-readable four-column `## Closure state`
  table (`ID`, local status, runtime status, evidence kind) and a matching
  five-column `## Causal proof` table (`ID`, gate path, production
  establishment, order/reset coverage, anti-vacuity);
- authoritative plan paths;
- current phase and honest status;
- active slice and sole writer;
- exact next action.

New initialization uses workflow contract v2. Start with
`inventory_state: WORKING_INVENTORY`, a non-empty unresolved-path list,
`inventory_final_sweep: NOT_RUN`, numeric progress consistent with the matrix,
no active worker, and no source/executable/runtime claim.

Run `recovery_tool.py init` with an explicit repository root and task directory. The command is create-only. If state already exists, run `validate` and recover it instead of overwriting it.

Initialization records no implementation success. Default task status is
`TASK_OPEN`; every matrix row begins with the evidence state recorded in the
provided matrix.

## 5. Checkpoint protocol

Checkpoint only at a stable semantic boundary: completed causal increment,
verified postimage, phase transition, owner gate, reconciled drift, or
pause/handoff. Worker waiting, intermediate review messages, and individual
findings from one unfinished read-only sweep are not checkpoint boundaries.

1. Reconcile the actual changed paths and verification result.
2. Update numeric progress, inventory lifecycle, evidence layer, source checks,
   cumulative regression, and active-worker fields from actual evidence.
3. Preserve the owner-outcome hash and every receipt-anchored row ID. Update
   evidence/status and causal-proof state only for rows actually affected by
   the new evidence.
4. If owner smoke failed, mark the affected runtime row `FAILED` and set the
   task to `TASK_OPEN`/`OWNER_SMOKE_FAIL_REOPENED` before any other claim.
5. Append one receipt with the next sequence number.
6. Replace the capsule coherently and set `last_receipt_seq` to that number.
7. Run `validate`; optionally run `snapshot` when Git/path drift matters.

One checkpoint per meaningful slice is enough. Do not checkpoint after every file or tool call.

## 6. NORMAL_RECOVERY

Use after ordinary compaction, restart, or handoff when state appears consistent.

1. Read the current user instruction, nearest `AGENTS.md`, and `RECOVERY_CAPSULE.md`.
2. Run the bounded `snapshot` helper.
3. Read only the latest three receipts.
4. Confirm that HEAD/path drift is explained and that one writer owns overlapping files.
5. Restore the immutable owner outcome/hash, all matrix row IDs and statuses,
   their causal-proof state, phase/task status, non-closing active slice,
   write-set, latest owner evidence, and exact next action.
6. Confirm that the active slice is only a work priority and did not replace the
   owner outcome or acceptance matrix.
7. Read only the source hunks, tests, and plan sections required by that slice.
8. Continue from the exact next action.

Do not reread all plans, all source, the full diff, or a historical inventory merely because compaction occurred.

## 7. GLOBAL_RECOVERY

Trigger only when:

- capsule or receipts are missing, malformed, contradictory, or oversized;
- receipt sequence and `last_receipt_seq` disagree;
- HEAD or changed paths drift without explanation;
- more than one writer may have touched overlapping files;
- the active slice, permissions, or next action cannot be determined safely.
- the owner-outcome hash or acceptance-row receipt anchor changed without a new
  explicit owner task identity.

Procedure:

1. Freeze writes and capture one bounded snapshot.
2. Re-read the current user request and applicable `AGENTS.md` chain.
3. Reconcile capsule, latest receipts, name-only/numstat evidence, and only the implicated plan/source sections.
4. Preserve unrelated user changes and distinguish inherited delta from current-agent delta.
5. Re-establish the immutable owner-outcome hash and full row set from the last
   consistent owner-authorized anchor; never infer a narrowed task from an
   active slice or compaction summary.
6. Append one reconciliation receipt.
7. Replace the capsule with one coherent snapshot.
8. Continue only when identity, scope, writer, evidence boundary, and next
   action agree.

Do not turn `GLOBAL_RECOVERY` into a default full repository audit.

## 8. Status vocabulary

There are two separate vocabularies. Capsule `phase`/`status` uses honest
scoped task states:

- `TASK_OPEN` — the complete matrix is not closed;
- `OWNER_SMOKE_FAIL_REOPENED` — owner runtime evidence invalidated an earlier
  local closing claim and reopened the row/task;
- `SLICE_FIXED_TASK_OPEN` — one active slice is fixed, but other matrix rows
  remain failed or unproven;
- `NOT_STARTED` — initialized, no implementation claim;
- `DESIGN_VERIFIED` — design/source mapping checked, no code claim;
- `CODED_UNVERIFIED` — code exists but the current postimage lacks required checks;
- `TARGETED_VERIFIED` — named targeted checks passed for the exact scope/postimage;
- `FULL_VERIFIED` — the full required local pipeline passed for the exact postimage;
- `DEPLOYED_UNACCEPTED` — verified artifacts deployed, runtime not accepted;
- `LOCAL_VERIFIED_AWAITING_OWNER_SMOKE` — every required local behavioral row
  has production-path or justified-seam evidence, but runtime remains open;
- `LOCAL_MATRIX_VERIFIED_AWAITING_OWNER_SMOKE` — same gate, explicitly naming
  full-matrix local closure;
- `RUNTIME_ACCEPTED` — the authorized runtime/owner acceptance gate passed.

The `## Closure state` local-status column uses exactly:

- `UNPROVEN` — the row remains open;
- `PROVEN_EXECUTABLE` — an executed production path proves the row;
- `PROVEN_JUSTIFIED_SEAM` — a justified seam plus production establishment and
  anti-vacuity proves the row;
- `NOT_REQUIRED` — the row genuinely has no local proof requirement.

Never put `FULL_VERIFIED`, `LOCAL_VERIFIED_AWAITING_OWNER_SMOKE`, `PASS`,
`COMPLETE`, `PRODUCTION_EXECUTED`, or another task/causal label in that column.
Before a closing task status, run the deterministic `validate` command against
the final state and require exit code 0, `ok=true`, and the appropriate
closure-allowed field. If it fails, keep an open status and follow the first
actionable issue rather than guessing a token.

Avoid bare `PASS`, `COMPLETE`, `READY`, or `VERIFIED` without exact scope and evidence. A worker report is evidence, not final proof.

Source shape, token/regex checks, compilation, build, or deployment do not by
themselves prove a behavioral matrix row. A row may close locally only through
an executed production path or an explicitly justified seam. Any runtime
`FAILED` row forces an open task status regardless of earlier local evidence.

A seam that preloads a prerequisite which production must establish is
`PRECONDITION_INJECTED`; a test that bypasses the producer and calls only the
consumer is `DOWNSTREAM_ONLY`. Both remain non-closing. Local closure also
requires the task-specific producer-to-consumer gate path, all materially
different required arrival/reset orders, and an anti-vacuity oracle where a
seam could otherwise stay green after its producer is removed or delayed.

## 9. Slice and context budgets

Prefer one semantic owner, one observable behavior, one oracle, and a small
write-set per slice. The slice limits work-in-progress, never task identity.
Coupled changes may be larger when splitting would violate the invariant;
record that reason rather than creating overlapping writers.

For workflow contract v2, every source-implemented increment must record
completed source checks before using a source-verified phase, and every later
increment must record cumulative regression as `PASS` or `NOT_REQUIRED` before
advancing. A present worker requires both a bounded scope and a stopping
condition. Waiting for it does not change progress counters.

Default limits:

- capsule: 12,288 bytes;
- changed paths in snapshot: 80;
- snapshot output: 16,384 bytes;
- receipts read during normal recovery: latest three.

Never emit full diff bodies or logs from the snapshot helper. Save detailed logs to files only when the task already authorizes them, then bring concise errors and receipt references into context.

## 10. Permission boundary

Recovery state does not broaden authority. Read-only requests remain read-only unless the user authorizes task-local recovery writes. Git, deployment, external systems, credentials, runtime smoke, and acceptance remain separate gates. When artifact creation itself is outside the granted scope, explain the recommended task-local files and ask before persisting them.
