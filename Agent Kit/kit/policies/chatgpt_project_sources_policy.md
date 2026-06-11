# ChatGPT Project Sources Policy

Policy for maintaining ChatGPT Project sources in Agent Memory Kit projects.

## Purpose

Give the owner a **local, deterministic manifest** of what to upload or update in ChatGPT Project sources and Instructions — without UI automation.

## Surfaces

| Surface | Role |
|---------|------|
| GPT web | Read project sources; analyze; draft; scoped IDE-agent tasks |
| Cursor / Codex | Run generator; edit project files; commit when owner asks |
| Owner | Manually upload sources and paste Instructions in ChatGPT UI |

## Generator contract

- Tool: `Agent Kit/kit/tools/generate_chatgpt_project_sources.py`
- Project config: copy `CHATGPT_PROJECT_SOURCES_CONFIG.template.json` → project `CHATGPT_PROJECT_SOURCES.config.json`
- Outputs (under configured `output_dir`):
  - `GPT_CONTEXT_PACK.md` / `.json`
  - `CHATGPT_PROJECT_SOURCES_TODO.md`
  - `CHATGPT_PROJECT_SOURCES_MANIFEST.json`
  - `CHATGPT_PROJECT_SOURCES.sha256`

## Default source set

**Minimal required** (default):

- operating contract
- project brief
- generated context pack
- `current_state.md`
- `working_state.yaml`
- `source_authority.yaml`
- `memory/index.yaml`

**Optional granular** sources only with explicit `--include-optional`.

## Determinism

- Context pack content must **not** include volatile wall-clock timestamps that affect sha.
- Use `source_latest_mtime` (max mtime of configured input files) or omit timestamp.
- Run timestamp belongs only in TODO/manifest metadata.
- Two `--write` runs without source changes must not change context pack content.

## Project Instructions

- Track compact instructions file in project (`instructions_compact_path` in config).
- Owner **manually copies** the `text` block into ChatGPT Project Instructions.
- Generator cannot verify ChatGPT UI state.

## Safety exclusions (never upload)

- `.env`, secrets, credentials files
- `archive/releases` (previous kit releases — not sources by default)
- `.git/`, runtime/canvas/agent-transcript folders
- `*.zip`
- unrelated product trees unless task-scoped and owner-approved

## Manifest actions

Relative to **previous local manifest** only (not verified against ChatGPT UI):

- `ADD` — new desired file
- `UPDATE` — sha changed
- `KEEP` — sha unchanged
- `REMOVE` — was tracked, no longer desired
- `MISSING` — desired but absent on disk

## Release archives

Do not read previous AMK release archives by default when generating sources. Use current Project Map and adopted kit state.
