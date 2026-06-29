# ChatGPT Project Sources Policy

Status: optional integration policy
Last aligned: <YYYY-MM-DD>
Audience: project owners, AI/Codex sessions, ChatGPT Project maintainers
Runtime impact: none
Authority: optional export policy; subordinate to source authority and core governance

---

## Purpose

Maintain a local deterministic manifest of what to upload or update in ChatGPT
Project sources and Instructions without UI automation.

## Surfaces

| Surface | Role |
|---|---|
| ChatGPT Project | Read project sources, analyze, draft scoped IDE-agent tasks |
| Codex/Cursor/local agent | Run generator, edit project files, verify changes |
| Owner | Manually upload sources and paste Instructions in ChatGPT UI |

## Generator Contract

- Tool: `Agent Kit/kit/optional_integrations/chatgpt_project_sources/generate_chatgpt_project_sources.py`
- Project config: copy `CHATGPT_PROJECT_SOURCES.config.template.json` to project
  root as `CHATGPT_PROJECT_SOURCES.config.json`
- Outputs under configured `output_dir`:
  - `GPT_CONTEXT_PACK.md`
  - `GPT_CONTEXT_PACK.json`
  - `CHATGPT_PROJECT_SOURCES_TODO.md`
  - `CHATGPT_PROJECT_SOURCES_MANIFEST.json`
  - `CHATGPT_PROJECT_SOURCES.sha256`

## Safety Exclusions

Never upload secrets, `.env`, credential stores, raw local databases, raw logs,
runtime dumps, archive releases, `.git/`, zip archives, or unrelated code trees
unless the owner explicitly scopes them and source authority allows it.

## Manifest Semantics

Actions are relative to the previous local manifest, not the ChatGPT UI:

- `ADD` - desired file newly appears in the local manifest.
- `UPDATE` - desired file hash changed.
- `KEEP` - desired file hash unchanged.
- `REMOVE` - previously tracked file is no longer desired.
- `MISSING` - desired file is absent on disk.
