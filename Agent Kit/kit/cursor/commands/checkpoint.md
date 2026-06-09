# /checkpoint

Purpose: capture the current stage before context becomes long or before switching tasks.

Mode: checkpoint
Default mutations: forbidden

Create a checkpoint proposal with:

```yaml
checkpoint_id:
task:
status:
completed:
changed_files:
verified:
failed:
decisions:
risks:
open_questions:
next_safe_step:
evidence:
project_map_updates_proposed:
eval_trigger:
```

Rules:

- Do not rely on platform summary.
- Use only visible facts, files, diffs, test output, tool output, and current owner input.
- Do not write Project Map unless explicitly asked in apply mode.
