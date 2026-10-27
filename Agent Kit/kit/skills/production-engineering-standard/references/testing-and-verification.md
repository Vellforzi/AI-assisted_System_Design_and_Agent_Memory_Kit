# Testing and verification

Mandatory when the entrypoint routing applies. These details preserve existing
requirements; they do not add authority or a separate workflow.

## Professional responsibility

Act as a senior production engineer responsible for long-term correctness,
maintainability, reliability, performance and operational safety.

Professional quality is demonstrated by the resulting design and evidence,
not by claims such as "clean", "robust", "production-ready" or "best practice".
Use `engineering-review-checklist.md` for the final engineering review.

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
