# Agent-authored memory (optional module)

Version: `0.1.1-local`. Local source addition, not an Agent Kit release.
Requires Python 3.11+ with SQLite FTS5. Uses only the standard library.
No LLM API, embeddings, other models, GPU, WSL, network calls or background
collection. The current owner-selected agent performs semantic work in its
existing session. This module stores, validates and retrieves its results.

## Responsibilities and source authority

The owner defines requirements. Opened current source and actual observations
establish implemented behavior. The agent extracts a compact English record and
RU/EN search alternatives. The tool checks structure, identity, evidence file
hashes, revision-bound relationships and lifecycle. These mechanical checks do
not prove that the agent understood the source, translated correctly, chose the
right evidence role or satisfied the owner's acceptance criteria.

One JSON file per memory ID under the configured `records_dir` contains its
append-only, hash-linked revision history. This is part of the adopting project's
Project Map, not an independent competing source of truth. Existing project
memory remains in place. `reference_files` only adds explicitly selected files
to a search projection; it never imports them as newly verified facts.

SQLite under `cache_dir` is disposable. Search checks the corpus fingerprint and
builds an in-memory index when the persistent index is absent/stale. A search does
not write canonical records or the persistent index. `index` explicitly refreshes
the generated cache. Missing/oversized reference sections report partial coverage.
An empty result is never proof that the information does not exist.

## Language contract

- `language: en` labels canonical project records; the current agent writes the
  title, summary, applicability and verification explanation in English.
- `original.text` retains exact owner/source wording in Russian, English or mixed
  language. Paths, symbols, errors, protocol tokens and original bytes stay intact.
- `search_keys.ru` and `search_keys.en` are search aids, not independent facts.
- Owner-facing conversation follows the owner's preferred language.
- Bilingual Space pages keep their original language. Only an explicitly supplied
  local export can become a source. This module does not access or synchronize
  ChatGPT Space, Pages, cloud conversations or the user's entire chat history.
- Unicode tokenization plus agent-written aliases is not an embedding model,
  automatic translation or a complete Russian morphological search engine.

## Installation and safe updating

From an inspected module checkout:

```text
python "Agent Kit/memory/install.py" --project "path/to/project"
python "Agent Kit/memory/install.py" --project "path/to/project" --write
```

Preview writes nothing. The installer changes only `Agent Kit/memory/` and the
separate `Agent Kit/MEMORY_INSTALLATION.json`. It does not change the core package
version, `INSTALLATION.json`, project records, instructions or global settings.
Unmodified installed files can be updated; local edits/removals block application
and remain intact. Source manifest integrity and target preimages are checked.
Installation is atomic per file, not a filesystem-wide transaction. A interrupted
installation is rerun from the same inspected source; identical files are retained.

Create a project-owned configuration from `config.example.json`, deliberately
select source files and languages, then connect the project router to `SKILL.md`.
`write_enabled` is a storage guard, not permission to perform arbitrary actions.
The current owner request and applicable project instructions remain controlling.
No extra approval for an already authorized memory update is implied.

## Commands (run from the selected project)

```text
python "Agent Kit/memory/cli.py" --project . status
python "Agent Kit/memory/cli.py" --project . source "path/to/evidence.md"
python "Agent Kit/memory/cli.py" --project . stage --input "candidate.json" --operation-id TASK-001-stage --expected-revision 0
python "Agent Kit/memory/cli.py" --project . lifecycle MEM-001 --status active --operation-id TASK-001-activate --expected-revision 1 --reason "Source-level evidence reviewed; runtime not checked"
python "Agent Kit/memory/cli.py" --project . search --query "память без API" --query "subscription memory" --branch main
python "Agent Kit/memory/cli.py" --project . context --query "component lifecycle" --scope agent.memory --budget 8000
python "Agent Kit/memory/cli.py" --project . read MEM-001 --history
python "Agent Kit/memory/cli.py" --project . audit
python "Agent Kit/memory/cli.py" --project . index
```

Use structured argv (especially for spaces and Cyrillic). All responses are JSON;
errors use exit code 2 and do not echo payload content. `stage` accepts an exact
input file; it does not call a model. IDs and operation IDs are stable across retries.
`expected-revision=0` creates a new ID. Every lifecycle transition increments its
revision. An identical repeated operation reports both its original accepted
revision and the current revision; it does not apply again.

## Capture, consolidation and lifecycle

