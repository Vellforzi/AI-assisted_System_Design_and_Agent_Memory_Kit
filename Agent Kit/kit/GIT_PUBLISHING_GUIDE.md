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
- checksums;
- `LICENSE`.

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

## 2.1 Live extraction into the published kit

The intended maintainer path is:

1. a practice that worked in a private project;
2. strip product names, hosts, account ids, owner-identifying paths, and secrets;
3. keep the invariant, gate, oracle, and failure mode;
4. write or update a kit guide so a stranger can use it;
5. point `START_HERE.md` and `QUESTIONS_THIS_KIT_ANSWERS.md` at the new file;
6. add an eval case if the failure is repeatable.

Do not publish a private Project Map as the kit. Do not leave Cursor/Codex
setup only in the private repo: those packs belong in the kit so the
contour actually loads for other users.

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

---

## 5. Windows Explorer and `.git` (`desktop.ini`)

Windows Explorer can drop `desktop.ini` into `.git/refs/`, `.git/objects/`,
and `.git/logs/` if those folders are opened in Explorer. Git then treats
them as broken refs (`bad object refs/desktop.ini`) and fetch/repack can
fail. These files are not git objects. They are not part of the kit.

Do not browse `.git` in Explorer. `desktop.ini` is already in the kit
`.gitignore` for the working tree; that does not protect files inside `.git`.

If warnings appear, delete only files named `desktop.ini` under `.git`
(never delete hex object files). From Git Bash at the repository root:

```bash
find .git -name desktop.ini -type f -delete
```

Then `git status` and `git log -1` must still work. Do not rewrite tags or
history to "fix" this. Do not commit anything from `.git/`.

