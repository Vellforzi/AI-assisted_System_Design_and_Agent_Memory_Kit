# /amk-context-compact

Run AMK v3.9.5 context compaction control.

Mode: read-only planning by default. Do not edit files, update Project Map, or run git unless the owner explicitly changes mode.

Purpose: reduce active context pressure while preserving replay-critical state.

Procedure:

1. State that the agent cannot assume it can directly delete arbitrary past platform chat history.
2. Identify the trigger:
   - owner_request;
   - high_water_mark;
   - phase_boundary;
   - tool_output_bloat;
   - suspected_platform_compaction;
   - pre_project_map_update.
3. Separate replay-critical state from re-fetchable bloat.
4. Emit:

```yaml
context_compaction_plan:
  trigger: "<trigger>"
  mode: propose_only
  goal: "reduce active context while preserving replay-critical state"
  keep: []
  drop_or_do_not_reinclude: []
  evidence_refs: []
  missing_evidence: []
  unsafe_to_repeat_actions: []
  owner_approval_required: true
  post_compaction_recovery: []
```

5. Ask owner approval before any agent-created summary, compacted handoff, Project Map update, or platform summarize/compact action that may affect replay-critical state.
6. If approved, produce a compact handoff/checkpoint payload with refs, not raw payload dumps.
7. If the host platform provides native summarize/compact controls, tell the owner when it is safe to run them after the plan is approved.

Keep:

- current owner task and latest explicit instructions;
- active intent, mode, scope, allowed/forbidden actions;
- Project Map/current_state, working_state, source_authority refs;
- accepted decisions and facts with evidence refs;
- changed-file refs, diff summary, validation commands/results;
- open risks, blockers, unresolved claims, next safe step;
- side-effect receipts and unsafe-to-repeat actions.

Drop or do not re-include:

- old raw file bodies that can be re-read;
- duplicate terminal output, old search dumps, repeated plan text;
- raw logs except short error signatures needed for repair;
- stale hypotheses unless audit/repair needs them;
- provider/model UI details unless dated and relevant;
- secrets, credentials, tokens, hidden chain-of-thought.
