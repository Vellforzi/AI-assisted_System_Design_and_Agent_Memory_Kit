# Memory Tool Interface Contract

Status: implementation-facing guidance  
Purpose: define how a file-backed memory helper, project API, or IDE extension should expose Project Map memory to agents.

---

## 1. Tool design goals

A memory tool should return high-signal context, not a dump.

It should help the agent:

- find relevant memory quickly;
- distinguish current from stale facts;
- see evidence and authority;
- enforce action intent and permission policy;
- avoid branch leakage;
- choose concise or detailed output;
- recover from empty or truncated results;
- write candidate memory safely;
- check claim support;
- create clean handoffs;
- avoid duplicate side effects.
- keep raw tool outputs compact and evidence-addressable.

---

## 2. Recommended operations

| Operation | Purpose |
|---|---|
| `memory.search` | Search index/cards by query, tags, class, status, scope, branch, and profile. |
| `memory.read` | Read exact memory units by ID. |
| `memory.hydrate` | Build profile-specific context bundle from Working State and retrieval policy. |
| `memory.read_policy` | Read source authority, permissions, and retrieval policies. |
| `memory.score` | Score already-gated retrieval candidates according to retrieval scoring policy. |
| `memory.classify_intent` | Classify answer/analyze/plan/stage/apply intent conservatively. |
| `memory.check_permission` | Check whether requested action is allowed by current intent, mode, and scope. |
| `memory.write_candidate` | Stage unverified candidate memory. |
| `memory.promote` | Promote candidate to durable memory after evidence/approval. |
| `memory.update_lifecycle` | Mark stale, superseded, rejected, archived, or verified. |
| `memory.link` | Add relationships between memory units. |
| `memory.claim_check` | Validate claim ledger entries before final answer. |
| `memory.create_handoff` | Create a clean-slate continuation packet. |
| `memory.record_tool_output_ref` | Record a compact reference to long raw tool output. |
| `memory.receipt_check` | Check side-effect receipts before repeating actions. |
| `memory.record_receipt` | Record completed external side effect. |
| `commitment.open` | Record a planned action and expected outcome before execution. |
| `commitment.settle` | Append terminal success, failure, or cancellation with provenance and outcome evidence. |
| `artifact.describe` | Return ArtifactDescriptorV1 metadata without promoting content. |
| `artifact.inspect_bounded` | Return ArtifactExcerptV1 within explicit byte/line caps. |
| `verification.record_receipt` | Record a deterministic verification result linked to claims. |

Unknown contract versions and unknown fields fail closed. Helpers must not rewrite terminal commitments. `self` provenance is advisory and cannot authorize automatic promotion. Full artifact loading requires an explicit profile or owner trigger; summaries and extracts remain navigation-only.

These are conceptual operations. Implementations may use different names.

Retrieval must apply hard gates before scoring:

```text
profile
-> allowed memory classes
-> allowed lifecycle states
-> branch/scope boundary
-> source authority boundary
-> permission boundary
-> security/privacy boundary
-> scoring
-> dynamic top-k
-> compact context bundle
```

A high score must not bypass source authority, stale suppression, scope, branch, permission, security, privacy, or explicit owner-decision rules.

---

## 3. Required result fields

Every memory retrieval result should include:

```yaml
id: FACT-0001
class: fact_current
status: current
review_state: verified
scope: api.routes
branch_scope: main
title: "Routes source of truth"
summary: "Routes are documented in docs/ROUTES_REFERENCE.md and code lives in Options_api/app/routes/."
evidence_refs:
  - "docs/ROUTES_REFERENCE.md:10-45"
last_verified_at: "2026-06-08"
confidence: high
authority_rank: 2
freshness: current
retrieval_tags: [api, routes]
truncated: false
```

Do not return a memory unit without status and evidence metadata unless the caller explicitly requests raw mode.

For hydration results, return omitted-result metadata:

```yaml
profile: resume
intent: plan
policy_refs:
  - "Project Map/retrieval_policy.yaml"
  - "Project Map/source_authority.yaml"
mandatory_context:
  working_state: "..."
retrieved_memory:
  - id: FACT-0001
    class: fact_current
    status: current
    review_state: verified
    summary: "..."
    evidence_refs: ["..."]
omitted:
  stale_suppressed: 4
  below_score_threshold: 9
warnings:
  - "No side-effect receipts found for active task."
```

---

## 4. Response formats

Support at least two response modes:

