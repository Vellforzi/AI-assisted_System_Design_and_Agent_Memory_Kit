"""Git-backed content views for worktree, index, HEAD and merge-base checks."""

from __future__ import annotations

import subprocess
import json
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath


class GitSnapshotError(RuntimeError):
    pass


@dataclass(frozen=True)
class Snapshot:
    label: str
    files: dict[str, str]
    paths: frozenset[str]
    revision: str | None
    baseline_paths: frozenset[str] | None = None


def _git(root: Path, args: tuple[str, ...], *, binary: bool = False) -> bytes | str:
    completed = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args], cwd=root,
        capture_output=True, check=False,
    )
    if completed.returncode:
        raise GitSnapshotError(completed.stderr.decode("utf-8", errors="replace").strip() or "git command failed")
    return completed.stdout if binary else completed.stdout.decode("utf-8", errors="replace")


def _decode(blob: bytes) -> str:
    return blob.decode("utf-8", errors="replace")


def _content_paths(paths: set[str], policy_path: str, policy_raw: str) -> set[str]:
    """Select document bodies while retaining all paths separately for existence checks."""
    selected = {policy_path}
    try:
        policy = json.loads(policy_raw)
    except json.JSONDecodeError:
        policy = {}
    roots = tuple(str(item).replace("\\", "/").strip("/") + "/" for item in policy.get("document_roots", []) if isinstance(item, str))
    root_documents = {str(item).replace("\\", "/") for item in policy.get("root_documents", []) if isinstance(item, str)}
    entrypoints = {str(item).replace("\\", "/") for item in policy.get("entrypoints", []) if isinstance(item, str)}
    suffixes = {str(item).lower() for item in policy.get("document_suffixes", [".md", ".json", ".yaml", ".yml"]) if isinstance(item, str)}
    configured = {
        str(policy.get("lifecycle_registry", "")).replace("\\", "/"),
        str(policy.get("exceptions_registry", "")).replace("\\", "/"),
    }
    selected.update(root_documents)
    selected.update(entrypoints)
    selected.update(configured)
    selected.update(path for path in paths if any(path.startswith(root) for root in roots) and PurePosixPath(path).suffix.lower() in suffixes)
    # Local Markdown anchors can target a document outside a managed root.
    selected.update(path for path in paths if path.lower().endswith(".md"))
    return selected.intersection(paths)


def _configured_baseline_paths(root: Path, registry_raw: str) -> frozenset[str] | None:
    """Resolve the frozen registry baseline without mixing its bodies into the candidate view."""
    try:
        registry = json.loads(registry_raw)
        revision = registry.get("baseline", {}).get("revision")
    except (json.JSONDecodeError, AttributeError):
        return None
    if not isinstance(revision, str) or not revision:
        return None
    raw = _git(root, ("ls-tree", "-rz", "--name-only", revision), binary=True)
    assert isinstance(raw, bytes)
    return frozenset(
        item.decode("utf-8", errors="replace").replace("\\", "/")
        for item in raw.split(b"\0") if item
    )


def _baseline_from_files(root: Path, policy_raw: str, files: dict[str, str]) -> frozenset[str] | None:
    try:
        registry_path = str(json.loads(policy_raw).get("lifecycle_registry", "")).replace("\\", "/")
    except (json.JSONDecodeError, AttributeError):
        return None
    registry_raw = files.get(registry_path)
    return _configured_baseline_paths(root, registry_raw) if registry_raw is not None else None


def _batch_blobs(root: Path, objects: list[tuple[str, str]]) -> dict[str, str]:
    if not objects:
        return {}
    completed = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=root,
        input="".join(f"{oid}\n" for oid, _ in objects).encode("ascii"),
        capture_output=True, check=False,
    )
    if completed.returncode:
        raise GitSnapshotError(completed.stderr.decode("utf-8", errors="replace").strip() or "git cat-file failed")
    output = memoryview(completed.stdout)
    offset = 0
    result: dict[str, str] = {}
    for _, path in objects:
        newline = completed.stdout.find(b"\n", offset)
        if newline < 0:
            raise GitSnapshotError(f"cannot read Git blob header for {path}")
        header = output[offset:newline].tobytes().decode("ascii", errors="replace").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise GitSnapshotError(f"cannot read Git blob for {path}")
        size = int(header[2])
        start = newline + 1
        end = start + size
        if end >= len(output) or output[end] != 10:
            raise GitSnapshotError(f"truncated Git blob for {path}")
        result[path] = _decode(output[start:end].tobytes())
        offset = end + 1
    return result


