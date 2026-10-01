"""Exercise real installer CLIs on unrelated temporary projects; never run models."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PORTABLE = Path(__file__).resolve().parent

class AdoptionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='kit-adoption-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.project = self.root / 'library-catalog'
        self.project.mkdir()
        self.package = self.root / 'upstream-package'
        shutil.copytree(PORTABLE, self.package, ignore=shutil.ignore_patterns('__pycache__'))
        self.agents = b'\xef\xbb\xbf# Library catalog\r\nUse SQLite fixtures.\r\n'
        (self.project / 'AGENTS.md').write_bytes(self.agents)
        (self.project / 'catalog.py').write_bytes(b'print("catalog")\n')

    def run_cli(self, write=False, expected=0):
        args = [sys.executable, '-B', '-X', 'utf8', str(PORTABLE / 'manage.py'), '--project', str(self.project), '--package', str(self.package / 'package.json')]
        if write:
            args.append('--write')
        result = subprocess.run(args, text=True, encoding='utf-8', capture_output=True, timeout=15)
        self.assertEqual(expected, result.returncode, result.stdout+result.stderr)
        return json.loads(result.stdout)

    def upstream(self, source, suffix=b'\nUpstream improvement.\n'):
        path = self.package / source
        path.write_bytes(path.read_bytes()+suffix)
        manifest = json.loads((self.package / 'package.json').read_bytes())
        manifest['version'] = '4.3.0-test-update'
        next(item for item in manifest['files'] if item['source']==source)['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.package / 'package.json').write_bytes(json.dumps(manifest).encode('utf-8'))

    def test_dry_run_creates_nothing_and_install_preserves_existing_entry_bytes(self):
        self.run_cli()
        self.assertEqual({'AGENTS.md','catalog.py'}, {p.name for p in self.project.iterdir()})
        self.run_cli(write=True)
        self.assertTrue((self.project / 'AGENTS.md').read_bytes().startswith(self.agents))
        self.assertEqual(b'print("catalog")\n', (self.project / 'catalog.py').read_bytes())
        self.assertEqual(0, self.run_cli()['writes_planned'])

    def test_update_preserves_local_core_context_and_entry_but_updates_unchanged_core(self):
        self.run_cli(write=True)
        workflow = self.project / 'Agent Kit/core/WORKFLOW.md'
        workflow.write_bytes(workflow.read_bytes()+b'\nLocal catalog rule.\n')
        context = self.project / 'Project Map/README.md'
        context.write_bytes(b'# Catalog decisions\nUse SQLite.\n')
        entry = self.project / 'AGENTS.md'
        entry.write_bytes(entry.read_bytes()+b'\r\nLocal owner rule.\r\n')
        protected = {p:p.read_bytes() for p in (workflow,context,entry)}
        self.upstream('core/WORKFLOW.md')
        self.upstream('core/OPTIONAL.md')
        report = self.run_cli(write=True)
        self.assertEqual(1, report['local_overrides'])
        for path, data in protected.items():
            self.assertEqual(data, path.read_bytes())
        self.assertEqual((self.package / 'core/OPTIONAL.md').read_bytes(), (self.project / 'Agent Kit/core/OPTIONAL.md').read_bytes())
        self.assertEqual(0, self.run_cli()['writes_planned'])

    def test_existing_colliding_files_are_preserved(self):
        path = self.project / 'Agent Kit/core/WORKFLOW.md'
        path.parent.mkdir(parents=True)
        path.write_bytes(b'Existing custom process\n')
        self.assertEqual(1, self.run_cli(write=True)['local_overrides'])
        self.upstream('core/WORKFLOW.md')
        self.run_cli(write=True)
        self.assertEqual(b'Existing custom process\n', path.read_bytes())

    def test_local_deletion_and_retired_upstream_file_are_preserved(self):
        self.run_cli(write=True)
        (self.project / 'Agent Kit/core/OPTIONAL.md').unlink()
        manifest_path = self.package / 'package.json'
        manifest = json.loads(manifest_path.read_bytes())
        manifest['files'] = [f for f in manifest['files'] if f['source']!='attribution/AUTHORS.md']
        manifest_path.write_bytes(json.dumps(manifest).encode('utf-8'))
        self.run_cli(write=True)
        self.assertFalse((self.project / 'Agent Kit/core/OPTIONAL.md').exists())
        self.assertTrue((self.project / 'Agent Kit/core/AUTHORS.md').exists())

    def test_bad_package_hash_is_rejected_before_any_project_write(self):
        (self.package / 'core/WORKFLOW.md').write_bytes(b'Unexpected bytes')
        self.run_cli(write=True, expected=2)
        self.assertEqual(self.agents, (self.project / 'AGENTS.md').read_bytes())
        self.assertFalse((self.project / 'Agent Kit').exists())

    def test_escape_and_duplicate_targets_are_rejected_before_any_project_write(self):
        manifest_path = self.package / 'package.json'
        original = json.loads(manifest_path.read_bytes())
        for target in ('../outside', 'C:/outside', '.git/config', 'AGENTS.md', 'Agent Kit/core/WORKFLOW.md'):
            manifest = json.loads(json.dumps(original))
            manifest['files'][1]['target'] = target
            manifest_path.write_bytes(json.dumps(manifest).encode('utf-8'))
            with self.subTest(target=target):
                self.run_cli(write=True, expected=2)
                self.assertEqual(self.agents, (self.project / 'AGENTS.md').read_bytes())

if __name__ == '__main__':
    unittest.main()
