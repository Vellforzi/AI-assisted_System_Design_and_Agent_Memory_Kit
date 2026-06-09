# Codex Workspace Check Workflow

Use this workflow when the owner asks which workspace to select.

The agent should:

1. inspect visible project roots;
2. check for `Project Map/`, `AGENTS.md`, `.codex/`, `.cursor/`, and project components;
3. recommend a shared project root when one Project Map governs multiple components;
4. explain that workspace selection is a visibility boundary, not a permission guarantee;
5. avoid changing files unless the owner explicitly asks.
