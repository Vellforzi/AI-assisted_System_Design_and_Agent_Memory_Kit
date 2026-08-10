# `.work/<change-id>` change folder

Use this reusable folder only for resumable multi-session work, coordination
among multiple executors, more than three independently verifiable slices,
high-risk acceptance, or a requested audit trail. Routine single-session work
should stay artifact-light.

The minimal activated folder contains:

- `TASKS.md`
- `ACCEPTANCE.md`

`PLAN.md` is conditional when an intended approach, scope, or recovery record
is useful. `DEVIATIONS.md` is conditional when material departures need an
append-only record. `artifacts/` is conditional for useful agent-produced
material.

Only in this activated `.work` process, `TASKS.md` is the authority for
operational task status, blockers, and recorded verification state. All other
files and all Kit artifacts may link to task IDs, but must not duplicate a
task-status register. It does not make `.work` authoritative for product facts,
requirements, ADRs, or archives.
