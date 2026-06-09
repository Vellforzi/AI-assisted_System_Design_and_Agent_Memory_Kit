# Codex Settings Recommendations

Recommended Codex settings for owner-controlled work with Agent Memory Kit.

## UI settings

| Setting | Recommended value | Reason |
|---|---:|---|
| Language | Auto Detect | Keep UI flexible; language policy should be in instructions. |
| Speed | Standard | Prefer stable cost/quality for normal work. Use faster tiers only for short tasks. |
| Code review | Detached | Keep review context separate from the active implementation thread. |
| Show context window usage | On | Use context pressure as a checkpoint/handoff trigger. |
| Follow-up behavior | Queue | Avoid accidentally steering a running task. |
| Require modifier + Enter for long prompts | On | Prevent accidental submission of unfinished task contracts. |
| Personality | Pragmatic | Best fit for terse, controlled engineering work. |

## Project behavior

- Codex should be read-only by default.
- Apply work requires explicit task, mode, scope, allowed actions, forbidden actions, and verification.
- Codex memories should be disabled for project truth.
- Web search is allowed for external technical knowledge, not for project facts.
- Platform summaries are non-authoritative hints only.

## Recommended model effort

Use `medium` as the default reasoning effort for normal work. Use `high` for design review, bug hunting, architecture audits, and difficult recovery.

## Codex inside Cursor

Using Codex inside Cursor is useful because it keeps both agent surfaces in one IDE while preserving separation of duties:

- Cursor is the primary local implementation agent.
- Codex is a second reviewer, auditor, recovery assistant, and controlled executor.
- Project Map is shared truth between both.

---

## v3.8 default role settings

Recommended owner-controlled default:

```toml
model = "gpt-5.5"
model_reasoning_effort = "medium"
personality = "pragmatic"
approval_policy = "on-request"
approvals_reviewer = "user"
default_permissions = ":read-only"
web_search = "cached"
file_opener = "cursor"

[features]
hooks = true
memories = false
multi_agent = true
undo = true
```

This makes Codex a restricted second agent by default.

Use Codex primarily for:

- review;
- audit;
- recovery;
- second opinion;
- scope proposal;
- Project Map consistency checking.

Use Codex for mutations only after an explicit task contract, narrow write scope, approval, and permission boundary.

## Sandbox note

Do not combine `default_permissions` with older `sandbox_mode` or `[sandbox_workspace_write]` settings. Use one configuration path. For this kit, prefer permission profiles:

```toml
default_permissions = ":read-only"
```

See `CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`.
