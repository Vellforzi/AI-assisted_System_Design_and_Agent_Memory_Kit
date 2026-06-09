# /cursorignore-audit

Use this command to audit `.cursorignore` before enabling Hierarchical Cursor Ignore.

## Intent

Read-only analysis. Do not edit `.cursorignore` unless the owner explicitly asks for apply.

## Agent procedure

1. Locate root `.cursorignore` in the active workspace.
2. Check whether it ignores noisy files: `.git/`, caches, virtual environments, dependency folders, build outputs, logs, temp folders, generated artifacts.
3. Check whether it hides project truth files:
   - `AGENTS.md`;
   - `PROJECT_AI_BRIEF.md`;
   - `Project Map/**`;
   - `docs/**`;
   - `db_sql/**`;
   - active component folders.
4. Report whether Hierarchical Cursor Ignore should be enabled.
5. If unsafe, propose a minimal patch.

## Output

```text
.cursorignore audit
Mode: read-only
Safe to enable hierarchical ignore: yes/no
Noise patterns found: <list>
Risky patterns found: <list>
Missing evidence: <list>
Suggested patch: <optional>
```
