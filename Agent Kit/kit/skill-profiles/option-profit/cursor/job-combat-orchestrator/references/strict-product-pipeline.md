# Strict product pipeline

Read this entire reference and task-execution.md before strict execution.
These requirements are inactive without the core's strict-mode gate.
The current owner request and applicable project/task-class policy govern;
the retained procedure is not independent authorization for Task, writes,
compile, deploy, hosting, Git or trading-terminal control.

## Explicit policy conflicts — 2026-10-27

- C-DELEGATION: The retained text sends heavy units through Task. Current
  project AGENTS.md uses solo execution by default; the matching
  `Project Map/gpt/OPTION_PROFIT_MT_CODE_FIX_POLICY.yaml` forbids subagents.
  The table below describes roles, not permission to spawn them against that
  policy. Keep the parent responsible and preserve one-writer boundaries.
- C-ACCEPTANCE: The retained preapply/capsule/ACK procedure and candidate status
  are stricter than current `.cursor/rules/owner-acceptance-lock.mdc`, which
  requires owner acceptance when the task actually asks for owner judgment and
  does not require a contract/hash/receipt. Do not turn the retained procedure
  into an extra approval for already authorized ordinary work. Preserve locked
  owner meaning and any acceptance actually required by the selected task.
- C-PROCESS: The retained Walker, inventory and review-before-compile gates
  differ from current project execution rules and the updated bounded workflow.
  Determine the governing current task policy explicitly. Do not silently
  treat an old mandatory process as universally current, nor discard a genuinely
  applicable strict requirement. Ordinary work remains outside these sections.
- C-EXTERNAL: The retained Git/hosting and compile/deploy prerequisites do not
  authorize external actions. `full toolkit`, internal PASS or `DEPLOY_PASS`
  still cannot substitute for the named authority or product/runtime acceptance.

These conflicts are surfaced, not resolved by changing hooks, roles, rules or
other skills. A material unresolved authority/product choice must be reported;
independent authorized work may continue.

## Retained strict procedure

The following reproduces former core lines 73–147 exactly, including the full
role table, acceptance procedure, Walker rules, BLOCK_WALK branches, all four
compile/deploy prerequisites, repair continuation and snapshot reuse exceptions.

## Orchestrator vs workers (Cursor adaptation of Codex combat)

Parent chat = **руководитель**. Heavy units go through `Task`:

| Unit | `subagent_type` |
|---|---|
| bounded source/test/task-root writes | `job-writer` |
| managed C# / Premia.Tests | `csharp-builder` |
| MQL compile | `mql-compiler` |
| GC6099 live deploy | `mt-deployer` |
| independent review | `job-reviewer` |
| cheap inventory | `explore-cheap` |
| journal forensics | `journal-forensic` |
| Option Profit map (`docs/Option Profit map/`) — Walker main thinking mapper via INBOX/STATUS; Cursor `system-mapper` mechanical canonical snapshot + promote only | Walker (Grok schedule) + `system-mapper` (Mode D / promote) |

Do **not** put `job-hosting` or `job-git` in this combat pipeline. Spawn them
only when the **current** owner prompt asks:

- `job-hosting`: two separate commands (approved version → local mirror;
  later distinct command → remote FTP)
- `job-git`: commit / push / tag / GitHub release named explicitly

`full toolkit` includes neither. Apply and smoke PASS do not mean git or hosting.

Owner-visible product picture: before `job-writer`, use project skill
`preapply-intake` (or an already ACK'd `owner_acceptance_lock`). Do **not**
rewrite locked fields. No capsule → `OWNER_SEMANTIC_GATE_REQUIRED`. After
internal PASS: `CANDIDATE_READY_AWAITING_OWNER_ACCEPTANCE`, not DONE. Mismatch
(reviewer PASS + owner FAIL): task-root `COMPLETION_MISMATCH` from
`Agent Kit/kit/COMPLETION_MISMATCH.template.yaml`. See
`.cursor/rules/owner-acceptance-lock.mdc`.

**Pre-apply:** open `docs/Option Profit map/TRAVEL.md` and `_audit/NOTICE.md`.
If new schemes are needed: parent writes `_audit/INBOX.md`, holds until STATUS
`done`+sha (or `blocked`). **Wait STATUS ≠ stop:** keep the course — re-read
`_audit/STATUS.md` until match; no owner Grok poke; no apply-stopped / «ваш ход»;
parallel work without new schemes OK; no writer/compile/thinking `system-mapper`
until match. Do **not** Task thinking `system-mapper`. Spawn `system-mapper`
**mechanical only** for Mode D snapshot / promote **after** STATUS match when
canonical maps or NOTICE-newer resnapshot is required. Reuse task-root snapshot
when same bag/block.
Closed `⇢`/`🔗` or STOP from snapshot. `🔒` = source walk, not owner smoke.
Marker neighborhood is a step, not the gate. Do not hot-swap Walker mid-apply.
Coherence is post-push only.

## Post-apply BLOCK_WALK (product apply)

After `job-writer` returns on a **product** apply:

1. Require `BLOCK_WALK.md` (or `.json`) on disk in the product task root.
2. If a **this-block** case is `still-broken`, re-Task `job-writer` on the
   **same task** (distinct Task `description` suffix); do **not** spawn compile
   or deploy.
3. After this-block `BLOCK_WALK` is complete (`not_this_bag` holes may remain ●):
   parent may spawn `mql-compiler` then `mt-deployer` **only if all** are true:
   1. Current owner `/apply` named `host_cycle` / compile / GC6099 deploy.
   2. Reviewer verdict is **PASS** (not `PASS_WITH_CAVEAT`, not `NOT PASS`). If no reviewer was run, do not treat BLOCK_WALK paper-green as PASS.
   3. `APPLY_RESULT.why_closes_hole` restates owner meaning, not journal tokens as the close.
   4. `this_block_closed` is not a marble pass (new-branch source-walk only).
   Otherwise: do **not** spawn compile/deploy (unchanged). `PASS_WITH_CAVEAT` ≠ compile. Named `host_cycle` does not override this. `DEPLOY_PASS` ≠ bag `[OK]`. Do not spawn `job-git` / `job-hosting`. Distinct Task descriptions still required.
   If reviewer caveat / NOT PASS / `patched_unproven` / `this_block_still_broken` is remaining in-scope branches of the **same owner meaning**: parent **must** re-Task `job-writer` (distinct `description` suffix, same meaning, no new INBOX, no H-seminar). Do **not** ask the owner. Do **not** end the course / «ваш ход». This is the same rule as BLOCK_WALK step 2, also when the leftover is a reviewer caveat instead of writer `still-broken`.
   Ask the owner only: other bag, EA/DLL/forbidden write, environment, smoke, ambiguous meaning, Task/hook failure.
   If compile/deploy were **not** named in this apply: **stop**; do not invent host cycle.

## Same bag snapshot

Same semantic block, same bag, and NOTICE `updated` **not** newer than the
task-root `atlas-snapshot/` stamp:

- Do **not** write INBOX for a new thinking walk; do **not** Task thinking
  `system-mapper` for impact-draft novel.
- Reuse the apply-start snapshot.
- New INBOX / Walker walk only if NOTICE moved, write-set/bag/block changed, or
  the **hole class of the block** changed (not a new journal token of the same
  class).
