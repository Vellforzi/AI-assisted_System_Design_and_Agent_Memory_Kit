# Eval Case Builder Skill

Purpose: convert failures into behavior checks.

Use this when the agent repeated a mistake, violated a core rule, or the owner had to correct the agent.

Output a candidate case with:

- id;
- category;
- severity;
- title;
- fixture/context;
- prompt;
- expected behavior;
- disallowed behavior;
- pass conditions;
- fail conditions;
- proposed repair target.

The candidate case is not automatically added to the eval-suite unless the owner approves an apply task.
