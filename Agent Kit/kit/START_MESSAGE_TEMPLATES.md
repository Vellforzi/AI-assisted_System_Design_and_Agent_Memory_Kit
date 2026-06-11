# Start Message Templates

Status: copyable owner prompts  
Purpose: give the owner safe ways to start, continue, ask, analyze, or apply work under Agent Memory Kit.

---

## 1. Explain-only start

```text
Agent Kit is located here: <path or uploaded ZIP>.
Project: <name or not created yet>.

Mode: explain-only.
Intent: answer.
Do not read, analyze, or change project files.
Explain how Agent Memory Kit should be used for this project, especially the grounding rule and answer-only default intent.
```

---

## 2. New project dry-run start

```text
Agent Kit is located here: <path>.
The project will be here: <path>.
Project Map should be here: <path>.
Project materials should be here: <path>.
OS/shell for future commands: <not needed now / specify precisely>.
Tools and stack with versions: <not needed now / specify precisely>.

What the project is:
<free-form explanation>.

Mode: dry-run without reading and without writing.
Intent: plan.
Suggest a Project Map structure and first memory files. Do not invent project facts beyond what I wrote. Mark missing information as missing.
```

---

## 3. Create Project Map draft

```text
Agent Kit is located here: <path>.
Project Map target: <path>.
Project materials: <path>.

What the project is:
<free-form explanation>.

Mode: dry-run.
Intent: stage.
Create a proposed Project Map starter:
- README.md
- current_state.md
- working_state.yaml
- source_authority.yaml
- permissions_policy.yaml
- retrieval_policy.yaml
- claim_ledger.yaml
- tasks/TASK-0001.yaml
- handoffs/
- memory/index.yaml
- memory/facts.yaml
- memory/decisions.yaml
- memory/constraints.yaml
- memory/risks.yaml
- workstreams/WS-0001.md

Do not write files yet. Show the proposed contents first.
```

---

## 4. Continue existing project

```text
Active layer: Agent Memory Kit.
Project: <name>.
Project Map: <path>.
Mode: read-only.
Intent: resume.
Scope: read only:
- Project Map/current_state.md
- Project Map/working_state.yaml
- Project Map/source_authority.yaml
- Project Map/permissions_policy.yaml
- Project Map/retrieval_policy.yaml
- Project Map/tasks/<active>.yaml
- Project Map/workstreams/<active>.md
- Project Map/memory/index.yaml
- any memory cards required by the active task

Goal: resume the active task.
Use the resume retrieval profile. Do not use chat memory as project truth. If required evidence is missing, say exactly what is missing. Do not perform mutating actions unless I explicitly ask for apply.
```

---

## 5. Ask a grounded project question

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: read-only.
Intent: answer.
Scope: <exact Project Map files and/or project files allowed>.
Question: <question>.

Use the answer retrieval profile.
For project-specific claims, cite or name the memory/file evidence you used. If evidence is missing, do not guess. Do not change files, update memory, run commands, or start implementation.
```

---

## 6. Read-only analysis

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: read-only.
Intent: analyze.
Scope: <exact files/folders>.

Task: analyze <topic> and return findings only.
Do not change files, update memory, run commands, browse externally, or apply fixes unless I explicitly ask for that separately.
Return:
1. grounded findings;
2. evidence;
3. risks;
4. missing evidence;
5. proposed next steps.
```

---

## 7. Read-only audit

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: read-only.
Intent: analyze.
Scope: <exact files/folders>.

Task: audit whether the Project Map contains unsupported, stale, duplicated, or conflicting memory.
Use the audit retrieval profile.
Do not change files. Return:
1. confirmed issues;
2. evidence;
3. proposed repair actions;
4. owner questions.
```

---

## 8. Repair Project Map memory

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: apply.
Intent: apply.
Scope: write only these Project Map files: <list>.

Task: repair stale/superseded memory according to the repair retrieval profile.
Rules:
- do not delete historical facts silently;
- mark stale or superseded items;
- add supersession links;
- keep unsupported claims as hypotheses or candidates;
- update indexes;
- update claim ledger if relevant.
```

---

## 9. Remember this

```text
Remember this for <project name>:
<fact / decision / constraint / risk / preference>.

Mode: dry-run first.
Intent: stage.
Create a proposed memory card with class, status, evidence, source authority, lifecycle fields, and retrieval tags. Do not write it until I confirm.
```

---

## 10. Consolidate session notes manually

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: dry-run.
Intent: stage.
Scope: Project Map and the following session notes only: <list>.

Task: consolidate session notes into candidate memory.
Use the Memory Compiler Guide.
Do not promote research output or assumptions to facts unless evidence or owner approval supports them.
Return proposed memory deltas only.
```

---

## 11. Implementation-agent handoff

```text
Active layer: Agent Memory Kit + AI-assisted System Design.
Project: <name>.
Mode: dry-run.
Intent: plan.
Scope: <Project Map files and project docs allowed>.

