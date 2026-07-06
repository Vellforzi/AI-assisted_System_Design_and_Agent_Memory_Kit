# Generated Retrieval Evidence Guide

Status: portable retrieval-safety guide
Purpose: use generated indexes, search caches, and FTS read-models without
treating them as project truth.

---

## Core Rule

Generated retrieval output can narrow candidate sources. It cannot establish
project truth by itself.

Before answering, reviewing, planning, or applying based on a generated hit, the
agent must reopen the canonical source file and verify the relevant content.

## Examples

Generated retrieval evidence includes:

- SQLite/FTS indexes over project files;
- semantic search caches;
- MCP metadata caches;
- local search manifests;
- tool-generated context packs;
- ranked snippets produced from source files.

## Required Metadata

A generated read-model should record enough metadata to support canonical
readback:

- canonical path;
- line range or stable section id;
- content hash when practical;
- generated_at timestamp;
- source allowlist/denylist;
- tool version or script path.

## Forbidden Uses

- Do not treat generated snippets as durable memory.
- Do not use generated output as proof when the source file is missing.
- Do not index secrets or private runtime dumps unless a task explicitly allows
  that private analysis and keeps the output private.
- Do not replace source authority with ranking score.

## Repair Behavior

If generated search points to stale or deleted sources, mark the hit as stale
retrieval evidence and fall back to canonical files, source authority, or
missing evidence.
