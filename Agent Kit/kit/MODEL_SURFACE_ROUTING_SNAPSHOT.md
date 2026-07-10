# Model and Surface Routing Snapshot

Status: volatile, source-qualified snapshot
Captured at: 2026-07-10, Europe/Berlin
Expires at: 2026-08-09

Machine-readable refs:

- `context_advisor/provider_surface_routing_snapshot_2026-07-10.yaml`
- `context_advisor/codex_provider_capability_snapshot_2026-07-10.yaml`
- `context_advisor/execution_surface_routing_matrix.v1.json`

Provider/model facts are dated evidence, not permanent project truth. Current
Codex evidence and the expired 2026-06-10 Cursor evidence remain separate.

## Surface-first routing

| Surface | Default role | Typical work |
|---|---|---|
| Composer 2.5 / Cursor Agent | clear scoped implementation | explicit file edits, build/test iteration, mechanical orchestration, local verification |
| ChatGPT desktop app (Codex mode) | reasoning, review, and repair | analysis, planning, task contracts, evidence-chain review, repair/recovery, execution-integrity checks |
| Codex IDE extension | editor-attached Codex coding | scoped code work and review in a supported IDE |
| Codex CLI | terminal-first Codex coding | local command-line workflows |
| Codex web | hosted Codex work | web/cloud tasks subject to current availability |
| GPT web | current external research | deep/current sources and synthesis; no direct repository authority |
| Owner | side-effect gate | deploy, DB writes, git push/release, credentials, Project Map writes, destructive cleanup, acceptance smoke |

`chatgpt_desktop_codex` is the current structured desktop id and `ChatGPT Codex`
is the compact owner-facing label. `codex_app` is a backward-compatible alias
for desktop mode. `codex_ide` is a distinct current client, not an alias.

## AMK cost-aware Codex routing

These routes are AMK guidance, not an OpenAI universal benchmark.

| Task class | Model display label | Reasoning | Speed/delegation |
|---|---|---|---|
| extraction, inventory, classification, repeatable static checks | GPT-5.6-Luna | Low/Medium | Standard |
| routine analysis, planning, task contracts, review, bounded repair | GPT-5.6-Terra | Medium | Standard |
| difficult code/test repair or ambiguous root cause | GPT-5.6-Terra or GPT-5.6-Sol | High | Standard |
| hooks, routing, schemas, evals, protocols, cross-system or production-risk recovery | GPT-5.6-Sol | High/XHigh | Standard |
| one hardest sequential problem | GPT-5.6-Sol | Max with an explicit trigger | Standard |
| meaningfully independent parallel subproblems | GPT-5.6-Sol or GPT-5.6-Terra | Ultra | Standard; independent scopes, stop conditions, and fuel justification |

Cost-aware default config: `gpt-5.6-terra` with `medium` reasoning and Standard
speed. `gpt-5.6-sol` Medium is the quality-biased alternative, not the AMK
cost-aware default.

## Exact controls

| Display label | Config slug | Owner-local reasoning choices on 2026-07-10 | Owner-local context |
|---|---|---|---:|
| GPT-5.6-Sol | gpt-5.6-sol | low, medium, high, xhigh, max, ultra | 372000 |
| GPT-5.6-Terra | gpt-5.6-terra | low, medium, high, xhigh, max, ultra | 372000 |
| GPT-5.6-Luna | gpt-5.6-luna | low, medium, high, xhigh, max | 372000 |

Keep the display label, config slug, and reasoning effort in separate fields.
Do not emit invented combined labels such as `GPT-5.6-Sol High` when a separate
reasoning field is present.

Owner-facing ChatGPT Codex recommendations use only
`surface / model / reasoning / speed`. Standard already means Fast is not
selected; High already means Max and Ultra are not selected. Do not append
those negative states or unrelated application/terminal settings.

## Max, Ultra, Cursor Max Mode, and Fast

- Codex Max gives one selected model more reasoning depth for one hardest task.
- Codex Ultra adds automatic delegation. It is useful only when meaningful work
  can be split into independent scopes. Luna Ultra is unsupported by the
  owner-local 2026-07-10 snapshot.
- Cursor Max Mode is a context/capacity control. It is not Codex Max reasoning.
- Standard is the default speed.
- Fast is latency-first and increased-usage, never cheaper.

Fast evidence conflict: the owner-local Codex cache exposes Fast for all three
GPT-5.6 models and describes it as 1.5x speed with increased usage. The checked
public Speed page explicitly lists GPT-5.5 and GPT-5.4. No fixed GPT-5.6 Fast
credit multiplier is established by current public evidence.

## Cursor evidence boundary

The bundled Cursor model set was captured on 2026-06-10 and expired on
2026-07-10. Preserve that historical model set without adding GPT-5.6. Exact
current Cursor advice requires refreshed Cursor evidence. Codex GPT-5.6
availability does not establish GPT-5.6 availability in Cursor.

## Refresh triggers

- Codex model labels, effort choices, context, speed, subagent behavior, or rate card changes.
- Cursor model picker or current Cursor documentation is rechecked.
- Provider UI control labels change.
- The snapshot reaches its expiry date.
