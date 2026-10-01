# AGENTS.md — Agent Memory Kit Repository Entrypoint

Purpose: route repository-aware agents to the Project Map and enforce safe default behavior.

## Core contract

- The Project Map is the source of durable project memory.
- Built-in model knowledge is not project-specific truth.
- Answer-only is the default intent.
- Reading context is not permission to mutate files, memory, git state, databases, deployments, or external systems.
- If project evidence is missing, say so. Do not invent project facts.
- Non-trivial task contracts, bootstraps, task blocks, and model/service recommendations require an Executor Routing Gate.
- Encoding-sensitive or UI-visible text edits require byte-safe tooling and readback verification.
- Blocking hooks should return actionable recovery fields, and agents should follow them.

## Human and model capability boundary

Agent Memory Kit is a multiplier, not a brain. It does not make every model
sufficient and it does not replace the project owner's judgment.

- Answer questions about the kit through the agent from current kit files.
- Choose the model for the required result and reasoning risk; optimize cost only
  after the capability floor is met.
- If the current model cannot preserve owner meaning, reconcile evidence or use
  the installed controls, name the gap and reroute rather than lowering the
  quality standard.
- Keep goals, product semantics, material trade-offs, durable truth and final
  acceptance with the human owner.
- Treat provider model labels as volatile; dated owner examples are evidence, not
  permanent defaults.

Read `HUMAN_MODEL_CAPABILITY_CONTRACT.md` before material adoption or routing
advice.

## Product semantics and production quality controls

The owner's stated product behavior is the authority for required behavior.
Current production code establishes existing behavior and integration constraints
that must be preserved unless the owner explicitly changes them.

Missing instruction means preserve current behavior. It does not authorize a new
default, fallback, relationship, state transition, schedule, retry, cache rule,
persistence rule, error behavior, user-visible result, trading action or public
contract.

Tests, documentation, comments, plans, previous agent reports and model inference
are evidence only. They must not create, replace or silently reinterpret product
semantics.

For a project that adopts the production quality pack:

- specialize `PRODUCT_CODE_CHANGE_POLICY.template.yaml` into a project policy;
- create one task-local `CODE_CHANGE_CONTRACT.yaml` from the supplied template;
- install and apply `$production-engineering-standard` before the first technical
  decision and through implementation, diff review and verification;
- install and apply `$complete-technical-communication` before every owner-facing
  report, generated explanation, documentation page, comment, handoff or release
  note;
- allow causal file-scope expansion required by the exact owner outcome, but never
  treat another file as permission for another behavior;
- trace every changed production symbol to an owner acceptance criterion or a
  preserved invariant;
- ask the owner only when an unresolved assumption can change observable product
  semantics; do not ask about internal choices with identical behavior;
- complete semantic, causal-chain, failure, lifecycle, performance and resource
  review before relying on tests or declaring completion.

These quality controls do not authorize writes or external side effects. The
current owner request and project policy remain the authority for action.

## Read order for project questions

1. `Project Map/README.md`
2. `Project Map/current_state.md`
3. `Project Map/working_state.yaml`
4. `Project Map/source_authority.yaml`
5. `Project Map/permissions_policy.yaml`
6. `Project Map/retrieval_policy.yaml`
7. Active task contract in `Project Map/tasks/` if the user references one.
8. Relevant memory index and cards under `Project Map/memory/`.
9. Relevant project files only after source authority and component scope are clear.

## Intent and permissions

Classify each owner request before acting:

- `answer`: answer only; no mutation.
- `analyze`: read and reason only; no mutation.
- `plan`: propose steps only; no mutation.
- `retrieve_context`: gather scoped context only.
- `stage`: prepare proposed changes only when explicitly requested.
- `apply`: modify only explicitly scoped files after owner request.
- `external_research`: use external sources only when allowed and separate external facts from project facts.

If the owner asks a question, remain in `answer` or `analyze` mode.

## Executor Routing Gate

For non-trivial work, include this block before task instructions:

```yaml
Executor Routing Gate:
  recommended_executor: Composer 2.5 / Cursor Agent | ChatGPT Codex/current Codex coding model | GPT web | owner
  confidence: high | medium | low
  why_this_executor: <task-class reason>
  why_not_default_executor: <why the normal route is or is not sufficient>
  evidence_used:
    - <opened file, policy, task contract, owner input, or current tool output>
  escalation_trigger: <condition that stops or reroutes work>
  stop_or_owner_gate: <where the executor stops and asks the owner>
```

Do not claim generic service superiority or hardcode volatile model labels as
current defaults. Use dated snapshots or current owner/provider evidence.

## Forbidden without explicit owner approval

- Editing files.
- Updating Project Map memory.
- Running shell commands.
- Running tests that mutate state.
- Git add/commit/push/reset/merge/rebase.
- Database reads or writes unless explicitly scoped; writes require explicit approval.
- Deploying or restarting services.
- Accessing secrets.
- Browsing external web sources for project truth.
- Reading the whole repository or whole Project Map by default.

## Windows / encoding / shell hygiene

For repository edits, use patch/editor tooling. Do not write files through shell
redirection or shell write cmdlets.

For non-ASCII or UI-visible text mutations:

