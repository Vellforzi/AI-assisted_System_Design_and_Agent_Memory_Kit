# /plan

Purpose: produce a scoped implementation or audit task for the coding agent.

Mode: plan
Mutations: forbidden

Required output:

```text
Task: <one goal>
Mode: apply | read-only | analyze
Project Map refs:
Scope:
Allowed:
Forbidden:
Expected result:
Verification:
After work:
```

Rules:

- One task, one goal.
- Exact paths where possible.
- No broad "fix everything" scope.
- Include forbidden actions: push, DB writes, deploy, secrets, unrelated files.
- Include Project Map update behavior.
