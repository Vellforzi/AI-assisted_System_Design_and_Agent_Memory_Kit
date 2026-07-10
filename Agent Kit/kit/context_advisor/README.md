# Context Advisor Files

This folder contains machine-readable support files for the Context / Scope / Model Advisor.

Files:

- `context_advisor_v1.types.ts` — strict TypeScript contract for advisor traces and policies.
- `context_advisor_v1.profile_matrix.json` — default profile matrix for common owner tasks.
- `context_advisor_v1.hint_policy.json` — compact/expanded/blocking hint rules.
- `context_advisor_v1.example_run.json` — example trace for an under-scoped package update.
- `provider_capability_snapshot.example.yaml` — example of volatile model/provider capability evidence.
- `codex_provider_capability_snapshot_2026-07-10.yaml` — source-qualified GPT-5.6 Codex capability evidence.
- `provider_surface_routing_snapshot_2026-07-10.yaml` — current surface-first AMK routing and evidence-state split.
- `cursor_provider_capability_snapshot_2026-06-10.yaml` — dated Cursor UI/docs/forum snapshot for model controls and routing.
- `cursor_model_routing_matrix.v1.json` — machine-readable Cursor model routing matrix.

The 2026-06-10 Cursor snapshots are historical and expired. Keep their model
set unchanged until current Cursor evidence is available. Codex GPT-5.6 evidence
must not be used to claim GPT-5.6 availability in Cursor.

## v3.11.1 GPT-5.6 routing

The current Codex snapshot keeps full structured evidence separate while the
owner-facing ChatGPT Codex tuple contains only surface, model, reasoning, and
speed. ChatGPT desktop Codex, Codex IDE extension, CLI, and web are distinct
clients. The AMK
cost-aware default is GPT-5.6-Terra with Medium reasoning and Standard speed. Use Luna Low/Medium for
clear repeatable extraction, Sol High/XHigh for protocol or cross-system risk,
Sol Max for one hardest sequential problem, and Sol/Terra Ultra only for
meaningfully independent scopes with stop conditions and fuel justification.

Fast remains latency-first and increased-usage. The owner-local cache exposes
GPT-5.6 Fast, while the checked public Speed page names GPT-5.5 and GPT-5.4;
no fixed GPT-5.6 Fast credit multiplier is asserted.

Use these as templates. Project-specific copies should live under `Project Map/` or the project runtime layer, not inside always-loaded prompts.


## v3.9.2 Cost-aware model routing

The profile matrix includes model cost and capability fields. Agents should choose the lowest sufficient model/settings class. Premium/frontier/high/pro recommendations require an escalation trigger, a cheaper alternative, and a short reason why the cheaper option is insufficient.

## v3.9.3 Dated Cursor provider snapshot

v3.9.3 records the owner-observed Cursor model controls collected on 2026-06-10. The snapshot is intentionally volatile. Agents should cite its `collected_at` date when making model/settings recommendations and ask for refresh when the owner needs current pricing, current availability, or changed UI controls.

Do not add more models to the default router unless the current model set fails a concrete task class or the owner requests a benchmark.
