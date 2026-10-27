# Performance and resources

Mandatory when the entrypoint routing applies. These details preserve existing
requirements; they do not add authority or a separate workflow.

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
