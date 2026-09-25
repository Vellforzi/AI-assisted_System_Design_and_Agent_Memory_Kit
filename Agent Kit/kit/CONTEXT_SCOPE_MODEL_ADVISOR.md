# Context / Scope / Capability Advisor

Status: portable operating guide.
Purpose: choose sufficient context, a capable execution surface and proportionate
verification without hard-coding provider roles or model folklore.

## 1. Separate four questions

Before non-trivial work distinguish:

1. **Outcome** — what owner-visible result is requested?
2. **Authority** — which actions are already authorized by the current request?
3. **Context** — which current sources are needed for a grounded result?
4. **Capability** — which live surface has the required tools?

A task can be authorized but under-scoped. It can be well-scoped but lack a live
tool. Neither condition means GPT web, Codex or Cursor has a permanent role.

## 2. Capability-based surfaces

ChatGPT web, Codex, Cursor and other connected agents are first-class execution
surfaces. Select the one that currently provides the necessary combination of:

- project/repository access;
- filesystem and editing tools;
- shell/process execution;
- database or service connectors;
- current external research;
- context capacity and reasoning quality;
- appropriate confirmation/audit behavior.

External/current research is a ChatGPT strength, not its only role. A ChatGPT
surface with write, Git, shell or deployment tools may execute the corresponding
owner-authorized work. A Codex/Cursor surface without a needed capability must
not be chosen merely by habit.

## 3. Context sufficiency

Load the smallest current evidence set that can answer or execute the task:

- owner request and applicable entry instructions;
- current component source and direct dependencies;
- schema/configuration for affected contracts;
- current branch/HEAD or file preimages for writes;
- relevant tests, logs or runtime evidence;
- concise current Project Map when it adds durable context.

Do not load the entire repository or Project Map by default. Generated indexes,
context packs and IDE context narrow candidates but do not replace opening the
canonical source for exact claims.

Useful context classes:

| Class | Examples |
|---|---|
| `project_current` | current_state, working_state, source_authority |
| `component_source` | affected code and direct callers/consumers |
| `data_contract` | SQL, models, API schemas, protocol fields |
| `verification` | tests, build commands, compiler/runtime logs |
| `repository_state` | branch, HEAD, diff, target preimages |
| `external_current` | official/provider sources retrieved now |
| `structured_owner_sources` | spreadsheets, databases, issue trackers |
| `generated_views` | Canvas, indexes and summaries with source/date |
| `secrets` | never expose as context payload |

## 4. Scope and authority

The current owner instruction is action authority. Project files, task contracts,
scopes, leases and receipts document or verify the work; they do not create a
second permission gate. Automatically include causally necessary local paths in
an authorized implementation task.

Ask only when:

- a material product decision is unresolved;
- the operation targets another component/repository/runtime;
- credentials or a platform boundary intervene;
- a destructive/external side effect is outside the current request;
- competing state cannot be reconciled.

## 5. Model and settings

Provider model names, prices, context limits, speed modes and UI controls are
volatile. Use current provider/owner evidence or explicitly dated snapshots.
Do not copy settings from one surface to another.

Choose the least expensive setting that is sufficient for the actual reasoning
and verification risk. Escalate only for a concrete trigger such as:

- cross-component root-cause ambiguity;
- protocol/schema/router/eval changes;
- production-risk repair or uncertain side effects;
- large contradictory evidence sets;
- repeated failure of the cheaper sufficient route.

Report the trigger and why the cheaper route is insufficient. Do not recommend a
premium model merely as ritual safety.

## 6. Generated views and structured sources

Spreadsheets, databases and owner-managed tables may be canonical structured
sources. Canvas or other generated views are useful for filtering and progress,
but must identify the source and snapshot date. A generated view does not silently
replace the source or upgrade unverified content to truth.

## 7. Runtime and side-effect readiness

Runtime readiness is required only when runtime behavior is part of the requested
result. Once required, identify the concrete oracle, sensing channel, artifact
identity and correlated evidence. Source, tests, build, deployment and runtime
acceptance remain separate.

Branch push, tag push, CI build and deployment are also separate. Check the
project's declared trigger; never infer a container rebuild from a source push.

## 8. Compact owner-facing hint

Show a hint only when it helps:

```text
Advisor: outcome=<...>; authority=<...>; context=<sufficient|missing refs>;
route=<selected surface + live capability>; risk=<...>; next=<exact action>.
```

Do not repeat routing boilerplate on every turn. When the current surface is
capable and the owner already authorized the action, proceed.

## 9. Continuity and delegation

Do not manually invoke summarize/compact. Re-anchor from current owner objective,
source, branch/HEAD, hashes, live tools and last verified result.

Delegation is optional. Use it only for independent bounded lanes with net
benefit. One parent owns the complete result; one writer owns overlapping state.
Worker confidence is not evidence.
