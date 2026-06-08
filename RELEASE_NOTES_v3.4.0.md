# Release Notes — Agent Memory Kit v3.4.0

Release name: Checkpointed Eval Automation Release  
Release date: 2026-06-08  
Package: `AI-assisted_System_Design_and_Agent_Memory_Kit_v3.4.0_EN.zip`

---

## Summary

v3.4.0 clarifies when project work is significant, when a checkpoint exists, when Project Map updates should be proposed, and when evals should be triggered.

The release also adds a new-project adoption guide, a day-to-day owner usage guide, a plain-language glossary, positioning against alternative memory approaches, and a small optional helper script for checklist-assisted eval runs.

---

## Added

- `Agent Kit/kit/SIGNIFICANT_WORK_AND_CHECKPOINTS.md`.
- `Agent Kit/kit/EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`.
- `Agent Kit/kit/NEW_PROJECT_ADOPTION_GUIDE.md`.
- `Agent Kit/kit/OWNER_USAGE_GUIDE.md`.
- `Agent Kit/kit/POSITIONING_AND_ALTERNATIVES.md`.
- `Agent Kit/kit/PLAIN_LANGUAGE_GLOSSARY.md`.
- `Agent Kit/kit/eval_suite/eval_trigger_policy.yaml`.
- `Agent Kit/kit/eval_suite/failure_to_eval_case_template.yaml`.
- `Agent Kit/kit/tools/README.md`.
- `Agent Kit/kit/tools/run_eval_checklist.py`.
- Additional eval cases for significant work, eval automation, new-project adoption, and usage/adoption behavior.

---

## Changed

- Updated `PROJECT_MEMORY_OPERATING_PROTOCOL.md` with explicit checkpoint and significant-work behavior.
- Updated `EVAL_SUITE_GUIDE.md` with automation levels and trigger policy.
- Updated `AGENTS.md_TEMPLATE.md` and `CURSOR_RULE_TEMPLATE.mdc` so agents report Project Map and eval triggers at the end of meaningful tasks.
- Updated README and manifest files to explain where the kit is strong, where it is intentionally limited, and how to use it in new and existing projects.
- Updated eval manifest and grader rubric to include eval automation and significant-work categories.

---

## Not changed

- The kit remains file-first and owner-controlled.
- The kit remains provider-neutral and implementation-agnostic.
- Evals still do not run automatically unless connected to a runner, hook, command, CI workflow, or API harness.
- Eval failures still do not grant permission to edit kit files, project rules, Project Map, or source code.
- Answer-only remains the default intent.
- Long-running autonomous work remains optional and should not be used until Project Map, source authority, permissions, and eval checks are reliable.
