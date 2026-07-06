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
| Execution | MCP Tools Protection | On | MCP tools, especially database MCP, must be protected. |
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



## v3.9.3 dated Cursor model routing snapshot

Collected at: `2026-06-10T00:00:00+02:00`. Treat this as volatile provider evidence, not durable project truth. Refresh when Cursor model picker, pricing, context choices, or docs change.

Owner-observed Cursor model controls:

| Model | Available controls in snapshot | Cost-aware default |
|---|---|---|
| Composer 2.5 | Fast on/off only | routine default; Fast off for cost-aware work |
| Fable 5 | Thinking; 300K/1M context; effort low/medium/high/extra high/max | premium emergency fallback only |
| Opus 4.8 | Thinking, Fast; 300K/1M context; effort low/medium/high/extra high/max | premium architecture/audit fallback only |
| GPT-5.5 | Fast; 272K/1M context; reasoning none/low/medium/high/extra high | medium first; high/extra high only with trigger |
| Sonnet 4.6 | Thinking; 200K/1M context; effort low/medium/high/max | balanced fallback, medium first |
| Codex 5.3 | Fast; reasoning low/medium/high/extra high | code/test/repair specialist |

Do not invent missing controls. Example: Composer 2.5 has no reasoning/effort selector in this snapshot, so the agent must not recommend “Composer 2.5 High”. It can recommend Composer 2.5 Fast OFF/ON only.

Additional models are not needed for the Cursor-agent workhorse profile unless a project benchmark or failure case shows a gap.

## v3.9.3 Cursor model snapshot policy

Exact Cursor model advice must cite a dated provider/model snapshot. The packaged example is:

```text
Agent Kit/kit/context_advisor/cursor_provider_model_snapshot_2026-06-10.yaml
captured_at=2026-06-10
```

As of that owner-observed snapshot, the core Cursor Agent set is enough with surplus:

- Composer 2.5: default working horse for small/medium scoped Cursor Agent work.
- GPT-5.3 Codex: code/test/repair loop executor.
- GPT-5.5: hard reasoning escalation, not default for narrow Project Map/docs updates.
- Sonnet 4.6: balanced review/refactor/code-analysis alternative.
- Opus 4.8: rare hard planning or independent audit escalation.
- Fable 5: rare long-running autonomous agentic work.

Optional only:

- Gemini 3.1 Pro: huge/multimodal/1M-context fallback.
- Grok 4.3 or Grok Build: fast coding experiment/fallback.

Do not add optional models to default routing without a concrete capability gap, cheaper alternative, and owner approval.

When the owner asks `settings?`, include:

- snapshot date;
- model controls that matter for the chosen route;
- cheaper sufficient alternative;
- escalation trigger if using GPT-5.5 High/Extra High, Opus, Fable, Max/1M, Fast on expensive models, or optional models.

## Cost-aware model and reasoning policy

The agent must not recommend the strongest or most expensive model as a generic default. Use the lowest sufficient model/settings class for the task.

Practical default ladder:

| Work type | Default class |
|---|---|
| Formatting, extraction, grep-like checks, simple cleanup | low/fast or cheapest project default |
| Owner-provided facts, Project Map refs, version updates, small docs/root-router edits | medium/standard |
| Bounded implementation patch with exact scope and verification | medium/standard |
| Cross-subsystem root-cause, schema/protocol/eval/router changes, audit/repair/recovery, production-risk work | high/standard |
| Critical ambiguous synthesis or owner-approved maximum-quality run | extra-high/pro only with explicit reason |

If the agent recommends premium/frontier/high/pro, it must report:

1. the escalation trigger;
2. the cheaper alternative;
3. why the cheaper alternative is insufficient.

A vague phrase like “for maximum safety” is not enough.

## Include IDE Context boundary

`Include IDE Context` is a Cursor/provider UI setting. Agent Memory Kit policy does not toggle that setting through prompt text.

When implicit IDE context is present, treat open tabs, selections, diagnostics, terminal snippets, editor history, and workspace state as advisory only unless the owner explicitly scoped them. If the agent needs to use that context to expand read/apply scope, it must report the needed paths/classes and request owner approval first. File changes remain limited to approved scope.

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

MCP allowlists should be empty by default unless the MCP server is read-only and the owner approves automatic use.

Fetch domain allowlists should be empty by default unless the project has trusted docs domains.

## Agent obligation

When asked about Cursor settings, the agent should:

1. explain the setting in plain language;
2. state the owner-controlled default;
3. mention the cost/fuel and quality tradeoff;
4. name the cheaper sufficient alternative;
5. ask for project-specific preference only if the default is unsafe or insufficient.

The agent must not tell the owner to enable maximum autonomy or premium models as a default.

## Example owner-controlled profile

The following profile is a synthetic example of an owner-controlled Cursor setup.
Treat project-specific profiles as local examples, not package defaults:

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
- MCP Tools Protection: on when available.
- Command allowlist: read-only commands only by default.
- MCP allowlist: empty by default.
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


## v3.9.3 Auto/Max explicit boundary

Auto is not a specific model. For owner-controlled work, do not recommend Auto
as the default route unless the owner explicitly accepts non-deterministic
provider/model routing for low-risk exploration.

Max Mode is a separate Cursor-level capacity toggle for explicit models except Auto. Keep Max OFF by default; recommend 1M/Max only with context-overflow, broad-audit, large multimodal context, or explicit owner approval.
