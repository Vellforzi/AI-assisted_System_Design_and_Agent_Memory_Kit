# Optional skill library

This source update packages the thirteen skill families revised on 2026-10-27:
twelve reusable skills and the two client variants of OPTION_PROFIT's
`job-combat-orchestrator`. The compact entrypoints retain mandatory conditional
references. Moving a requirement into a reference does not make it optional.

The five-file portable core installer is unchanged. It does not install or
activate these skills, hooks, worker bridges, model settings or agents. Source
publication is not proof that an already-open client has loaded a skill.

## Select the appropriate bundle

| Need | Canonical skill | Retained support and dependencies |
| --- | --- | --- |
| Production engineering | [production-engineering-standard](skills/production-engineering-standard/SKILL.md) | Contracts/lifecycle, code quality, performance, tests, diagnosis, review checklist and project toolchain guidance; MQL skill when applicable |
| Complete technical explanation | [complete-technical-communication](skills/complete-technical-communication/SKILL.md) | Technical explanations, anti-patterns, starter owner style; engineering standard for code policy |
| Ordinary coupled implementation | [bounded-coupled-task](skills/bounded-coupled-task/SKILL.md) | Cursor worker reference; engineering, communication, recovery and conditional strict closure |
| Continuity across compaction/handoff | [long-task-recovery](skills/long-task-recovery/SKILL.md) | Protocol, template, validator, session-binding helper and tests; ordinary mode remains default |
| Explicit strict/full-proof escalation | [outcome-driven-task-closure](skills/outcome-driven-task-closure/SKILL.md) | Proof/prompt templates, prompt compiler and evals; engineering, communication, bounded work and recovery |
| Model/effort recommendation | [select-effort](skills/select-effort/SKILL.md) | Dated basis and invocation metadata; opt-in Sol/Astra recommendation and owner-choice pause policy |
| Author client hooks | [create-hook](skills/create-hook/SKILL.md) | Cursor reference; consult actual current client capability before authoring |
| Author subagents | [create-subagent](skills/create-subagent/SKILL.md) | Cursor reference and preserved Codex explicit-only invocation metadata |
| MQL event behavior | [mql-event-lifecycle](skills/mql-event-lifecycle/SKILL.md) | Platform and temporal-verification references, invocation metadata |
| Bounded Cursor worker | [codex-worker-contract](skills/codex-worker-contract/SKILL.md) | Requires the separately supplied compatible bridge and result-submission tool; skill alone does not implement either |
| Author project rules | [create-rule](skills/create-rule/SKILL.md) | Cursor reference; existing rules/settings stay under project authority |
| Author skills | [create-skill](skills/create-skill/SKILL.md) | Resolve the system skill-creator through the active client catalog; never copy over client-managed built-ins |
| OPTION_PROFIT orchestration | [Project profile](skill-profiles/option-profit/README.md) | Distinct Codex and Cursor variants, local toolchain facts; no generic activation |

`skills/library.json` declares exact payload files, SHA-256 identities, mirrors,
conditional library dependencies and source-to-package adaptations. It is a
distribution inventory, not a client configuration file or runtime authority.
Payload hashes normalize CRLF to LF so Git's text checkout conversion does not
invalidate equivalent text. Provenance hashes record the raw transfer snapshots.
Mutual conditional references between bounded work, recovery and strict closure
do not mean that strict mode is activated by ordinary work.

## Adopt without changing unrelated configuration

1. Select skills for the owner's actual workflow. Copy each complete directory,
   including its references, assets, scripts, evals and metadata declared in the
   inventory. Include relevant library dependencies; do not copy only SKILL.md.
2. Inspect existing installed copies before replacing them. Merge reviewed local
   specialization; do not overwrite drift. Declare a canonical project source
   and mirrors so later updates have one owner.
3. For Codex, resolve discovery from the current catalog and client instructions.
   The usual project location is `.agents/skills/<name>/`; personal adoption uses
   `~/.agents/skills/<name>/`. A plain `skills/` directory is a source library and
   is not by itself proof of discovery. Honor supported explicitly chosen legacy
   locations. Obtain system `$skill-creator` from that client rather than vendoring
   its changing implementation. Hook, rule and subagent authoring also require
   `$openai-docs` from the target client's catalog. Report an unavailable required
   client skill rather than pretending the dependency was applied.
4. For Cursor, use its verified discovery location, normally
   `.cursor/skills/<name>/` or `~/.cursor/skills/<name>/`. The engineering,
   communication and bounded-task Cursor directories in this kit are byte mirrors
   of canonical sources. Other reusable directories need client metadata review;
   never assume Cursor honors Codex `agents/openai.yaml`.
5. Preserve `create-subagent`'s explicit-only policy. If the target Cursor version
   supports it, map that invocation policy to `disable-model-invocation: true`;
   verify support first. Preserve other existing invocation metadata. Adoption is
   not permission to change a skill to automatic or explicit-only by preference.
6. Apply the adopting project's language, toolchain and authority rules. Selecting
   `select-effort` explicitly opts into its named Sol/Astra recommendation and
   pause policy; it does not choose or switch the running model. Recheck actual
   host support. Its dated basis and examples are not current benchmark claims.
7. Confirm the client sees the intended directory and reads the updated entrypoint
   and applicable references for the current task. Do not infer activation from
   a copied file or invent a mandatory session restart. Report unavailable client
   discovery or runtime evidence as a gap.

## Verification

From the repository root, using the project's Python interpreter:

```text
python -B "Agent Kit/kit/tools/check_skill_library.py" --helpers
```

The check verifies declared payload identities, local Markdown links, dependency
presence and mirror equality; `--helpers` also executes negative checker tests,
the packaged recovery tests and prompt-compiler evals. It neither installs skills nor controls a trading
terminal. Run it after intentional edits and update reviewed inventory hashes.
Do not bless unknown drift by regenerating hashes without source/diff review.

These checks establish packaging and helper behavior. They do not prove that a
model follows instructions, a client has loaded them, or a target runtime passed
owner acceptance. The [transfer review](SKILL_TRANSFER_REVIEW.md) records what was
preserved and which project-specific adaptations were made.
