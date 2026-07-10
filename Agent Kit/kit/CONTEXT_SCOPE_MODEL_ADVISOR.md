# Context / Scope / Model Advisor

Status: portable operating guide
Purpose: help the agent choose the smallest sufficient context and the right execution surface/settings before doing expensive or risky work.

---

## 1. Problem

The owner usually cannot know in advance which context will be needed for a task.

A prompt may be under-scoped:

- important Project Map entries are missing;
- source authority is not loaded;
- active task/workstream is absent;
- code is loaded without DB schema, tests, logs, or docs;
- stale memory is loaded as if it were current;
- provider/model settings are guessed from old memory.

A prompt may also be over-scoped:

- the whole repository is loaded for a narrow question;
- raw logs or transcripts are pasted when card summaries would suffice;
- Max Mode or full IDE context is enabled before the need is proven;
- external research is performed when project evidence was the missing piece.

Both failures reduce agent quality. Under-scoping increases wrong answers and wrong patches. Over-scoping increases token burn, latency, usage cost, and instruction conflict risk.

---

## 2. Design goal

Add a lightweight **preflight advisor** before retrieval/hydration and before heavy agent work.

```text
owner task
  -> task intake
  -> intent/risk classification
  -> context-needs estimation
  -> scope sufficiency gate
  -> surface/model/settings routing
  -> compact user hint if needed
  -> hydration request / prompt assembly
  -> answer, plan, audit, or apply
  -> optional trace ref in Working State
```

The advisor does not replace Retrieval Policy. It prepares the retrieval request and warns when the owner-provided scope is likely insufficient or wasteful.

---

## 3. Core principles

### 3.1 Advisory by default

The advisor should not interrupt every simple answer. It should stay silent when scope is adequate and risk is low.

It should show a compact hint when:

- the sufficiency gate is amber, red, or blocked;
- the task is apply, audit, repair, recover, or cross-subsystem debug;
- mandatory context classes are missing;
- the owner directly asks for model/settings/scope guidance;
- a provider capability snapshot is stale or absent;
- Max Mode, full IDE context, or high reasoning looks unjustified or necessary.

### 3.2 Refs over payloads

The advisor should recommend context refs, not paste large file bodies.

Good:

```text
Need: Project Map/source_authority.yaml, active workstream, db_sql schema, affected route file, test command.
```

Bad:

```text
Paste the whole Project Map and repository into the prompt.
```

### 3.3 Scope sufficiency is separate from permission

A task can be allowed but under-scoped. A task can be well-scoped but not authorized for mutation.

The advisor checks both:

- **context sufficiency**: does the agent have enough evidence to produce a grounded result?
- **action safety**: is mutation explicitly authorized, scoped, verified, and free of blockers?

### 3.4 Provider/model facts are volatile

Model lists, pricing, context windows, speed modes, Max Mode behavior, and IDE features change. They must be treated as provider capability snapshots with timestamps and source refs. They are not durable project facts.

### 3.5 Implicit IDE context boundary

Implicit IDE context means open tabs, selections, diagnostics, terminal snippets, editor history, workspace state, or other provider/IDE-supplied context that was not named in the task scope.

This context is **advisory only** unless it is explicitly listed in the task scope or the owner approves it during preflight. A prompt note such as `IDE Context OFF` is a policy marker for the agent; it does not toggle the provider or IDE UI.

If the agent needs to use implicit IDE context to expand read or apply scope, it must first report the needed paths/classes and request owner approval. File changes remain limited to the approved scope. Implicit IDE context must never silently expand write scope.

### 3.6 Cost-aware model routing

The advisor must recommend the **lowest sufficient model/settings class** for the task. It must not recommend the strongest or most expensive model merely as a vague safety default.

A premium/frontier/high/pro route is allowed only when at least one concrete escalation trigger is present, such as:

- cross-subsystem root-cause analysis;
- schema, protocol, retrieval, eval, root-router, or agent-behavior contract changes;
- production-risk code, DB, deploy, git, or side-effect safety;
- audit, repair, recovery, branch-lineage ambiguity, or stale-fact conflict;
- long-horizon synthesis where cheaper models are likely to miss dependencies;
- owner explicitly requests maximum quality after seeing the cost/fuel tradeoff.

For routine work, prefer cheaper settings:

- GPT-5.6-Luna with Low/Medium reasoning and Standard speed: clear extraction, inventory, classification, and repeatable static checks;
- GPT-5.6-Terra with Medium reasoning and Standard speed: routine analysis, planning, task contracts, review, and bounded repair;
- GPT-5.6-Terra or GPT-5.6-Sol with High reasoning and Standard speed: only when difficult repair or ambiguous root cause is present;
- GPT-5.6-Sol with High/XHigh reasoning and Standard speed: hooks, routing, schemas, evals, protocols, or cross-system/production-risk recovery.

