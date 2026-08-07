# Context Budget and Progressive Disclosure

`CONTEXT_BUDGET_POLICY_TEMPLATE.yaml` sets deterministic limits; it does not create a runtime or persist usage history. `context_budget_audit.py` compares a supplied read set with the policy and an optional caller-supplied baseline, reports stable reason codes, and never modifies inspected files.

Use metadata first, then a bounded excerpt or structured extract. `full_if_explicit` means a large artifact may be loaded in full only after an explicit profile or owner trigger. The context helper's `inspect` operation always returns descriptor and truncation metadata. Excluded/private paths fail closed and are not opened.

`ArtifactDescriptorV1` and `ArtifactExcerptV1` are defined in `project_artifact_contract_v1/schemas`. Descriptions, excerpts, extracts, and generated summaries are navigation-only projections. The original artifact remains the source of truth.
