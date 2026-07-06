# Retrieval Policy Profiles

Status: portable policy guide
Purpose: define how an agent should hydrate project memory for different task types without loading too much, missing required context, using stale facts as current truth, or executing work when the owner only asked for an answer.

---

## 0. Context Advisor preflight

Before retrieval/hydration for non-trivial work, run Context Advisor if scope, settings, or risk are unclear.

Context Advisor decides:

- whether the current scope is sufficient;
- which context classes are mandatory, recommended, optional, or forbidden;
- whether a read-only discovery step is safer than immediate work;
- which surface/model class/reasoning/speed/context mode should be used;
- whether provider capability snapshots are needed.

Retrieval Policy still controls what is actually loaded. Context Advisor prepares the hydration request and compact user hint.

---

## 0.5 Generated retrieval evidence

Generated search or index output is retrieval evidence only. It may help narrow a
candidate source set, but it does not prove a project fact.

Before answering, reviewing, planning, or applying based on a generated hit, the
agent must reopen the canonical source file and verify the relevant line range
or section.

Examples include SQLite/FTS indexes, semantic search caches, MCP metadata
caches, generated context packs, and ranked snippets.

---

## 1. Core retrieval rule

Retrieve the smallest set of high-signal context that can satisfy the current intent with grounded output.

Default order:

1. current user instruction;
2. Action Intent Contract and Permissions Policy;
3. Source Authority;
4. Retrieval Policy;
5. Working State;
6. current state;
7. active task contract;
8. active workstream;
9. memory index;
10. relevant memory cards;
11. project files or tool outputs if in scope;
12. raw sources only when required.

---

## 2. Profile matrix

| Profile | Main purpose | Stale facts | Raw sources | Mutation |
|---|---|---|---|---|
| `answer` | answer a project question | suppressed unless labeled | only if proof needed | forbidden |
| `analyze` | review/diagnose/compare without changes | labeled only | allowed if needed | forbidden |
| `plan` | plan next work | suppressed unless risk context | rarely | forbidden |
| `resume` | continue active task | suppressed | only if checkpoint insufficient | forbidden unless separate apply intent exists |
| `recover` | recover lost/failed state | diagnostic only | allowed when needed | forbidden by default |
| `fork` | explore alternate branch | current shared facts only | rarely | forbidden |
| `audit` | verify or inspect correctness | allowed and labeled | allowed | forbidden by default |
| `repair` | fix memory/project inconsistency | allowed as repair input | allowed | requires explicit apply |

---

## 3. `answer` profile

Use when the user asks a direct question about the project.

Allowed memory:

- `fact_current`
- `accepted_decision`
- `constraint`
- `risk`
- relevant `procedure`
- current workstream summary if relevant
- open questions if relevant to missing evidence

Blocked by default:

- `fact_stale` as valid context;
- `hypothesis` as fact;
- `research_output` as project fact;
- raw chat as authority;
- branch-local facts from unrelated branches.

Behavior:

1. Retrieve current state and relevant memory cards.
2. Answer only from supported evidence.
3. Mark inference where needed.
4. If evidence is missing, say so.
5. Do not write memory unless the user asked to remember or apply.
6. Do not execute any proposed next step.

---

## 4. `analyze` profile

Use when the user asks to review, compare, inspect, audit lightly, diagnose, or reason without applying changes.

Allowed memory:

- current state;
- relevant facts and decisions;
- constraints;
- risks;
- procedures;
- open questions;
- hypotheses if labeled;
- research output if labeled;
- stale facts only when relevant to conflict or risk.

Behavior:

1. Perform read-only context intake inside scope.
2. Separate facts, inferences, risks, and proposals.
3. Produce findings or recommendations.
4. Do not fix, rewrite, execute, or update durable memory unless separately instructed.

---

## 5. `plan` profile

Use when the user asks for a plan, next step, implementation instruction, or task breakdown.

Allowed memory:

- current state;
- active task contract;
- active workstream;
- accepted decisions;
- constraints;
- risks;
- open questions;
- relevant facts and procedures.

Behavior:

1. Load active task and constraints first.
2. Identify blockers and unknowns.
3. Produce a scoped plan with no hidden assumptions.
4. Distinguish facts, assumptions, and owner decisions.
5. Do not imply permission to execute.

