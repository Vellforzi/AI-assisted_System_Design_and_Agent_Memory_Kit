# /amk-model-settings

Run AMK v3.9.6 model/settings label fidelity check.

Mode: read-only verification by default.

Required tuple:

```yaml
surface: Cursor Agent
work_mode: Agent/apply
model: Codex 5.3
reasoning: medium
run_mode: Allowlist
terminal_profile: Debian WSL
snapshot_ref: owner-observed Cursor controls captured 2026-06-10
```

Rules:

1. Use exact owner/provider UI labels.
2. Do not invent merged or non-existent labels.
3. Do not output contradictory pairs (forbidden: `Model: Codex 5.3 High` + `Reasoning: Medium`).
4. If labels are unverified, report missing evidence and ask for exact labels.
