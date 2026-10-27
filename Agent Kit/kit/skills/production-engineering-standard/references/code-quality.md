# Comments, types, language idioms and error boundaries

Read the relevant sections when writing or materially changing code. These rules
describe implementation quality inside the owner-authorized behavior. They do not
authorize a repository-wide annotation, formatting or modernization campaign.

## Comments that help the next reader

Automatically explain the purpose of new and materially changed modules, classes
and functions. Add local explanations at meaningful algorithm, state, ownership
or compatibility boundaries. Cover adjacent code only when needed to understand
the changed behavior. A trivial accessor does not need its name repeated.

Start with what the code accomplishes in domain terms. Add relevant inputs,
outputs, units, constraints, side effects and failure behavior that a caller
cannot infer reliably from the signature. Explain why a non-obvious choice is
necessary. Do not duplicate types already clear from annotations, narrate syntax,
assert unverified guarantees, or add a template paragraph for every statement.

For example, `# Increment index` adds nothing to `index += 1`; an evidenced
explanation that an offset excludes a header row describes the actual contract.
Do not invent that explanation without checking the data layout.

Use Python docstrings for callable/module documentation, C# XML documentation
for public contracts, and normal language comments for local reasoning. Follow
the adopting project's comment-language policy. Keep comments current when the
code changes; delete or correct claims no longer enforced by the implementation.
Put a long design explanation in existing relevant documentation and link it
locally. Never substitute a comment for needed executable behavior.

## Types describe the real contract

For new and materially changed Python functions, annotate inputs and results,
including `-> None` when appropriate, and parameterize collections. Reuse domain
types. Annotate locals when inference is insufficient, not merely to label every
assignment. Preserve accepted input shapes, mutability, nullability, numeric
precision, units, return states and exceptions.

Use `TypedDict` for an actual structured mapping and `Protocol` for an actual
consumer interface when they clarify a real boundary. Do not create a class,
protocol, enum or wrapper for every field. Prefer an existing correct type over a
parallel type hierarchy. `Sequence`, `Mapping` and `Iterable` are appropriate
only when the implementation actually accepts their contracts.

Do not replace missing data with zero to satisfy a type checker. `object` means
an unknown value that must be narrowed before use; it is not interchangeable
with `Any`. A cast changes static interpretation, not runtime validity. Justify
casts from established evidence; do not cast an unchecked payload into validity.
Keep unavoidable `Any` at the actual dynamic/library boundary. A targeted
diagnostic suppression needs its rule and a concrete limitation or contract
explanation; whole-file ignores and weakening checks are not fixes.

Ordinary annotations are not runtime input validation. In frameworks that inspect
annotations or documentation, they may nevertheless change behavior:

- FastAPI return annotations can change response validation, serialization,
  filtering and OpenAPI; parameter annotations can change input validation.
- Pydantic model fields and ORM annotations may affect schemas and runtime
  construction. Do not rewrite them as a supposedly cosmetic typing change.
- FastAPI route docstrings can become public OpenAPI descriptions. Use a normal
  comment for an internal explanation that must not change the public contract.

Check the actual framework version and compare the relevant contract before and
after such edits. Do not add `response_model=None`, validators, defaults, coercion
or new model classes merely to make a typing change pass.

## Idiomatic code within the supported toolchain

Establish language/runtime/compiler versions and local conventions first.
Preserve the module's coherent style and external names. Prefer standard,
readable constructs; do not introduce a formatter or broad restyling as a side
effect of a behavior change.

- Python: use direct iteration, `enumerate`, suitable standard collections and
  readable comprehensions where they express the operation clearly. Prefer a
  normal loop to nested or side-effectful comprehensions. Use `is None` where
  absence differs from false/zero/empty. Choose generators only when lazy
  execution, resource lifetime and exception timing preserve the contract.
  Do not import Java/C#-style factories and getter/setter scaffolding by habit.
- C#: use the target compiler's type, async, nullability and disposal features.
  Do not assume nullable-reference support or newer syntax in a legacy target.
  Avoid `dynamic`, null-forgiving operators or broad casts as diagnostic
  workarounds. Preserve cancellation, synchronization context and native ABI.
- MQL4/MQL5: verify each platform's actual type widths, conversions, event
  signatures, object ownership and API result/error contract. Do not invent
  Python/.NET exception handling. `GetLastError()` is not a substitute for the
  documented operation result; account for its retained error state. Preserve
  serialization, buffer layout and DLL parameter compatibility.
- SQL: match schema types, row grain, `NULL` semantics, integer/decimal precision
  and parameter binding. Do not convert values or add `COALESCE`, joins or casts
  as stylistic repairs when they change meaning, cardinality or index use.
- Other languages: inspect their supported version, project conventions and
  authoritative guidance for the relevant feature; do not impose another
  language's abstractions or naming syntax.

## Catch and clean up only for a real responsibility

For each new or changed handler, determine the expected failure, who owns it and
the required outcome. Catch when this layer has an evidenced recovery,
translation or final failure-reporting responsibility. Otherwise let the error
reach its established owner. Keep `try` narrow so an unrelated bug cannot be
mistaken for the expected failure. Prefer specific exception types.

A broad handler can be correct at an established task/process/protocol boundary.
Preserve its defined failed outcome; never silently turn failure into success,
empty data, a retry, stale data or a new fallback. Avoid duplicate log-and-rethrow
handlers at every layer. Preserve traceback/cause when propagating or translating
errors, without exposing credentials or sensitive payloads.

Use `finally` only for owned resource cleanup or required state restoration.
Prefer `with`, `async with` or `using` when their acquire/release/transaction
semantics match the contract. Do not close a caller-owned resource, release twice,
commit an unsuccessful transaction, or suppress the original error through a
cleanup failure or `return` in `finally`. Plain `except: raise` and `finally:
pass` add no behavior.

Treat cancellation as cancellation, not a retryable business failure. Python
`CancelledError` must normally propagate after required cleanup; .NET
cancellation must retain its token and defined completion behavior. Consider
partial acquisition, failed acquisition, early return, repeated close and
concurrent use only where relevant to the resource's real lifecycle.

## Sources

- [PEP 8](https://peps.python.org/pep-0008/): project consistency, readable idioms,
  comments, narrow exception regions and resource management.
- [PEP 257](https://peps.python.org/pep-0257/): purpose and callable contracts.
- [Python typing](https://docs.python.org/3.13/library/typing.html) and
  [asyncio cancellation](https://docs.python.org/3.13/library/asyncio-task.html).
- [C# conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
  and [.NET exceptions](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions).
- [FastAPI response types](https://fastapi.tiangolo.com/tutorial/response-model/)
  and [route docstrings](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/).
- [MQL5 casts](https://www.mql5.com/en/docs/basis/types/casting) and
  [GetLastError](https://www.mql5.com/en/docs/check/getlasterror).

These are platform references, not authority to change product semantics.


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
Read the relevant sections of [code quality](code-quality.md) when
writing comments/types, choosing idioms or changing error/resource handling.

Each catch must have a defined responsibility and outcome; keep try regions
narrow. Broad handling is justified only at an established failure boundary.
Use finally for real owned cleanup/state restoration, not as a template.
Prefer matching language resource-management constructs; preserve the original
failure, cancellation, partial state and ownership.

For competing root-cause hypotheses or useful invariant-based tests, consult
[diagnosis and properties](diagnosis-and-properties.md). These are
conditional techniques, not extra mandatory workflows or dependencies.

For project language/version and local type-check routing, read
[project toolchains](project-toolchains.md).
