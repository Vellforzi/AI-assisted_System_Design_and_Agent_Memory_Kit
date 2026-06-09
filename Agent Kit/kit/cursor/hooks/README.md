# Cursor Hooks Examples

These files are optional examples for projects that want technical checks around agent actions.

Agent Memory Kit does not require Python. The scripts are written in Python because Python is portable and convenient for the original owner. You may replace them with shell, Node.js, PowerShell, Go, or any other language.

Always verify the current Cursor hooks schema before installing `hooks.json.example`.

---

## Scripts

| Script | Purpose |
|---|---|
| `block_secrets.py` | Detect likely secrets in files or stdin. |
| `block_db_writes.py` | Block dangerous SQL or DB-write commands. |
| `block_git_danger.py` | Block git push/reset/clean/rebase unless allowed. |
| `scope_guard.py` | Block changed files outside allowed path globs. |
| `project_map_write_guard.py` | Block Project Map writes unless the run is explicitly authorized. |

---

## Standalone examples

```bash
python3 cursor/hooks/scripts/block_secrets.py --paths .
python3 cursor/hooks/scripts/block_db_writes.py --command "psql -c 'DROP TABLE x'"
python3 cursor/hooks/scripts/block_git_danger.py --command "git push origin main"
python3 cursor/hooks/scripts/scope_guard.py --allowed "docs/**" --changed "docs/a.md" "app/main.py"
python3 cursor/hooks/scripts/project_map_write_guard.py --changed "Project Map/current_state.md"
```

---

## Owner policy

Hooks should fail closed for dangerous operations and fail open only for clearly non-mutating checks.

Do not make hooks so strict that they prevent ordinary read-only work. Start with warnings, then switch to blocking after testing.
