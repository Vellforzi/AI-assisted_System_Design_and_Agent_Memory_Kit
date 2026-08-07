#!/usr/bin/env python3
"""Report-first checks and safe generated-document projections for documentation governance.

This utility is intentionally dependency-free.  Adopt it by creating the
configuration with ``init`` and then adding the generated markers to the files
that own generated projections.  ``check`` never writes.  ``fix`` replaces
only text strictly between paired markers that already exist.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

CONFIG_NAME = ".documentation-governance.json"
MARKER_PREFIX = "<!-- documentation-governance:"
# Angle-bracket placeholders are supported by the supplied templates, but an
# angle-bracket match alone is not enough: Markdown may legitimately contain
# inline HTML.  Keep this list deliberately broad for ordinary HTML elements;
# unknown angle-bracket text remains a useful placeholder signal.
PLACEHOLDER = re.compile(r"<[^>\n]+>|\{\{[^}\n]+\}\}")
HTML_TAG = re.compile(
    r"</?(?:a|abbr|address|area|article|aside|audio|b|bdi|bdo|blockquote|body|br|button|"
    r"canvas|caption|cite|code|col|colgroup|data|datalist|dd|del|details|dfn|dialog|div|dl|"
    r"dt|em|embed|fieldset|figcaption|figure|footer|form|h[1-6]|head|header|hgroup|hr|html|i|"
    r"iframe|img|input|ins|kbd|label|legend|li|link|main|map|mark|menu|meta|meter|nav|noscript|"
    r"object|ol|optgroup|option|output|p|picture|pre|progress|q|rp|rt|ruby|s|samp|script|search|"
    r"section|select|slot|small|source|span|strong|style|sub|summary|sup|table|tbody|td|template|"
    r"textarea|tfoot|th|thead|time|title|tr|track|u|ul|var|video|wbr)(?:\s+[^>\n]*)?\s*/?>",
    re.IGNORECASE,
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.M)


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str
    path: str
    message: str

    def as_dict(self):
        return {"check": self.check, "severity": self.severity,
                "path": self.path, "message": self.message}


def posix(path: Path) -> str:
    return path.as_posix()


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("cannot read configuration %s: %s" % (path, error)) from error


def has_unresolved_placeholder(text: str) -> bool:
    """Return true for template placeholders, excluding normal inline HTML."""
    return any(not HTML_TAG.fullmatch(match.group(0)) for match in PLACEHOLDER.finditer(text))


def default_config():
    return {
        "version": 1,
        "document_globs": ["docs/**/*.md", "specs/active/**/*.md"],
        "required_metadata": {"docs/**/*.md": ["title"], "specs/active/**/*.md": ["title"]},
        "last_verified": {"required_for": [], "max_age_days": 90},
        "navigation": {"required_links": {}},
        "work_link_policy": {"allow_references_in": []},
        "generated": {
            "index": {"path": "docs/project_map/INDEX.md"},
            "work-board": {"path": "docs/project_map/WORK_BOARD.md"},
            "phase-status": {"path": "docs/project_map/PHASE_STATUS.md"},
            "freshness-report": {"path": "docs/project_map/FRESHNESS.md"}
        }
    }


def load_config(root: Path, config_arg: str):
    path = root / config_arg
    config = read_json(path)
    if config.get("version") != 1:
        raise ValueError("unsupported configuration version (expected 1)")
    return config, path


def matches(relative: str, pattern: str) -> bool:
    # pathlib-style patterns make ** match zero or more directories.
    pure = PurePosixPath(relative)
    return pure.match(pattern) or fnmatch.fnmatchcase(relative, pattern) or (
        pattern.startswith("**/") and fnmatch.fnmatchcase(relative, pattern[3:]))


def documents(root: Path, config) -> list[Path]:
    found = set()
    for pattern in config.get("document_globs", []):
        found.update(path for path in root.glob(pattern) if path.is_file())
    # Derived projections are outputs, never their own source data.  This also
    # keeps output-only files out of configured human-metadata requirements.
    generated_paths = {
        (root / entry["path"]).resolve()
        for entry in config.get("generated", {}).values() if "path" in entry
    }
    # Project Map is derived navigation rather than a primary source, while
    # ADRs are immutable history. Neither may feed a projection of current
    # documentation, even if a broad ``docs/**/*.md`` glob selected it.
    non_primary_zones = {
        (root / "docs/project_map").resolve(),
        (root / "docs/adr").resolve(),
    }
    found = {
        path for path in found
        if path.resolve() not in generated_paths
        and not any(zone == path.resolve() or zone in path.resolve().parents for zone in non_primary_zones)
    }
    return sorted(found, key=lambda item: posix(item.relative_to(root)).lower())


def frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return {}
    values = {}
    for line in text[4:closing].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"\'')
    return values


def anchor_set(text: str) -> set[str]:
    anchors, used = set(), {}
    for heading in HEADING.findall(text):
        label = re.sub(r"`([^`]*)`", r"\1", heading).lower()
        label = re.sub(r"[^\w\- ]", "", label, flags=re.UNICODE)
        label = re.sub(r"\s+", "-", label.strip())
        count = used.get(label, 0)
        used[label] = count + 1
        anchors.add(label if count == 0 else "%s-%d" % (label, count))
    return anchors


def resolve_link(root: Path, source: Path, target: str):
    target = unquote(target.strip("<>"))
    if target.startswith("#"):
        return source.resolve(), target[1:]
    if target.startswith(("http://", "https://", "mailto:", "tel:")):
        return None, None
    destination, separator, fragment = target.partition("#")
    candidate = (source.parent / destination).resolve() if destination else source.resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return "outside repository", fragment if separator else None
    return candidate, fragment if separator else None


def marker_pair(name: str):
    return ("%s%s:start -->" % (MARKER_PREFIX, name),
            "%s%s:end -->" % (MARKER_PREFIX, name))


def projection_index(root, docs):
    lines = ["# Documentation index", "", "_Generated; do not edit between markers._", ""]
    for doc in docs:
        relative = posix(doc.relative_to(root))
        meta = frontmatter(doc.read_text(encoding="utf-8"))
        title = meta.get("title") or next(iter(HEADING.findall(doc.read_text(encoding="utf-8"))), relative)
        lines.append("- [%s](../../%s)" % (title, relative))
    return "\n".join(lines) + "\n"


def work_items(root):
    rows = []
    work = root / ".work"
    if not work.is_dir():
        return rows
    for tasks in sorted(work.glob("*/TASKS.md"), key=lambda item: posix(item)):
        change = tasks.parent.name
        text = tasks.read_text(encoding="utf-8")
        headings = re.findall(r"^##\s+(.+)$", text, re.M)
        statuses = re.findall(r"^Operational status:\s*`?([^`\n]+)`?", text, re.M)
        for index, heading in enumerate(headings):
            status = statuses[index].strip() if index < len(statuses) else "unreported"
            rows.append((change, heading, status))
    return rows


def projections(root, config, docs):
    output = {}
    for name in sorted(config.get("generated", {})):
        if name == "index":
            content = projection_index(root, docs)
        elif name == "work-board":
            # ``.work`` is resumable execution state. Persisting its task
            # statuses in a Project Map would create a stale, competing
            # operational-status register, so this projection is only a
            # routing reminder.
            content = (
                "# Work board\n\n"
                "Operational task status is not projected from `.work/`.\n"
                "Read `.work/<change-id>/TASKS.md` for the current task state.\n"
            )
        elif name == "phase-status":
            lines = ["# Phase status", "", "| Document | Phase |", "| --- | --- |"]
            for doc in docs:
                metadata = frontmatter(doc.read_text(encoding="utf-8"))
                lines.append("| %s | %s |" % (posix(doc.relative_to(root)), metadata.get("phase", "unspecified")))
            content = "\n".join(lines) + "\n"
        elif name == "freshness-report":
            lines = ["# Freshness report", "", "| Document | last_verified |", "| --- | --- |"]
            for doc in docs:
                metadata = frontmatter(doc.read_text(encoding="utf-8"))
                lines.append("| %s | %s |" % (posix(doc.relative_to(root)), metadata.get("last_verified", "missing")))
            content = "\n".join(lines) + "\n"
        else:
            continue
        output[name] = content
    return output


def replace_block(text, name, content):
    start, end = marker_pair(name)
    first, last = text.find(start), text.find(end)
    if first < 0 or last < 0 or last < first or text.find(start, first + len(start)) >= 0 or text.find(end, last + len(end)) >= 0:
        return None
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = content.replace("\r\n", "\n").rstrip().replace("\n", newline)
    return text[:first + len(start)] + newline + normalized + newline + text[last:]


def read_preserving_newlines(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_preserving_newlines(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def check(root: Path, config) -> list[Finding]:
    findings, docs = [], documents(root, config)
    today = dt.date.today()
    metadata_rules = config.get("required_metadata", {})
    required_verified = config.get("last_verified", {}).get("required_for", [])
    max_age = config.get("last_verified", {}).get("max_age_days")
    allow_work = config.get("work_link_policy", {}).get("allow_references_in", [])
    for doc in docs:
        relative, text = posix(doc.relative_to(root)), doc.read_text(encoding="utf-8")
        metadata = frontmatter(text)
        for pattern, fields in metadata_rules.items():
            if matches(relative, pattern):
                for field in fields:
                    if not metadata.get(field):
                        findings.append(Finding("DG-METADATA", "error", relative, "missing configured metadata: %s" % field))
        verified = metadata.get("last_verified")
        needs_verified = any(matches(relative, pattern) for pattern in required_verified)
        if needs_verified and not verified:
            findings.append(Finding("DG-LAST-VERIFIED", "error", relative, "missing required last_verified"))
        if verified:
            try:
                date = dt.date.fromisoformat(verified)
                if max_age is not None and (today - date).days > int(max_age):
                    findings.append(Finding("DG-LAST-VERIFIED", "warning", relative, "last_verified is older than %s days" % max_age))
            except ValueError:
                findings.append(Finding("DG-LAST-VERIFIED", "error", relative, "last_verified must be YYYY-MM-DD"))
        if has_unresolved_placeholder(re.sub(r"<!--.*?-->", "", text, flags=re.S)):
            findings.append(Finding("DG-PLACEHOLDER", "error", relative, "contains an unresolved placeholder"))
        if ".work/" in text and not any(matches(relative, pattern) for pattern in allow_work):
            findings.append(Finding("DG-WORK-LEAKAGE", "warning", relative, "references ephemeral .work content outside configured allowance"))
        for raw in LINK.findall(text):
            target, fragment = resolve_link(root, doc, raw)
            if target == "outside repository":
                findings.append(Finding("DG-LINK", "error", relative, "link escapes repository: %s" % raw)); continue
            if target is not None and not target.exists():
                findings.append(Finding("DG-LINK", "error", relative, "missing link target: %s" % raw)); continue
            if fragment and target is not None and fragment not in anchor_set(target.read_text(encoding="utf-8")):
                findings.append(Finding("DG-ANCHOR", "error", relative, "missing anchor #%s in %s" % (fragment, raw.split("#", 1)[0] or relative)))
    navigation = config.get("navigation", {}).get("required_links", {})
    for source, targets in navigation.items():
        path = root / source
        if not path.is_file():
            findings.append(Finding("DG-NAVIGATION", "error", source, "configured navigation file is missing")); continue
        text = path.read_text(encoding="utf-8")
        for target in targets:
            if target not in text:
                findings.append(Finding("DG-NAVIGATION", "error", source, "missing required navigation link: %s" % target))
    for name, content in projections(root, config, docs).items():
        target = root / config["generated"][name]["path"]
        relative = posix(target.relative_to(root))
        if not target.is_file():
            findings.append(Finding("DG-GENERATED", "warning", relative, "generated projection file is missing")); continue
        replacement = replace_block(target.read_text(encoding="utf-8"), name, content)
        if replacement is None:
            findings.append(Finding("DG-GENERATED", "error", relative, "missing or ambiguous generated markers for %s" % name))
        elif replacement != target.read_text(encoding="utf-8"):
            findings.append(Finding("DG-GENERATED", "warning", relative, "generated projection is out of date"))
    return findings


def report(findings, as_json=False):
    if as_json:
        print(json.dumps([item.as_dict() for item in findings], indent=2, sort_keys=True))
    elif not findings:
        print("Documentation governance check: no findings.")
    else:
        for item in findings:
            print("%s %s %s: %s" % (item.severity.upper(), item.check, item.path, item.message))
        print("%d finding(s)." % len(findings))


def fix(root, config):
    docs = documents(root, config)
    changed = []
    for name, content in projections(root, config, docs).items():
        target = root / config["generated"][name]["path"]
        if not target.is_file():
            continue
        original = read_preserving_newlines(target)
        replacement = replace_block(original, name, content)
        if replacement is not None and replacement != original:
            write_preserving_newlines(target, replacement)
            changed.append(posix(target.relative_to(root)))
    print("Updated %d generated block(s)." % len(changed))
    for path in changed: print(path)


def self_test():
    assert not has_unresolved_placeholder("line<br>more <details><kbd>Ctrl</kbd></details>"), "inline HTML was treated as a placeholder"
    assert has_unresolved_placeholder("{{ owner }} and <requirement title>"), "template placeholders were not detected"
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        config = default_config()
        config["document_globs"] = ["docs/**/*.md"]
        config["required_metadata"] = {"docs/**/*.md": ["title"]}
        config["last_verified"]["required_for"] = ["docs/**/*.md"]
        config["generated"] = {"index": {"path": "docs/project_map/INDEX.md"}}
        (root / "docs/project_map").mkdir(parents=True)
        (root / "docs/guide.md").write_text("---\ntitle: Guide\nlast_verified: 2026-01-01\n---\n# Guide\n", encoding="utf-8")
        start, end = marker_pair("index")
        target = root / "docs/project_map/INDEX.md"
        target.write_text("before\n%s\nstale\n%s\nafter\n" % (start, end), encoding="utf-8")
        before = target.read_text(encoding="utf-8")
        check(root, config)
        assert target.read_text(encoding="utf-8") == before, "check mutated a project file"
        fix(root, config); once = target.read_text(encoding="utf-8")
        fix(root, config); assert target.read_text(encoding="utf-8") == once, "fix is not idempotent"
        assert "before\n" in once and "after\n" in once, "fix escaped generated markers"
    print("self-test passed")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Report-first documentation-governance checker (v1).")
    parser.add_argument("--root", default=".", help="adopted project root (default: current directory)")
    parser.add_argument("--config", default=CONFIG_NAME, help="configuration path relative to root")
    parser.add_argument("--json", action="store_true", help="emit check findings as JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="report findings without modifying files")
    sub.add_parser("fix", help="update only existing marked generated blocks")
    init = sub.add_parser("init", help="create a new configuration; refuses to overwrite")
    init.add_argument("--path", default=CONFIG_NAME, help="configuration path relative to root")
    sub.add_parser("self-test", help="run isolated safety and idempotence tests")
    args = parser.parse_args(argv)
    if args.command == "self-test": self_test(); return 0
    root = Path(args.root).resolve()
    if args.command == "init":
        path = root / args.path
        if path.exists():
            print("refusing to overwrite existing file: %s" % path, file=sys.stderr); return 2
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(default_config(), indent=2) + "\n", encoding="utf-8")
        print("Created %s" % posix(path.relative_to(root))); return 0
    try: config, _ = load_config(root, args.config)
    except ValueError as error: print(str(error), file=sys.stderr); return 2
    if args.command == "fix": fix(root, config); return 0
    findings = check(root, config); report(findings, args.json)
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
