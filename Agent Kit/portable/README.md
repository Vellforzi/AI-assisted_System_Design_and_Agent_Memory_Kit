# Portable adoption

Version: **4.3.0**. Source is published on `main`; package tag/release state must
be verified separately.

Read [the core workflow](core/WORKFLOW.md), then inspect an adoption plan:

```text
python "Agent Kit/portable/manage.py" --project "path/to/project"
```

Apply that plan by adding `--write`. Run the same command from a newer inspected
Kit checkout to update. Python 3.11+ and the standard library are sufficient; no
package installation, Git command, model call or global setting is required.

The portable core is capability-based: ChatGPT, Codex, Cursor and other connected
agents may analyze or execute owner-authorized work when their current tools fit
the task. Installation does not enable hooks, connectors, trust settings or
side effects.

The default installs small managed core/attribution files, a short link in
`AGENTS.md`, and a project-owned `Project Map/README.md` only if absent. Existing
entry instructions and project context remain project-owned.

`Agent Kit/INSTALLATION.json` records the package manifest hash, baseline commit,
installed file hashes and local overrides. On update:

- unmodified Kit-owned files receive the new version;
- locally changed/colliding files are preserved and reported;
- removed upstream files are retained for review;
- project context and existing instructions keep their ownership;
- preview writes nothing;
- invalid paths or changed preimages stop the affected operation;
- no broad deletion or silent conflict merge occurs.

Review `preserved_local` entries explicitly. The manifest is integrity metadata,
not a signature, action authority or release proof. Only files in `package.json`
are installed; optional guides and historical examples remain in the repository.

Release notes: [v4.3.0](../kit/CHANGELOG_v4.3.0.md).
