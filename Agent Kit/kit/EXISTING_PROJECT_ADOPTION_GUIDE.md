# Existing project adoption

Candidate version: 4.2.0-dev.

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
