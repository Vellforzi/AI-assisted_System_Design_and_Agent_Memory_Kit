# Cursor Live Adoption Guide — AMK v3.9.4

This guide covers live adoption of kit-owned Cursor rule and command assets.

## Source paths

- `Agent Kit/kit/cursor_integration/rules/context_advisor_preflight.mdc`
- `Agent Kit/kit/cursor_integration/commands/*`

## Live target paths

- `.cursor/rules/context_advisor_preflight.mdc`
- `.cursor/commands/*`

## Adoption rule

Presence in `Agent Kit/` is not live adoption. Live adoption means the files exist
under `.cursor/` in the repo root and are verified after merge.

## Merge policy

Use semantic merge. Do not overwrite unrelated Cursor settings. If target files
already exist, preserve owner-specific additions unless they conflict with
AMK v3.9.4 safety or authority rules.

## Verification

After merge, run:

```bash
test -f ".cursor/rules/context_advisor_preflight.mdc"
find ".cursor/commands" -maxdepth 1 -type f -print
python "Project Map/eval_suite/run_eval_checklist.py" --root "Project Map/eval_suite" --format markdown
```

## Forbidden

- git push without owner approval;
- DB writes;
- deploy;
- secrets in answers or logs;
- unrelated file changes;
- leaving release ZIP files in the working repo after merge.
