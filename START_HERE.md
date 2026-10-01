# Start here

Published release: **4.3.1**.

> [!IMPORTANT]
> **Agent Memory Kit is a multiplier, not a brain.** A model that cannot reason
> about the task will use the kit poorly; a person who stops thinking will
> supervise it poorly. Ask questions about the kit through the agent. Select the
> model for the required result first and consider cost only after the capability
> floor is met. See
> [`HUMAN_MODEL_CAPABILITY_CONTRACT.md`](Agent%20Kit/kit/HUMAN_MODEL_CAPABILITY_CONTRACT.md).

1. Read `Agent Kit/portable/core/WORKFLOW.md`.
2. Keep the adopting project's current instructions and source authority.
3. Inspect current live tools before choosing ChatGPT, Codex, Cursor or another
   execution surface.
4. Preview adoption with:

```text
python "Agent Kit/portable/manage.py" --project "your/project"
```

5. Add `--write` only when installation/update is intended.

The owner request defines action authority. Any capable surface may execute the
owner-authorized work; no product name creates a mandatory intermediary. A
missing tool is a routing fact, not a new permission gate.

The installation manifest tracks managed baselines and preserves local
modifications. Optional reference material is selected by a concrete task need,
not loaded as a mandatory checklist. Python is required only when using the
installation helper.

See `Agent Kit/portable/README.md` for adoption/update rules and
`Agent Kit/kit/CHANGELOG_v4.3.1.md` for release-source notes.
