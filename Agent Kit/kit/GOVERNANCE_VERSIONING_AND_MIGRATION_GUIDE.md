# Governance Versioning and Migration Guide

Release: v5.0.0

Governance contracts and templates use explicit versions. A breaking change
removes or reinterprets a field, tightens a previously valid lifecycle, or
changes authority, permission, or promotion semantics. Breaking changes
require a major Kit release, a migration note, the full core eval suite, and
owner review before adoption.

Every governed contract declares:

```yaml
governance:
  contract_version: "2.0"
  supersedes: "<prior-contract-or-null>"
  effective_from: "<YYYY-MM-DD>"
  compatibility: "breaking|additive|compatible"
  migration_note: "<what adopters must review>"
```

Unknown versions fail closed. Migration preserves IDs, evidence, lifecycle,
and authority. Missing v4 fields become `unknown`, `pending`, or an explicit
owner-review obligation; they are never reconstructed from chat or model
guessing.
