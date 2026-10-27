"""Explicit session-to-task selection. Historical task directories are never scanned."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


class TaskBindingError(ValueError):
    pass


def session_identity(payload: dict[str, Any]) -> str | None:
    values = [payload[key] for key in ("session_id", "sessionId", "thread_id", "threadId")
              if key in payload and payload[key] is not None]
    if not values:
        return None
    if any(not isinstance(value, str) or not value.strip() or len(value) > 1024 for value in values):
        raise TaskBindingError("Invalid session identity")
    if len(set(values)) != 1:
        raise TaskBindingError("Conflicting session identities")
    return values[0]


def starting_directory(payload: dict[str, Any]) -> Path:
    for key in ("cwd", "repo_root", "repoRoot", "workspace_root", "workspaceRoot"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return Path(value).resolve()
    return Path.cwd().resolve()


def binding_path(root: Path, session_id: str) -> Path:
    session_identity({"session_id": session_id})
    root = root.resolve()
    filename = hashlib.sha256(session_id.encode("utf-8")).hexdigest() + ".json"
    path = (root / ".codex/runtime/task_bindings" / filename).resolve()
    if not path.is_relative_to(root):
        raise TaskBindingError("Session binding path escapes the repository")
    return path


def selected_capsule(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise TaskBindingError("Binding must contain a repository-relative capsule path")
    capsule = (root / relative).resolve()
    if not capsule.is_relative_to(root) or capsule.name != "RECOVERY_CAPSULE.md":
        raise TaskBindingError("Bound capsule escapes the repository or has the wrong filename")
    if not capsule.is_file():
        raise TaskBindingError(f"Selected recovery capsule is missing: {capsule}")
    return capsule


def read_binding(root: Path, session_id: str) -> Path | None:
    root = root.resolve()
    path = binding_path(root, session_id)
    if not path.exists():
        return None
    if path.stat().st_size > 16_384:
        raise TaskBindingError("Session binding exceeds 16 KiB")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict) or record.get("schema_version") != 1:
        raise TaskBindingError("Invalid session binding schema")
    if record.get("session_id") != session_id or record.get("repository_root") != str(root):
        raise TaskBindingError("Session binding belongs to a different session or repository; rebind explicitly")
    return selected_capsule(root, record.get("capsule_path"))


def find_selected_capsule(payload: dict[str, Any], explicit: Path | None = None) -> Path | None:
    cwd = starting_directory(payload)
    values = [explicit] if explicit is not None else [payload[key] for key in
              ("capsule_path", "capsulePath", "recovery_capsule") if key in payload]
    if values:
        if any(not isinstance(value, (str, Path)) or not str(value).strip() for value in values):
            raise TaskBindingError("Invalid explicit recovery capsule path")
        paths = {(cwd / Path(value)).resolve() for value in values}
        if len(paths) != 1:
            raise TaskBindingError("Conflicting explicit recovery capsule paths")
        capsule = paths.pop()
        if not capsule.is_file():
            raise TaskBindingError(f"Selected recovery capsule is missing: {capsule}")
        return capsule
    session_id = session_identity(payload)
    if session_id is None:
        return None
    for root in (cwd, *cwd.parents):
        capsule = read_binding(root, session_id)
        if capsule is not None:
            return capsule
        # One explicitly bound session may span nested component repositories.
        # Only its exact session record can select a parent workspace task.
    return None


def bind_task(root: Path, capsule: Path, session_id: str, *, replace: bool = False) -> Path:
    root = root.resolve(strict=True)
    capsule = capsule.resolve(strict=True)
    if not capsule.is_relative_to(root):
        raise TaskBindingError("Selected task is outside the repository")
    relative = capsule.relative_to(root).as_posix()
    selected_capsule(root, relative)
    path = binding_path(root, session_id)
    if path.exists() and not replace:
        previous = read_binding(root, session_id)
        if previous != capsule:
            raise TaskBindingError("Session already selects another task; use --replace for an intentional task change")
        return path
    data = (json.dumps({"schema_version": 1, "session_id": session_id,
                       "repository_root": str(root), "capsule_path": relative},
                      ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.stem + ".", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)
    if read_binding(root, session_id) != capsule:
        raise TaskBindingError("Session binding readback failed")
    return path


def unbind_task(root: Path, capsule: Path, session_id: str) -> Path:
    root = root.resolve(strict=True)
    path = binding_path(root, session_id)
    if path.exists():
        if read_binding(root, session_id) != capsule.resolve():
            raise TaskBindingError("Refusing to remove a different task's session binding")
        path.unlink()
    return path
