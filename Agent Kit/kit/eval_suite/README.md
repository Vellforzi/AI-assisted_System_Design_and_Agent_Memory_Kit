# Agent Memory Kit Eval Suite

Version: v3.8.0

This folder contains a portable starter eval-suite for Agent Memory Kit.

The suite checks contract behavior, not general model quality.

Primary categories:

- action intent;
- grounding;
- retrieval;
- memory compiler;
- external research boundary;
- long-task continuity;
- side-effect safety;
- owner-control workflow;
- significant-work handling;
- eval automation triggers;
- new-project adoption;
- usage/adoption behavior.

Recommended flow:

1. Read `eval_manifest.yaml`.
2. Read `eval_trigger_policy.yaml` to decide whether smoke, category, or full eval should run.
3. Run cases from `core_behavior_eval_cases.yaml`.
4. Grade with `grader_rubric.yaml`.
5. Store run notes using `eval_run_report_template.yaml`.
6. For any failure, capture a trace using `eval_trace_template.yaml`.
7. Convert repeated or critical failures using `failure_to_eval_case_template.yaml`.

This suite can be run manually, checklist-assisted with `tools/run_eval_checklist.py`, or later automated by a full harness.
