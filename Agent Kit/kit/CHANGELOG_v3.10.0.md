# Agent Memory Kit v3.10.0 — ChatGPT Project Sources Manifest Workflow

Release date: 2026-06-11
Status: minor feature release.

## Purpose

v3.10.0 adds a generic, config-driven workflow for building ChatGPT Project sources manifests from local project files. The workflow is local and deterministic; the owner manually updates ChatGPT Project sources in the UI.

## Added

- `CHATGPT_PROJECT_SOURCES_WORKFLOW.md`
- `CHATGPT_PROJECT_SOURCES_CONFIG.template.json`
- `GPT_PROJECT_INSTRUCTIONS_COMPACT.template.md`
- `PROJECT_GPT_OPERATING_CONTRACT.template.md`
- `policies/chatgpt_project_sources_policy.md`
- `tools/generate_chatgpt_project_sources.py` — config-driven stdlib generator
- `tools/fixtures/gpt_project_sources_minimal/` — minimal fixture for generator validation
- eval case `AMK-GPS-001` (`gpt_project_sources` category)

## Updated

- `eval_suite/manifest.yaml` — `gpt_project_sources` category and `AMK-GPS-001`
- `eval_suite/eval_trigger_policy.yaml` — smoke category and trigger matrix for `gpt_project_sources`
- `eval_suite/README.md`
- `tools/README.md`, `kit/README.md`

## Key rules

- Generator workflow is local, config-driven, and deterministic.
- Owner manually pastes compact Instructions and uploads sources in ChatGPT Project UI.
- No ChatGPT UI automation.
- No JOB-specific payload included.
- Default minimal required source set unless owner requests granular optional sources.
- Exclude secrets, `.env`, runtime/canvas dumps, and `archive/releases` paths from uploads.
