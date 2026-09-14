#!/usr/bin/env python3
"""Plan/apply portable Agent Kit adoption without overwriting local customization."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import tempfile

MANIFEST_TARGET = 'Agent Kit/INSTALLATION.json'
ENTRY_MARKER = b'<!-- agent-kit-core -->'
ENTRY_BLOCK = (b'<!-- agent-kit-core -->\n'
               b'## Agent Kit\n\n'
               b'Read `Agent Kit/core/WORKFLOW.md` for the short working process.\n'
               b'Use `Project Map/README.md` for project-owned context when relevant.\n'
               b'Optional guides apply only when the current task needs them.\n'
               b'<!-- /agent-kit-core -->\n')

def digest(data: bytes | None) -> str | None:
    return hashlib.sha256(data).hexdigest() if data is not None else None

def safe_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Expected a portable relative path')
    relative = PurePosixPath(value)
    if relative.is_absolute() or PureWindowsPath(value).is_absolute() or any(p in {'', '.', '..'} for p in value.split('/')):
        raise ValueError(f'Unsafe package path: {value}')
    path = root.joinpath(*relative.parts)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes selected root: {value}')
    if path.is_dir():
        raise ValueError(f'Expected a file: {value}')
    return path

def read(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None

def atomic_write(path: Path, data: bytes, expected: bytes | None) -> None:
    if read(path) != expected:
        raise ValueError(f'Concurrent change; reread the adoption plan: {path.name}')
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix='.agent-kit-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(handle, 'wb') as stream:
            stream.write(data)
        # Recheck after preparing bytes; do not replace a concurrent user edit.
        if read(path) != expected:
            raise ValueError(f'Concurrent change: {path.name}')
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)

def plan(project: Path, package: Path) -> tuple[dict, list[tuple[Path, bytes | None, bytes]]]:
    project = project.resolve(strict=True)
    if not project.is_dir():
        raise ValueError('Project must be an existing directory')
    package = package.resolve(strict=True)
    package_bytes = package.read_bytes()
    spec = json.loads(package_bytes)
    if spec.get('schema_version') != 1 or not isinstance(spec.get('files'), list):
        raise ValueError('Unsupported package manifest')
    package_root = package.parent
    sources = []
    seen = {MANIFEST_TARGET.casefold(), 'agents.md'}
    for entry in spec['files']:
        if not entry['target'].startswith('Agent Kit/core/') and entry['target'] != 'Project Map/README.md':
            raise ValueError('Package target is outside the portable core and context seed')
        source = safe_path(package_root, entry['source'])
        target = safe_path(project, entry['target'])
        if entry['target'].casefold() in seen:
            raise ValueError('Duplicate/reserved package target')
        seen.add(entry['target'].casefold())
        data = source.read_bytes()
        if digest(data) != entry['sha256']:
            raise ValueError(f'Package integrity mismatch: {entry["source"]}')
        if entry.get('mode', 'managed') not in {'managed', 'seed'}:
            raise ValueError('Unknown package file mode')
        sources.append((entry, source, target, data))
    manifest_path = safe_path(project, MANIFEST_TARGET)
    manifest_before = read(manifest_path)
    previous = json.loads(manifest_before) if manifest_before else {'schema_version':1, 'files':{}}
    if previous.get('schema_version') != 1 or not isinstance(previous.get('files'), dict):
        raise ValueError('Unsupported installation manifest; preserve it and migrate explicitly')
    if manifest_before is not None and previous.get('package_id') != spec['package_id']:
        raise ValueError('Installation belongs to a different package')
    previous_files = previous['files']
    # A malicious or damaged prior manifest cannot introduce foreign paths.
    for name in previous_files:
        safe_path(project, name)
    operations = []
    rows = []
    files = {}
    for entry, source, target, data in sources:
        name = entry['target']
        before = read(target)
        old = previous_files.get(name)
        mode = entry.get('mode', 'managed')
        if mode == 'seed' and (before is not None or old):
            state = 'preserved_project_owned'
        elif old and before is None:
            state = 'preserved_local_removal'
        elif before == data:
            state = 'unchanged'
        elif before is None and not old:
            state = 'install'
        elif old and mode == 'managed' and digest(before) == old.get('installed_sha256'):
            state = 'update'
        else:
            state = 'preserved_local'
        if state in {'install', 'update'}:
            operations.append((target, before, data))
        installed = digest(data) if state in {'install', 'update', 'unchanged'} else (old or {}).get('installed_sha256')
        files[name] = {'source':entry['source'], 'mode':mode, 'installed_sha256':installed,
                       'upstream_sha256':digest(data), 'local_override':state.startswith('preserved_local')}
        rows.append({'path':name, 'state':state, 'source':str(source)})
    retired = sorted(set(previous_files) - set(files))
    entry_path = safe_path(project, 'AGENTS.md')
    entry_before = read(entry_path)
    entry_state = 'preserved_existing'
    if not previous.get('entrypoint_managed') and ENTRY_MARKER not in (entry_before or b''):
        if b'\x00' in (entry_before or b''):
            raise ValueError('AGENTS.md needs an explicit encoding-safe integration')
        (entry_before or b'').decode('utf-8-sig', errors='strict')
        eol = b'\r\n' if b'\r\n' in (entry_before or b'') else b'\n'
        separator = eol * 2 if entry_before else b''
        operations.append((entry_path, entry_before, (entry_before or b'') + separator + ENTRY_BLOCK.replace(b'\n', eol)))
        entry_state = 'append_core_link'
    rows.append({'path':'AGENTS.md', 'state':entry_state})
    installed_manifest = {'schema_version':1, 'package_id':spec['package_id'], 'package_version':spec['version'],
                          'base_commit':spec['base_commit'], 'package_manifest_sha256':digest(package_bytes),
                          'entrypoint_managed':True, 'files':files,
                          'retired_preserved':sorted(set(previous.get('retired_preserved', [])) | set(retired))}
    encoded = (json.dumps(installed_manifest, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    if manifest_before != encoded:
        operations.append((manifest_path, manifest_before, encoded))
    return {'package_version':spec['version'], 'project':str(project), 'files':rows,
            'retired_preserved':installed_manifest['retired_preserved'], 'writes_planned':len(operations)}, operations

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--package', type=Path, default=Path(__file__).with_name('package.json'))
    parser.add_argument('--write', action='store_true', help='Apply the plan; the default is read-only')
    args = parser.parse_args()
    try:
        report, operations = plan(args.project, args.package)
        if args.write:
            # Resolve every destination and preimage before the first write.
            for path, before, _ in operations:
                safe_path(args.project.resolve(), path.relative_to(args.project.resolve()).as_posix())
                if read(path) != before:
                    raise ValueError('Concurrent change before applying the plan')
            for path, before, data in operations:
                atomic_write(path, data, before)
        report.update(ok=True, applied=args.write, local_overrides=sum(row['state'].startswith('preserved_local') for row in report['files']))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'ok':False, 'error':str(error)}, ensure_ascii=False))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
