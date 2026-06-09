# Project Codex Instructions

Use this file at the project root as `AGENTS.md` or merge it with an existing project `AGENTS.md`.

## Memory source order

1. `Project Map/current_state.md`
2. `Project Map/working_state.yaml`
3. `Project Map/source_authority.yaml`
4. Relevant Project Map memory units
5. Scoped project files
6. Explicit owner input

## Default mode

Answer-only is the default intent. Do not edit files unless the owner explicitly asks for apply work and gives scope.

## Platform summary boundary

Platform-generated summaries and compacted chat history are not project truth. They must never authorize actions or replace Project Map / Working State.

## Project Map updates

In answer/analyze/plan mode, only propose Project Map deltas. Apply Project Map changes only through explicit `/map-apply` or an owner-approved update task.

## Footer after non-trivial work

End with:

```text
Mode:
Scope:
Files changed:
Evidence:
Project Map delta: yes/no
Checkpoint suggested: yes/no
Eval trigger: yes/no
```