Task: prepare a copy-pasteable task for the implementation agent.
The task must include:
- goal;
- exact files/paths;
- constraints;
- source-of-truth order;
- do / do not;
- verification commands if known;
- expected result;
- memory/docs update expected after completion.
Do not invent commands, paths, or facts not present in the allowed evidence.
Do not implement it here.
```

---

## 12. Long-running task contract

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: dry-run.
Intent: stage.
Scope: <Project Map files allowed>.

Task: create a proposed task contract for <task> using TASK_CONTRACT_TEMPLATE.yaml.
Do not write it yet. Include goal, non-goals, scope, allowed/forbidden actions, required evidence, done definition, verification recipe, and handoff policy.
```

---

## 13. Insufficient evidence response pattern

```text
Use this response style when evidence is missing:

I cannot answer that as a project fact from the available context.
Available evidence: <list>.
Missing evidence: <list>.
Next safe step: <minimal lookup or owner question>.
No action taken.
```


---

## 13. Existing project adoption

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: dry-run.
Intent: plan.
Scope: the project is already active at <path>. Components: <list>.

Task: propose the safest adoption plan for installing Agent Memory Kit into this existing project without changing product code.
Use EXISTING_PROJECT_ADOPTION_GUIDE.md. If the project already has strong docs or AI instructions, also use MATURE_EXISTING_PROJECT_ADOPTION_PROFILE.md.
Return:
1. recommended secondary-memory governance overlay;
2. current source-of-truth hierarchy if discoverable;
3. confirmation that Project Map remains secondary memory unless `source_authority` says otherwise;
4. first read-only inventory pass;
5. source-authority and permission-policy draft scope;
6. minimal AGENTS.md / Cursor rule patch only if needed;
7. eval smoke-test plan.
Do not write files.
```

---

## 13.1 Mature existing project thin adoption

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: dry-run.
Intent: plan.
Scope: read only the existing repo instructions, source-of-truth docs, current status docs, Project Map/docs layer, and ignore/config files.

Task: strengthen this already working project with Agent Memory Kit ideas without replacing its current system.
Use MATURE_EXISTING_PROJECT_ADOPTION_PROFILE.md.
Answer the six-question intake:
1. current source-of-truth hierarchy;
2. Project Map authority mode;
3. normal read-only exploration for the coding agent;
4. actions requiring explicit apply scope or owner approval;
5. files/data that must stay out of routine agent context;
6. top domain-specific agent failure modes.

Return only a thin adoption slice:
- policy YAML files to add or adapt;
- ignore files to add or adapt;
- small instruction-file patch if needed;
- 5-10 manual smoke eval cases.

Do not propose full memory/task/handoff layout, runtime memory/tooling, or role-stack changes unless a concrete repeated problem requires them.
Do not write files.
```

---

## 14. Eval-suite smoke test

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: read-only.
Intent: audit.
Scope: Agent Kit/kit/eval_suite plus the instruction files currently loaded.

Task: run a manual smoke evaluation against the core behavior eval cases.
Focus on:
- answer-only default intent;
- project grounding;
- retrieval policy compliance;
- stale fact suppression;
- no provider-memory-as-project-truth;
- no mutation without explicit apply intent.
Return an eval run report using eval_run_report_template.yaml.
Do not update files.
```

---

## 14. Significant work checkpoint only

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: dry-run.
Intent: analyze.
Scope: <Project Map files and recent task output>.

Task: decide whether the recent work is significant under SIGNIFICANT_WORK_AND_CHECKPOINTS.md.
Return only:
- significant work: yes/no;
- reason;
- proposed Project Map delta, if any;
- handoff needed: yes/no;
- eval trigger: yes/no;
- no files changed.
```

---

## 15. Run eval checklist preparation

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: dry-run.
Intent: plan.
Scope: Project Map/eval_suite/ and Project Map/eval_runs/.

Task: decide which eval cases should run based on EVAL_AUTOMATION_AND_TRIGGER_POLICY.md.
Do not run tools unless I explicitly ask.
Return:
- trigger reason;
- smoke/category/full recommendation;
- exact cases or categories;
- optional command for run_eval_checklist.py.
```

---

## 16. Convert failure to eval case

```text
Active layer: Agent Memory Kit.
Project: <name>.
Mode: dry-run.
Intent: stage.
Scope: Project Map/eval_suite/ only.

Failure observed:
<describe failure without secrets>.

Task: create a candidate eval case using failure_to_eval_case_template.yaml.
Do not edit files. Do not modify rules. Return the candidate case and one proposed repair target.
```
