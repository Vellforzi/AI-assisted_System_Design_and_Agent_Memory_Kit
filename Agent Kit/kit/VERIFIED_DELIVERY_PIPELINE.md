# Verified Delivery Pipeline

Status: optional stronger delivery profile  
Purpose: turn owner intent into one proportionate, evidence-backed delivery
candidate without outsourcing technical discovery or internal repair to the
owner.

The default process is `../portable/core/WORKFLOW.md`. This reference applies
only when the adopting project selects stronger delivery proof for the current
task. Selection never adds authority, overrides an explicit solo constraint,
or requires another permission for already-authorized local work. The lifecycle
below describes that optional profile.

## Responsibility split

The owner normally supplies the result wanted, relevant known facts, protected
behavior, and subjective UX expectations. The agent discovers implementation
details from current source, interfaces, tests, traces, runtime evidence,
configuration, persistence, identity rules, compatibility consumers, and
build/deploy consumers.

Absolute promises such as "nothing anywhere can ever break" are invalid.
Completion is supported by explicit invariants, executable oracles, review,
receipts, and disclosed unverified external conditions.

## Conditional gates

The lifecycle is one state machine with risk-selected gates, not a mandatory
sixteen-step train.

| Class | Minimum active gates |
|---|---|
| R0 answer/read-only | grounded evidence; no contract, receipt, lease, or mutation |
| isolated trivial R1 | compact core, exact scope, oracle, targeted check, diff |
| coupled R1/R2 | dependency neighborhood, characterization, targeted/baseline checks, independent review |
| runtime/UI R2 | coupled gates plus environment readiness and structured black-box evidence |
| external R3 | runtime gates plus target/action allowance, preimage, rollback, readback |
| destructive/release R4 | R3 plus release contract, independent verification, owner gate |

Build, deploy, rollback, black-box, environment-readiness, and independent
review extensions activate only when the task changes the corresponding
consumer or crosses the corresponding risk boundary. Missing applicability is
not represented by dozens of `not_applicable` fields.

## Canonical state machine

```text
compiled
-> characterized        (only when protected existing behavior is affected)
-> implemented
-> repaired             (zero or more bounded iterations)
-> verified
-> reviewed             (only when the selected gate profile requires it)
-> verified_delivery_candidate
-> task_completed        (clean orchestration finalization only)
-> owner_accepted       (explicit owner decision only)
```

From any active pre-completion state, a separately validated terminal branch is
available:

```text
active_state -> terminal_blocker_proven -> task_blocked
```

That branch uses the same primary receipt, cannot pass through
`verified_delivery_candidate`, and never implies delivery or owner acceptance.

`first_generated_patch` and `internally_repaired_candidate` are diagnostic
candidate labels, not completion states. Compilation or a polished report
cannot advance a candidate to `verified_delivery_candidate`.

## Compact acceptance contract

`VERIFIED_DELIVERY_CONTRACT.template.yaml` schema 1.3 has a small mandatory
core:

- task id and owner goal;
- allowed change and protected behavior;
- write scope;
- acceptance criteria and separately named oracles;
- stop condition.

At authorized apply intake, the primary agent compiles the owner's requested
observable result, supplied facts and protected behavior into this contract. It
resolves implementation details, directly required dependencies and executable
oracles from current project evidence. Routine discoverable or reversible
details do not create an owner pause. The agent returns to the owner only when
a material owner-visible choice, new authority, scope expansion,
irreversible/external action or missing objective oracle cannot be resolved
inside the active contract.

Conditional extensions cover characterization, dependency neighborhood,
black-box/runtime, build, deploy, rollback, independent review, environment
readiness, and metrics. The validator keeps schema 1.0 and 1.1 compatibility
and schema 1.2 compatibility for already-open tasks; new contracts use 1.3.

Every criterion has a stable id and references one unambiguous oracle. Oracles
produce task-local evidence; narrative memory is not an oracle.

Schema 1.3 adds conditional controls without adding lifecycle stages. Each
criterion belongs to exactly one defect unit. Independent root causes use
separate units unless the contract records an explicit coupling justification.
An oracle declares both its mechanical kind and its acceptance layer
(`static`, `synthetic`, `runtime`, or `owner`) plus authorization. Mandatory
owner-visible criteria can complete only from an authorized `runtime` or
`owner` oracle; compile, build, or synthetic PASS remains a lower layer.

