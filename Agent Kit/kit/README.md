# Agent Memory Kit reference library

Source version: **4.5.0**. Source date: 2026-10-27.
Start with [the small portable core](../portable/core/WORKFLOW.md).
This directory holds optional packs, templates and historical reference material.

The owner defines required behavior. Current source and actual observations
establish implemented behavior. Retrieved memory, comments, tests and agent
reports support reasoning; they do not create new authority or product rules.
Read the [human/model capability contract](HUMAN_MODEL_CAPABILITY_CONTRACT.md).

## Current entrypoints

| Need | Read |
| --- | --- |
| Adopt or update the core | [Portable adoption](../portable/README.md) |
| Understand owner and model responsibilities | [Capability contract](HUMAN_MODEL_CAPABILITY_CONTRACT.md) |
| Adopt compact skills and their complete dependencies | [Optional skill library](SKILL_LIBRARY.md) |
| Govern production-code changes | [Production quality pack](PRODUCTION_CODE_CHANGE_GUIDE.md) |
| Write and review code | [Engineering standard](skills/production-engineering-standard/SKILL.md) |
| Explain code and system behavior clearly | [Communication standard](skills/complete-technical-communication/SKILL.md) |
| Add local records and search | [Optional memory module](../memory/README.md) |
| Adapt a client integration | [Cursor](cursor/README.md), [Codex](codex/README.md) |
| Evaluate agent behavior | [Active evaluation suite](eval_suite/README.md) |
| Review the package contents and history | [Manifest](MANIFEST.md), [4.5.0 changes](CHANGELOG_v4.5.0.md) |

## Engineering and communication standards

The engineering skill owns code-quality requirements. Its
[code-quality reference](skills/production-engineering-standard/references/code-quality.md)
explains purpose comments, truthful types, language/version idioms, framework
contract hazards, justified exception handling and owned-resource cleanup.
The [diagnosis reference](skills/production-engineering-standard/references/diagnosis-and-properties.md)
covers competing causal hypotheses, related-defect searches and independent
properties. The existing review checklist ties these checks to the requested
behavior and affected consumers.

The communication skill owns how to explain intent, contracts, causes and
limitations without repeating syntax. It refers technical policy to the
engineering standard. Both have corresponding Cursor mirrors; edit the canonical
source and synchronize declared mirrors rather than maintaining divergent rules.

Adopting projects choose comment language, supported versions, static-analysis
tools and their configuration. These references do not install a type checker,
rewrite existing product code or turn legacy diagnostics into acceptable new
defects. Follow the pack's adoption guide and verify actual client discovery.

## Additional references

Use a guide only when its problem applies:

- [Project memory storage](PROJECT_MEMORY_STORAGE_GUIDE.md) and
  [working state/recovery](WORKING_STATE_AND_REPLAY_GUIDE.md).
- [Source authority template](SOURCE_AUTHORITY_TEMPLATE.yaml) and
  [grounding contract](PROJECT_GROUNDING_CONTRACT.md).
- [Orchestration choices](ORCHESTRATION_CHOICE.md) and
  [specialist functions](PROPOSED_SPECIALIST_FUNCTIONS.md).
- [Hooks](proposed_hooks/README.md), [workspace selection](WORKSPACE_SELECTION_GUIDE.md),
  [Windows text/command hygiene](WINDOWS_ENCODING_AND_SHELL_HYGIENE.md).
- [README authoring](README_AUTHORING_GUIDE.md) and
  [Git publishing](GIT_PUBLISHING_GUIDE.md).

Older changelogs, provider snapshots, role splits and protocol generations are
historical references. They do not override current owner instructions, the
portable core or the adopting project's current rules. A fixed claim such as
"Cursor implements, Codex reviews, ChatGPT researches" is not current routing
policy. Select a surface by available capabilities and task fit.

## Verification limits

The active cases are selected by `eval_suite/manifest.yaml`. A checklist or
schema validator does not execute the agent scenarios. A hash manifest verifies
content identity, not semantic correctness, permissions or runtime acceptance.
Python is needed for Python helpers; reading and applying the written method
does not depend on a particular language, host or model API.

## Skill source update, 2026-10-27

The [optional library](SKILL_LIBRARY.md) includes twelve reusable skills and
separate Codex/Cursor OPTION_PROFIT orchestration profiles. See the
[transfer review](SKILL_TRANSFER_REVIEW.md) for retained protections, portable
adaptations and verification limits. This source update does not change the
five-file core installer or claim a new tagged release.
