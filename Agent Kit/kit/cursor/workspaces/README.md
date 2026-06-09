# Cursor Workspace Templates

Use these templates to open a project with the right project boundary.

For a multi-component project with one Project Map, prefer opening the shared project root as the workspace.

A workspace is not a permission model by itself. It defines the IDE project perimeter. Still use task contracts, rules, hooks, and scope guards.

## Templates

- `OPTION_PROFIT_JOB.code-workspace.example` — single-root workspace for the OPTION PROFIT / JOB layout.
- `single-root-project.code-workspace.template` — generic one-root project template.

## How to use

1. Copy the template into the project root.
2. Rename it, for example `OPTION_PROFIT_JOB.code-workspace`.
3. Open it from Cursor.
4. Keep `.cursor/`, `.codex/`, `Project Map/`, and project components under the same workspace when they belong to one project.
