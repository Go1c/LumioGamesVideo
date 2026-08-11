#!/usr/bin/env python3
"""Validate a provider-neutral Lumio game-video job."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
RATIO_RE = re.compile(r"^[1-9][0-9]*:[1-9][0-9]*$")
RESOLUTION_RE = re.compile(r"^[1-9][0-9]{2,4}x[1-9][0-9]{2,4}$")
WORKFLOWS = {
    "cinematic",
    "character-performance",
    "menu-motion",
    "in-game-loop",
    "gameplay-previs",
    "marketing",
    "2d-animation",
}
MODES = {
    "text-to-video",
    "image-to-video",
    "first-frame-to-video",
    "first-last-frame-to-video",
    "reference-to-video",
    "video-to-video",
}
KINDS = {
    "cinematic-master",
    "localized-clips",
    "menu-background",
    "video-texture",
    "previs-comparison",
    "marketing-cuts",
    "frame-package",
}
EXPECTED_KIND = {
    "cinematic": "cinematic-master",
    "character-performance": "localized-clips",
    "menu-motion": "menu-background",
    "in-game-loop": "video-texture",
    "gameplay-previs": "previs-comparison",
    "marketing": "marketing-cuts",
    "2d-animation": "frame-package",
}
REQUIRED_QA = {
    "cinematic": {"continuity", "action", "camera"},
    "character-performance": {"identity", "action", "audio"},
    "menu-motion": {"continuity", "camera", "text"},
    "in-game-loop": {"continuity", "text", "seam"},
    "gameplay-previs": {"camera", "truthful-claims"},
    "marketing": {"text", "truthful-claims"},
    "2d-animation": {"identity", "action", "alpha", "runtime"},
}
ASSET_TYPES = {"image", "video", "audio", "text", "ui", "gameplay"}
RIGHTS = {"owned", "licensed", "consented", "unknown"}
QA_CHECKS = {
    "identity",
    "continuity",
    "action",
    "camera",
    "text",
    "audio",
    "seam",
    "truthful-claims",
    "alpha",
    "runtime",
}
CONTAINERS = {"mp4", "mov", "webm", "png-sequence", "sprite-atlas", "spine-json"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_keys(
    value: Any,
    label: str,
    required: set[str],
    allowed: set[str],
    errors: list[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - allowed)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
    return value


def validate(job: Any) -> list[str]:
    errors: list[str] = []
    top = {
        "schema_version",
        "job_id",
        "workflow",
        "goal",
        "inputs",
        "generation",
        "delivery",
        "rights",
        "qa_checks",
    }
    job = check_keys(job, "job", top, top, errors)
    if job.get("schema_version") != "0.1.0":
        errors.append("schema_version must be 0.1.0")
    job_id = job.get("job_id")
    if not isinstance(job_id, str) or not ID_RE.fullmatch(job_id):
        errors.append("job_id must use lowercase ASCII letters, digits, and single hyphens")
    workflow = job.get("workflow")
    if workflow not in WORKFLOWS:
        errors.append("workflow is unsupported")
    if not isinstance(job.get("goal"), str) or not job.get("goal", "").strip():
        errors.append("goal must be a non-empty string")

    inputs = check_keys(job.get("inputs"), "inputs", {"assets"}, {"assets"}, errors)
    assets = inputs.get("assets")
    if not isinstance(assets, list) or len(assets) > 24:
        errors.append("inputs.assets must be an array with at most 24 entries")
        assets = []
    asset_ids: set[str] = set()
    counts = {kind: 0 for kind in ASSET_TYPES}
    for index, raw_asset in enumerate(assets):
        label = f"inputs.assets[{index}]"
        fields = {
            "id",
            "type",
            "source",
            "role",
            "rights_status",
            "remote_upload_approved",
        }
        asset = check_keys(raw_asset, label, fields, fields, errors)
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not ID_RE.fullmatch(asset_id):
            errors.append(f"{label}.id is invalid")
        elif asset_id in asset_ids:
            errors.append(f"{label}.id is duplicated")
        else:
            asset_ids.add(asset_id)
        asset_type = asset.get("type")
        if asset_type not in ASSET_TYPES:
            errors.append(f"{label}.type is invalid")
        else:
            counts[asset_type] += 1
        for field in ("source", "role"):
            if not isinstance(asset.get(field), str) or not asset.get(field, "").strip():
                errors.append(f"{label}.{field} must be a non-empty string")
        if asset.get("rights_status") not in RIGHTS:
            errors.append(f"{label}.rights_status is invalid")
        if not isinstance(asset.get("remote_upload_approved"), bool):
            errors.append(f"{label}.remote_upload_approved must be boolean")

    generation_fields = {
        "provider",
        "model",
        "mode",
        "duration_seconds",
        "aspect_ratio",
        "resolution",
        "audio",
        "variants",
        "execution",
        "provider_terms_approved",
        "paid_generation",
        "paid_generation_approved",
    }
    generation = check_keys(
        job.get("generation"), "generation", generation_fields, generation_fields, errors
    )
    for field in ("provider", "model"):
        if generation.get(field) is not None and not isinstance(generation.get(field), str):
            errors.append(f"generation.{field} must be a string or null")
    mode = generation.get("mode")
    if mode not in MODES:
        errors.append("generation.mode is invalid")
    duration = generation.get("duration_seconds")
    if not finite_number(duration) or not 0 < duration <= 60:
        errors.append("generation.duration_seconds must be greater than 0 and no more than 60")
    if not isinstance(generation.get("aspect_ratio"), str) or not RATIO_RE.fullmatch(
        generation.get("aspect_ratio", "")
    ):
        errors.append("generation.aspect_ratio must look like 16:9")
    if not isinstance(generation.get("resolution"), str) or not RESOLUTION_RE.fullmatch(
        generation.get("resolution", "")
    ):
        errors.append("generation.resolution must look like 1280x720")
    if not isinstance(generation.get("audio"), bool):
        errors.append("generation.audio must be boolean")
    variants = generation.get("variants")
    if not isinstance(variants, int) or isinstance(variants, bool) or not 1 <= variants <= 12:
        errors.append("generation.variants must be an integer from 1 to 12")
    execution = generation.get("execution")
    if execution not in {"plan-only", "local", "remote"}:
        errors.append("generation.execution is invalid")
    for field in ("provider_terms_approved", "paid_generation", "paid_generation_approved"):
        if not isinstance(generation.get(field), bool):
            errors.append(f"generation.{field} must be boolean")
    if execution in {"local", "remote"}:
        if not generation.get("provider") or not generation.get("model"):
            errors.append("render execution requires provider and model")
        if generation.get("provider_terms_approved") is not True:
            errors.append("render execution requires provider_terms_approved true")
    if execution == "remote":
        unapproved = [
            asset.get("id", f"asset-{index}")
            for index, asset in enumerate(assets)
            if isinstance(asset, dict) and asset.get("remote_upload_approved") is not True
        ]
        if unapproved:
            errors.append(f"remote execution has unapproved uploads: {', '.join(unapproved)}")
    if generation.get("paid_generation") is True and execution != "plan-only":
        if generation.get("paid_generation_approved") is not True:
            errors.append("paid render execution requires paid_generation_approved true")

    if mode in {"image-to-video", "first-frame-to-video"} and counts["image"] < 1:
        errors.append(f"{mode} requires at least one image asset")
    if mode == "first-last-frame-to-video" and counts["image"] < 2:
        errors.append("first-last-frame-to-video requires at least two image asset entries")
    if mode == "reference-to-video" and not assets:
        errors.append("reference-to-video requires at least one reference asset")
    if mode == "video-to-video" and counts["video"] + counts["gameplay"] < 1:
        errors.append("video-to-video requires a video or gameplay asset")

    delivery_fields = {"kind", "loop", "fps", "containers"}
    delivery = check_keys(
        job.get("delivery"), "delivery", delivery_fields, delivery_fields, errors
    )
    kind = delivery.get("kind")
    if kind not in KINDS:
        errors.append("delivery.kind is invalid")
    if workflow in EXPECTED_KIND and kind != EXPECTED_KIND[workflow]:
        errors.append(f"workflow {workflow} requires delivery.kind {EXPECTED_KIND[workflow]}")
    if not isinstance(delivery.get("loop"), bool):
        errors.append("delivery.loop must be boolean")
    if workflow == "in-game-loop" and delivery.get("loop") is not True:
        errors.append("in-game-loop requires delivery.loop true")
    fps = delivery.get("fps")
    if not finite_number(fps) or not 0 < fps <= 120:
        errors.append("delivery.fps must be greater than 0 and no more than 120")
    containers = delivery.get("containers")
    if not isinstance(containers, list) or not containers:
        errors.append("delivery.containers must be a non-empty array")
    else:
        if len(containers) != len(set(map(str, containers))):
            errors.append("delivery.containers must not contain duplicates")
        invalid = sorted({str(item) for item in containers if item not in CONTAINERS})
        if invalid:
            errors.append(f"delivery.containers contains invalid values: {', '.join(invalid)}")

    rights_fields = {"public_release", "ai_disclosure_decision", "notes"}
    rights = check_keys(job.get("rights"), "rights", rights_fields, rights_fields, errors)
    if not isinstance(rights.get("public_release"), bool):
        errors.append("rights.public_release must be boolean")
    if rights.get("ai_disclosure_decision") not in {"pending", "required", "not-required"}:
        errors.append("rights.ai_disclosure_decision is invalid")
    if not isinstance(rights.get("notes"), str):
        errors.append("rights.notes must be a string")

    qa_checks = job.get("qa_checks")
    if not isinstance(qa_checks, list) or not qa_checks:
        errors.append("qa_checks must be a non-empty array")
        qa_set: set[str] = set()
    else:
        qa_set = {str(item) for item in qa_checks}
        if len(qa_checks) != len(qa_set):
            errors.append("qa_checks must not contain duplicates")
        invalid_qa = sorted(qa_set - QA_CHECKS)
        if invalid_qa:
            errors.append(f"qa_checks contains invalid values: {', '.join(invalid_qa)}")
    if workflow in REQUIRED_QA:
        missing_qa = sorted(REQUIRED_QA[workflow] - qa_set)
        if missing_qa:
            errors.append(f"workflow {workflow} requires QA checks: {', '.join(missing_qa)}")
    if execution != "plan-only":
        unknown_assets = [
            asset.get("id", f"asset-{index}")
            for index, asset in enumerate(assets)
            if isinstance(asset, dict) and asset.get("rights_status") == "unknown"
        ]
        if unknown_assets:
            errors.append(f"render execution has assets with unknown rights: {', '.join(unknown_assets)}")
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
        print("Game video job is valid." if not errors else "Game video job is invalid.")
        for error in errors:
            print(f"error: {error}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
