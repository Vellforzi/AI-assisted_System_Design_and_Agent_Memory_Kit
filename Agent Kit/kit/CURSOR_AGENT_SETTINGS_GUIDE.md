# Cursor Agent Settings Guide

This guide defines the recommended Cursor Agent settings for owner-controlled projects that use Agent Memory Kit.

The goal is not maximum autonomy. The goal is controlled implementation work: explicit task, explicit scope, visible context usage, protected tools, and reviewable diffs.

## Recommended default profile

Use this profile when Cursor is the primary local implementation agent.

| Area | Setting | Recommended default | Reason |
|---|---|---|---|
| Agents | Text Size | Default | UI preference only. |
| Agents | Submit with Ctrl + Enter | On | Prevents accidental submission of incomplete task contracts. |
| Agents | Max Tab Count | 5 | Enough parallel context without losing control. |
| Agents | Queue Messages | Send after current message | Follow-ups should not unexpectedly steer the active run. |
| Agents | Usage Summary | Always | The owner must see context usage and checkpoint before context risk. |
| Agents | Agent Autocomplete | On | Helpful prompting aid; not a permission. |
| Agents | Auto-Approve Mode Transitions | Off | The agent must not silently switch from planning to acting. |
| Subagents | Explore subagent model | Fast model acceptable | Exploration should stay read-only unless explicitly changed. |
| Agent Review | Start Agent Review on Commit | Off | Avoid hidden automatic work after each commit. Run review intentionally. |
| Agent Review | Include Submodules | Off unless `.gitmodules` exists | Avoid irrelevant or nonexistent submodule context. |
| Agent Review | Include Untracked Files | On | New agent-created files must be included in review. |
| Agent Review | Default Approach | Quick | Use thorough review only for critical diffs, release gates, or risky changes. |
| Context | Web Search Tool | On | Useful for external docs and libraries, not for project truth. |
| Context | Auto-Accept Web Search | Off | External research should not be silently accepted. |
| Context | Web Fetch Tool | On | Useful for explicit URLs. |
| Context | Hierarchical Cursor Ignore | On only after root `.cursorignore` is verified | Good for reducing noise, unsafe if it hides project memory. |
| Context | Ignore Symlinks in Cursor Ignore Search | Off | Enable only for projects with many symlinks and verified ignore coverage. |
| Execution | Run Mode | Auto-review or stricter; never Run Everything | Actions must be classified, allowlists respected, and protections active. |
| Execution | Browser Protection | On | Browser tools should not run automatically. |
| Execution | File-Deletion Protection | On | Deletion should require explicit owner intent. |
| Execution | External-File Protection | On | The agent should not write outside the workspace automatically. |
| Applying Changes | Inline Diffs | On | Makes changes visible. |
| Applying Changes | Jump to Next Diff on Accept | On | Speeds manual review. |
| Applying Changes | Auto Format on Agent Finish | Off | Avoids broad formatting noise outside the task scope. |
| Terminal | Legacy Terminal Tool | Off | Use only for unsupported shell setups. |
| Terminal | Toolbar on Selection | On | Convenience feature only. |
| Terminal | Auto-Parse Links | Off | Fetching links should be intentional. |
| Terminal | Themed Diff Backgrounds | On | Review convenience. |
| Terminal | Terminal Hint | Off | UI preference only. |
| Terminal | Preview Box for Terminal Ctrl+K | On | Safer than streaming generated commands directly into the shell. |
| Voice | Submit Keywords | Empty unless voice workflow is intentionally used | Avoid accidental voice auto-submit. |
| Attribution | Commit Attribution | Off by default | Owner preference; not required for safety. |
| Attribution | PR Attribution | Off by default | Owner preference; not required for safety. |
| Git | Branch Prefix | `cursor/` or project-specific prefix | Keeps agent-created branches recognizable. |

## Run Mode policy

`Run Everything` is not compatible with the owner-controlled default because it allows commands without approval, classification, or sandboxing.

Acceptable defaults are:

- Auto-review, if protections are enabled and allowlists remain narrow;
- a stricter approval/manual mode, if available;
- read-only or planning modes for audit tasks.

Use `Run Everything` only in disposable sandboxes or owner-approved experiments.

## Allowlist policy

Command allowlists should contain only read-only or inspection commands by default.

Safe examples:

```text
pwd, ls, cat, head, tail, dirname, basename, which, file, stat, du, df, grep, wc, sort, uniq, cut, rg, echo, printf, date, sleep, whoami, id, uname, printenv, git status, git diff, git log, git show, docker ps, docker images, docker logs, docker inspect, docker compose ps, docker compose logs, docker compose config
```

Do not allowlist mutating commands such as `git push`, `git reset --hard`, `git clean`, package installs, migrations, database writes, deploy commands, or container rebuilds unless the owner explicitly accepts that risk for a specific workspace.

Fetch domain allowlists should be empty by default unless the project has trusted docs domains.

## Agent obligation

When asked about Cursor settings, the agent should:

1. explain the setting in plain language;
2. state the owner-controlled default;
3. mention the tradeoff;
4. ask for project-specific preference only if the default is unsafe or insufficient.

The agent must not tell the owner to enable maximum autonomy as a default.

## OPTION PROFIT finalized owner profile

Use this as the practical default for owner-controlled work in OPTION PROFIT:

- Submit with Ctrl + Enter: on.
- Max Tab Count: 5.
- Queue Messages: send after current message.
- Usage Summary: always visible.
- Agent Autocomplete: on.
- Auto-Approve Mode Transitions: off.
- Explore subagent model: Composer 2.5 Fast.
- Start Agent Review on Commit: off.
- Include Submodules in Agent Review: off unless `.gitmodules` exists.
- Include Untracked Files in Agent Review: on.
- Agent Review approach: Quick by default; use stronger review for release-critical diffs.
- Web Search Tool: on.
- Auto-Accept Web Search: off.
- Web Fetch Tool: on.
- Hierarchical Cursor Ignore: on only after the root `.cursorignore` is reviewed.
- Ignore Symlinks in Cursor Ignore Search: off unless the project has many symlinks and ignore files remain reachable.
- Run Mode: Auto-review or stricter; never Run Everything for the normal project workspace.
- Browser Protection: on.
- File-Deletion Protection: on.
- External-File Protection: on.
- Command allowlist: read-only commands only by default.
- Fetch domain allowlist: empty by default.
- Inline Diffs: on.
- Jump to Next Diff on Accept: on.
- Auto Format on Agent Finish: off.
- Legacy Terminal Tool: off.
- Toolbar on Selection: on.
- Auto-Parse Links: off.
- Themed Diff Backgrounds: on.
- Terminal Hint: off.
- Preview Box for Terminal Ctrl+K: on.
- Voice submit keywords: empty unless the owner intentionally uses voice mode.
- Commit Attribution: off by owner preference.
- PR Attribution: off by owner preference.
- Branch Prefix: `cursor/`.
