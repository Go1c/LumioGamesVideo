from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "prompt-to-2d-animation"
SCRIPTS = SKILL_ROOT / "scripts"


def run_script(name: str, *args: object, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
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


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="lumio-pipeline-")
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_rgba_frames(self, directory: Path, clip_id: str, count: int = 12) -> None:
        directory.mkdir(parents=True)
        for index in range(count):
            image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            x = 22 + (index % 3) - 1
            draw.rectangle((x, 24, x + 18, 58), fill=(230, 40, 40, 255))
            image.save(directory / f"{clip_id}_{index:04d}.png")

    def test_job_validator_accepts_example(self) -> None:
        example = SKILL_ROOT / "assets" / "animation-job.example.json"
        run_script("validate_job.py", example)

    def test_job_validator_rejects_over_budget_frames(self) -> None:
        source = json.loads(
            (SKILL_ROOT / "assets" / "animation-job.example.json").read_text(encoding="utf-8")
        )
        source["video"]["trim_duration_seconds"] = 4
        source["sequence"]["delivery_fps"] = 24
        bad_job = self.root / "bad-job.json"
        bad_job.write_text(json.dumps(source), encoding="utf-8")
        completed = run_script("validate_job.py", bad_job, expect_success=False)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("exceeding max_frames", completed.stdout)

    def test_frames_to_spine_package(self) -> None:
        raw = self.root / "raw"
        cleaned = self.root / "cleaned"
        package = self.root / "package"
        self.make_rgba_frames(raw, "hero-idle")

        run_script(
            "stabilize_sequence.py",
            raw,
            cleaned,
            "--clip-id",
            "hero-idle",
            "--mode",
            "alpha-bottom-center",
        )
        run_script(
            "build_spine_flipbook.py",
            cleaned,
            package,
            "--clip-id",
            "hero-idle",
            "--fps",
            12,
            "--loop",
            "--spine-version",
            "4.1",
            "--max-page-size",
            256,
        )
        run_script("validate_package.py", package)

        manifest = json.loads((package / "sequence-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["animation_kind"], "flipbook")
        self.assertEqual(manifest["frame_count"], 12)
        self.assertTrue(manifest["loop"])
        self.assertEqual(len(manifest["atlas_pages"]), 2)
        atlas = json.loads((package / "atlas.json").read_text(encoding="utf-8"))
        first_region = atlas["pages"][0]["regions"][0]
        with Image.open(package / atlas["pages"][0]["file"]) as page:
            sample = page.convert("RGBA").getpixel(
                (first_region["x"] + 32, first_region["y"] + 40)
            )
        self.assertGreater(sample[0], 200)
        self.assertEqual(sample[3], 255)
        spine = json.loads((package / "hero-idle.json").read_text(encoding="utf-8"))
        sequence = spine["skins"][0]["attachments"]["sprite"]["hero-idle"]["sequence"]
        self.assertEqual(sequence["count"], 12)
        timeline = spine["animations"]["hero-idle"]["attachments"]["default"]["sprite"]["hero-idle"]["sequence"]
        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[1]["mode"], "hold")
        self.assertAlmostEqual(timeline[1]["time"], 1.0)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_video_inspect_and_chroma_extract(self) -> None:
        source_frames = self.root / "source-frames"
        source_frames.mkdir()
        for index in range(12):
            image = Image.new("RGB", (64, 64), (0, 255, 0))
            draw = ImageDraw.Draw(image)
            draw.rectangle((20 + index // 4, 22, 40 + index // 4, 58), fill=(230, 30, 30))
            image.save(source_frames / f"source_{index:04d}.png")
        video = self.root / "source.mkv"
        encode = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-framerate",
                "12",
                "-i",
                str(source_frames / "source_%04d.png"),
                "-c:v",
                "ffv1",
                str(video),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(encode.returncode, 0, encode.stderr)

        inspected = run_script("inspect_video.py", video)
        metadata = json.loads(inspected.stdout)
        self.assertEqual(metadata["width"], 64)
        self.assertAlmostEqual(metadata["source_fps"], 12)

        extracted = self.root / "extracted"
        run_script(
            "extract_frames.py",
            video,
            extracted,
            "--clip-id",
            "test-action",
            "--fps",
            12,
            "--size",
            "64x64",
            "--duration",
            1,
            "--chroma-key",
            "0x00FF00",
            "--similarity",
            0.25,
            "--blend",
            0.02,
        )
        extraction = json.loads((extracted / "extraction.json").read_text(encoding="utf-8"))
        self.assertEqual(extraction["frame_count"], 12)
        self.assertTrue(extraction["has_transparent_pixels"])


if __name__ == "__main__":
    unittest.main()
