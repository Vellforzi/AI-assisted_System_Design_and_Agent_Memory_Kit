"""Check missing payload/dependency/link and mirror-drift rejection in isolation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from check_skill_library import contained, verify


class LibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.payload = b'---\nname: demo\ndescription: Fixture\n---\n'
        self.manifest = {
            'schema': 'agent-kit-skill-library/v1',
            'files': {}, 'mirrors': [],
            'skills': [{'name': 'demo', 'path': 'skills/demo',
                        'files': ['SKILL.md'], 'conditional_dependencies': []}],
        }
        self.put('skills/demo/SKILL.md', self.payload)
        self.save_manifest()

    def put(self, relative: str, data: bytes) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        self.manifest['files'][relative] = hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()

    def save_manifest(self) -> None:
        (self.root / 'skills/library.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_complete_bundle_and_git_eol_conversion(self) -> None:
        (self.root / 'skills/demo/SKILL.md').write_bytes(self.payload.replace(b'\n', b'\r\n'))
        self.assertTrue(all(verify(self.root).values()))

    def test_missing_payload_rejected(self) -> None:
        (self.root / 'skills/demo/SKILL.md').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing or changed'):
            verify(self.root)

    def test_modified_payload_rejected(self) -> None:
        (self.root / 'skills/demo/SKILL.md').write_bytes(self.payload + b'changed')
        with self.assertRaisesRegex(ValueError, 'Missing or changed'):
            verify(self.root)

    def test_missing_dependency_rejected(self) -> None:
        self.manifest['skills'][0]['conditional_dependencies'] = ['absent']
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'Missing dependency'):
            verify(self.root)

    def test_broken_link_rejected_even_with_matching_hash(self) -> None:
        self.put('skills/demo/SKILL.md', self.payload + b'[required](missing.md)\n')
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'Broken local link'):
            verify(self.root)

    def test_mirror_drift_rejected_even_with_matching_hash(self) -> None:
        self.put('cursor/demo/SKILL.md', self.payload + b'different\n')
        self.manifest['mirrors'] = [{'source': 'skills/demo/SKILL.md', 'mirror': 'cursor/demo/SKILL.md'}]
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'Mirror drift'):
            verify(self.root)

    def test_path_escape_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, 'Path outside kit'):
            contained(self.root, '../outside')


if __name__ == '__main__':
    unittest.main()