- `concise`: IDs, titles, summaries, evidence refs, lifecycle fields.
- `detailed`: full card payload plus selected raw evidence excerpts.

Default to `concise`.

---

## 5. Pagination and filtering

Any operation that can return many results must support:

- limit;
- offset or cursor;
- class filter;
- status filter;
- scope filter;
- branch filter;
- date/freshness filter;
- authority filter;
- response format.

If results are truncated, say so and return a continuation cursor.

---

## 6. Natural identifiers

Use human-readable IDs:

- `DEC-0001`
- `FACT-0007`
- `RISK-0003`
- `TASK-0001`
- `HO-0001`
- `CLM-0001`
- `WS-001`
- `CKPT-0004`
- `SE-0002`

Opaque UUIDs may exist internally, but the agent-facing layer should expose meaningful IDs.

---

## 7. Empty result behavior

An empty result must return actionable guidance:

```yaml
status: empty
query: "routes reference"
profile: answer
suggested_next_steps:
  - "Retry with tags: api, routes"
  - "Check Project Map/source_authority.yaml"
  - "Ask owner for read-only scope to docs/ROUTES_REFERENCE.md"
```

Do not let the agent treat an empty retrieval as proof that something does not exist.

---

## 8. Error behavior

Errors should be specific and repairable.

Bad:

```text
Error: invalid request
```

Good:

```yaml
error: invalid_status_filter
message: "status='active' is not valid for memory class fact_current. Use current, stale, superseded, rejected, or archived."
retry_hint: "Set status=current or omit status."
```

---

## 9. Write safety

Memory writes should be staged unless the caller has explicit apply/write permission and explicit memory-write intent.

For durable writes, require:

- memory class;
- summary;
- scope;
- evidence;
- source authority;
- lifecycle status;
- owner approval flag or verification basis.

Reject writes that attempt to store unsupported assumptions as verified facts.

`memory.write_candidate --dry-run` or equivalent should show proposed memory updates without writing when the owner did not explicitly request memory mutation.

---

## 10. Intent and permission enforcement

A memory/runtime tool should reject mutating operations when:

- current intent is `answer`, `analyze`, `plan`, or `retrieve_context`;
- permission mode is not `apply`;
- scope is missing;
- target is ambiguous;
- source authority conflict is unresolved;
- claim gate fails;
- side-effect receipt check is required and missing.

Example rejection:

```yaml
error: mutation_not_allowed_for_intent
intent: answer
requested_operation: memory.promote
message: "The owner asked a question. Durable memory promotion requires explicit memory-write intent."
retry_hint: "Return a proposed memory delta instead."
```

---

## 11. Claim checking

The tool should support claim checking for complex answers.

`memory.claim_check` should return:

```yaml
status: fail
unsupported_claims:
  - CLM-0003
conflicts: []
stale_as_current: []
required_action: "remove or relabel unsupported project claims before final answer"
```

A failed claim check should block final project assertions, not block a missing-evidence answer.

---

## 12. Side-effect receipts

For actions outside memory retrieval, the tool should support receipts or idempotency keys.

Before replaying or recovering a task, the agent should call receipt check if available.

## 13. Tool-output references

Long tool outputs should be recorded as compact references, not pasted into current durable memory:

```yaml
id: TO-0001
created_at: "2026-06-13T12:00:00Z"
source_tool: "rg"
command_or_operation: "rg -n retrieval"
scope: "<repo-or-folder>"
full_output_ref: "Project Map/raw_sources/tool_outputs/TO-0001.txt"
excerpt:
  summary: "Search found retrieval policy and stale suppression references."
  relevant_ranges:
    - "120-180"
byte_count: 184231
retention_policy: "keep_until_task_closed"
sensitivity: "normal"
linked_task: "TASK-0001"
```

Do not store secrets, tokens, private account IDs, raw external-system/account payloads, or raw private user data. If output is sensitive, store only a digest or summary and state the limitation.

## 14. v5 workflow projections

Workflow tools are report-only by default. They may derive a WorkItemGraph or ExplorationMap frontier, the latest valid CapabilityRegistry status, and TriageLedger readiness. Responses must include `read_only: true`, `navigation_only: true`, `activated: false`, and `files_modified: false`.

A projection is not a scheduler, assignment, owner decision, review acceptance, repair permission, prototype promotion, or capability promotion. Mutating workflow artifacts requires an explicit TaskContractV3 apply scope and every activated owner/evidence gate.
