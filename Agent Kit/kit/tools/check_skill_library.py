"""Verify the optional skill payload and optionally run its existing helper suites."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def contained(root: Path, relative: str) -> Path:
    """Reject manifest paths outside the source kit, including symlink escapes."""
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError(f'Path outside kit: {relative}')
    return path


def verify(root: Path, helpers: bool = False) -> dict[str, bool]:
    """Check distribution integrity, not instruction adherence or client activation."""
    manifest = json.loads((root / 'skills/library.json').read_text(encoding='utf-8'))
    if manifest['schema'] != 'agent-kit-skill-library/v1':
        raise ValueError('Unsupported skill library schema')
    cases = {}
    for relative, expected in manifest['files'].items():
        path = contained(root, relative)
        if not path.is_file() or hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise ValueError(f'Missing or changed payload: {relative}')
        if path.suffix in {'.md', '.py', '.yaml', '.json'}:
            content = path.read_text(encoding='utf-8-sig')
            if '\ufffd' in content:
                raise ValueError(f'Replacement character: {relative}')
        if path.suffix == '.md':
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
                if re.match(r'^[a-zA-Z][\w+.-]*:', target) or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0].strip('<>')
                if target and not (path.parent / target).exists():
                    raise ValueError(f'Broken local link in {relative}: {target}')
    cases['declared_payload_integrity'] = True
    cases['local_references_resolve'] = True
    names = {entry['name'] for entry in manifest['skills']}
    if len(names) != len(manifest['skills']):
        raise ValueError('Duplicate skill identity')
    for entry in manifest['skills']:
        for dependency in entry['conditional_dependencies']:
            if dependency not in names:
                raise ValueError(f'Missing dependency: {dependency}')
        for relative in entry['files']:
            target = entry['path'] + '/' + relative
            if target not in manifest['files']:
                raise ValueError(f'Undeclared skill file: {target}')
        core = contained(root, entry['path'] + '/SKILL.md').read_text(encoding='utf-8-sig')
        if not core.startswith('---\n') or f'name: {entry["name"]}\n' not in core:
            raise ValueError(f'Invalid skill identity: {entry["name"]}')
    cases['library_dependencies_present'] = True
    for entry in manifest['mirrors']:
        if (contained(root, entry['source']).read_bytes().replace(b'\r\n', b'\n') !=
                contained(root, entry['mirror']).read_bytes().replace(b'\r\n', b'\n')):
            raise ValueError(f'Mirror drift: {entry["mirror"]}')
    cases['declared_mirrors_equal'] = True
    if helpers:
        for name, relative in [
            ('checker_regressions', 'tools/test_skill_library.py'),
            ('recovery_helper_regressions', 'skills/long-task-recovery/scripts/test_recovery_tool.py'),
            ('prompt_compiler_regressions', 'skills/outcome-driven-task-closure/evals/run_prompt_compiler_evals.py'),
        ]:
            result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(contained(root, relative))],
                                    cwd=root, capture_output=True, timeout=120)
            if result.returncode:
                sys.stderr.buffer.write(result.stdout + result.stderr)
                raise ValueError(f'Helper suite failed: {name}')
            cases[name] = True
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kit', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--helpers', action='store_true')
    args = parser.parse_args()
    try:
        cases = verify(args.kit.resolve(), args.helpers)
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps({'schema': 'behavior-check-report/v1', 'cases': cases}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
