from __future__ import annotations

import json
import copy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_SKILL = REPO_ROOT / "skills" / "write-game-video-prompt"
LOOP_SKILL = REPO_ROOT / "skills" / "create-in-game-loop-media"


def run_python(
    script: Path, *args: object, expect_success: bool = True
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, str(script), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        check=False,
    )
    if expect_success and completed.returncode != 0:
        raise AssertionError(
            f"{script.name} failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


class GameVideoSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="lumio-game-video-")
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_generic_job_validator_accepts_all_examples(self) -> None:
        examples = [
            PROMPT_SKILL / "assets" / "game-video-job.example.json",
            *(PROMPT_SKILL / "assets" / "examples").glob("*.json"),
        ]
        self.assertEqual(len(examples), 8)
        for example in examples:
            with self.subTest(example=example.name):
                run_python(PROMPT_SKILL / "scripts" / "validate_job.py", example)

    def test_generic_job_validator_rejects_unapproved_remote_upload(self) -> None:
        job = json.loads(
            (PROMPT_SKILL / "assets" / "game-video-job.example.json").read_text(
                encoding="utf-8"
            )
        )
        job["generation"]["provider"] = "example-provider"
        job["generation"]["model"] = "example-video-model"
        job["generation"]["execution"] = "remote"
        job["generation"]["provider_terms_approved"] = True
        path = self.root / "remote-job.json"
        path.write_text(json.dumps(job), encoding="utf-8")
        completed = run_python(
            PROMPT_SKILL / "scripts" / "validate_job.py",
            path,
            expect_success=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("unapproved uploads", completed.stdout)

    def test_generic_job_validator_rejects_cross_field_errors(self) -> None:
        base = json.loads(
            (PROMPT_SKILL / "assets" / "game-video-job.example.json").read_text(
                encoding="utf-8"
            )
        )
        cases = []

        missing_endpoint = copy.deepcopy(base)
        missing_endpoint["inputs"]["assets"] = missing_endpoint["inputs"]["assets"][:1]
        cases.append(("endpoint", missing_endpoint, "requires at least two image"))

        unapproved_paid = copy.deepcopy(base)
        unapproved_paid["generation"].update(
            {
                "provider": "local-provider",
                "model": "local-model",
                "execution": "local",
                "provider_terms_approved": True,
                "paid_generation": True,
                "paid_generation_approved": False,
            }
        )
        cases.append(("paid", unapproved_paid, "paid_generation_approved true"))

        unknown_rights = copy.deepcopy(base)
        unknown_rights["generation"].update(
            {
                "provider": "local-provider",
                "model": "local-model",
                "execution": "local",
                "provider_terms_approved": True,
            }
        )
        unknown_rights["inputs"]["assets"][0]["rights_status"] = "unknown"
        cases.append(("rights", unknown_rights, "assets with unknown rights"))

        wrong_delivery = copy.deepcopy(base)
        wrong_delivery["delivery"]["kind"] = "marketing-cuts"
        cases.append(("delivery", wrong_delivery, "requires delivery.kind video-texture"))

        missing_qa = copy.deepcopy(base)
        missing_qa["qa_checks"].remove("seam")
        cases.append(("qa", missing_qa, "requires QA checks: seam"))

        for label, job, expected in cases:
            with self.subTest(case=label):
                path = self.root / f"{label}.json"
                path.write_text(json.dumps(job), encoding="utf-8")
                completed = run_python(
                    PROMPT_SKILL / "scripts" / "validate_job.py",
                    path,
                    expect_success=False,
                )
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stdout)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_loop_analyzer_compares_first_and_last_displayed_frames(self) -> None:
        frames = self.root / "frames"
        frames.mkdir()
        for index in range(12):
            image = Image.new("RGB", (64, 36), (8, 10, 18))
            if index not in {0, 11}:
                draw = ImageDraw.Draw(image)
                draw.rectangle((8 + index, 10, 26 + index, 28), fill=(220, 30, 90))
            image.save(frames / f"loop_{index:04d}.png")
        video = self.root / "loop.mkv"
        encoded = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-framerate",
                "12",
                "-i",
                str(frames / "loop_%04d.png"),
                "-c:v",
                "ffv1",
                str(video),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(encoded.returncode, 0, encoded.stderr)
        analyzed = run_python(
            LOOP_SKILL / "scripts" / "analyze_loop.py", video, "--json"
        )
        report = json.loads(analyzed.stdout)
        self.assertAlmostEqual(report["duration_seconds"], 1.0, places=3)
        self.assertFalse(report["has_audio"])
        self.assertLess(
            report["seam_metrics"]["normalized_mean_absolute_difference"], 0.001
        )


if __name__ == "__main__":
    unittest.main()
