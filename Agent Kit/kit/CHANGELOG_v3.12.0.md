# Agent Memory Kit v3.12.0 Changelog

Release date: 2026-08-12

Previous published tag: `v3.11.3`. This is the public execution-runtime
minor. It does not dump a private project's Product Map, hosts, or
account paths.

This file is release metadata, not publication proof. Publication requires a
matching repository commit, annotated tag, archive checksum, and release
receipt.

## Why this release exists

v3.11.3 published the working-method guides (FAQ, schemes, CN facts, hook
cards). The live high-control layout also had an execution runtime: unique
route, write lock, verified delivery, and fail-closed launchers. That
runtime now ships as portable templates, validators, evals, and hooks.

## Added

- `EXECUTION_PROFILE_GATE.md` — pair with Executor Routing Gate. Route key
  is `mode + task class + path zone`. Zero or equal-priority matches block.
- Registry templates: `PATH_ZONES_TEMPLATE.yaml`,
  `AGENT_EXECUTION_PROFILES_TEMPLATE.yaml`, `SCOPE_PROFILES_TEMPLATE.yaml`,
  `WINDOWS_TOOLCHAIN_PROFILE_TEMPLATE.yaml`.
- Scope lease (write lock): baseline-bound CAS update/release. A lock is
  not deploy permission.
- Archive provenance: commit parity from Git blobs only. Worktree ZIP
  bytes cannot receive `commit_parity`.
- Verified delivery: `VERIFIED_DELIVERY_PIPELINE.md`, contract/receipt
  templates, validators under `tools/`.
- Windows command-launch hygiene: registered interpreter, structured argv,
  file-association rejection (`cursor/rules/windows-command-hygiene.mdc`,
  eval `AMK-WCL-001`).
- Mode commands `/stage` and `/review` (task-root only / read-only).
- Codex hook examples: `thread_health_recovery.py`,
  `verified_delivery_stop_guard.py`.
- Eval cases for profile uniqueness, path-zone fail-closed, lease, archive
  provenance, mode boundaries, lean R0–R4 control, runtime acceptance,
  orchestration lanes, and verified delivery (`AMK-EPG-001`, `AMK-PZ-001`,
  `AMK-SL-001`, `AMK-ARC-001`, `AMK-MODE-001`, `AMK-LC-001`, `AMK-WCL-001`,
  `AMK-RA-001`/`002`, `AMK-CDO-001`/`002`, `AMK-VDP-001`–`034`).
- Validator `tools/verify_execution_profile_gate.py`.

## Not in this public release

- Product evals (named terminals, private API sentinels, host log paths).
- App Server / context-runtime / `AMK-CTX-*` / `AMK-APP-*` controllers.
  Those files were not in the portable Agent Kit tree; they stay project-
  local until a later extraction.

## Unchanged from v3.11.3

- Motive, FAQ, capability-management thesis, behavioral oracles, schemes,
  CN catalog, proposed hook cards, specialist function cards.
- Eval `AMK-CM-001`.

## Safety boundary

These files are guides and validators. They do not authorize commit, push,
deploy, credentials, or copying a private Project Map into the kit.
