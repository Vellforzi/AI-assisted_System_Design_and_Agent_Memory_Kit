# Simplification Pilot Acceptance Report

Status: passed local recovery verification

## Scope

This report covers the dependency-free acceptance test for the Core, Standard,
Workflow, and Reference Lab adoption profiles. The test invokes the existing
documentation harness; it does not reimplement Markdown link, URI, or anchor
handling.

## Acceptance coverage

- Core uses two ordinary project files in the isolated fixture, below the
  six-file maximum. The fixture has no Project Map, Python, `.work`, eval,
  generated-content, hook, CI, or MkDocs dependency.
- Core invokes the harness through its CLI with valid local links and anchors,
  plus `HTTPS:`, `ftp:`, `vscode:`, and `mailto:` URI targets. URI targets are
  non-local and are not dereferenced; local targets and anchors are checked.
- Standard checks are selected only through an explicit `standard` profile.
- Workflow checks are selected only through an explicit `workflow` profile;
  the profile contract requires an observable activation trigger before
  workflow artifacts are adopted.
- Reference Lab material is omitted from the fixture. Re-running the default
  Core harness report produces the same result, so its omission does not
  change Core behavior.

## Commands and results

The following commands were run with the executor's locally resolved
`PYTHON_BIN`. That machine-local fallback is not recorded in project files.

```powershell
& $env:PYTHON_BIN 'Agent Kit/kit/tests/test_adoption_profiles.py'
& $env:PYTHON_BIN 'Agent Kit/kit/tests/test_documentation_governance.py'
& $env:PYTHON_BIN 'Agent Kit/kit/tools/context_contract_v1_oracle.py'
& $env:PYTHON_BIN 'Agent Kit/kit/tools/project_artifact_contract_v2_oracle.py'
& $env:PYTHON_BIN 'Agent Kit/kit/tools/architecture_lint.py'
& $env:PYTHON_BIN 'Agent Kit/kit/tools/generate_checksums.py' --write
& $env:PYTHON_BIN 'Agent Kit/kit/tools/generate_checksums.py' --verify
rg -n "ADOPTION_PROFILES.md|Core|Standard|Workflow|Reference Lab|passed|compatib|limitation|report-only|full change" "Agent Kit/kit/optional_integrations/README.md" "Agent Kit/kit/optional_integrations/documentation_governance/SIMPLIFICATION_PILOT_REPORT.md" "Agent Kit/kit/MANIFEST.md"
git diff --check; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; $untracked = @(git ls-files --others --exclude-standard); foreach ($file in $untracked) { $result = git -c core.safecrlf=false -c core.autocrlf=false diff --no-index --check -- NUL $file 2>&1; if ($result) { $result | ForEach-Object { Write-Output $_ }; exit 1 } }; exit 0
```

Observed results:

- `test_adoption_profiles.py`: passed (`Ran 2 tests`, `OK`).
- `test_documentation_governance.py`: passed (`Ran 8 tests`, `OK`).
- Context Contract V1 oracle: passed (5 cases).
- Project Artifact Contract V2 oracle: `AMK-PROJECT-ARTIFACT-V2: passed`,
  including all schema and activation checks.
- Architecture lint: passed (0 findings).
- Checksum generator: `checksums: wrote 325 entries`; verification:
  `checksums: passed`.
- Inventory wording scan and full-change tracked-plus-untracked whitespace
  check: passed (exit code 0).

## Limitations

This acceptance coverage does not test remote URI reachability, every
Markdown dialect, or an adopter's separately owned Reference Lab automation.
URI-scheme targets are deliberately treated as non-local by the harness. The
test is report-only acceptance coverage and is not a release claim.

## Compatibility statement

This is an additive acceptance test and report. It exercises the existing
documentation-harness CLI and public report API without changing its schemas,
link policy, optional integration behavior, or legacy Kit oracle interfaces.
Core remains dependency-free; Standard, Workflow, and Reference Lab remain
opt-in according to their existing adoption triggers.
