# Project Artifact Contract V2

Release: Agent Memory Kit v5.0.0
Dialect: JSON Schema Draft 2020-12
Status: core, file-based, provider-neutral

V2 adds workflow-aware project artifacts while leaving Context Contract V1
and Project Artifact Contract V1 unchanged. Core inclusion means every type is
normatively specified and evaluated; an artifact is required for a task only
when `TaskContractV3.workflow_profile` activates its mode, scale, risk, review,
capability, or bounded-context rule.

Breaking contracts are TaskContractV3, HandoffV3, WorkingStateV3,
CommitmentLedgerV2, and VerificationReceiptV2. New contracts are
WorkItemGraphV1, PlanChallengeV1, ReviewReceiptV1, ExplorationMapV1,
TriageLedgerV1, DesignProbeV1, CapabilityRegistryV1, and DomainLanguageV1.
ClaimLedgerV2, MemoryDeltaV1, and SideEffectReceiptV1 remain compatible and
are referenced from V1 without copying them.

Unknown versions and properties fail closed. Validation never selects work,
activates a frontier, mutates a tracker, repairs reviewer findings, promotes a
prototype, or changes capability status. Run:

```bash
python "Agent Kit/kit/tools/project_artifact_contract_v2_oracle.py" --format json
```
