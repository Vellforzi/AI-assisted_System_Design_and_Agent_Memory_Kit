# Agent Memory Kit Adoption Profiles

Choose the smallest profile that solves an observed problem. These profiles
describe adoption scope; they do not rename, delete, or relocate any Kit
module.

The presence of a mechanism in the Kit is **not** a recommendation to install
it. Greenfield adoption removes migration cost, not operating cost. Every
optional artifact needs an observable activation trigger before it is added.

## Profile ladder

| Profile | Use it when | Add | Deliberately leave out |
|---|---|---|---|
| **Core** | One owner or a small team needs grounded, owner-controlled work and a lightweight durable record. | A short authority-and-action rule in the existing instruction/documentation system; a current-work note; and, only if decisions would otherwise be lost, a decision note. | Project Map, Python, evals, task contracts, `.work`, generated projections, hooks, CI, MkDocs, and all tool integrations. |
| **Standard** | Repeated sessions or contributors need a bounded way to find relevant project context, or existing-project onboarding is producing context-selection mistakes. | The `secondary_memory_governance/` baseline, used as secondary navigation and memory for an existing repo-centric project. | Workflow contracts and lab automation unless their own trigger is met. |
| **Workflow** | Work is demonstrably multi-session, risky, review-sensitive, or blocked by unclear ownership/dependencies. | The applicable v5 TaskContractV3 and Project Artifact Contract V2 workflow artifacts. | Unrelated lab tooling, automation, or integrations. |
| **Reference Lab** | The owner is evaluating, comparing, or maintaining optional mechanisms with evidence and an explicit operating owner. | Selected evals, helper scripts, integrations, report-only harnesses, hooks, CI, or MkDocs material. | Anything without an explicit owner and an observable activation trigger. |

## Core: small, useful, dependency-free

Core is a usable operating layer, not a placeholder. It has three outcomes:

1. project-specific claims are grounded in the owner and opened project sources;
2. answers stay answer-only until the owner explicitly authorizes a scoped action;
3. current work and important decisions survive the next session in ordinary project documentation.

Core starts with three project-created files, and often fewer because it
extends existing instructions or documentation. It may add up to three more
ordinary project documents only when they have real content, so Core never
requires more than six project-created files. It has no runtime or tool
dependency. Do not create a `Project Map/` for Core. Do not add Python, evals,
task contracts, `.work`, generated projections, hooks, CI, or MkDocs merely to
make Core look complete.

For an existing project, its current `AGENTS.md`, operational documentation,
code, tests, specifications, issues, and current owner instructions retain
their established authority. A Core note is a local operating aid; it does not
replace or elevate itself above those sources.

## Activation rules for optional material

An optional artifact may be proposed only when its trigger is observable in
the project, and it should state its owner, purpose, and removal/rollback path.

| Mechanism | Observable activation trigger |
|---|---|
| `secondary_memory_governance/` / Project Map routing | Repeated session handoffs, multiple contributors, or a documented context-selection error requires bounded navigation. |
| Context Contract V1 or its adapter/oracle | An adopter needs an interoperable, read-only request/bundle/receipt boundary or parity checks across adapters. |
| v5 workflow artifacts and `.work` | `TaskContractV3.workflow_profile`, documented task scale/risk, or an owner-approved review/dependency need requires the specific artifact. |
| Evals | A repeated or material failure mode has a concrete behavior that can be checked. |
| Generated projections, hooks, CI, or MkDocs | An owner adopts a maintained generation/automation path and identifies a reproducible check or publication need. |
| Python helpers or another tool dependency | The owner chooses the helper for a named task and accepts its local operating and maintenance cost. |
| Optional integrations | The target platform or workflow is actually in use and the owner approves the integration boundary. |

No trigger means no installation. A trigger permits a narrow proposal; it does
not grant mutation authority or make the mechanism permanent.

## Standard: existing-project authority first

For a mature repo-centric project, Standard uses
`secondary_memory_governance/` as a secondary-memory overlay. It summarizes,
navigates, and supports bounded retrieval; it does not replace the existing
source-of-truth system. Operational docs, code, tests, specs, issues, and
current owner instructions win whenever the project's authority policy says
Project Map is `secondary_memory`.

Context Contract V1 remains a compatible, read-only projection over the
existing helper surface. Its schemas and fixtures do not require a service,
database, persistent index, or background runtime.

## Workflow: v5 contracts only when the work calls for them

Workflow builds on Core or Standard. Use only the specific v5 artifact that
the observable task need calls for: delivery graph, plan challenge, independent
review, exploration, triage, design probe, capability registry, or bounded
domain language. Routine, single-session work can remain Core; it need not
manufacture workflow files.

Keep v5 schemas and contracts compatible. For existing artifacts, preserve
their authority and follow the existing migration path, including owner review
where it is required. Do not treat workflow metadata as permission to mutate
project sources.

## Reference Lab: evidence before automation

Reference Lab is an opt-in evaluation and integration area, not the default
installation. It is appropriate only after the owner has an observed problem,
a responsible maintainer, and a way to inspect whether the added mechanism
helps. Report-only checks remain report-only unless the owner separately
authorizes a change.

## Selecting a profile

Start at Core. Move up one profile only when a trigger is observable. An
adopter may use a higher profile selectively, but should retain the lower
profile's source-authority and explicit-action rules. Review optional material
periodically: if its trigger disappears, remove it from the adopted workflow
through the project's normal change process rather than treating its presence
in this Kit as a standing requirement.