Fast is latency-first and increased-usage, not a cheaper substitute for Standard.

When the advisor recommends premium/frontier/high/pro, it must include:

1. the escalation trigger;
2. the cheaper alternative that would normally be sufficient;
3. why the cheaper alternative is not enough for this task.

If no escalation trigger is present, the route should downgrade to medium/standard or ask the owner before using the more expensive setting.


### 3.8 Dated provider/model snapshots

Provider model names, prices, context limits, and UI controls are volatile.
Owner-facing settings advice must use either current owner/provider evidence or a
dated snapshot that is explicitly identified as dated. A dated example is useful
for understanding the policy, but it is not a current recommendation.

The historical snapshot below was captured on 2026-06-10. Do not treat its model
labels as current without refresh.

### 3.9 Current Codex GPT-5.6 snapshot

The source-qualified Codex snapshot was captured on **2026-07-10**:

- `context_advisor/codex_provider_capability_snapshot_2026-07-10.yaml`
- `context_advisor/provider_surface_routing_snapshot_2026-07-10.yaml`

AMK routing uses Terra Medium/Standard for routine analysis and contract work,
Luna Low/Medium for clear repeatable extraction, and Sol High/XHigh only for
protocol or cross-system risk. Sol Max is one hardest sequential problem.
Sol/Terra Ultra is delegation and requires independent scopes, stop conditions,
and fuel justification. Luna Ultra is unsupported by the local snapshot.

Keep full structured controls separate, but keep owner-facing prompt tuples
surface-specific and minimal. The current desktop id is
`chatgpt_desktop_codex`; `codex_app` is its compatibility alias. `codex_ide`
is the distinct current Codex IDE extension.

### 3.10 Historical Cursor model snapshot example

When the owner asks which Cursor model/settings to use, the advisor must rely on a dated provider snapshot, not memory. The v3.9.3 snapshot was collected on **2026-06-10** from owner-observed Cursor UI plus Cursor docs/blog/forum sources.

Historical working set in the captured example:

| Model | Snapshot controls | Default role | Default rule |
|---|---|---|---|
| Composer 2.5 | Fast on/off only | routine Cursor-agent workhorse | default for Project Map, owner-provided facts, small docs/root-router edits, mechanical package merges |
| GPT-5.5 | Fast; 272K/1M context; reasoning none/low/medium/high/extra high | frontier reasoning escalation | medium first; high/extra high only with concrete escalation trigger |
| Codex 5.3 | Fast; reasoning low/medium/high/extra high | code/test/repair specialist | medium first; high for failing tests or multi-step repair loop |
| Sonnet 4.6 | Thinking; 200K/1M context; effort low/medium/high/max | balanced code/docs fallback | medium effort first; 1M/thinking/high only with reason |
| Opus 4.8 | Thinking/Fast; 300K/1M context; effort low/medium/high/extra high/max | premium architecture/audit fallback | not default; requires escalation reason |
| Fable 5 | Thinking; 300K/1M context; effort low/medium/high/extra high/max | premium emergency coding-agent fallback | not default; requires escalation reason |
| Auto | provider-routed | optional cheap/non-deterministic route | use only when exact model repeatability is not important |

Do not add more models to the routing set merely because they are available. Add a model only when:

1. the current set fails a concrete task class;
2. the owner requests benchmarking;
3. the provider changes availability/pricing enough to justify a snapshot refresh.

If recommending 1M context, Max Mode, Fast, premium models, high/extra/max effort, or high/extra-high reasoning, the advisor must show the escalation trigger and cheaper sufficient alternative.

### 3.11 Historical Cursor snapshot boundary

Exact Cursor model advice must name the provider snapshot date or say that the snapshot is missing/stale.

The v3.9.3 example snapshot is `context_advisor/cursor_provider_model_snapshot_2026-06-10.yaml`, captured on 2026-06-10. It records owner-observed Cursor UI controls plus Cursor docs/forum refs. It is a volatile operational snapshot, not permanent project truth.

For the historical 2026-06-10 snapshot, the Cursor Agent set was sufficient with surplus on its capture date:

- Composer 2.5 — default working horse;
- GPT-5.3 Codex — code/test/repair executor;
- GPT-5.5 — hard reasoning escalation, not narrow-update default;
- Sonnet 4.6 — balanced review/refactor alternative;
- Opus 4.8 — rare hard planning/audit escalation;
- Fable 5 — rare long-running autonomous agentic escalation.

That Cursor snapshot expired on 2026-07-10. Preserve its model list unchanged,
report it as stale/pending refresh, and do not infer GPT-5.6 Cursor availability
from current Codex evidence. Optional models should not enter default routing
without current evidence, a capability gap, a cheaper alternative, and owner approval.

