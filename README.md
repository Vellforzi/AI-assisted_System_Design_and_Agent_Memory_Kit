# AI-assisted System Design and Agent Memory Kit

Working candidate: **4.2.0-dev**, based on published **4.1.0**, commit
`557e340208d8661f00d76bdd9c4a4ea1a748ed59`. This source update does not create a tagged release.

Agent Memory Kit is a set of working instructions, project-context conventions
and optional helpers. It helps an agent ground its work in current source,
retain decisions and recover the right task. It does not run agents itself.

Start with [the short core](Agent%20Kit/portable/core/WORKFLOW.md).
For installation and updates, use [portable adoption](Agent%20Kit/portable/README.md).
The default does not require hooks, plugins, an orchestration server or a model.

The owner's action request authorizes its necessary local work. Analysis and
planning stay read-only. Extra approval is needed only for a material missing
decision or an action outside the authority already supplied.

## Authors and layers

| Layer | Author |
|---|---|
| `AI-assisted System Design/` | Alexander Lozovoy (All-fatherOdin) |
| `Agent Kit/` | Vellforzi |

See [AUTHORS.md](AUTHORS.md) and [LICENSE](LICENSE). Authorship follows the
layer. The design-method layer remains separate and unchanged.

The `new_version` branch is a separate alternative. Its useful profile concept
was considered; its workflow schemas, documentation engine and file removals
are not merged by this candidate.

## What is included

- `Agent Kit/portable/`: small universal core, manifest, adoption and update CLI.
- `Agent Kit/kit/`: optional reference guides, stronger workflows and historical cases.
- `AI-assisted System Design/`: the separately authored design-method layer.

Project-specific rules, local additions and private history stay in the adopting
project. Updates preserve them and report conflicts instead of replacing them.
The portable manifest is an allowlist, not a trust signature.

## Verification

Run `python "Agent Kit/portable/test_manage.py"` to verify adoption and updates
on unrelated temporary projects. Run `python "Agent Kit/portable/build_manifest.py"`
to check package/version/hash consistency. The optional YAML eval checker
validates definitions only; actual model behavior needs captured runs and grading.
