# Communication anti-patterns

## Vague source

Bad:

> Показатель добавляется из Dashboard.

Why it fails:

- writer is unknown;
- reader is unknown;
- table is unknown;
- cache behavior is unknown;
- cadence is unknown;
- "Dashboard" may be a UI label rather than storage;
- missing-data behavior is unknown;
- source precedence is unknown.

Required correction:

Name the producer, technical storage, field, reader, cadence, cache path,
precedence, fallback and relation between the UI name and technical identifier.

## False completeness

Bad:

> Данные сохраняются, кеши обновляются, API формирует график.

Why it fails:

- which data;
- which tables;
- which caches;
- which keys;
- which process updates them;
- when;
- which API route;
- which transformation;
- which client;
- what happens on partial failure.

## Test-only confidence

Bad:

> Всё проверено, тесты проходят.

Required correction:

List the checks, exact behavior exercised, evidence layer, missing runtime
coverage and whether production/deployment/owner acceptance occurred.

## Tool-centric answer

Bad:

> Обновил 17 разделов и проверил страницу.

Why it fails:

It reports the work process but may not answer how the business logic actually
works.

Required correction:

Explain the resulting logic first, then state what artifact was updated and how
it was checked.

## Business label used as technical identity

Bad:

> Данные берутся из Sales Dashboard / Risk View / Vendor Portal.

Why it fails:

A UI tab, business label or external product name does not identify the actual
producer class, table, field, cache key, API path or ownership boundary.

Required correction:

State the UI/business name and then map it to the exact technical producer,
storage, field and consumer. If the mapping was not verified, say so.

## Compressed transition

Bad:

> После этого система обновляет всё необходимое.

Why it fails:

The action, trigger, affected state, order, failure behavior and downstream
consumer are hidden.

Required correction:

Name each material transition, its owner, condition, written state and next
consumer. Separate successful, missing-data and failure paths.
