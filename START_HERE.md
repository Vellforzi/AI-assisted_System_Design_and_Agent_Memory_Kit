# Start here

Source version: **4.4.0**.

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
`Agent Kit/kit/CHANGELOG_v4.4.0.md` for release-source notes.

## Optional local agent-authored memory module

An independently versioned optional source module is available at
`Agent Kit/memory/README.md`. It uses the current agent for semantic work and local
Python for evidence-linked records, RU/EN search and lifecycle control; no model or
API dependency is installed. Preview adoption with its `install.py`. The module
has a separate manifest and does not change the core version or prior release
claims above. Existing project instructions, evidence and customization remain
project-owned.
