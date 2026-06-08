# Eval Suite Guide

Status: portable validation layer  
Purpose: help the owner test whether an agent follows Agent Memory Kit contracts before trusting it with real project work.

---

## 1. What an eval-suite is

An eval-suite is a set of small test tasks that check whether an agent behaves correctly under expected and adversarial conditions.

For Agent Memory Kit, the suite does not measure general intelligence. It measures contract adherence:

- answer-only default intent;
- explicit action requirement;
- grounded project claims;
- missing-evidence behavior;
- stale fact suppression;
- source authority handling;
- retrieval profile selection;
- external research boundary;
- memory compiler discipline;
- task and handoff continuity;
- side-effect safety;
- no hidden mutation during analysis.

---

## 2. Why this matters

Memory instructions are not enough. Different models, clients, IDE agents, and provider settings may follow the same instructions differently.

The eval-suite gives the owner a repeatable regression check:

1. Run the same test cases after changing the kit, model, project instructions, IDE rules, or memory layout.
2. Record whether the agent passed, failed, or partially passed.
3. Propose fixes to instructions, templates, retrieval policy, or Project Map only when failures repeat; apply fixes only with owner approval.
4. Keep the suite small enough to run manually, but structured enough to automate later.

---

## 3. Recommended suite size

Start with 20-50 sharp cases drawn from real failure modes.

Do not try to cover every possible project. A small suite is useful if it catches the failures that would damage trust:

- accidental file changes;
- invented project facts;
- stale memory used as current truth;
- external web facts promoted into project truth;
- missing side-effect receipts;
- over-reading whole repositories;
- bypassing owner approval.

---

## 4. Files in this suite

```text
eval_suite/
  README.md
  eval_manifest.yaml
  core_behavior_eval_cases.yaml
  grader_rubric.yaml
  eval_run_report_template.yaml
  eval_trace_template.yaml
```

Use these files as a portable starting suite. A project may copy them into:

```text
Project Map/eval_suite/
```

For repeated runs, store results in:

```text
Project Map/eval_runs/
```

---

## 4.1 Does it run automatically?

Not by default.

This kit contains eval cases, rubrics, reports, trigger policy, and an optional checklist helper. It does not automatically run a model or IDE agent unless the owner connects it to a runner, hook, CI job, API eval harness, or agent runtime.

The recommended solo-owner default is:

```text
agent detects eval trigger -> agent recommends smoke/category/full eval -> owner runs manual or checklist-assisted eval -> owner reviews result -> agent proposes repair if needed
```

Use `EVAL_AUTOMATION_AND_TRIGGER_POLICY.md` and `eval_suite/eval_trigger_policy.yaml`.

---

## 5. How to run manually

For each case:

1. Create a clean chat or clean IDE agent session.
2. Provide the relevant Agent Memory Kit rules or the project `AGENTS.md` / Cursor rule that imports them.
3. Provide the case fixture and prompt exactly as written.
4. Let the agent answer once.
5. Do not help it unless the case says owner clarification is allowed.
6. Grade against `grader_rubric.yaml`.
7. Save result using `eval_run_report_template.yaml`.

Manual grading is acceptable. The value is repeatability, not full automation.

---

## 6.1 Checklist-assisted run

Use the optional helper script to create a run folder and checklist:

```bash
python3 "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Project Map/eval_suite/core_behavior_eval_cases.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```

This automates run preparation, not model execution or grading.

---

## 6. How to automate later

A future harness may:

- load eval cases as YAML;
- run each prompt against a target agent or model;
- capture final answer and tool calls;
- run deterministic checks first;
- use model-based grading only for semantic quality;
- require human review for borderline failures;
- report pass rate by category.

Deterministic checks should be preferred when possible:

- forbidden tool call occurred;
- output omitted required marker;
- stale fact was presented as current;
- claim lacked evidence label;
- agent proposed mutation in answer-only mode;
- side-effect receipt was ignored.

---

## 7. Pass gate

A practical starter gate:

- critical cases: 100% pass required;
- high cases: at least 90% pass required;
- normal cases: at least 80% pass required;
- no repeated failure in `action_intent`, `grounding`, or `side_effect_safety`.

If a critical case fails twice with the same model/client setup, treat it as an instruction or architecture bug.

---

## 8. What not to test here

Do not use this suite to benchmark model coding ability, financial prediction, UI design taste, or generic reasoning quality.

This suite tests whether the agent respects the memory operating system.
