# Codex Settings Recommendations

Recommended Codex application configuration and prompt-time choices for
owner-controlled work with Agent Memory Kit. Keep these two layers separate.

## UI settings

| Setting | Recommended value | Reason |
|---|---:|---|
| Language | Auto Detect | Keep UI flexible; language policy should be in instructions. |
| Speed | Standard | Prefer stable cost/quality for normal work. Fast is latency-first and increased-usage, not cheaper. |
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

Use GPT-5.6-Terra with `medium` reasoning and Standard speed as the AMK
cost-aware default for normal Codex work. Use GPT-5.6-Luna with Low/Medium reasoning for clear
repeatable extraction, and GPT-5.6-Sol with High/XHigh reasoning only for hooks, routing,
schemas, evals, protocols, or cross-system/production-risk recovery. Sol Max is
for one hardest sequential task. Sol/Terra Ultra requires independent scopes,
stop conditions, and fuel justification; Luna Ultra is unsupported by the
owner-local 2026-07-10 snapshot.

Keep model display label, config slug, reasoning effort, speed, Cursor Max Mode,
and delegation in separate fields. Exact model names and UI labels are volatile;
use `../context_advisor/codex_provider_capability_snapshot_2026-07-10.yaml` or
newer current evidence.

Owner-facing ChatGPT Codex recommendation example:

```text
ChatGPT Codex / GPT-5.6-Terra / Medium / Standard
```

Do not append `Fast off`, `Max off`, `Ultra off`, IDE context, shell, or
terminal profile. Those are redundant, unavailable on this prompt surface, or
application/policy details rather than choices made before prompt submission.

## ChatGPT Codex and Cursor

Using Codex inside Cursor is useful because it keeps both agent surfaces in one IDE while preserving separation of duties:

- Cursor/Composer is a strong executor for clear scoped implementation.
- ChatGPT Codex is preferred for analysis, planning, task contracts, independent review, evidence verification, and repair/recovery; it may also execute bounded repairs when task evidence supports it.
- Recommend the best executor or the two best comparable executors; do not present Composer as the only implementation route.
- Project Map is shared truth between both.

---

## v3.8 dated default role settings example

The following block is an example captured for the v3.8 package line. Treat model
names and UI labels as dated examples, not current defaults.

Recommended owner-controlled shape:

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
