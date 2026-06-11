# /multitask

Purpose: decide whether work can be split across independent agents/tasks.

Mode: plan/audit
Mutations: forbidden unless each child task has explicit apply scope

Rules:

- Do not use multitask to compensate for vague scope.
- Split only when tasks have independent files, independent verification, and no shared side effects.
- Require checkpoint/handoff before starting parallel work.
- Prefer separate worktrees/branches if available.
- Warn about higher fuel/token usage.
- Each child task must have: goal, paths, allowed/forbidden, verification, model/settings route, and stop condition.

Return task split, dependency graph, per-task scope, route/settings, fuel risk, and approval points.
