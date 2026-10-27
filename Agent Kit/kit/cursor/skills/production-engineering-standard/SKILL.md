---
name: production-engineering-standard
description: Mandatory production-engineering standard for any task that analyzes, designs, writes, modifies, reviews, debugs, optimizes, tests, migrates or documents code, business logic, schemas, APIs, caches, jobs, integrations or runtime behavior in the adopting project.
---

# Production engineering standard

Deliver the owner's complete outcome with the smallest coherent change.
Quality is established by behavior and evidence, not labels or metrics.
Apply this standard before technical decisions and through final review.

## 1. Preserve meaning and authority

The owner defines required behavior. Current production code establishes
existing behavior and integration constraints to preserve unless changed
by the owner. Tests, documentation and agent reports are evidence, not
permission or product specifications.

Do not invent business rules, defaults, fallbacks, component responsibilities,
state transitions, schedules, retries, caching, persistence, deletion,
data precedence, UI/trading behavior or compatibility/public contracts.

Resolve material product ambiguity with the owner before dependent edits;
continue independent authorized work. Choose internal implementation details
autonomously only when they preserve the same observable semantics.
A necessary causal file expansion is allowed; semantic expansion is not.

## 2. Establish the real affected behavior

Before editing, identify:
- the requested delta and existing behavior that must remain;
- producer -> calculation -> state/storage -> transport/cache -> consumer
  -> owner-visible result;
- affected callers, shared state and lifecycle entry points;
- acceptance criteria, preserved invariants and required evidence layers.

Read the smallest complete dependency neighborhood. Do not omit working
consumers or expand into unrelated repository inspection.

Before relying on a dependency, verify the relevant version's actual contract:
inputs, result/error meaning, side effects, state after success and failure,
ownership and completion guarantees. Names, examples, language analogies
and test doubles are insufficient.

Trace initial state -> call -> resulting state -> consumer decision -> next
action, including failure cleanup. Check relevant built-in capabilities
before adding wrappers. Follow generated code and packaging when they alter
the delivered contract.

For callbacks, queues and deferred work, establish both safety and progress
from initial state through completion. An accepted request is not completion;
a duplicate-work guard does not prove progress.

## 3. Implement only the necessary change

Every changed production symbol must serve an owner acceptance criterion
or preserve an identified invariant. Remove unexplained changes or obtain
the required owner decision.

Preserve unrelated work. Avoid speculative features, broad cleanup,
unnecessary abstractions, frameworks, dependencies and parallel implementations.
Choose the simplest maintainable implementation with the least unnecessary
state, I/O, allocation, locking and repeated work.

Make domain meaning, component boundaries, state ownership, units,
time zones, valid states and error/empty-data semantics explicit.
Reuse correct project primitives and one authoritative implementation
of each business rule.

Explain the purpose and material constraints of new or materially changed
code locally; avoid obvious-syntax comments and boilerplate. Give changed
Python functions accurate input/return types and parameterized collections.
Preserve supported language, framework, ABI and serialization contracts;
do not silence errors with unchecked casts, fake defaults or broad suppression.

## 4. Preserve failure, lifecycle and resource behavior

Review relevant missing, malformed, stale, duplicate, reordered, concurrent
and partial states, including restart, cancellation and version mismatch.
Check fallbacks against the actual deployed producer, not only the new one.

Each handler needs a defined responsibility and outcome. Preserve the original
failure, cancellation and partial state. Release owned resources on every
applicable exit; do not release borrowed or transferred resources.
Verify cleanup and transaction semantics instead of applying templates.

Inspect changed hot paths and repeated operations for avoidable work.
Do not introduce cache, retry, asynchronous completion or recovery semantics
unless they match the owner-authorized behavior.

## 5. Use independent behavioral evidence

Derive expected results from owner requirements, verified preserved behavior
or authoritative platform contracts, never from the new implementation.

Prefer existing production-linked checks. Add a test only for a named criterion
or distinct regression that existing checks cannot establish, with an
independent oracle. Do not copy the implementation into the test, weaken
assertions, remove regressions or mock away the boundary being claimed.

Verify that doubles reproduce the dependency's relevant states and failures.
When practical and authorized, show that a regression check rejects the faulty
version and accepts the correction. For a critical new guard, an isolated
bypass can establish sensitivity. Do not create a broad mutation campaign
without a task need.

Challenge assumptions shared by implementation and tests. Green tests,
coverage percentages and successful compilation do not override a semantic
defect or establish target-runtime behavior.

## 6. Verify the deliverable and report its limits

Review the complete diff against the requested delta and preserved invariants,
including callers, failures, lifecycle, concurrency and resource costs.
Obtain useful authorized executable feedback before combining further slices.

Map every acceptance criterion and affected preserved invariant to its check
and required evidence layer, or an explicit verification gap.
Check transformed/generated deliverables when relevant. Reuse unaffected
evidence; do not rerun unrelated checks.

Keep source review, tests, build, publication, deployment, native runtime
and owner acceptance distinct. Neither hashes nor self-declared review flags
replace behavioral evidence. Follow existing project verification and
candidate-state rules; this skill grants no extra execution authority.

Do not declare the requested outcome complete while necessary work,
material ambiguity or required evidence remains unresolved.
Report the actual change, preserved behavior, affected files/symbols,
reason for the chosen implementation, checks performed and exact remaining
limitations. Never imply an execution or acceptance that did not occur.

## Required references

Read applicable sections before the decision or action they govern.
These references retain mandatory rules; moving a rule out of this file
does not make it optional. Reuse already-read guidance while it remains current.

- Dependency use, shared state, integration, lifecycle or failure-path work:
  [Contracts and lifecycle](references/contracts-and-lifecycle.md).
- Writing/reviewing code, comments, types, idioms or error/resource handling:
  [Code quality](references/code-quality.md).
- Changed hot paths, repeated work, I/O, caching or resource lifetime:
  [Performance and resources](references/performance-and-resources.md).
- Selecting, writing or interpreting tests and verification evidence:
  [Testing and verification](references/testing-and-verification.md).
- Competing root-cause hypotheses or useful invariant-based tests:
  [Diagnosis and properties](references/diagnosis-and-properties.md).
- Project language versions and local checks:
  [Project toolchains](references/project-toolchains.md).
- Before final engineering conclusions:
  [Engineering review checklist](references/engineering-review-checklist.md).

For MQL initialization, timers, chart events, deferred work, shutdown or bridge
completion, load $mql-event-lifecycle before design/edits and retain it for review.
Pure calculations, text edits and unchanged compilation alone do not trigger it.
