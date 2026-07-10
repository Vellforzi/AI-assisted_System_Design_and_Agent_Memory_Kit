# /amk-model-settings

Run AMK v3.11.1 model/settings label and surface-evidence checks.

Mode: read-only verification by default.

Required current ChatGPT Codex owner-facing tuple:

```yaml
surface: ChatGPT Codex
model: GPT-5.6-Terra
reasoning: Medium
speed: Standard
```

Evidence/config stays outside the prompt tuple: slug `gpt-5.6-terra`, snapshot
`context_advisor/codex_provider_capability_snapshot_2026-07-10.yaml`.

Rules:

1. Use exact owner/provider labels and keep label, slug, and reasoning separate.
2. Do not list `Fast off` when Standard is selected or `Max off`/`Ultra off` when another reasoning effort is selected.
3. Do not add IDE context, shell, terminal profile, approval, or app configuration unless the owner asks for those settings.
4. Ultra requires supported Sol/Terra evidence, independent scopes, stop conditions, and fuel justification; Luna Ultra is rejected.
5. Standard is default. Fast is latency-first/increased-usage, never cheaper; do not invent a fixed GPT-5.6 multiplier.
6. Treat ChatGPT desktop Codex, Codex IDE extension, CLI, web, and Cursor Agent as distinct surfaces.
7. Do not infer GPT-5.6 Cursor availability from Codex evidence. The bundled 2026-06-10 Cursor snapshot is stale pending refresh.
8. If labels or surface availability are unverified, report missing/stale evidence.