### 3.8 User-facing hints must be compact

Default hint format:

```text
ContextAdvisor: gate=<green|amber|red|blocked>; missing=<classes/refs>; route=<surface/model-class/reasoning/cost>; settings=<CursorMax/CodexMax/delegation/IDE/Plan/speed>; action=<proceed|ask|discovery|block>.
```

Expanded reasoning appears only on direct ask: `settings?`, `scope?`, `fuel?`, `why?`, or `safe apply?`.

---

## 4. Gate levels

| Gate | Meaning | Default action |
|---|---|---|
| `green` | Scope and settings are sufficient for the requested intent. | Proceed. |
| `amber` | Work can proceed, but a missing or noisy context risk should be shown. | Proceed with compact warning or run read-only discovery. |
| `red` | Required context or safety proof is missing. | Ask for refs/scope or perform read-only discovery only. |
| `blocked` | Secrets, unauthorized mutation, duplicate side-effect risk, unsafe DB/deploy/git action, or branch leakage risk. | Stop until owner resolves blocker. |

---

## 5. Context classes

Use these classes instead of asking for vague “more context”.

| Class | Examples |
|---|---|
| `project_map_core` | `current_state.md`, `working_state.yaml`, permissions, retrieval policy. |
| `source_authority` | `source_authority.yaml`, declared source-of-truth order. |
| `memory_relevant` | memory index and specific fact/decision/constraint/risk cards. |
| `active_workstream` | current workstream, task contract, checkpoint, handoff. |
| `progress_logs` | WORKLOG, `.agent-progress`, recent verified run notes. |
| `routes_contracts` | route files, API reference, OpenAPI docs. |
| `services_logic` | domain/service calculation code and docs. |
| `db_schema` | SQL schema, ORM models, migration files. |
| `scraper_jobs` | scraper entrypoints, schedules, cache invalidation matrix. |
| `redis_cache` | cache usage docs, invalidation paths, Redis keys. |
| `mt_client` | MetaTrader client files and contracts. |
| `tests` | unit/integration tests and verification commands. |
| `runtime_logs` | tracebacks, server logs, scraper logs, browser/noVNC logs. |
| `external_current_docs` | provider/library docs retrieved in the current run. |
| `screenshots_ui` | screenshots needed for UI/settings interpretation. |
| `secrets` | access files, credentials, tokens; always forbidden. |

---

## 6. Routing policy

The advisor recommends a surface, not a guarantee.

| Task type | Default surface | Model/settings class |
|---|---|---|
| Project answer | ChatGPT Codex; Cursor read-only is an alternative after current Cursor evidence is checked | ChatGPT Codex: GPT-5.6-Terra with Medium reasoning and Standard speed; Luna only for clear extraction. Do not project this model tuple onto Cursor. |
| Architecture/spec/memory-kit design | ChatGPT Codex | Terra Medium first; Sol High/XHigh for schema/protocol/eval/router changes. |
| Bounded repo patch | Cursor Agent or ChatGPT Codex, selected by task fit | Composer 2.5 or another current evidence-supported Cursor route for mechanical apply; ChatGPT Codex Terra Medium/Standard for reasoning-heavy repair. Refresh Cursor evidence before exact current Cursor settings. |
| Multi-file root-cause debug | ChatGPT Codex; Cursor Agent remains a valid executor-loop alternative | ChatGPT Codex: Terra High or Sol High, plan first, logs/tests/schema included. Cursor exact model/settings require current Cursor evidence. |
| Independent diff review | ChatGPT Codex; Cursor read-only reviewer is an alternative after current Cursor evidence is checked | ChatGPT Codex: Terra Medium/High with exact diff refs. Do not reuse that tuple as a Cursor claim. |
| External current docs research | GPT web | current citations, external facts not project truth. |
| Package/handoff update | Cursor for mechanical apply; ChatGPT Codex for protocol reasoning | Composer 2.5 for merge/version/checksum; Sol High for behavior/schema/router/eval/protocol changes. |

---

## 7. Default settings policy

| Setting | Default | Escalate only when |
|---|---|---|
| Max Mode / huge context | Off | exact required context exceeds normal window or many refs must be co-read. |
| Include IDE Context | Off | open files are exactly the intended scope and owner-approved; otherwise implicit IDE context is advisory only. |
| Plan Mode | Off for direct answers; on for complex apply/debug/audit. | the task touches multiple files/subsystems or has uncertain root cause. |
| Speed | Standard | use fast only for low-risk draft/exploration where quality cost is acceptable. |
| Reasoning | Medium | high only for concrete escalation triggers: cross-subsystem, schema/protocol/eval/router changes, audit, repair, recovery, production-risk, side-effect safety. |
| Codex Max | Off | one hardest sequential problem with an explicit depth-over-usage trigger. |
| Codex Ultra delegation | Off | independent scopes, per-scope stop conditions, fuel justification, and supported Sol/Terra evidence. |
| External research | Off unless requested or needed for volatile external facts. | model/provider/library/regulatory facts may have changed. |

