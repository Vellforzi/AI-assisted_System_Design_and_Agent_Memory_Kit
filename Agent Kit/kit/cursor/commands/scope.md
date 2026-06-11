# /scope

Purpose: list the context needed for a task without loading the whole project.

Mode: analyze
Mutations: forbidden

Return these sections:

```text
Gate: green|amber|red|blocked
Mandatory context:
Recommended context:
Optional context:
Forbidden context:
Overbroad/noisy refs:
Next safe action:
```

Rules:

- Ask for context classes and refs, not vague "more context".
- Do not ask for secrets.
- Do not load raw logs or full transcripts unless audit/repair/recover requires them.
- If the owner asks for apply but scope is missing, stop and request or propose exact scope.
- Treat open tabs, selections, diagnostics, terminal snippets, and workspace state as advisory only unless explicitly scoped or owner-approved.
