# CI templates

Before using either template, merge
`justfile.documentation-governance.template` into the adopting repository's
`justfile`. Both providers install the optional pinned site dependencies and
invoke only `just ci`; validation logic remains in the shared local command
surface. The Git checkout is deliberately complete so Git-derived page
modification dates are available to MkDocs.

Do not add deployment or publication steps until the adopter has reviewed the
MkDocs exclusion policy for `.work`, receipts, secrets, and temporary files.
