#!/usr/bin/env python3
"""Check/regenerate the portable allowlist from canonical version and attribution."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]

def generate(write=False):
    version = (ROOT.parent / 'VERSION').read_text(encoding='utf-8').strip()
    attribution = {ROOT / 'attribution/LICENSE': (REPO / 'LICENSE').read_bytes(),
                   ROOT / 'attribution/AUTHORS.md': (REPO / 'AUTHORS.md').read_bytes()}
    mappings = [('core/WORKFLOW.md', 'Agent Kit/core/WORKFLOW.md', 'managed'),
                ('core/OPTIONAL.md', 'Agent Kit/core/OPTIONAL.md', 'managed'),
                ('core/PROJECT_CONTEXT.template.md', 'Project Map/README.md', 'seed'),
                ('attribution/LICENSE', 'Agent Kit/core/LICENSE', 'managed'),
                ('attribution/AUTHORS.md', 'Agent Kit/core/AUTHORS.md', 'managed')]
    files = []
    for source, target, mode in mappings:
        path = ROOT / source
        data = attribution[path] if path in attribution else path.read_bytes()
        files.append({'source':source, 'target':target, 'mode':mode, 'sha256':hashlib.sha256(data).hexdigest()})
    manifest = {'schema_version':1, 'package_id':'agent-memory-kit-core', 'version':version,
                'base_commit':'557e340208d8661f00d76bdd9c4a4ea1a748ed59', 'release_status':'local_candidate_not_published', 'files':files}
    outputs = {**attribution, ROOT / 'package.json':(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode('utf-8')}
    changed = [str(path.relative_to(ROOT)) for path, data in outputs.items() if not path.exists() or path.read_bytes() != data]
    if write:
        for path, data in outputs.items():
            if str(path.relative_to(ROOT)) in changed:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    return {'ok':write or not changed, 'version':version, 'changed':changed, 'written':write}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    result = generate(parser.parse_args().write)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
