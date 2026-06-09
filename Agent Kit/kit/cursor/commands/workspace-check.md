# /workspace-check

Purpose: check whether the active IDE workspace is appropriate for Agent Memory Kit.

Mode: read-only.

Agent behavior:

1. identify workspace root(s);
2. check whether `Project Map/`, `AGENTS.md`, `.cursor/`, `.codex/`, and relevant project components are visible;
3. report missing project-memory or instruction layers;
4. recommend one shared project-root workspace when the project has multiple components and one Project Map;
5. do not edit workspace files unless explicitly asked.
