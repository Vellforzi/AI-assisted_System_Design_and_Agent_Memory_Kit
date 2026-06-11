## Model/settings label fidelity (v3.9.6)

Use exact labels from owner/provider UI snapshot; do not normalize into invented variants.

Required tuple for this patch:

- `surface: Cursor Agent`
- `work_mode: Agent/apply`
- `model: Codex 5.3`
- `reasoning: medium`
- `run_mode: Allowlist`
- `terminal_profile: Debian WSL`
- `snapshot_ref: owner-observed Cursor controls captured 2026-06-10`

Hard constraints:

- no combined labels;
- no contradictory model/reasoning pairs;
- report missing evidence when labels are unknown.
