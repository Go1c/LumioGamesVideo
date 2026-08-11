#!/usr/bin/env python3
"""Inspect the first video stream with ffprobe and emit normalized JSON."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ALPHA_PIXEL_FORMAT_PREFIXES = ("rgba", "argb", "bgra", "abgr", "gbrap", "yuva", "ya")


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def parse_rate(value: str | None) -> float | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None


def probe_video(path: Path) -> dict[str, Any]:
    if shutil.which("ffprobe") is None:
        fail("ffprobe is required but was not found on PATH")
    if not path.is_file():
        fail(f"video does not exist: {path}")

    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,nb_frames,duration:format=duration",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "unknown ffprobe error"
        fail(f"ffprobe failed: {detail}")

    try:
        payload = json.loads(completed.stdout)
        stream = payload["streams"][0]
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        fail(f"ffprobe did not return a usable video stream: {exc}")

    fps = parse_rate(stream.get("avg_frame_rate")) or parse_rate(stream.get("r_frame_rate"))
    duration_raw = stream.get("duration") or payload.get("format", {}).get("duration")
    try:
        duration = float(duration_raw) if duration_raw is not None else None
    except (TypeError, ValueError):
        duration = None

    frame_count_raw = stream.get("nb_frames")
    frame_count: int | None
    try:
        frame_count = int(frame_count_raw) if frame_count_raw not in {None, "N/A"} else None
    except (TypeError, ValueError):
        frame_count = None
    if frame_count is None and duration is not None and fps is not None:
        frame_count = round(duration * fps)

    pix_fmt = str(stream.get("pix_fmt") or "unknown")
    return {
        "schema_version": "0.1.0",
        "file": path.name,
        "codec": stream.get("codec_name"),
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "pixel_format": pix_fmt,
        "has_declared_alpha": pix_fmt.startswith(ALPHA_PIXEL_FORMAT_PREFIXES),
        "source_fps": fps,
        "duration_seconds": duration,
        "frame_count": frame_count,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--output", type=Path, help="Write JSON to a new file instead of stdout")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = probe_video(args.video.expanduser().resolve())
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output.expanduser().resolve()
        if output.exists():
            fail(f"refusing to overwrite existing output: {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
    else:
        sys.stdout.write(encoded)


if __name__ == "__main__":
    main()
