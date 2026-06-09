# Command Vocabulary

Commands make intent explicit. They are safer than vague natural-language phrases.

Do not treat ordinary words as hidden commands. The owner should use slash commands or an explicit mode block when behavior matters.

---

## Modes

| Command | Mode | Mutates files? | Purpose |
|---|---:|---:|---|
| `/answer` | answer | No | Answer from allowed evidence. |
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
