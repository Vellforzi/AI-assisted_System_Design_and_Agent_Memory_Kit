# Codex Ignore Templates

This directory contains optional `.codexignore` templates for projects that use Codex alongside Agent Memory Kit.

## Boundary

`.codexignore` is a context-hygiene and project-policy artifact. Native support may vary by Codex runtime/version. If the runtime does not read `.codexignore` directly, use the same patterns through hooks, scope guards, `.cursorignore`, `.gitignore`, or project instructions.

Do not rely on ignore files as a security boundary. Secrets must also be protected by rules, hooks, permissions, git hygiene, and owner review.

## Recommended project root files

For owner-controlled projects, keep both files aligned:

```text
.cursorignore
.codexignore
```

Both should hide noise and local secrets, but must not hide project truth:

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

## Desktop metadata

Windows may create `desktop.ini` in many directories. Ignore it everywhere:

```text
**/desktop.ini
```
