# Documentation Governance Work-Model Mapping

Status: optional guidance; inactive until an owner adopts it

## Authority boundary

Only when the `.work/<change-id>/` process is activated, its `TASKS.md` is the
**only authority** for that change's operational task status: the state of each
task, its blockers, and whether its verification has been recorded. Do not
maintain a task-status table, checklist, roll-up, or copied state in a Kit
artifact, a document, an active specification, an archived specification, or
an ADR. Those sources may link to the change folder and task IDs, but a link is
navigation, not a status claim. When no `.work` process is activated, use the
adopting project's existing operational-status system.

The existing knowledge-zone rules still apply: `.work` is ephemeral and cannot
by itself establish durable product facts. Promote a durable fact through the
appropriate reviewed `docs/` or `specs/active/` update. This makes `.work` the
operational-status authority only while its change process is active, without
making it the authority for current behavior, requirements, or historical
decisions.

## `.work` activation and minimal contents

Create `.work/<change-id>/` from `templates/work_change/` only for resumable
multi-session work, coordination among multiple executors, more than three
independently verifiable slices, high-risk acceptance, or a requested audit
trail. Routine single-session work remains artifact-light.

The minimal activated folder contains:

- `TASKS.md` — independently verifiable tasks and the sole operational-status
  register for the activated process.
- `ACCEPTANCE.md` — change-level acceptance criteria and verification evidence
  expectations.

Add `PLAN.md` for an intended approach, scope, or recovery record;
`DEVIATIONS.md` for material departures from that plan; and `artifacts/` only
for useful supporting outputs. Do not create a change folder or any v5
artifact merely because the template exists. Select additional contracts only
from `TaskContractV3.workflow_profile`, task scale, and risk.

## Exact contract mapping

| Contract | `.work` location / template field | Mapping and authority rule |
| --- | --- | --- |
| `TaskContractV3` | `TASKS.md`: `TaskContractV3 ID`; optional `PLAN.md`: reference | The TaskContract is the classification and permission contract. `TASKS.md` uses `task_id` only as an identifier; it does not copy `TaskContractV3.status`. Classify `mode`, `task_scale`, `risk_class`, `delivery_strategy`, and `review_policy` before deciding whether an activation trigger exists or optional plan/heavier artifacts are needed. |
| `WorkingStateV3` | Optional `PLAN.md`: `WorkingStateV3 reference` | When a plan is needed, map only a pointer to the current working-state artifact plus its `active_task` ID. Its `cursor`, `next_safe_step`, and `workflow_state` remain in the Kit artifact. Never mirror those fields or a task status into the change folder. |
| `WorkItemGraphV1` | `TASKS.md`: task `ID`, `Title`, `Behavior`, `Scope`, `Acceptance criteria`, `Verification recipe`, `Dependencies`, `Operational status` | For an activated change where `task_scale: multi_session` delivery also requires this contract, map each task to `id`, `title`, `behavior`, `vertical_scope`, `acceptance_claims`, `verification_recipe`, `blocked_by`, and `status`. `.work/TASKS.md` remains the manually maintained operational authority. A schema-valid generated projection is Reference Lab material: its status and frontier must be recomputed from `.work`, and it must never be edited or treated as an independent status source. `frontier_assertion` remains navigation-only and is not an execution command. If no trustworthy projection adapter exists, stop rather than claiming that the required multi-session graph is active. |
| `VerificationReceiptV2` | `ACCEPTANCE.md`: criterion ID, subject/task ID, verifier, level, environment, evidence reference, verified timestamp | One recorded verification result maps to `receipt_id`, `task_id`, `subject_refs`, `claim_ids`, `verifier_type`, `verification_level`, `environment_ref`, `status`, `evidence_refs`, and `verified_at`. The acceptance file defines criteria and evidence links; the receipt remains the typed evidence record. A passing receipt needs evidence. |
| `ReviewReceiptV1` | Optional `PLAN.md`: review requirement/reference; optional `DEVIATIONS.md`: findings disposition link | When workflow profile requires fresh-context or adversarial review, map `review_id`, `task_id`, `profile`, `result_refs`, `criteria_refs`, `intentional_decision_refs`, `status`, `findings`, and `owner_disposition`. Review input excludes author reasoning; the reviewer must not mutate or repair. The change folder records only links and owner decisions, not a duplicate review state. |

`PlanChallengeV1`, exploration, triage, probes, capability, and domain-language
contracts are outside this template set. Add references only when the selected
workflow profile activates them; do not pre-create them.

## Lifecycle

1. Classify workflow profile, scale, and risk in `TaskContractV3`.
2. Only when an activation trigger applies, create `.work/<change-id>/` with
   `TASKS.md` and `ACCEPTANCE.md`, then register each independently verifiable
   task in `TASKS.md`.
3. Add a plan, material deviations, and agent artifacts only when their
   specific purpose applies; retain optional artifacts only while useful.
4. If durable documentation, requirements, or a decision changed, update the
   matching template in its proper zone through review; do not promote a task
   status.
5. Archive or remove ephemeral `.work` material under the adopting project's
   retention policy after the work is no longer resumable.
