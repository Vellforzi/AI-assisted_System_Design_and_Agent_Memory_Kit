# Context Compaction Control Policy — AMK v3.9.5

Status: portable policy for Cursor/Codex/chat agents.
Purpose: let long-running agents intentionally reduce active context load without converting compressed chat history into project truth.

## 1. Core rule

The agent cannot assume it can directly delete arbitrary past chat history from the host platform. It can control context pressure by:

1. stopping re-introduction of bulky payloads;
2. using provider/platform compaction or summarize controls when available;
3. clearing or excluding old re-fetchable tool outputs when the runtime supports it;
4. creating a structured checkpoint or handoff;
5. hydrating future work from Project Map, Working State, Source Authority, and exact evidence refs.

A visible context-token count may decrease because the platform compacted, summarized, truncated, cleared tool outputs, or changed accounting. A decrease is useful operational signal, not proof that project state was safely preserved.

## 2. Authority boundary

Platform summaries and compressed chat history are non-authoritative hints. They must never:

- establish project facts;
- authorize file edits, git actions, DB writes, deploys, or external side effects;
- replace Project Map, Working State, Source Authority, opened files, diffs, test output, or explicit owner input;
- become durable memory without Memory Compiler promotion and evidence.

## 3. Trigger conditions

Run the compaction-control gate when any condition appears:

- owner asks to summarize, compact, trim, shrink, or continue longer in one chat;
- visible context usage approaches a high-water mark or unexpectedly decreases;
- a task phase finishes and the next phase can continue from refs;
- tool outputs dominate context: file bodies, logs, search result dumps, full diffs, duplicate terminal output;
- before a multi-file apply/repair loop when the chat is already long;
- after platform auto-compaction or suspected summary/truncation;
- before durable Project Map updates from a long session.

## 4. Required CompactionPlan

Before summarizing or compacting project state, output this plan and ask for owner approval unless the owner already gave explicit checkpoint/update permission.

```yaml
context_compaction_plan:
  trigger: owner_request|high_water_mark|phase_boundary|tool_output_bloat|suspected_platform_compaction|pre_project_map_update
  mode: propose_only|owner_approved_compaction|approved_checkpoint_update
  goal: "reduce active context while preserving replay-critical state"
  keep:
    - owner task and latest explicit instructions
    - active intent, mode, scope, allowed/forbidden actions
    - Project Map/current_state ref, working_state ref, source_authority ref
    - accepted decisions with evidence refs
    - changed files, diffs summary, validation commands/results
    - open risks, blockers, unresolved claims, next safe step
    - side-effect receipts and unsafe-to-repeat actions
  drop_or_do_not_reinclude:
    - raw re-fetchable tool output older than the latest checkpoint
    - full file bodies unless the exact snippet is required
    - duplicate terminal logs; keep command + result summary + ref
    - stale hypotheses not needed for repair/audit
    - provider/model UI details unless dated and relevant
    - secrets, credentials, tokens, chain-of-thought
  evidence_refs: []
  missing_evidence: []
  owner_approval_required: true
  post_compaction_recovery:
    - reload Project Map/current_state.md
    - reload Project Map/working_state.yaml
    - reload Project Map/source_authority.yaml
    - hydrate only policy-allowed memory units
    - re-fetch raw evidence only when needed
```

## 5. Summary payload contract

The summary/handoff may contain:

- project/task identity;
- latest owner-approved scope and permission mode;
- current checkpoint;
- decisions and facts with evidence refs;
- files changed and validation results;
- open risks/missing evidence;
- next safe step;
- unsafe-to-repeat side effects and receipts;
- explicit exclusions and stale facts to avoid.

The summary/handoff must not contain:

- secrets;
- hidden chain-of-thought;
- raw logs or full file bodies when refs/summaries suffice;
- unsupported claims as facts;
- platform/provider model facts without observed date/source;
- owner approvals inferred from prior chat summary.

## 6. Tool-output clearing rule

Prefer clearing/excluding old re-fetchable tool outputs before summarizing the whole conversation. Safe candidates:

- file reads that can be re-read by path;
- web/Drive search results that can be re-run or cited by ref;
- terminal output where command + pass/fail + short error excerpt is enough;
- duplicate diffs where file path + hunk summary is enough.

Never clear without preserving:

- evidence refs;
- validation command and result;
- error signatures needed for repair;
- side-effect receipts;
- unsafe-to-repeat actions;
- latest owner instruction and scope.

## 7. Recovery after suspected compaction

When platform compaction is suspected, switch to recovery behavior:

1. State that platform summary is not project truth.
2. Load Project Map/current_state.md, working_state.yaml, and source_authority.yaml.
3. Load active task/checkpoint/handoff.
4. Retrieve only policy-allowed memory units.
5. Continue from confirmed evidence or report missing evidence.

## 8. Cursor command integration

Use `/amk-context-compact` as a controlled prompt command. It does not magically force the IDE to drop history; it makes the agent produce the plan, gated summary/handoff, and verification checks. If the host provides a native `/summarize` or compact command, the owner may run it after approving the plan.

## 9. Evaluation expectations

Smoke eval must verify:

- summaries cannot establish facts or approvals;
- compaction requires a keep/drop/evidence plan;
- old tool outputs are treated as re-fetchable bloat when possible;
- Working State and Project Map refs survive compaction;
- side-effect receipts survive compaction;
- stale facts do not re-enter normal answer context as current truth.
