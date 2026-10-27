# Runtime and authority

Read with the core before acting. Retained requirements below are subject to
the current owner request and applicable project instructions. Configuration
descriptions are evidence to verify, not proof that a guard is active.
This reference neither creates a second guard policy nor authorizes repairs.

## Observed discrepancies — 2026-10-27

- C-HOOK: The retained inventory says `failClosed: true` and names
  `C:/Users/user/.cursor/hooks/job_task_contract_guard.py`. That wrapper is
  absent. The current `C:/Users/user/.cursor/hooks.json` registers
  `job_workflow_adapter.py` for six events and contains no `failClosed: true`.
  The adapter imports `codex_guard_bridge.dispatch` indirectly; absence of
  direct bridge registration does not mean the bridge cannot be called.
  Its repository search is limited to JOB / _agent_worktrees/JOB and its
  exception path returns `continue: true`. File inspection does not establish
  fail-closed protection for OPTION_PROFIT or execution in the open client.
  Preserve hook-block reporting and do not claim protection without evidence.
- C-MODEL-GATE: `task_model_allowlist_hook.py` exists but is not registered.
  The retained prohibition on re-registering it without owner authorization
  remains. No hook was enabled, disabled, changed or exercised in this revision.
- C-AUTH: The retained numbered list places Project Map/source/schema before
  live output. Current project AGENTS.md treats maps as evidence and current
  source/live state as the implemented baseline; owner requirements define
  desired behavior. Do not let the retained ordering make a stale map override
  current evidence or create a new permission gate.
- C-ROOT: The retained JOB paths are not proof of the actual task root.
  Resolve the current workspace/worktree; do not infer applicability from a
  historical directory name.

## Dependency identities — inspect before relying on them

The following were observed on 2026-10-27; presence is not proof of discovery,
selection or loading by an already-open Cursor client.

| Dependency | Current source available in this workspace | Personal Cursor copy |
|---|---|---|
| bounded-coupled-task | `E:/Dev Projects/OPTION_PROFIT/.cursor/skills/bounded-coupled-task/SKILL.md` | Exists; differs from updated project source |
| production-engineering-standard | `E:/Dev Projects/OPTION_PROFIT/.cursor/skills/production-engineering-standard/SKILL.md` | Exists; differs from updated project source |
| complete-technical-communication | `E:/Dev Projects/OPTION_PROFIT/.cursor/skills/complete-technical-communication/SKILL.md` | Exists; differs from updated project source |
| outcome-driven-task-closure | `E:/Dev Projects/OPTION_PROFIT/skills/outcome-driven-task-closure/SKILL.md` | No personal Cursor copy found |
| codex-worker-contract | `C:/Users/user/.cursor/skills/codex-worker-contract/SKILL.md` | Present; preserve its exact contract |
| preapply-intake | `E:/Dev Projects/OPTION_PROFIT/.cursor/skills/preapply-intake/SKILL.md` | Project source used by the retained strict procedure |

Updated project copies of the first three matched their .agents counterparts
when inspected. Resolve the actual applicable source, report ambiguity, and do
not claim an updated skill was applied merely because a same-named file exists.
No other skill was synchronized in this revision.

## Retained authority, surface inventory and posture

The following is the exact former core block (lines 39–67).
Its paths and configuration assertions must be interpreted with the discrepancies
above; its authorization, reporting and no-re-registration protections remain.

## Authority

1. Current owner prompt
2. Nearest project `AGENTS.md`
3. Project Map + canonical source/schema
4. Live tool output

Codex `~/.codex/memories` and platform summaries are hints only.

## Fail-closed surfaces

- User hooks: `C:/Users/user/.cursor/hooks.json` (`failClosed: true`)
- Wrapper: `C:/Users/user/.cursor/hooks/job_task_contract_guard.py`
- Bridge: `C:/Users/user/.cursor/hooks/codex_guard_bridge.py` → repo `.codex/hooks/*`
- Task model gate: **OFF** (owner 2026-08-15). File
  `C:/Users/user/.cursor/hooks/task_model_allowlist_hook.py` is not registered
  in `hooks.json`. Cursor owns Task spawn. Do not re-register without owner allow.
- Rules: `codex-operating-defaults.mdc`, `job-orchestrator-delegation.mdc`,
  `task-subagent-model-allowlist.mdc`, `job-harness-hygiene.mdc`

Do not invent a second policy text. Prefer calling existing Codex guards.

## Required posture

- Answer-only until explicit apply/map-apply scope
- Resolve worktree root correctly (parent JOB or `_agent_worktrees/JOB/...`)
- On hook block: report `violationCode`, `requiredNextResponse`, allowed/forbidden
- If hooks are silent/missing: report `CODEX_HOOKS_DISABLED` and stop claiming protection
- No commit/push/deploy/credentials unless the current owner prompt authorizes it
