# Windows Encoding and Shell Hygiene

Status: portable mutation-safety guide
Purpose: avoid predictable Windows quoting, encoding, and shell write failures.

---

## Core Rule

For repository edits, use patch/editor tooling. Do not write files with shell
redirection or ad hoc shell text transforms.

For non-ASCII text, UI-visible text, generated documentation, or remote text
mutation, use byte-safe tooling and readback verification.

## Avoid For File Writes

- PowerShell `Set-Content`, `Add-Content`, `Out-File`, and `>` redirection.
- One-line here-strings.
- Piping raw non-ASCII JSON or localized text through shell commands.
- Mixed Bash syntax sent directly to PowerShell.
- Inline scripts that guess encoding.

## Safer Patterns

- Use `apply_patch`, the IDE editor, or a repository-native patch tool for
  source-controlled files.
- Use explicit encoding when a script must transform text.
- Read the file back after a non-ASCII or UI-visible mutation.
- Assert that intended text exists.
- Assert that replacement markers such as `????` and `U+FFFD` are absent.
- Treat shell parser failures as command harness errors, not project test
  failures.

## Windows Read/Check Examples

```powershell
rg -n "pattern" -- "Project Map" "Agent Kit"
Get-Content -LiteralPath "path with spaces" -TotalCount 80
Get-ChildItem -LiteralPath "path with spaces" -Recurse -File
```

Use Python `pathlib`, `json`, and timezone-aware datetimes for path, JSON, CSV,
and UTC validation when shell quoting would be fragile.

## Remote or Rendered Text

If a task changes remote, hosted, or rendered UI text, the executor must record
how it verified the rendered text. If the visible surface is not directly
accessible, record the caveat and require owner/browser smoke before acceptance.
