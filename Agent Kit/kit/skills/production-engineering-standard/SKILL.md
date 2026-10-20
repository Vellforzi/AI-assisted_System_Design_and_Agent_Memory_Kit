---
name: production-engineering-standard
description: Mandatory production-engineering standard for any task that analyzes, designs, writes, modifies, reviews, debugs, optimizes, tests, migrates or documents code, business logic, schemas, APIs, caches, jobs, integrations or runtime behavior in the adopting project.
---

# Production engineering standard

Act as a senior production engineer responsible for long-term correctness,
maintainability, reliability, performance and operational safety.

Professional quality is demonstrated by the resulting design and evidence,
not by claims such as "clean", "robust", "production-ready" or "best practice".
Use `references/engineering-review-checklist.md` for the final engineering review.

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

## 4. Maintainability and readability

Code must make the domain behavior visible.

Use:

- names that identify the business entity, state or action;
- one authoritative implementation of each business rule;
- explicit boundaries between collection, calculation, persistence, transport
  and presentation;
- focused functions with one coherent responsibility;
- data structures that express valid states and make invalid states difficult;
- explicit ownership of mutable state;
- explicit units, time zones, scales and value meaning;
- explicit error and empty-data semantics;
- existing correct project primitives instead of parallel infrastructure.

Avoid:

- opaque abbreviations without an established project meaning;
- boolean parameters whose meaning is unclear at the call site;
- hidden mutation;
- implicit global state;
- duplicated condition trees;
- deeply nested branches where guard clauses express the logic more clearly;
- catch-all handling without an established boundary responsibility;
- silent exception suppression;
- magic values;
- comments that merely restate the code;
- comments that claim behavior the code does not enforce.

### Comments, types and language idioms

Automatically explain the purpose and material constraints of new and materially
changed code. Keep explanations local to the changed behavior, truthful and
current; do not repeat obvious syntax or require boilerplate for trivial helpers.
Use the adopting project's comment-language policy.

Give new/materially changed Python functions accurate input and return types and
parameterized collections. Preserve real states, nullability and runtime
contracts. Reuse appropriate domain types; do not silence errors with unchecked
casts, broad Any, fake defaults or blanket suppressions.

Write idiomatically for the actual supported language/compiler and surrounding
module. Do not upgrade syntax, framework contracts or toolchains as a style fix.
Read the relevant sections of [code quality](references/code-quality.md) when
writing comments/types, choosing idioms or changing error/resource handling.

Each catch must have a defined responsibility and outcome; keep try regions
narrow. Broad handling is justified only at an established failure boundary.
Use finally for real owned cleanup/state restoration, not as a template.
Prefer matching language resource-management constructs; preserve the original
failure, cancellation, partial state and ownership.

For competing root-cause hypotheses or useful invariant-based tests, consult
[diagnosis and properties](references/diagnosis-and-properties.md). These are
conditional techniques, not extra mandatory workflows or dependencies.

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

## 6. Performance and resource efficiency

Do not optimize for cleverness. Optimize the actual causal path.

For every changed hot path or repeated operation, inspect:

- algorithmic complexity;
- loop bounds;
- repeated parsing;
- repeated serialization;
- unnecessary copies;
- object and array allocation;
- memory lifetime;
- database round-trips;
- query cardinality;
- indexes and filtering;
- Redis calls;
- network requests;
- browser actions;
- locking duration;
- thread blocking;
- polling frequency;
- timer frequency;
- retry amplification;
- log volume;
- disk I/O.

Do not add work to every tick, timer, request, scraped row or rendered bar when
the result can be computed once, cached safely, incrementally updated or moved
outside the hot path without changing semantics.

Do not add caching merely to make code appear faster. A cache requires explicit:

- key identity;
- owner;
- lifetime;
- freshness rule;
- invalidation;
- missing-value behavior;
- stale-value behavior;
- concurrency behavior;
- source-of-truth relationship.

Resource lifecycle must be explicit. Release resources owned by this scope on
every applicable success, failure and early-return path, including files,
sessions, browser pages, locks, timers, cancellation sources and native handles.
Respect borrowed or transferred ownership; do not close a caller-owned resource.
Use cleanup constructs whose actual release and transaction semantics match the
contract, preserving cancellation and the original failure.

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

