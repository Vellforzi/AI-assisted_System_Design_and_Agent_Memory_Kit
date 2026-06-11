# Cursor Owner-Controlled Defaults

This is the recommended Cursor configuration profile for Agent Memory Kit.

## Role

Cursor is the primary local implementation agent.

It may edit files only when the owner explicitly gives an apply task with scope and verification.

Codex is the restricted reviewer/auditor/recovery helper.
GPT web chat is for research, architecture, analysis, and task specs.
Project Map is the shared memory boundary; it is source of truth only when the project's authority policy says so.

## Defaults

```yaml
agents:
  text_size: default
  submit_with_ctrl_enter: true
  max_tab_count: 5
  queue_messages: send_after_current_message
  usage_summary: always
  agent_autocomplete: true
  auto_approve_mode_transitions: false

subagents:
  explore_subagent_model: composer_2_5_fast
  default_policy: read_only

agent_review:
  start_on_commit: false
  include_submodules: false
  include_untracked_files: true
  default_approach: quick

context:
  web_search_tool: true
  auto_accept_web_search: false
  web_fetch_tool: true
  hierarchical_cursor_ignore: true_after_verified_root_cursorignore
  ignore_symlinks_in_cursor_ignore_search: false

approvals_and_execution:
  run_mode: auto_review_or_stricter
  forbidden_default_run_mode: run_everything
  browser_protection: true
  file_deletion_protection: true
  external_file_protection: true
  fetch_domain_allowlist_default: []

applying_changes:
  inline_diffs: true
  jump_to_next_diff_on_accept: true
  auto_format_on_agent_finish: false

inline_editing_and_terminal:
  legacy_terminal_tool: false
  toolbar_on_selection: true
  auto_parse_links: false
  themed_diff_backgrounds: true
  terminal_hint: false
  preview_box_for_terminal_ctrl_k: true

voice_mode:
  submit_keywords: []

attribution:
  commit_attribution: false
  pr_attribution: false

git:
  branch_prefix: cursor/
```

## Safety note

These settings reduce accidental execution. They do not replace task contracts, source authority, Project Map, git review, or owner approval.

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
