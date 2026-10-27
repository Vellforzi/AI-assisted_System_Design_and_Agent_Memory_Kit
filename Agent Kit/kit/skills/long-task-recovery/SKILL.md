---
name: long-task-recovery
description: Preserve and recover compact task-local state across compaction, restart or handoff. Use ordinary continuity by default; use locked proof only for an explicitly selected strict task.
---

# Long task recovery

Preserve task continuity without expanding scope, authority or evidence.
Ordinary continuity is the default, including behavioral programming.
Duration or compaction alone does not justify locked proof, a full audit,
a new task or a fresh agent.

Use locked proof only when explicitly selected by the owner/applicable task
policy or substantively escalated through $outcome-driven-task-closure.
Record the reason. An active lock remains binding until genuine completion,
cancellation or task replacement; never switch modes to bypass missing evidence.

## Ordinary continuity

Use the existing task directory, otherwise .codex/tasks/<task-slug>/.
Keep a compact RECOVERY_CAPSULE.md with:
- owner outcome, current steering and remaining work;
- actual repository/branch, relevant changes and protected unrelated work;
- completed checks, evidence paths and limits;
- pending/partial side effects and authorization boundaries;
- blockers/product questions and the exact next action.

Update at meaningful boundaries. Keep compact receipts only when they help
reconstruct effects; do not log commentary or waiting. Ordinary mode requires
no outcome hash, numeric matrix, causal-proof table, binding or closure validator.

To resume:
1. Read the current owner request and capsule.
2. Reconcile actual paths, diff/HEAD, competing writes and partial effects.
   Summaries and old PASS labels are hints, not execution proof.
3. Reuse unaffected evidence and read only sources needed for the next step.
4. Ask about a material missing decision or ambiguous external effect.
   Continue independent authorized work without blindly repeating a successful
   side effect or requesting identical authorization already in scope.
5. Continue until the owner outcome is complete or a real boundary blocks it.

Investigate contradictions only in the affected state and its dependents.
Use a handoff only when safe continuation cannot be reconstructed.

## Locked proof

Read [the protocol](references/protocol.md) only for locked initialization,
schema repair or ambiguity unresolved here. Its strict schema is not the
ordinary-mode default.

Use scripts/recovery_tool.py for init/snapshot/validate/bind/unbind; do not
recreate its schemas. Init is create-only. Bind the exact selected task directory
to the verified current native session. Binding survives compaction, stays local
and must never be published. Repair missing/malformed selected state rather
than silently unbinding it.

Preserve owner-outcome hash, acceptance IDs, causal proof, source/evidence
identity, receipt sequence, active operation and remaining rows.
Read the latest three receipts first; broaden only for a concrete inconsistency.
Failed owner smoke reopens the affected rows and task.

Before a locked closing status, require validator exit 0, ok=true and the
matching closure-allowed field. Remove only that task's binding after genuine
completion, cancellation or replacement. Ordinary unbound tasks have no such gate.

## Reporting

Report completed work, actual checks, limitations and the next necessary action.
Counters and bookkeeping never replace the owner's outcome.
