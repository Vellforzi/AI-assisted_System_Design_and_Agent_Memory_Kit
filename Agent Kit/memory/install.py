#!/usr/bin/env python3
"""Preview/apply only the optional memory module; never replace project memory."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from engine import MemoryError, atomic_write, digest, encoded, file_lock, load_json, read_bytes, safe_path

PACKAGE_FILES = {"engine.py", "cli.py", "install.py", "test_memory.py", "README.md", "SKILL.md", "config.example.json", "record.example.json", "manifest.json", "EVALUATION.md"}


def install(source: Path, project: Path, write: bool = False) -> dict[str, object]:
    """Preserve local overrides and carry the source publication status into the receipt."""
    source = source.resolve(strict=True); project = project.resolve(strict=True)
    manifest = load_json(source / "manifest.json")
    if manifest.get("package_id") != "agent-authored-memory" or manifest.get("schema_version") != 1:
        raise MemoryError("invalid_manifest", "Not a supported memory module")
    entries = manifest.get("files", {})
    if set(entries) != PACKAGE_FILES - {"manifest.json"}:
        raise MemoryError("invalid_manifest", "Manifest paths differ from the supported optional module")
    payloads = {name: read_bytes(safe_path(source, name)) for name in PACKAGE_FILES}
    for name, expected in entries.items():
        if digest(payloads[name]) != expected:
            raise MemoryError("integrity_mismatch", "Module source differs from its manifest: " + name)
    receipt_path = safe_path(project, "Agent Kit/MEMORY_INSTALLATION.json")
    previous = load_json(receipt_path) if receipt_path.exists() else {}
    if previous and previous.get("package_id") != manifest["package_id"]:
        raise MemoryError("installation_identity", "Existing installation belongs to another package")
    rows = []; operations = []
    for name in sorted(payloads):
        relative = "Agent Kit/memory/" + name
        target = safe_path(project, relative)
        before = read_bytes(target) if target.exists() else None
        expected = digest(before) if before is not None else None
        old = previous.get("files", {}).get(relative)
        if before == payloads[name]:
            state = "unchanged"
        elif before is None and old:
            state = "preserved_local_removal"
        elif before is None:
            state = "install"
        elif old and expected == old:
            state = "update"
        else:
            state = "preserved_local"
        rows.append({"path": relative, "state": state})
        if state in {"install", "update"}:
            operations.append((target, payloads[name], expected))
    blocked = any(r["state"].startswith("preserved_local") for r in rows)
    receipt = {"schema_version": 1, "package_id": manifest["package_id"], "module_version": manifest["version"],
               "manifest_sha256": digest(payloads["manifest.json"]),
               "release_status": manifest.get("release_status", "local_unpublished"),
               "files": {"Agent Kit/memory/" + name: digest(data) for name, data in payloads.items()}}
    if "publication" in manifest:
        receipt["publication"] = manifest["publication"]
    before_receipt = digest(read_bytes(receipt_path)) if receipt_path.exists() else None
    if write and not blocked:
        with file_lock(safe_path(project, ".generated/agent-memory-install/write.lock")):
            for target, _, expected in operations:
                if (digest(read_bytes(target)) if target.exists() else None) != expected:
                    raise MemoryError("cas_conflict", "Installation target changed after preview")
            for target, data, expected in operations:
                atomic_write(target, data, expected)
            if not receipt_path.exists() or load_json(receipt_path) != receipt:
                atomic_write(receipt_path, encoded(receipt), before_receipt)
    return {"ok": not blocked, "applied": write and not blocked, "blocked_by_local_override": blocked,
            "rows": rows, "core_installation_changed": False, "project_memory_changed": False}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", required=True); p.add_argument("--write", action="store_true")
    args = p.parse_args()
    try:
        result = install(Path(__file__).parent, Path(args.project), args.write)
        print(json.dumps(result)); return 0 if result["ok"] else 2
    except (MemoryError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": getattr(exc, "code", type(exc).__name__), "message": str(exc) if isinstance(exc, MemoryError) else "Installation input unreadable"})); return 2


if __name__ == "__main__":
    raise SystemExit(main())
