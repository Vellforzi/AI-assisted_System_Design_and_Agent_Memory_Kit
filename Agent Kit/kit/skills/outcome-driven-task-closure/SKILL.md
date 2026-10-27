---
name: outcome-driven-task-closure
description: Strict forensic/full-product-proof escalation for locked or explicitly escalated behavioral work. Do not use as the default for ordinary multi-file or multi-component tasks.
---

# Outcome-driven task closure

Strict forensic/full-product-proof escalation; ordinary coupled programming
uses $bounded-coupled-task. File, language or component count alone is no trigger.

Activate only for:
- explicit owner request for full-product proof;
- two failed bounded repair slices on the same causal surface;
- safety or state-machine correctness that cannot be localized;
- executable evidence of an unresolved cross-system invariant;
- runtime regression recurring after a green local postimage;
- required forensic reconstruction across restart/handoff.

The owner outcome and complete acceptance rows define task identity.
Causes, patches, traces, slices and worker reports cannot replace or shrink it
without an explicit owner change. Apply Workflow V2 controls only where current
project/task policy enforces them; historical advice creates no permission gate.

Apply $production-engineering-standard and its applicable references for
engineering and verification; $complete-technical-communication for reporting.
Keep evidence layers distinct. Resolve skills through the active catalog;
report unavailable required guidance instead of claiming it was applied.

## Frame and discover

Before coupled production edits, record outcome, protected behavior,
authorization and required owner runtime acceptance. Map each representative
scenario's preconditions/order, action, expected result, forbidden effects
and proof route. Trace actual entry points, state owners/writers,
transport/persistence, readers, callbacks/timers, reset/stale/error paths,
lifecycle boundaries and validation.

Remain in `WORKING_INVENTORY` while any row, causal edge, owner, write-set
member or proof route is unresolved. `INVENTORY_COMPLETE` requires every row
mapped, empty `unresolved_paths` and a final bounded read-only sweep without
new gaps. A relevant omission reopens inventory: freeze overlapping writes,
reconcile the path/dependents and extend inventory before further overlapping edits.
Do not call partial passes complete, append one-off symptom patches or pursue unrelated defects.

Prove every controlling state's producer -> transport/persistence -> consumer,
including reset/stale behavior and materially different arrival orders.
For event joins, A -> B does not prove B -> A, duplicate, reattach or restart.
Use [the causal-proof table](assets/CAUSAL_PROOF.template.md) for durable proof.
A required producer outside authorization leaves its row open.

## Implement causal increments

Use one writer for overlapping files. Each invariant-preserving increment needs:
- an observable outcome, acceptance rows and minimal complete causal path/write-set;
- immediate structural, syntax, encoding, diff and readback checks;
- strongest focused authorized executable proof;
- cumulative re-verification of earlier increments sharing affected state,
  transitions, contracts, files or consumers.

Reach the strongest authorized evidence layer before the next increment.
If build, tests, native compile or runtime are forbidden, label
`SOURCE_IMPLEMENTED_NOT_EXECUTED` and keep behavioral rows open.
Use one coherent batch if splitting creates an invalid intermediate state.

## Verify without overclaiming

Prefer production-linked execution. After per-edit checks, run focused
affected-row oracles, available build/test/native compile, one cumulative
locally executable matrix/regression against the final postimage, then required
owner runtime evidence.

Separate product failures from harness/environment failures. Repair an in-scope
harness without weakening assertions; otherwise report the exact blocker.

Tests preloading production-owned state are `PRECONDITION_INJECTED`;
consumer-only tests are `DOWNSTREAM_ONLY`. Neither closes a behavioral row.
A justified seam also requires the real production establishment path,
required order/reset coverage and an anti-vacuity oracle that fails when
the producer is removed or invalidated.

Long-task reports retain `total_rows`, `source_implemented`,
`executable_proven`, `runtime_accepted`, `remaining_rows`, active increment
and each worker's exact scope/stopping condition. Waiting and source reading are not progress.

Locked local row statuses are only `UNPROVEN`, `PROVEN_EXECUTABLE`,
`PROVEN_JUSTIFIED_SEAM` or `NOT_REQUIRED`; they are distinct from task status,
causal tokens, source checks, build and deployment.
Immediately before closing, run the registered recovery validator on final state:
require exit 0, `ok=true` and the matching closure-allowed field.

Interactive runtime smoke, including MT5, is owner-operated unless explicitly
delegated. If all locally executable rows pass but runtime remains, report
`LOCAL_VERIFIED_AWAITING_OWNER_SMOKE` with one compact protocol.
Failed owner smoke reopens the same task and affected rows.

## Delegation

Delegate only for concrete capability or material latency gain; freeze scope,
expected evidence and stopping condition. No automatic successors, duplicate
broad reviews or another analysis worker after the parent knows the root cause.
The parent verifies results and owns the verdict.

## Prompt compiler

For launch, continuation, correction, recovery or handoff prompts, follow
[the prompt contract](assets/TASK_PROMPT.template.md): create
`TASK_PROMPT_SPEC_V1`, run its `roundtrip` and `validate` commands,
and return canonical output unchanged. Never append the workflow manually.
Use `inherited` when the target can read AGENTS.md, skills and task state;
`standalone` only otherwise. Carry task identity/location, owner outcome,
current evidence, optional active slice and authorization.

For compaction/restart/handoff, use $long-task-recovery. Preserve outcome,
matrix/causal state, exact postimage, unresolved evidence, active operation
and next action, not chat history.
