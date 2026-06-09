# Hook Packaging Guide

This guide defines how to package hooks as user-copyable artifacts.

## Package types

### Generic kit package

Lives inside Agent Memory Kit and contains templates.

```text
Agent Kit/kit/codex/hooks/
Agent Kit/kit/cursor/hooks/
```

### Project-local hook package

Generated for a specific project.

Example for Codex:

```text
.codex/
  hooks.json
  hooks/
    pre_compact_checkpoint_guard.py
    dangerous_command_guard.py
    project_map_write_guard.py
    secret_guard.py
  README.md
  ALLOWED_SCOPE.txt
  test_hooks.cmd
```

## Naming

Use project-specific package names:

```text
<PROJECT>_Codex_hooks_project_local.zip
<PROJECT>_Cursor_hooks_project_local.zip
```

## Required README contents

Every hook package must include:

- install path;
- enable instructions;
- test command;
- list of hooks;
- what is blocked;
- how to temporarily permit scoped work;
- how to reset to safe defaults;
- runtime requirements;
- known boundaries.

## Runtime neutrality

Agent Memory Kit is language-agnostic. Python examples are optional. If the owner does not want Python hooks, generate an equivalent package in the requested runtime.

## Checksum

If possible, include SHA256 checksums for generated hook files.
