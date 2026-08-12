# /stage

Purpose: create or update only the requested task contract/bootstrap artifact.

Mode: stage
Mutations: active task-output root only

Execution routing: resolve `stage + task_stage + path zone` to
`stage_task_artifacts`. Acquire a task-output-only CAS lease. Source files,
Project Map, git, DB, deploy, and execution of the staged task remain forbidden.

Required behavior:

1. Read the minimum Project Map core and explicitly named evidence.
2. Create both `Executor Routing Gate` and `Execution Profile Gate` before task instructions.
3. Validate both gates.
4. Stop after the requested contract/bootstrap exists and reports its exact path.
5. Do not execute `next_step` or the staged contract.
