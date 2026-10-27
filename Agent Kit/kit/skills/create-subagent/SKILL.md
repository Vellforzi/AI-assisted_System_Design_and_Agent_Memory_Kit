---
name: create-subagent
description: Create or update a focused custom subagent for the selected Codex or Cursor client, including its prompt, configuration and validation.
---

# Create a custom subagent

Use the client requested by the owner, otherwise establish the actual host from
current configuration. Do not infer it from this skill's old title or examples.
Separate creation of a role from launching it. Honor analysis-only requests.

Use context isolation, specialization or reusable configuration where it serves
a concrete task. An isolated conversation does not imply an isolated checkout.
Reuse a suitable existing role instead of creating a duplicate.

## 1. Define scope and authority

Infer purpose and workflow from the conversation. Establish project/user scope,
one focused responsibility, trigger, inputs, permitted reads/writes/actions,
required evidence, output and stopping condition. Ask only for material gaps.

Follow current owner and project delegation rules. A role description does not
authorize spawning, recursive delegation, product changes, external actions or
Git publication. Preserve unrelated roles and configuration.

## 2. Use the target client's format

- **Codex:** use $openai-docs and the installed configuration/schema. Current
  native custom agents use TOML under .codex/agents or the personal Codex agents
  directory, with name, description and developer_instructions. Verify discovery,
  supported fields and effective settings on the actual host.
- **Cursor:** before writing, read [Cursor format and examples](references/cursor-subagents.md).
  Use project .cursor/agents/ or personal ~/.cursor/agents/ Markdown files with
  YAML frontmatter and a prompt body. Check name collisions and scope precedence.

Prefer project scope for codebase-specific roles and user scope for personal
cross-project reuse. Use explicit, descriptive names and triggers. Keep name
and description even where the client makes them optional; distinguish this
authoring convention from schema requirements.

## 3. Write the role

State the task, bounded workflow, constraints, evidence and response format.
Avoid vague descriptions. Use proactive trigger language only when the owner
and applicable delegation policy permit that behavior, never as a blanket default.

Reuse applicable engineering and communication guidance instead of copying
general quality checklists into every role. Read the relevant reviewer, debugger
or data-analysis example in the reference when using that pattern; examples do
not add authority or require unrelated work.

Choose model and effort for the task under current policy; preserve explicit
owner settings and registered-role constraints. Verify supported configuration
and effective model, effort and execution mode before claiming they applied.
Do not treat a prompt restriction or an unsupported configuration field as
enforced permissions, sandboxing or runtime isolation.

## 4. Validate and report

Create or update only the selected role and necessary registration. Use native
paths and tools, preserve unrelated entries, and validate the actual TOML/YAML
schema, filename, discovery path and description.

Test a bounded representative invocation when authorized and supported; inspect
the result against the role contract, including forbidden actions and required
evidence. Do not claim a file/schema check proves discovery or runtime behavior.
Do not launch an agent merely because a template says to test it.

If unavailable, inspect path, extension, naming, frontmatter/configuration and
host capability before changing settings. Report the installed files, intended
scope/trigger, actual validation and any discovery, model or execution gap.
The parent remains responsible for verifying results and the final verdict.