### Conditional evidence ceiling and cross-component code proof

When the owner asks for code-level rather than platform-level proof, the
contract may declare one `verification_target` from this ordered vocabulary:

```text
source_structure
-> component_behavior
-> cross_component_contract
-> harness_runtime
-> platform_runtime
-> owner_acceptance
```

The primary receipt records every level independently as `pass`, `not_run`,
`failed`, or `blocked`. A lower PASS never implies a higher PASS. Completion is
valid when every level through the requested target passes; higher unrequested
levels remain explicit. If platform runtime or owner acceptance was requested,
code-level evidence cannot substitute for it.

Evidence class is level-bound. `harness_runtime` and `platform_runtime` require
`runtime` or `owner` evidence; `owner_acceptance` requires `owner` evidence,
an `owner` oracle kind, and the resulting `owner_gate_receipt` / `.owner.json`
artifact policy. A command log cannot prove owner acceptance.
The lifecycle runtime-acceptance result must cover every deciding oracle listed
for those high levels, even when its acceptance criterion is not owner-visible.

Every level marked `pass` lists its authorized deciding oracle ids. Each oracle
points to a structured PASS receipt that matches the contract check, pass
condition, verification level, producer, artifact kind and SHA-256. The
identity-protected artifact is then parsed against the declared production,
lifecycle, boundary or mutation contract; a generic `{"status":"pass"}` file
is not a deciding oracle. Production artifacts must also be distinct file
identities from the contract, oracle receipts and deciding artifacts; resolved
paths and NTFS hardlinks cannot alias those control files.

`extensions.cross_component_code_proof` is conditional, not a new lifecycle
stage. It binds tests to the real production entrypoint, authoritative
initializer/state machine, actual component route, production artifacts, typed
state, field ownership, transitions, rollback, concurrency/interleavings,
instance invariants, and deferred-trigger independence. A separately
reimplemented test model may support diagnosis but cannot prove production
behavior by itself.

The lifecycle section has its own structured deciding oracle. It must report
the declared typed state, field ownership, observed transitions, success,
rollback and failure invariants, concurrency cases, instance invariants and
deferred-trigger independence. A simple profile may mark proportional oracle
strength `not_run` with empty oracle/evidence arrays; PASS sections still need
one deciding oracle and artifact.

Boundary proof identifies the interfaces and authoritative identity fields and
mechanically compares import/export names, parameter names/types/sizes/order,
return type, calling convention, architecture and protocol version, then binds
the result to compile/signature evidence, production call-route evidence, and
executable contract tests when available. Regex or text search alone is not a
strong boundary oracle. Complex state machines conditionally activate negative
paths, fault injection, mutation testing, or a justified combination so the
suite records each production mutation and demonstrably fails on initializer bypass, duplicate identity, missing
ready transition, ownership leakage, or rollback defects. Simple tasks record
why this strength gate is not required.

The receipt states the verified claim and residual condition without numeric
confidence percentages. Documentation and developer forums may support a
versioned premise, but they are not standalone behavioral oracles.

For product repair/diagnostic/runtime work, implementation begins only after a
five-field forensic record identifies the first divergent event, execution
sequence, falsifiable hypothesis, and deciding oracle. Coupled or high-risk
work conditionally requires one pre-implementation architecture review covering
root cause, mutation point, dependency neighborhood, expected diff, and oracle.
The same logical reviewer-role id is reused for final review.

## Dependency, preservation, and characterization

Before coupled edits, inspect the smallest sufficient direct neighborhood:
entrypoints, callers, callees, shared interfaces/state/data contracts,
persistence, instance identity, configuration, tests, build/deploy consumers,
and compatibility consumers. Stop retrieval when behavior and regression
impact are supported. This read expansion never expands write scope.

For affected behavior, distinguish what may change from what must remain
stable, including public interfaces, persistence, identity, transitions,
timers, fallbacks, error paths, and unrelated paths. When legacy tests are
missing and scope permits, create targeted characterization before changing
behavior.

## Bounded repair loop

```text
inspect -> implement -> static/compile -> targeted -> baseline
-> diff/scope -> adversarial self-review -> repair -> repeat
```

The primary agent owns the lifecycle and adjudicates review findings against
the owner goal, accepted contract, scope and objective oracle evidence. Only a
confirmed defect enters repair. Rejected or duplicate findings retain an
evidence-backed disposition; an out-of-scope confirmed defect becomes an owner
gate rather than an automatic scope expansion. Conditional independent review
uses one logical reviewer role, reused for re-review; it is not a reviewer
chain or vote.

