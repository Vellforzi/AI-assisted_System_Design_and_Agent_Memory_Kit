# Significant Work and Checkpoint Policy

Status: runtime-core policy  
Purpose: define when work is important enough to produce a Project Map update proposal, a handoff, an eval trigger, or a checkpoint note.

---

## 1. Core rule

The agent must not rely on intuition to decide that work is significant.

It must use explicit triggers.

A work item is significant when it changes, verifies, invalidates, or exposes something that future sessions should know.

A work item is not significant merely because the conversation was long, interesting, or technical.

---

## 2. What counts as significant work

Treat work as significant if at least one trigger is true.

| Trigger group | Significant when |
|---|---|
| Project state | current state, active task, next safe step, blocker, or milestone changed |
| Project facts | a fact was verified, disproved, superseded, or found missing |
| Decisions | owner accepted, rejected, changed, or deferred a decision |
| Source authority | authoritative files, docs, schemas, rules, or evidence order changed |
| Implementation | files were edited, generated, deleted, moved, or intentionally left unchanged after investigation |
| Verification | tests/checks/audits were run, failed, passed, or could not be run |
| Risk | new risk, contradiction, unsafe assumption, dependency issue, or unresolved claim was found |
| Permissions | task mode, allowed scope, forbidden scope, or action gate changed |
| Side effects | shell, git, database, deployment, external API, browser action, message, purchase, or similar effect occurred |
| Memory | memory card lifecycle should change: candidate, verified, stale, superseded, rejected, archived |
| Continuity | another session would need a checkpoint, handoff, task cursor, or must-read refs to continue safely |
| Failure | the agent violated a rule, repeated a mistake, or produced a near miss that should become an eval case |

---

## 3. What does not count as significant by default

Do not create memory updates for:

- casual discussion;
- generic explanations;
- temporary preference inside one answer;
- brainstorming without owner decision;
- a question answered from existing memory with no new information;
- external research that was not promoted by the owner;
- a hypothesis that has no project evidence;
- raw transcript content;
- secrets or credentials.

These may be mentioned in the answer, but they do not become durable memory without a separate trigger.

---

## 4. When the agent is "after" significant work

"After significant work" means a safe checkpoint has been reached.

A checkpoint is reached when one of these is true:

| Situation | Checkpoint moment |
|---|---|
| Answer/analyze/plan task | the final answer, findings, or plan is ready |
| Apply task | the scoped change is complete or blocked, and verification status is known |
| Audit task | findings, conflicts, and missing evidence are listed |
| Memory repair task | candidate changes and lifecycle effects are identified |
| Long task | a planned checkpoint, owner pause, context limit, failure, or handoff point is reached |
| Interrupted task | current cursor, completed actions, unsafe-to-repeat actions, and next safe step are known |

Time spent is not the criterion. The criterion is whether the next session would lose important state without a note.

---

## 5. Required end-of-work check

At the end of any non-trivial project task, the agent should silently run this checklist and report only the useful result.

```text
Significant work check:
1. Did project state, facts, decisions, files, verification, risk, permissions, side effects, or continuity change?
2. Would a future session need this result to avoid rework or a wrong answer?
3. Is the result supported by project evidence or owner approval?
4. Is the item safe to store and not a secret?
5. Is the current intent allowed to write memory?
```

If the answer to 1-4 is yes but memory-write intent is absent, propose a memory delta instead of applying it.

---

## 6. Output pattern

For answer/analyze/plan modes:

```text
Project Map update: recommended / not needed
Reason: <one sentence>
Proposed memory delta: <only if useful; do not apply>
Eval trigger: yes/no
```

For apply mode:

```text
Checkpoint:
- Completed: <what changed>
- Verified: <checks run or not run>
- Project Map update: applied / proposed / not needed
- Handoff needed: yes/no
- Eval trigger: yes/no
```

Do not include this block for tiny one-off questions unless it would help.

---

## 7. Memory delta proposal template

```yaml
memory_delta_proposal:
  reason: ""
  intent_required_to_apply: "update_project_map"
  proposed_changes:
    - target: "Project Map/memory/<file>.yaml"
      operation: "add|update|mark_stale|supersede|reject|archive"
      summary: ""
      evidence_refs: []
      review_state: "owner_review_required"
  not_applied_because: "no explicit memory-write intent"
```

---

## 8. Eval trigger from significant work

Significant work should trigger an eval proposal when:

- agent instructions changed;
- Project Map source authority, permission policy, or retrieval policy changed;
- a repeated or critical failure occurred;
- action-intent, grounding, stale-fact, or side-effect behavior was involved;
- a new failure mode was found;
- a model/client/tooling setup changed;
- long-running or higher-autonomy work is about to be allowed.

See `EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`.
