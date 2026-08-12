# Agent Memory Kit v3.11.3 Changelog

Release date: 2026-08-12

Previous published tag: `v3.11.2`. This release does not claim a public
v3.12.0 package, tag, ZIP, or GitHub Release.

This file is release metadata, not publication proof. Publication requires a
matching repository commit, annotated tag, archive checksum, and release
receipt.

## Why this release exists

Live owner work showed that the kit was already a constraint contour, but
the published package did not say that clearly enough for a stranger:

- people still blame "stupid agents" when the contour is missing;
- the kit was readable as a file dump instead of a guide;
- Cursor and Codex setup existed, but the FAQ did not send users there
  first;
- the honest reply to "you cannot write unit tests without reading code"
  was missing.

## Added

- `QUESTIONS_THIS_KIT_ANSWERS.md` — FAQ surface for what the kit is, why
  it exists, what it can and cannot do, and how to install Cursor/Codex.
- `CAPABILITY_MANAGEMENT.md` — claim that output quality is dominated by
  capability management, not model IQ; reply to the structural-unit-test
  objection.
- `BEHAVIORAL_ORACLES.md` — compile is not done; behavioral oracles vs
  structural unit tests; owner smoke; label vs pipeline; independent
  review.
- `eval_suite/cases/AMK-CM-001.yaml` — agent must not blame model IQ when
  the constraint contour is missing.
- `PROPOSED_SPECIALIST_FUNCTIONS.md` — how to create limited specialist
  functions (writer, reviewer, mapper, forensic, builder, deployer).
- Example Cursor subagent cards under `cursor/subagents/` for those
  functions. Copy the limits, not a private project's agent tree.
- `SCHEMES_AND_COVERAGE_ATLAS.md` plus `coverage_atlas/` — schemes as a
  method to offer (INDEX, tokens, impact-draft, one mapper). They do not
  replace CNs, hooks, contracts, or source.
- `WORKING_METHOD_CATALOG.md` — owner-gated smoke, contract hygiene, mode
  boundaries, write-lock pattern, constraint types.
- `CONSTRAINT_CATALOG.md` plus `constraint_catalog/` — numbered CN facts.
  Product CNs stay in the adopting Project Map.
- `proposed_hooks/` — combat-method hook cards and example bytes
  (wrapper, contract, profile, finalization, encoding).
- `MOTIVE_AND_ANALOGY.md` — standing analogy the agent must be able to say:
  lay your knowledge on disk; a capable model looks like you; sub-agents
  multiply that copy; a fool plus folders is pointless.

## Changed

- Root `README.md` and `START_HERE.md` point at the FAQ and thesis.
- Kit README, owner guide, positioning, and system-design method mention
  the same claim.
- Maintainer extraction rule is explicit: live diff → abstract projection
  → kit guide, with private names stripped.

## Unchanged

- No JOB-local v3.12.0 runtime (leases, App Server, verified-delivery
  state machine) is extracted into this public release.
- Older eval case files may keep an inherited `suite_id` / `kit_version`.
  The checklist runner compares the manifest against
  `eval_trigger_policy.yaml` and does not fail smoke solely on inherited
  per-case version labels.

## Safety boundary

These files are guides. They do not authorize commit, push, deploy,
credentials, or copying a private Project Map into the published kit.
