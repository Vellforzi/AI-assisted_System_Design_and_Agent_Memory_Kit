# Secondary Memory Governance Integration And Data Update Plan

Status: staged implementation plan
Updated for: v3.8.0 rules with canonical policy templates, task contracts,
claim ledgers, handoffs, eval triggers, and the repo-centric context governance
baseline.

This plan is intentionally split into several passes. The repository contains
many interdependent guides, YAML policies, examples, skills, eval cases, and
integration notes. Do not update everything in one large edit. Each pass should
produce a small, reviewable diff and a verification receipt.

## Current Finding

The kit now has two related sets of reusable artifacts:

1. Generic canonical templates in `Agent Kit/kit/`:
   `SOURCE_AUTHORITY_TEMPLATE.yaml`, `PERMISSIONS_POLICY_TEMPLATE.yaml`,
   `RETRIEVAL_POLICY_TEMPLATE.yaml`, `RETRIEVAL_SCORING_POLICY_TEMPLATE.yaml`,
   `TASK_CONTRACT_TEMPLATE.yaml`, `CLAIM_LEDGER_TEMPLATE.yaml`, and
   `HANDOFF_TEMPLATE.yaml`.
2. A repo-centric context governance baseline in
   `Agent Kit/kit/secondary_memory_governance/`.

The canonical templates are already mostly generic and use placeholders such as
`<project-id>`. The integration problem addressed by this plan was preventing
the reusable baseline from accumulating concrete adopter defaults and
domain-specific rules.

Main risk:

- adopters may copy the reusable baseline and accidentally inherit concrete
  adopter runtime assumptions, paths, smoke cases, and boundaries.

## Objective

Align the reusable repo-centric context governance baseline with the generic
canonical templates. Concrete adopter-specific project context must
not be added to this package as a built-in profile; it belongs in the downstream
project or in an external/private fixture set.

The final state should provide:

- generic reusable governance templates;
- a generic repo-centric context governance baseline derived from the templates;
- no bundled concrete adopter runtime profile in the reusable kit;
- aligned schema, examples, lifecycle, retrieval, task, claim, and handoff data;
- generic eval/smoke cases that adopters can copy and extend in their own
  projects;
- optional helper tooling only after the data model is stable.

## Non-Goals

Do not implement these during the data-update passes:

- autonomous memory writes;
- vector database integration;
- runtime memory daemon;
- automatic promotion from candidate memory to current memory;
- hidden hooks that mutate Project Map data;
- full model-eval harness;
- replacement `AGENTS.md` for existing projects;
- adopter-specific runtime behavior.

## Pass 0: Inventory Updated Rules

Purpose: establish the current source set and avoid editing from stale
assumptions.

Read these first:

- `README.md`
- `START_HERE.md`
- `RELEASE_NOTES_v3.8.0.md`
- `Agent Kit/README.md`
- `Agent Kit/START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md`
- `Agent Kit/kit/README.md`
- `Agent Kit/kit/MANIFEST.md`
- `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`
- `Agent Kit/kit/MATURE_EXISTING_PROJECT_ADOPTION_PROFILE.md`
- `Agent Kit/kit/secondary_memory_governance/README.md`

Then read the canonical templates:

- `Agent Kit/kit/SOURCE_AUTHORITY_TEMPLATE.yaml`
- `Agent Kit/kit/PERMISSIONS_POLICY_TEMPLATE.yaml`
- `Agent Kit/kit/RETRIEVAL_POLICY_TEMPLATE.yaml`
- `Agent Kit/kit/RETRIEVAL_SCORING_POLICY_TEMPLATE.yaml`
- `Agent Kit/kit/TASK_CONTRACT_TEMPLATE.yaml`
- `Agent Kit/kit/CLAIM_LEDGER_TEMPLATE.yaml`
- `Agent Kit/kit/HANDOFF_TEMPLATE.yaml`

Then read implementation data:

- all files under `Agent Kit/kit/secondary_memory_governance/`
- `Agent Kit/kit/MEMORY_SCHEMA_REFERENCE.yaml`
- `Agent Kit/kit/memory_card_examples.yaml`
- all files under `Agent Kit/kit/eval_suite/`
- relevant Codex/Cursor skills and commands for memory, source authority, scope,
  checkpoints, handoff, evals, and recovery.

Record:

- canonical fields present in templates but missing from overlay files;
- overlay fields that are domain-specific and must be removed or replaced with
  placeholders;
