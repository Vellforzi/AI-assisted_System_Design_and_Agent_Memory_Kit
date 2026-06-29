# Codex Prompt Rules

Status: Active Codex prompt rule
Last aligned: <YYYY-MM-DD>
Audience: future AI/Codex sessions and maintainers
Runtime impact: none; governs task prompts only
Authority: workflow rule under `docs/source_of_truth_hierarchy.md`

---

## Purpose

Codex prompts in this project must connect:

- project goals;
- source authority;
- selected read set;
- affected files or layers;
- mutation scope;
- out-of-scope boundaries;
- tests/checks;
- retrieval receipt requirements.

The goal is small, explicit, bounded, and reviewable work.

---

## Required Prompt Sections

Every non-trivial Codex task should include:

1. Repository name
2. Task title
3. Task type
4. Goal
5. Required startup context
6. Task-specific read set
7. Triggered deep reads
8. Skipped-by-default context
9. Allowed files/layers
10. Mutation scope
11. Forbidden paths/layers
12. Scope
13. Out of scope
14. Constraints
15. Expected output
16. Tests/checks
17. Retrieval receipt requirement
18. Report-back requirements
19. Handoff update requirement when the task can change what a future session
    should do next

---

## Prompt Template

````markdown
You are working in the `<project-name>` repository.

## Task

<title>

## Task type

<docs-only | review | planning | implementation | validation | research | memory-update | api-agent design | other explicit scope>

## Goal

<what should be achieved and why>

## Context contract

Required startup context:

- AGENTS.md
- docs/NEXT_STEPS.md
- docs/source_of_truth_hierarchy.md
- docs/context_packs/current_status.md

Task-specific read set:

- <selected context pack, spec, rule, or file>

Triggered deep reads:

- <read only if the task needs this layer>

Skip by default:

- docs/project_map/** unless secondary Project Map, memory-update, retrieval routing,
  source-authority, or drift analysis is explicitly in scope
- docs/archive/**
- docs/proposals/**
- docs/research/** unless research or promotion is explicitly in scope
- data/**
- raw logs
- local databases
- secrets and environment files
- raw external-system payloads

## Allowed files/layers

- <files, directories, modules, or docs layers Codex may inspect/change>

## Mutation scope

- <read-only | docs-only edits | code/test edits | scripts-only edits | other explicit scope>

## Forbidden paths/layers

- <paths or layers Codex must not read or mutate>

## Scope

- <what to change>

## Out of scope

- <what must not be changed>

## Constraints

- Follow existing architecture and source authority.
- Do not make unrelated refactors.
- Do not add hidden side effects.
- Do not read or write high-risk artifacts unless explicitly scoped.
- Add or update tests if logic changes.
- Update docs if behavior, architecture, or workflow changes.
- If the result changes the next safe step, current phase, required read set, or
  roadmap/spec direction, update `docs/NEXT_STEPS.md`,
  `docs/context_packs/current_status.md`, and the relevant
  roadmap/status/spec entrypoint instead of leaving that state only in evidence,
  terminal output, or chat memory.

## Expected output

- <expected change>

## Tests/checks

```bash
<commands to run>
```

## Retrieval receipt requirement

Use the local helper when available:

```bash
python scripts/ai_context_helper.py receipt --task "<task title>" --profile "<task profile>" --read "<path>" --changed "<path>" --check "<command/result>" --format markdown
```

If the helper is not used, provide the same receipt manually.

## Report back

Report task-local scope, selected read set, skipped context, changed files,
summary, checks run, assumptions, risks, and confirmation that forbidden scope
was not expanded. If next-step state changed, report which handoff/status or
roadmap/spec entrypoint was updated.
````

---

## Anti-Patterns

Avoid prompts like:

- "improve the project";
- "refactor everything";
- "add AI";
- "optimize the architecture";
- "continue from memory";
- "use all available context".

Replace them with small task-specific prompts with explicit read set and
mutation scope.
