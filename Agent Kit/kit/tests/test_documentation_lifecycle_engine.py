"""Contract coverage for the opt-in documentation lifecycle engine."""

from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


KIT = Path(__file__).resolve().parents[1]
ENGINE = KIT / "optional_integrations/documentation_governance/engine"
sys.path.insert(0, str(ENGINE))

from documentation_governance.checks import build_report  # noqa: E402
from documentation_governance.config import PolicyError, load_exceptions, load_policy, load_registry  # noqa: E402
from documentation_governance.delta import build_delta_report  # noqa: E402
from documentation_governance.git_snapshot import (  # noqa: E402
    _batch_blobs,
    revision_snapshot,
    staged_snapshot,
    worktree_snapshot,
)


POLICY_PATH = "docs/documentation_governance_policy.json"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class DocumentationLifecycleEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = Path(tempfile.mkdtemp(prefix="documentation-lifecycle-"))
        self.addCleanup(shutil.rmtree, self.temporary, True)
        self.root = self.temporary / "project"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Documentation Test")
        write_json(self.root / POLICY_PATH, {
            "schema_version": "documentation-governance-policy.v1",
            "document_roots": ["docs/"],
            "root_documents": ["README.md", ".codexignore"],
            "entrypoints": ["README.md"],
            "lifecycle_registry": "docs/documentation_lifecycle_registry.json",
            "exceptions_registry": "docs/documentation_validation_exceptions.json",
            "active_lifecycles": ["current-source", "active-support"],
            "history_lifecycles": ["historical-record", "superseded"],
            "delta_forbid": ["DOC-REACH-001"],
        })
        write_json(self.root / "docs/documentation_validation_exceptions.json", {
            "schema_version": "documentation-validation-exceptions.v1", "exceptions": [],
        })
        write_json(self.root / "docs/documentation_lifecycle_registry.json", {
            "schema_version": "documentation-lifecycle-registry.v1",
            "rules": [
                {"id": "entry", "lifecycle": "current-source", "paths": ["README.md"]},
                {"id": "root-support", "lifecycle": "active-support", "paths": [".codexignore"]},
                {"id": "governance", "lifecycle": "current-source", "paths": [
                    POLICY_PATH,
                    "docs/documentation_lifecycle_registry.json",
                    "docs/documentation_validation_exceptions.json",
                ]},
                {"id": "active", "lifecycle": "active-support", "globs": ["docs/active/**"]},
                {"id": "history", "lifecycle": "historical-record", "globs": ["docs/archive/**"]},
                {"id": "superseded", "lifecycle": "superseded", "paths": ["docs/legacy.md"]},
            ],
            "navigation": {
                "routes": [],
                "superseded_successors": [{"path": "docs/legacy.md", "successor": "docs/active/guide.md"}],
                "moved_paths": [{"old": "docs/old-location.md", "new": "docs/archive/moved.md"}],
            },
        })
        (self.root / "docs/active").mkdir(parents=True)
        (self.root / "docs/archive").mkdir(parents=True)
        (self.root / "README.md").write_text(
            "# Project\n\n"
            "[Policy](docs/documentation_governance_policy.json)\n"
            "[Registry](docs/documentation_lifecycle_registry.json)\n"
            "[Exceptions](docs/documentation_validation_exceptions.json)\n"
            "[Guide](docs/active/guide.md#guide)\n"
            "[Unicode](docs/active/память.md)\n",
            encoding="utf-8",
        )
        (self.root / "docs/active/guide.md").write_text("# Guide\n\n[Archive directory](../archive)\n", encoding="utf-8")
        (self.root / ".codexignore").write_text("secrets/\n", encoding="utf-8")
        (self.root / "docs/active/память.md").write_text("# Память\n", encoding="utf-8")
        (self.root / "docs/archive/history.md").write_text("# History\n\n[Missing](missing.md)\n", encoding="utf-8")
        (self.root / "docs/archive/moved.md").write_text("# Moved\n", encoding="utf-8")
        (self.root / "docs/legacy.md").write_text("# Legacy\n", encoding="utf-8")
        (self.root / "src").mkdir()
        (self.root / "src/app.py").write_text("print('runtime is not a documentation body')\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def git(self, *args: str) -> str:
        completed = subprocess.run(["git", *args], cwd=self.root, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return completed.stdout

    def test_active_and_history_body_modes_keep_global_lifecycle_invariants(self) -> None:
        snapshot = revision_snapshot(self.root, "HEAD")
        self.assertIn("src/app.py", snapshot.paths)
        self.assertNotIn("src/app.py", snapshot.files)
        active = build_report(snapshot, policy_path=POLICY_PATH, today=dt.date(2026, 8, 14))
        history = build_report(snapshot, policy_path=POLICY_PATH, include_history=True, today=dt.date(2026, 8, 14))

        self.assertEqual(active["status"], "passed")
        self.assertLess(active["body_document_count"], history["body_document_count"])
        self.assertEqual(history["finding_count"], 1)
        self.assertEqual(history["findings"][0]["id"], "DOC-LINK-001")
        self.assertEqual(active, build_report(snapshot, policy_path=POLICY_PATH, today=dt.date(2026, 8, 14)))

    def test_staged_snapshot_ignores_unstaged_substitution(self) -> None:
        guide = self.root / "docs/active/guide.md"
        guide.write_text("# Guide\n\nSafe staged text.\n", encoding="utf-8")
        self.git("add", "docs/active/guide.md")
        guide.write_text("# Guide\n\n[Escape](../../../outside.md)\n", encoding="utf-8")

        staged = build_report(staged_snapshot(self.root), policy_path=POLICY_PATH, today=dt.date(2026, 8, 14))
        worktree = build_report(worktree_snapshot(self.root), policy_path=POLICY_PATH, today=dt.date(2026, 8, 14))

        self.assertEqual(staged["status"], "passed")
        self.assertIn("DOC-LINK-002", {item["id"] for item in worktree["findings"]})

    def test_worktree_delta_blocks_only_new_reachability_finding(self) -> None:
        baseline = build_report(revision_snapshot(self.root, "HEAD"), policy_path=POLICY_PATH, today=dt.date(2026, 8, 14))
        (self.root / "docs/active/orphan.md").write_text("# Orphan\n", encoding="utf-8")
        candidate = build_report(worktree_snapshot(self.root), policy_path=POLICY_PATH, today=dt.date(2026, 8, 14))
        delta = build_delta_report(baseline, candidate, ["DOC-REACH-001"])

        self.assertEqual(delta["status"], "failed")
        self.assertEqual(delta["introduced_finding_count"], 1)
        self.assertEqual(delta["introduced_findings"][0]["path"], "docs/active/orphan.md")

    def test_ambiguous_lifecycle_and_expired_exception_fail_closed(self) -> None:
        registry_path = self.root / "docs/documentation_lifecycle_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["rules"].append({"id": "overlap", "lifecycle": "historical-record", "paths": ["docs/active/guide.md"]})
        write_json(registry_path, registry)
        exceptions_path = self.root / "docs/documentation_validation_exceptions.json"
        write_json(exceptions_path, {
            "schema_version": "documentation-validation-exceptions.v1",
            "exceptions": [{
                "rule_id": "DOC-LIFECYCLE-002", "path": "docs/active/guide.md",
                "message": "Managed document matches multiple lifecycle rules: active, overlap.",
                "owner": "docs-owner", "expires": "2026-08-13",
            }],
        })

        report = build_report(worktree_snapshot(self.root), policy_path=POLICY_PATH, today=dt.date(2026, 8, 14))
        ids = {item["id"] for item in report["findings"]}
        self.assertIn("DOC-LIFECYCLE-002", ids)
        self.assertIn("DOC-EXCEPTION-001", ids)

    def test_missing_successor_and_moved_destination_are_global_findings(self) -> None:
        (self.root / "docs/active/guide.md").unlink()
        (self.root / "docs/archive/moved.md").unlink()
        report = build_report(worktree_snapshot(self.root), policy_path=POLICY_PATH, today=dt.date(2026, 8, 14))
        ids = {item["id"] for item in report["findings"]}
        self.assertIn("DOC-SUCCESSOR-002", ids)
        self.assertIn("DOC-MOVE-002", ids)

    def test_cli_reports_are_deterministic_and_delta_exit_is_blocking(self) -> None:
        cli = ENGINE / "documentation_governance_cli.py"
        command = [
            sys.executable, str(cli), "--root", str(self.root), "--policy", POLICY_PATH,
            "--format", "json", "check", "--full",
        ]
        first = subprocess.run(command, text=True, capture_output=True, check=False)
        second = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)

        (self.root / "docs/active/orphan.md").write_text("# Orphan\n", encoding="utf-8")
        delta = subprocess.run([
            sys.executable, str(cli), "--root", str(self.root), "--policy", POLICY_PATH,
            "--format", "json", "delta", "--worktree", "--forbid", "DOC-REACH-001",
        ], text=True, capture_output=True, check=False)
        self.assertEqual(delta.returncode, 1, delta.stderr + delta.stdout)
        self.assertEqual(json.loads(delta.stdout)["introduced_finding_count"], 1)

    def test_distributed_templates_validate_and_unsafe_policy_path_fails(self) -> None:
        templates = ENGINE / "templates"
        load_policy((templates / "documentation_governance_policy.template.json").read_text(encoding="utf-8"))
        load_registry((templates / "documentation_lifecycle_registry.template.json").read_text(encoding="utf-8"))
        load_exceptions((templates / "documentation_validation_exceptions.template.json").read_text(encoding="utf-8"))
        for schema in sorted((ENGINE / "schemas").glob("*.json")):
            self.assertEqual(json.loads(schema.read_text(encoding="utf-8"))["$schema"], "https://json-schema.org/draft/2020-12/schema")
        registry = json.loads((ENGINE / "checks_registry.json").read_text(encoding="utf-8"))
        ids = [item["id"] for item in registry["checks"]]
        self.assertEqual(ids, sorted(set(ids)))
        implementation = (ENGINE / "documentation_governance/checks.py").read_text(encoding="utf-8")
        emitted = set(re.findall(r'Finding\("(DOC-[A-Z0-9-]+)"', implementation))
        self.assertEqual(set(ids), emitted)

        unsafe = json.loads((templates / "documentation_governance_policy.template.json").read_text(encoding="utf-8"))
        unsafe["lifecycle_registry"] = "../outside.json"
        with self.assertRaises(PolicyError):
            load_policy(json.dumps(unsafe))

    def test_git_batch_provider_handles_more_requests_than_a_pipe_buffer(self) -> None:
        oid = self.git("rev-parse", "HEAD:README.md").strip()
        objects = [(oid, f"virtual/{index}.md") for index in range(2000)]
        result = _batch_blobs(self.root, objects)
        self.assertEqual(len(result), 2000)
        self.assertTrue(result["virtual/1999.md"].startswith("# Project"))

    def test_baseline_prefix_adapter_preserves_frozen_classification_and_post_baseline_rules(self) -> None:
        baseline = self.git("rev-parse", "HEAD").strip()
        policy = json.loads((self.root / POLICY_PATH).read_text(encoding="utf-8"))
        policy["registry_adapter"] = "baseline-prefix-v1"
        write_json(self.root / POLICY_PATH, policy)
        write_json(self.root / "docs/documentation_lifecycle_registry.json", {
            "schema_version": "documentation_lifecycle_registry.v1",
            "documentation_metadata": {"status": "active"},
            "baseline": {"revision": baseline},
            "review_metadata": {"reviewed": True},
            "rules": [
                {"id": "baseline-active", "lifecycle": "active-support", "baseline_only": True,
                 "prefixes": ["docs/active/"], "exclude_paths": ["docs/active/guide.md"]},
                {"id": "baseline-current", "lifecycle": "current-source", "baseline_only": True,
                 "paths": ["docs/active/guide.md", POLICY_PATH,
                           "docs/documentation_lifecycle_registry.json", "docs/documentation_validation_exceptions.json"]},
                {"id": "post-baseline", "lifecycle": "active-support", "paths": ["docs/active/new.md"]},
                {"id": "baseline-history", "lifecycle": "historical-record", "baseline_only": True,
                 "fallback_for_baseline": True, "prefixes": ["docs/"]},
            ],
            "navigation": {
                "approved_entrypoints": ["README.md"],
                "routes": [{"id": "active", "from": "README.md", "prefixes": ["docs/active/"]}],
                "superseded_successors": [], "moved_paths": [],
            },
        })
        write_json(self.root / "docs/documentation_validation_exceptions.json", {
            "schema_version": "documentation_validation_exceptions.v1",
            "documentation_metadata": {"status": "active"},
            "review_metadata": {"cadence": "weekly"},
            "exceptions": [{
                "id": "history-link", "rule_id": "DOC-REFERENCE-001",
                "target": {"path": "docs/archive/history.md", "line": 3,
                           "details": {"destination": "missing.md"}},
                "reason": "reviewed", "owner": "docs", "created": "2026-08-14", "expires": "2026-09-01",
            }],
        })
        (self.root / "docs/active/new.md").write_text("# New\n", encoding="utf-8")

        snapshot = worktree_snapshot(self.root)
        report = build_report(snapshot, policy_path=POLICY_PATH, include_history=True, today=dt.date(2026, 8, 14))

        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["suppressed_finding_count"], 1)
        self.assertEqual(report["lifecycle_counts"], {
            "active-support": 3, "current-source": 5, "historical-record": 3, "superseded": 0,
        })


if __name__ == "__main__":
    unittest.main()
