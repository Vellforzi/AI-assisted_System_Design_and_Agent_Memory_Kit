---
name: mql-event-lifecycle
description: Design, change, debug or review MQL4/MQL5 event-driven behavior across initialization, timers, chart events, deferred work and shutdown, including a bridge that supplies those callbacks. Trace readiness, queue ownership and progress before relying on function-level correctness. Not needed for compile-only work, text-only edits or pure calculations with no affected event or resource lifecycle.
---

# MQL event lifecycle

Apply $production-engineering-standard throughout. This skill adds temporal
checks, not product semantics or terminal permissions. Correct calculations
and individual handlers do not establish a correct event protocol.

## 1. Establish the execution contract

Identify platform, EA/indicator, terminal build when known, current/other chart,
bridge and shared state. Read applicable
[platform contracts](references/platform-contracts.md); verify material API
assumptions against official sources and actual wrappers. Do not transfer
timing/completion guarantees between platforms.

Name functions and fields along the smallest complete producer -> dispatch ->
consumer route, including initialization, early returns, cancellation and
shutdown. For DLL/imported work, establish blocking versus external completion
and its return route to MQL; names do not establish behavior.

## 2. Trace reachable states before editing

For each affected transition, use existing notes or a compact table without
a new mandatory framework:

`entry/event -> preconditions -> state before -> call/result -> state after
-> next executor -> owner-visible outcome`

Trace construction/OnInit through first useful completion, including callbacks
before data, groups, bindings or chart resources are ready. OnInit success or
an object pointer does not prove readiness. For each early return, identify
who supplies the prerequisite and subsequently starts work; a guard must not
make required work unreachable.

Distinguish readiness, requested/dirty work, accepted-but-unconsumed events,
executing portions, data/view revision, event ownership, completion,
cancellation and terminal failure. Use the smallest existing representation;
add independent state only when reachable states require independent values;
never add fields, enums or a scheduler merely to match this list. Correct a
resource's readiness invalidation where sufficient; do not couple it to
unrelated source data.

## 3. Establish safety and progress

Safety means obsolete/wrong-instance work cannot mutate current state,
accepted source data remains intact, and the task-defined pending-continuation
limit is respected. One pending continuation is not a universal requirement.

Progress means accepted finite work can reach completion or its specified
failure/cancellation outcome, assuming prerequisites arrive, events continue
and relevant inputs settle. State these assumptions; endless cancellation
does not promise completion, and an invented timeout cannot establish it.

For every pending/busy/wait state identify:

- exact request/event and producer; complete consumer route, filters and early
  returns; enqueue success is not acknowledgement;
- ownership release/transfer on consumption, failure and cancellation;
  validate event identity before changing current ownership;
- reachable next executor, unblocked by the flag, handler or resource whose
  completion it supplies;
- progress measure, such as cursor/remaining work; routine timers/probes must
  not continually reset it or postpone its turn.

Inspect all queues/execution contexts: serialized program callbacks do not
serialize GUI, other programs or asynchronous bridge work. Never wait inside
a callback for another callback of that program. Sleep, faster timers and busy
loops cannot replace a missing completion dependency.

Timer cadence does not guarantee deliveries. Bound callback work, preserve
settings/UI priority, and inspect hot-path scans, chart reads, verification
requests, queue pressure and logging. Failed enqueue or a stationary cursor
alone does not prove queue overflow.

## 4. Preserve lifecycle and failure meaning

Separate ticket, instance and revision. Establish whether a ticket serves the
latest view or a captured revision from owner requirements/current behavior;
do not invent latest-wins. A view change must not forget a queued event, nor
may an old event clear a newer event's pending state.

Trace affected reinitialization, period changes, clear/remove and shutdown.
Cancel/invalidate owned continuations before releasing accessible resources.
Separate reusable source data from chart bindings; verify storage lifetime and
deinitialization reason instead of assuming wholesale retention or reset.

Distinguish enqueue failure, execution failure, property mismatch and
unfinished rendering; preserve the required outcome. Normal continuation,
permitted independent scheduled work, new owner action and failure retry are
different. Preserve periodic work after success; repetition alone is not a
defect. A timer tick alone does not create a new operation after failure.
When recovery/retry is forbidden, later Timer/ChartEvent paths must not restart
failed work. No automatic retry, forced flag reset or timeout recovery without
matching owner authority.

## 5. Verify and report

Before selecting or interpreting checks, read
[temporal verification](references/temporal-verification.md).
Its sequence coverage, diagnostics and evidence rules remain mandatory.
Verify both forbidden effects and progress, including normal completion.

Models/translated tests prove modeled transitions; compilation proves
syntax/linkage. Actual queues, object completion and chart behavior require
authorized native/runtime evidence; otherwise name the exact gap.
Terminal launch/close/restart, charts, settings and attach/remove remain
owner-controlled unless explicitly delegated. Read-only observation adds no
control authority; agent runtime evidence is not owner acceptance.

Apply $complete-technical-communication. Report the causal sequence, minimal
change, checked safety/progress and runtime gap. Checkboxes or valid skill
files do not prove the protocol works.
