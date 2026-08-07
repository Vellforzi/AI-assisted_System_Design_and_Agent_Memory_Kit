# Migration from v4.0 to v5.0

Project Artifact Contract V2 is a reviewed transformation, not an in-place schema upgrade. Project Artifact Contract V1 remains available unchanged for validating v4 artifacts, but v4 artifacts are not schema-valid v5 artifacts.

## Preservation rules

- Preserve IDs, evidence references, lifecycle state, settlements, and receipts verbatim.
- Convert `TaskContractV2` to `TaskContractV3` with `mode: standard`; use `unknown`, empty refs, or an explicit owner-review requirement for facts that cannot be proved.
- Do not invent a WorkItemGraph, PlanChallenge, ReviewReceipt, ExplorationMap, TriageLedger, DesignProbe, capability assessment, or domain term.
- A v4 verification status remains historical evidence; it does not imply a new capability assessment.
- Keep source files unchanged. Store an accepted v5 artifact separately only after owner review.

## Helper

`python tools/migrate_v4_artifact.py --input artifact.json --contract TaskContractV2`

The dependency-free helper reads one JSON artifact and prints a proposal plus the source SHA-256. It never writes, promotes, or activates the proposal. YAML artifacts can be migrated by copying their fields into JSON first or by performing the same mapping manually.

## Review checklist

1. Confirm the source hash, IDs, evidence refs, and lifecycle values.
2. Select workflow mode, scale, risk, delivery strategy, review policy, and capability impact from project evidence.
3. Add workflow artifact refs only when the referenced artifacts actually exist.
4. Validate the reviewed result with `project_artifact_contract_v2_oracle.py` or its schemas.
