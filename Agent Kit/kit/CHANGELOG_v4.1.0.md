# Agent Memory Kit v4.1.0 Changelog

Release date: 2026-08-13

Previous published tag: `v4.0.0`. This is a minor release: authorship
surface, host-plugins guide, and one eval case. Not v5 (friend's `new_version`
branch uses v5-style numbering separately).

This file is release metadata, not publication proof. Publication requires a
matching repository commit, annotated tag, archive checksum, and release
receipt.

Eval suite id: `AMK-EVAL-v4.1.0`.

## Why this release exists

The package already contained two layers but did not state authorship by
layer on the GitHub landing page. Host plugins (PStack, Cursor plugins,
Codex skills) were in common use but never explained as host add-ons
distinct from the kit.

v4.1.0 adds that surface without merging the friend's `new_version` branch.

## Added

- Root `AUTHORS.md` and an **Authors / layers** block in root `README.md`.
- `Agent Kit/kit/HOST_PLUGINS_GUIDE.md` — portable guide for PStack,
  Cursor plugins, and Codex skills; no-trigger-no-install discipline.
- Eval case `AMK-PL-001` (host plugins are not the kit; do not vend plugin
  trees; plugin output is not Project Map truth).
- FAQ row and starter cross-links in `QUESTIONS_THIS_KIT_ANSWERS.md`,
  `START_HERE.md`, kit README, and `MANIFEST.md`.

## Unchanged

- Execution Profile Gate, verified delivery, durable-truth role, CN catalog,
  schemes, hook cards, orchestration choice, and inherited eval cases.
- The `new_version` branch is not merged. Compare only:
  [`main...new_version`](https://github.com/Vellforzi/AI-assisted_System_Design_and_Agent_Memory_Kit/compare/main...new_version).
