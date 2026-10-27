---
name: codex-worker-contract
description: Follow one bounded Cursor task contract delegated by Codex, with one causal read hop and structured result admission.
---

# Codex worker contract

Apply when the Codex Cursor-worker bridge prompt contains all three:
`TASK_ID`, `RUN_ID`, `CONTRACT_HASH`.

- Execute only `OPERATION`; write only `ALLOWED_PATHS`; use only
  `ALLOWED_ACTIONS`. Respect explicit `FORBIDDEN_ACTIONS` denials.
- Read named paths plus at most one direct causal hop: direct caller, callee,
  or directly production-linked test.
- Request additional write scope once via `SCOPE_DELTA_REQUEST`;
  write those paths only after parent Codex accepts.
- Never expand compilation into repair, testing into refactoring, or editing
  into commit, push, deploy, cleanup or parent-task recovery.
- Parent Codex permits at most two attempts per semantic slice;
  never retry an unchanged contract.
- Classify with exactly one:
  `TRANSPORT_FAILED_NO_EXECUTION`, `RUN_FAILED`,
  `PATCH_USABLE_RESULT_MISSING`, `SEMANTIC_REJECTED`, `SUCCESS`.
- On normal `SUCCESS`, call `cursor_submit_result` exactly once with task,
  agent, run and contract identifiers, then stop.
- Missing envelope with an inspectable bounded diff: parent Codex may inspect
  it once. Never rerun solely for the envelope.

Never read or print API keys, private keys, tokens, passwords, `.env` files or
unrelated credential stores.
