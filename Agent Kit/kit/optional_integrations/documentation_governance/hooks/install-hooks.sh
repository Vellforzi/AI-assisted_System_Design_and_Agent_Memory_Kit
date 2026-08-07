#!/bin/sh
set -eu

root=${1:-.}
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
hooks_dir=$(git -C "$root" rev-parse --git-path hooks)
case "$hooks_dir" in
  /*) ;;
  *) hooks_dir="$root/$hooks_dir" ;;
esac
mkdir -p "$hooks_dir"
for hook in pre-commit pre-push; do
  cp "$source_dir/$hook" "$hooks_dir/$hook"
  chmod +x "$hooks_dir/$hook"
done
printf '%s\n' "Installed documentation-governance hooks for Unix and Windows-compatible Git at $hooks_dir"
