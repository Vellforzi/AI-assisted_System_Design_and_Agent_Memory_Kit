# T001: Existing Context Governance Surface

Task: `T001`
Kind: `scout`
Status: `current`

## Artifact map

- `Agent Kit/kit/tools/context_governance_helper.py` is the existing read-only, standard-library reference implementation. It owns deterministic read-set selection, legacy governance receipts, the current `api-context` bundle/receipt shape, and context-selection smoke execution.
- `Agent Kit/kit/secondary_memory_governance/context_index.yaml` owns routing metadata: task profiles, priority, authority, lifecycle status, retrieval mode, purpose, mutation boundary, and excluded high-risk path globs. Its own authority statement makes it navigation metadata subordinate to operational sources.
- `Agent Kit/kit/secondary_memory_governance/retrieval_policy.yaml` owns retrieval hard gates, profile/lifecycle rules, missing-evidence behavior, smallest-working-set limits, and required result metadata.
- `Agent Kit/kit/secondary_memory_governance/retrieval_scoring_policy.yaml` owns hard-gate-before-scoring order, scoring signals/weights, top-k behavior, profile limits, and result metadata requirements.
- `Agent Kit/kit/secondary_memory_governance/context_selection_smoke_cases.yaml` owns the existing portable selection cases and their required/forbidden path expectations.

## Reusable implementation surface

`build_read_set()` already returns profile resolution, selected sources with `path`, `priority`, `authority`, `status`, `layer`, `retrieval_mode`, inclusion reason, purpose and mutation boundary, plus missing paths, skipped trigger-only items, skipped high-risk globs, truncation count, and explicit no-scope-expansion booleans.

`build_api_context_bundle()` already produces a request envelope, read set, denied tool outcomes, and a nested receipt. This is the compatibility source for V1 field mapping, but its legacy discriminator strings (`api_agent_context_bundle`, `api_agent_context_receipt`) and duplicated top-level/context read-set fields are not yet a language-independent versioned contract.

`run_smoke_checks()` already emits stable failure prefixes for `over_retrieval`, `under_retrieval`, `task_scope_miss`, `wrong_retrieval`, `missing_required_files`, and `missing_read_set_files`. Expected fixtures can normalize these prefixes to reason codes rather than retaining full Python error prose.

## Gaps and boundary risks

- The helper does not load `retrieval_policy.yaml` or `retrieval_scoring_policy.yaml`; it cannot currently prove stale-authority suppression from those policies.
- Selection currently excludes high-risk paths and respects index profile/retrieval mode, but it does not filter index entries by lifecycle `status`. A stale-authority fixture therefore needs an explicit policy-evaluation seam rather than a schema-only assertion.
- The existing smoke YAML supports selection inputs plus required/forbidden paths, but not arbitrary ContextRequest/Bundle/Receipt payload validation or portable expected reason-code arrays.
- The repository has no JSON Schema files, no Python dependency manifest, no `jsonschema` installation, and no automated unit-test harness for this helper. The helper's standard-library-only property is documented and should be preserved unless Judge explicitly approves an optional validator dependency path.
- Template smoke instructions assume an installed target project (`python scripts/ai_context_helper.py smoke-check --format json`); the Kit template itself is not laid out as such a target root.

## Verification and integration candidates

Current helper discovery/check commands:

```powershell
python "Agent Kit/kit/tools/context_governance_helper.py" --help
python scripts/ai_context_helper.py smoke-check --format json
```

The second command is the documented adopter-project command and requires a copied/installed project layout. T003 should add a Kit-local standard-library oracle command that runs the canonical V1 corpus directly, plus retain a compatibility check over existing selection smoke cases.

Candidate package layout for Judge to confirm:

- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/schemas/`
- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/examples/{valid,invalid}/`
- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/fixtures/`
- `Agent Kit/kit/secondary_memory_governance/context_contract_v1/README.md`
- `Agent Kit/kit/tools/context_contract_v1_oracle.py`
- compatible additions to `Agent Kit/kit/tools/context_governance_helper.py`, `Agent Kit/kit/MANIFEST.md`, and relevant Kit README/checksum inventory only if required by repository conventions.

Judge must choose whether V1 is a normalized replacement view over the legacy `api-context` result or a minimally disruptive versioned projection. The contract must keep schema validation structural and policy evaluation delegated to the named canonical policy/index/helper sources.

## Board Receipt Snippet

See the T001 receipt in `state.yaml`.
