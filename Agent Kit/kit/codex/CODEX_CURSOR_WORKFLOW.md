# Codex + Cursor Workflow

Use Codex and Cursor as two controlled agent surfaces over the same Project Map.

## Default split

```text
Cursor:
  apply work;
  local tests;
  diffs;
  repository edits under strict scope.

Codex:
  review;
  audit;
  second opinion;
  checkpoint validation;
  context recovery;
  alternative solution design.
```

## Recommended loop

1. Ask GPT or Codex for analysis and a task spec.
2. Run Cursor with a narrow `/apply` task.
3. Ask Codex to review the diff in detached mode.
4. Accept or reject findings manually.
5. Ask Cursor to fix only accepted findings.
6. Ask either agent to propose a Project Map delta.
7. Apply the Project Map update in a fresh or low-context session.
8. Run eval smoke if rules changed or a failure mode repeated.

## Do not do this

Do not let Cursor and Codex both edit the same files in parallel without a shared task contract and clean git state.

Do not treat Codex review as automatic approval.

Do not allow Codex to promote its own memory or chat summary into Project Map.
