# Documentation Governance Pilot Report

Status: passed (2026-08-07)

## Existing project pilot

Fixture: `fixtures/existing_project/`, copied to an isolated temporary directory
by `tests/test_documentation_governance.py`.
The existing project fixture represents a project with current, historical,
secondary-navigation, and ephemeral-work sources.

Commands run:

```powershell
& 'C:\Users\Администратор\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'Agent Kit/kit/tests/test_documentation_governance.py'
& 'C:\Users\Администратор\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'Agent Kit/kit/optional_integrations/documentation_governance/tools/documentation_governance.py' self-test
```

Results: passed. The actual CLI reported stale generated blocks without writing
on `check`; `fix` updated only four marked blocks and a second `fix` updated
zero. The generated index, phase, and freshness projections contained the two
current primary files and excluded the archived specification, historical ADR,
and Project Map note. The Work Board removed the copied `.work` status and
kept only its route back to `TASKS.md`. Text before and after every marker was
unchanged. A `{{ owner }}` placeholder made `check` fail.

## Empty project pilot

Fixture: `fixtures/empty_project/`, with its fixture marker removed before the
CLI is run.
The empty project fixture has no adopted documentation-governance files before
`init`.

Command exercised by the same dependency-free test:

```powershell
python documentation_governance.py --root <temporary-empty-project> init
python documentation_governance.py --root <temporary-empty-project> check
```

Results: passed. `init` created the configuration once and refused a second
attempt without changing its bytes. `check` reported missing optional generated
projections and left the empty project byte-for-byte unchanged.

## Compatibility checks

Commands run:

```powershell
& 'C:\Users\Администратор\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'Agent Kit/kit/tools/context_contract_v1_oracle.py'
& 'C:\Users\Администратор\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'Agent Kit/kit/tools/project_artifact_contract_v2_oracle.py'
```

Results: passed. No legacy Kit contract was weakened.

## False positives

Known false positives are intentionally narrow:

- Standard inline HTML such as `<br>` and `<details>` is not treated as a
  placeholder; the CLI self-test covers this.
- Deliberately unusual angle-bracket prose can still be reported as a
  placeholder. Use normal prose, inline code, or a project-specific exemption
  when that syntax is intentional.

## Remaining limitations

These limitations are retained to keep the integration safe and bounded:

- The CLI enforces source-zone boundaries for its generated projections; it
  cannot prove that arbitrary prose claims match code, tests, or owner
  instructions. Conflicts still require review against those operational
  sources.
- `fix` only repairs pre-existing, unambiguous marker pairs. It intentionally
  does not create missing projection files or infer ownership for unmarked
  content.
- The checker is dependency-free and local only; it does not perform remote
  link validation or YAML frontmatter parsing.
