#!/usr/bin/env python3
"""Build an engine-neutral atlas and Spine 4.1+ sequence package from RGBA PNGs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


CLIP_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
VERSION_RE = re.compile(r"^([0-9]+)\.([0-9]+)$")
BUILDER_VERSION = "0.1.0"


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def ensure_empty_directory(path: Path) -> None:
    if path.exists() and not path.is_dir():
        fail(f"output path is not a directory: {path}")
    if path.exists() and any(path.iterdir()):
        fail(f"refusing to write into non-empty output directory: {path}")
    path.mkdir(parents=True, exist_ok=True)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def choose_grid(count: int, cell_width: int, cell_height: int, max_size: int) -> tuple[int, int]:
    max_cols = max_size // cell_width
    max_rows = max_size // cell_height
    if max_cols < 1 or max_rows < 1:
        fail("one frame plus padding exceeds the maximum atlas page size")
    best: tuple[float, int, int] | None = None
    for cols in range(1, min(max_cols, count) + 1):
        rows = math.ceil(count / cols)
        if rows > max_rows:
            continue
        page_width = cols * cell_width
        page_height = rows * cell_height
        score = (max(page_width, page_height), page_width * page_height, cols)
        if best is None or score < (best[0], best[1], best[2]):
            best = (score[0], score[1], cols)
    if best is None:
        fail("frames cannot fit on an atlas page with the configured maximum size")
    cols = best[2]
    return cols, math.ceil(count / cols)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frames_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--fps", type=float, default=12.0)
    behavior = parser.add_mutually_exclusive_group(required=True)
    behavior.add_argument("--loop", action="store_true")
    behavior.add_argument("--once", action="store_true")
    parser.add_argument("--spine-version", default="4.1")
    parser.add_argument("--pivot", choices=("bottom-center", "center"), default="bottom-center")
    parser.add_argument("--max-page-size", type=int, default=4096)
    parser.add_argument("--padding", type=int, default=2)
    parser.add_argument("--allow-opaque", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not CLIP_ID_RE.fullmatch(args.clip_id):
        fail("clip id must use lowercase ASCII letters, digits, and single hyphens")
    version_match = VERSION_RE.fullmatch(args.spine_version)
    if not version_match:
        fail("Spine version must be a major.minor value such as 4.1")
    version_tuple = (int(version_match.group(1)), int(version_match.group(2)))
    if version_tuple not in {(4, 1), (4, 2), (4, 3)}:
        fail("v0.1 supports the Spine sequence profile for versions 4.1, 4.2, and 4.3")
    if args.fps <= 0 or args.fps > 60:
        fail("FPS must be greater than 0 and no more than 60")
    if args.max_page_size < 64 or args.max_page_size > 16384:
        fail("max page size must be between 64 and 16384")
    if args.padding < 0 or args.padding > 32:
        fail("padding must be between 0 and 32")

    frames_dir = args.frames_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    pattern = re.compile(rf"^{re.escape(args.clip_id)}_([0-9]{{4}})\.png$")
    frames: list[tuple[int, Path]] = []
    for path in frames_dir.iterdir() if frames_dir.is_dir() else []:
        match = pattern.fullmatch(path.name)
        if match:
            frames.append((int(match.group(1)), path))
    frames.sort()
    if not frames:
        fail(f"no frames named {args.clip_id}_0000.png and onward were found")
    if len(frames) > 48:
        fail("v0.1 packages at most 48 frames per clip")
    expected_indices = list(range(len(frames)))
    actual_indices = [index for index, _ in frames]
    if actual_indices != expected_indices:
        fail(f"frame indices must be consecutive from 0000; found {actual_indices}")

    frame_size: tuple[int, int] | None = None
    has_transparency = False
    frame_hashes: list[dict[str, str]] = []
    for _, path in frames:
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            if frame_size is None:
                frame_size = rgba.size
            elif rgba.size != frame_size:
                fail(f"frame dimensions differ: {path.name} is {rgba.size}, expected {frame_size}")
            if rgba.getchannel("A").getextrema()[0] < 255:
                has_transparency = True
        frame_hashes.append({"file": path.name, "sha256": file_sha256(path)})
    if not has_transparency and not args.allow_opaque:
        fail("frames contain no transparency; provide a reliable matte or pass --allow-opaque")

    width, height = frame_size or (0, 0)
    pivot_x = width / 2
    pivot_y = height if args.pivot == "bottom-center" else height / 2
    cell_width = width + args.padding * 2
    cell_height = height + args.padding * 2
    max_per_page = (args.max_page_size // cell_width) * (args.max_page_size // cell_height)
    if max_per_page < 1:
        fail("a frame cannot fit in the configured atlas page size")

    ensure_empty_directory(output_dir)
    packaged_frames_dir = output_dir / "frames"
    packaged_frames_dir.mkdir()
    for _, path in frames:
        shutil.copy2(path, packaged_frames_dir / path.name)

    pages: list[dict[str, object]] = []
    atlas_lines: list[str] = []
    atlas_cursor = 0
    page_index = 0
    while atlas_cursor < len(frames):
        chunk = frames[atlas_cursor : atlas_cursor + max_per_page]
        cols, rows = choose_grid(len(chunk), cell_width, cell_height, args.max_page_size)
        page_width = cols * cell_width
        page_height = rows * cell_height
        page_name = f"{args.clip_id}-{page_index}.png"
        page_image = Image.new("RGBA", (page_width, page_height), (0, 0, 0, 0))
        regions: list[dict[str, object]] = []

        atlas_lines.extend(
            [
                page_name,
                f"\tsize: {page_width}, {page_height}",
                "\tformat: RGBA8888",
                "\tfilter: Linear, Linear",
                "\trepeat: none",
                "\tpma: false",
            ]
        )

        for local_index, (global_index, frame_path) in enumerate(chunk):
            col = local_index % cols
            row = local_index // cols
            x = col * cell_width + args.padding
            y = row * cell_height + args.padding
            with Image.open(frame_path) as image:
                page_image.alpha_composite(image.convert("RGBA"), dest=(x, y))
            region_name = f"{args.clip_id}_{global_index:04d}"
            region = {
                "name": region_name,
                "frame_index": global_index,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
            }
            regions.append(region)
            atlas_lines.extend(
                [
                    region_name,
                    f"\tindex: {global_index}",
                    "\trotate: false",
                    f"\tbounds: {x}, {y}, {width}, {height}",
                    f"\toffsets: 0, 0, {width}, {height}",
                ]
            )

        page_image.save(output_dir / page_name, format="PNG")
        pages.append(
            {
                "file": page_name,
                "width": page_width,
                "height": page_height,
                "region_count": len(regions),
                "regions": regions,
            }
        )
        atlas_cursor += len(chunk)
        page_index += 1
        if atlas_cursor < len(frames):
            atlas_lines.append("")

    atlas_path = output_dir / f"{args.clip_id}.atlas"
    atlas_path.write_text("\n".join(atlas_lines) + "\n", encoding="utf-8")
    (output_dir / "atlas.json").write_text(
        json.dumps({"schema_version": "0.1.0", "pages": pages}, indent=2) + "\n",
        encoding="utf-8",
    )

    delay = 1.0 / args.fps
    clip_duration = len(frames) / args.fps
    sequence_mode = "loop" if args.loop else "once"
    attachment_x = width / 2 - pivot_x
    attachment_y = pivot_y - height / 2
    skeleton = {
        "skeleton": {
            "spine": f"{args.spine_version}.00",
            "x": -pivot_x,
            "y": -(height - pivot_y),
            "width": width,
            "height": height,
            "fps": args.fps,
            "images": "./",
        },
        "bones": [{"name": "root"}],
        "slots": [{"name": "sprite", "bone": "root", "attachment": args.clip_id}],
        "skins": [
            {
                "name": "default",
                "attachments": {
                    "sprite": {
                        args.clip_id: {
                            "type": "region",
                            "path": f"{args.clip_id}_",
                            "x": attachment_x,
                            "y": attachment_y,
                            "width": width,
                            "height": height,
                            "sequence": {
                                "count": len(frames),
                                "start": 0,
                                "digits": 4,
                                "setup": 0,
                            },
                        }
                    }
                },
            }
        ],
        "animations": {
            args.clip_id: {
                "attachments": {
                    "default": {
                        "sprite": {
                            args.clip_id: {
                                "sequence": [
                                    {
                                        "time": 0,
                                        "mode": sequence_mode,
                                        "index": 0,
                                        "delay": delay,
                                    },
                                    {
                                        "time": clip_duration,
                                        "mode": "hold",
                                        "index": 0 if args.loop else len(frames) - 1,
                                        "delay": delay,
                                    },
                                ]
                            }
                        }
                    }
                }
            }
        },
    }
    skeleton_path = output_dir / f"{args.clip_id}.json"
    skeleton_path.write_text(json.dumps(skeleton, indent=2) + "\n", encoding="utf-8")

    manifest_frames = [
        {
            "index": index,
            "file": f"frames/{path.name}",
            "region": f"{args.clip_id}_{index:04d}",
            "duration_seconds": delay,
        }
        for index, path in frames
    ]
    manifest = {
        "schema_version": "0.1.0",
        "clip_id": args.clip_id,
        "animation_kind": "flipbook",
        "width": width,
        "height": height,
        "fps": args.fps,
        "duration_seconds": clip_duration,
        "loop": args.loop,
        "alpha": has_transparency,
        "pivot": {"x": pivot_x, "y": pivot_y},
        "frame_count": len(frames),
        "frames": manifest_frames,
        "atlas_pages": [
            {
                "file": page["file"],
                "width": page["width"],
                "height": page["height"],
                "region_count": page["region_count"],
            }
            for page in pages
        ],
        "approx_rgba_bytes": width * height * 4 * len(frames),
    }
    (output_dir / "sequence-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    provenance = {
        "schema_version": "0.1.0",
        "builder": "build_spine_flipbook.py",
        "builder_version": BUILDER_VERSION,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "spine_target_version": args.spine_version,
        "source_frames": frame_hashes,
        "options": {
            "fps": args.fps,
            "loop": args.loop,
            "pivot": args.pivot,
            "max_page_size": args.max_page_size,
            "padding": args.padding,
        },
    }
    (output_dir / "provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    qa = {
        "schema_version": "0.1.0",
        "status": "data-passed-visual-pending",
        "data_checks": {
            "consecutive_frames": True,
            "identical_dimensions": True,
            "atlas_built": True,
            "spine_sequence_built": True,
            "animation_kind": "flipbook",
        },
        "visual_checks": [],
    }
    (output_dir / "qa-report.json").write_text(
        json.dumps(qa, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
