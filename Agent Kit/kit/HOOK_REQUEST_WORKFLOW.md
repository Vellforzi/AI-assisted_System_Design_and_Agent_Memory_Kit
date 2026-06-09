# Hook Request Workflow

This guide defines how an agent should respond when the owner asks for hooks.

## Default behavior

If the owner asks for hooks, the agent should not blindly generate generic scripts.

The agent must first decide whether enough context exists to generate a safe hook package.

## Required context

Minimum information:

- target tool: Codex, Cursor, or another agent tool;
- operating system and shell;
- project root;
- desired enforcement level: warn-only or block;
- source authority for project facts;
- secrets policy;
- database write policy;
- git policy;
- Project Map write policy;
- allowed write scope workflow;
- whether Python, Node, PowerShell, shell, or another runtime is acceptable.

## If information is missing

Ask short questions only for missing safety-critical items.

Do not ask for information that can be read from the project or inferred from existing Project Map and owner instructions.

## If information is sufficient

Generate a project-local package:

```text
.<tool>/
  hooks.json
  hooks/
    <hook scripts>
  README.md
  test_hooks.<cmd-or-sh>
```

For Codex project-local hooks, use:

```text
.codex/
  hooks.json
  hooks/
```

For Cursor hooks, use the structure expected by the current Cursor configuration layer.

## Agent response format

When generating hooks, the agent should include:

- what hooks were generated;
- where to place them;
- how to enable hooks;
- how to test hooks;
- what they block;
- what they do not guarantee;
- whether Python or another runtime is required for the examples.

## Hook safety rule

Hooks are guardrails, not owner approval.

A hook passing does not authorize a mutation.
