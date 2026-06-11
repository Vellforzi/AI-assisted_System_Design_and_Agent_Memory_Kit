# Git Publishing Guide

Status: publishing and repository hygiene guide
Purpose: help publish Agent Memory Kit without leaking private project data or confusing toolkit files with project memory.

---

## 1. What can be committed

Safe to commit:

- toolkit guides;
- templates;
- eval-suite templates and generic cases;
- example memory cards with fake data;
- README files;
- release notes;
- checksums.

Do not commit:

- real project secrets;
- private raw chats;
- credentials;
- access tokens;
- private client data;
- unreviewed Project Map memory from a private project;
- provider-specific hidden/session dumps.

---

## 2. Recommended repository structure

```text
agent-memory-kit/
  README.md
  START_HERE.md
  RELEASE_NOTES_vX.Y.Z.md
  AI-assisted System Design/
  Agent Kit/
```

For a real project using the kit:

```text
my-project/
  AGENTS.md
  Project Map/
  Agent Kit/              # optional vendored copy or submodule
  src/
```

Keep the toolkit repository separate from private project repositories unless there is a specific reason to vendor it.

---

## 3. Versioning

Use semantic-ish versions:

- patch: wording, typo, small clarification;
- minor: new template, guide, or eval cases;
- major: breaking change in memory schema or operating protocol.

Record major behavior changes in release notes.

---

## 4. Suggested `.gitignore` for projects using the kit

```gitignore
# Local/private agent notes
CLAUDE.local.md
*.local.md
.cursor/rules/*.local.mdc

# Private memory and evidence, if not meant for git
Project Map/raw_sources/
Project Map/eval_runs/
Project Map/side_effects/private*
Project Map/**/secrets*
Project Map/**/*.secret.*

# Common secrets
.env
.env.*
*.pem
*.key
*.p12
*.pfx
```

Adjust per project. Some teams may intentionally commit parts of Project Map; solo owners may prefer private storage.
