# Contracts, product semantics and lifecycle

Mandatory when the entrypoint routing applies. These details preserve existing
requirements; they do not add authority or a separate workflow.

## 1. Product semantics come first

The owner's business logic defines required behavior.

Current production code defines existing behavior and integration constraints
that must be preserved unless the owner explicitly changes them.

Never invent or silently add:

- business rules;
- defaults;
- fallbacks;
- relationships between components;
- state transitions;
- schedules;
- retry policies;
- cache behavior;
- persistence behavior;
- deletion behavior;
- data precedence;
- user-visible behavior;
- trading behavior;
- compatibility behavior;
- public contracts.

Missing instruction means preserve existing behavior.

If more than one materially different observable behavior is possible, stop
the semantic implementation and ask the owner. Do not resolve product ambiguity
through personal preference, generic best practice, tests or model inference.

Purely internal implementation choices may be made independently only when all
available choices preserve exactly the same observable semantics.

## 2. Understand the causal chain before changing it

Before modifying production logic, identify the affected chain:

- producer;
- normalization or calculation;
- storage or shared state;
- transport or protocol;
- cache;
- consumer;
- owner-visible result.

For the affected chain, inspect as applicable:

- direct callers and consumers;
- ownership of state;
- database schema and row meaning;
- Redis keys, TTL and invalidation;
- schedules and time zones;
- retries, timeouts and cancellation;
- initialization and shutdown;
- reconnect and recovery;
- partial success;
- concurrency and multi-instance behavior;
- ABI, API, protocol and compatibility contracts;
- production fallback paths;
- performance-sensitive paths.

Read the smallest complete dependency neighborhood that establishes this
behavior. Do not scan the whole repository without cause, but do not reduce a
cross-component behavior to only the file where the symptom appears.

For the affected chain, name the existing behaviors that the change could break,
including callers of a shared method and lifecycle entry points. Bind each to a
specific preserved invariant and a check or an explicit verification gap. Trace
new call edges through generated code, packaging and post-build transformations
when those stages can change the executed contract. Unchanged names or successful
source compilation do not establish compatibility of the delivered artifact.

### Verify dependency contracts before relying on them

Before choosing or changing the use of a function, class, language operator,
query or external API, verify each property on which the proposed solution
depends. Use authoritative documentation for the relevant version and inspect
the actual implementation when available. This also applies to new guards and
consumers around existing calls. Names, examples, language analogies and test
doubles do not establish the contract.

Inspect related built-in capabilities that could satisfy the task before
inventing a wrapper or state check. Bound this investigation to relevant
properties: preconditions, return/error meaning, side effects, state after
success or failure, repeated calls, resource ownership, and threading or
completion guarantees. Check special values and their actual comparison rules;
do not assume NULL, an empty value and an invalid identifier are interchangeable.

Trace the real sequence: initial state -> call -> changed state -> consumer
condition -> next action. Verify that the condition handles states the dependency
actually produces, including lifecycle transitions relevant to the defect.
Distinguish wrapper state from the underlying resource and an accepted request
from completed work.

Retain the material assumption, source/version and dependent check or gap in
existing task evidence; a new form or approval gate is not required. Reuse
verified facts while the relevant version and conditions remain unchanged.
Resolve material ambiguity with the smallest decisive authorized check in the
target environment when source evidence is insufficient. If that check is
unavailable, name the unresolved property and do not present dependent behavior
as verified. This requirement grants no additional runtime or external actions.

### Event-driven safety and progress

For work split across callbacks, queues or deferred continuations, establish
both safety (forbidden effects cannot occur) and progress (accepted work can
reach its defined outcome once required prerequisites arrive and relevant
input changes settle). A limit on duplicate work does not prove progress.

Trace from the real initial state through first completion, including callbacks
before resource readiness. For each pending/busy/wait state name its actual
request, producer, reachable next executor, ownership release and failure or
cancellation outcome. Inspect dispatch filters and early returns; an accepted
enqueue is not completion. Check that a waiting handler/flag cannot block its
own completion and routine probes cannot continually reset partial progress.
Keep readiness, queue occupancy and requested work revision semantically distinct.
State external progress assumptions; do not invent retries, timeout recovery,
schedules or product state transitions to make the sequence pass.

For affected MQL4/MQL5 initialization, timers, chart events, deferred work,
shutdown or bridge completion routes, load $mql-event-lifecycle before design
or edits and keep it active for review. Resolve it from the client's skill
catalog; in this checkout its canonical entrypoint is
$mql-event-lifecycle through the active skill catalog. It supplies the platform-specific checks
without changing owner authority. Pure calculations, text edits and unchanged
compilation alone do not require that specialized skill.

## 3. Keep the change minimal but complete

Implement the smallest coherent change that completely satisfies the owner's
requested behavior.

Causal file expansion is allowed when another file must change for the exact
owner outcome. Semantic expansion is forbidden.

Do not add:

- speculative features;
- unrelated cleanup;
- broad refactoring;
- abstractions for hypothetical future use;
- new frameworks;
- new layers;
- new dependencies;
- generic factories or registries without a current requirement;
- duplicate implementations of the same business rule;
- compatibility behavior the owner did not request.

Every changed production symbol must map to:

1. a named owner acceptance criterion; or
2. preservation of a named existing invariant.

If a changed line, branch, field, helper, abstraction, dependency or relationship
cannot be traced to one of those two reasons, remove it or obtain an owner
decision.

## 5. System design standard

For every material design decision, determine:

- component responsibility;
- source of truth;
- state owner;
- data contract;
- consistency model;
- lifecycle;
- concurrency model;
- failure boundary;
- recovery behavior;
- observability;
- compatibility;
- rollout and rollback implications.

Do not create cyclic ownership or hidden coupling.

A component must not assume responsibility for another component's business
rule merely because doing so is locally convenient.

Prefer:

- explicit contracts;
- single ownership;
- idempotent operations where retries are possible;
- deterministic state transitions;
- bounded work;
- fail-closed behavior at trust boundaries;
- fail-explicit behavior when silent continuation would corrupt meaning;
- graceful degradation only when the owner-approved business logic defines it.

Do not introduce eventual consistency, stale fallback, asynchronous completion,
background retry or cache-first behavior without proving that it matches the
required product semantics.

## 7. Reliability

The implementation must work for all defined states, not only the happy path.

Inspect:

- empty input;
- missing data;
- malformed data;
- stale data;
- duplicate events;
- reordered events;
- retries;
- partial writes;
- process restart;
- component restart;
- cache loss;
- network timeout;
- database timeout;
- concurrent instances;
- repeated initialization;
- shutdown during work;
- version skew between producer and consumer.

Fallback behavior must be tested against what the currently deployed producer
or system actually emits, not only against the new producer version.

Do not treat an edge path as irrelevant when it may be the production path
during staggered deployment, missing cache, delayed data or component mismatch.
