# Production code quality pack

This optional pack prevents an agent from silently inventing product behavior,
using tests as a specification, or declaring completion from a green suite alone.
It is portable and contains no adopting-project product logic.

## Offer this pack when

Offer it to the project owner when the project contains production code, business
logic, database contracts, caches, scheduled jobs, integrations, clients, runtime
components, or user-visible behavior that agents may modify.

Do not enable it merely for prose-only repositories unless the owner wants the
communication standard independently.

## Files

- `PRODUCT_CODE_CHANGE_POLICY.template.yaml` — canonical semantic and verification policy.
- `CODE_CHANGE_CONTRACT.template.yaml` — one compact task-local record.
- `skills/production-engineering-standard/` — canonical engineering skill.
- `skills/complete-technical-communication/` — canonical communication skill.
- `cursor/skills/...` — Cursor-ready mirrors.
- `tools/validate_code_change_contract.py` — reusable pre-edit/final validator.
- `PRODUCT_CODE_QUALITY_HOOK_GUIDE.md` — optional hook integration.

## Adoption

1. Copy both canonical skill directories into `<project>/skills/`.
2. Copy the Cursor mirrors into `<project>/.cursor/skills/` when Cursor is used.
3. Copy and specialize `PRODUCT_CODE_CHANGE_POLICY.template.yaml` into the
   project's policy location. Replace generic component classes with real roots.
4. Use one task-local `CODE_CHANGE_CONTRACT.yaml`, created from the template, for
   each product-code task.
5. Add the activation block from `AGENTS.md_TEMPLATE.md` to the nearest project
   instruction file.
6. Optionally wire the validator into pre-edit and final hooks after defining the
   project's production roots and contract discovery rule.
7. Add project-specific component instructions only for actual local hazards;
   do not duplicate the full policy in every component.

## Semantic boundary

Missing owner instruction means preserve current behavior. A causally required
new file is allowed; a new product rule is not. Ask the owner only when an
unresolved assumption can change observable behavior, data meaning, ownership,
failure behavior, timing, persistence, compatibility, public contracts, or a
material correctness/performance tradeoff.

## Evidence boundary

Tests, docs, comments, plans, previous agent reports and model inference are
evidence. They do not create product semantics. Every changed production symbol
must trace to an owner acceptance criterion or a preserved invariant.

## What this pack does not authorize

The pack defines quality controls. It does not authorize file writes, Git,
deployment, database changes, external actions, or new product behavior. Those
remain governed by the current owner request and the adopting project's policy.
