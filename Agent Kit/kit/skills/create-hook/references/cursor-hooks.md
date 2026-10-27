# Cursor hooks

Mandatory before applying Cursor-specific paths, events, matchers or examples.
Use with [the core](../SKILL.md); these examples do not configure Codex or
authorize activating a hook, restarting a client or running external actions.

## Scope and paths

- **Project hooks**: `.cursor/hooks.json` and `.cursor/hooks/*`
- **User hooks**: `~/.cursor/hooks.json` and `~/.cursor/hooks/*`

Path behavior matters:

- **Project hooks** run from the project root, so use paths like `.cursor/hooks/my-hook.sh`
- **User hooks** run from `~/.cursor/`, so use paths like `./hooks/my-hook.sh` or `hooks/my-hook.sh`

Prefer project scope for behavior shared through the repository; publication
still requires authority. Verify the execution host: desktop examples do not
establish cloud support or access to local user configuration.

## Events and chooser

Choose the narrowest supported event. This retained list is a selection aid,
not a claim that every listed event is available on every Cursor surface.

### Common Agent events

- `sessionStart`, `sessionEnd`: set up or audit a session
- `preToolUse`, `postToolUse`, `postToolUseFailure`: work across all tools
- `subagentStart`, `subagentStop`: control or continue Task/subagent workflows
- `beforeShellExecution`, `afterShellExecution`: gate or audit terminal commands
- `beforeMCPExecution`, `afterMCPExecution`: gate or audit MCP tool calls
- `beforeReadFile`, `afterFileEdit`: control file reads or post-process edits
- `beforeSubmitPrompt`: validate prompts before they are sent
- `preCompact`: observe context compaction
- `stop`: handle agent completion
- `afterAgentResponse`, `afterAgentThought`: track agent output or reasoning

### Tab events

- `beforeTabFileRead`: control file access for inline completions
- `afterTabFileEdit`: post-process edits made by Tab

### Quick event chooser

- **Block or approve shell commands** -> `beforeShellExecution`
- **Audit shell output** -> `afterShellExecution`
- **Format files after edits** -> `afterFileEdit`
- **Block or rewrite a specific tool call** -> `preToolUse`
- **Add follow-up context after a tool succeeds** -> `postToolUse`
- **Control whether subagents can run** -> `subagentStart`
- **Chain subagent loops** -> `subagentStop`
- **Check prompts for secrets or policy violations** -> `beforeSubmitPrompt`
- **Protect MCP calls** -> `beforeMCPExecution`

## Configuration

Create a `hooks.json` file with schema version 1:

```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [
      {
        "command": ".cursor/hooks/format.sh"
      }
    ]
  }
}
```

Each hook definition can include:

- `command`: shell command or script path
- `type`: `"command"` or `"prompt"` (defaults to `"command"`)
- `timeout`: timeout in seconds
- `matcher`: filter for when the hook runs

- `failClosed`: block process failures such as crashes, timeouts, nonzero
  failure exits or missing output. Permission hooks already block invalid JSON
  or schema-invalid responses even when this option is false.
- `loop_limit`: mainly for `stop` and `subagentStop` follow-up loops

## Matchers

Use matchers to avoid running the hook on every event.

- `preToolUse` / `postToolUse` / `postToolUseFailure`: match on tool type such as `Shell`, `Read`, `Write`, `Task`, or MCP tools in `MCP: ...` form
- `subagentStart` / `subagentStop`: match on subagent type such as `generalPurpose`, `explore`, or `shell`
- `beforeShellExecution` / `afterShellExecution`: match on the full shell command string
- `beforeReadFile`: match on tool type such as `Read` or `TabRead`
- `afterFileEdit`: match on tool type such as `Write` or `TabWrite`
- `beforeSubmitPrompt`: matches the value `UserPromptSubmit`

Do not assume POSIX/grep regex syntax. The prior guidance uses JavaScript-style
patterns: avoid `[[:space:]]` and prefer the supported equivalent such as `\s`.
The current official page describes regex matchers without specifying the engine;
verify any nontrivial syntax and the actual event match target on the installed host.

- If the matcher is at all tricky, start by getting the hook working without one or with a very simple matcher, then tighten it after the hook is confirmed to load and fire

If the user wants a hook for only one risky command family, prefer script-side filtering for the first working version and add a matcher afterward only if it is simple and clearly correct.

