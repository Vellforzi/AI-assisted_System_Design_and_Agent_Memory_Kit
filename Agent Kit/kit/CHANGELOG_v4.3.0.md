# Agent Memory Kit v4.3.0 Changelog

Release source date: 2026-10-01.
Previous published release: `v4.2.0`.

v4.3.0 adds a portable production-quality layer derived from real code-change and
technical-communication failures, without binding the package to one product.

## Added

- Generic `PRODUCT_CODE_CHANGE_POLICY.template.yaml`.
- Generic task-local `CODE_CHANGE_CONTRACT.template.yaml`.
- Canonical `$production-engineering-standard` skill and engineering review
  checklist.
- Canonical `$complete-technical-communication` skill, owner-style starter
  profile and communication anti-patterns.
- Cursor-ready mirrors of both skills.
- `PRODUCTION_CODE_CHANGE_GUIDE.md` with an explicit owner opt-in adoption flow.
- `PRODUCT_CODE_QUALITY_HOOK_GUIDE.md` for pre-edit and final gates.
- Reusable `validate_code_change_contract.py` plus deterministic unit tests.
- Active semantic-authority and complete-communication eval cases.

## Changed

- `AGENTS.md_TEMPLATE.md` now includes portable product-semantic authority,
  missing-instruction preservation, test-evidence and mandatory-skill activation
  rules for projects that adopt the pack.
- New/existing project adoption guides explicitly offer the pack rather than
  enabling hooks silently.
- README, manifest, Cursor guidance and owner questions describe the new pack.
- Current package/eval metadata advances to 4.3.0.

## Preserved

- The portable core remains small and model/tool/folder-layout independent.
- Owner authorization and tool availability remain separate facts.
- Skills and validators define quality; they do not authorize mutations, Git,
  deployment, database writes or external actions.
- Project-specific product logic stays in the adopting project, not this package.
- Tests remain evidence and never become product semantics.

## Verification

- Portable adoption/update tests.
- Package manifest generation/check.
- Contract-validator unit tests.
- YAML/JSON parse validation.
- Canonical/Cursor skill mirror byte parity.
- SHA-256 manifest regeneration and verification.
- `git diff --check`.
