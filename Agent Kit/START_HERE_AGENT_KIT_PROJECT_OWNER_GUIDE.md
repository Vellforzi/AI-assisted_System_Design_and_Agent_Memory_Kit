# Owner start

Published version: 4.3.0.

Describe the outcome, important constraints and what would count as success.
The agent inspects the relevant current source, implements the authorized local
work and verifies it. Analysis-only requests do not authorize mutation.

Read `portable/core/WORKFLOW.md`. Preview installation with
`python "Agent Kit/portable/manage.py" --project "your/project"` and add
`--write` to install. Existing instructions and context are preserved.

Afterward, ask for a normal small project change and inspect its evidence.
Enable optional recovery, hooks, evals or delegation only when a repeated problem
or the task's risk justifies the mechanism. See `portable/core/OPTIONAL.md`.

Production-code projects should also review
`kit/PRODUCTION_CODE_CHANGE_GUIDE.md`. During adoption, the kit should offer this
quality pack explicitly rather than enabling hooks silently.
