"""Read-only context budget audit using only the Python standard library."""

from __future__ import annotations

import argparse
import fnmatch
import json
import math
from pathlib import Path
import re


DEFAULT_EXCLUDES = (".git/**", ".env", ".env.*", "**/.env", "**/.env.*", "data/**", "output/**", "**/*.db", "**/*.sqlite", "**/*.log")


def _scalar(text: str):
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def load_policy(path: Path) -> dict:
    """Parse the deliberately small policy-template YAML subset."""
    result: dict = {"profiles": {}, "always_sources": [], "excluded": []}
    section = ""
    profile = ""
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        value = line.strip()
        if indent == 0 and value.endswith(":"):
            section = value[:-1]
            profile = ""
            continue
        if indent == 0 and ":" in value:
            key, val = value.split(":", 1)
            result[key] = _scalar(val)
            continue
        if section == "retrieval_profiles" and indent == 2 and value.endswith(":"):
            profile = value[:-1]
            result["profiles"][profile] = {}
            continue
        if section == "retrieval_profiles" and indent == 4 and ":" in value:
            key, val = value.split(":", 1)
            result["profiles"][profile][key] = _scalar(val)
            continue
        if section == "always_loaded" and indent == 2 and ":" in value:
            key, val = value.split(":", 1)
            if val.strip():
                result[f"always_{key}"] = _scalar(val)
            continue
        if section == "always_loaded" and value.startswith("- "):
            result["always_sources"].append(_scalar(value[2:]))
        if section == "excluded_path_globs" and value.startswith("- "):
            result["excluded"].append(_scalar(value[2:]))
    return result


def audit(root: Path, paths: list[str], policy: dict, profile: str, baseline: dict | None) -> dict:
    root = root.resolve()
    excluded = tuple(policy.get("excluded") or DEFAULT_EXCLUDES)
    sources = []
    reasons = []
    for supplied in paths:
        rel = Path(supplied).as_posix()
        if rel.startswith("./"):
            rel = rel[2:]
        if any(fnmatch.fnmatch(rel, pattern) for pattern in excluded):
            reasons.append({"code": "CTX_PATH_EXCLUDED", "path": rel})
            continue
        target = (root / rel).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            reasons.append({"code": "CTX_PATH_OUTSIDE_ROOT", "path": rel})
            continue
        if not target.is_file():
            reasons.append({"code": "CTX_SOURCE_MISSING", "path": rel})
            continue
        size = target.stat().st_size
        sources.append({"path": rel, "bytes": size, "estimated_tokens": math.ceil(size / 4)})
    sources.sort(key=lambda item: (-item["estimated_tokens"], item["path"]))
    total = sum(item["estimated_tokens"] for item in sources)
    limits = policy.get("profiles", {}).get(profile, {})
    max_sources = int(limits.get("max_sources", policy.get("always_max_sources", 0)) or 0)
    profile_max = int(limits.get("max_estimated_tokens", policy.get("always_max_estimated_tokens", 0)) or 0)
    absolute_max = int(policy.get("absolute_max_estimated_tokens", 0) or 0)
    if max_sources and len(sources) > max_sources:
        reasons.append({"code": "CTX_SOURCE_LIMIT_EXCEEDED", "actual": len(sources), "limit": max_sources})
    if profile_max and total > profile_max:
        reasons.append({"code": "CTX_PROFILE_TOKEN_LIMIT_EXCEEDED", "actual": total, "limit": profile_max})
    if absolute_max and total > absolute_max:
        reasons.append({"code": "CTX_ABSOLUTE_TOKEN_LIMIT_EXCEEDED", "actual": total, "limit": absolute_max})
    growth = None
    if baseline is not None:
        old = int(baseline.get("estimated_tokens", 0))
        growth = None if old <= 0 else round((total - old) * 100 / old, 2)
        threshold = int(policy.get("relative_growth_threshold_percent", 0) or 0)
        if growth is not None and growth > threshold:
            reasons.append({"code": "CTX_RELATIVE_GROWTH_EXCEEDED", "actual_percent": growth, "limit_percent": threshold})
    return {"schema_version": "1.0", "profile": profile, "status": "pass" if not reasons else "fail", "estimated_tokens": total, "source_count": len(sources), "relative_growth_percent": growth, "largest_sources": sources[:10], "reasons": reasons, "read_only": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--profile", default="startup")
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--paths-file", type=Path)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    paths = list(args.path)
    if args.paths_file:
        paths.extend(line.strip() for line in args.paths_file.read_text(encoding="utf-8-sig").splitlines() if line.strip())
    baseline = json.loads(args.baseline.read_text(encoding="utf-8")) if args.baseline else None
    payload = audit(args.root, paths, load_policy(args.policy), args.profile, baseline)
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
