# Eval Automation and Trigger Policy

Status: optional automation policy  
Purpose: define when evals should run, what can be automated, and what still requires owner approval.

---

## 1. Core rule

An eval-suite does not run by magic.

This kit is file-first and provider-neutral. It can define eval cases, triggers, checklists, reports, and optional helper scripts. Actual automatic execution requires a runner, IDE hook, command, CI job, API harness, or provider-specific integration.

The safe default is:

```text
Agent notices eval trigger -> agent proposes eval run -> owner runs or approves run.
```

---

## 2. Automation levels

| Level | Name | What happens | Recommended for solo owner |
|---|---|---|---|
| 0 | Manual | owner manually copies cases into the target AI client and grades them | yes |
| 1 | Agent-prompted | agent states `Eval trigger: yes/no` at checkpoint | yes |
| 2 | Checklist-assisted | a local script creates a run folder and checklist from YAML cases | yes |
| 3 | Hook/CI-triggered | file changes trigger an eval checklist or API run | later |
| 4 | Full harness | prompts are sent to a model/agent, traces captured, graders run automatically | later |

For high-control solo work, use levels 1-2 first. Do not jump to level 4 until the Project Map and instruction files are stable.

---

## 3. Eval trigger matrix

Run or propose evals when any trigger fires.

| Trigger | Minimum action |
|---|---|
| Agent instruction file changed: `AGENTS.md`, Cursor rule, `CLAUDE.md`, project instructions | run smoke eval |
| Kit rule/template changed | run smoke eval before trusting the release |
| Project Map `source_authority.yaml` changed | run grounding and source-authority cases |
| Project Map `permissions_policy.yaml` changed | run action-intent and side-effect cases |
| Project Map `retrieval_policy.yaml` changed | run retrieval and stale-fact cases |
| Model, provider, IDE client, or tool permissions changed | run smoke eval |
| Agent made or nearly made an unauthorized mutation | add failure case and run action-intent cases |
| Agent invented a project fact | add failure case and run grounding cases |
| Agent used stale memory as current truth | add failure case and run retrieval/staleness cases |
| Agent repeated a side effect or ignored receipt | add failure case and run side-effect cases |
| Owner is considering long-running autonomous work | run full core behavior suite first |

---

## 4. Smoke eval versus full eval

A smoke eval is a small, fast subset used after routine changes.

Recommended smoke categories:

- `action_intent`
- `grounding`
- `retrieval`
- `side_effect_safety`
- `owner_control`

A full eval uses all active cases. Run full eval when publishing a kit release, changing the operating protocol, changing project-wide agent rules, or enabling higher autonomy.

---

## 5. What the agent may automate

In answer/analyze/plan mode, the agent may:

- detect that an eval trigger exists;
- say which cases should run;
- draft a new eval case from a failure;
- produce a checklist or command suggestion;
- propose changes to kit/rules/templates based on failures.

It must not:

- change kit files;
- change project rules;
- update Project Map;
- mark evals as passed;
- hide failed evals;
- run tools or scripts;
- call model APIs;

unless the owner explicitly asks for that action and grants scope.

---

## 6. What can be automated with a local helper script

The kit includes an optional helper:

```text
Agent Kit/kit/tools/run_eval_checklist.py
```

It can create an eval run folder and a Markdown checklist from YAML cases.

Example:

```bash
python3 "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Project Map/eval_suite/core_behavior_eval_cases.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```

This does not grade an AI model by itself. It automates run preparation and reporting structure.

---

## 7. Full automation requires a harness

A full harness must be explicit about:

- target model or agent client;
- instructions loaded;
- Project Map fixture;
- allowed tools;
- prompt for each case;
- captured final answer;
- captured tool calls;
- deterministic checks;
- model-based rubric checks where needed;
- human review for borderline failures.

Do not let the harness modify the real project. Use fixtures, sandbox folders, or dry-run modes.

---

## 8. Failure-to-eval rule

If the agent fails or nearly fails in a way that matters, create a candidate eval case.

```text
Failure observed -> short trace -> failure category -> candidate eval case -> owner review -> add to suite -> rerun relevant category.
```

A repeated failure should not remain only in chat memory.

Use `eval_suite/failure_to_eval_case_template.yaml`.

---

## 9. Eval results do not edit the kit automatically

Eval failures are diagnostic signals.

The normal repair loop is:

1. run eval;
2. identify failure category;
3. propose one small repair to instruction, template, policy, memory lifecycle, or retrieval profile;
4. owner reviews;
5. apply only if explicitly approved;
6. rerun the failed case.

The owner remains the final authority.
