# AI-assisted System Design and Agent Memory Kit

Source version: **4.5.0**. See [what changed](Agent%20Kit/kit/CHANGELOG_v4.5.0.md).
Source publication, a version tag and a GitHub Release are separate states.

Agent Memory Kit gives developers and project owners an inspectable, portable
way to keep project decisions, guide coding agents and resume interrupted work.
It is useful when a project spans many components or sessions and the agent
needs reliable current context without loading the entire project history.

> [!IMPORTANT]
> **Agent Memory Kit is a multiplier, not a brain.** The owner defines the
> intended outcome and accepts the result. A capable model still has to reason
> from current evidence. Ask the agent to explain the installed kit from its
> actual files; choose capability before optimizing cost.
> See [the capability contract](Agent%20Kit/kit/HUMAN_MODEL_CAPABILITY_CONTRACT.md).

## Start with a small core

Read [the workflow](Agent%20Kit/portable/core/WORKFLOW.md), then preview adoption:

```text
python "Agent Kit/portable/manage.py" --project "path/to/project"
```

Add `--write` to apply the inspected plan. The installer preserves existing
project instructions and reports local modifications instead of overwriting
them. Python 3.11+ is needed for this helper, not for reading the kit.
See [installation and updates](Agent%20Kit/portable/README.md).

## Choose the parts your project needs

| Part | Purpose |
| --- | --- |
| [Portable core](Agent%20Kit/portable/README.md) | Short workflow, project context template, tracked installation and updates. |
| [Production quality pack](Agent%20Kit/kit/PRODUCTION_CODE_CHANGE_GUIDE.md) | Existing engineering and communication skills, change contracts, optional validation and hooks. |
| [Agent-authored memory](Agent%20Kit/memory/README.md) | Optional local records, evidence links, RU/EN search and lifecycle control using the current agent; no LLM or embedding API. |
| [Reference library](Agent%20Kit/kit/README.md) | Optional recovery, client integration, review, evaluation and workflow material. |
| [AI-assisted System Design](AI-assisted%20System%20Design/README.md) | Separately authored system-design method. |

The core installer installs only its declared files. Optional skills, hooks and
memory are adopted separately; downloading the repository does not activate them.

## Compact skills in 4.5.0

The [optional skill library](Agent%20Kit/kit/SKILL_LIBRARY.md) now includes twelve
reusable skills and separate Codex/Cursor OPTION_PROFIT orchestration profiles.
Compact entrypoints retain their required references, templates, helpers and
invocation metadata. A payload manifest and executable checks cover dependencies,
mirrors and helper regressions. Project profiles are explicitly separated from
portable defaults; the five-file core installer remains unchanged.

## Code quality in 4.4.0

The two existing standards now cover useful purpose comments, accurate types,
the idioms and supported version of each language, justified error handling and
explicit resource ownership. They also guide causal debugging, checking related
defects, challenging review findings and using independently justified property
tests. Small functions do not need comments that merely repeat their names.

Types and documentation must preserve runtime behavior: framework-visible
annotations or docstrings can change validation, serialization or API
documentation. A passing type checker, test or structural validator proves only
what it checked. Existing diagnostic debt does not excuse a new defect.

Projects choose their comment language, tools, versions and adoption scope.
The kit does not impose a formatter, type checker, dependency, agent chain or
new worktree. See the [engineering skill](Agent%20Kit/kit/skills/production-engineering-standard/SKILL.md)
and [communication skill](Agent%20Kit/kit/skills/complete-technical-communication/SKILL.md).

## Authority and evidence

Current source establishes implemented behavior; the owner establishes required
behavior. Missing instructions mean preserve existing semantics. Tests, plans,
comments and retrieved memory are evidence, not authority to invent defaults,
retries, cache rules or public contracts.

ChatGPT, Codex, Cursor and other connected agents may execute authorized work
when their live tools fit the task. No client is a mandatory intermediary.
Source, tests, build, publication, deployment, runtime and owner acceptance remain
separate evidence layers. The kit does not guarantee model compliance or replace
the host's permissions and security controls.

## Authors and layers

| Layer | Author |
| --- | --- |
| `AI-assisted System Design/` | Alexander Lozovoy (All-fatherOdin) |
| `Agent Kit/` | Vellforzi |

See [AUTHORS.md](AUTHORS.md) and [LICENSE](LICENSE). Authorship follows the layer;
the separate `new_version` branch is not merged by this update.

## Verification

Run `python "Agent Kit/portable/test_manage.py"` for adoption/update checks and
`python "Agent Kit/portable/build_manifest.py"` for core metadata/hash checks.
Run `python "Agent Kit/portable/test_build_manifest.py"` for cross-platform
attribution/hash regression coverage.
Optional behavioral cases require actual agent runs and grading; parsing their
YAML does not prove that an agent follows the instructions.
