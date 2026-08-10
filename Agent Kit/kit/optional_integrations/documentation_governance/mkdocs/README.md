# Optional strict MkDocs profile (Reference Lab)

This MkDocs variant is a Reference Lab example outside the normal installation
path. It is not required to adopt the compact policy layer.

Copy this directory's `mkdocs.strict.yml`, `overrides/`, and
`docs/javascripts/` into the adopting repository. Install the exact optional
site dependencies from `requirements-site.txt`, then build with:

```text
mkdocs build --strict --config-file mkdocs.strict.yml
```

The profile rejects MkDocs warnings, enables Mermaid fenced blocks, and shows
frontmatter `last_verified` beside the Git-derived last-modified date when the
Git revision plugin can resolve it. Use a full Git checkout in CI so the date
is available.

`docs_dir` intentionally limits publication to `docs/`; the exclusion rules
also reject `.work`, receipts, secrets, and common temporary artifacts should
they appear below that directory. Keep credentials and task artifacts outside
published documentation regardless of these safeguards.