Simplify only in a safe test context; do not remove an active protection merely
to discover whether a hook loads.

## Command hooks

Command hooks receive JSON on stdin and can return JSON on stdout. Verify the
interpreter, launcher, working directory and every helper in the real hook
environment, including jq, Python, Node and repo-local CLIs. Do not assume their
presence from another shell. Directly executed shell scripts need a valid shebang
and executable permission; interpreter-launched Windows scripts need the matching
launcher rather than a mechanically applied Unix chmod step.

- Exit `0` means success; use the event's supported response schema. An invalid
  permission response blocks the action rather than becoming implicit permission.
- Exit `2` intentionally blocks the action, equivalent to deny.
- Other nonzero exits normally fail open unless `failClosed: true` applies.
- A helper failure hidden by a successful allow response cannot be caught by
  the outer failure policy. Propagate it instead.

### Minimal project-level example

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": ".cursor/hooks/approve-network.sh",
        "matcher": "curl|wget|nc ",
        "failClosed": true
      }
    ]
  }
}
```

```bash
#!/bin/bash
input=$(cat) || exit 2
command=$(printf '%s' "$input" | jq -r '.command // empty') || exit 2

if [[ "$command" =~ curl|wget|nc ]]; then
  echo '{
    "permission": "ask",
    "user_message": "This command may make a network request. Please review it before continuing.",
    "agent_message": "A hook flagged this shell command as a possible network call."
  }'
  exit 0
fi

echo '{ "permission": "allow" }'
exit 0
```

The example's `curl|wget|nc` substring check is illustrative, not a complete
shell parser or network-security policy. Its matcher and script do not define
product policy. The two error checks prevent failed input reads or jq execution
from falling through to successful allow. Confirm jq availability before use;
this example is not installed as a live hook by reading this skill.

## Prompt hooks

Use only when supported on the selected Cursor surface.

Prompt hooks are useful when the policy is easier to describe than to script.

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "type": "prompt",
        "prompt": "Does this command look safe to execute? Only allow read-only operations. Here is the hook input: $ARGUMENTS",
        "timeout": 10
      }
    ]
  }
}
```

Use prompt hooks for lightweight policy decisions. Prefer command hooks when the logic must be deterministic or when the user needs exact, auditable behavior.

## Event outputs

Use the event's supported output fields only.

- `preToolUse`: can return `permission`, `user_message`, `agent_message`, and `updated_input`
- `postToolUse`: can return `additional_context`; for MCP tools it can also return `updated_mcp_tool_output`
- `subagentStart`: can return `permission` and `user_message`
- `subagentStop`: can return `followup_message`
- `beforeShellExecution` / `beforeMCPExecution`: can return `permission`, `user_message`, and `agent_message`

When the user wants to rewrite a tool call, prefer `preToolUse`. When they want to gate only shell commands, prefer `beforeShellExecution`.

Verify the exact event schema and supported operations for the target surface;
field names in an example do not prove that the operation is implemented there.

## Troubleshooting

Cursor watches hooks.json and reloads configuration on save. If loading still
fails, first inspect Cursor's Hooks diagnostics (the Hooks tab in Customize and
Hooks output channel), source paths, schema and matcher parsing. Recheck project
paths against the project root and user paths against ~/.cursor/.

If needed, simplify a matcher in a safe test context and confirm loading/firing
before tightening it. Verify each external executable with command -v or the
platform equivalent in the hook environment. Use failClosed when failures must
block and exit 2 for an intentional denial. Restart Cursor only within current
authority when the remaining loading issue requires it. Do not transfer these
Cursor reload/UI instructions to Codex or silently re-enable a disabled hook.

## Sources and correction boundaries

Official pages read on 2026-10-27:
- [Cursor Hooks](https://cursor.com/docs/hooks): paths, event contracts, failure
  handling and Cursor reload/diagnostics. Recheck when host/version changes.
- [Codex Hooks](https://learn.chatgpt.com/docs/hooks): separate configuration,
  handler and trust contracts; use $openai-docs for Codex work. At that snapshot,
  command and mcp_tool handlers are supported; prompt/agent handlers are parsed
  but skipped. This does not change any installed hook.

Compared with the old core, the Cursor/Codex reload and diagnostic attribution,
permission-response failure semantics, swallowed Bash errors and platform-specific
executability requirements are explicitly corrected. All current hook configuration,
enabled/trust state and native attachment still require independent verification.
