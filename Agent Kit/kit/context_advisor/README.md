# Context Advisor Files

This folder contains machine-readable support files for the Context / Scope / Model Advisor.

Files:

- `context_advisor_v1.types.ts` — strict TypeScript contract for advisor traces and policies.
- `context_advisor_v1.profile_matrix.json` — default profile matrix for common owner tasks.
- `context_advisor_v1.hint_policy.json` — compact/expanded/blocking hint rules.
- `context_advisor_v1.example_run.json` — example trace for an under-scoped package update.
- `provider_capability_snapshot.example.yaml` — example of volatile model/provider capability evidence.
- `cursor_provider_capability_snapshot_2026-06-10.yaml` — dated Cursor UI/docs/forum snapshot for model controls and routing.
- `cursor_model_routing_matrix.v1.json` — machine-readable Cursor model routing matrix.

Use these as templates. Project-specific copies should live under `Project Map/` or the project runtime layer, not inside always-loaded prompts.


## v3.9.2 Cost-aware model routing

The profile matrix includes model cost and capability fields. Agents should choose the lowest sufficient model/settings class. Premium/frontier/high/pro recommendations require an escalation trigger, a cheaper alternative, and a short reason why the cheaper option is insufficient.

## v3.9.3 Dated Cursor provider snapshot

v3.9.3 records the owner-observed Cursor model controls collected on 2026-06-10. The snapshot is intentionally volatile. Agents should cite its `collected_at` date when making model/settings recommendations and ask for refresh when the owner needs current pricing, current availability, or changed UI controls.

Do not add more models to the default router unless the current model set fails a concrete task class or the owner requests a benchmark.
