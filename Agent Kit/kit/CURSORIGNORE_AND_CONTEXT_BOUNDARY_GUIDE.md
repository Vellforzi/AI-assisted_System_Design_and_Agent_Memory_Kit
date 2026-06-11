# Cursor Ignore and Context Boundary Guide

`.cursorignore` controls what Cursor should ignore for context and search. It is a context hygiene tool, not a security boundary.

## Recommended use

Use a root `.cursorignore` to hide noisy generated files, caches, dependency folders, build outputs, logs, and large generated artifacts.

Do not hide the files that define project truth.

Usually keep visible:

```text
AGENTS.md
PROJECT_AI_BRIEF.md
Project Map/**
docs/**
db_sql/**
Options_api/**
Options_scraper/**
Options_MT/**
```

Usually ignore:

```text
.git/
**/desktop.ini
**/.DS_Store
**/Thumbs.db
**/__pycache__/
**/*.pyc
**/.pytest_cache/
**/.mypy_cache/
**/.ruff_cache/
**/.venv/
**/venv/
**/env/
**/node_modules/
**/.next/
**/dist/
**/build/
**/*.log
**/logs/
**/tmp/
**/temp/
**/downloads/
**/artifacts/
**/cache/
```

## Secret patterns

Secret patterns are useful, but they can also hide evidence from audits.

For owner-controlled projects, choose one of two modes:

1. **Ignore secret files for normal agent work.** This is safer for routine coding.
2. **Do not hide secret patterns in `.cursorignore`; instead protect them through rules, permissions, and allowlists.** This is better when the agent must audit repository hygiene without reading actual secret values.

Never ask the agent to copy secrets into chat or Project Map.

## Hierarchical Cursor Ignore

Enable hierarchical ignore only after a root `.cursorignore` exists and has been reviewed.

If no `.cursorignore` exists, the setting provides little value.

If `.cursorignore` accidentally hides Project Map, AGENTS.md, source authority, docs, or active component files, the agent may lose the very context Agent Memory Kit depends on.

## Agent audit procedure

When the owner asks whether Hierarchical Cursor Ignore should be enabled, the agent should:

1. locate root `.cursorignore`;
2. inspect whether it hides Project Map, AGENTS.md, source authority, docs, or active component files;
3. report safe/noisy/risky patterns;
4. recommend enabling only if the ignore file removes noise without hiding project truth.

## Codex ignore alignment

When the project uses both Cursor and Codex, keep `.cursorignore` and `.codexignore` aligned unless there is a deliberate reason to separate them.

For Windows or Google Drive projects, include:

```text
**/desktop.ini
```

The agent may propose or apply ignore-file updates only under explicit scope. It must not hide Project Map, AGENTS.md, source authority, docs, or active component source files.
