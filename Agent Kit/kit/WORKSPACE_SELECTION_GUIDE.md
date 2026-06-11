# Workspace Selection Guide

This guide explains how to choose a workspace for agent-assisted work.

## Core idea

The workspace is the agent's visible project perimeter.

It affects:

- what files the agent can see;
- where project instructions are discovered;
- where config is loaded;
- what paths are considered workspace roots;
- what Project Map is available;
- what files may be included in searches and edits.

## Recommended default

For one project with multiple components, open the shared project root as one workspace.

Example:

```text
JOB/
  AGENTS.md
  PROJECT_AI_BRIEF.md
  Agent Kit/
  Project Map/
  docs/
  db_sql/
  Options_api/
  Options_scraper/
  Options_MT/
  .cursor/
  .codex/
```

In this case, the recommended Cursor workspace root is `JOB/`, not only `Options_api/` or `Options_scraper/`.

## Why one root is safer here

Opening only a component folder can hide project memory and cross-component source authority from the agent.

For Agent Memory Kit, that is usually worse than a larger workspace because the agent may see code but miss the Project Map.

A large workspace is acceptable when task scope is strict.

Bad:

```text
Fix whatever is needed across API and scraper.
```

Good:

```text
/analyze
Scope:
- Options_api/app/routes/
- Options_scraper/app/main.py
- docs/SCRAPER_CACHE_MATRIX.md
Forbidden:
- edits
- DB writes
- git push
```

## When to use multiple workspaces

Use separate workspaces only when:

- they are genuinely different projects;
- you need physical visibility isolation;
- you are working in separate git worktrees;
- you intentionally want a component-only view;
- the task does not require the Project Map.

## Parallel component work

For read-only analysis across API and scraper, use one workspace and one scoped task.

For parallel apply work, prefer git branches or worktrees, not hidden workspace fragmentation.

Use separate chats or runs with separate task contracts:

```text
Run A: API task, scoped to API files.
Run B: scraper task, scoped to scraper files.
Shared: Project Map updates only after explicit merge/review.
```

## Workspace file template

A `.code-workspace` file can store folder roots and workspace settings. Place it in the project root and open it from Cursor.

For a single root project, use a folder path of `.`.

See:

```text
cursor/workspaces/OPTION_PROFIT_JOB.code-workspace.example
```


## Authoritative existing workspace rule

If Project Map, `AGENTS.md`, `current_state`, source authority, or existing project docs reference a specific `.code-workspace` file, the agent must treat that file as the primary workspace.

The agent must not replace it with a generated fallback workspace.

The agent may only:

- inspect it;
- explain it;
- compare it with a proposed template;
- suggest a patch;
- create a fallback workspace only if no authoritative workspace exists or the owner explicitly asks for a fallback.

For existing projects, workspace generation is a last resort. Workspace audit comes first.