At a meaningful task boundary, the current agent prepares a candidate, checks its
sources and scope, stages it, activates only supported content, and reads it back.
Do not record every message. Record decisions, facts, reusable experiences,
failed approaches, questions or compact task recovery state. An experience must
state applicability, limitations and evidence rather than generalize one success.

Candidates are excluded from default recall. To update an active record, stage a
new candidate with the current revision; reactivation requires current evidence.
The previous active version stays in history, not as a fallback truth.
`revoked`, `rejected` and `superseded` records cannot be resurrected by delayed
processing. Record a genuinely new owner decision under a new ID with new evidence.

Supersession is explicit: activate the supported successor, then mark the older
record `superseded` with `--successor`. They must address the same subject, scope
and branch. These are two checked operations, not an atomic multi-record update.
Do not claim consolidation finished between them. Revoking the successor never
automatically makes the older decision current again.

`derived_from` links bind a parent revision. A parent correction, retirement or
source drift makes dependent recall stale. A `related` link is navigation, not a
truth dependency. Existing independent evidence must still support each claim.
Injected context markers and recall/translation-only origins are rejected. Known
same-subject duplicates are rejected. Arbitrary paraphrases are not guaranteed to
be detected mechanically: the agent must preserve provenance and check for them.

## Evidence and safety

Each evidence reference specifies project-relative path, SHA-256, role and
`freshness` (`required` or `historical`). A current claim needs at least one
currently checked origin. Use required current-source evidence for implementation
claims; retain an owner statement as the requirement's source and mark incidental
code references historical when code drift should not repeal the requirement.
Never label source/test evidence as runtime, publication or owner acceptance.
Hash checks preserve provenance, not authenticity or semantic validity.

A file change invalidates affected recall, not the whole project. Required missing
sources suppress active recall. Audit exposes the reason; it never silently
repairs facts. Memory/cache files cannot be their own independent evidence.
Secrets and hidden reasoning do not belong in records. Obvious credential patterns,
credential paths, traversal, symlinks and Windows reparse paths are rejected; this
is a conservative guard, not a complete secret-detection system. Source readers
use explicit local files only. Raw source contents are not copied automatically.

OS file locks serialize cooperating writes and release on process exit. Revision
CAS, append-only history hashes and preimage/readback checks protect updates.
Non-cooperating filesystem writers are not a distributed transaction system;
preserve the adopting project's writer coordination. Do not edit JSON histories
manually or erase cancelled decisions to make a check pass.

## Retrieval bounds and costs

FTS5 `unicode61` indexes normalized title, aliases and content. Exact record IDs
rank first; FTS uses BM25 field weights 8/5/1 for title/aliases/content. Scope and
branch are filtered before selecting results. `*` branch means explicitly shared
knowledge, never permission to merge branch-local facts. Historical mode retains
the status labels. Pagination exposes the next offset; the caller must retain
query/filter arguments. Hit objects obey a configurable character budget; the
small metadata envelope is additional. The tool does not claim tokenizer counts.

The initial bounded implementation rereads/hash-checks the explicit corpus for
freshness; no whole-repository scan is performed. Max 5000 indexed records/sections,
8 MiB per input/history file, 48 KB per record, and 20 evidence refs per record.
Large repeated dependency graphs can need additional caching; measure before
expanding. No background model job or hidden subscription usage is started.

## Verification

Run `python -B -m unittest discover -s "Agent Kit/memory" -p test_memory.py -v`.
See `EVALUATION.md`. Deterministic test success is not an LLM benchmark or proof
that another ChatGPT/Codex session has discovered/used this skill.

Implementation references (checked 2026-10-17): SQLite FTS5 documentation
https://www.sqlite.org/fts5.html and Python sqlite3 documentation
https://docs.python.org/3/library/sqlite3.html. Design inspiration: Hy-Memory's
separation of working facts/experience, search keys and derived-echo safeguards;
no Tencent model or SDK code is required or included.

## Local completion hardening (0.1.1-local)

CLI stdout is explicitly UTF-8, including under a non-UTF-8 Windows parent
locale. No shell code-page change is needed. English canonical summaries and
original RU/EN/mixed Unicode survive the real CLI boundary.

An active record's claimed verification level must have matching `required`
evidence; a `historical` runtime/owner report cannot satisfy that level. The same
check applies during read, search, audit and generated context, including records
accepted by an older writer. History is preserved; affected records are reported
as effectively stale. Hash validity still does not prove semantic truth.

Both language-key arrays must be nonempty. Invalid optional text/list fields are
rejected before storage, so a malformed candidate cannot poison the next search.
