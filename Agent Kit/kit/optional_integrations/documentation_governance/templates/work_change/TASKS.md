# Tasks: <change title>

Change ID: `<change-id>`
TaskContractV3 ID: `<TASK-id or none>`

When this `.work` process is activated, this file is the sole authority for
operational task status, blockers, and recorded verification state for this
change. Use one independently verifiable, vertical task per section. Do not
copy this register into Kit artifacts or durable documents.

## WI-<id>: <task title>

Operational status: `<proposed | accepted | blocked | active | verified | failed | cancelled>`
Behavior: <User-visible or independently observable result.>
Vertical scope: <Relevant layers or files.>
Dependencies / blockers: <Task IDs or `none`.>

### Acceptance criteria

1. <Observable acceptance claim.>

### Verification recipe

1. <Exact independently runnable check and expected result.>

### Verification record

<VerificationReceiptV2 reference or evidence link, verifier, environment, and
timestamp. A link is evidence navigation; the receipt remains the typed record.>

### WorkItemGraphV1 mapping

<When independently activated, map this task to `id`, `title`, `behavior`,
`vertical_scope`, `acceptance_claims`, `verification_recipe`, and `blocked_by`.
Any generated WorkItemGraphV1 projection is Reference Lab material: recompute
its status and frontier from this file, never edit it, and never treat it as an
independent status source.>
