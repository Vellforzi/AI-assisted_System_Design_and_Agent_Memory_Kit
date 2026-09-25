# ChatGPT Project Sources Policy

Policy for maintaining ChatGPT Project Instructions and source files in an Agent
Memory Kit project.

## Capability rule

ChatGPT web, Codex and Cursor may all read, generate, edit and publish project
source files when their current tools and the owner request allow it. Do not
hard-code GPT web as read-only or require Cursor/Codex as an intermediary.

Updating local source files, updating connected Drive/Project files, updating the
Project Instructions UI and publishing Git are separate states. Verify each one
that the task claims.

## Source set

Recommended current sources:

- compact Project Instructions source;
- detailed project operating contract;
- project brief/context pack;
- concise `current_state.md`;
- concise `working_state.yaml`;
- `source_authority.yaml`;
- memory index and only relevant current memory records;
- current generated dashboard/index only when it adds useful navigation.

Do not upload an entire repository or Project Map by default. Historical task
artifacts and release archives are not current sources unless the owner requests
historical/forensic work.

## Generator contract

A project may use `Agent Kit/kit/tools/generate_chatgpt_project_sources.py` or an
equivalent deterministic generator. Common outputs:

- `GPT_CONTEXT_PACK.md` / `.json`;
- `CHATGPT_PROJECT_SOURCES_TODO.md`;
- `CHATGPT_PROJECT_SOURCES_MANIFEST.json`;
- `CHATGPT_PROJECT_SOURCES.sha256`.

The generator is optional. A connected tool may update Project Source files
directly when authorized. Generator output does not prove the ChatGPT UI or
another connected copy was updated.

## Determinism

- Context content should avoid volatile timestamps that change hashes without a
  source change.
- Put run timestamps in manifest/TODO metadata, not durable context bodies.
- Repeat generation without source changes should preserve content hashes.
- Record source path, source hash and generated hash.

## Project Instructions

Track a compact instructions source in the project. When the current ChatGPT
surface exposes Project Instructions write access, apply and verify it. Otherwise
update the tracked source and state that UI application remains manual. Do not
claim UI state from a Git or Drive update.

## Structured sources and Canvas

Owner-designated spreadsheets, databases and tables may be Project Sources.
Interactive Canvas files may provide dashboard/filter views but must identify
source and snapshot date. Canvas complements and does not silently replace the
structured source.

## Safety exclusions

Do not upload secret values or secret-bearing raw files, including credentials,
private keys, DPAPI material, browser/session databases and private `.env`
payloads. Use configured authentication without displaying it.

Large raw logs, archives, binaries and unrelated product trees are included only
when the current task and source policy require them.

## Manifest actions

Relative to a verified previous manifest/source state:

- `ADD` — new desired source;
- `UPDATE` — content hash changed;
- `KEEP` — content hash unchanged;
- `REMOVE` — explicitly no longer desired;
- `MISSING` — desired but unavailable.

A local manifest is not proof that a connected ChatGPT Project received the
change. Verify the actual destination when the task requires it.
