# /review

Purpose: independently compare implementation, result, validation, receipts,
and execution integrity against the active contract.

Mode: review
Mutations: forbidden

Execution routing: resolve `review + independent_review + path zone` to
`job_review` / `review_read_only`. Do not reuse an executor's write lease.

Required verdict dimensions:

- contract/scope compliance;
- data validity;
- execution integrity and final-event discipline;
- verification and side-effect receipts;
- risks, missing evidence, and exact owner gate.

Do not repair findings in review mode. A bounded repair requires a separate
owner `/apply` and new/updated validated execution profile.
