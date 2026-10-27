---
name: job-combat-orchestrator
description: Use only for explicitly escalated or locked strict-combat JOB/PremiaOP orchestration. Ordinary coupled tasks and ordinary worker contracts use bounded-coupled-task plus codex-worker-contract.
---

# JOB combat orchestrator (Cursor)

## Mode gate

Strict combat is active only when the current owner/parent contract or live
locked state explicitly establishes at least one:
- requested combat mode or full-product proof;
- active `task_identity_locked`, `strict_forensic` or equivalent locked signal;
- parent-selected $outcome-driven-task-closure;
- another already-proven registered strict escalation trigger.

Ordinary multi-file/component work or mutation under a task contract is not
a strict trigger. Use $bounded-coupled-task; bridge workers with `TASK_ID`,
`RUN_ID` and `CONTRACT_HASH` also use $codex-worker-contract.

For ordinary work:
- do not require preapply-intake, owner_acceptance_lock, a capsule,
  TRAVEL/NOTICE/Atlas, BLOCK_WALK, reviewer-before-compile or Task fan-out;
- use one bounded vertical slice, early executable feedback, dependency-local
  invalidation, at most two Cursor attempts and one post-green review;
- a missing result envelope does not erase an independently inspectable bounded diff;
- retain authority, hook enforcement, exact write scope and side-effect gates.

Without the mode gate, the strict references below are inactive.

## Authority and execution boundaries

Before acting, read [Runtime and authority](references/runtime-and-authority.md).
It retains authority order, root resolution, hook paths/rules and response fields.
Current owner/project authority governs conflicts; a historical configuration
statement is not evidence of active enforcement. Verify actual hook registration,
execution and failure behavior before claiming protection.

Remain answer-only until explicit apply/map-apply scope.
On a hook block, report `violationCode`, `requiredNextResponse` and allowed/forbidden
actions. Silent/missing hooks require `CODEX_HOOKS_DISABLED`; stop claiming protection.
Commit/push/deploy/credentials require current owner authorization.
Do not invent a second guard policy or re-enable the retired model gate without
owner authorization.

Resolve named skills from the actual client/project sources. Do not assume a
personal Cursor copy equals the updated project skill; report missing or
conflicting dependencies rather than claiming the intended version was applied.

## Strict combat — conditional requirements

After the mode gate, before strict execution, read both:
- [Strict product pipeline](references/strict-product-pipeline.md):
  worker roles, Git/hosting exclusions, owner acceptance, Walker/snapshots,
  BLOCK_WALK, repair continuation and compile/deploy prerequisites.
- [Task execution](references/task-execution.md):
  delegation contract, failure handling, model constraints, harness hygiene
  and the strict worker-result bridge.

These references retain requirements, exceptions and stopping conditions;
they are not optional advice. Apply them under current owner/project authority.
Do not silently drop an unresolved policy conflict or restore superseded gates.
Keep internal PASS, deployment, runtime evidence and owner acceptance distinct.