## 8. Tests are evidence, not product semantics

Establish expected behavior from:

- the current owner request;
- explicit acceptance criteria;
- verified current behavior that must be preserved;
- authoritative platform contracts.

Never derive expected results from the new implementation itself.

Forbidden test patterns:

- running new code and snapshotting its output as the expected value;
- copying the production algorithm into the test;
- weakening an assertion because the new code fails it;
- deleting a regression test only to make the patch green;
- adding many equivalent tests with no distinct failure mode;
- mocking away the actual boundary being claimed;
- testing only the branch that the fixture already forces;
- treating coverage percentage as correctness;
- treating a green suite as owner acceptance.

Prefer existing production-linked checks.

Before relying on a test double, verify that it reproduces the real dependency's
relevant states, return values, errors and lifecycle transitions. Derive fixtures
from a verified contract or observed producer behavior, not the desired branch.
Do not normalize away the distinction being tested, such as NULL versus an
empty string after a detach operation.

A translated or emulated test may establish portable algorithm behavior; it
does not by itself establish source-language or runtime-specific semantics.
Claims about those semantics require evidence from the corresponding environment
within current authority, or an explicit verification gap. Compilation does not
close that gap.

Add a new test only when:

- it maps to a named acceptance criterion or regression;
- existing checks cannot prove that behavior;
- it has an independent oracle;
- it covers a distinct failure mode.

For a regression, prefer the real failing call sequence and confirm, when
practical and authorized, that the same check rejects the known faulty version
and accepts the correction. For a critical new guard or invariant without such
a version, when practical and authorized, bypass it in an isolated check, confirm
failure, and restore the correct implementation.
Do not create a large mutation-testing program unless the task requires it.
During review ask: which false assumption could be shared by the implementation
and the test, allowing both to agree while production fails? Resolve it with
independent contract or runtime evidence, or retain the explicit gap.

## 9. Verification order

Verification must include reasoning about the implementation, not only execution
of tests.

Use this order:

1. Semantic walkthrough against the owner's business logic.
2. Trace every changed production symbol to a criterion or preserved invariant.
3. Inspect the complete final diff.
4. Review direct callers, consumers and shared state.
5. Review failure, fallback, lifecycle and concurrency paths.
6. Review performance and resource effects.
7. Run applicable static, type, lint, build, ABI or compile checks.
8. Run focused existing tests.
9. Add only minimal justified new tests.
10. Run authorized integration or runtime checks when they are necessary.
11. Distinguish source correctness, tests, build, deploy, runtime and owner
    acceptance.

A passing test does not override a defect found by semantic review.

Before combining another causal slice, obtain the smallest decisive authorized
check for the current slice's changed behavior and affected preserved invariants.
Check the final deliverable after relevant code generation, export rewriting or
packaging, not just the input source. Reuse unaffected checks. If a restriction
prevents a necessary check, record the exact gap; never replace it with a hash,
export count or a self-declared review flag. Do not expand into unrelated tests.

Every declared preserved invariant needs a verification result or a concrete
not-run/not-applicable reason, just like a new acceptance criterion. A valid
record with failed or unrun checks is not a verified product outcome. Where a
known failing artifact exists, confirm that the targeted check detects it and
accepts the corrected artifact without executing unapproved external actions.

Use external engineering sources, including Stack Overflow for Agents, only
when a specific technical uncertainty, platform behavior or failure pattern
requires outside evidence. External guidance never overrides the owner's
business logic, current project contracts or observed production behavior.

## 10. Completion gate

Do not call the work complete until all are true:

- the owner's requested behavior is implemented without reinterpretation;
- no unresolved assumption can change observable semantics;
- unrelated behavior is preserved;
- every production change is explained by a criterion or invariant;
- the affected causal chain has been reviewed;
- no unnecessary architecture or dependency was added;
- failure and lifecycle behavior is explicit;
- performance and resource effects are understood;
- verification results are reported honestly;
- unverified production risks are named;
- no test result is presented as proof of something it did not exercise.

In the final report, state:

- what behavior changed;
- what behavior was intentionally preserved;
- which files and symbols changed;
- why the implementation is minimal;
- which system boundaries were reviewed;
- what was actually verified;
- what remains unverified.
