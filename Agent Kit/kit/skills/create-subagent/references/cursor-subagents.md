# Cursor format and subagent examples

Read for Cursor configuration or a relevant example pattern. Use with
[the core](../SKILL.md). These templates do not create, invoke or authorize a
role by themselves. Apply the current parent/owner contract and project policy;
do not copy Cursor metadata into a native Codex role.

## Locations and format

| Location | Scope | Priority |
|----------|-------|----------|
| `.cursor/agents/` | Current project | Higher |
| `~/.cursor/agents/` | All your projects | Lower |

When multiple subagents share the same name, the higher-priority location wins.

Use project scope for codebase-specific roles and user scope for personal
cross-project reuse. Sharing through Git requires current publication authority.
Check existing definitions and name collisions before adding one.

Create a `.md` file with YAML frontmatter and a markdown body (the system prompt):

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Use the following explicit authoring fields, even though current Cursor
documentation makes both optional (name can derive from the filename). This is
our clarity convention, not a schema-required-fields claim.

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (lowercase letters and hyphens only) |
| `description` | When to delegate to this subagent (be specific!) |

Create only the selected file using tools native to the execution host. The
following Unix shell illustration preserves the path examples; it is not a
Windows command requirement or an instruction to create both scopes.

```bash
# For project-level
mkdir -p .cursor/agents
touch .cursor/agents/my-agent.md

# For user-level
mkdir -p ~/.cursor/agents
touch ~/.cursor/agents/my-agent.md
```

## Descriptions

The description guides delegation: name the task and trigger rather than saying
"Helps with code". Proactive language is appropriate only when owner/project
delegation policy permits it; it never overrides a no-spawn boundary.

```yaml
description: Reviews the assigned diff for correctness, security and maintainability when delegated by the parent.
```

## Reviewer example

Adapt the relevant checklist to the assigned work and current engineering rules.
Do not add a separate review task merely because this example exists.

```markdown
---
name: code-reviewer
description: Reviews the assigned diff for correctness, security and maintainability when delegated by the parent.
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff for the assigned change; remain read-only
2. Focus on modified files
3. Begin the assigned review once invocation is authorized

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

## Debugger example

```markdown
---
name: debugger
description: Investigates assigned errors, test failures and unexpected behavior; fixes only within the parent-authorized write scope.
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement the minimal fix only within the authorized paths/actions; otherwise report the proposed fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging only when needed and within authorized write scope
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

## Data-analysis example

```markdown
---
name: data-scientist
description: Analyzes assigned SQL/BigQuery questions and data; executes queries only within current authorization.
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate, available and authorized; otherwise provide the query and execution gap
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

## Validation and troubleshooting

Validate the selected file's path, .md extension, YAML syntax and prompt content.
When invocation is authorized, use a bounded representative task, for example:

```
Use the my-agent subagent to [task description]
```

Inspect the actual result, forbidden effects and evidence. A valid file does
not establish discovery, actual model selection or runtime enforcement. If the
role is unavailable, check .cursor/agents/ versus ~/.cursor/agents/, extension,
name conflicts, frontmatter and host capability before changing settings.

## Client boundaries and sources

Official sources read on 2026-10-27; refresh when the target host/version changes:
- [Cursor subagents](https://cursor.com/docs/subagents): Markdown configuration,
  scope precedence and optional name/description fields.
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents):
  native TOML and required name, description and developer_instructions; use
  $openai-docs for current Codex configuration instead of these Cursor templates.
- [Codex skill metadata](https://learn.chatgpt.com/docs/build-skills#optional-metadata):
  this skill's explicit-only intent is represented by policy.allow_implicit_invocation=false
  in agents/openai.yaml, replacing its legacy disable-model-invocation field.

The old invocation flag's actual effect was not verified; the new file uses the
documented mechanism. This says nothing about whether an already-open client has
loaded the new policy. It does not disable or reconfigure any existing subagent.

At this documentation snapshot, sandbox_mode in a Codex custom-agent file does
not override the parent configuration, and service tier follows the root session.
Existing local roles contain such fields. Their presence is not proof of runtime
enforcement. Preserve those role files; report any mismatch between project
constraints and effective settings rather than claiming an unsupported guarantee
or bypassing the constraint. Model/effort choices and capabilities require their
own current verification. A prompt boundary is not an OS sandbox.
