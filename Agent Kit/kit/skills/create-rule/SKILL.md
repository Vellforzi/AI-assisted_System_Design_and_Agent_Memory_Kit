---
name: create-rule
description: >-
  Create client-appropriate project instructions for Codex or Cursor. Use when you want to create a
  rule, add coding standards, set up project conventions, configure
  file-specific patterns, create RULE.md files, or asks about .cursor/rules/ or
  AGENTS.md.
---

# Creating project instructions

Identify the actual client and preserve existing project rules and owner
authority. Infer purpose, scope and file patterns from the request,
conversation and inspected files. Choose the narrowest useful scope; reuse
correct existing patterns. Ask only about a material unresolved choice or
information the project cannot supply, not routine globs or repeat approval.

## Client routing

- Codex: use AGENTS.md under its native instruction hierarchy. Consult
  $openai-docs and installed configuration when discovery, precedence or an
  alternate filename matters. Do not copy Cursor frontmatter into Codex
  instructions or assume RULE.md is automatically discovered.
- Cursor: before creating or changing .cursor/rules/*.mdc, read
  [Cursor rules](references/cursor-rules.md) for format, activation and examples.
  Cursor also supports AGENTS.md for plain instructions; preserve the existing
  appropriate mechanism.

## Author the rule

Keep always-loaded guidance short, actionable and focused on one concern.
Split distinct concerns or file scopes when useful; conversation context may
justify several rules. Include concrete examples or relevant canonical files,
preserving conditions, exceptions and safeguards. Examples illustrate agreed
project behavior; they do not authorize new conventions or error semantics.
Reuse existing engineering/communication guidance rather than duplicating it.

Prefer under 50 lines per focused rule; split large rules to stay under 500.
These are authoring guidelines, not platform limits or reasons to drop meaning.

## Verify

Review the diff against the request and preserved instructions. Check the
selected client's path, format and discovery rules. For Cursor, parse YAML,
quote glob strings, verify activation fields and representative matching and
nonmatching paths. Check examples and referenced files.

Report the edited paths, intended scope and actual verification. Valid files
alone do not prove loading or adherence in an already-open client.
