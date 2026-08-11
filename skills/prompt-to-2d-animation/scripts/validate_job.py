#!/usr/bin/env python3
"""Validate an animation job, including constraints JSON Schema cannot express."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


JOB_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
RECIPES = {"character-idle-loop", "character-emote", "character-action"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate(job: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(job, dict):
        return ["job must contain a JSON object"]
    required = {
        "schema_version",
        "job_id",
        "recipe",
        "prompt",
        "reference_image",
        "anchor_policy",
        "video",
        "sequence",
        "spine",
        "render_policy",
    }
    missing = sorted(required - set(job))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    unknown = sorted(set(job) - required)
    if unknown:
        errors.append(f"unknown top-level fields: {', '.join(unknown)}")
    if job.get("schema_version") != "0.1.0":
        errors.append("schema_version must be 0.1.0")
    job_id = job.get("job_id")
    if not isinstance(job_id, str) or not JOB_ID_RE.fullmatch(job_id):
        errors.append("job_id must use lowercase ASCII letters, digits, and single hyphens")
    recipe = job.get("recipe")
    if recipe not in RECIPES:
        errors.append("recipe is not supported by v0.1")
    if not isinstance(job.get("prompt"), str) or not job.get("prompt", "").strip():
        errors.append("prompt must be a non-empty string")

    reference = job.get("reference_image")
    anchor_policy = job.get("anchor_policy")
    if reference is not None and not isinstance(reference, str):
        errors.append("reference_image must be a string or null")
    if anchor_policy not in {"use-reference", "generate-and-approve", "not-required"}:
        errors.append("anchor_policy is invalid")
    if anchor_policy == "use-reference" and not reference:
        errors.append("anchor_policy use-reference requires reference_image")

    video = job.get("video")
    sequence = job.get("sequence")
    spine = job.get("spine")
    render_policy = job.get("render_policy")
    if not isinstance(video, dict):
        errors.append("video must be an object")
        video = {}
    if not isinstance(sequence, dict):
        errors.append("sequence must be an object")
        sequence = {}
    if not isinstance(spine, dict):
        errors.append("spine must be an object")
        spine = {}
    if not isinstance(render_policy, dict):
        errors.append("render_policy must be an object")
        render_policy = {}

    duration = video.get("duration_seconds")
    trim_start = video.get("trim_start_seconds")
    trim_duration = video.get("trim_duration_seconds")
    source_fps = video.get("source_fps")
    for label, value in (
        ("video.duration_seconds", duration),
        ("video.trim_duration_seconds", trim_duration),
        ("video.source_fps", source_fps),
    ):
        if not number(value) or value <= 0:
            errors.append(f"{label} must be a finite positive number")
    if not number(trim_start) or trim_start < 0:
        errors.append("video.trim_start_seconds must be a finite non-negative number")
    if number(duration) and number(trim_start) and number(trim_duration):
        if trim_start + trim_duration > duration + 1e-9:
            errors.append("video trim window extends past duration_seconds")
    if video.get("fixed_camera") is not True:
        errors.append("video.fixed_camera must be true in v0.1")
    if video.get("background") not in {"flat-contrast", "transparent", "segmentation-required"}:
        errors.append("video.background is invalid")

    delivery_fps = sequence.get("delivery_fps")
    max_frames = sequence.get("max_frames")
    if not number(delivery_fps) or delivery_fps <= 0 or delivery_fps > 60:
        errors.append("sequence.delivery_fps must be greater than 0 and no more than 60")
    if not isinstance(max_frames, int) or isinstance(max_frames, bool) or not 1 <= max_frames <= 48:
        errors.append("sequence.max_frames must be an integer from 1 to 48")
    if number(trim_duration) and number(delivery_fps) and isinstance(max_frames, int):
        estimated_frames = math.ceil(trim_duration * delivery_fps - 1e-9)
        if estimated_frames > max_frames:
            errors.append(
                f"trim window would produce about {estimated_frames} frames, exceeding max_frames"
            )
    canvas = sequence.get("canvas")
    if not (
        isinstance(canvas, list)
        and len(canvas) == 2
        and all(isinstance(value, int) and not isinstance(value, bool) and 64 <= value <= 2048 for value in canvas)
    ):
        errors.append("sequence.canvas must contain two integers from 64 to 2048")
    if not isinstance(sequence.get("alpha"), bool):
        errors.append("sequence.alpha must be boolean")
    if sequence.get("pivot") not in {"bottom-center", "center"}:
        errors.append("sequence.pivot is invalid")
    if not isinstance(sequence.get("loop"), bool):
        errors.append("sequence.loop must be boolean")
    if recipe == "character-idle-loop" and sequence.get("loop") is not True:
        errors.append("character-idle-loop requires sequence.loop true")

    enabled = spine.get("enabled")
    target_version = spine.get("target_version")
    profile = spine.get("profile")
    if not isinstance(enabled, bool):
        errors.append("spine.enabled must be boolean")
    if enabled:
        match = re.fullmatch(r"([0-9]+)\.([0-9]+)", str(target_version))
        supported = match is not None and (int(match.group(1)), int(match.group(2))) in {
            (4, 1),
            (4, 2),
            (4, 3),
        }
        if not supported:
            errors.append("v0.1 Spine output requires target_version 4.1, 4.2, or 4.3")
        if profile != "sequence-attachment":
            errors.append("enabled Spine output requires profile sequence-attachment")
    elif target_version is not None or profile is not None:
        errors.append("disabled Spine output requires null target_version and profile")

    variants = render_policy.get("max_video_variants")
    if not isinstance(variants, int) or isinstance(variants, bool) or not 1 <= variants <= 8:
        errors.append("render_policy.max_video_variants must be an integer from 1 to 8")
    if not isinstance(render_policy.get("remote_upload_approved"), bool):
        errors.append("render_policy.remote_upload_approved must be boolean")
    return errors


def main() -> None:
    args = parse_args()
    path = args.job.expanduser().resolve()
    try:
        job = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"job does not exist: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"job is not valid JSON: {exc}")
    errors = validate(job)
    result = {"valid": not errors, "errors": errors}
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print("Animation job is valid." if not errors else "Animation job is invalid.")
        for error in errors:
            print(f"error: {error}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
