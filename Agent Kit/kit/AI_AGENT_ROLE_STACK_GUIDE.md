# AI Agent Role Stack Guide

This guide defines the default owner-controlled multi-agent setup.

## Default role stack

The recommended default is:

```text
Cursor = primary active working hands
Codex = restricted second hands and reviewer
GPT web chat = research, design, architecture, and task specifications
Project Map = shared project truth
Owner = final authority
```

## Cursor role

Cursor is the primary local implementation agent.

Use Cursor for:

- scoped code edits;
- local project navigation;
- tests and verification;
- implementation work;
- Project Map updates only when explicitly approved.

Cursor should have strong project rules and task scope gates.

## Codex role

Codex is the second controlled agent inside or near the IDE.

Default Codex role:

- read-only audit;
- review Cursor diffs;
- challenge assumptions;
- check Project Map consistency;
- recover from context risk;
- propose patches and scopes.

Codex should not be the first broad mutating agent. It may apply changes only under an explicit task contract, narrow scope, approval, and permission guardrails.

Recommended default:

```toml
default_permissions = ":read-only"
approval_policy = "on-request"
```

## GPT web chat role

Use GPT web chat for:

- external research;
- design alternatives;
- architecture comparison;
- task specification drafting;
- long-form analysis;
- synthesis across sources.

Do not use provider chat memory as project truth. Promote reusable findings into Project Map only through owner-approved memory compilation.

## Project Map role

Project Map is the durable project memory and source-of-truth layer.

All agents should treat it as the shared memory boundary.

## Why this split works

It avoids one overloaded agent thread doing everything.

It also prevents a reviewer from having the same assumptions as the implementer:

```text
Cursor implements.
Codex reviews.
GPT researches.
Project Map stores truth.
Owner approves.
```

## Default interaction loop

```text
1. GPT or Cursor creates a scoped task plan.
2. Cursor applies a narrow change.
3. Codex reviews the diff or context.
4. Owner accepts/rejects.
5. Agent proposes Project Map delta.
6. Owner approves map update.
7. Eval trigger is checked.
```
