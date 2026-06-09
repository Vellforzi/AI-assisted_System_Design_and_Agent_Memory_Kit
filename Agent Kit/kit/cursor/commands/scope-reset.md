# /scope-reset

Purpose: reset the task write whitelist to the safe project default.

Mode: apply-to-scope-file only.

Agent behavior:

1. write the safe default to `.codex/ALLOWED_SCOPE.txt` or the configured scope file;
2. report the final scope;
3. do not edit project files;
4. recommend checkpoint or Project Map delta only if significant work just ended.
