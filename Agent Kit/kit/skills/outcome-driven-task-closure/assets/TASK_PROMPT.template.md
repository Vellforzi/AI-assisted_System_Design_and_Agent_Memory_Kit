# Task prompt compiler contract

Do not manually copy the outcome-driven workflow into a launch, continuation,
correction, recovery, or handoff prompt. Describe only task-specific truth in a
`TASK_PROMPT_SPEC_V1` and let `scripts/task_prompt_tool.py` render and validate
the prompt.

## Spec

```json
{
  "schema": "TASK_PROMPT_SPEC_V1",
  "mode": "inherited",
  "task_id": "stable task id",
  "tree": "absolute workspace path",
  "baseline_head": "optional Git HEAD",
  "continuation": true,
  "owner_outcome": "owner-visible outcome, preserved verbatim when practical",
  "task_state": [
    "task-local capsule/matrix/receipt paths or another durable state locator"
  ],
  "current_evidence": [
    "new facts only; evidence is not scope"
  ],
  "active_slice": "optional current priority, not a replacement outcome",
  "authorization": {
    "allowed": ["explicitly allowed side effects"],
    "forbidden": ["separately gated or forbidden side effects"]
  }
}
```

Allowed top-level fields are exactly those shown above. `baseline_head`,
`task_state`, `current_evidence`, and `active_slice` may be omitted when they do
not apply. A continuation in `inherited` mode must identify durable task state.

## Modes

- `inherited` is the default for Codex tasks that can read applicable
  `AGENTS.md`, skills, and task-local state. It never repeats workflow,
  acceptance-matrix mechanics, test order, status vocabulary, or recovery
  procedure.
- `standalone` is only for a target agent without those inherited resources. It
  adds one fixed compact execution contract; callers cannot supply arbitrary
  process prose.

## Commands

```text
<python> -X utf8 scripts/task_prompt_tool.py roundtrip --spec-file <spec.json>
<python> -X utf8 scripts/task_prompt_tool.py validate --spec-file <spec.json> --prompt-file <prompt.txt>
```

`roundtrip` validates the spec, renders the canonical prompt, validates that
exact output, and writes it to stdout. Use `--spec-file -` to read JSON from
stdin. All text boundaries are strict UTF-8; `U+FFFD` is a fatal corruption
signal. Do not edit the rendered prompt; update the spec and rerun instead.
