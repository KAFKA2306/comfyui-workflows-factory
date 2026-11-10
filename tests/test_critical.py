"""実害の大きい事故だけを防ぐ最小回帰テスト。

対象: 正本の検証と復旧、競合統合、選定時の出典保持、
公開判定・重複送信防止、制作物の改ざん・意図しないディレクトリ書き込み。
仕様の細部や実装手順を追認するテストは置かない。
"""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gwp.discovery import record_file
from gwp.ledger import put
from gwp.production import handoff_job
from gwp.registry import load_registry, validate_registry
from gwp.state import (
    atomic_save, backup, empty_catalog, health, load_catalog, main as state_main,
    merge_catalog, restore,
)


class CriticalSafetyTests(unittest.TestCase):
    def test_verify_backup_restore_reject_missing_checksum(self):
        with tempfile.TemporaryDirectory() as root:
            source = Path(root) / "source.json"
            target = Path(root) / "target.json"
            atomic_save(source, empty_catalog())
            source.with_name(source.name + ".sha256").unlink()
            # 旧版移行の読み込みは許すが、検証・復旧の正本には使わない。
            self.assertEqual(load_catalog(source)["artifacts"], {})
            with self.assertRaisesRegex(ValueError, "SHA-256検証ファイル"):
                state_main(["verify", "--catalog", str(source)])
            with self.assertRaisesRegex(ValueError, "SHA-256検証ファイル"):
                backup(source, Path(root) / "backups")
            with self.assertRaisesRegex(ValueError, "SHA-256検証ファイル"):
                restore(target, source)

    def test_atomic_update_backup_corruption_restore(self):
        with tempfile.TemporaryDirectory() as root:
            file = Path(root) / "registry.json"
            original = empty_catalog()
            original["artifacts"]["id-a"] = {"id": "id-a", "revisions": []}
            atomic_save(file, original)
            changed = load_catalog(file)
            changed["artifacts"]["id-b"] = {"id": "id-b", "revisions": []}
            atomic_save(file, changed)
            backup = Path(str(file) + ".bak")
            self.assertTrue(backup.exists())
            self.assertEqual(len(load_catalog(backup)["artifacts"]), 1)
            file.write_bytes(b'{"broken"')
            with self.assertRaises(ValueError):
                load_catalog(file)
            # 破損した本体を上書きできないなら、まず破損を隔離して復旧する。
            corrupt = file.with_suffix(".corrupt")
            file.rename(corrupt)
            Path(str(file) + ".sha256").unlink()
            restore(file, backup)
            self.assertEqual(set(load_catalog(file)["artifacts"]), {"id-a"})

    def test_multi_machine_merge_keeps_origins_revisions_and_counts(self):
        a, b = empty_catalog(), empty_catalog()
        record_file(a, "alice/workflows", "1" * 40,
                    {"path": "x.json", "sha": "a" * 40}, "2026-11-01")
        record_file(b, "alice/workflows", "2" * 40,
                    {"path": "x.json", "sha": "b" * 40}, "2026-11-02")
        record_file(b, "bob/workflows", "3" * 40,
                    {"path": "y.json", "sha": "b" * 40}, "2026-11-02")
        merged = merge_catalog(a, b)
        self.assertEqual(len(merged["artifacts"]), 2)
        item = merged["artifacts"]["github:alice/workflows:x.json"]
        self.assertEqual(item["blob_sha"], "b" * 40)
        self.assertEqual(len(item["revisions"]), 2)
        self.assertEqual(len(merged["content_index"]["b" * 40]), 2)
        self.assertEqual(health(merged, a)["status"], "ok")

    def test_handoff_without_repository_registration_checks_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output"
            output.mkdir()
            (output / "001-1.png").write_bytes(b"image-bytes")
            manifest = output / "manifest.json"
            manifest.write_text(json.dumps({
                "target": "new-project", "promptId": "id-1", "state": "GENERATED_UNVERIFIED",
                "files": [{"file": "001-1.png",
                           "sha256": hashlib.sha256(b"image-bytes").hexdigest()}]
            }), encoding="utf-8")
            project = root / "project"
            project.mkdir()
            result = handoff_job(manifest, project)
            destination = Path(result["destination"])
            self.assertEqual(destination, project / ".artifacts/comfyui/new-project/id-1")
            self.assertEqual((destination / "001-1.png").read_bytes(), b"image-bytes")
            with self.assertRaises(FileExistsError):
                handoff_job(manifest, project)
            (output / "001-1.png").write_bytes(b"tampered")
            second = root / "another-project"
            second.mkdir()
            with self.assertRaises(ValueError):
                handoff_job(manifest, second)

    def test_handoff_rejects_symlink_redirect_outside_project(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output"
            output.mkdir()
            raw = b"verified-workflow-output"
            (output / "001-1.png").write_bytes(raw)
            manifest = output / "manifest.json"
            manifest.write_text(json.dumps({
                "target": "youtube", "promptId": "job-1", "state": "GENERATED_UNVERIFIED",
                "files": [{"file": "001-1.png", "sha256": hashlib.sha256(raw).hexdigest()}],
            }), encoding="utf-8")
            project = root / "project"
            project.mkdir()
            outside = root / "outside"
            outside.mkdir()
            try:
                (project / ".artifacts").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symbolic links are unavailable: {exc}")
            with self.assertRaises(ValueError):
                handoff_job(manifest, project)
            self.assertEqual(list(outside.iterdir()), [])

    def test_publication_requires_verifiable_claim(self):
        c = empty_catalog()
        base = {"project_id": "cafe", "platform": "VRChat",
                "state": "verified", "url": "https://vrchat.com/home/world/wrld_1"}
        with self.assertRaises(ValueError):
            put(c, "publications", "world", base)
        ready = {**base, "verified_at": "2026-11-03T00:00:00Z",
                 "verification_method": "公開ページをブラウザで確認",
                 "evidence_urls": ["https://vrchat.com/home/world/wrld_1"]}
        self.assertIsNotNone(put(c, "publications", "world", ready))

    def test_job_uses_same_client_id_and_valid_transition(self):
        c = empty_catalog()
        job = {"state": "planned", "target": "cafe", "client_id": "fixed-request",
               "workflow_sha256": "a" * 64}
        put(c, "jobs", "job1", job)
        with self.assertRaises(ValueError):
            put(c, "jobs", "job1", {**job, "state": "succeeded"},
                change_kind="correction")
        put(c, "jobs", "job1", {**job, "state": "submission_unknown"},
            change_kind="correction")
        with self.assertRaises(ValueError):
            put(c, "jobs", "job1", {**job, "client_id": "new"},
                change_kind="correction")

    def test_report_does_not_merge_different_content_with_same_nodes(self):
        from gwp.evaluate import report

        catalog = empty_catalog()
        for repo, blob in [("example/first", "1" * 40), ("example/second", "2" * 40)]:
            name = "3d/same-nodes.json"
            record_file(catalog, repo, "a" * 40, {
                "path": name, "sha": blob, "size": 100,
            }, "2026-11-01T00:00:00Z")
            row = catalog["artifacts"]["github:" + repo + ":" + name]
            row.update({"inspection": "complete", "format": "workflow-ui",
                        "node_types": ["LoadImage", "SaveGLB"],
                        "model_references": ["same-model"], "mission_ids": ["3d-models"]})
        before = json.dumps(catalog, sort_keys=True)
        evaluated = report(catalog, load_registry(), now=datetime(2026, 11, 4, tzinfo=timezone.utc))
        # Existing registry workflows also contribute independent source rows.
        self.assertEqual(evaluated["groups"], evaluated["candidates"])
        self.assertEqual(len([row for row in evaluated["ranked"]
                              if row["id"].startswith("github:example/")]), 2)
        self.assertEqual(json.dumps(catalog, sort_keys=True), before)

        # Identical blob contents may be grouped, but both provenance IDs survive.
        rows = list(catalog["artifacts"].values())
        rows[1]["blob_sha"] = rows[0]["blob_sha"]
        grouped = report(catalog, load_registry(), now=datetime(2026, 11, 4, tzinfo=timezone.utc))
        self.assertEqual(grouped["groups"], grouped["candidates"] - 1)
        merged = [row for row in grouped["ranked"]
                  if row["id"].startswith("github:example/")]
        self.assertEqual(len(merged), 1)
        self.assertEqual(len(merged[0]["similar_candidates"]), 1)

    def test_pipeline_inputs_and_references(self):
        data = load_registry()
        self.assertIn("codex-imagegen-source", {row["id"] for row in data["pipelines"]})
        broken = copy.deepcopy(data)
        broken["pipelines"][0]["steps"][1]["requires"].append("missing.mp4")
        with self.assertRaisesRegex(ValueError, "未生成の入力"):
            validate_registry(broken)
        broken = copy.deepcopy(data)
        broken["projects"]["broken"] = {
            "title": "制作", "tags": ["映像"], "mission_ids": ["video"],
            "primary_mission_id": "video", "pipeline_ids": ["unknown"]
        }
        with self.assertRaisesRegex(ValueError, "制作パイプライン"):
            validate_registry(broken)


    def test_domain_reclassification_preserves_sources_and_separates_delivery(self):
        from gwp.evaluate import report
        from gwp.select import candidates, MISSION_CATEGORIES

        registry = load_registry()
        domains = set(registry["missions"])
        self.assertEqual(domains, set(MISSION_CATEGORIES))
        self.assertEqual(domains, {
            "vrchat-world", "avatars", "3d-models", "illustration",
            "video", "audio", "games", "tabletop",
        })
        self.assertFalse({"booth", "youtube", "podcast", "movies"} & domains)
        for row in registry["workflows"] + registry["pipelines"]:
            self.assertTrue(set(row["mission_ids"]) <= domains)
            self.assertTrue(set(row["media_types"]) <= set(registry["media_types"]))
            self.assertTrue(set(row["delivery_targets"]) <= set(registry["delivery_targets"]))
        # BOOTHの過去データは販売先であり、イラストへ自動誤分類しない。
        historic = empty_catalog()
        record_file(historic, "example/archive", "a" * 40,
                    {"path": "legacy/no-hints.json", "sha": "b" * 40}, "2026-11-01")
        entry_id = "github:example/archive:legacy/no-hints.json"
        historic["artifacts"][entry_id]["mission_ids"] = ["booth", "youtube"]
        video_ids = {item["id"] for item in candidates(historic, registry, "video")}
        image_ids = {item["id"] for item in candidates(historic, registry, "illustration")}
        self.assertIn(entry_id, video_ids)
        self.assertNotIn(entry_id, image_ids)
        selection = report(historic, registry, now=datetime(2026, 11, 10, tzinfo=timezone.utc))
        self.assertEqual(set(selection["assignments"]), domains)
        self.assertEqual(selection["candidates"], len(historic["artifacts"]) + len(registry["workflows"]))
        self.assertEqual(historic["artifacts"][entry_id]["mission_ids"], ["booth", "youtube"])
        broken = copy.deepcopy(registry)
        broken["workflows"][0]["media_types"] = ["unknown"]
        with self.assertRaisesRegex(ValueError, "制作媒体"):
            validate_registry(broken)
        broken = copy.deepcopy(registry)
        broken["projects"]["invalid"] = {
            "title": "不整合", "tags": ["作品"], "mission_ids": ["audio"],
            "primary_mission_id": "video",
        }
        with self.assertRaisesRegex(ValueError, "主制作領域"):
            validate_registry(broken)


if __name__ == "__main__":
    unittest.main()