- schema entries present in `MEMORY_SCHEMA_REFERENCE.yaml` but missing examples;
- examples that still use older schema versions;
- eval cases that are generic;
- eval cases that are project-specific;
- manifest/release-note references that would become stale after moving files.

Suggested search:

```powershell
rg -n "<known-adopter-specific-marker>|<private-product-track>|<external-system-name>|<runtime-specific-path>" .
```

Exit criteria:

- a file-level update map exists;
- no data has been moved yet;
- canonical-vs-overlay ownership is explicit.

## Pass 1: Define Canonical Ownership

Purpose: prevent duplicated rules from drifting.

Declare this ownership model in the relevant README files:

- root templates in `Agent Kit/kit/*_TEMPLATE.yaml` are canonical generic
  policy templates;
- `secondary_memory_governance/` is a ready-to-copy overlay profile for mature
  existing projects where Project Map is secondary memory;
- example/profile folders, if added later, contain only generic copyable
  examples, not private adopter runtime assumptions;
- project-specific copied files must replace placeholders and must not be
  treated as universal kit defaults.

Update or verify:

- `Agent Kit/kit/README.md`
- `Agent Kit/kit/MANIFEST.md`
- `Agent Kit/kit/secondary_memory_governance/README.md`
- `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`
- `Agent Kit/kit/MATURE_EXISTING_PROJECT_ADOPTION_PROFILE.md`

Exit criteria:

- a future agent can tell which files are canonical templates and which files
  are installable overlay/profile data;
- no guide claims that project-specific overlay data is a universal baseline.

## Pass 2: Normalize Secondary-Memory Overlay Files

Purpose: make the reusable overlay generic and aligned with canonical templates.

Update these files by deriving them from the canonical templates, not by adding
new independent rules:

- `Agent Kit/kit/secondary_memory_governance/source_authority.yaml`
- `Agent Kit/kit/secondary_memory_governance/permissions_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/retrieval_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/retrieval_scoring_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/memory_lifecycle_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/tool_output_reference_template.yaml`
- `Agent Kit/kit/secondary_memory_governance/working_state.yaml`
- `Agent Kit/kit/secondary_memory_governance/AGENTS_SNIPPET.md`

Required changes:

- replace concrete `project_id` values with placeholder or template value;
- replace concrete operational docs with placeholder examples;
- preserve `project_map_mode: "secondary_memory"` for this overlay profile;
- preserve answer-only default, explicit action gates, scoped read-only
  exploration, hard-gated retrieval scoring, and claim-evidence rules;
- add or align fields from canonical templates where missing, especially
  `claim_evidence_rule`, runtime capability labels, eval policy, significant
  work review, and retrieval result metadata;
- remove domain-specific forbidden interpretations from generic overlay files;
- keep context hygiene warnings for `.codexignore` and `.cursorignore`.

Exit criteria:

- generic overlay files have no adopter-specific product names, external-system
  names, runtime paths, current priorities, or project-only smoke cases;
- overlay policy semantics match the canonical templates;
- differences from canonical templates are deliberate and explained as
  secondary-memory profile differences.

## Pass 3: Remove Concrete Adopter Data From The Kit

Purpose: make sure concrete adopter data is not included in the reusable kit.

Do not create a bundled profile for a concrete external system, messaging
surface, test environment, or other adopter-specific project. If a downstream
project uses this kit as its test consumer, keep that project's concrete source
authority, smoke cases, runtime paths, and boundaries in that downstream project
repository or a separate private fixture set.

Update or verify:

- no `secondary_memory_governance/examples/<concrete-project>/` folder is added;
- generic files in `secondary_memory_governance/` stay free of adopter-specific
  state;
- README text tells adopters to create their own project-local profiles if
  needed;
- any retained examples use placeholders and portable domains only.

Exit criteria:

- the reusable kit does not contain concrete adopter runtime assumptions;
- generic overlay does not leak downstream-project state;
- README explains that concrete project profiles are outside the reusable kit.

## Pass 4: Update Adoption Workflow Data

Purpose: make adoption deterministic for owners and agents.

Add or update a compact adoption checklist in the governance README or a
separate adoption guide.

The checklist must require the adopter to set:

- `project_id`;
- Project Map mode: `authority`, `secondary_memory`, or `absent`;
- operational truth roots;
- source authority order;
- permission defaults and runtime capability labels;
- retrieval profiles and task-type entrypoints;
- task contract location and usage rule;
- claim ledger usage rule;
- handoff location and resume/recover rule;
- working state;
- domain boundaries;
- smoke/eval cases;
- ignore-file policy;
- review ownership;
- candidate memory promotion rule.

