# /amk-context-advisor

Run Agent Memory Kit context-advisor preflight for the current task.

Mode: read-only unless the owner explicitly requested apply.

Steps:

1. Identify task intent: answer, analyze, plan, patch-builder, audit, repair, or apply.
2. Load only the scoped project context in the AMK read order.
3. Check whether `Project Map/eval_suite` is synced to `Agent Kit/kit/eval_suite` or must be treated as stale mirror.
4. Check whether live Cursor integration paths exist when relevant:
   - `.cursor/rules/context_advisor_preflight.mdc`
   - `.cursor/commands/*`
5. Report missing evidence instead of inventing project facts.
6. If an implementation is needed, produce a scoped Cursor task block.

Forbidden unless owner explicitly authorizes apply: edits, Project Map updates, git push, deploy, DB writes, secret disclosure, unrelated file reads.
