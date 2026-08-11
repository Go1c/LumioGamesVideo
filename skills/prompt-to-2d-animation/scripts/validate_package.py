#!/usr/bin/env python3
"""Validate a generated Lumio flipbook and Spine sequence package."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

from PIL import Image


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing file: {path.name}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path.name} must contain a JSON object")
        return None
    return value


def nested(value: Any, *keys: str) -> Any:
    current = value
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def validate(package_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest = load_json(package_dir / "sequence-manifest.json", errors)
    atlas = load_json(package_dir / "atlas.json", errors)
    load_json(package_dir / "provenance.json", errors)
    load_json(package_dir / "qa-report.json", errors)
    if manifest is None or atlas is None:
        return {"valid": False, "errors": errors, "warnings": warnings}

    clip_id = manifest.get("clip_id")
    if not isinstance(clip_id, str) or not clip_id:
        errors.append("sequence manifest has no valid clip_id")
        return {"valid": False, "errors": errors, "warnings": warnings}
    if manifest.get("animation_kind") != "flipbook":
        errors.append("animation_kind must be flipbook")

    frames = manifest.get("frames")
    frame_count = manifest.get("frame_count")
    width = manifest.get("width")
    height = manifest.get("height")
    fps = manifest.get("fps")
    if not isinstance(frames, list) or not frames:
        errors.append("sequence manifest must list at least one frame")
        frames = []
    if frame_count != len(frames):
        errors.append("frame_count does not match frames length")
    if not isinstance(frame_count, int) or not 1 <= frame_count <= 48:
        errors.append("frame_count must be between 1 and 48")
    if not isinstance(width, int) or not isinstance(height, int) or width < 1 or height < 1:
        errors.append("manifest dimensions must be positive integers")
    if not isinstance(fps, (int, float)) or fps <= 0:
        errors.append("manifest FPS must be positive")

    expected_regions: list[str] = []
    for expected_index, frame in enumerate(frames):
        if not isinstance(frame, dict):
            errors.append(f"frame entry {expected_index} is not an object")
            continue
        if frame.get("index") != expected_index:
            errors.append(f"frame entry {expected_index} has the wrong index")
        region = frame.get("region")
        expected_region = f"{clip_id}_{expected_index:04d}"
        if region != expected_region:
            errors.append(f"frame {expected_index} region should be {expected_region}")
        expected_regions.append(expected_region)
        raw_file = frame.get("file")
        if not isinstance(raw_file, str):
            errors.append(f"frame {expected_index} has no file")
            continue
        frame_path = package_dir / raw_file
        if not frame_path.is_file():
            errors.append(f"missing frame file: {raw_file}")
            continue
        try:
            with Image.open(frame_path) as image:
                if image.size != (width, height):
                    errors.append(f"frame {raw_file} dimensions do not match the manifest")
                if image.convert("RGBA").getchannel("A").getextrema()[0] == 255:
                    warnings.append(f"frame {raw_file} has no transparent pixels")
        except OSError as exc:
            errors.append(f"unable to read frame {raw_file}: {exc}")

    pages = atlas.get("pages")
    found_regions: list[str] = []
    if not isinstance(pages, list) or not pages:
        errors.append("atlas.json must list at least one page")
        pages = []
    for page in pages:
        if not isinstance(page, dict):
            errors.append("atlas page entry is not an object")
            continue
        page_file = page.get("file")
        page_path = package_dir / page_file if isinstance(page_file, str) else None
        if page_path is None or not page_path.is_file():
            errors.append(f"missing atlas page: {page_file}")
            continue
        try:
            with Image.open(page_path) as image:
                if image.size != (page.get("width"), page.get("height")):
                    errors.append(f"atlas page dimensions disagree for {page_file}")
        except OSError as exc:
            errors.append(f"unable to read atlas page {page_file}: {exc}")
        regions = page.get("regions")
        if not isinstance(regions, list):
            errors.append(f"atlas page {page_file} has no regions")
            continue
        if page.get("region_count") != len(regions):
            errors.append(f"atlas page {page_file} region_count is wrong")
        for region in regions:
            if not isinstance(region, dict):
                errors.append(f"atlas page {page_file} contains a bad region entry")
                continue
            name = region.get("name")
            if isinstance(name, str):
                found_regions.append(name)
            bounds = [region.get(key) for key in ("x", "y", "width", "height")]
            if not all(isinstance(value, int) for value in bounds):
                errors.append(f"atlas region {name} has invalid bounds")
                continue
            x, y, region_width, region_height = bounds
            if x < 0 or y < 0 or x + region_width > page.get("width", 0) or y + region_height > page.get("height", 0):
                errors.append(f"atlas region {name} is outside page bounds")
    if sorted(found_regions) != sorted(expected_regions):
        errors.append("atlas regions do not match the sequence frame regions")

    spine_path = package_dir / f"{clip_id}.json"
    spine = load_json(spine_path, errors)
    atlas_text_path = package_dir / f"{clip_id}.atlas"
    if not atlas_text_path.is_file():
        errors.append(f"missing Spine atlas: {atlas_text_path.name}")
        atlas_text = ""
    else:
        atlas_text = atlas_text_path.read_text(encoding="utf-8")
    for region in expected_regions:
        if re.search(rf"(?m)^{re.escape(region)}$", atlas_text) is None:
            errors.append(f"Spine atlas does not declare region {region}")

    if spine is not None:
        version = nested(spine, "skeleton", "spine")
        version_match = re.match(r"^([0-9]+)\.([0-9]+)", str(version))
        supported_version = version_match is not None and (
            int(version_match.group(1)),
            int(version_match.group(2)),
        ) in {(4, 1), (4, 2), (4, 3)}
        if not supported_version:
            errors.append("Spine skeleton must target supported version 4.1, 4.2, or 4.3")
        attachment = nested(
            spine,
            "skins",
        )
        try:
            attachment_data = spine["skins"][0]["attachments"]["sprite"][clip_id]
            sequence = attachment_data["sequence"]
            if sequence.get("count") != frame_count:
                errors.append("Spine sequence count does not match frame_count")
            if sequence.get("start") != 0 or sequence.get("digits") != 4:
                errors.append("Spine sequence naming must start at 0 with four digits")
            timeline_entries = spine["animations"][clip_id]["attachments"]["default"]["sprite"][clip_id]["sequence"]
            if not isinstance(timeline_entries, list) or len(timeline_entries) != 2:
                errors.append("Spine sequence timeline must contain start and terminal hold keys")
                timeline_entries = [{}, {}]
            timeline = timeline_entries[0]
            terminal = timeline_entries[1]
            expected_mode = "loop" if manifest.get("loop") else "once"
            if timeline.get("mode") != expected_mode:
                errors.append("Spine sequence mode does not match manifest loop behavior")
            if isinstance(fps, (int, float)) and not math.isclose(timeline.get("delay", -1), 1 / fps, rel_tol=1e-9):
                errors.append("Spine sequence delay does not equal 1 / FPS")
            if terminal.get("mode") != "hold":
                errors.append("Spine sequence terminal key must use hold mode")
            if not math.isclose(
                terminal.get("time", -1), manifest.get("duration_seconds", -2), rel_tol=1e-9
            ):
                errors.append("Spine sequence terminal key does not define the clip duration")
            expected_terminal_index = 0 if manifest.get("loop") else frame_count - 1
            if terminal.get("index") != expected_terminal_index:
                errors.append("Spine sequence terminal frame index is incorrect")
        except (KeyError, IndexError, TypeError, AttributeError):
            errors.append("Spine sequence attachment/timeline structure is incomplete")

    expected_rgba = width * height * 4 * frame_count if all(
        isinstance(value, int) for value in (width, height, frame_count)
    ) else None
    if expected_rgba is not None and manifest.get("approx_rgba_bytes") != expected_rgba:
        errors.append("approx_rgba_bytes is incorrect")

    return {
        "valid": not errors,
        "clip_id": clip_id,
        "frame_count": frame_count,
        "atlas_pages": len(pages),
        "errors": errors,
        "warnings": sorted(set(warnings)),
    }


def main() -> None:
    args = parse_args()
    package_dir = args.package_dir.expanduser().resolve()
    result = validate(package_dir)
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print("Package validation passed." if result["valid"] else "Package validation failed.")
        for warning in result["warnings"]:
            print(f"warning: {warning}")
        for error in result["errors"]:
            print(f"error: {error}")
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
