# Codex Ignore and Context Boundary Guide

This guide explains how to use `.codexignore` with Agent Memory Kit.

## Purpose

`.codexignore` is a context hygiene and project-policy file for Codex-oriented workflows.

Use it to keep noisy, generated, local, or sensitive files out of routine agent context.

## Important boundary

Do not treat `.codexignore` as a guaranteed security mechanism.

Native support may vary by Codex runtime/version. If the active Codex runtime does not read `.codexignore` directly, the file is still useful as a policy artifact, but enforcement must come from hooks, permission profiles, scope guards, `.cursorignore`, `.gitignore`, or explicit agent instructions.

## Keep project truth visible

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

## Ignore noise and local artifacts

Recommended baseline:

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

For normal coding, keep real local secrets out of agent context:

```text
**/.env
**/.env.*
!**/.env.example
**/*secret*
**/*secrets*
**/*credential*
**/*credentials*
```

If the owner intentionally asks for a repository hygiene audit, the agent may inspect paths and filenames, but it must not copy secret values into chat, Project Map, logs, or durable memory.

## Agent procedure

When the owner asks for `.codexignore` help, the agent must:

1. identify the project root;
2. check whether `.codexignore` already exists;
3. check whether `.cursorignore` exists and should be mirrored;
4. avoid hiding Project Map, instructions, source authority, docs, or active components;
5. include `**/desktop.ini` for Windows/Drive projects;
6. explain that ignore files reduce context noise but do not replace permissions, hooks, or owner approval;
7. propose a patch or create the file only under explicit apply/scope permission.
