# Context Contract V1

This package defines language-independent, read-only wire contracts for:

- `ContextRequestV1` — task intent, bounded selection inputs, and policy references;
- `ContextBundleV1` — selected source metadata and selection/truncation evidence;
- `ContextReceiptV1` — normalized checks, stable reason codes, and scope evidence.

The package is not a service and does not store context. It adds no server,
daemon, database, vector index, background capture, or hidden agent memory.

## Version and schema dialect

All contracts use `contract_version: "1.0"` and JSON Schema Draft 2020-12.
Schemas are standalone and use stable URN identifiers:

```text
urn:agent-memory-kit:context-contract:v1:ContextRequestV1
urn:agent-memory-kit:context-contract:v1:ContextBundleV1
urn:agent-memory-kit:context-contract:v1:ContextReceiptV1
```

V1 intentionally has no cross-file `$ref`, so adapters do not need different
URI registries. Unknown properties are rejected.

## Rule ownership

Schemas validate payload structure only. They do not copy retrieval profiles,
scoring weights, authority tiers, excluded globs, or lifecycle rules. Resolve
the `policy_refs` in each payload against the adopter project's canonical:

```text
docs/project_map/context_index.yaml
docs/project_map/retrieval_policy.yaml
docs/project_map/retrieval_scoring_policy.yaml
```

The existing `context_governance_helper.py` remains the Python reference for
deterministic read-set construction and legacy context-selection smoke cases.
Operational sources remain above Project Map navigation metadata on conflict.

## Portable fixture oracle

`fixtures/context-contract-v1-smoke.json` is the canonical corpus. Each case
contains the exact Request, Bundle, Receipt, expected schema-valid booleans,
policy-valid boolean, and ordered reason codes. Current policy codes are:

- `OVER_RETRIEVAL`
- `UNDER_RETRIEVAL`
- `FORBIDDEN_PATH_SELECTED`
- `STALE_AUTHORITY`

Adapters compare these codes, not validator-specific messages. The corpus also
links applicable cases to existing context-selection smoke ids; the Python
oracle verifies those ids through the existing helper parser.

Run the repository gate:

```bash
python "Agent Kit/kit/tools/context_contract_v1_oracle.py" --format json
```

The gate is dependency-free. It validates the JSON Schema keywords used by
the three checked-in schemas and evaluates cross-payload invariants against
the named policy sources. Production adapters should additionally use a full
Draft 2020-12 validator.

## Python adapter

Use `jsonschema` 4.x when a full validator dependency is acceptable:

```python
import json
from pathlib import Path

from jsonschema import Draft202012Validator

root = Path("Agent Kit/kit/secondary_memory_governance/context_contract_v1")
schema = json.loads((root / "schemas/context-request-v1.schema.json").read_text())
payload = json.loads((root / "examples/valid/context-request-v1.json").read_text())

Draft202012Validator.check_schema(schema)
Draft202012Validator(schema).validate(payload)
```

Construct a bundle by calling the existing helper's `build_read_set()` and
projecting its source metadata into `ContextBundleV1`. Do not copy policy
tables into Python. Resolve `policy_refs`, apply hard gates, then normalize
outcomes to the reason codes in the fixture corpus.

For parity testing, call `run_oracle()` from
`tools/context_contract_v1_oracle.py` or execute its CLI. Treat `case_id`, the
three schema-valid booleans, `policy_valid`, and `reason_codes` as the oracle
comparison tuple.

## TypeScript adapter

Use Ajv 8's Draft 2020-12 entry point:

```typescript
import Ajv2020 from "ajv/dist/2020.js";
import requestSchema from "./schemas/context-request-v1.schema.json" with { type: "json" };

const ajv = new Ajv2020({ allErrors: true, strict: true });
const validateRequest = ajv.compile(requestSchema);

if (!validateRequest(payload)) {
  // Keep local diagnostics for logs only. Do not put Ajv message text into
  // ContextReceiptV1 or fixture expectations.
  throw new Error("ContextRequestV1 schema validation failed");
}
```

Load `fixtures/context-contract-v1-smoke.json` unchanged. For every case:

1. validate `request`, `bundle`, and `receipt` with the three schemas;
2. resolve the same `policy_refs` and apply hard gates before scoring;
3. normalize policy outcomes to the stable reason codes;
4. compare only the oracle tuple described above.

Do not rewrite the fixture data as TypeScript objects and do not use Ajv error
strings as expected results. The JSON file is the shared source for both
languages.

## Compatibility boundary

V1 is a normalized projection over the existing read-only helper surface. It
does not rename or break the legacy `api-context` command, bundle discriminator,
or receipt discriminator. Adapters may support both shapes during migration,
but only the versioned schemas and fixture corpus define Context Contract V1.
