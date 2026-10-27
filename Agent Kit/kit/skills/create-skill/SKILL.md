---
name: create-skill
description: Create or update a skill for the selected Codex or Cursor client. Establish its actual discovery path and invocation policy; preserve existing client-specific metadata.
---

# Create or update a skill

Use the owner's named client, otherwise the current client. Infer established
facts; ask only when unresolved client/scope ambiguity changes the installation
location. Resolve host paths and the user's home; do not copy another platform's
absolute paths.

## Source and copies

Resolve the declared canonical source and mirrors before editing; use the
installed path only if no separate source is declared. Inspect drift and edit
the source. For mirrors, synchronize only declared files and run the registered
mirror checker. Never overwrite unreviewed drift or create an independently
maintained duplicate. Preserve portable variants; add project semantics only
when expressly part of adoption. Never write into client-managed built-in skill
directories. Do not edit versioned plugin caches as durable fixes.

## Client rules

For Codex, read system $skill-creator through the current catalog for authoring;
do not duplicate it. Resolve discovery against the actual client/catalog and
current documentation, not a generic initializer default. Normally use
.agents/skills/<name>/ for repository skills and ~/.agents/skills/<name>/ for
personal skills. Honor explicitly selected supported locations; legacy .codex
locations may already be catalogued.

SKILL.md requires YAML name and description. Preserve interface, invocation
and dependency metadata. Automatic selection is the default; only an explicit
owner request changes a skill to explicit-only:
- Codex: policy.allow_implicit_invocation: false in agents/openai.yaml.
- Cursor: disable-model-invocation: true when the target version supports it.
Never substitute Cursor's field for Codex policy.

For Cursor, consult current documentation or installed instructions for
discovery/metadata. Normally use .cursor/skills/<name>/ or
~/.cursor/skills/<name>/; preserve supported invocation settings.

## Author and verify

1. Establish task, trigger, exclusions, inputs and observable result; retain
   owner-required exact wording. Reuse suitable skills; avoid duplicate names.
2. Keep the entrypoint focused; link conditional detail only when it saves
   context. No empty scaffolding. Match procedure to risk; retain authority
   boundaries without invented approvals, fixed agent counts or client-specific
   tool names.
3. Review the final diff, parse supported frontmatter, resolve references and
   run changed helpers. Test positive/negative trigger examples when possible.
4. Report exact installed paths and verification limits. Static validity does
   not prove activation; claim an already-open client loaded changes only with
   evidence.
