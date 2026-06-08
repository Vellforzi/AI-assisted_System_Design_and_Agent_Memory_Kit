# AGENTS.md — Agent Memory Kit Repository Entrypoint

Purpose: route repository-aware agents to the Project Map and enforce safe default behavior.

## Core contract

- The Project Map is the source of durable project memory.
- Built-in model knowledge is not project-specific truth.
- Answer-only is the default intent.
- Reading context is not permission to mutate files, memory, git state, databases, deployments, or external systems.
- If project evidence is missing, say so. Do not invent project facts.

## Read order for project questions

1. `Project Map/README.md`
2. `Project Map/current_state.md`
3. `Project Map/working_state.yaml`
4. `Project Map/source_authority.yaml`
5. `Project Map/permissions_policy.yaml`
6. `Project Map/retrieval_policy.yaml`
7. Active task contract in `Project Map/tasks/` if the user references one.
8. Relevant memory index and cards under `Project Map/memory/`.
9. Relevant project files only after source authority and component scope are clear.

## Intent and permissions

Classify each owner request before acting:

- `answer`: answer only; no mutation.
- `analyze`: read and reason only; no mutation.
- `plan`: propose steps only; no mutation.
- `retrieve_context`: gather scoped context only.
- `stage`: prepare proposed changes only when explicitly requested.
- `apply`: modify only explicitly scoped files after owner request.
- `external_research`: use external sources only when allowed and separate external facts from project facts.

If the owner asks a question, remain in `answer` or `analyze` mode.

## Forbidden without explicit owner approval

- Editing files.
- Updating Project Map memory.
- Running shell commands.
- Running tests that mutate state.
- Git add/commit/push/reset/merge/rebase.
- Database reads or writes unless explicitly scoped; writes require explicit approval.
- Deploying or restarting services.
- Accessing secrets.
- Browsing external web sources for project truth.
- Reading the whole repository or whole Project Map by default.

## Project-specific grounding

For every project-specific claim, use evidence from:

- current owner input;
- Project Map;
- opened project files;
- tool outputs from the current run;
- owner-approved memory.

If evidence conflicts, follow `Project Map/source_authority.yaml` and label the conflict.

## Significant work and eval triggers

At the end of any meaningful project task, check whether work was significant using `Project Map` policy or `Agent Kit/kit/SIGNIFICANT_WORK_AND_CHECKPOINTS.md`.

Significant work includes changes or verified discoveries involving project state, facts, decisions, files, verification, risks, permissions, side effects, memory lifecycle, continuity, or repeated failures.

If significant work occurred, propose any needed Project Map delta, checkpoint, handoff, or eval trigger. Do not apply these updates unless the owner explicitly asks.

Eval triggers include instruction changes, Project Map policy changes, model/client/tool changes, critical or repeated failures, stale-fact misuse, unauthorized action, or side-effect safety issues.

## End-of-work output

For implementation tasks, finish with:

- files read;
- files changed;
- tests or checks run;
- risks or unresolved claims;
- proposed Project Map updates;
- checkpoint or handoff need;
- eval trigger: yes/no and why;
- side effects performed and receipt IDs if applicable.

Do not update Project Map unless the owner explicitly asks.
