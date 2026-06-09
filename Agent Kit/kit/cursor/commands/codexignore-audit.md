# /codexignore-audit

Mode: analyze.

Goal: inspect the project `.codexignore` policy and propose a safe update.

Rules:

- Do not edit files unless the owner explicitly switches to apply mode.
- Treat `.codexignore` as a context hygiene/policy artifact, not a security boundary.
- If native Codex support is unknown, say so and recommend hooks/scope guards for enforcement.
- Keep Project Map, AGENTS.md, source authority, docs, and active components visible.
- Include `**/desktop.ini` for Windows or Google Drive projects.
- Mirror `.cursorignore` where appropriate.

Output:

```text
Codex ignore audit:
- file exists: yes/no
- noisy files covered: yes/no
- desktop.ini covered: yes/no
- secrets patterns covered: yes/no
- project truth accidentally hidden: yes/no
- recommended patch:
```
