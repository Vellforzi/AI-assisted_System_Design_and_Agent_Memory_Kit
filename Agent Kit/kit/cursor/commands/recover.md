# /recover

Purpose: recover after context compaction, missing chat history, interrupted work, or suspected state drift.

Mode: recover
Default mutations: forbidden

Procedure:

1. Ignore platform summary as project truth.
2. Load `Project Map/current_state.md`.
3. Load `Project Map/working_state.yaml`.
4. Load `Project Map/source_authority.yaml`.
5. Load active task/checkpoint/handoff if present.
6. Retrieve only policy-allowed memory units.
7. Report the confirmed state and next safe step.
8. If state cannot be recovered, say `missing evidence`.

Do not apply changes until the owner explicitly asks.
