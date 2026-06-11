# Router fragment — Context Compaction Control v3.9.5

Use when a session is long, the owner asks to shrink/compact/summarize context, visible context usage decreases unexpectedly, or tool outputs dominate the active context.

Policy:

1. The agent cannot assume arbitrary past chat history can be deleted; it can control future context by reducing payloads, using refs, and invoking platform compaction/summarize only when available and approved.
2. Platform summaries are non-authoritative hints, not project truth.
3. Before agent-created summary/compact/checkpoint, emit `context_compaction_plan` with trigger, keep, drop, evidence refs, missing evidence, unsafe-to-repeat actions, and post-compaction recovery steps.
4. Ask owner approval before compacting replay-critical project state unless already inside an approved checkpoint/update task.
5. Prefer clearing/excluding old re-fetchable tool outputs before whole-transcript summary.
6. Preserve Working State refs, source authority, accepted decisions with evidence, validation summaries, side-effect receipts, and next safe step.
7. Never put secrets, unsupported claims, stale facts as current truth, full raw logs, or hidden chain-of-thought into summary payloads.
