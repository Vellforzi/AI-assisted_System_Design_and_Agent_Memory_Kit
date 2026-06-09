# Codex Scope Set Workflow

Use this workflow when the owner asks Codex to set task write scope.

## Required input

- task title;
- exact allowed write paths;
- reset-after-task preference;
- confirmation that the scope update is approved.

## Agent behavior

1. validate paths;
2. reject unsafe or unrelated paths;
3. update `.codex/ALLOWED_SCOPE.txt` using direct file edit or `codex/scope/update_allowed_scope.py`;
4. show final scope;
5. stop unless a separate apply task is also explicitly approved.
