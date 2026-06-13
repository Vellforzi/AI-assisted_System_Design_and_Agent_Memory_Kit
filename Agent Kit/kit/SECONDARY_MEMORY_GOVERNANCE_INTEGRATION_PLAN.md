# Secondary Memory Governance Integration Plan

This plan describes how to integrate and update the secondary-memory governance
data in controlled passes. Do not treat this as a request to edit all files at
once. The repository has many interdependent guides, policies, examples, skills,
and eval files, so the safe path is a staged data-first rollout with explicit
verification after each pass.

## Objective

Make the secondary-memory governance package reusable across mature existing
projects without leaking the concrete `ai-stock-analyst-class` project state into
the generic kit.

The final package should provide:

- a generic baseline governance overlay;
- a separate concrete example/profile for `ai-stock-analyst-class`;
- aligned memory schemas, lifecycle rules, retrieval rules, and examples;
- smoke/eval cases that separate generic behavior from domain-specific behavior;
- optional helper tooling only after the policy data is stable.

## Non-Goals

Do not implement these during the initial integration passes:

- autonomous memory writes;
- vector database integration;
- runtime memory daemon;
- automatic promotion from candidate memory to current memory;
- hooks that mutate project memory without explicit owner approval;
- replacement AGENTS files for existing projects;
- project-specific runtime behavior for any adopter project.

## Pass 0: Inventory And Drift Baseline

Purpose: establish the current state before changing data.

Read and compare:

- `README.md`
- `START_HERE.md`
- `RELEASE_NOTES_v3.8.0.md`
- `Agent Kit/README.md`
- `Agent Kit/START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md`
- `Agent Kit/kit/README.md`
- `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`
- `Agent Kit/kit/MATURE_EXISTING_PROJECT_ADOPTION_PROFILE.md`
- `Agent Kit/kit/secondary_memory_governance/README.md`
- all files under `Agent Kit/kit/secondary_memory_governance/`
- `Agent Kit/kit/MEMORY_SCHEMA_REFERENCE.yaml`
- `Agent Kit/kit/memory_card_examples.yaml`
- all files under `Agent Kit/kit/eval_suite/`
- relevant Codex/Cursor skills and workflows for memory, source authority, and eval cases.

Record:

- files that currently contain concrete `ai-stock-analyst-class` data;
- files that should stay generic;
- files that should move into an example/profile directory;
- schema fields already supported;
- schema fields referenced in docs but missing from canonical schema;
- eval cases that are generic;
- eval cases that are domain-specific.

Suggested search:

```powershell
rg -n "ai-stock|owner-only|broker|Telegram|autotrade|LRG|NEXT_STEPS|sandbox execution" .
```

Exit criteria:

- a concrete file list exists for generic baseline updates;
- a concrete file list exists for example/profile extraction;
- no implementation work has started yet.

## Pass 1: Split Generic Baseline From Concrete Example Data

Purpose: remove project-specific state from the reusable governance baseline.

Update these generic baseline files first:

- `Agent Kit/kit/secondary_memory_governance/source_authority.yaml`
- `Agent Kit/kit/secondary_memory_governance/permissions_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/retrieval_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/retrieval_scoring_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/memory_lifecycle_policy.yaml`
- `Agent Kit/kit/secondary_memory_governance/tool_output_reference_template.yaml`
- `Agent Kit/kit/secondary_memory_governance/working_state.yaml`
- `Agent Kit/kit/secondary_memory_governance/AGENTS_SNIPPET.md`
- `Agent Kit/kit/secondary_memory_governance/README.md`

Required changes:

- replace concrete project identifiers with placeholder values;
- replace project-specific operational source paths with generic examples;
- mark all adopter-owned values as required customization points;
- keep policy semantics strict and concrete;
- remove domain-specific runtime boundaries from generic files;
- keep the answer-only default and explicit-action requirements;
- keep hard gates for source authority, permissions, retrieval, and lifecycle.

Create a concrete example/profile directory:

```text
Agent Kit/kit/secondary_memory_governance/examples/ai-stock-analyst-class/
```

Move or copy domain-specific versions there:

- source authority example;
- retrieval policy example;
- working state example;
- smoke cases that depend on owner-only execution, Telegram, broker/account, or other project-specific facts.

Exit criteria:

- generic baseline files do not contain `ai-stock`, `Telegram`, `broker`, `autotrade`, `LRG`, or `NEXT_STEPS`;
- the concrete example/profile preserves the useful ai-stock-specific data;
- README explains when to use the generic baseline and when to study the example.

## Pass 2: Normalize Adoption Data Update Workflow

Purpose: make adoption deterministic for project owners and agents.

Add or update a short adopter checklist in the governance README or a separate
guide. The checklist should require the adopter to replace:

- `project_id`;
- operational source-of-truth roots;
- source authority precedence;
- permission defaults;
- task-type retrieval entrypoints;
- working state;
- domain-specific boundaries;
- smoke cases;
- ignore-file rules;
- review ownership;
- promotion rules for candidate memory.

The checklist must say that copying the package without replacing these values
is an incomplete adoption.

Exit criteria:

- an agent can apply the package to a new existing project without inheriting
  the example project's runtime assumptions;
- all required adopter-specific values are discoverable in one pass.

## Pass 3: Align Memory Schema And Examples

Purpose: make canonical schema, examples, lifecycle, and retrieval rules agree.

Update or verify:

