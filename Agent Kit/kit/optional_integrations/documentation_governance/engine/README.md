# Documentation Lifecycle Governance Engine

Status: optional Reference Lab implementation; inactive until copied and
configured by an adopting repository

This directory is the portable implementation for repositories whose document
corpus has outgrown the compact report-only harness. It adds explicit lifecycle
classification, Git-backed snapshots, active/history body selection,
reachability, successor and moved-path invariants, precise expiring exceptions,
and finding-delta gates.

Every Git path under `document_roots` participates in lifecycle classification,
including binary evidence and digest-bound artifacts. `document_suffixes`
selects only the bodies that are safe and useful to decode for link/anchor
checks. Thus global lifecycle coverage and recurring body-scan cost remain
separate quantities.

[`checks_registry.json`](checks_registry.json) is the stable public finding-ID
contract for gates and reporting. Add or change a blocking ID only through an
explicit compatibility decision.

It does not replace `../../../../tools/documentation_harness.py`. The compact
harness remains the default Core/Standard/Workflow surface. Adopt this engine
only after an inventory and report-only pilot demonstrate the need.

## Install shape

Copy `documentation_governance/` and `documentation_governance_cli.py` beside
each other, normally below the target repository's `scripts/`. Copy the three
JSON templates into repository-owned paths and replace every example path with
the target repository's reviewed inventory. The loaders are dependency-free
and enforce the contract directly; the Draft 2020-12 schemas are supplied for
editors and independent validators.

Never copy another repository's lifecycle rules, counts, entrypoints,
exceptions, or baseline revision as defaults.

Repositories that already own a reviewed frozen-baseline registry may set
`"registry_adapter": "baseline-prefix-v1"`. The adapter resolves the registry's
baseline revision through Git, keeps baseline-only and post-baseline rules
separate, supports exact paths, prefixes, exclusions and fallback, expands
multi-target navigation routes, and translates only the legacy exact-reference
exception shape it recognizes. Unknown adapter fields and exception rule IDs
fail closed.

## Commands

```powershell
# Explicit report-only pilot over the current worktree
python scripts/documentation_governance_cli.py --root . --format json check --worktree --fail-on never

# Pre-commit: candidate is exactly the Git index; unstaged substitutions are ignored
python scripts/documentation_governance_cli.py --root . --format markdown check --staged
python scripts/documentation_governance_cli.py --root . --format markdown delta --staged --forbid DOC-REACH-001

# Pull request: candidate is HEAD; baseline is the merge base
python scripts/documentation_governance_cli.py --root . --format json delta --changed origin/main --forbid DOC-REACH-001

# Scheduled committed snapshots
python scripts/documentation_governance_cli.py --root . --format json check --full
python scripts/documentation_governance_cli.py --root . --format json check --full --include-history
```

`--worktree` is deliberately explicit and is intended for report-only pilots
and Orchestrator task gates before staging. `--staged` and `--changed` never
read worktree content. `--full` reads committed `HEAD`, making repeated reports
for one revision deterministic.

## Orchestrator boundary

Orchestrator already understands `DocumentationGovernancePolicyV1`. Use
`templates/orchestrator_documentation_governance.template.yaml` in a queue's
project block. Orchestrator owns task scope, required command execution, and
final whole-change acceptance. This engine remains the repository-owned oracle
that decides whether `DOC-REACH-001` or another prohibited finding was added.

The engine does not move files. Archive migration remains an explicit atomic
change: move, lifecycle update, old-to-new registration, active-reference
update, and full validation.
