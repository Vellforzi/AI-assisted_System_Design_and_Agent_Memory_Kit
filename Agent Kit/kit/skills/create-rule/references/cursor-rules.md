# Cursor rule format and examples

Read before creating or changing Cursor .mdc rules. These examples are not
Codex configuration or permission to change existing project conventions.

## Location and activation

Project rules use .cursor/rules/*.mdc, for example typescript-standards.mdc,
react-patterns.mdc or api-conventions.mdc. Plain AGENTS.md is another supported
instruction mechanism; RULE.md is not a substitute for a discoverable .mdc rule.

Frontmatter fields: description is a string describing relevance, globs is a
quoted pattern string (comma-separated for multiple patterns), and alwaysApply
is a boolean.

| alwaysApply | globs | description | Inclusion |
|---|---|---|---|
| true | any | any | Every chat session |
| false | provided | optional | Matching file is in context |
| false | omitted | provided | Agent selects by relevance |
| false | omitted | omitted | Manual @mention |

An open editor tab alone is not the stated attachment contract. Keep essential
instructions in the rule body; referenced files are read when needed, not
automatically inlined. Do not claim syntax validation proves actual inclusion.

## Minimal templates

Always-applied project standards:

```markdown
---
description: Core coding standards for the project
alwaysApply: true
---

# Project standards

State the authorized project conventions here.
```

File-scoped rule:

```markdown
---
description: TypeScript conventions for this project
globs: "**/*.ts"
alwaysApply: false
---

# TypeScript conventions

State the conventions for matching files here.
```

Quote glob strings beginning with *: unquoted **/*.ts is invalid YAML.
Use the real project paths and verify relevant matches and exclusions.
Templates contain placeholders; replace them before delivery.

## TypeScript example

This preserves the original error-handling illustration. Use it only where
the project requires this logging and error wrapping, and logger/DataFetchError
exist. Otherwise use the authorized error contract; do not introduce wrapping
or logging merely to imitate the example.

````markdown
---
description: TypeScript coding standards
globs: "**/*.ts"
alwaysApply: false
---

# Error handling

Do not swallow a failure:

```typescript
try {
  await fetchData();
} catch (e) {}
```

Where the project requires logging and a domain error, preserve the cause:

```typescript
try {
  await fetchData();
} catch (e) {
  logger.error('Failed to fetch', { error: e });
  throw new DataFetchError('Unable to retrieve data', { cause: e });
}
```
````

## React example

Use only when these are the project's intended conventions:

```markdown
---
description: React component patterns
globs: "**/*.tsx"
alwaysApply: false
---

# React patterns

- Use functional components.
- Extract custom hooks for reusable logic.
- Colocate styles with components.
```

## Review and source

Check .mdc location, YAML/frontmatter, activation mode and globs, concise focused
content, examples and referenced files. Aim below 50 lines per focused rule;
split large rules to stay below 500 without deleting conditions or safeguards.
The first is our compactness target; the latter follows Cursor's published
authoring recommendation. Neither is a parser limit.

Official source consulted 2026-10-27:
[Cursor Rules](https://cursor.com/docs/rules).
Refresh material platform details when the target client changes.
