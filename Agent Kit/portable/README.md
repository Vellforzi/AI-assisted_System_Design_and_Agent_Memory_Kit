# Portable adoption

Candidate version: **4.2.0-dev**, based on published 4.1.0. No release is claimed.

Read [the core workflow](core/WORKFLOW.md), then inspect an adoption plan:

```text
python "Agent Kit/portable/manage.py" --project "path/to/project"
```

Apply that plan by adding `--write`. Run the same command from a newer Kit
checkout to update. Python 3.11+ and its standard library are sufficient; no
package installation, Git command, model call or global setting is involved.

The default installs three small reference files, attribution, a short link in
`AGENTS.md`, and a project-owned `Project Map/README.md` if it is absent. Existing
entry instructions and project context keep their bytes. Installation does not
enable hooks or change a client's trust settings. A client that does not load
AGENTS.md needs an explicit link from its own project entry instructions.

`Agent Kit/INSTALLATION.json` records the exact package manifest hash, upstream
base commit, installed file hashes and local overrides. On update:

- Unmodified Kit-owned files receive the new version.
- Locally changed or colliding files are preserved and reported as overrides.
- Removed upstream files are retained and reported for review.
- Project context, other files and existing AGENTS.md text stay project-owned.
- A default invocation writes nothing. Invalid paths or a changed preimage
  stop the affected operation; no broad deletion or automatic conflict merge occurs.

Review `preserved_local` entries after an update. Compare the reported source
file with the local file and explicitly reconcile useful upstream changes.
If a managed file is deliberately removed, the updater preserves that removal.

Only files in `package.json` are distributed by this installer. The full
repository's optional guides and historical examples are not installed by
default. `AUTHORS.md` and `LICENSE` retain their original authorship and terms.

To vendor this helper, retain the entire `portable/` folder and the declared
attribution files at their package-relative locations. Use `--package` only
with an inspected package manifest. The manifest is integrity metadata, not a
signature or a source of permission.
