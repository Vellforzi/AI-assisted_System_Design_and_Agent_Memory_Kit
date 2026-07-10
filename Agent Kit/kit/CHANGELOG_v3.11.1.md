# Agent Memory Kit v3.11.1 Candidate Changelog

Status: unreleased working-tree candidate
Candidate date: 2026-07-10

No commit, tag, ZIP, publication, or release asset is implied by this file.

## Added

- Source-qualified Codex capability snapshot for GPT-5.6-Sol,
  GPT-5.6-Terra, and GPT-5.6-Luna.
- Current provider-surface routing snapshot with generic executor roles kept
  separate from volatile exact model choices.
- Eval cases `AMK-ML-002` and `AMK-MR-001` for exact-label and routing behavior.

## Changed

- AMK cost-aware Codex default is GPT-5.6-Terra with Medium reasoning and Standard speed.
- GPT-5.6-Luna with Low/Medium reasoning handles clear extraction, inventory,
  classification, and repeatable static checks.
- GPT-5.6-Sol with High/XHigh reasoning handles hooks, routing, schemas, evals, protocols,
  and cross-system or production-risk recovery.
- Sol Max is one hardest sequential problem. Sol/Terra Ultra is automatic
  delegation and requires independent scopes, stop conditions, and fuel
  justification. Luna Ultra is rejected by the 2026-07-10 local capability
  snapshot.
- `chatgpt_desktop_codex` is current for ChatGPT desktop Codex; `codex_app` is
  its compatibility alias, while `codex_ide`, `codex_cli`, and `codex_web` are
  distinct current clients.
- Owner-facing ChatGPT Codex recommendations use only
  `surface / model / reasoning / speed`; derived off states and application or
  terminal settings stay outside the prompt tuple.
- The 2026-06-10 Cursor model set is marked stale/pending refresh and remains
  unchanged. Codex evidence does not establish GPT-5.6 Cursor availability.

## Evidence boundary

- Official OpenAI documentation establishes public model roles, config slugs,
  Max/Ultra semantics, and credit rates.
- The owner-local Codex cache establishes labels, supported effort choices,
  372000-token context, and Fast availability for this environment only.
- The checked public Speed page names GPT-5.5 and GPT-5.4, while the local cache
  exposes GPT-5.6 Fast. AMK preserves that conflict and does not invent a fixed
  GPT-5.6 Fast credit multiplier.
- The owner-provided agent answer is intake evidence, not an official source.

## Preserved

- All provider snapshots dated 2026-06-10.
- Versioned historical examples and changelogs.
- Generic service routing: Cursor/Composer as a strong clear scoped executor,
  ChatGPT Codex for analysis/review/repair and evidence-supported bounded
  execution, GPT web for current external research, and owner gates for side
  effects. Recommend the best executor or the two best comparable executors.