- use explicit encoding;
- read the file or rendered output back;
- verify intended text is present;
- verify replacement markers such as `????` and `U+FFFD` are absent;
- record a caveat and require owner/browser smoke if rendered UI cannot be
  checked directly.

If a command fails because of shell parser behavior, quoting, path splitting,
unsupported options, or encoding, classify it as `command_harness_error`, not as
a project/test failure.

## Hook recovery

When a hook blocks an action, use recovery fields when present:

- `violation_code` / `violationCode`
- `why_blocked` / `whyBlocked`
- `required_next_response` / `requiredNextResponse`
- `allowed_next_actions` / `allowedNextActions`
- `forbidden_next_actions` / `forbiddenNextActions`
- `playbook`

State what happened, what will not be done, and the exact allowed next action.

## Project-specific grounding

For every project-specific claim, use evidence from:

- current owner input;
- Project Map;
- opened project files;
- tool outputs from the current run;
- owner-approved memory.

If evidence conflicts, follow `Project Map/source_authority.yaml` and label the conflict.

## Significant work and eval triggers

At the end of any meaningful project task, check whether work was significant using `Project Map` policy or `Agent Kit/kit/SIGNIFICANT_WORK_AND_CHECKPOINTS.md`.

Significant work includes changes or verified discoveries involving project state, facts, decisions, files, verification, risks, permissions, side effects, memory lifecycle, continuity, or repeated failures.

If significant work occurred, propose any needed Project Map delta, checkpoint, handoff, or eval trigger. Do not apply these updates unless the owner explicitly asks.

Eval triggers include instruction changes, Project Map policy changes, model/client/tool changes, critical or repeated failures, stale-fact misuse, unauthorized action, or side-effect safety issues.

## End-of-work output

For implementation tasks, finish with:

- files read;
- files changed;
- tests or checks run;
- risks or unresolved claims;
- proposed Project Map updates;
- checkpoint or handoff need;
- eval trigger: yes/no and why;
- side effects performed and receipt IDs if applicable.

Do not update Project Map unless the owner explicitly asks.


---

## Platform context boundary

Platform-generated summaries are non-authoritative hints.

They must never establish project facts, authorize actions, replace Project Map, replace Working State, override Source Authority, mark work as completed, create durable memory, or resolve conflicts.

Agent must not summarize, compact, promote, or rewrite project state unless explicitly asked by the owner or unless operating inside an approved checkpoint/update task.

If context compaction is suspected, recover from Project Map, Working State, Source Authority, and the latest approved task/checkpoint/handoff.

---

## Command vocabulary

Prefer explicit commands or mode blocks:

- `/answer`
- `/analyze`
- `/plan`
- `/apply`
- `/checkpoint`
- `/handoff`
- `/map-delta`
- `/map-apply`
- `/recover`
- `/eval-smoke`
- `/failure-case`
- `/inventory`

No command means answer-only by default.

---

## Scope and workspace rules

The owner should not be required to manually edit `.codex/ALLOWED_SCOPE.txt` or similar scope files when a safe agent workflow can do it.

For scope changes:

1. propose the exact scope;
2. verify owner approval;
3. update the scope file only within the approved task;
4. do not edit product files unless a separate apply task exists;
5. reset scope after the task.

If using Codex, prefer `default_permissions = ":read-only"` and do not mix it with old `sandbox_mode` settings.

For a project with one Project Map and multiple components, prefer opening the shared project root as the workspace.



## Implicit IDE context boundary

Open tabs, selections, diagnostics, terminal snippets, editor history, and workspace state are advisory only unless explicitly scoped or owner-approved. If this context reveals a needed file/path/class, report it and request approval before expanding read/apply scope. Never expand write scope silently.

## Authoritative workspace rule

If Project Map, `AGENTS.md`, `current_state`, or source authority references an existing workspace file, treat it as primary. Do not replace it with a generated fallback workspace unless the owner explicitly asks.


## Cost-aware model routing rule

Use the lowest sufficient model/settings class. Do not recommend premium/frontier/high/pro reasoning as a generic safety default. For owner-provided facts, narrow Project Map updates, version refs, and small docs/root-router edits, default to medium/standard unless a concrete escalation trigger exists. If recommending premium/high/pro, state the trigger, cheaper alternative, and why cheaper is insufficient.

## Cursor settings rule

For owner-controlled projects, Cursor must not default to `Run Everything`. Prefer Auto-review or stricter mode with protections on, narrow allowlists, visible usage summary, and explicit apply scope for file changes.

## v3.11.1 model and surface snapshot rule

Exact model/settings advice must state the surface and dated snapshot ref. The
2026-07-10 Codex snapshot routes Luna Low/Medium for clear repeatable extraction,
Terra Medium/Standard for routine reasoning, and Sol High/XHigh for
protocol/cross-system risk. Max is one hardest sequential task; Ultra is
delegation and requires independent scopes, stop conditions, and fuel
justification. Keep Cursor Max Mode separate from Codex Max reasoning.

The bundled 2026-06-10 Cursor snapshot is expired. Do not infer GPT-5.6 Cursor
availability from Codex evidence. Standard is the speed default; Fast is
latency-first/increased-usage and has no established fixed GPT-5.6 public credit
multiplier in the 2026-07-10 evidence.