def revision_snapshot(root: Path, revision: str, policy_path: str = "docs/documentation_governance_policy.json") -> Snapshot:
    resolved = str(_git(root, ("rev-parse", "--verify", revision))).strip()
    raw = _git(root, ("ls-tree", "-rz", "--full-tree", resolved), binary=True)
    assert isinstance(raw, bytes)
    object_by_path: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        if kind == "blob":
            object_by_path[path.decode("utf-8", errors="replace").replace("\\", "/")] = oid
    if policy_path not in object_by_path:
        return Snapshot(f"revision:{resolved}", {}, frozenset(object_by_path), resolved)
    policy_raw = _batch_blobs(root, [(object_by_path[policy_path], policy_path)])[policy_path]
    selected = _content_paths(set(object_by_path), policy_path, policy_raw)
    objects = [(object_by_path[path], path) for path in sorted(selected)]
    files = _batch_blobs(root, objects)
    return Snapshot(f"revision:{resolved}", files, frozenset(object_by_path), resolved,
                    _baseline_from_files(root, policy_raw, files))


def staged_snapshot(root: Path, policy_path: str = "docs/documentation_governance_policy.json") -> Snapshot:
    raw = _git(root, ("ls-files", "--stage", "-z"), binary=True)
    assert isinstance(raw, bytes)
    object_by_path: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        _, oid, stage = metadata.decode("ascii").split()
        if stage == "0" and set(oid) != {"0"}:
            object_by_path[path.decode("utf-8", errors="replace").replace("\\", "/")] = oid
    if policy_path not in object_by_path:
        return Snapshot("staged-index", {}, frozenset(object_by_path), None)
    policy_raw = _batch_blobs(root, [(object_by_path[policy_path], policy_path)])[policy_path]
    selected = _content_paths(set(object_by_path), policy_path, policy_raw)
    objects = [(object_by_path[path], path) for path in sorted(selected)]
    files = _batch_blobs(root, objects)
    return Snapshot("staged-index", files, frozenset(object_by_path), None,
                    _baseline_from_files(root, policy_raw, files))


def worktree_snapshot(root: Path, policy_path: str = "docs/documentation_governance_policy.json") -> Snapshot:
    raw = _git(root, ("ls-files", "-z", "--cached", "--others", "--exclude-standard"), binary=True)
    assert isinstance(raw, bytes)
    candidates = {
        item.decode("utf-8", errors="replace").replace("\\", "/")
        for item in raw.split(b"\0") if item
    }
    paths = {
        path for path in candidates
        if (root / Path(path)).is_file() or (root / Path(path)).is_symlink()
    }
    policy_file = root / Path(policy_path)
    policy_raw = policy_file.read_text(encoding="utf-8", errors="replace") if policy_file.is_file() else "{}"
    selected = _content_paths(paths, policy_path, policy_raw)
    files: dict[str, str] = {}
    for path in sorted(selected):
        absolute = root / Path(path)
        if absolute.is_file():
            if absolute.is_symlink():
                files[path] = str(absolute.readlink())
            else:
                files[path] = absolute.read_text(encoding="utf-8", errors="replace")
    return Snapshot("explicit-worktree", files, frozenset(paths), None,
                    _baseline_from_files(root, policy_raw, files))


def merge_base(root: Path, base: str) -> str:
    return str(_git(root, ("merge-base", "--end-of-options", base, "HEAD"))).strip()


def candidate_snapshot(root: Path, mode: str, base: str | None = None, policy_path: str = "docs/documentation_governance_policy.json") -> Snapshot:
    if mode == "staged":
        return staged_snapshot(root, policy_path)
    if mode == "worktree":
        return worktree_snapshot(root, policy_path)
    if mode == "changed":
        return revision_snapshot(root, "HEAD", policy_path)
    if mode == "full":
        return revision_snapshot(root, "HEAD", policy_path)
    raise GitSnapshotError(f"unsupported snapshot mode: {mode}")


def baseline_snapshot(root: Path, mode: str, base: str | None = None, policy_path: str = "docs/documentation_governance_policy.json") -> Snapshot:
    if mode in {"staged", "worktree"}:
        return revision_snapshot(root, "HEAD", policy_path)
    if mode == "changed":
        if not base:
            raise GitSnapshotError("changed mode requires a base reference")
        return revision_snapshot(root, merge_base(root, base), policy_path)
    raise GitSnapshotError(f"delta is unsupported for mode: {mode}")
