# AI-assisted System Design and Agent Memory Kit

Published release: **4.2.0**.

Agent Memory Kit is a portable operating and project-memory layer. It helps an
owner ground work in current source, preserve concise durable decisions and
recover an interrupted task. It does not require a specific model, plugin, hook,
MCP server or folder layout.

Start with [the portable core](Agent%20Kit/portable/core/WORKFLOW.md), then use
[portable adoption](Agent%20Kit/portable/README.md) when installation or update
tracking is useful.

## Execution surfaces

ChatGPT web, Codex, Cursor and other connected agents are first-class execution
surfaces. Select from current owner authority, live capabilities and task fit.
Do not hard-code GPT web as read-only or require Cursor/Codex as a repository
intermediary. External/current research is a ChatGPT strength, not its only role.

An action request authorizes its causally necessary implementation and
verification within the named scope. Analysis-only requests remain read-only.
A missing capability on one surface is a routing fact, not a project-wide
prohibition and not a reason to repeat an approval already supplied.

## What is included

- `Agent Kit/portable/` — small universal core, manifest and adoption/update CLI.
- `Agent Kit/kit/` — optional templates, stronger workflows and historical
  references.
- `AI-assisted System Design/` — separately authored design-method layer.

## Current principles

- Current source establishes implemented behavior; the owner establishes intended
  behavior.
- Project Map current-state files are concise durable truth, not task transcripts.
- Source, tests, build, publication, deployment, runtime and owner acceptance are
  separate evidence layers.
- Branch push, tag push and deployment are not interchangeable claims.
- Owner-designated spreadsheets/databases remain sources; Canvas and other
  generated dashboards complement rather than silently replace them.
- Package release proof requires matching version metadata, repository commit,
  tag and verifiable release state.

## Authors and layers

| Layer | Author |
|---|---|
| `AI-assisted System Design/` | Alexander Lozovoy (All-fatherOdin) |
| `Agent Kit/` | Vellforzi |

See [AUTHORS.md](AUTHORS.md) and [LICENSE](LICENSE). Authorship follows the layer.
The `new_version` branch remains a separate alternative and is not merged by
this source update.

## Verification

Run `python "Agent Kit/portable/test_manage.py"` for adoption/update tests and
`python "Agent Kit/portable/build_manifest.py"` for package/version/hash
consistency. Optional eval definitions do not substitute for captured behavioral
runs and grading.

Release-source notes: [v4.2.0](Agent%20Kit/kit/CHANGELOG_v4.2.0.md).
