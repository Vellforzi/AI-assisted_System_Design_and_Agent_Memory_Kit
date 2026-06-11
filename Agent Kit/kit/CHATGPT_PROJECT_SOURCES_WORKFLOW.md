# ChatGPT Project Sources Workflow

Generic Agent Memory Kit workflow for generating a ChatGPT Project sources manifest and owner TODO.

Works from Cursor or Codex shell. No network calls. No ChatGPT UI automation.

---

## 1. Adopt in a project

1. Copy kit templates into the project (customize names/paths as needed):
   - `CHATGPT_PROJECT_SOURCES_CONFIG.template.json` → `CHATGPT_PROJECT_SOURCES.config.json` (project root)
   - `PROJECT_GPT_OPERATING_CONTRACT.template.md` → `PROJECT_GPT_OPERATING_CONTRACT.md`
   - `GPT_PROJECT_INSTRUCTIONS_COMPACT.template.md` → `Project Map/gpt/GPT_PROJECT_INSTRUCTIONS_COMPACT.md`
2. Copy or symlink the generator into the project, **or** run it from vendored `Agent Kit/kit/tools/`:

```bash
python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config CHATGPT_PROJECT_SOURCES.config.json \
  --write
```

Optional project wrapper (example):

```bash
python docs/tools/generate_chatgpt_project_sources.py --write
```

Project wrappers may hard-code paths; the package tool stays config-driven.

---

## 2. Generate outputs

```bash
python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config CHATGPT_PROJECT_SOURCES.config.json \
  --write

python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config CHATGPT_PROJECT_SOURCES.config.json \
  --check
```

Flags:

| Flag | Meaning |
|------|---------|
| `--write` | Generate/update outputs |
| `--check` | Validate outputs and required sources |
| `--include-optional` | Add optional granular sources from config |
| `--no-optional` | Deprecated alias for default minimal set |
| `--project-root` | Override project root (default: directory containing config) |

---

## 3. Owner manual step (ChatGPT UI)

1. Open `CHATGPT_PROJECT_SOURCES_TODO.md` in configured `output_dir`.
2. Upload/update **minimal project sources** per action table.
3. Copy `text` block from compact Instructions file into ChatGPT **Project Instructions**.
4. Generator actions are relative to the **local manifest**, not verified against ChatGPT UI.

---

## 4. Deterministic rerun check

```bash
python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config CHATGPT_PROJECT_SOURCES.config.json --write
python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config CHATGPT_PROJECT_SOURCES.config.json --write
git diff --name-only
```

Expected: no diff in `GPT_CONTEXT_PACK.md` / `.json` / `.sha256` when inputs unchanged.

---

## 5. Package self-test (fixture)

```bash
python "Agent Kit/kit/tools/generate_chatgpt_project_sources.py" \
  --config "Agent Kit/kit/tools/fixtures/gpt_project_sources_minimal/config.json" \
  --write --check
```

---

## Related files

| File | Role |
|------|------|
| `policies/chatgpt_project_sources_policy.md` | Policy |
| `CHATGPT_PROJECT_SOURCES_CONFIG.template.json` | Project config template |
| `PROJECT_GPT_OPERATING_CONTRACT.template.md` | Operating contract template |
| `GPT_PROJECT_INSTRUCTIONS_COMPACT.template.md` | Instructions template |
| `tools/generate_chatgpt_project_sources.py` | Generator (stdlib only) |
| `eval_suite/cases/AMK-GPS-001.yaml` | Behavior eval case |
