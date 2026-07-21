"""Deterministic AST architecture lint driven by repository-owned JSON rules."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Sequence


DEFAULT_CONFIG_PATH = Path("docs/architecture/architecture_lint_rules.json")


@dataclass(frozen=True)
class ImportEdge:
    source_path: str
    source_module: str
    target_module: str
    line: int


def build_report(
    root: Path | str = Path.cwd(),
    *,
    config_path: Path | str | None = None,
) -> dict[str, object]:
    root_path = Path(root).resolve()
    config = _load_config(root_path, config_path)
    findings: list[dict[str, object]] = []
    scanned = 0
    for path in _python_files(root_path, config):
        scanned += 1
        relative = path.relative_to(root_path).as_posix()
        module = _module_for_path(relative)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(text, filename=relative)
        except SyntaxError as exc:
            findings.append({
                "rule_id": "ARCH-SYNTAX",
                "severity": "error",
                "path": relative,
                "line": exc.lineno or 1,
                "message": exc.msg,
            })
            continue
        edges = _import_edges(tree, relative, module)
        for edge in edges:
            findings.extend(_edge_findings(edge, config))
        findings.extend(_path_reference_findings(relative, module, text, config))
    findings.sort(key=lambda item: (str(item["path"]), int(item["line"]), str(item["rule_id"])))
    failed = any(item["severity"] == "error" for item in findings)
    return {
        "report_type": "architecture_lint",
        "status": "failed" if failed else ("warning" if findings else "passed"),
        "read_only": True,
        "files_scanned": scanned,
        "finding_count": len(findings),
        "findings": findings,
    }


def _load_config(root: Path, config_path: Path | str | None) -> dict[str, object]:
    raw = Path(config_path) if config_path is not None else DEFAULT_CONFIG_PATH
    path = raw if raw.is_absolute() else root / raw
    if not path.is_file():
        return {"scan_roots": ["src", "scripts"], "layers": {}, "forbidden_imports": [], "forbidden_path_references": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    for key in ("scan_roots", "layers", "forbidden_imports", "forbidden_path_references"):
        if key not in payload:
            raise ValueError(f"architecture lint config missing {key}")
    return payload


def _python_files(root: Path, config: dict[str, object]) -> list[Path]:
    paths: list[Path] = []
    for scan_root in config.get("scan_roots", []):
        base = root / str(scan_root)
        if base.is_dir():
            paths.extend(path for path in base.rglob("*.py") if "__pycache__" not in path.parts)
    return sorted(set(paths))


def _import_edges(tree: ast.AST, path: str, source_module: str) -> list[ImportEdge]:
    edges: list[ImportEdge] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            edges.extend(ImportEdge(path, source_module, alias.name, node.lineno) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            target = node.module or ""
            if node.level:
                package = source_module.split(".")[:-1]
                keep = max(0, len(package) - node.level + 1)
                target = ".".join([*package[:keep], target]).strip(".")
            edges.append(ImportEdge(path, source_module, target, node.lineno))
    unique = {(edge.source_path, edge.target_module, edge.line): edge for edge in edges}
    return list(unique.values())


def _edge_findings(edge: ImportEdge, config: dict[str, object]) -> list[dict[str, object]]:
    source_layer = _layer_for_module(edge.source_module, config)
    target_layer = _layer_for_module(edge.target_module, config)
    findings: list[dict[str, object]] = []
    for raw in config.get("forbidden_imports", []):
        if not isinstance(raw, dict):
            continue
        if raw.get("from_layer") == source_layer and raw.get("to_layer") == target_layer:
            findings.append({
                "rule_id": str(raw.get("rule_id", "ARCH-IMPORT")),
                "severity": str(raw.get("severity", "error")),
                "path": edge.source_path,
                "line": edge.line,
                "message": f"{source_layer} must not import {target_layer}: {edge.target_module}",
                "source_layer": source_layer,
                "target_layer": target_layer,
            })
    return findings


def _path_reference_findings(
    path: str,
    module: str,
    text: str,
    config: dict[str, object],
) -> list[dict[str, object]]:
    source_layer = _layer_for_module(module, config)
    findings: list[dict[str, object]] = []
    for raw in config.get("forbidden_path_references", []):
        if not isinstance(raw, dict) or raw.get("from_layer") != source_layer:
            continue
        pattern = str(raw.get("path_pattern", ""))
        for line_number, line in enumerate(text.splitlines(), start=1):
            if pattern and re.search(pattern, line.replace("\\", "/")):
                findings.append({
                    "rule_id": str(raw.get("rule_id", "ARCH-PATH")),
                    "severity": str(raw.get("severity", "error")),
                    "path": path,
                    "line": line_number,
                    "message": f"{source_layer} references a forbidden path pattern: {pattern}",
                    "source_layer": source_layer,
                })
    return findings


def _layer_for_module(module: str, config: dict[str, object]) -> str:
    layers = config.get("layers", {})
    if not isinstance(layers, dict):
        return "unclassified"
    matches: list[tuple[int, str]] = []
    for layer, prefixes in layers.items():
        if not isinstance(prefixes, list):
            continue
        for prefix in prefixes:
            normalized = str(prefix)
            if module == normalized or module.startswith(normalized + "."):
                matches.append((len(normalized), str(layer)))
    return max(matches)[1] if matches else "unclassified"


def _module_for_path(path: str) -> str:
    normalized = path.removesuffix(".py").replace("/", ".")
    return normalized.removesuffix(".__init__")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args(argv)
    report = build_report(args.root, config_path=args.config)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"architecture lint: {report['status']} ({report['finding_count']} findings)")
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
