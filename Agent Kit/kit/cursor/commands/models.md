# /models

Purpose: show the current dated provider/model routing snapshot and explain whether the working model set is sufficient.

Mode: analyze
Mutations: forbidden

Rules:

- Use `context_advisor/cursor_provider_capability_snapshot_2026-06-10.yaml`, `context_advisor/provider_surface_routing_snapshot_2026-06-10.yaml`, and `context_advisor/cursor_model_routing_matrix.v1.json` when available.
- Always show `collected_at` and warn that provider/model facts are volatile.
- Do not add new models merely because they exist in the provider picker.
- Recommend adding a model only if the current set fails a concrete task class, the owner requests benchmarking, or current provider changes justify a refresh.
- Do not invent missing controls for a model.

Return:

```text
Model snapshot:
- collected_at:
- expires_at:
- current working set sufficient: yes/no
- missing model class, if any:
- default Cursor-agent workhorse:
- premium fallbacks:
- refresh needed: yes/no/why
```


## v3.9.3 Auto/Max explicit boundary

Auto is not a specific model. For OPTION-PROFIT controlled work, do not recommend Auto as the default route unless the owner explicitly accepts non-deterministic provider/model routing for low-risk exploration.

Max Mode is a separate Cursor-level capacity toggle for explicit models except Auto. Keep Max OFF by default; recommend 1M/Max only with context-overflow, broad-audit, large multimodal context, or explicit owner approval.

## Surface summary

The command must answer three questions:

1. Is the Cursor-agent core model set sufficient? Default answer for 2026-06-10 snapshot: yes, with surplus.
2. Should more models be added? Default: no, unless a concrete capability gap or benchmark need appears.
3. Which surface should run the task: Cursor Agent, Codex IDE extension, or ChatGPT Pro web?
