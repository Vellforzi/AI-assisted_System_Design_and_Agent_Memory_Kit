"""Behavioral tests for memory storage/retrieval, not scores for an LLM.

Oracles: explicit owner constraints, literal fixture bytes and independent
expected lifecycle/branch/revision boundaries. All files are disposable.
"""
from __future__ import annotations
import copy
import json
import os
import socket
import tempfile
import unittest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from engine import Memory, MemoryError, digest, encoded, safe_path
from install import install, PACKAGE_FILES


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.config = {"schema_version": 1, "project_id": "fixture", "records_dir": "Project Map/memory/records",
                       "cache_dir": ".generated/memory", "record_language": "en", "default_branch": "main",
                       "write_enabled": True, "reference_files": [], "term_aliases": [["подписка", "subscription"]]}
        (self.root / "Project Map").mkdir()
        (self.root / "source.txt").write_bytes(b"Actual source version one.\n")
        (self.root / "owner.txt").write_text("Пиши мне на русском, project records in English.\n", encoding="utf-8")
        self.configure()

    def tearDown(self):
        self.tmp.cleanup()

    def configure(self):
        (self.root / "Project Map/memory.config.json").write_bytes(encoded(self.config))
        self.m = Memory(self.root)

    def record(self, identifier="MEM-001", **overrides):
        r = {"id": identifier, "kind": "fact", "subject": "memory-routing", "scope": "agent.memory", "branch": "main", "language": "en",
             "title": "Subscription-only memory", "summary": "The active agent writes English project records without another model.",
             "search_keys": {"ru": ["память без API", "русский запрос английские записи", "подписка"], "en": ["subscription memory", "English records", "no API"]},
             "original": {"text": "Память без API; records in English.", "language": "mixed", "kind": "agent_analysis", "event_id": identifier + "-origin", "ref": "fixture-turn"},
             "evidence": [{"path": "source.txt", "sha256": digest((self.root / "source.txt").read_bytes()), "role": "source", "freshness": "required"}],
             "applicability": "Only the named fixture project and main branch.", "verification": {"level": "source", "note": "Source bytes only; no runtime or acceptance claim."}}
        r.update(overrides)
        return r

    def active(self, record=None):
        r = record or self.record()
        self.m.stage(r, r["id"] + "-stage")
        return self.m.transition(r["id"], "active", r["id"] + "-active", 1, "Inspected the literal fixture source")

    def assert_error(self, code, fn):
        with self.assertRaises(MemoryError) as cm:
            fn()
        self.assertEqual(code, cm.exception.code)

    def test_new_owner_reaffirmation_keeps_old_record_retired(self):
        r = self.record(kind="owner_decision")
        literal = (self.root / "owner.txt").read_text(encoding="utf-8")
        r["original"].update(text=literal, kind="owner_statement", language="mixed", ref="owner.txt")
        r["evidence"] = [{"path": "owner.txt", "sha256": digest((self.root / "owner.txt").read_bytes()), "role": "owner_statement", "freshness": "required"}]
        r["verification"] = {"level": "owner_statement", "note": "Explicit fixture owner decision."}
        self.active(r)
        self.m.transition("MEM-001", "revoked", "revoke-original", 2, "Owner withdrew this decision.")
        prior = self.m.record_path("MEM-001").read_bytes()
        (self.root / "owner-new.txt").write_text(literal, encoding="utf-8")
        renewed = copy.deepcopy(r)
        renewed["id"] = "MEM-002"
        renewed["original"].update(event_id="new-independent-owner-event", ref="owner-new.txt")
        renewed["evidence"][0].update(path="owner-new.txt", sha256=digest((self.root / "owner-new.txt").read_bytes()))
        self.active(renewed)
        self.assertEqual("active", self.m.read("MEM-002")["status"])
        self.assertEqual("revoked", self.m.read("MEM-001")["status"])
        self.assertEqual(prior, self.m.record_path("MEM-001").read_bytes())

    def test_retired_origin_cannot_be_replayed_under_new_id(self):
        r = self.record()
        self.active(r)
        self.m.transition("MEM-001", "revoked", "revoke-original", 2, "Origin no longer accepted.")
        replay = copy.deepcopy(r)
        replay["id"] = "MEM-002"
        self.assert_error("duplicate_or_echo", lambda: self.m.stage(replay, "replayed-origin"))

    def test_candidate_is_not_current(self):
        self.m.stage(self.record(), "test-stage")
        self.assertEqual([], self.m.search(["память"])["hits"])
        self.assertEqual("candidate", self.m.search(["память"], include_history=True)["hits"][0]["status"])

    def test_bilingual_queries_and_exact_id(self):
        self.active()
        for query in ["память без API", "English project records", "subscription-only", "MEM-001", "русский запрос", "memory", "SUBSCRIPTION", "подписка"]:
            with self.subTest(query=query):
                self.assertEqual("MEM-001", self.m.search([query])["hits"][0]["id"])
        self.assertTrue(self.m.search(["MEM-001"])["hits"][0]["exact_identifier"])

    def test_original_is_preserved(self):
        r = self.record(); r["original"]["text"] = "«Ёж» и E:\\Dev Projects — don't translate identifiers."
        self.active(r)
        self.assertEqual(r["original"], self.m.read("MEM-001")["record"]["original"])

    def test_search_does_not_write_even_when_index_missing(self):
        self.active(); before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.m.search(["memory"])
        after = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_cas_conflict_preserves_bytes(self):
        self.active(); p = self.m.record_path("MEM-001"); before = p.read_bytes()
        self.assert_error("cas_conflict", lambda: self.m.transition("MEM-001", "revoked", "revoke", 1, "stale writer"))
        self.assertEqual(before, p.read_bytes())

    def test_duplicate_operation_not_repeated_after_later_revision(self):
        r = self.record(); self.m.stage(r, "stage-once"); self.m.transition(r["id"], "active", "activate-once", 1, "Source reviewed")
        result = self.m.stage(r, "stage-once")
        self.assertTrue(result["duplicate"]); self.assertEqual(1, result["accepted_revision"]); self.assertEqual(2, result["current_revision"])

    def test_operation_reuse_with_different_payload_fails(self):
        r = self.record(); self.m.stage(r, "same-key"); r["summary"] = "Changed claim"
        self.assert_error("operation_conflict", lambda: self.m.stage(r, "same-key"))

    def test_source_drift_hides_current_claim_without_canonical_write(self):
        self.active(); p = self.m.record_path("MEM-001"); before = p.read_bytes()
        (self.root / "source.txt").write_bytes(b"Version two\n")
        result = self.m.search(["memory"])
        self.assertEqual([], result["hits"]); self.assertEqual(1, result["skipped"]["stale"])
        self.assertEqual("stale", self.m.read("MEM-001")["effective_status"])
        self.assertEqual(1, len(self.m.audit()["findings"]))
        self.assertEqual(before, p.read_bytes())

    def test_late_promotion_of_old_source_fails(self):
        self.m.stage(self.record(), "stage")
        (self.root / "source.txt").write_bytes(b"New source\n")
        self.assert_error("stale_evidence", lambda: self.m.transition("MEM-001", "active", "activate", 1, "Outdated result"))

    def test_retirement_does_not_require_missing_source(self):
        self.active(); (self.root / "source.txt").unlink()
        self.m.transition("MEM-001", "revoked", "retire", 2, "Origin removed")
        self.assertEqual("revoked", self.m.read("MEM-001")["status"])

    def test_retired_record_cannot_resurrect(self):
        self.active(); self.m.transition("MEM-001", "revoked", "retire", 2, "Owner corrected this")
        self.assert_error("retired_record", lambda: self.m.stage(self.record(), "late-stage", 3))

    def test_agent_analysis_cannot_be_owner_decision(self):
        r = self.record(kind="owner_decision"); self.m.stage(r, "stage")
        self.assert_error("owner_evidence_required", lambda: self.m.transition(r["id"], "active", "activate", 1, "No owner evidence"))

    def test_source_test_build_runtime_are_not_interchangeable(self):
        r = self.record(); r["verification"]["level"] = "runtime"; self.m.stage(r, "stage")
        self.assert_error("evidence_level_mismatch", lambda: self.m.transition(r["id"], "active", "activate", 1, "No runtime evidence"))

    def test_owner_requirement_not_cancelled_by_implementation_change(self):
        r = self.record(kind="owner_decision"); r["original"]["kind"] = "owner_statement"
        r["evidence"] = [{"path": "owner.txt", "sha256": digest((self.root / "owner.txt").read_bytes()), "role": "owner_statement", "freshness": "required"}, {**r["evidence"][0], "freshness": "historical"}]
        r["verification"]["level"] = "owner_statement"; self.active(r)
        (self.root / "source.txt").write_bytes(b"Implementation changed\n")
        self.assertEqual("active", self.m.read(r["id"])["effective_status"])

    def test_branch_and_scope_isolation(self):
        self.active(); other = self.record("MEM-002", branch="feature"); self.active(other)
        third = self.record("MEM-003", scope="api.cache"); self.active(third)
        result = self.m.search(["memory"], scope="agent.memory")
        self.assertEqual(["MEM-001"], [h["id"] for h in result["hits"]])
        self.assertEqual(["MEM-002"], [h["id"] for h in self.m.search(["memory"], scope="agent.memory", branch="feature")["hits"]])

    def test_immutable_identity(self):
        self.active(); r = self.record(branch="feature")
        self.assert_error("immutable_identity", lambda: self.m.stage(r, "edit", 2))

    def test_revision_bound_dependency(self):
        self.active(); r = self.record("MEM-002", subject="derived-case", summary="Derived experience in a different subject")
        r["relationships"] = [{"id": "MEM-001", "revision": 2, "relation": "derived_from"}]; self.active(r)
        self.m.transition("MEM-001", "revoked", "parent-retire", 2, "Owner correction")
        self.assertEqual("stale", self.m.read("MEM-002")["effective_status"])

    def test_unknown_relationship_fails(self):
        r = self.record(); r["relationships"] = [{"id": "MEM-999", "revision": 1, "relation": "related"}]
        self.assert_error("stale_relationship", lambda: self.m.stage(r, "stage"))

    def test_supersession_requires_matching_subject(self):
        self.active(); self.active(self.record("MEM-002", subject="different", summary="Different subject"))
        self.assert_error("invalid_successor", lambda: self.m.transition("MEM-001", "superseded", "supersede", 2, "Wrong subject", "MEM-002"))

    def test_supersession_preserves_history_and_hides_old_record(self):
        self.active(); self.active(self.record("MEM-002", summary="The new supported decision replaces the former behavior."))
        self.m.transition("MEM-001", "superseded", "replace", 2, "New supported decision", "MEM-002")
        self.assertEqual("MEM-002", self.m.read("MEM-001")["successor"])
        self.assertEqual(3, len(self.m.read("MEM-001", True)["history"]))
        self.assertNotIn("MEM-001", [h["id"] for h in self.m.search(["memory"])["hits"]])
        self.m.transition("MEM-002", "revoked", "revoke-new", 2, "Do not restore the old decision")
        self.assertEqual([], self.m.search(["memory"])["hits"])

    def test_marked_echo_and_fake_origin_rejected(self):
        r = self.record(); r["original"]["text"] = '<amk_memory_context>old memory</amk_memory_context>'
        self.assert_error("derived_echo", lambda: self.m.stage(r, "stage"))
        r = self.record(); r["original"]["kind"] = "translation"
        self.assert_error("invalid_origin", lambda: self.m.stage(r, "stage-other"))

    def test_known_duplicate_rejected(self):
        self.active(); self.assert_error("duplicate_or_echo", lambda: self.m.stage(self.record("MEM-002"), "duplicate"))

    def test_memory_not_independent_source(self):
        self.active(); r = self.record("MEM-002", subject="second")
        p = self.m.record_path("MEM-001"); r["evidence"][0].update(path=p.relative_to(self.root).as_posix(), sha256=digest(p.read_bytes()))
        self.assert_error("derived_echo", lambda: self.m.stage(r, "stage-derived"))

    def test_history_tampering_is_detected(self):
        self.active(); p = self.m.record_path("MEM-001"); data = json.loads(p.read_bytes()); data["versions"][0]["reason"] = "Rewritten past"
        p.write_bytes(encoded(data)); self.assert_error("invalid_history", lambda: self.m.read("MEM-001"))

    def test_cross_project_file_rejected(self):
        self.active(); self.config["project_id"] = "other"; self.configure()
        self.assert_error("record_identity", lambda: self.m.read("MEM-001"))

    def test_path_traversal_and_windows_devices(self):
        for p in ["../outside", "/tmp/file", "C:/file", "a/../file", "a\\b", "CON.txt", ".git/config"]:
            with self.subTest(path=p): self.assert_error("unsafe_path", lambda: safe_path(self.root, p))

    def test_symlink_rejected_when_os_allows_fixture(self):
        p = self.root / "link"
        try: p.symlink_to(self.root / "source.txt")
        except OSError: self.skipTest("OS account cannot create a disposable symlink")
        self.assert_error("unsafe_path", lambda: self.m.source("link"))

    def test_obvious_secret_rejected_without_echo(self):
        r = self.record(); r["summary"] = "sk-proj-" + "X" * 40
        self.assert_error("unsafe_record", lambda: self.m.stage(r, "stage"))

    def test_read_only_profile(self):
        self.config["write_enabled"] = False; self.configure()
        self.assert_error("read_only", lambda: self.m.stage(self.record(), "stage"))

    def test_no_network_or_model_is_used(self):
        with patch.object(socket, "socket", side_effect=AssertionError("Network access forbidden")):
            self.active(); self.m.index(); self.m.search(["memory"]); self.m.audit()

    def test_cache_is_disposable_and_source_bound(self):
        self.active(); self.m.index(); cache = self.m.cache / "index.sqlite3"; before = cache.read_bytes()
        self.assertEqual("valid_cache", self.m.search(["memory"])["index"])
        self.active(self.record("MEM-002", subject="other", summary="New indexing example"))
        self.assertEqual("stale_rebuilt_in_memory", self.m.search(["memory"])["index"])
        self.assertEqual(before, cache.read_bytes())

    def test_safe_fts_syntax(self):
        self.active(); self.assertEqual("ok", self.m.search(['memory OR NOT " : () *'])["status"])

    def test_reference_is_not_verified_and_history_requires_opt_in(self):
        (self.root / "notes.md").write_text("UniqueOldTerm historical memory decision", encoding="utf-8")
        self.config["reference_files"] = [{"path": "notes.md", "scope": "reference", "status": "historical", "branch": "*"}]; self.configure()
        self.assertEqual([], self.m.search(["UniqueOldTerm"])["hits"])
        result = self.m.search(["UniqueOldTerm"], include_history=True)["hits"][0]
        self.assertEqual("historical", result["status"]); self.assertFalse(result["semantic_truth_verified_by_tool"])

    def test_missing_reference_reports_partial_coverage(self):
        self.config["reference_files"] = [{"path": "missing.md", "scope": "reference", "status": "reference", "branch": "*"}]; self.configure()
        result = self.m.search(["memory"])
        self.assertEqual("partial", result["coverage"]); self.assertTrue(result["warnings"])

    def test_pagination_and_budget(self):
        for n in range(12): self.active(self.record(f"MEM-{n:03}", subject=f"subject-{n}", summary=f"Memory item {n}"))
        ids = []; offset = 0
        while True:
            result = self.m.search(["memory"], limit=3, offset=offset, budget=2200)
            self.assertLessEqual(result["returned_characters"], 2200)
            ids += [h["id"] for h in result["hits"]]
            if result["next_offset"] is None: break
            self.assertGreater(result["next_offset"], offset); offset = result["next_offset"]
        self.assertEqual(12, len(ids)); self.assertEqual(12, len(set(ids)))

    def test_invalid_language_label_rejected(self):
        self.assert_error("invalid_record", lambda: self.m.stage(self.record(language="ru"), "stage"))

    def test_task_state_is_not_runtime_acceptance(self):
        r = self.record(kind="task_state"); r["task"] = {"task_id": "FIX-001", "baseline_head": "a"*40, "next_action": "Check the current source", "unsafe_to_repeat": ["Previous publication"], "state": "active"}
        self.active(r); result = self.m.read(r["id"])
        self.assertEqual("source", result["record"]["verification"]["level"])
        self.assertFalse(result["semantic_truth_verified_by_tool"])



    def test_historical_runtime_cannot_activate_current_claim(self):
        r = self.record()
        (self.root / "old-runtime.txt").write_text("Past observation only", encoding="utf-8")
        r["evidence"].append({"path": "old-runtime.txt", "sha256": digest((self.root / "old-runtime.txt").read_bytes()), "role": "runtime", "freshness": "historical"})
        r["verification"]["level"] = "runtime"
        (self.root / "old-runtime.txt").unlink()
        self.m.stage(r, "historical-runtime-stage")
        before = self.m.record_path("MEM-001").read_bytes()
        self.assert_error("evidence_level_mismatch", lambda: self.m.transition("MEM-001", "active", "historical-runtime-active", 1, "Cannot promote historical proof"))
        self.assertEqual(before, self.m.record_path("MEM-001").read_bytes())

    def test_historical_owner_source_is_not_current_authority(self):
        r = self.record(kind="owner_decision")
        r["original"]["kind"] = "owner_statement"
        r["verification"]["level"] = "owner_statement"
        r["evidence"].append({"path": "owner.txt", "sha256": digest((self.root / "owner.txt").read_bytes()), "role": "owner_statement", "freshness": "historical"})
        self.m.stage(r, "historical-owner-stage")
        self.assert_error("owner_evidence_required", lambda: self.m.transition("MEM-001", "active", "historical-owner-active", 1, "Historical wording is not current proof"))

    def test_legacy_active_with_wrong_current_level_is_suppressed(self):
        r = self.record()
        r["verification"]["level"] = "runtime"
        r["evidence"].append({"path": "source.txt", "sha256": digest((self.root / "source.txt").read_bytes()), "role": "runtime", "freshness": "historical"})
        # Simulate a record accepted by the old writer, without rewriting history.
        with patch.object(Memory, "_promotion_error", return_value=None):
            self.active(r)
        before = self.m.record_path("MEM-001").read_bytes()
        self.assertEqual("stale", self.m.read("MEM-001")["effective_status"])
        self.assertEqual([], self.m.search(["MEM-001"])["hits"])
        self.assertEqual("evidence_level_mismatch", self.m.audit()["findings"][0]["issues"][0]["reason"])
        self.assertEqual(before, self.m.record_path("MEM-001").read_bytes())

    def test_cli_json_utf8_under_non_utf8_locale(self):
        r = self.record()
        r["original"]["text"] = "Русский оригинал — English detail — 日本語"
        self.active(r)
        before = self.m.record_path("MEM-001").read_bytes()
        env = dict(os.environ, PYTHONIOENCODING="cp1251", PYTHONUTF8="0")
        p = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("cli.py")), "--project", str(self.root), "read", "MEM-001"], capture_output=True, env=env, timeout=20)
        self.assertEqual(0, p.returncode)
        self.assertEqual(r["original"]["text"], json.loads(p.stdout.decode("utf-8"))["record"]["original"]["text"])
        self.assertEqual(before, self.m.record_path("MEM-001").read_bytes())

    def test_cli_error_preserves_cyrillic_source_path(self):
        path = self.root / "источник.txt"
        path.write_text("Original source", encoding="utf-8")
        r = self.record()
        r["evidence"][0].update(path=path.name, sha256=digest(path.read_bytes()))
        self.m.stage(r, "cyrillic-stage")
        path.write_text("Changed source", encoding="utf-8")
        env = dict(os.environ, PYTHONIOENCODING="cp1251", PYTHONUTF8="0")
        p = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("cli.py")), "--project", str(self.root), "lifecycle", "MEM-001", "--status", "active", "--operation-id", "cyrillic-active", "--expected-revision", "1", "--reason", "Observe source change"], capture_output=True, env=env, timeout=20)
        self.assertEqual(2, p.returncode)
        result = json.loads(p.stdout.decode("utf-8"))
        self.assertEqual("stale_evidence", result["error"])
        self.assertIn(path.name, result["message"])

    def test_malformed_optional_fields_fail_before_storage(self):
        cases = [("details", [], "invalid_record"), ("not_applicable", "not-a-list", "invalid_record"), ("relationships", {}, "invalid_relationship")]
        for key, value, code in cases:
            with self.subTest(field=key):
                r = self.record(); r[key] = value
                self.assert_error(code, lambda: self.m.stage(r, "invalid-optional-" + key))
                self.assertFalse(self.m.record_path("MEM-001").exists())

    def test_bilingual_search_keys_cannot_be_empty(self):
        for language in ["ru", "en"]:
            with self.subTest(language=language):
                r = self.record(); r["search_keys"][language] = []
                self.assert_error("invalid_search_keys", lambda: self.m.stage(r, "missing-language-" + language))
                self.assertFalse(self.m.record_path("MEM-001").exists())


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.source = self.root / "source"; self.target = self.root / "target"
        self.source.mkdir(); self.target.mkdir()
        for name in PACKAGE_FILES - {"manifest.json"}: (self.source / name).write_bytes(("fixture " + name + "\n").encode())
        self.manifest()

    def manifest(self):
        (self.source / "manifest.json").write_bytes(encoded({"schema_version": 1, "package_id": "agent-authored-memory", "version": "fixture", "files": {name: digest((self.source / name).read_bytes()) for name in PACKAGE_FILES - {"manifest.json"}}}))

    def tearDown(self): self.tmp.cleanup()

    def test_preview_has_zero_target_writes(self):
        self.assertFalse(install(self.source, self.target)["applied"]); self.assertEqual([], list(self.target.iterdir()))

    def test_install_and_repeat_preserve_core_and_project_memory(self):
        (self.target / "AGENTS.md").write_bytes(b"project-owned\n")
        self.assertTrue(install(self.source, self.target, True)["applied"])
        self.assertTrue(all(r["state"] == "unchanged" for r in install(self.source, self.target, True)["rows"]))
        self.assertEqual(b"project-owned\n", (self.target / "AGENTS.md").read_bytes())
        self.assertFalse((self.target / "Project Map").exists())

    def test_local_customization_preserved_and_no_partial_update(self):
        install(self.source, self.target, True)
        target = self.target / "Agent Kit/memory/engine.py"; target.write_bytes(b"local change\n")
        (self.source / "cli.py").write_bytes(b"upstream changed\n"); self.manifest()
        result = install(self.source, self.target, True)
        self.assertFalse(result["applied"]); self.assertEqual(b"local change\n", target.read_bytes())
        self.assertEqual(b"fixture cli.py\n", (self.target / "Agent Kit/memory/cli.py").read_bytes())

    def test_manifest_tamper_rejected(self):
        (self.source / "engine.py").write_bytes(b"changed after manifest")
        with self.assertRaises(MemoryError): install(self.source, self.target, True)
        self.assertEqual([], list(self.target.iterdir()))

    def test_local_removal_preserved(self):
        install(self.source, self.target, True); (self.target / "Agent Kit/memory/cli.py").unlink()
        self.assertFalse(install(self.source, self.target, True)["applied"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