The checklist must state that copying the overlay without replacing adopter
values is incomplete adoption.

Exit criteria:

- a new project can adopt the overlay without inheriting example data;
- an agent can determine which fields must be customized before use.

## Pass 5: Align Schema, Examples, And Data Versions

Purpose: make schema reference, examples, storage guide, operating protocol, and
policy templates agree.

Update or verify:

- `Agent Kit/kit/MEMORY_SCHEMA_REFERENCE.yaml`
- `Agent Kit/kit/memory_card_examples.yaml`
- `Agent Kit/kit/PROJECT_MEMORY_STORAGE_GUIDE.md`
- `Agent Kit/kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md`
- `Agent Kit/kit/MEMORY_COMPILER_GUIDE.md`
- `Agent Kit/kit/PROJECT_GROUNDING_CONTRACT.md`
- `Agent Kit/kit/MEMORY_TOOL_INTERFACE_CONTRACT.md`

Required alignment:

- `MEMORY_SCHEMA_REFERENCE.yaml` currently references schema `3.4.0`; examples
  should not remain on older schema versions unless explicitly marked legacy;
- examples should cover `tool_output_reference`, `episodic_event`,
  `tool_use_lesson`, `checkpoint_note`, `memory_delta_proposal`, `eval_trigger`,
  `eval_case`, `eval_result`, and `eval_trace`;
- templates and examples should consistently use `source_ref`, `evidence_ref`
  or `evidence_refs` naming, or explicitly explain the distinction;
- lifecycle states in `memory_lifecycle_policy.yaml` should match schema
  statuses and retrieval profile rules;
- `claim_ledger`, `task_contract`, and `handoff` artifacts should be linked from
  storage, operating protocol, and replay guides.

Exit criteria:

- every memory/artifact type referenced by policy files has a canonical schema
  entry and at least one example or template;
- schema versioning is consistent or intentionally documented;
- lifecycle, retrieval, and claim-gate behavior do not contradict each other.

## Pass 6: Split Generic Eval Data From Domain Examples

Purpose: keep portable behavior tests generic and make adopter-specific smoke
cases a downstream-project responsibility.

Use these as portable sources:

- `Agent Kit/kit/eval_suite/eval_manifest.yaml`
- `Agent Kit/kit/eval_suite/eval_trigger_policy.yaml`
- `Agent Kit/kit/eval_suite/core_behavior_eval_cases.yaml`
- `Agent Kit/kit/eval_suite/domain_boundary_smoke_cases_template.yaml`
- `Agent Kit/kit/eval_suite/grader_rubric.yaml`
- `Agent Kit/kit/eval_suite/failure_to_eval_case_template.yaml`
- `Agent Kit/kit/secondary_memory_governance/manual_smoke_cases.yaml`

Required changes:

- keep generic governance cases in the reusable overlay;
- do not add concrete adopter-specific domain cases to this package;
- ensure the core suite includes claim ledger, task contract, handoff,
  retrieval hard gates, tool-output references, stale suppression, permission
  boundaries, eval-trigger behavior, and significant-work behavior;
- ensure `run_eval_checklist.py` can generate checklists from the updated
  generic suite files;
- update eval manifest paths if files move.

Core generic smoke cases should include:

- answer-only prompt does not mutate memory;
- explicit action prompt requires target and scope;
- stale memory cannot override verified source-of-truth docs;
- high retrieval score cannot bypass hard gates;
- conflicting sources require explicit conflict reporting;
- unsupported project claim fails the claim ledger/final-answer gate;
- task that spans sessions requires a task contract or handoff;
- long tool output is stored as a compact reference, not raw transcript;
- failed tool usage can become a candidate lesson only after review;
- analysis prompt may propose Project Map deltas but must not apply them.

Exit criteria:

- generic evals can run without downstream-project knowledge;
- downstream projects may keep their own concrete profile evals outside this
  reusable kit;
- eval trigger policy references the correct files;
- checklist generation works for generic suite files.

## Pass 7: Integrate Review Rules Into Agent Workflows

Purpose: make the new rules operational for Codex and Cursor without
introducing automatic mutation.

Update or verify:

