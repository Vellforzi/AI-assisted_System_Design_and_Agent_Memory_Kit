# Executor Routing Gate

Status: portable task-contract rule
Purpose: make executor/service selection explicit, evidence-based, and owner
reviewable before non-trivial work starts.

---

## Core Rule

Every non-trivial bootstrap prompt, task contract, task block, or owner-facing
model/service recommendation should include an `Executor Routing Gate` block
before task instructions.

The gate is not a status badge. It is a decision record that states which
executor should do the work, why that executor fits this task, what evidence was
used, when to escalate, and where the owner gate is.

## Required Block

```yaml
Executor Routing Gate:
  recommended_executor: Composer 2.5 / Cursor Agent | Codex App/current Codex coding model | GPT web | owner
  confidence: high | medium | low
  why_this_executor: <task-class reason>
  why_not_default_executor: <why the normal route is not enough, or why this is the normal route>
  evidence_used:
    - <opened file, policy, task contract, owner input, or current tool output>
  escalation_trigger: <condition that should stop or reroute the task>
  stop_or_owner_gate: <where the executor stops and asks the owner>
```

## Routing Defaults

- Composer 2.5 / Cursor Agent: scoped mechanical implementation, exact write
  scope, local build/test iteration, and package file edits.
- Codex App/current Codex coding model: analysis, planning, contract authoring,
  review, execution-integrity checks, evidence-chain recovery, and repair loops.
- GPT web: current external research, official documentation lookup, and
  source-cited synthesis that is not project truth until promoted.
- owner: deploy, DB writes, credentials, git push/tag/release, destructive
  cleanup, external send/post actions, and ambiguous side-effect scope.

These defaults are task-class guidance, not claims that one service is generally
better.

## Prohibited Claims

Do not say an executor is superior in general.

Do not say another executor would fail unless you have a current task-class
reason, a concrete prior failure, current provider evidence, or an active
project policy.

Do not hardcode volatile model names as current recommendations. Use dated
snapshots or current owner/provider evidence.

## Validation

Use the included helper to check contract/bootstrap files:

```bash
python "Agent Kit/kit/tools/verify_executor_routing_gate.py" --path <contract-or-bootstrap> --json
```

Missing or malformed gates are blocking defects for non-trivial bootstraps and
contracts. Result files, validation files, logs, inventories, and reports are
normally excluded unless they are explicitly used as task contracts.
