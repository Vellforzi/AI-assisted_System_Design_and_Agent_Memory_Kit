#!/usr/bin/env python3
"""Audit Codex AGENTS.md discovery, precedence, bytes and truncation."""

from __future__ import annotations

import argparse
import json
import os
import tomllib
from pathlib import Path
from typing import Any


DEFAULT_LIMIT = 32 * 1024
DEFAULT_FALLBACKS: list[str] = []


def first_nonempty(directory: Path, names: list[str]) -> Path | None:
    for name in names:
        candidate = directory / name
        if candidate.is_file() and candidate.stat().st_size > 0:
            return candidate
    return None


def config(codex_home: Path) -> tuple[int, list[str], str]:
    path = codex_home / "config.toml"
    if not path.exists():
        return DEFAULT_LIMIT, DEFAULT_FALLBACKS, "default_no_config"
    value = tomllib.loads(path.read_text(encoding="utf-8"))
    limit = int(value.get("project_doc_max_bytes", DEFAULT_LIMIT))
    fallbacks = [str(item) for item in value.get("project_doc_fallback_filenames", DEFAULT_FALLBACKS)]
    source = "configured" if "project_doc_max_bytes" in value else "default_32_kib"
    return limit, fallbacks, source


def ancestors(root: Path, cwd: Path) -> list[Path]:
    cwd.relative_to(root)
    result = [root]
    current = root
    for part in cwd.relative_to(root).parts:
        current = current / part
        result.append(current)
    return result


def item(path: Path, precedence: int, layer: str) -> dict[str, Any]:
    return {"path": path.as_posix(), "precedence": precedence, "layer": layer, "bytes": path.stat().st_size}


def audit(repo_root: Path, cwd: Path, codex_home: Path) -> dict[str, Any]:
    limit, fallbacks, limit_source = config(codex_home)
    files: list[dict[str, Any]] = []
    global_file = first_nonempty(codex_home, ["AGENTS.override.md", "AGENTS.md"])
    if global_file:
        files.append(item(global_file, 0, "global"))
    names = ["AGENTS.override.md", "AGENTS.md", *fallbacks]
    for directory in ancestors(repo_root, cwd):
        selected = first_nonempty(directory, names)
        if selected:
            files.append(item(selected, len(files), "project"))

    project_bytes = sum(entry["bytes"] for entry in files if entry["layer"] == "project")
    global_bytes = sum(entry["bytes"] for entry in files if entry["layer"] == "global")
    separator_bytes = max(0, len(files) - 1) * 2
    merged_bytes = project_bytes + global_bytes + separator_bytes
    return {
        "schema_version": "1.0",
        "repo_root": repo_root.as_posix(),
        "cwd": cwd.as_posix(),
        "codex_home": codex_home.as_posix(),
        "configured_limit_bytes": limit,
        "limit_source": limit_source,
        "fallback_filenames": fallbacks,
        "loaded_files": files,
        "project_instruction_bytes": project_bytes,
        "global_instruction_bytes": global_bytes,
        "merged_chain_bytes": merged_bytes,
        "project_safety_margin_bytes": limit - project_bytes,
        "project_truncated": project_bytes > limit,
        "merged_chain_exceeds_project_limit": merged_bytes > limit,
        "follow_up_documents": [
            "Project Map/README.md",
            "Project Map/current_state.md",
            "Project Map/working_state.yaml",
            "Project Map/source_authority.yaml",
            "Project Map/permissions_policy.yaml",
            "Project Map/retrieval_policy.yaml",
            "Agent Kit/kit/VERIFIED_DELIVERY_PIPELINE.md"
        ],
        "official_discovery_reference": "https://learn.chatgpt.com/docs/agent-configuration/agents-md.md"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--cwd")
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME") or str(Path.home() / ".codex"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve(strict=True)
    cwd = Path(args.cwd).resolve(strict=True) if args.cwd else root
    result = audit(root, cwd, Path(args.codex_home).resolve(strict=True))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.json else None, sort_keys=True))
    return 0 if not result["project_truncated"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

