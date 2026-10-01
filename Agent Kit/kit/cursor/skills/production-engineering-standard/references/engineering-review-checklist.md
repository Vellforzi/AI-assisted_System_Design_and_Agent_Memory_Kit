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

## Design and code

- The implementation is the smallest coherent complete change.
- Every changed production symbol maps to an acceptance criterion or invariant.
- No speculative feature, future-use abstraction, broad cleanup, new framework
  or unrelated refactor was added.
- Domain names, state ownership, units, time zones and empty/error semantics are
  explicit.
- Resource ownership and cleanup are correct on success, failure and early exit.

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

## Tests and verification

- Expected behavior came from owner criteria, preserved behavior or an
  authoritative platform contract, never from the new implementation output.
- Existing checks were preferred.
- Every new test has a criterion, independent oracle and distinct failure mode.
- No assertion was weakened or duplicated merely to make the patch green.
- Semantic walkthrough and final-diff review were completed before relying on
  tests.
- Static/build/compile/test/runtime/owner-acceptance evidence levels are reported
  separately.

## Final report

- Changed and intentionally preserved behavior are stated.
- Changed files and symbols are stated.
- Why the implementation is minimal is stated.
- Reviewed system boundaries and actual checks are stated.
- Remaining unverified production risks are stated.
