# Model Escalation Policy — Agent Memory Kit v3.9.4

Release date: 2026-06-10. Provider/model capability information is volatile and
must be dated when used.

## Normative wording

The user is not expected to predict model insufficiency.

The agent must start with the lowest sufficient route for the current task and
escalate only after reporting a concrete trigger:

1. validation failure;
2. schema/router conflict;
3. insufficient context window;
4. missing model control;
5. repeated scoped failure;
6. task reclassification to audit, repair, or protocol design.

## Operating rule

The agent should not ask the user to choose a stronger model merely because the
task may be difficult. The agent owns route selection. The user may impose a route,
but absent that, the agent uses the least capable route that is sufficient for the
scoped task.

## Escalation report format

When escalating, report the trigger before or with the escalation decision:

```text
Escalation trigger: <one of the six allowed triggers>.
Evidence: <brief observable failure/conflict/window/control reason>.
Route change: <from> -> <to>.
Scope impact: <what changes, if anything>.
```

## Provider/model volatility rule

Provider/model names, context windows, tool availability, pricing, latency, and
quality observations are not durable project facts. They may be recorded only with
an `observed_at` date and should be treated as volatile capability observations.
Do not place volatile provider/model data into permanent Project Map facts unless
the owner explicitly accepts it as a dated decision or constraint.
