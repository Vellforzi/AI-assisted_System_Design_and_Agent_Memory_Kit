"""Check that Windows attribution line endings cannot invalidate package hashes."""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ManifestPortabilityTests(unittest.TestCase):
    """Exercise the actual generator on a minimal independent package fixture."""

    def test_crlf_attribution_produces_stable_lf_payloads(self) -> None:
        """The same package remains valid when root license checkout endings change."""
        with tempfile.TemporaryDirectory(prefix="kit-manifest-") as directory:
            repository = Path(directory)
            portable = repository / "Agent Kit/portable"
            (portable / "core").mkdir(parents=True)
            (portable / "attribution").mkdir()
            (portable.parent / "VERSION").write_bytes(b"4.4.0\n")
            (repository / "LICENSE").write_bytes(b"License fixture\r\nSecond line\r\n")
            (repository / "AUTHORS.md").write_bytes(b"Fixture author\n")
            for name in ("WORKFLOW.md", "OPTIONAL.md", "PROJECT_CONTEXT.template.md"):
                (portable / "core" / name).write_bytes(b"# Fixture\n")
            script = portable / "build_manifest.py"
            script.write_bytes(Path(__file__).with_name("build_manifest.py").read_bytes())
            command = [sys.executable, "-B", str(script)]
            result = subprocess.run(command + ["--write"], capture_output=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = b"License fixture\nSecond line\n"
            self.assertEqual((portable / "attribution/LICENSE").read_bytes(), expected)
            manifest = json.loads((portable / "package.json").read_bytes())
            license_entry = next(item for item in manifest["files"]
                                 if item["source"] == "attribution/LICENSE")
            self.assertEqual(license_entry["sha256"], hashlib.sha256(expected).hexdigest())
            for ending in (b"\r\n", b"\n"):
                (repository / "LICENSE").write_bytes(ending.join([b"License fixture", b"Second line", b""]))
                check = subprocess.run(command, capture_output=True, timeout=15)
                self.assertEqual(check.returncode, 0, check.stderr + check.stdout)
                self.assertFalse(json.loads(check.stdout)["changed"])


if __name__ == "__main__":
    unittest.main()
