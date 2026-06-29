# Cursor Settings Optional Integration

Status: optional integration guide
Last aligned: <YYYY-MM-DD>
Audience: project owners using Cursor, AI/Codex sessions, maintainers
Runtime impact: none unless owner changes Cursor settings
Authority: Cursor settings guidance; subordinate to core governance and current owner choice

---

## Purpose

Use this module when Cursor is the local implementation agent and the owner wants
an owner-controlled settings profile around the core repo-centric governance
baseline.

Primary reference:

- `Agent Kit/kit/CURSOR_AGENT_SETTINGS_GUIDE.md`

## Practical Effect

- reduce accidental submission or unintended mode transitions;
- keep context usage visible;
- keep browser/MCP/deletion/external-file protections enabled where available;
- avoid broad command allowlists;
- keep Cursor implementation work aligned with `AGENTS.md`,
  `docs/source_of_truth_hierarchy.md`, and `docs/project_map/context_index.yaml`.

## Adoption

1. Install the core `secondary_memory_governance/` baseline first.
2. Review `CURSOR_AGENT_SETTINGS_GUIDE.md`.
3. Apply only settings that exist in the current Cursor UI.
4. Treat exact Cursor model lists and UI labels as volatile provider facts.
5. Keep project-specific overrides in the target project, not in this kit.

## Boundaries

This integration does not require hooks, does not change files automatically,
and does not grant mutation permission. It is a settings guide for owner control.