---

## 8. Integration with Retrieval Policy

Context Advisor runs before `memory.hydrate`.

It emits:

- `ContextNeedsManifest`;
- `ScopeSufficiencyReport`;
- `RoutingRecommendation`;
- `HydrationRequestDraft`;
- `ContextAdvisorTrace`.

Retrieval Policy then decides which memory classes and refs are actually loaded under the active profile.

---

## 9. Integration with Working State

Working State may store refs to advisor outputs:

```yaml
context_advisor:
  latest_trace_ref: "Project Map/runtime/context_advisor/CTX-0007.json"
  latest_context_needs_ref: "Project Map/runtime/context_advisor/CTX-0007.context_needs.json"
  provider_capability_snapshot_ref: "Project Map/provider_capabilities/provider_surface_routing_2026-07-10.yaml"
```

Do not store full traces, large inventories, raw logs, or provider docs in Working State. Store refs.

---

## 10. On-demand owner commands

Use these when the owner wants an explicit explanation:

```text
settings?   Explain surface/model/reasoning/speed/context choice, cost class, escalation trigger, cheaper alternative, and why not cheaper if premium is recommended.
scope?      List mandatory/recommended/optional/forbidden context refs.
fuel?       Show compact token/fuel plan: keep/defer/drop; Max/IDE context yes/no.
safe apply? Check mutation gate: target, scope, owner OK, verification, side effects.
```

---

## 11. Failure modes

| Failure | Guard |
|---|---|
| Under-scoped task produces confident wrong patch. | Red/amber gate plus read-only discovery. |
| Whole-project over-retrieval. | Context class matrix and token budget plan. |
| Stale fact poisoning. | Retrieval profile suppresses stale facts outside audit/repair/recover. |
| Provider/model settings drift. | Timestamped provider capability snapshots with TTL and captured date in exact model advice. |
| Duplicate side effect. | Working State side-effect receipts and idempotency checks. |
| Branch leakage. | Branch/checkpoint scope rules before hydration. |
| Secret exposure. | Forbidden context class and blocking trigger. |
| Advisor noise. | Silent default; compact hints only on risk or direct ask. |
| Over-expensive model routing. | Lowest-sufficient model rule; premium/high/pro requires escalation reason plus cheaper alternative. |
| Unnecessary model-list expansion. | Keep core set; optional models require capability gap, cheaper alternative, and owner approval. |

---

## 12. Minimal copy-paste preflight

```text
Run ContextAdvisor preflight first.
Task: <one goal>
Mode: answer|analyze|plan|apply|audit|repair|debug|research
Scope: <exact refs or unknown>
Risk: low|medium|high|critical
Need: <expected output>
Return compact gate/settings/scope hint only if amber/red/blocked or if settings/scope are requested.
```


## v3.9.3 Auto/Max explicit boundary

Auto is not a specific model. For owner-controlled project work, do not recommend Auto as the default route unless the owner explicitly accepts non-deterministic provider/model routing for low-risk exploration.

Max Mode is a separate Cursor-level capacity toggle for explicit models except Auto. Keep Max OFF by default; recommend 1M/Max only with context-overflow, broad-audit, large multimodal context, or explicit owner approval.

## v3.11.1 dated surface/model routing snapshot

For exact model/mode advice, ContextAdvisor uses the 2026-07-10 provider-surface
and Codex capability snapshots. Generic service routing remains separate from
exact model routing:

- Cursor Agent / Composer 2.5: strong clear scoped implementation workhorse.
- ChatGPT desktop app (Codex mode): analysis, planning, task contracts, independent review,
  evidence-chain verification, and repair/recovery.
- GPT web: deep/current external research; no direct repository authority.

The current Codex family is GPT-5.6-Sol, GPT-5.6-Terra, and GPT-5.6-Luna.
Standard is the default speed. Max is single-task reasoning. Ultra is delegation
for independent scopes. Cursor Max Mode remains a separate capacity control.

The local cache exposes GPT-5.6 Fast, while the checked public Speed page names
GPT-5.5 and GPT-5.4; no fixed GPT-5.6 Fast credit multiplier is asserted. The
2026-06-10 Cursor snapshot is expired, so current GPT-5.6 Cursor availability is
missing evidence.

When recommending ChatGPT Codex prompt-time choices, output only
`ChatGPT Codex / model / reasoning / speed`. Do not append Fast/Max/Ultra off,
IDE context, shell, terminal profile, or application configuration. Recommend
Composer, Codex, or both when task evidence shows comparable executor fit.