- `Agent Kit/kit/MEMORY_SCHEMA_REFERENCE.yaml`
- `Agent Kit/kit/memory_card_examples.yaml`
- `Agent Kit/kit/PROJECT_MEMORY_OPERATING_PROTOCOL.md`
- `Agent Kit/kit/PROJECT_MEMORY_STORAGE_GUIDE.md`
- `Agent Kit/kit/MEMORY_COMPILER_GUIDE.md`
- `Agent Kit/kit/PROJECT_GROUNDING_CONTRACT.md`
- `Agent Kit/kit/MEMORY_TOOL_INTERFACE_CONTRACT.md`

Required schema coverage:

- `tool_output_reference`;
- `episodic_event`;
- `tool_use_lesson`;
- `candidate_memory`;
- `source_ref`;
- `evidence_ref`;
- `authority_level`;
- `freshness_status`;
- `last_verified_at`;
- `supersedes`;
- `superseded_by`;
- `review_state`;
- `promotion_receipt`;
- `truncation_or_compaction_note`.

Exit criteria:

- every memory type referenced by policy files has a canonical schema entry;
- every required schema field has at least one example;
- lifecycle states in schema and policy match.

## Pass 4: Split And Expand Eval Data

Purpose: ensure regressions are caught without mixing generic behavior with a
single adopter project's domain behavior.

Split smoke/eval data into:

- generic secondary-memory governance cases;
- example/profile-specific cases.

Core generic cases should cover:

- answer-only prompt does not mutate memory;
- explicit action prompt may stage a candidate update;
- stale memory cannot override verified source-of-truth docs;
- conflicting sources require explicit conflict reporting;
- missing evidence metadata fails memory quality review;
- tool output is summarized as a reference, not copied as raw transcript;
- failed tool usage can become a candidate lesson only after review;
- hydrate/resume retrieves the minimal relevant context, not the whole memory tree.

Update or verify:

- `Agent Kit/kit/eval_suite/README.md`
- `Agent Kit/kit/eval_suite/eval_manifest.yaml`
- `Agent Kit/kit/eval_suite/core_behavior_eval_cases.yaml`
- `Agent Kit/kit/eval_suite/grader_rubric.yaml`
- `Agent Kit/kit/secondary_memory_governance/manual_smoke_cases.yaml`
- `Agent Kit/kit/tools/run_eval_checklist.py`

Exit criteria:

- generic evals can run without ai-stock project knowledge;
- example/profile evals can still validate the concrete ai-stock adoption profile;
- checklist generation works for the updated suite structure.

## Pass 5: Integrate Review Rules Into Agent Workflows

Purpose: make memory quality review operational for Codex/Cursor agents without
introducing automatic mutation.

Update or add:

- Codex memory-quality review skill or workflow;
- Cursor memory-quality review command or skill;
- references from existing memory compiler and source authority audit skills;
- instructions to run review before promoting candidate memory.

Relevant existing locations:

- `Agent Kit/kit/secondary_memory_governance/memory_quality_review_bar.md`
- `Agent Kit/kit/codex/skills/memory-compiler/SKILL.md`
- `Agent Kit/kit/codex/skills/source-authority-audit/SKILL.md`
- `Agent Kit/kit/cursor/skills/memory_compiler_skill.md`
- `Agent Kit/kit/cursor/skills/source_authority_audit_skill.md`

Exit criteria:

- agents know when to use the review bar;
- review remains advisory unless owner explicitly authorizes memory promotion;
- no workflow silently writes to project memory.

## Pass 6: Optional Read-Only Helper Tooling

Purpose: add convenience tooling only after the governance data is stable.

Do not start this pass until Passes 1-5 are complete.

Optional helper:

```text
Agent Kit/kit/tools/memory_cli.py
```

Allowed initial commands:

- `read-policy`
- `search`
- `hydrate`
- `claim-check`
- `write-candidate --dry-run`
- `review-candidate --checklist`

Forbidden initial commands:

- automatic promote;
- automatic delete;
- automatic rewrite of source-of-truth docs;
- hidden hook execution;
- background sync.

Exit criteria:

- helper is read-only by default;
- writes require explicit command intent;
- candidate writes are dry-run first;
- tests or manual smoke receipts exist.

## Verification Gates

Run after each pass:

```powershell
rg -n "ai-stock|owner-only|broker|Telegram|autotrade|LRG|NEXT_STEPS|sandbox execution" "Agent Kit/kit/secondary_memory_governance"
```

Expected result:

- generic baseline has no matches;
- matches are allowed only under `examples/` or `profiles/`.

Run checklist generation after eval changes:

```powershell
python "Agent Kit/kit/tools/run_eval_checklist.py" --help
```

Then run the supported checklist command for the updated generic smoke suite.

Before final release, verify:

- root README and START_HERE mention the updated adoption path;
- manifest lists new or moved files;
- release notes explain the governance split;
- examples do not override the generic baseline;
- no generated runtime state or adopter-specific private data is included.

## Recommended Release Strategy

Use a small release for documentation/data cleanup:

```text
v3.8.1: generic governance baseline cleanup and example/profile split
```

Use a larger release only if helper tooling or workflow behavior changes:

```text
v3.9.0: optional memory helper tooling and integrated review workflows
```

## Done Definition

The integration is complete when:

- generic governance files are reusable without domain leakage;
- concrete adopter examples are clearly separated;
- schema, lifecycle, retrieval, and examples agree;
- smoke/eval data is split into generic and example-specific layers;
- agent workflows reference the memory quality review bar;
- optional tooling, if added, is read-only by default and owner-controlled;
- all changes are documented in manifest and release notes.
