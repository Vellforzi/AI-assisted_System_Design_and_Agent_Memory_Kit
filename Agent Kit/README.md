# Agent Memory Kit

Source version: **4.5.0**. [Change notes](kit/CHANGELOG_v4.5.0.md).

This is the agent workflow and project-memory layer of the repository. It helps
an owner keep concise decisions, recover ongoing work and require evidence for
code changes. The owner retains product meaning and final acceptance; the model
still needs sufficient reasoning and tool capability.

## Start here

1. Read [the capability contract](kit/HUMAN_MODEL_CAPABILITY_CONTRACT.md) and
   [short workflow](portable/core/WORKFLOW.md).
2. Preview [portable adoption](portable/README.md) in the actual project.
3. For coding work, inspect [the production quality pack](kit/PRODUCTION_CODE_CHANGE_GUIDE.md).
4. Add [local agent-authored memory](memory/README.md) if evidence-linked records
   and search solve a real continuity problem.
5. Use [the reference library](kit/README.md) for a specific task need.

## What each part owns

`portable/package.json` declares the small managed core. An adopting project's
`Agent Kit/INSTALLATION.json` records its installed version, hashes and local
overrides. The project keeps its own instructions, business logic and durable
context. The core installer does not activate all skills, hooks or examples.

The independently versioned `memory/` module stores agent-authored records and
provides local search. The current agent supplies meaning and bilingual search
keys. The module validates structure and provenance without calling a model,
embedding service or external API. Its manifest is separate from the core.

The optional quality pack contains the existing
`production-engineering-standard` and `complete-technical-communication` skills.
Version 4.4.0 expands comments, types, language idioms, failure handling,
resource ownership, causal diagnosis and property-based reasoning. Comment
language and exact tool versions remain adopting-project decisions.

## Working rules

The current owner request authorizes its explicit and causally necessary work.
Analysis-only requests remain read-only. Current source establishes existing
behavior; an unspecified product rule must be preserved.

Choose ChatGPT, Codex, Cursor or another execution surface by current tools and
task fit. No client, helper agent, orchestration hierarchy or new worktree is a
mandatory step. Adopt optional controls proportionally to the task.

Separate source, tests, build, publication, deployment, runtime and owner
acceptance. Documentation and integrity checks do not prove skill activation or
future agent behavior. Tag and release state require separate repository
readback; this source version is not a claim that a release object was created.
