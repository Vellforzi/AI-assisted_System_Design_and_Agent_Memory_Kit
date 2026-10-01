# Agent Memory Kit v4.3.1 Changelog

Release source date: 2026-10-01.
Previous published release: `v4.3.0`.

v4.3.1 makes the human/model capability boundary impossible to mistake during
onboarding and model routing. It does not add provider-specific product logic.

## Added

- Canonical `HUMAN_MODEL_CAPABILITY_CONTRACT.md`.
- A first-class adoption check: ask the kit questions through the agent and treat
  an agent that cannot answer from current files as not ready for material work.
- Active `AMK-HMC-001` eval for model capability, result-first routing and human
  responsibility.

## Changed

- Root and package entrypoints now display a prominent warning that Agent Memory
  Kit is a multiplier, not a brain.
- `MOTIVE_AND_ANALOGY.md` now states the missing model and human halves explicitly.
- `CAPABILITY_MANAGEMENT.md` uses a four-factor weakest-link model: model
  capability, constraint contour, current evidence and operator judgment.
- Model routing now establishes the capability floor before price optimization;
  planning and execution may use different models.
- Adoption guides and owner review begin with capability and responsibility
  checks instead of hiding them in optional guidance.
- Package, eval and release metadata advances to 4.3.1.

## Dated owner example

The contract records the owner's 2026-10-01 example: `Astra` for planning and
`GPT-6 Sol` or `GPT-6.1 Sol` for execution when result quality is the priority.
The labels are explicitly dated evidence, not permanent portable defaults.

## Preserved

- Provider labels and capabilities remain volatile and must be verified before
  current recommendations.
- Cost still matters after a model meets the task's capability floor.
- The owner remains the source of goals, product semantics, material trade-offs
  and final acceptance.
- The kit does not claim autonomous intelligence or guaranteed correctness.
- Project-specific content remains outside the generic package.

## Verification

- Portable adoption/update tests.
- Package manifest generation/check.
- Contract-validator unit tests.
- YAML/JSON parse validation.
- Active eval manifest/category validation.
- SHA-256 manifest regeneration and verification.
- `git diff --check`.
