# Causal proof table

For every acceptance row, add this section to the task-local scenario matrix.
Populate it from the current production path; do not copy example component or
state names from another task.

## Causal proof

| ID | Gate path | Production establishment | Order/reset coverage | Anti-vacuity |
|---|---|---|---|---|
| ROW_ID | producer -> transport/persistence -> consumer | UNPROVEN | UNPROVEN | UNPROVEN |

Use these machine-readable values:

- `Production establishment`: `PRODUCTION_EXECUTED`, `NOT_REQUIRED`,
  `UNPROVEN`, `PRECONDITION_INJECTED`, or `DOWNSTREAM_ONLY`.
- `Order/reset coverage`: `PROVEN`, `NOT_REQUIRED`, `PARTIAL`, or `UNPROVEN`.
- `Anti-vacuity`: `PROVEN`, `NOT_REQUIRED`, or `UNPROVEN`.

`Gate path` is task-specific. Name the authoritative producer, cross-boundary
transport or persistence mechanism, and consumer. Use `NOT_REQUIRED` only when
the row has no production-established behavioral prerequisite and all three
status cells are also `NOT_REQUIRED`.

A behavioral row closes locally only when its production establishment is
`PRODUCTION_EXECUTED` or genuinely `NOT_REQUIRED`, its required order/reset
coverage is `PROVEN` or genuinely `NOT_REQUIRED`, and anti-vacuity is `PROVEN`
or genuinely `NOT_REQUIRED`. A `JUSTIFIED_SEAM` requires `Anti-vacuity =
PROVEN`.
