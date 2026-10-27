# Cursor worker protocol

Read before assigning work to Cursor or interpreting its result. These rules
apply within current delegation authority; they do not authorize delegation.

A Cursor worker reads its named scope and a direct causal caller/callee/test
when needed. Return missing facts or additional scope to the parent through
`SCOPE_DELTA_REQUEST`; no per-file owner approval for an authorized causal delta.
Use at most two Cursor attempts per slice, never an unchanged-contract retry.
The parent then repairs/completes the slice or reports the real blocker;
exhausting worker attempts alone is not a reason to abandon available work.

Classify worker results as `TRANSPORT_FAILED_NO_EXECUTION`, `RUN_FAILED`,
`PATCH_USABLE_RESULT_MISSING`, `SEMANTIC_REJECTED`, or `SUCCESS`. Inspect a
usable bounded diff when the result envelope is missing; do not rerun solely
to obtain `cursor_submit_result` or a cleaner report. Reports are evidence,
not proof; retain source references, omissions and uncertainty.
