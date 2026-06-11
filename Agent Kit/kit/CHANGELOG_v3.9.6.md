# Agent Memory Kit v3.9.6 — Shell Reliability Gate + Model/Settings Label Fidelity

Release date: 2026-06-11
Status: micro-patch overlay for live workspace adoption.

## Purpose

v3.9.6 closes two execution safety gaps discovered during shell-dependent audit/commit runs:

- shell transport reliability must be proven before any shell-dependent PASS/commit decision;
- model/settings prompt labels must match owner/provider UI labels exactly, with no invented combined labels.

## Added

- `policies/shell_reliability_gate_policy.md`
- `policies/model_setting_label_fidelity_policy.md`
- `router_fragments/shell_reliability_gate_v3.9.6.md`
- `router_fragments/model_setting_label_fidelity_v3.9.6.md`
- Cursor commands:
  - `/amk-shell-health`
  - `/amk-model-settings`

## Updated

- `cursor_integration/rules/context_advisor_preflight.mdc`
- live `.cursor/rules/context_advisor_preflight.mdc`
- eval suite manifest/policy/cases for v3.9.6 categories:
  - `shell_reliability_gate`
  - `model_setting_label_fidelity`

## Key rules

- Start shell-dependent audit/apply with:
  - `echo AMK_SHELL_OK; pwd; git rev-parse HEAD`
- Unknown/no-output/no-exit-code shell result is a hard failure, not PASS.
- Use Run Mode `Allowlist` when sandbox transport is unreliable. Do not use Run Everything.
- Use exact structured settings tuple:
  - `surface: Cursor Agent`
  - `work_mode: Agent/apply`
  - `model: Codex 5.3`
  - `reasoning: medium`
  - `run_mode: Allowlist`
  - `terminal_profile: Debian WSL`
  - `snapshot_ref: owner-observed Cursor controls captured 2026-06-10`
- Do not invent combined labels or contradictory settings (example forbidden: `Model: Codex 5.3 High` + `Reasoning: Medium`).
