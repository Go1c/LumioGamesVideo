from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "use-zealman-autodl-workflows"
VENDOR_ROOT = SKILL_ROOT / "assets" / "vendor" / "zealman-autodl-v8.88"
SCRIPTS = SKILL_ROOT / "scripts"


def run_script(
    name: str, *args: object, expect_success: bool = True
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        check=False,
    )
    if expect_success and completed.returncode != 0:
        raise AssertionError(
            f"{name} failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ZealmanWorkflowSkillTests(unittest.TestCase):
    def test_canonical_vendor_snapshot_is_complete_and_data_only(self) -> None:
        ui_paths = sorted((VENDOR_ROOT / "V9镜像内工作流").rglob("*.json"))
        api_paths = sorted((VENDOR_ROOT / "V9面板API-json").glob("*.json"))
        guide_paths = sorted((VENDOR_ROOT / "工作流说明").glob("*.md"))
        self.assertEqual(len(ui_paths), 259)
        self.assertEqual(len(api_paths), 29)
        self.assertEqual(len(guide_paths), 22)

        allowed_suffixes = {".html", ".json", ".md", ".txt"}
        all_files = [path for path in VENDOR_ROOT.rglob("*") if path.is_file()]
        self.assertEqual(len(all_files), 316)
        self.assertFalse(
            {path.suffix.casefold() for path in all_files} - allowed_suffixes
        )
        for path in ui_paths + api_paths:
            with self.subTest(path=path.relative_to(VENDOR_ROOT)):
                self.assertIsInstance(
                    json.loads(path.read_text(encoding="utf-8")), dict
                )

    def test_search_handles_english_intent_aliases(self) -> None:
        completed = run_script(
            "find_workflows.py",
            "--query",
            "motion transfer",
            "--kind",
            "api",
            "--json",
        )
        report = json.loads(completed.stdout)
        self.assertGreater(report["count"], 0)
        self.assertTrue(
            any(result["name"].startswith("P07-") for result in report["results"])
        )

    def test_inspector_distinguishes_api_and_ui_json(self) -> None:
        api_path = (
            VENDOR_ROOT
            / "V9面板API-json"
            / "G01-图生视频-Wan2.2万相基础版.json"
        )
        api_report = json.loads(
            run_script("inspect_workflow.py", api_path, "--json").stdout
        )
        self.assertEqual(api_report["format"], "api")
        self.assertTrue(
            any(
                parameter["parameter"] == "119:text"
                for parameter in api_report["enabled_parameters"]
            )
        )

        ui_path = (
            VENDOR_ROOT
            / "V9镜像内工作流"
            / "G视频-Wan图生"
            / "G01-图生视频-Wan2.2万相基础版.json"
        )
        ui_report = json.loads(
            run_script("inspect_workflow.py", ui_path, "--json").stdout
        )
        self.assertEqual(ui_report["format"], "ui")
        self.assertGreater(ui_report["link_count"], 0)

    def test_staging_preserves_source_and_refuses_overwrite(self) -> None:
        source = (
            VENDOR_ROOT
            / "V9面板API-json"
            / "P07-动作迁移-Wan2.2AnimateV4.json"
        )
        with tempfile.TemporaryDirectory(prefix="zealman-stage-") as temp:
            output = Path(temp)
            completed = run_script(
                "stage_workflow.py",
                source,
                output,
                "--name",
                "lumio-motion-test.json",
            )
            report = json.loads(completed.stdout)
            target = output / "lumio-motion-test.json"
            sidecar = output / "lumio-motion-test.json.source.json"
            self.assertTrue(target.is_file())
            self.assertTrue(sidecar.is_file())
            self.assertEqual(sha256(source), sha256(target))
            self.assertEqual(report["source_kind"], "api")
            self.assertEqual(report["source_sha256"], sha256(source))

            repeated = run_script(
                "stage_workflow.py",
                source,
                output,
                "--name",
                "lumio-motion-test.json",
                expect_success=False,
            )
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn("Refusing to overwrite", repeated.stderr)


if __name__ == "__main__":
    unittest.main()
