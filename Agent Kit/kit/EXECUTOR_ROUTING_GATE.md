# Executor Routing Gate

Status: portable capability-based routing rule.
Purpose: choose an execution surface from current evidence without turning a
product name into authority or a mandatory intermediary.

## Core rule

Route by:

1. current owner outcome and authorized actions;
2. current live tool/capability catalog;
3. task fit, context and evidence needs;
4. current repository/runtime boundaries.

ChatGPT web, Codex, Cursor and other connected agents are first-class execution
surfaces. Any may analyze or execute owner-authorized work when its current tools
support the task. External/current research is a ChatGPT strength, not a
read-only role restriction. Tool identity never creates permission; owner
instruction does.

Do not require an Executor Routing Gate for every trivial task. Use it when the
surface materially affects capability, cost, evidence, side effects or handoff.

## Recommended block

```yaml
Executor Routing Gate:
  candidate_surfaces:
    - <surface and current live capabilities>
  selected_surface: <one surface>
  selection_reason: <task-fit reason>
  capability_evidence:
    - <current tool catalog, project file or owner input>
  missing_capabilities: []
  owner_authority: <current instruction/ref>
  side_effect_boundary: <what is and is not in scope>
  reroute_trigger: <specific condition>
```

## Rules

- No surface is generally superior.
- Do not hard-code that repository edits belong to Cursor/Codex or that GPT web
  is advisory-only.
- Do not route to another surface merely because an old template says so.
- A missing capability on one surface is a reason to select another capable
  surface, not a project-wide prohibition.
- Use exactly one writer for overlapping state. Independent writers need truly
  isolated scopes and explicit integration ownership.
- Do not invent model names, context limits or UI controls from memory; use
  current provider evidence when exact settings matter.
- The owner gate is required only for an action outside authority already given,
  not for a duplicate confirmation.

## Evidence layers

A selected executor must still distinguish:

- source edit;
- test/check;
- build/compile;
- repository publication;
- deployment or tag-triggered rebuild;
- runtime smoke;
- owner acceptance.

Routing to a capable surface does not collapse those layers or prove success.

## Validation guidance

A project-specific validator may verify that a routing block is syntactically
present, but a missing block must not automatically block useful work when the
surface and capability are already unambiguous. Validators are evidence tools,
not independent permission gates.
