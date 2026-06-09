# /map-apply

Purpose: update Project Map from an approved delta, checkpoint, or handoff.

Mode: apply
Allowed mutations: Project Map paths only

Required inputs:

- current Project Map;
- approved delta/checkpoint/handoff;
- evidence artifacts or owner approval;
- exact target Project Map paths.

Rules:

- Prefer a fresh or low-context session.
- Do not reconstruct previous chat.
- Do not use platform summary as evidence.
- Preserve lifecycle metadata, evidence, confidence, and supersession links.
- Do not change product code.

After work:

- summarize Project Map changes;
- list evidence;
- identify unresolved items;
- Eval trigger yes/no.
