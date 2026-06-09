# Hook Generation Questions

Use these questions only when the answer is not already available from owner input, Project Map, or project files.

## Essential questions

1. Which tool should the hooks target: Codex, Cursor, Claude Code, or another tool?
2. What is the project root path?
3. Should hooks warn only or block unsafe actions?
4. Which runtime is acceptable for hook scripts: Python, Node.js, PowerShell, shell, Go, or another language?
5. Are database writes forbidden by default?
6. Are git push/reset/clean/rebase forbidden by default?
7. Should Project Map writes require a separate enable/disable gate?
8. Should scope be managed through `ALLOWED_SCOPE.txt` or another whitelist file?
9. What paths are never allowed: secrets, `.env`, credentials, `.git`, deployment configs, production data?
10. Should context compaction be blocked until checkpoint/handoff exists?

## Optional questions

- Should hooks log decisions to a file?
- Should hooks integrate with CI?
- Should hooks support multiple operating systems?
- Should hook scripts be packaged separately from the main kit?
- Should scripts be project-specific or generic templates?

## Do not over-ask

If the owner already has a known project structure and safety policy, generate a reasonable safe default and explain what to customize.
