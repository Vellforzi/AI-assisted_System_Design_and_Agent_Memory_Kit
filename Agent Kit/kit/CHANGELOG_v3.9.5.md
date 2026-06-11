# Agent Memory Kit v3.9.5 — Context Compaction Control micro-patch

Release date: 2026-06-10
Status: patch overlay; live repo merge must be done by Cursor/owner.

## Purpose

v3.9.5 adds owner-controlled context compaction for long-running agent sessions. The goal is to intentionally reduce active context pressure while preserving replay-critical state and preventing platform summaries from becoming project truth.

## Added

- `context_compaction_control_policy.md`
- `PLATFORM_CONTEXT_COMPACTION_BOUNDARY.md` v3.9.5 wording
- Cursor command `/amk-context-compact`
- Context Advisor rule additions for compaction plan/gate
- Eval category `context_compaction_control`
- Eval cases `AMK-CC-001..003`

## Key rules

- The agent cannot assume it can directly delete arbitrary host chat history.
- Platform summaries are non-authoritative hints.
- Agent-created summary/compact/checkpoint requires a CompactionPlan and owner approval unless inside an approved checkpoint/update task.
- Prefer clearing/excluding old re-fetchable tool outputs before whole-transcript summary.
- Preserve Working State refs, source authority, evidence refs, validation summaries, receipts, unsafe-to-repeat actions, and next safe step.
- Do not put secrets, raw dumps, unsupported facts, stale facts as current truth, or hidden chain-of-thought into summary payloads.
