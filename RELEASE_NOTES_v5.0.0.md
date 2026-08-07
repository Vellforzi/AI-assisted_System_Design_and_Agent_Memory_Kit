# Agent Memory Kit v5.0.0 release notes

Release date: 2026-08-07

v5 introduces Project Artifact Contract V2. It turns eight agentic coding practices into closed, evidence-gated file contracts while keeping routine work lightweight. Activation is derived from `TaskContractV3.workflow_profile`, task scale, and risk; the Kit does not create irrelevant workflow artifacts for a routine single-session task.

## Breaking changes

- `TaskContractV2` becomes `TaskContractV3` with a required workflow profile.
- `HandoffV2` and `WorkingStateV2` become V3 and preserve active workflow references and the next safe step.
- `CommitmentLedgerV1` and `VerificationReceiptV1` become V2 with workflow subjects and verification level/environment.
- v4 Project Artifact files are not schema-valid v5 artifacts until a reviewed transformation is completed.

`ClaimLedgerV2`, `MemoryDeltaV1`, and `SideEffectReceiptV1` remain compatible. `project_artifact_contract_v1/` remains unchanged so v4 artifacts can still be validated. Context Contract V1 is unchanged and fully compatible.

## New core contracts

- WorkItemGraphV1: independently verifiable vertical work and a derived runnable frontier.
- PlanChallengeV1: one open owner decision at a time before risky apply work.
- ReviewReceiptV1: fresh-context or adversarial review without author reasoning, mutation, or repair authority.
- ExplorationMapV1 and TriageLedgerV1: evidence-bounded discovery and delegation readiness without product mutation or tracker replacement.
- DesignProbeV1: disposable, isolated design experiments that cannot be promoted to production.
- CapabilityRegistryV1: immutable definitions, append-only assessments, and end-to-end evidence for passing status.
- DomainLanguageV1: bounded-context terminology authority without implementation-fact authority.

## Helpers and evals

The dependency-free V2 oracle validates closed schemas, workflow activation, graph cycles/frontier, owner gates, evidence, isolation, and lifecycle invariants. The projection helper reports graph/exploration frontiers, capability status, and triage readiness without persisting or activating them. Mocked workflow fixtures cover reviewer isolation, exploration/delivery separation, and prohibited prototype promotion.

## Unchanged non-goals

There is no daemon, scheduler, issue tracker, model API, database, vector index, background reviewer, automatic mutation, automatic frontier selection, prototype merge, or capability promotion. External runtimes may act only under their own explicit owner-approved policies.
