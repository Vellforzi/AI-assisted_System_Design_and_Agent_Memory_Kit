# Release Notes v3.9.1 — Implicit IDE Context Boundary Patch

Release date: 2026-06-10

## Purpose

v3.9.1 is a micro-patch on top of v3.9.0. It makes the Context Advisor rule for implicit IDE context explicit across portable docs, templates, Cursor/Codex workflow notes, machine-readable policy, and eval cases.

## What changed

- Added the **Implicit IDE Context Boundary** rule:
  - open tabs, selections, diagnostics, terminal snippets, editor history, and workspace state are advisory only unless explicitly scoped;
  - if the agent needs to use implicit IDE context to expand read/apply scope, it must first report needed paths/classes and request owner approval;
  - file changes remain limited to approved scope only;
  - prompt text such as `IDE Context OFF` is a policy marker, not a UI toggle.
- Updated Context Advisor docs and scope-control docs with the new boundary.
- Updated Cursor and Codex workflow guidance.
- Updated root instruction templates so new projects inherit the rule.
- Updated machine-readable Context Advisor policy with an implicit-IDE-context trigger and violation code.
- Added eval case `AMK-CA-007` for unscoped implicit IDE context.
- Updated the optional `context_advisor_preflight.py` helper with `--implicit-ide-context` and `--implicit-ide-approved` flags.

## Compatibility

This patch is backward-compatible with v3.9.0. It does not change the Project Map schema, memory schema, retrieval profiles, or required runtime dependencies.

## Upgrade guidance

For projects that already adopted v3.9.0:

1. Replace the portable `Agent Kit/` files with v3.9.1, or apply only the changed files listed in the manifest/diff.
2. If the project uses root routers such as `AGENTS.md`, `.cursor/rules/*.mdc`, or `PROJECT_AI_BRIEF.md`, add a one-line reference to the Implicit IDE Context Boundary.
3. Do not install TypeScript solely for this patch. The TypeScript file is a contract artifact unless the project edits or compiles kit contracts locally.

## Eval trigger

Yes. The patch changes agent behavior around scope expansion, Cursor/Codex context handling, and Context Advisor eval coverage.
