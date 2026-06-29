# ChatGPT Project Sources Optional Integration

Status: optional integration
Last aligned: <YYYY-MM-DD>
Audience: project owners, AI/Codex sessions, ChatGPT Project maintainers
Runtime impact: none; local file generation only
Authority: optional export workflow; does not override source authority or core governance

---

## Purpose

Generate a local, deterministic manifest of files to upload to ChatGPT Project
sources, plus a compact context pack and manual owner TODO. The generator does
not call the network and does not automate the ChatGPT UI.

Use this when ChatGPT is a read-only research, design, or analysis surface and
local agents such as Codex/Cursor remain responsible for repository changes.

## Files

- `generate_chatgpt_project_sources.py` - stdlib-only generator.
- `CHATGPT_PROJECT_SOURCES.config.template.json` - copy to project root as
  `CHATGPT_PROJECT_SOURCES.config.json`.
- `PROJECT_GPT_OPERATING_CONTRACT.template.md` - copy to project root as
  `PROJECT_GPT_OPERATING_CONTRACT.md`.
- `PROJECT_AI_BRIEF.template.md` - copy to project root as
  `PROJECT_AI_BRIEF.md`.
- `GPT_PROJECT_INSTRUCTIONS_COMPACT.template.md` - copy to
  `docs/project_map/chatgpt_project/GPT_PROJECT_INSTRUCTIONS_COMPACT.md`.
- `chatgpt_project_sources_policy.md` - optional policy reference.

## Adopt

1. Finish the core `secondary_memory_governance/` install first.
2. Copy and customize the templates listed above.
3. Run:

```bash
python "Agent Kit/kit/optional_integrations/chatgpt_project_sources/generate_chatgpt_project_sources.py" --config CHATGPT_PROJECT_SOURCES.config.json --write --check
```

4. Open `docs/project_map/chatgpt_project/CHATGPT_PROJECT_SOURCES_TODO.md`.
5. Manually upload/update the listed files in ChatGPT Project.
6. Manually copy the `text` block from
   `docs/project_map/chatgpt_project/GPT_PROJECT_INSTRUCTIONS_COMPACT.md` into
   ChatGPT Project Instructions.

## Boundaries

- No UI automation.
- No network calls.
- No secrets, `.env`, local databases, raw logs, archives, runtime dumps, or
  unrelated code trees.
- Manifest actions are relative to the previous local manifest only; they do
  not prove current ChatGPT UI state.
