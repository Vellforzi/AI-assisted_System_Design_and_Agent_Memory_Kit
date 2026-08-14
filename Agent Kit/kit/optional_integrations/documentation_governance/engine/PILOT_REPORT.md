# Documentation Lifecycle Engine Pilot Report

Status: passed local contract verification (2026-08-14)

## Scope

The isolated temporary Git fixture covers the optional lifecycle engine only.
It does not activate the engine for Agent Memory Kit Core or for any adopting
repository.

Verified contracts:

- four lifecycle states and exactly-one classification;
- lifecycle coverage for every managed path while only configured text suffixes
  participate in body scans;
- active weekly-style versus include-history body selection;
- global successor and moved-path invariants in both modes;
- Unicode paths and repository-escape link diagnostics;
- explicit worktree delta blocking for a new `DOC-REACH-001`;
- staged-index isolation from an unstaged substitution;
- exact, owned, expiring exceptions;
- safe policy paths and strict repository configuration;
- deterministic repeated JSON for one committed snapshot;
- repository-wide path existence without loading non-document source bodies;
- non-zero CLI exit for a prohibited introduced finding.

## Commands and result

```powershell
python "Agent Kit/kit/tests/test_documentation_lifecycle_engine.py"
python "Agent Kit/kit/tests/test_documentation_governance.py"
python "Agent Kit/kit/tests/test_adoption_profiles.py"
python "Agent Kit/kit/tools/architecture_lint.py"
```

Observed result: 9 lifecycle-engine tests, 8 existing documentation-governance
tests, and 2 adoption-profile tests passed; architecture lint reported zero
findings.

## Real repository report-only pilot

The engine was also evaluated against committed `ai-stock-analyst` revision
`29111871115f0060feb4c59cd98585795e93cb91` through an in-memory adapter for its
richer repository registry. The source harness remained the oracle.

The pilot exposed and closed four portable-engine defects: a large Git batch
pipe deadlock, conflation of lifecycle paths with body paths, missing Git
directory-target recognition, and reachability requirements on
root-discoverable non-entrypoint files. It also aligned the successor invariant
with the adopted contract, which requires an existing registered successor.

Final comparison:

- source lifecycle: 3,209 `docs/` paths;
- source and engine active bodies: 357, 0 findings;
- source and engine include-history bodies: 1,447, 0 findings;
- one exact historical exception translated and applied;
- engine lifecycle total: 3,213 after explicitly adding four root-discoverable
  files.

The durable `baseline-prefix-v1` adapter was subsequently implemented and
installed report-only in `ai-stock-analyst`. Its current worktree report covered
3,216 managed paths and 359 active bodies with zero findings; the explicit
include-history report covered 1,449 bodies with zero unsuppressed findings.
Four repository
contract tests passed across committed active/history, worktree delta, staged
isolation, and merge-base delta modes. Blocking rollout remains a separate
decision after the installation is committed and its Git-backed modes can read
the repository-owned policy from HEAD/index.

## Boundaries

- The engine validates local Markdown links only and does not use the network.
- JSON is the dependency-free canonical configuration syntax. JSON documents
  may use a `.yaml` name because JSON is a YAML subset, but general YAML syntax
  requires a separately owned adapter.
- The engine deliberately does not move or rewrite documents, install hooks,
  create CI jobs, or mutate Git configuration.
- `--worktree` is an explicit mutable view for report-only pilots and
  Orchestrator gates. `--staged`, `--changed`, and `--full` are Git-backed
  views and do not substitute worktree content.
- Semantic truth, authority selection, custody restrictions, and safe archive
  eligibility still require repository-owner review.