---

## 6. `resume` profile

Use when continuing an active task.

Mandatory context:

- `working_state.yaml`;
- active `tasks/TASK-xxxx.yaml` if present;
- active workstream file;
- checkpoint ID;
- latest handoff if resuming after pause;
- mandatory memory refs;
- pending obligations;
- blockers;
- side-effect receipts.

Behavior:

1. Restore from Working State, task contract, and handoff state, not from chat memory.
2. Load only mandatory refs plus directly relevant cards.
3. Check whether pending actions were already completed.
4. Continue from the recorded cursor.
5. If checkpoint is incompatible or missing, switch to `recover`.
6. Do not perform a mutating next step unless current user instruction explicitly asks to apply.

---

## 7. `recover` profile

Use when context is lost, a session failed, state is inconsistent, or a tool returned partial output.

Allowed memory:

- Working State;
- handoff/session notes;
- task contract;
- side-effect receipts;
- stale facts as diagnostic context;
- raw sources if needed;
- recent worklog entries.

Behavior:

1. Reconstruct the latest safe checkpoint.
2. Identify completed, pending, and unsafe-to-repeat actions.
3. Rebuild a minimal current state.
4. Mark uncertain reconstruction as inference.
5. Ask owner before repeating side effects.
6. Return a recovery summary and next safe step.

---

## 8. `fork` profile

Use when exploring an alternative branch, scenario, or design option.

Behavior:

1. Load shared stable memory.
2. Load only branch-local facts for the selected branch.
3. Do not read future facts from another branch unless explicitly merged.
4. Mark branch assumptions.
5. Keep fork output separate from main durable memory until owner accepts it.

---

## 9. `audit` profile

Use when checking correctness, consistency, source support, or memory quality.

Allowed memory:

- current facts;
- stale facts;
- superseded facts;
- rejected decisions;
- raw sources;
- source authority;
- conflicts;
- evidence trails;
- claim ledger.

Behavior:

1. Load current memory and conflicting/stale related memory.
2. Escalate to raw evidence where needed.
3. Report unsupported claims and contradictions.
4. Do not mutate memory by default.
5. Produce a proposed repair plan if required.

---

## 10. `repair` profile

Use when fixing Project Map memory, stale state, broken links, duplicate cards, claim ledger defects, or source-authority problems.

Allowed memory:

- all relevant current/stale/superseded/conflicting units;
- candidate memory;
- raw evidence;
- session notes;
- index files;
- claim ledger;
- task/handoff artifacts.

Behavior:

1. Identify the defect.
2. Preserve historical facts instead of deleting them silently.
3. Add supersession links.
4. Move unverified claims to candidate or hypothesis status.
5. Require apply/write permission before changing files.

---

## 11. Empty-result recovery

If retrieval returns nothing or too little:

1. Retry with broader tags or adjacent workstream terms.
2. Check current state and source-authority files.
3. Ask whether scope can be expanded.
4. If still missing, answer with `[missing evidence]`.
5. Do not manufacture a project answer.

---

## 12. Eval review profile usage

Eval-suite review is not a separate default interaction profile. It uses:

- `audit` when checking outputs, traces, claim ledgers, or behavior against eval cases;
- `repair` only when the owner explicitly asks to update eval cases, Project Map memory, or instruction files.

Allowed eval artifacts:

- `eval_case`;
- `eval_result`;
- `eval_trace`;
- manual review notes;
- confirmed failure reports.

Rules:

1. Failed evals do not automatically prove the agent is wrong; they identify behavior that requires owner review.
2. Passing evals do not prove the agent is safe or correct; they only show that known cases passed.
3. New real failures should become new eval cases after the owner confirms that the failure mode is worth preserving.
4. Eval artifacts are diagnostic memory, not project domain truth.

---

## 13. Token budget strategy

Prefer:

- policy summary before full policy file;
- index before full card;
- card summary before details;
- concise tool response before detailed response;
- relevant raw excerpt before full raw source;
- multiple targeted searches before one broad dump.

If truncation occurs, the response must say what was omitted and how to retrieve more.
