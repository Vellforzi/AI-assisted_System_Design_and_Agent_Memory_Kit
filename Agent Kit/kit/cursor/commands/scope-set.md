# /scope-set

Purpose: update the task write whitelist for an approved apply workflow.

Mode: apply-to-scope-file only.

Required owner input:

- task name;
- exact allowed write paths;
- forbidden paths/actions;
- whether scope should reset after task.

Agent behavior:

1. verify the request is explicit;
2. reject broad unsafe scope;
3. update `.codex/ALLOWED_SCOPE.txt` or the configured scope file only if approved;
4. display the resulting scope;
5. do not edit product files unless a separate `/apply` task contract exists.

Default reset scope:

```text
AGENTS.md
PROJECT_AI_BRIEF.md
docs/**
Project Map/**
```
