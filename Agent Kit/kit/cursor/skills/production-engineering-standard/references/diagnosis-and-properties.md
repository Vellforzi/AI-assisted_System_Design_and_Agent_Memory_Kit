# Root-cause checks and useful properties

Use the diagnosis section for a defect with competing causal explanations. Use
the property section only when an established invariant gives stronger coverage
than a few examples. Neither adds a separate workflow or mandatory dependency.

## Distinguish cause from symptom

State the observed failure, expected preserved behavior, relevant source version
and competing hypotheses. Choose the smallest authorized observation that would
separate the hypotheses. Record the observation that could disprove the favored
explanation, not only evidence consistent with it.

Trace the bad value or state backward to its first evidenced divergence.
Suppression, sleep, fallback and an extra guard do not establish a root cause.
Use existing evidence before adding instrumentation. Do not infer architecture
failure from a fixed attempt count or repeat an unchanged failed collection.

After confirming a cause, search the exact causal pattern in related callers or
implementations. Generalize one condition at a time and inspect each match.
A lexical match is a candidate, not a defect; a discovered defect does not
authorize unrelated repairs. Preserve independent valid verification.

## Properties need an independent oracle

Derive a property from an owner requirement, a verified preserved contract or an
authoritative dependency rule. Do not infer it from the new implementation.
Examples that can be useful when the contract actually promises them:

- round-trip preservation for supported serialization inputs;
- idempotence for normalization or an explicitly idempotent operation;
- conservation, ordering or bounds for a defined calculation;
- equivalent results for two independently specified representations.

Choose inputs covering meaningful boundaries and a case that violates the
property. Check that the generator reaches those cases, assumptions do not
discard almost every example, and comparisons are not vacuous (for example,
empty collections or comparing the function to itself).

Use existing test facilities. A small deterministic set of boundary examples
may be sufficient; do not require Hypothesis or refactor production code merely
to accommodate a generator. If a new testing dependency materially helps a real
task, justify it under that task's authority.

Mock only the boundary not under investigation. Preserve a dependency's actual
failure and lifecycle behavior in a double. When available and safe, demonstrate
that the check rejects the known faulty implementation/artifact.

## Provenance

Adapted selectively from the hypotheses in
[systematic-debugging](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging)
and the invariant/variant-analysis techniques in
[Trail of Bits skills](https://github.com/trailofbits/skills/tree/5c99c03fb8a9ea568432ecbcba5d86e9f4ac2bf0).
Do not import their mandatory agent chains, retry counts, repository-wide
rewrites, branch policies or tool-installation assumptions.
