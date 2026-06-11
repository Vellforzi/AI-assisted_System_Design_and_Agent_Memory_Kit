# /fuel

Purpose: show a compact token/fuel plan for the current task.

Mode: analyze
Mutations: forbidden

Return:

```text
Fuel plan:
Keep:
Defer:
Drop:
Max Mode: yes/no/why
Include IDE Context: yes/no/why
Raw escalation: yes/no/why
```

Rules:

- Optimize context before wording.
- Prefer refs and summaries over raw payloads.
- Prefer targeted files and memory units over whole-project intake.
- If truncation risk exists, say what should be loaded first and what can wait.
- If IDE context is present but not explicitly scoped, count it as advisory/noisy and recommend exact refs or owner approval before using it to expand scope.
