# Model/Settings Label Fidelity Policy (AMK v3.9.6)

## Why this policy exists

Agent prompts must match real provider/UI controls. Invented or mixed labels create invalid execution configs and audit noise.

## Core rule

Use exact owner/provider UI labels from a dated snapshot or explicit owner confirmation.

Do not:

- invent combined labels;
- rewrite labels into non-existent variants;
- pair contradictory model/reasoning tuples.

## Required structured tuple

```yaml
surface: Cursor Agent
work_mode: Agent/apply
model: Codex 5.3
reasoning: medium
run_mode: Allowlist
terminal_profile: Debian WSL
snapshot_ref: owner-observed Cursor controls captured 2026-06-10
```

## Explicit negative example

Forbidden contradictory setting:

```text
Model: Codex 5.3 High
Reasoning: Medium
```

## Verification requirement

If label fidelity cannot be verified from current snapshot/owner input:

1. report missing evidence;
2. ask for exact labels;
3. avoid fabricated substitutions.
