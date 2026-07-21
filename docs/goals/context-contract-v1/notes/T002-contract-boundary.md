# T002: Context Contract V1 Boundary

Task: `T002`
Kind: `judge`
Status: `current`

## Decision

Approved as one bounded implementation package.

Use JSON Schema Draft 2020-12. Each of the three schemas is standalone, declares `$schema`, and uses a stable URN `$id` in the namespace `urn:agent-memory-kit:context-contract:v1:*`. Cross-file `$ref` is intentionally avoided in V1 so Python and TypeScript adapters do not need different URI registries.

The V1 layer is a normalized, versioned projection over the existing read-only helper surface. It does not replace or mutate legacy `api-context` output. The Python oracle/adaptor reference imports `context_governance_helper.py` and maps its deterministic read-set metadata into V1 payloads.

## Contract ownership

### ContextRequestV1

Owns transport intent only:

- `contract_type: ContextRequestV1`
- `contract_version: 1.0`
- `request_id`
- `task` and normalized `profile`
- read-only `mutation_scope`
- selection constraints: `max_sources`, `include_triggered`, `required_paths`, `forbidden_paths`
- `requested_tools`
- exact `policy_refs` for context index, retrieval policy, and retrieval scoring policy

It does not embed profile tables, scoring weights, excluded globs, authority ranks, or stale rules.

### ContextBundleV1

Owns the selected context result:

- linkage to `request_id` and a unique `bundle_id`
- normalized profile and policy refs
- `sources` using existing helper/index fields (`path`, `priority`, `authority`, `status`, `layer`, `retrieval_mode`, inclusion metadata)
- selection summary: configured limit, omitted count, missing paths, skipped trigger-only items, skipped high-risk globs, and truncation state
- explicit no-scope-expansion flags

It does not contain raw file contents, hidden memory, embeddings, caches, database identifiers, or copied policy tables.

### ContextReceiptV1

Owns portable evaluation evidence:

- receipt/request/bundle linkage
- outcome (`pass` or `fail`)
- stable `reason_codes`
- structured checks with stable ids/status/reason codes
- counts and policy refs
- requested/allowed/denied tool outcomes
- changed paths and explicit scope-expansion flags

Human/validator-specific error prose is not part of expected fixture truth. Adapters may log local diagnostics outside the contract, but the canonical receipt contains normalized reason codes only.

## Fixture oracle

One JSON fixture manifest contains complete Request/Bundle/Receipt payloads for every case plus:

- `case_id`
- expected schema validity per payload type
- expected policy validity
- ordered, de-duplicated expected reason codes
- references to canonical source artifacts and any reused legacy smoke case id

Required policy reason codes:

- `OVER_RETRIEVAL`
- `UNDER_RETRIEVAL`
- `FORBIDDEN_PATH_SELECTED`
- `STALE_AUTHORITY`

Schema-invalid examples use stable schema reason categories derived from instance paths/keywords, never a validator library's message text. Oracle equality is defined over case id, schema-valid booleans, policy-valid boolean, and reason-code set/order.

Policy evaluation remains source-backed:

- over/under/forbidden semantics reuse the existing helper smoke invariants and legacy case identifiers;
- stale authority is derived from the active profile's lifecycle exclusions in `retrieval_policy.yaml` and source status/authority from `context_index.yaml`/bundle metadata;
- result metadata requirements point to `retrieval_policy.yaml` and `retrieval_scoring_policy.yaml` rather than copying their lists into fixtures.

## Validation strategy

The checked-in Python oracle must remain standard-library-only and import the existing helper. It validates the schema subset used by V1, runs relational/policy checks, confirms all referenced legacy smoke ids exist through the helper parser, and emits normalized JSON results. The guide also documents the preferred full validators:

- Python: `jsonschema` 4.x with Draft 2020-12
- TypeScript: Ajv 8 with the 2020 entry point

The dependency-free oracle is the repository gate; adapters should additionally use their ecosystem's full JSON Schema implementation.

## Explicit non-goals

- no HTTP service, MCP server, daemon, scheduler, database, vector store, embedding index, or background capture;
- no hidden agent/user memory or payload persistence;
- no policy-table duplication inside schemas or fixtures;
- no TypeScript runtime/package added in this tranche;
- no breaking change to the legacy helper CLI or its current bundle/receipt discriminators.

## Worker package

T003 owns only the exact files recorded on its board card. It must implement the full package and all documentation/inventory/checksum updates as one coherent slice.
