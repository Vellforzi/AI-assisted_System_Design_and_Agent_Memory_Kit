# Release Notes v4.0.0

Released: 2026-08-07

v4.0 introduces a separate, strict Project Artifact Contract based on JSON Schema Draft 2020-12. TaskContractV2, ClaimLedgerV2, HandoffV2, and WorkingStateV2 are breaking schema upgrades. CommitmentLedgerV1, MemoryDeltaV1, SideEffectReceiptV1, VerificationReceiptV1, ArtifactDescriptorV1, and ArtifactExcerptV1 are new.

Reality-gated memory now links planned commitments to outcome evidence and provenance. A self-grade cannot automatically promote memory; promotion remains a separate owner-approved action. Verified claims require evidence or verification receipts.

Context budgets, bounded inspection, incident-to-eval lifecycle, mocked workflow traces, capability governance, and offline policy canaries are included as dependency-free, read-only/report-only helpers.

Context Contract V1 is unchanged. Core remains file-based, provider-neutral, and has no daemon, model API, database, vector index, background capture, automatic mutation, live traffic, Agent Circuit Breaker, or execution lanes.

Migration instructions: `Agent Kit/kit/MIGRATION_v3.8_TO_v4.0.md`.
