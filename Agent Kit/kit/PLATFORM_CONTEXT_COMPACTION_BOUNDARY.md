# Platform Context Compaction Boundary — AMK v3.9.5

Purpose: protect durable project memory from platform-generated summaries, compressed chat history, provider personalization, hidden context reconstruction, and unmanaged context compaction.

## Core rule

Platform-generated summaries are non-authoritative hints.

They must never:

- establish project facts;
- authorize actions;
- replace the Project Map;
- replace Working State;
- override Source Authority;
- mark work as completed;
- create durable memory;
- resolve conflicts;
- replace explicit owner approval;
- replace opened files, tool output, diffs, test output, or other evidence artifacts.

If a platform summary conflicts with Project Map, Source Authority, opened project files, or current owner input, the platform summary loses.

## Agent-created summaries are also gated

The agent must not summarize, compact, promote, or rewrite project state unless explicitly asked by the owner or operating inside an approved checkpoint/update task.

Allowed without write permission:

- propose a checkpoint;
- propose a handoff;
- propose a CompactionPlan;
- propose a Project Map delta;
- say that context risk exists;
- ask the owner to start a fresh session;
- explain what evidence is missing.

Not allowed without explicit owner approval:

- writing Project Map memory;
- converting chat recall into durable facts;
- treating a summary as an accepted decision;
- claiming that work was completed from summary alone;
- using summary-only approval for file edits, DB writes, git actions, deploys, or external side effects.

## Controlled compaction addition

When context must be reduced, the agent must separate:

- **replay-critical state**: owner task, scope, decisions, evidence refs, changed-file refs, validation summary, side-effect receipts, next safe step;
- **re-fetchable bloat**: old file bodies, full logs, duplicate terminal output, search dumps, obsolete failed attempts.

Before compaction, the agent should output a `context_compaction_plan` with keep/drop/evidence/missing-evidence fields and ask for owner approval unless the task already authorizes checkpoint/update work.

## When context compaction is suspected

Context compaction should be suspected when:

- the chat is very long;
- the host tool indicates that context is compressed, summarized, or truncated;
- the visible context-token count unexpectedly decreases;
- the agent cannot see earlier raw messages it previously referenced;
- the agent sees a vague or platform-generated summary of prior work;
- the next step depends on facts that are only present in chat history;
- the owner says that the session may be near the context limit.

When suspected, the agent must switch to recovery behavior:

1. State that platform summary will not be used as project truth.
2. Load or request `Project Map/current_state.md`.
3. Load or request `Project Map/working_state.yaml`.
4. Load or request `Project Map/source_authority.yaml`.
5. Load or request the active task contract, latest checkpoint, or latest handoff.
6. Retrieve only policy-allowed memory units.
7. Continue only from confirmed evidence.
8. If evidence is missing, report `missing evidence` instead of reconstructing project state from chat recall.

## Fresh-session Project Map update rule

Project Map updates should preferably be performed in a fresh or low-context session.

If the active session is long, near the context limit, or may have been compacted, the agent must not directly update durable project memory from chat recall.

Instead, it should produce a structured handoff or Project Map delta for owner review.

The owner may then start a fresh session and apply the Project Map update from:

1. the current Project Map;
2. the approved handoff or delta;
3. explicit evidence artifacts such as changed-file lists, diffs, test output, opened source files, or owner statements.

Platform summaries and compressed chat history must not be used as evidence.

## Safe chat phrase

```text
Context may be compressed. Do not use platform summary as project truth. Recover from Project Map, Working State, Source Authority, and the latest approved handoff only. If context needs shrinking, propose a CompactionPlan first.
```

## Codex PreCompact policy

When using Codex, automatic context compaction should be treated as a checkpoint boundary.

Recommended behavior:

1. Block automatic compaction if no checkpoint or handoff exists.
2. Ask the owner to create a structured checkpoint/handoff.
3. Resume work from Project Map and Working State in a fresh or recovered session.
4. Do not promote compressed chat history into Project Map.

The optional Codex hook `pre_compact_checkpoint_guard.py` implements the first safety step by stopping auto-compaction and asking for checkpoint/handoff first.
