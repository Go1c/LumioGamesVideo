#!/usr/bin/env python3
"""Inspect a video and compare its first and last displayed frames."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        fail(completed.stderr.strip() or f"command failed: {command[0]}")
    return completed


def parse_rate(value: Any) -> float | None:
    if not isinstance(value, str) or value in {"", "0/0"}:
        return None
    try:
        rate = float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None
    return rate if math.isfinite(rate) and rate > 0 else None


def extract_frame(video: Path, timestamp: float, output: Path) -> None:
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.9f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-y",
            str(output),
        ]
    )


def image_metrics(first_path: Path, last_path: Path) -> dict[str, float]:
    with Image.open(first_path) as first_image, Image.open(last_path) as last_image:
        first = first_image.convert("RGB")
        last = last_image.convert("RGB")
        if first.size != last.size:
            fail("sampled frame dimensions do not match")
        difference = ImageChops.difference(first, last)
        histogram = difference.histogram()
        samples = first.width * first.height * 3
        absolute_sum = sum((index % 256) * count for index, count in enumerate(histogram))
        square_sum = sum((index % 256) ** 2 * count for index, count in enumerate(histogram))
        mae = absolute_sum / samples
        rms = math.sqrt(square_sum / samples)
        return {
            "mean_absolute_rgb_difference": mae,
            "normalized_mean_absolute_difference": mae / 255.0,
            "root_mean_square_rgb_difference": rms,
        }


def inspect(video: Path) -> dict[str, Any]:
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        fail("ffmpeg and ffprobe are required")
    probe = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(video),
        ]
    )
    payload = json.loads(probe.stdout)
    streams = payload.get("streams", [])
    video_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "video"), None
    )
    if not isinstance(video_stream, dict):
        fail("input has no video stream")
    format_data = payload.get("format", {})
    raw_duration = video_stream.get("duration") or format_data.get("duration")
    try:
        duration = float(raw_duration)
    except (TypeError, ValueError):
        fail("unable to determine video duration")
    if not math.isfinite(duration) or duration <= 0:
        fail("video duration must be positive")
    fps = parse_rate(video_stream.get("avg_frame_rate")) or parse_rate(
        video_stream.get("r_frame_rate")
    )
    if fps is None:
        fail("unable to determine video frame rate")
    last_timestamp = max(0.0, duration - 1.0 / fps)
    with tempfile.TemporaryDirectory(prefix="lumio-loop-analysis-") as temp:
        root = Path(temp)
        first_path = root / "first.png"
        last_path = root / "last.png"
        extract_frame(video, 0.0, first_path)
        extract_frame(video, last_timestamp, last_path)
        metrics = image_metrics(first_path, last_path)
    size_bytes = video.stat().st_size
    return {
        "file": str(video),
        "duration_seconds": duration,
        "fps": fps,
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "video_codec": video_stream.get("codec_name"),
        "has_audio": any(stream.get("codec_type") == "audio" for stream in streams),
        "file_size_bytes": size_bytes,
        "average_megabits_per_second": size_bytes * 8 / duration / 1_000_000,
        "first_sample_seconds": 0.0,
        "last_sample_seconds": last_timestamp,
        "seam_metrics": metrics,
        "interpretation": "Comparison signal only; review at least three cycles visually and audit audio.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    video = args.video.expanduser().resolve()
    if not video.is_file():
        fail(f"video does not exist: {video}")
    result = inspect(video)
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        seam = result["seam_metrics"]
        print(f"duration: {result['duration_seconds']:.3f}s")
        print(f"fps: {result['fps']:.3f}")
        print(f"normalized seam difference: {seam['normalized_mean_absolute_difference']:.6f}")
        print(result["interpretation"])


if __name__ == "__main__":
    main()