Schema 1.2/1.3 contracts declare a total repair budget: one iteration for simple
work, two for standard work and three for complex infrastructure. These are
full repair-and-reverification cycles, not individual commands or small edits.
The repeated-failure and no-progress limits below still stop earlier. A budget
above three requires a new explicit owner gate.

Recoverable in-scope failures stay in the same task. Stop and return to the
owner when any terminal trigger occurs:

- the same confirmed deterministic failure fingerprint appears a second time;
- two consecutive iterations produce no measurable progress;
- the repair needs write-scope or capability expansion;
- an external dependency required by an oracle is unavailable;
- an oracle is missing, contradictory, or incapable of deciding the outcome;
- the repair would change the owner goal or protected behavior.
- the profile-derived total repair budget is exhausted;
- authorization, baseline, CAS, lease or execution-integrity evidence fails
  closed and cannot be repaired inside the active contract.

Task contracts may lower these budgets but must not silently raise them to an
unbounded loop. Immaterial failed attempts with no persistent/external effect
remain internal.

Schema 1.3 binds one task-local lifecycle-evidence JSON to the primary receipt
by path and SHA-256; that artifact separately binds the per-cycle repair ledger
by path and SHA-256. Every cycle records the deterministic finding fingerprint,
adjudication, hypothesis/root-cause change, changed files, narrow oracle result,
measurable progress, and reviewer result. Ledger totals must reconcile with
`repair_summary`. The same confirmed fingerprint recurring after repair
triggers protective stop even if the proposed hypothesis changed; duplicate or
rejected review wording does not count as a confirmed fingerprint.

The configurable diff budget defaults to more than three product files, more
than 300 added-plus-deleted product lines, or an unplanned task-local framework.
Product and framework path patterns are declared by the contract; Git computes
the actual `baseline..candidate` counts. Crossing a threshold does not prove
failure, but mutation cannot resume until ordered replan and scope-confirmation
evidence exists. Verification escalates narrow oracle -> targeted regression ->
full suite only when the contract's integration/dependency-risk flag is true.
Registered runners from the execution profile/toolchain are reused; the receipt
names the canonical launcher actually executed and its evidence. A task-local
replacement needs a documented capability gap.

The contract validator enforces R1-R4 minimum gate sets, active-gate extension
consistency, a maximum of two repeated/no-progress iterations, and the complete
canonical terminal-trigger set. A high-risk contract cannot declare a
lower-risk gate profile.

## Independent review

Independent review is required for coupled/risky work, not trivial edits. The
read-only reviewer receives the original goal, accepted contract and hash,
complete diff, relevant public/state interfaces, receipts, and unresolved
conditions. It does not receive a persuasive implementation narrative.

The reviewer attempts to falsify missed dependencies, identity/state errors,
masking fallbacks, persistence or transition defects, compatibility regressions,
weak/circular oracles, insufficient characterization, and unsupported claims.
Deterministic checks outrank reviewer agreement.

## Final outcomes and autonomous continuation

After an authorized mutation begins, ordinary recoverable failures do not end
the task. A first failing test, command-harness defect, stale task-local output,
review suggestion, first-patch defect or other in-scope repair remains inside
the same lifecycle. The only orchestration final events are:

- `task_completed`: every declared acceptance oracle and finalization gate is
  proven by the completed branch of the primary receipt;
- `task_blocked`: a canonical terminal trigger is proven by the blocked branch
  of that same receipt, no useful in-scope action remains, and the required
  owner action plus safe final state are recorded.

