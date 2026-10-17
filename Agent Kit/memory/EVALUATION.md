# Memory evaluation contract

These tests measure deterministic storage/retrieval behavior, not an LLM score.
No API or extra model is used. Source files and databases are disposable fixtures.

| Criterion | Independent oracle |
|---|---|
| English records with RU/EN recall | Fixed RU/EN questions point to the preselected same ID |
| Original wording | Exact Unicode input equals stored/read original |
| Source freshness | Independently changed source bytes hide the older claim |
| Evidence levels | Source evidence cannot activate a runtime-level claim |
| Owner decisions | Agent analysis cannot activate as an owner statement |
| CAS and retries | Old revision fails byte-zero; identical operation executes once |
| Retirement | Revocation/supersession never restores an old fact |
| Dependencies | Parent revision/lifecycle change invalidates dependent recall |
| Scope/branch isolation | Main, feature and another component return different IDs |
| Echo and provenance | Marked recalls, record-as-evidence and known duplicates fail |
| Index integrity | Missing/stale cache is rebuilt in memory without canonical writes |
| Coverage/pagination | Missing refs are labelled; pages contain every eligible fixture ID once |
| Optional install | Preview writes nothing; local edits/removals block replacement |
| No model/network dependency | Networking is forbidden during the test pipeline |

Run with the adopting project's real Python on Windows, not only the authoring
container. Report test count, failures and skips. A symlink fixture may be skipped
when the Windows account cannot create symlinks; report that limitation.

For task-level improvement, maintain a separate fixed corpus of real project
questions and expected source IDs, with Russian/English/mixed versions. Compare
baseline literal search with aliases on the same corpus. Include wrong branches,
stale decisions, interrupted tasks and source/build/runtime distinctions. Record
correct references, false-current results, context size and latency. Do not present
a curated lexical fixture or a passing schema as measured improvement to actual
model reasoning, free-form paraphrase recall or production task completion.

Completion regressions: actual CLI subprocesses are tested with cp1251 and UTF-8
mode disabled; a deleted historical runtime report must not activate current
runtime status; an old-writer fixture must be suppressed without history edits;
malformed optional fields and missing RU/EN aliases fail before storage. These
are distinct transport, evidence-level and input-contract checks, not more LLM
benchmark cases. Top-1 and top-3 retrieval are separate metrics.
