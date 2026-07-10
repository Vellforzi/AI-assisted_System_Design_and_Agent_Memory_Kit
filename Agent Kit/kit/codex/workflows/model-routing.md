# Codex model-routing workflow

Purpose: choose prompt-time options for Codex in the current ChatGPT desktop
app without padding the recommendation with unrelated application settings.

Snapshot date: 2026-07-10, Europe/Berlin. Current refs:

- `../../context_advisor/codex_provider_capability_snapshot_2026-07-10.yaml`
- `../../context_advisor/provider_surface_routing_snapshot_2026-07-10.yaml`

## Default owner-facing tuple

```yaml
surface: ChatGPT Codex
model: GPT-5.6-Terra
reasoning: Medium
speed: Standard
```

Evidence/config: model slug `gpt-5.6-terra`; snapshot
`context_advisor/codex_provider_capability_snapshot_2026-07-10.yaml`.

Use `gpt-5.6-sol` Medium as a quality-biased alternative when additional polish
is worth the higher cost. It is not the AMK cost-aware default.

## Route by task class

- Luna Low/Medium: extraction, inventory, classification, and repeatable static checks.
- Terra Medium: routine analysis, planning, task contracts, review, and bounded repair.
- Terra High or Sol High: difficult code/test repair or ambiguous root cause.
- Sol High/XHigh: hooks, routing, schemas, evals, protocols, and cross-system or production-risk recovery.
- Sol Max: one hardest sequential problem with an explicit trigger.
- Sol/Terra Ultra: meaningfully independent subproblems with separate scopes,
  stop conditions, and fuel justification.

Luna does not support Ultra in the owner-local 2026-07-10 capability snapshot.
Most work should remain on Medium/Standard without delegation.

## Control boundaries

- Keep exact display label, config slug, and reasoning effort separate.
- High, Max, and Ultra are alternative reasoning-effort selections. If High is
  selected, do not add `Max off` or `Ultra off` to the owner tuple.
- Codex Max is deeper reasoning for one task; Ultra adds automatic delegation.
- Cursor Max Mode belongs to Cursor and is not part of a ChatGPT Codex tuple.
- Standard is the default speed.
- Selecting Standard already means Fast is not selected; do not append `Fast off`.
- Fast is latency-first and increased-usage, never cheaper.
- IDE context, shell, terminal profile, approval, and app configuration are not
  prompt-time model options and appear only when the owner asks for them.

The owner-local cache exposes GPT-5.6 Fast, while the checked public Speed page
explicitly lists GPT-5.5 and GPT-5.4. Do not invent a fixed GPT-5.6 Fast credit
multiplier.

## Surface boundary

The official current desktop client is `ChatGPT desktop app (Codex mode)`;
use `ChatGPT Codex` in compact owner recommendations and
`chatgpt_desktop_codex` in structured output. Keep `Codex IDE extension`,
`Codex CLI`, and `Codex web` as distinct clients. `codex_app` is only a legacy
alias for desktop Codex mode. Do not infer GPT-5.6 Cursor Agent availability
from Codex-client evidence; the bundled Cursor snapshot is expired pending
refresh.
