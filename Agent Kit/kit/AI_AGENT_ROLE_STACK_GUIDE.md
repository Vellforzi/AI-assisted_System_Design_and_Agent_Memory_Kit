# AI Agent Role Stack Guide

This guide defines owner-controlled agent role profiles.

## Default role stack

The recommended multi-agent default is:

```text
Cursor = primary active working hands
Codex = restricted second hands and reviewer
GPT web chat = research, design, architecture, and task specifications
Project Map = shared memory boundary; truth role follows source authority
Owner = final authority
```

This is not mandatory for every project. A mature solo project may use Codex or another local coding agent as the primary implementer when the task has explicit intent, scope, and verification.

Do not downgrade a working local coding agent into reviewer-only mode unless that role split solves a real risk.

---

## Supported role profiles

| Profile | Use when | Allowed behavior |
|---|---|---|
| `single-agent-local-implementer` | One local coding agent is the practical primary worker. | Read, edit, and verify inside explicit task scope. |
| `codex-reviewer` | Codex is used as independent audit or recovery surface. | Read-only review by default; propose patches and scope. |
| `cursor-implements-codex-reviews` | Cursor is primary implementer and Codex is second opinion. | Cursor applies scoped changes; Codex reviews diff and memory drift. |
| `research-only-agent` | The task is external/domain research or architecture comparison. | No repository mutation; research output is not project truth until promoted. |

Role profile does not create action intent. Permission policy, source authority, and current owner instruction still apply.

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

Codex can be the second controlled agent inside or near the IDE.

Default Codex role:

- read-only audit;
- review Cursor diffs;
- challenge assumptions;
- check Project Map consistency;
- recover from context risk;
- propose patches and scopes.

Codex should not be the first broad mutating agent. In the `single-agent-local-implementer` profile it may apply changes, but only under an explicit task contract, narrow scope, approval, and permission guardrails.

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

Project Map is the durable project memory layer.

All agents should treat it as the shared memory boundary. If the project declares Project Map as secondary memory, operational docs, specs, tests, code, issues, and current owner instructions remain authoritative.

## Why this split works

It avoids one overloaded agent thread doing everything.

It also prevents a reviewer from having the same assumptions as the implementer:

```text
Cursor implements.
Codex reviews.
GPT researches.
Project Map stores memory, and stores truth only when the project's source authority assigns that role.
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

For v5 review work, the reviewer receives the result or diff, acceptance criteria, and intentional-decision refs, but not the author's reasoning history. The reviewer must not mutate or repair. Significant delivery uses a fresh-context receipt; high or irreversible delivery uses an adversarial receipt. Any repair is a separate owner-authorized task.
