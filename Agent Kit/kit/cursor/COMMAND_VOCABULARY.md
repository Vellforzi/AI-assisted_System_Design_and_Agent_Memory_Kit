# Command Vocabulary

Commands make intent explicit. They are safer than vague natural-language phrases.

Do not treat ordinary words as hidden commands. The owner should use slash commands or an explicit mode block when behavior matters.

---

## Modes

| Command | Mode | Mutates files? | Purpose |
|---|---:|---:|---|
| `/answer` | answer | No | Answer from allowed evidence. |
| `/ask` | answer/analyze | No | Read-only Ask mode: clarify, explain, compare, no mutation. |
| `/analyze` | analyze | No | Analyze findings, conflicts, risks, missing evidence. |
| `/plan` | plan | No | Produce a scoped task plan. |
| `/apply` | apply | Yes, if scope is explicit | Perform one bounded change. |
| `/checkpoint` | checkpoint | No by default | Produce a checkpoint proposal. |
| `/handoff` | handoff | No by default | Produce a clean-slate handoff for a new chat/session. |
| `/map-delta` | plan | No | Propose Project Map changes. |
| `/map-apply` | apply | Project Map only | Apply approved Project Map delta/handoff. |
| `/recover` | recover | No by default | Recover from Project Map and Working State after context risk. |
| `/eval-smoke` | audit | No by default | Prepare or run lightweight behavior checks. |
| `/failure-case` | repair planning | No by default | Convert an agent failure into a candidate eval case. |
| `/inventory` | read-only audit | No | Inventory project structure and source authority. |
| `/context-advisor` | analyze | No | Preflight context/scope/model/settings gate. |
| `/settings` | analyze | No | Explain surface/model/reasoning/speed/context choice, cost class, escalation trigger, and cheaper alternative. |
| `/models` | analyze | No | Show dated provider/model snapshot and whether the working model set is sufficient. |
| `/scope` | analyze | No | List mandatory/recommended/optional/forbidden context. |
| `/fuel` | analyze | No | Token/fuel plan: keep/defer/drop and Max/IDE context advice. |
| `/safe-apply` | analyze | No | Check mutation safety before an apply task. |
| `/debug` | debug | No by default | Runtime/root-cause preflight; needs logs/tests/schema before apply. |
| `/multitask` | plan | No by default | Split independent tasks only when scopes/checkpoints are safe. |

---

## Explicit mode block

If slash commands are not available, use this block:

```text
Mode: answer | analyze | plan | apply | checkpoint | handoff | map-delta | map-apply | recover | eval-smoke | failure-case | inventory
Scope:
Allowed:
Forbidden:
Expected result:
```

---

## Default behavior

If no command or explicit mode is given, the mode is `answer`.

A question, review request, or analysis request does not authorize file edits, git actions, DB writes, deployment, Project Map writes, or external side effects.

---

## v3.8 commands

### `/scope-set`

Update task write scope after explicit owner approval. This command changes only the scope control file unless a separate apply task is provided.

### `/scope-reset`

Reset task write scope to safe defaults.

### `/workspace-check`

Check whether the active workspace exposes Project Map, agent rules, hooks, and all relevant project components.


## v3.8 settings and context commands

- `/settings-audit` — compare Cursor settings with the owner-controlled defaults. Analyze only unless the owner explicitly asks for apply.
- `/cursorignore-audit` — inspect `.cursorignore` and decide whether Hierarchical Cursor Ignore should be enabled.

These commands do not grant permission to change IDE settings or project files by themselves.

## /codexignore-audit

Inspect `.codexignore` as a Codex context-boundary policy file. Do not edit without explicit apply/scope permission.


## v3.9 Context Advisor commands

- `/context-advisor` — compact preflight gate for task context, scope, surface, model class, and settings.
- `/settings` — explain model/settings choice, cost class, escalation trigger, and cheaper alternative using provider capability snapshots when needed.
- `/models` — show dated model capability snapshot and model-set sufficiency; do not add models without benchmark/failure evidence.
- `/scope` — ask for context classes/refs without loading the whole project.
- `/fuel` — show token/fuel plan and Max/IDE context recommendation.
- `/safe-apply` — gate a later mutation; does not perform the mutation.

These commands do not grant permission to read beyond scope or mutate files.

## v3.9.3 model snapshot vocabulary

- `settings?` must show provider snapshot date/ref when giving exact Cursor model settings.
- `which model?` should choose from the core Cursor set first: Composer 2.5, GPT-5.3 Codex, GPT-5.5, Sonnet 4.6, Opus 4.8, Fable 5.
- Optional models such as Gemini 3.1 Pro or Grok 4.3/Grok Build require a capability gap and owner approval before entering default routing.

## v3.9.3 surface/mode routing vocabulary

- `/ask` maps to read-only answer/analyze. It must not mutate files or expand scope without approval.
- `/debug` maps to root-cause/debug preflight. It should request logs, tests, runtime evidence, schema, and affected files before recommending high reasoning.
- `/multitask` is not a generic speed-up command. It is allowed only for independent tasks with separate scopes, checkpoint/handoff boundaries, and explicit owner acceptance of higher fuel risk.
- `/models` and `/settings` must show the provider snapshot date when giving concrete model advice.
- Codex extension controls and ChatGPT Pro web modes belong to their own surfaces; do not copy them into Cursor settings unless the owner explicitly asks.
