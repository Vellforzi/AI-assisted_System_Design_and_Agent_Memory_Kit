# Project Artifact Contract V1

Release: Agent Memory Kit v4.0.0
Schema dialect: JSON Schema Draft 2020-12
Status: core, file-based, provider-neutral

This package defines closed, machine-readable contracts for the durable
project artifacts introduced or revised in Agent Memory Kit v4.0. Existing
Context Contract V1 remains unchanged and independent.

## Contracts

- `TaskContractV2`
- `ClaimLedgerV2`
- `HandoffV2`
- `WorkingStateV2`
- `CommitmentLedgerV1`
- `MemoryDeltaV1`
- `SideEffectReceiptV1`
- `VerificationReceiptV1`
- `ArtifactDescriptorV1`
- `ArtifactExcerptV1`

Unknown properties and unknown contract versions fail validation. Structural
validation does not grant authority, execute work, promote memory, settle a
commitment, or certify a claim. Semantic invariants are checked by
`tools/project_artifact_contract_oracle.py`.

Run the dependency-free oracle:

```bash
python "Agent Kit/kit/tools/project_artifact_contract_oracle.py" --format json
```

Valid and invalid examples live in `examples/`; cross-artifact semantic cases
live in `fixtures/project-artifact-v1-smoke.json`.