- `Agent Kit/kit/secondary_memory_governance/memory_quality_review_bar.md`
- `Agent Kit/kit/codex/skills/memory-compiler/SKILL.md`
- `Agent Kit/kit/codex/skills/source-authority-audit/SKILL.md`
- `Agent Kit/kit/codex/skills/checkpoint-builder/SKILL.md`
- `Agent Kit/kit/codex/skills/handoff-builder/SKILL.md`
- `Agent Kit/kit/codex/skills/context-recovery/SKILL.md`
- `Agent Kit/kit/codex/skills/eval-case-builder/SKILL.md`
- `Agent Kit/kit/cursor/skills/memory_compiler_skill.md`
- `Agent Kit/kit/cursor/skills/source_authority_audit_skill.md`
- `Agent Kit/kit/cursor/skills/checkpoint_builder_skill.md`
- `Agent Kit/kit/cursor/skills/handoff_builder_skill.md`
- `Agent Kit/kit/cursor/skills/context_recovery_skill.md`
- `Agent Kit/kit/cursor/skills/eval_case_builder_skill.md`

Required behavior:

- agents know when to use source authority, permissions policy, retrieval
  policy, task contract, claim ledger, handoff, and memory quality review bar;
- review stays advisory unless owner explicitly authorizes apply or
  memory_update scope;
- skills must not imply that eval failures grant write permission;
- handoff/recover workflows must check side-effect receipts before replaying
  work.

Exit criteria:

- Codex and Cursor workflows reference the same canonical policy model;
- no workflow silently writes to Project Map or source files;
- mutation still requires explicit intent, target, scope, and permission mode.

## Pass 8: Optional Helper Tooling

Purpose: add convenience tooling only after policy data and examples are stable.

Do not start this pass until Passes 1-7 are complete.

Optional helper:

```text
Agent Kit/kit/tools/memory_cli.py
```

Allowed initial commands:

- `read-policy`
- `search`
- `hydrate`
- `claim-check`
- `task-contract-check`
- `handoff-check`
- `write-candidate --dry-run`
- `review-candidate --checklist`

Forbidden initial behavior:

- automatic promote;
- automatic delete;
- automatic rewrite of source-of-truth docs;
- hidden hook execution;
- background sync;
- model grading without explicit owner-selected harness.

Exit criteria:

- helper is read-only by default;
- write-like operations require explicit command intent and scoped target;
- candidate writes are dry-run first;
- tool docs say helper output is evidence/reference, not project truth by
  itself.

## Verification Gates

Run after each pass:

```powershell
rg -n "<known-adopter-specific-marker>|<private-product-track>|<external-system-name>|<runtime-specific-path>" "Agent Kit/kit/secondary_memory_governance"
```

Expected result:

- generic baseline has no matches;
- matches are not expected in this reusable kit.

Check template/overlay drift:

```powershell
rg -n "claim_evidence_rule|runtime_capability|claim_ledger|task_contract|handoff|eval_policy|significant_work" "Agent Kit/kit" 
```

Expected result:

- canonical templates, guides, overlay files, and skills use compatible language;
- no rule exists only in one place without a cross-reference.

Check eval helper availability:

```powershell
python "Agent Kit/kit/tools/run_eval_checklist.py" --help
```

Then run the supported checklist command for:

- generic core behavior cases;
- generic secondary-memory smoke cases.

Before final release, verify:

- root README and START_HERE mention the updated adoption path;
- manifest lists moved or newly added files;
- release notes explain the canonical-template and overlay-profile split;
- examples do not introduce concrete adopter runtime assumptions;
- schema versions and example versions are consistent or documented;
- no generated runtime state or adopter-specific private data is included.

## Recommended Release Strategy

Use a patch release for documentation/data alignment:

```text
v3.8.1: canonical template alignment and generic overlay cleanup
```

Use a minor release only if helper tooling or agent workflow behavior changes:

```text
v3.9.0: optional memory helper tooling and integrated review workflows
```

## Done Definition

The integration is complete when:

- canonical templates are clearly identified as generic source templates;
- repo-centric baseline files are reusable without domain leakage;
- concrete adopter runtime profiles are not bundled into the reusable kit;
- schema, examples, lifecycle, retrieval, task contracts, claim ledgers, and
  handoffs agree;
- smoke/eval data remains generic in the reusable kit;
- Codex and Cursor workflows reference the same review and permission model;
- optional tooling, if added, is read-only by default and owner-controlled;
- manifest and release notes reflect the final file layout.
