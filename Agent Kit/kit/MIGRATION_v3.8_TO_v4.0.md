# Migration from v3.8 to v4.0

v4.0 is a breaking release for Project Artifact contracts. Context Contract V1 is unchanged and remains compatible. Existing v3.8 files are not schema-valid v4 artifacts until they are explicitly transformed and reviewed.

## Safe migration sequence

1. Keep the v3.8 artifact unchanged.
2. Run `python tools/migrate_v38_artifact.py <artifact> --type auto` and capture the JSON proposal.
3. Review every `unknown`, `pending`, and `owner_review_required` value against source evidence.
4. Validate the reviewed proposal with `project_artifact_contract_oracle.py`.
5. Promote or replace files only as a separate owner-approved action.

The helper is read-only: it writes only to stdout, includes the source SHA-256, and does not claim that missing facts were verified. It preserves recognized IDs, evidence references, and lifecycle/status values. Unsupported structures remain listed in `unmapped_source_fields` and require owner review.

Breaking schemas: TaskContractV2, ClaimLedgerV2, HandoffV2, WorkingStateV2. New schemas: CommitmentLedgerV1, MemoryDeltaV1, SideEffectReceiptV1, VerificationReceiptV1, ArtifactDescriptorV1, ArtifactExcerptV1.
