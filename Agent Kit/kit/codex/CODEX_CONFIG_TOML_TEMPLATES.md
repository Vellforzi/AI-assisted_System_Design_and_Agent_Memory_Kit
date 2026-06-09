# Codex `config.toml` Templates

Codex global configuration normally lives in:

```text
~/.codex/config.toml
```

On Windows, that is usually:

```text
C:\Users\<user>\.codex\config.toml
```

## Important TOML placement rule

Top-level settings must appear before the first table header such as `[features]` or `[mcp_servers.node_repl]`.

Do not paste top-level keys at the bottom of the file after `[desktop]`; then they become part of the `[desktop]` table.

## Recommended global top block

```toml
model = "gpt-5.5"
model_reasoning_effort = "medium"
personality = "pragmatic"

approval_policy = "on-request"
approvals_reviewer = "user"
default_permissions = ":read-only"
web_search = "cached"
file_opener = "cursor"
```

## Recommended `[features]` table

Use one `[features]` table only.

```toml
[features]
js_repl = false
hooks = true
memories = false
multi_agent = true
undo = true
```

## Recommended `[memories]` table

```toml
[memories]
use_memories = false
generate_memories = false
disable_on_external_context = true
```

## Safe overlay file

See:

```text
codex/config/config.toml.safe-overlay.toml
```

Use it to patch an existing Codex config without deleting auto-generated marketplace, plugin, MCP, or desktop sections.

## Full minimal example

See:

```text
codex/config/config.toml.owner-controlled.example
```

That example is intentionally minimal. It does not include machine-generated plugin paths from a specific installation.

---

## v3.7 owner-controlled default config

```toml
model = "gpt-5.5"
model_reasoning_effort = "medium"
personality = "pragmatic"

approval_policy = "on-request"
approvals_reviewer = "user"
default_permissions = ":read-only"
web_search = "cached"
file_opener = "cursor"

[plugins."browser@openai-bundled"]
enabled = true

[features]
js_repl = false
hooks = true
memories = false
multi_agent = true
undo = true

[memories]
use_memories = false
generate_memories = false
disable_on_external_context = true

[desktop]
conversationDetailMode = "STEPS_PROSE"
sansFontSize = 14
codeFontSize = 13
ambient-suggestions-enabled = true
```

Keep `sandbox_mode` out of this file when using `default_permissions`.
