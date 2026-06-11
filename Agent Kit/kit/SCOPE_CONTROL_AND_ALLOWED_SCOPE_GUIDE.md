# Scope Control and ALLOWED_SCOPE Guide

This guide defines how an agent should work with task-level edit scope files such as `.codex/ALLOWED_SCOPE.txt`.

## Core principle

The owner should not have to manually edit scope files when a safe agent workflow can do it.

Manual editing is allowed as an emergency fallback, but the normal workflow is:

1. the owner states an intended action;
2. the agent identifies the minimal write scope;
3. the agent proposes a scope update;
4. the owner explicitly approves the scope update;
5. the agent updates the scope control file;
6. the agent performs only the approved task;
7. the agent resets the scope back to a safe default.

Scope control is not permission by itself. It is a technical whitelist that supports an approved task contract.

If no runtime, wrapper, or agent client actually reads and enforces the scope file, the scope file is advisory. It is still useful as a policy artifact and review checklist, but the agent must not describe it as filesystem protection.

## Required distinction

- `Task Contract`: what the owner asked the agent to do.
- `Allowed Scope`: what file paths the agent may write during that task.
- `Permission Profile`: what the tool runtime can technically read or write.

All four layers should agree before mutation.

## Default rule

If the current prompt is a question, analysis request, review request, planning request, or context-gathering request, the agent must not change `ALLOWED_SCOPE.txt`.

The agent may propose the scope that would be needed for a later apply task.

## When the agent may update ALLOWED_SCOPE.txt

The agent may update `.codex/ALLOWED_SCOPE.txt` only when all conditions hold:

1. the owner explicitly requested an apply-capable workflow such as `/scope-set`, `/apply`, or `/map-apply`;
2. the task has a target and a minimal write scope;
3. the proposed paths are inside the active workspace root;
4. the paths do not include secrets, `.git/`, `.codex/` internals, credential stores, or unrelated project areas;
5. the agent reports the proposed scope before writing it;
6. owner approval is explicit or the current task contract already allows this exact scope update.

## Safe reset

After an apply task, the agent must propose or perform a scope reset according to the active mode.

Recommended safe default:

```text
AGENTS.md
PROJECT_AI_BRIEF.md
docs/**
Project Map/**
```

Product code should not be part of the default write scope. Add exact files only for the specific apply task.

## Scope update workflow

Use this pattern:

```text
/scope-set
Task: <one concrete task>
Allowed writes:
- <exact path or narrow glob>
Forbidden:
- secrets
- DB writes
- git push
- deploy
- unrelated files
After task: reset scope to safe default
```

Expected agent behavior:

1. validate that the request is explicit;
2. reject broad or unsafe paths;
3. write `.codex/ALLOWED_SCOPE.txt` only if approved;
4. show the resulting scope;
5. continue to the apply task only if the task contract is valid.

## Broad globs

Broad globs are allowed for read-only analysis but discouraged for writes.

Avoid:

```text
Options_api/**
Options_scraper/**
Options_MT/**
```

Prefer exact files:

```text
Options_api/app/routes/option_chain.py
docs/ROUTES_REFERENCE.md
```

## Missing scope

If the owner asks the agent to apply changes but no scope exists, the agent must stop and ask for scope or propose a narrow scope for approval.

The agent must not guess the target from chat memory.

## Relationship to Project Map updates

Project Map writes require a separate approval gate.

`ALLOWED_SCOPE.txt` may include `Project Map/**`, but that does not authorize memory updates by itself. The owner must still request `/map-apply` or provide an equivalent explicit task contract.
