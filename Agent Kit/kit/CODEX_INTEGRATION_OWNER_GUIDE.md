# Codex Integration Owner Guide

This guide explains how to use Codex alongside Cursor under Agent Memory Kit.

Codex is not a replacement for Project Map. Codex is another agent surface that can read the same owner-controlled project memory and follow the same action-intent and source-authority contracts.

## Recommended role split

```text
Cursor Agent:
  primary local implementation work;
  scoped apply tasks;
  repository diffs and local verification;
  Project Map updates only when explicitly authorized.

Codex:
  independent review;
  read-only audit;
  alternative design analysis;
  checkpoint and handoff validation;
  recovery after context-compaction risk;
  narrow apply tasks only with explicit scope and approval.

Project Map:
  the shared project truth for both Cursor and Codex.
```

## Core rule

Codex must follow the same memory boundary as any other agent:

```text
Project Map = project truth
Working State = recovery root
Source Authority = conflict resolver
Task Contract = permission boundary
Provider memory and platform summaries = non-authoritative hints
```

## Recommended Codex defaults

Start Codex in a conservative posture:

- Standard speed.
- Pragmatic personality.
- Read-only default permissions.
- Approval prompts enabled.
- Codex memories disabled for project truth.
- Hooks enabled.
- Context window usage visible.
- Follow-ups queued, not steering by default.
- Detached code review for serious review.

## Minimal setup sequence

1. Configure `~/.codex/config.toml` using the templates in `codex/config/`.
2. Add a project-level `.codex/hooks.json` if you want repository-local hooks.
3. Add hook scripts under `<repo>/.codex/hooks/`.
4. Add project `AGENTS.md` at the repository root.
5. Keep Project Map in the repository or workspace root.
6. Restart Codex after changing global config.
7. Run a small read-only audit first.

## When to use Codex

Use Codex for:

- independent review of Cursor-generated diffs;
- read-only audits of API, scraper, database, MetaTrader, and docs;
- checking whether a Project Map delta is properly evidenced;
- turning repeated failures into eval cases;
- preparing a handoff before starting a fresh session;
- recovering after context compaction.

Avoid using Codex for:

- unsupervised long-running work;
- broad repository edits without a task contract;
- DB writes;
- deploys;
- git push;
- secret handling;
- Project Map writes without `/map-apply` or explicit owner approval.

## Context compaction rule

If Codex is about to compact the conversation, it should stop and ask for a checkpoint or handoff first. The optional `pre_compact_checkpoint_guard.py` hook implements that behavior for auto-compaction.

If compaction has already happened, Codex must treat the platform-generated summary as a weak hint only and recover from Project Map and Working State.

## Practical workflow

```text
1. Cursor performs a scoped implementation task.
2. Codex reviews the diff in detached review mode.
3. Owner decides what to accept.
4. Cursor applies fixes.
5. Codex or Cursor proposes Project Map delta.
6. Owner approves `/map-apply` in a fresh or low-context session.
7. Run eval smoke if behavior rules or repeated failures changed.
```

## Python is optional

Agent Memory Kit does not require Python. Python hook scripts are examples only. Replace them with PowerShell, shell, Node.js, Go, Rust, or any other toolchain if that is better for your environment.