A blocked receipt is not a weaker completion receipt. It cannot claim delivery,
and it must not be used for a merely inconvenient or first recoverable failure.
Every blocked receipt observes the contract's total repair budget, regardless
of blocker code. Its blocker evidence is a schema-1.0 JSON object containing
the matching `blocker_code`, the code-specific `terminal_condition`, an empty
`remaining_in_scope_actions` array, and at least one objective fact. Each fact
has an id, contract `oracle_id`, observation, and the oracle's exact fresh
task-local `evidence_ref`. That evidence is a structured failed/blocked oracle
receipt bound to the contract's check and pass condition plus a hash-verified
underlying artifact. Schema-1.2 oracle kinds are exactly `command`, `state`,
`trace`, `diff`, `visual`, and `owner`; schema 1.3 retains the same set. Each maps to one runtime artifact kind
and canonical suffix. The artifact names its producer, has exactly one filesystem
link, and must be file-identity-distinct from the contract, primary receipt,
blocker wrapper, oracle receipt, finalization evidence, and recovery-attempt
evidence. Resolved-path checks alone are insufficient on NTFS; same-file/file-index
identity is also checked. A fresh control file that only restates `status:
blocked` is not proof. Repeated-failure,
no-progress, and total-budget outcomes additionally prove their configured
iteration threshold through recovery-attempt receipts.

## Runtime, UI, and worktree readiness

Runtime/UI gates prefer agent-legible evidence: fake clocks, structured state,
state-machine transitions, trace schemas, instance-aware integration checks,
layout geometry, and public API/CLI/file boundaries. GUI smoke follows
source-level checks and requires explicit authorization.

When runtime/build/black-box gates are active in a worktree, record an
environment-readiness check for the registered launcher, required dependencies,
fixtures, and fresh output/log path. Ignored local state is not assumed to be
present. `.worktreeinclude` must not copy credentials without a separate owner
allowance.

## Observability separation

- User-facing status uses product language.
- Developer trace may contain identifiers, transitions, and rejection reasons.
- Machine verification state uses stable structured fields and never parses
  localized UI text as its primary oracle.

## Codex hook boundary

Hooks enforce mechanical policy, not product semantics.

- Sandbox/permission mode, exact scope, lease, and agent discipline are the
  preventive boundary before writes.
- Codex `PreToolUse` and `PermissionRequest` hooks may warn with
  `systemMessage`; current Codex documentation does not support
  `continue: false` as a guaranteed block for those events.
- Post-change validators, tests, diff/scope checks, and receipts establish
  evidence.
- One independent/aggregating `Stop` hook may fail closed on missing or invalid
  declared receipts. Parallel hooks must not depend on one another's output.

Non-managed project hooks are inactive until the exact changed definition is
reviewed and trusted. If trust/execution is not proven on the current surface,
run the validator manually and report `CODEX_HOOKS_DISABLED`; do not claim live
hook enforcement.

The Stop hook delegates to the same strict receipt validator used by the CLI.
Before accepting any schema-1.2/1.3 outcome, that validator also runs the full
canonical contract validator; removing autonomous-continuation, intake,
repair-budget, reviewer-role, or gate-policy requirements therefore fails
closed at Stop. For a required schema 1.1 delivery, declaration check ids must exactly equal
the contract acceptance-criterion ids and declaration/receipt gates must
exactly equal `gate_profile.active`; a self-authored subset fails closed. It
also checks real and fresh task-local evidence files, clean review, and declared
finalization.
For schema 1.3 it additionally verifies bound lifecycle/repair-ledger hashes,
ordered forensic/replan/verification events, Git-derived diff budgets, runner
reuse, authorization-consistent runtime acceptance, and any declared evidence
ceiling. Stop detects invalid
completion evidence after the fact; it does not claim that PreToolUse prevented
an earlier write.
When Git finalization is required it also compares paths, binary diff digest,
candidate tree, HEAD, clean worktree, commit count/message, lease state, and
post-commit readback to current Git. Task-specific validators still own product
semantics.

## One primary receipt

`VERIFIED_DELIVERY_RECEIPT.schema.json` defines the one primary machine receipt.
Logs and test artifacts remain separate but are referenced by stable paths or
ids. Markdown is a view, never independent proof.

Optional `pipeline_metrics` may record only actually measured values such as
wall-clock time, repair iterations, active gate count, first-patch result,
false-block count, owner-wait time, human-touch time, or run cost. Missing
telemetry stays absent; it is never invented and never blocks delivery by
default. Aggregate the metrics after a meaningful sample to remove gates that
do not catch defects and strengthen gates that do.

The tracked candidate receipt is created before the final commit. Its own path
is explicitly excluded from `changed_paths`, `scope_diff.diff_sha256`, and
`final_git.candidate_tree`; Stop recomputes those three values with the same
exclusion. The final commit still contains the receipt, and a task-local ignored
post-commit receipt binds that commit to actual HEAD and the clean worktree.
This avoids a self-referential tree or diff hash without trusting self-reported
Git state.
