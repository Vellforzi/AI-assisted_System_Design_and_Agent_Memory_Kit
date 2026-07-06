# Codex Integration Owner Guide

This guide explains how to use Codex alongside Cursor under Agent Memory Kit.

Codex is not a replacement for Project Map. Codex is another agent surface that can read the same owner-controlled project memory and follow the same action-intent and source-authority contracts.

For connector-aware work, also read `CODEX_CONNECTOR_POLICY.md`. Connectors are
default-forbidden, reads require exact scope, writes require explicit Allowed
scope and receipts, and outbound messages should be draft-first unless the owner
approves a send/update/delete action in the current task.

For task handoffs, include an Executor Routing Gate. Use
`EXECUTOR_ROUTING_GATE.md` and validate non-trivial contracts with
`tools/verify_executor_routing_gate.py`.

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

---

## v3.8 scope and workspace policy

Codex should normally be configured as the restricted second agent:

```text
Cursor = primary implementation agent
Codex = read-only reviewer, auditor, recovery helper, and second opinion
GPT web chat = research, design, and task specifications
Project Map = shared project truth
```

Recommended Codex defaults:

```toml
approval_policy = "on-request"
default_permissions = ":read-only"
```

Do not ask the owner to manually edit `.codex/ALLOWED_SCOPE.txt` when a safe agent workflow can do it. Use the scope workflow:

1. propose exact write paths;
2. request or verify explicit owner approval;
3. update `.codex/ALLOWED_SCOPE.txt`;
4. apply only the approved task;
5. reset the scope afterwards.

See:

- `SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`
- `CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`
- `WORKSPACE_SELECTION_GUIDE.md`
- `AI_AGENT_ROLE_STACK_GUIDE.md`
- `codex/scope/README.md`


---

## v3.9 Context Advisor workflow

Codex can use the same Context Advisor gate as Cursor. Use `codex/workflows/context-advisor.md` for a read-only preflight before review, audit, recovery, or controlled apply.

Default policy:

- use `:read-only` or equivalent conservative permission first;
- use open files, selections, and `@file` refs only when they are exact scope;
- keep higher reasoning for root-cause debug, audit, repair, or cross-subsystem analysis;
- do not rely on compacted chat or Codex memory as Project Map truth;
- do not apply until owner intent, allowed scope, and verification are explicit.


## Cost-aware model routing

Use the lowest sufficient model/settings class. Do not recommend premium/frontier/high/pro as a generic safety default. Escalate only with a concrete trigger, and show a cheaper alternative when recommending the more expensive route.
