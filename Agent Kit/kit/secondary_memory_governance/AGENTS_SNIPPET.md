## Secondary-Memory Governance Overlay

This project uses `docs/project_map/` as secondary memory and navigation.
Operational docs, code, tests, specs, issues, and current owner instructions win
over Project Map on conflicts.

Minimum governance refs:

- `docs/project_map/source_authority.yaml`
- `docs/project_map/permissions_policy.yaml`
- `docs/project_map/retrieval_policy.yaml`
- `docs/project_map/retrieval_scoring_policy.yaml`
- `docs/project_map/memory_lifecycle_policy.yaml`
- `docs/project_map/working_state.yaml`

Apply retrieval hard gates before scoring. Similarity, entity links, or
embeddings must not override source authority, stale suppression, scope,
branch, permission, security, privacy, or owner-decision boundaries.

Question, analyze, review, and plan requests do not authorize mutation.
Scoped read-only repository exploration is allowed when needed for the current
coding task, but it does not authorize file writes, durable memory updates,
external service calls, database writes, broker/account mutations, commits,
pushes, or deploys.

Project Map updates require explicit memory-update intent or an approved delta.
New durable memory starts as candidate or staged unless evidence and owner or
review rules explicitly promote it. Stale, superseded, rejected, and archived
records are not current truth in normal answer, plan, or resume profiles.
Ignore files are context hygiene only, not secret protection.
