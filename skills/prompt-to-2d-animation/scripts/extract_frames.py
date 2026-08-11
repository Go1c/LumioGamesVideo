#!/usr/bin/env python3
"""Extract a fixed-canvas PNG sequence from a selected video."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image

from inspect_video import probe_video


CLIP_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SIZE_RE = re.compile(r"^([1-9][0-9]*)x([1-9][0-9]*)$")


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def parse_size(value: str) -> tuple[int, int]:
    match = SIZE_RE.fullmatch(value)
    if not match:
        raise argparse.ArgumentTypeError("size must look like 512x512")
    width, height = (int(match.group(1)), int(match.group(2)))
    if width > 2048 or height > 2048:
        raise argparse.ArgumentTypeError("v0.1 limits each canvas dimension to 2048")
    return width, height


def ensure_empty_directory(path: Path) -> None:
    if path.exists() and not path.is_dir():
        fail(f"output path is not a directory: {path}")
    if path.exists() and any(path.iterdir()):
        fail(f"refusing to write into non-empty output directory: {path}")
    path.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--fps", type=float, default=12.0)
    parser.add_argument("--size", type=parse_size, default=(512, 512))
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--max-frames", type=int, default=48)
    parser.add_argument("--chroma-key", help="FFmpeg color such as 0x00FF00")
    parser.add_argument("--similarity", type=float, default=0.16)
    parser.add_argument("--blend", type=float, default=0.04)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not CLIP_ID_RE.fullmatch(args.clip_id):
        fail("clip id must use lowercase ASCII letters, digits, and single hyphens")
    if args.fps <= 0 or args.fps > 60:
        fail("delivery FPS must be greater than 0 and no more than 60")
    if args.start < 0:
        fail("start must not be negative")
    if args.max_frames < 1 or args.max_frames > 48:
        fail("v0.1 max-frames must be between 1 and 48")
    if not 0 <= args.similarity <= 1 or not 0 <= args.blend <= 1:
        fail("similarity and blend must be between 0 and 1")
    if shutil.which("ffmpeg") is None:
        fail("ffmpeg is required but was not found on PATH")

    video = args.video.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    probe = probe_video(video)
    source_duration = probe.get("duration_seconds")
    duration = args.duration
    if duration is None:
        if source_duration is None:
            fail("source duration is unknown; pass --duration explicitly")
        duration = source_duration - args.start
    if duration <= 0:
        fail("duration must be greater than zero")
    if source_duration is not None and args.start + duration > source_duration + 0.05:
        fail("requested trim window extends past the source duration")

    expected_frames = math.ceil(duration * args.fps - 1e-9)
    if expected_frames > args.max_frames:
        fail(
            f"trim window would produce about {expected_frames} frames, exceeding "
            f"the configured maximum of {args.max_frames}"
        )

    ensure_empty_directory(output_dir)
    width, height = args.size
    filters: list[str] = []
    if args.chroma_key:
        filters.append(f"chromakey={args.chroma_key}:{args.similarity}:{args.blend}")
    filters.extend(
        [
            f"fps={args.fps}",
            f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos",
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x00000000",
            "format=rgba",
        ]
    )

    output_pattern = output_dir / f"{args.clip_id}_%04d.png"
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(video),
        "-ss",
        str(args.start),
        "-t",
        str(duration),
        "-an",
        "-vf",
        ",".join(filters),
        "-start_number",
        "0",
        "-frames:v",
        str(args.max_frames),
        str(output_pattern),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "unknown ffmpeg error"
        fail(f"ffmpeg frame extraction failed: {detail}")

    frames = sorted(output_dir.glob(f"{args.clip_id}_[0-9][0-9][0-9][0-9].png"))
    if not frames:
        fail("ffmpeg completed without producing any frames")
    if len(frames) > args.max_frames:
        fail("extractor produced more frames than the configured maximum")

    alpha_min = 255
    alpha_max = 0
    for frame in frames:
        with Image.open(frame) as image:
            rgba = image.convert("RGBA")
            if rgba.size != (width, height):
                fail(f"unexpected frame size for {frame.name}: {rgba.size}")
            extrema = rgba.getchannel("A").getextrema()
            alpha_min = min(alpha_min, extrema[0])
            alpha_max = max(alpha_max, extrema[1])

    if args.chroma_key and alpha_min == 255:
        fail("chroma key produced no transparent pixels; choose a better key or matte method")

    metadata = {
        "schema_version": "0.1.0",
        "source": probe,
        "clip_id": args.clip_id,
        "trim_start_seconds": args.start,
        "trim_duration_seconds": duration,
        "delivery_fps": args.fps,
        "width": width,
        "height": height,
        "frame_count": len(frames),
        "chroma_key": args.chroma_key,
        "has_transparent_pixels": alpha_min < 255,
        "has_visible_pixels": alpha_max > 0,
        "files": [frame.name for frame in frames],
    }
    (output_dir / "extraction.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
