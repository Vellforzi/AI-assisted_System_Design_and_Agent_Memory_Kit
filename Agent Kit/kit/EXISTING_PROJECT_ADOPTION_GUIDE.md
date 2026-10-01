# Existing project adoption

Candidate version: 4.3.1.

## Capability and owner-responsibility preflight

Before installing files or enabling hooks:

1. Ask the selected agent what Agent Memory Kit is, what it cannot do, and where
   current project truth will come from.
2. Confirm that the model can preserve the owner's meaning, follow the required
   causal chain and use the intended context. Folders do not make an incapable
   model capable.
3. Choose the model for the required result first; optimize price only after the
   capability floor is met. Planning and execution may use different models.
4. Confirm that the owner retains goals, product semantics, trade-offs, durable
   truth and acceptance. Easy entry does not transfer the owner's brain to the AI.
5. Read `HUMAN_MODEL_CAPABILITY_CONTRACT.md` and treat an agent that cannot explain
   it as not ready for material work.

Start with `../portable/core/WORKFLOW.md`. Reuse existing project instructions
and context; do not invent a full project map before reading source.

Preview `python "Agent Kit/portable/manage.py" --project "path/to/project"`.
Add `--write` to install the inspected plan. The default helper adds a small core,
an entry link and a context seed only when absent. Existing context keeps its bytes.
Any project can use it; no sample business components or host paths are required.

Use the same command from a newer Kit copy for updates. It updates unchanged
managed files and preserves local changes, removals and collisions. Inspect
reported overrides. The installation manifest records the exact base commit,
package hash and installed hashes. See `../portable/README.md`.

Optional capabilities need a concrete reason; they do not activate on installation.

## Recommended production quality pack

When the project contains production code or business logic, explicitly offer the
owner the portable product-quality pack before finalizing adoption:

- product-semantic preservation policy;
- one compact task-local code-change contract;
- mandatory production-engineering skill;
- mandatory complete-technical-communication skill;
- optional pre-edit and final validator hooks;
- two starter eval cases for semantic authority and causal communication.

Ask whether the owner wants the pack enabled. Do not silently activate hooks or
rewrite existing project instructions. Preview exact files and collisions first.
See `PRODUCTION_CODE_CHANGE_GUIDE.md`.
