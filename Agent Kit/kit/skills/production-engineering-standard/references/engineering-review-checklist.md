# Engineering review checklist

Use this checklist before declaring code or logic work complete.

## Product semantics

- The owner outcome is preserved in the owner's wording.
- The requested behavioral delta is explicit.
- Missing instructions were treated as preserve-current-behavior.
- No new fallback, schedule, retry, cache rule, persistence rule, relationship,
  state transition, public contract, UI behavior or trading behavior was invented.
- Every unresolved assumption that could change observable behavior was returned
  to the owner instead of being guessed.

## Causal chain

- Producer, normalization/calculation, storage/state, transport, cache, consumer
  and owner-visible result were identified where applicable.
- Direct callers, consumers and shared state were reviewed.
- Database, Redis, schedule, timezone, lifecycle, concurrency and compatibility
  boundaries were reviewed where applicable.
- The review covers the complete affected chain, not unrelated repository areas.

## Dependency contracts

- Material dependency assumptions were checked against relevant-version
  documentation and available implementation, including guards around old calls.
- Relevant built-in capabilities were considered before adding wrappers or checks.
- The actual call sequence, post-call states and subsequent consumer conditions
  were traced, including special values and relevant lifecycle/error transitions.
- Source/version and a dependent check or explicit gap support each material
  assumption; names, analogies and test doubles were not treated as evidence.

## Design and code

- The implementation is the smallest coherent complete change.
- Every changed production symbol maps to an acceptance criterion or invariant.
- No speculative feature, future-use abstraction, broad cleanup, new framework
  or unrelated refactor was added.
- Domain names, state ownership, units, time zones and empty/error semantics are
  explicit.
- Resource ownership and cleanup are correct on success, failure and early exit.

- Purpose comments/docstrings explain the materially changed code, remain
  accurate, and follow the project's language policy without restating syntax.
- Types preserve accepted inputs, actual output/absence states and collection
  elements; Any/casts/suppressions have narrow, evidenced reasons.
- Framework-visible annotations/docstrings preserve validation, serialization,
  ORM and OpenAPI contracts.
- Idioms match the actual compiler/runtime and local style; no unrelated
  modernization, abstractions or formatting were introduced.
- Each catch has a defined responsibility; finally/with/using reflect actual
  ownership and preserve original failures, cancellation and partial state.
- Trust-boundary validation, authorization and parameter binding were preserved.

## Performance

- Complexity and loop bounds are understood.
- No unnecessary database, Redis, network, browser, serialization, allocation,
  lock, polling, logging or disk work was added.
- Hot-path frequency and memory lifetime were reviewed.
- Any cache has explicit ownership, key identity, freshness and invalidation.

## Reliability

- Empty, missing, malformed, stale, duplicate, reordered and partial states were
  considered where relevant.
- Retry, timeout, restart, cache loss, concurrent instance and version-skew paths
  were considered where relevant.
- Fallback was checked against the currently deployed producer/system behavior,
  not only the new producer.

## Event-driven progress (when applicable)

- The real initial state and callbacks before resource readiness were traced.
- Each wait/pending state names the actual request, full dispatch route,
  reachable next executor, ownership release and terminal outcomes.
- Safety and progress were checked separately under explicit prerequisites;
  ordinary probes do not continually reset the progress measure.
- Event identity is validated before mutating current ownership; readiness,
  queue occupancy and work revision are not conflated.
- Relevant MQL4/MQL5 event/lifecycle work used $mql-event-lifecycle and verified
  its platform-specific contracts; no new retry/recovery semantics were invented.
- Sequence-model, native/runtime and owner-acceptance evidence remain distinct.

## Tests and verification

- Expected behavior came from owner criteria, preserved behavior or an
  authoritative platform contract, never from the new implementation output.
- Existing checks were preferred.
- Applicable type checks ran against the correct environment; baseline-aware
  success is distinguished from full typing correctness and runtime proof.
- A root-cause hypothesis has a discriminating observation where needed;
  symptom suppression alone is not a causal explanation.
- Every new test has a criterion, independent oracle and distinct failure mode.
- Test doubles and fixtures preserve the real dependency's relevant states and
  transitions; translated tests do not substitute for target-runtime semantics.
- Review challenged assumptions shared by the implementation and test; remaining
  uncertainty and unavailable target-environment checks are stated explicitly.
- No assertion was weakened or duplicated merely to make the patch green.
- Semantic walkthrough and final-diff review were completed before relying on
  tests.
- Every affected preserved invariant has a result or a concrete verification gap.
- Relevant generated/exported/packaged artifacts were checked after transformation.
- A targeted check rejects the known failing artifact when one is available.
- Static/build/compile/test/runtime/owner-acceptance evidence levels are reported
  separately.

## Final report

- Changed and intentionally preserved behavior are stated.
- Changed files and symbols are stated.
- Why the implementation is minimal is stated.
- Reviewed system boundaries and actual checks are stated.
- Remaining unverified production risks are stated.
