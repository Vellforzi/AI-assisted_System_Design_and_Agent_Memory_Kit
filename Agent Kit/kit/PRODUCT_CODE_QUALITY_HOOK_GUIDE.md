# Product code quality hook guide

The portable validator can enforce the production-quality contract without
introducing a new orchestration framework.

## Pre-edit gate

Run before a production-code write:

```text
python Agent Kit/kit/tools/validate_code_change_contract.py \
  --contract <task-root>/CODE_CHANGE_CONTRACT.yaml --phase pre-edit
```

The hook should match only declared production roots. Documentation-only edits,
changelog work and unrelated prose should not be blocked by this gate.

The pre-edit phase checks owner wording, both mandatory skills, required and
preserved behavior, non-goals, an empty unresolved-question list, the causal
chain, exact changed files/symbols, forbidden changes and impact-analysis fields.

## Final gate

Run before task completion:

```text
python Agent Kit/kit/tools/validate_code_change_contract.py \
  --contract <task-root>/CODE_CHANGE_CONTRACT.yaml --phase final
```

The final phase additionally requires semantic, diff, causal-chain, failure,
performance and resource-lifecycle review; preserved non-goals; no unexplained
production changes; tests not used as specifications; changed-symbol
traceability; and an explicit remaining-risk list.

## Hook adapter rule

A host-specific adapter may translate validator failure into a native deny or
follow-up response. Keep the validator host-neutral. The adapter must not infer
permission from the contract: owner authorization and quality validation are
separate facts.

## Fail behavior

Fail closed only for a matched production-code boundary. For unrelated local
work, report an advisory integration error instead of blocking the entire task.
Never inspect search text, patch bodies or arbitrary prose as if they were target
paths; evaluate normalized action operands.
