# Cursor Integration Owner Guide

Purpose: explain how to use Agent Memory Kit inside Cursor through Rules, Commands, Skills, Subagents, and optional Hooks.

This guide is written for a project owner who wants high control, short working loops, and no hidden autonomous behavior.

---

## Plain-language model

Use Cursor surfaces like this:

| Cursor surface | What it should do | What it should not do |
|---|---|---|
| Rules | Always-on safety and memory rules. | Store the whole Project Map or long guides. |
| Commands | Start a known workflow such as `/answer`, `/apply`, `/checkpoint`, or `/handoff`. | Act as vague magic words without scope. |
| Skills | Store reusable procedures that are too long for always-on Rules. | Become uncontrolled write permissions. |
| Subagents | Run focused read-only audits in one area. | Mutate code, git, DB, deploy, or Project Map by default. |
| Hooks | Add technical checks around dangerous actions. | Replace owner review or project tests. |

---

## Recommended Cursor setup

Minimum useful setup:

```text
.cursor/
  rules/
    agent_memory_core.mdc
    platform_context_compaction_boundary.mdc
    option_profit_safety.mdc

Agent Kit/
  kit/
    cursor/
      commands/
      skills/
      subagents/
      hooks/
```

Then create or paste the command bodies into Cursor Commands:

- `/answer`
- `/analyze`
- `/plan`
- `/apply`
- `/checkpoint`
- `/handoff`
- `/map-delta`
- `/map-apply`
- `/recover`
- `/eval-smoke`
- `/failure-case`
- `/inventory`
- `/context-advisor`
- `/settings`
- `/scope`
- `/fuel`
- `/safe-apply`

Do not rely on ordinary words such as "do it" or "continue" to switch modes. Use explicit commands when behavior matters.

---

## Practical owner workflow

A safe controlled loop:

```text
/answer or /analyze
  collect context and understand the task;

/plan
  produce a scoped task for Cursor;

/apply
  perform one bounded change;

/checkpoint or /handoff
  capture the stage before the chat becomes long;

/map-apply in a fresh session
  update Project Map from approved delta/handoff;

/eval-smoke
  check whether behavior rules still hold after rule/kit changes.
```

---

## Do not overload Rules

Rules should be short. A large always-loaded rule wastes context and can create instruction conflicts.

Keep in Rules:

- answer-only default;
- Project Map authority;
- Source Authority conflict rule;
- platform-summary boundary;
- mutation gates;
- response footer.

Keep in Skills or guides:

- memory compilation procedure;
- checkpoint procedure;
- handoff procedure;
- eval-case building;
- source-authority audit;
- adoption guides.

---

## Suggested response footer

For non-trivial work, ask Cursor to end with:

```text
Mode:
Scope:
Files changed:
Evidence:
Project Map delta: yes/no
Checkpoint suggested: yes/no
Eval trigger: yes/no
Next safe step:
```

This makes it harder for important state changes to disappear inside a long chat.

---

## Optional hooks

Hooks are useful when the host tool supports script execution at specific points in the agent lifecycle.

Use hooks to catch:

- possible secrets;
- dangerous git commands;
- database writes;
- edits outside allowed scope;
- unauthorized Project Map writes.

The hook scripts in `cursor/hooks/scripts/` are examples. Agent Memory Kit does not require Python. The examples are Python because the original owner works in Python and Python is convenient for portable local scripts. Replace them with shell, Node.js, PowerShell, Go, or any language that fits your environment.

Always verify the current Cursor hook schema before wiring `hooks.json.example` into a real project.

---


### Implicit IDE context boundary

Cursor may expose open tabs, selections, diagnostics, terminal snippets, or workspace state depending on UI settings. Treat that context as advisory only unless it is explicitly scoped or owner-approved. If the agent needs it to expand read/apply scope, it must report the needed paths/classes and ask approval first. It must not use implicit IDE context to expand write scope.

## v3.8 workspace and scope policy

For a multi-component project with one Project Map, prefer one shared workspace root.

Example:

```text
JOB/
  Project Map/
  Options_api/
  Options_scraper/
  Options_MT/
  docs/
  db_sql/
  .cursor/
  .codex/
```

Opening only `Options_api/` or only `Options_scraper/` may hide the Project Map and cross-component source authority from the agent.

Use task scope, not workspace fragmentation, as the main safety boundary.

New recommended commands:

- `/workspace-check` — read-only check of active workspace root and Project Map visibility.
- `/scope-set` — update the task write whitelist after explicit approval.
- `/scope-reset` — return the write whitelist to a safe default.

See `WORKSPACE_SELECTION_GUIDE.md` and `SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`.


## Cursor Agent settings profile

For owner-controlled work, install Rules and Commands first, then use the settings profile in:

```text
cursor/CURSOR_OWNER_CONTROLLED_DEFAULTS.md
cursor/settings/owner_controlled_profile.yaml
```

The recommended profile treats Cursor as active implementation hands, not as an unrestricted autonomous worker.

Core defaults:

- `Run Everything` is not allowed as the default run mode.
- Use Auto-review or stricter execution mode.
- Keep Browser Protection, MCP Tools Protection, File-Deletion Protection, and External-File Protection on.
- Keep Auto-Approve Mode Transitions off.
- Keep Auto-Accept Web Search off.
- Keep Usage Summary visible.
- Keep Auto Format on Agent Finish off.
- Enable Hierarchical Cursor Ignore only after `.cursorignore` is audited.

Use `/settings-audit` when the owner wants the agent to explain or check Cursor settings.
Use `/cursorignore-audit` before enabling Hierarchical Cursor Ignore.


---

## v3.9 Context Advisor workflow

Use Context Advisor when the owner may not know the correct scope or model/settings in advance.

Recommended loop:

```text
/context-advisor
  classify task, missing context, route/settings;

/scope or /fuel
  refine context/fuel before loading broad files;

/plan
  produce exact task contract;

/safe-apply
  verify mutation gate;

/apply
  perform one bounded change only after explicit owner approval.
```

Cursor defaults for advisor-guided work:

- Max Mode off first.
- Include IDE Context off unless exact open files are scoped and owner-approved; implicit IDE context is advisory only.
- Plan Mode on for multi-file/root-cause/debug/audit.
- Standard speed for risky or verification-heavy work.
- Medium reasoning for bounded edits; high reasoning for cross-subsystem/audit/repair/package design.


## Cost-aware model routing

Use the lowest sufficient model/settings class. Do not recommend premium/frontier/high/pro as a generic safety default. Escalate only with a concrete trigger, and show a cheaper alternative when recommending the more expensive route.
