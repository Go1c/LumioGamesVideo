#!/usr/bin/env python3
"""Normalize a PNG sequence and optionally stabilize it by alpha bounds."""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

from PIL import Image


CLIP_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def ensure_empty_directory(path: Path) -> None:
    if path.exists() and not path.is_dir():
        fail(f"output path is not a directory: {path}")
    if path.exists() and any(path.iterdir()):
        fail(f"refusing to write into non-empty output directory: {path}")
    path.mkdir(parents=True, exist_ok=True)


def alpha_bbox(image: Image.Image, threshold: int) -> tuple[int, int, int, int] | None:
    alpha = image.getchannel("A").point(lambda value: 255 if value >= threshold else 0)
    return alpha.getbbox()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument(
        "--mode",
        choices=("none", "alpha-bottom-center", "alpha-center"),
        default="none",
    )
    parser.add_argument("--alpha-threshold", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not CLIP_ID_RE.fullmatch(args.clip_id):
        fail("clip id must use lowercase ASCII letters, digits, and single hyphens")
    if not 1 <= args.alpha_threshold <= 255:
        fail("alpha threshold must be between 1 and 255")

    input_dir = args.input_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    frames = sorted(input_dir.glob(f"{args.clip_id}_[0-9][0-9][0-9][0-9].png"))
    if not frames:
        fail(f"no sequence frames found in {input_dir}")
    ensure_empty_directory(output_dir)

    loaded: list[tuple[Path, Image.Image, tuple[int, int, int, int]]] = []
    expected_size: tuple[int, int] | None = None
    anchors: list[tuple[float, float]] = []
    for frame in frames:
        image = Image.open(frame).convert("RGBA")
        if expected_size is None:
            expected_size = image.size
        elif image.size != expected_size:
            fail(f"frame dimensions differ: {frame.name} is {image.size}, expected {expected_size}")
        bbox = alpha_bbox(image, args.alpha_threshold)
        if bbox is None:
            fail(f"frame contains no visible alpha pixels: {frame.name}")
        left, top, right, bottom = bbox
        if args.mode == "alpha-center":
            anchor = ((left + right) / 2, (top + bottom) / 2)
        else:
            anchor = ((left + right) / 2, float(bottom))
        anchors.append(anchor)
        loaded.append((frame, image, bbox))

    target_x = statistics.median(anchor[0] for anchor in anchors)
    target_y = statistics.median(anchor[1] for anchor in anchors)
    shifts: list[dict[str, object]] = []
    width, height = expected_size or (0, 0)

    for index, ((frame, image, bbox), anchor) in enumerate(zip(loaded, anchors)):
        if args.mode == "none":
            dx = dy = 0
        else:
            dx = round(target_x - anchor[0])
            dy = round(target_y - anchor[1])
        left, top, right, bottom = bbox
        if left + dx < 0 or top + dy < 0 or right + dx > width or bottom + dy > height:
            fail(f"stabilization would crop visible pixels in {frame.name}; use --mode none")

        canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        canvas.alpha_composite(image, dest=(dx, dy))
        output_name = f"{args.clip_id}_{index:04d}.png"
        canvas.save(output_dir / output_name, format="PNG")
        shifts.append({"file": output_name, "dx": dx, "dy": dy})
        image.close()

    report = {
        "schema_version": "0.1.0",
        "clip_id": args.clip_id,
        "mode": args.mode,
        "width": width,
        "height": height,
        "frame_count": len(frames),
        "target_anchor": {"x": target_x, "y": target_y},
        "max_abs_shift": max(max(abs(item["dx"]), abs(item["dy"])) for item in shifts),
        "shifts": shifts,
    }
    (output_dir / "stabilization.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
