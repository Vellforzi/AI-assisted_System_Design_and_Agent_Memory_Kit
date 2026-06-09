# Agent Memory Kit v3.5.0 — Cursor Integration Pack Release

Release date: 2026-06-09

This release adds a Cursor-focused integration layer and a stricter platform-summary boundary.

The goal is to make Agent Memory Kit easier to use inside Cursor without relying on one huge prompt or on hidden chat memory.

---

## Added

- `Agent Kit/kit/PLATFORM_CONTEXT_COMPACTION_BOUNDARY.md`
- `Agent Kit/kit/CURSOR_INTEGRATION_OWNER_GUIDE.md`
- `Agent Kit/kit/cursor/README.md`
- `Agent Kit/kit/cursor/COMMAND_VOCABULARY.md`
- Cursor rule templates:
  - `cursor/rules/agent_memory_core.mdc`
  - `cursor/rules/project_map_authority.mdc`
  - `cursor/rules/platform_context_compaction_boundary.mdc`
  - `cursor/rules/option_profit_safety.mdc`
- Cursor command templates:
  - `/answer`
  - `/analyze`
  - `/plan`
  - `/apply`
  - `/checkpoint`
  - `/handoff`
  - `/map-delta`
  - `/map-apply`
  - `/recover`
  - `/eval-smoke`
  - `/failure-case`
  - `/inventory`
- Cursor skill templates:
  - Memory Compiler
  - Checkpoint Builder
  - Handoff Builder
  - Eval Case Builder
  - Source Authority Audit
  - Context Recovery
- Read-only subagent templates:
  - API Auditor
  - Scraper Auditor
  - MetaTrader Auditor
  - DB Schema Auditor
  - Docs Drift Auditor
  - Memory Auditor
- Optional hooks examples:
  - secret scan;
  - DB write guard;
  - dangerous git command guard;
  - scope guard;
  - Project Map write guard.

---

## Updated

- `README.md`
- `START_HERE.md`
- `Agent Kit/README.md`
- `Agent Kit/kit/README.md`
- `Agent Kit/kit/MANIFEST.md`
- `Agent Kit/kit/AGENTS.md_TEMPLATE.md`
- `Agent Kit/kit/CURSOR_RULE_TEMPLATE.mdc`
- `Agent Kit/kit/AGENT_INSTRUCTION_FILES_GUIDE.md`
- `Agent Kit/kit/OWNER_USAGE_GUIDE.md`
- `Agent Kit/kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md`
- `Agent Kit/kit/PROVIDER_MEMORY_AND_RUNTIME_BOUNDARY.md`
- `Agent Kit/kit/WORKING_STATE_AND_REPLAY_GUIDE.md`
- `Agent Kit/kit/eval_suite/*`

---

## Core behavioral additions

### Platform summaries are not project truth

Platform-generated summaries, compressed chat history, provider memory, and personalization are non-authoritative hints.

They must never establish project facts, authorize actions, replace Project Map, replace Working State, override Source Authority, mark work as completed, create durable memory, or resolve conflicts.

### Agent summaries are gated

The agent must not summarize, compact, promote, or rewrite project state unless explicitly asked by the owner or unless operating inside an approved checkpoint/update task.

### Fresh-session Project Map updates

If a chat is long or may have been compacted, the agent should not directly update Project Map from chat recall.

It should produce a checkpoint, handoff, or Project Map delta. The owner can then open a fresh session and apply the update from current Project Map plus approved evidence.

---

## Cursor workflow

The release adds explicit workflow commands so the owner does not need to repeatedly clarify intent:

```text
/answer      answer only
/analyze     analyze only
/plan        produce a scoped task
/apply       perform one scoped change
/checkpoint  capture the stage
/handoff     prepare a fresh-session transfer
/map-delta   propose memory changes
/map-apply   apply approved Project Map changes
/recover     recover from Project Map after context risk
/eval-smoke  run or prepare behavior checks
```

No command means answer-only by default.

---

## Python is not required

Agent Memory Kit is language-agnostic and file-based. Python helper scripts are optional examples only. They are included because the original owner works in Python. Replace them with another language if needed.

---

## Known boundaries

- Rules and commands guide the model; they do not technically sandbox it.
- Hook examples must be adapted to the current Cursor hooks schema before production use.
- Subagents should start read-only until the owner has strong Project Map discipline and verification gates.
- Eval checks still require a manual, scripted, hook-based, CI, or API runner to execute.
