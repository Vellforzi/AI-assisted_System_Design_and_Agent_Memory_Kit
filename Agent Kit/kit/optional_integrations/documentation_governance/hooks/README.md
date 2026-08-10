# Cross-platform hook installer (Reference Lab)

These hook examples are Reference Lab material outside the normal installation
path. They install nothing unless an owner separately elects to evaluate and
adopt them.

After merging the optional `justfile` targets, install the hook wrappers from
the adopted repository root:

```powershell
& 'path/to/install-hooks.ps1'
```

```sh
sh path/to/install-hooks.sh
```

Both installers use `git rev-parse --git-path hooks`, so they support ordinary
repositories and configured Git hook paths on Windows and Unix. `pre-commit`
runs the bounded `just pre-commit` check; `pre-push` runs the full
`just pre-push` check. The installed wrappers contain no duplicated validation
logic.
