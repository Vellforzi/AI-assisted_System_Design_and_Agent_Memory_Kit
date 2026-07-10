# Memory Tool Interface Contract

Status: implementation-facing guidance
Purpose: define how a memory tool, file-backed memory helper, MCP server, database API, or IDE extension should expose Project Map memory to agents.

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

---

## 2. Recommended operations

| Operation | Purpose |
|---|---|
| `memory.search` | Search index/cards by query, tags, class, status, scope, branch, and profile. |
| `memory.read` | Read exact memory units by ID. |
| `memory.hydrate` | Build profile-specific context bundle from Working State and retrieval policy. |
| `memory.read_policy` | Read source authority, permissions, and retrieval policies. |
| `memory.classify_intent` | Classify answer/analyze/plan/stage/apply intent conservatively. |
| `memory.check_permission` | Check whether requested action is allowed by current intent, mode, and scope. |
| `memory.write_candidate` | Stage unverified candidate memory. |
| `memory.promote` | Promote candidate to durable memory after evidence/approval. |
| `memory.update_lifecycle` | Mark stale, superseded, rejected, archived, or verified. |
| `memory.link` | Add relationships between memory units. |
| `memory.claim_check` | Validate claim ledger entries before final answer. |
| `memory.create_handoff` | Create a clean-slate continuation packet. |
| `memory.receipt_check` | Check side-effect receipts before repeating actions. |
| `memory.record_receipt` | Record completed external side effect. |
| `memory.advise_context` | Run pre-hydration Context Advisor: classify task, estimate context needs, gate scope sufficiency, and recommend surface/settings. |
| `memory.read_provider_capabilities` | Read a timestamped provider capability snapshot for volatile model/settings decisions. |

These are conceptual operations. Implementations may use different names.

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


---

## 11. Context Advisor operation

A memory tool may expose `memory.advise_context` before `memory.hydrate`.

Input should include:

```yaml
task: "<owner request>"
intent: answer|analyze|plan|apply|audit|repair|recover|resume|debug|research
mode: explain-only|dry-run|read-only|apply
current_scope_refs: []
known_context_classes: []
mutation_kind: none|docs|code|memory|db|deploy|git|external
owner_ok: false
verification_provided: false
```

Output should include:

```yaml
gate: green|amber|red|blocked
missing_mandatory_context: []
over_broad_refs: []
unsafe_refs: []
routing_recommendation:
  surface: cursor_agent|chatgpt_desktop_codex|codex_ide|codex_cli|codex_web|gpt_web
  surface_display_label: "<current exact client label>"
  model_or_model_class: "<volatile; from snapshot if needed>"
  reasoning: medium|high|extra_high|provider_default
  speed: standard|fast|provider_default
  max_mode: on|off|auto
  include_ide_context: on|off|only_exact_open_files
  owner_prompt_tuple:
    surface: "<owner-facing surface label>"
    model: "<exact model display label>"
    reasoning: "<selected reasoning effort>"
    speed: "<selected speed when exposed>"
compact_hint: "ContextAdvisor: ..."
hydration_request_draft: {}
```

The operation must not read secrets, load whole-project payloads by default, or treat provider capability snapshots as durable project facts. It must not pad the owner prompt tuple with derived off states, IDE context, shell, terminal profile, or application configuration unless the owner asked for those settings.
