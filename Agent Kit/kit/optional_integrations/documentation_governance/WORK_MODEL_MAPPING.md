# Documentation Governance Work-Model Mapping

Status: optional guidance; inactive until an owner adopts it

## Authority boundary

For an adopted project, `.work/<change-id>/TASKS.md` is the **only authority**
for operational task status: the state of each task, its blockers, and whether
its verification has been recorded. Do not maintain a task-status table,
checklist, roll-up, or copied state in a Kit artifact, a document, an active
specification, an archived specification, or an ADR. Those sources may link to
the change folder and task IDs, but a link is navigation, not a status claim.

The existing knowledge-zone rules still apply: `.work` is ephemeral and cannot
by itself establish durable product facts. Promote a durable fact through the
appropriate reviewed `docs/` or `specs/active/` update. This makes `.work` the
operational-status authority without making it the authority for current
behavior, requirements, or historical decisions.

## Required `.work` change-folder contents

Create `.work/<change-id>/` from `templates/work_change/` only when execution
needs resumable, multi-step coordination. It contains:

- `PLAN.md` — intended approach, scope, and rollback/recovery notes.
- `TASKS.md` — independently verifiable tasks and the sole operational-status
  register.
- `ACCEPTANCE.md` — change-level acceptance criteria and verification evidence
  expectations.
- `DEVIATIONS.md` — append-only departures from the plan, with disposition.
- `artifacts/` — optional agent outputs (for example, research notes or tool
  captures); create it only when an artifact is useful.

Routine single-session, routine-risk work may remain artifact-light: do not
create a change folder or any v5 artifact merely because this template exists.
Select heavier contracts only from `TaskContractV3.workflow_profile`, task
scale, and risk.

## Exact contract mapping

| Contract | `.work` location / template field | Mapping and authority rule |
| --- | --- | --- |
| `TaskContractV3` | `PLAN.md`: `TaskContractV3 reference`; `TASKS.md`: `Task ID` | The TaskContract is the classification and permission contract. Map `task_id`, `goal`, `scope`, `done_definition`, and `workflow_profile` to the plan. `TASKS.md` uses `task_id` only as an identifier; it does not copy `TaskContractV3.status`. Classify `mode`, `task_scale`, `risk_class`, `delivery_strategy`, and `review_policy` before deciding whether to create the folder or heavier artifacts. |
| `WorkingStateV3` | `PLAN.md`: `WorkingStateV3 reference` | Map only a pointer to the current working-state artifact plus its `active_task` ID. Its `cursor`, `next_safe_step`, and `workflow_state` remain in the Kit artifact. Never mirror those fields or a task status into the change folder. |
| `WorkItemGraphV1` | `TASKS.md`: task `ID`, `Title`, `Behavior`, `Scope`, `Acceptance criteria`, `Verification recipe`, `Dependencies`, `Operational status` | For `task_scale: multi_session` delivery, map each task to `id`, `title`, `behavior`, `vertical_scope`, `acceptance_claims`, `verification_recipe`, `blocked_by`, and `status`. `.work/TASKS.md` remains the manually maintained operational authority. A schema-valid WorkItemGraphV1 may be materialized only as a generated, reviewable projection whose status and frontier are recomputed from `.work`; never edit or treat the projection as an independent status source. `frontier_assertion` remains navigation-only and is not an execution command. If no trustworthy projection adapter exists, stop rather than claiming that the required multi-session graph is active. |
| `VerificationReceiptV2` | `ACCEPTANCE.md`: criterion ID, subject/task ID, verifier, level, environment, evidence reference, verified timestamp | One recorded verification result maps to `receipt_id`, `task_id`, `subject_refs`, `claim_ids`, `verifier_type`, `verification_level`, `environment_ref`, `status`, `evidence_refs`, and `verified_at`. The acceptance file defines criteria and evidence links; the receipt remains the typed evidence record. A passing receipt needs evidence. |
| `ReviewReceiptV1` | `PLAN.md`: review requirement/reference; `DEVIATIONS.md`: findings disposition link | When workflow profile requires fresh-context or adversarial review, map `review_id`, `task_id`, `profile`, `result_refs`, `criteria_refs`, `intentional_decision_refs`, `status`, `findings`, and `owner_disposition`. Review input excludes author reasoning; the reviewer must not mutate or repair. The change folder records only links and owner decisions, not a duplicate review state. |

`PlanChallengeV1`, exploration, triage, probes, capability, and domain-language
contracts are outside this template set. Add references only when the selected
workflow profile activates them; do not pre-create them.

## Lifecycle

1. Classify workflow profile, scale, and risk in `TaskContractV3`.
2. For work that warrants a folder, create `.work/<change-id>/` and register
   each independently verifiable task in `TASKS.md`.
3. Record acceptance evidence and material deviations; retain optional agent
   artifacts only while useful.
4. If durable documentation, requirements, or a decision changed, update the
   matching template in its proper zone through review; do not promote a task
   status.
5. Archive or remove ephemeral `.work` material under the adopting project's
   retention policy after the work is no longer resumable.
