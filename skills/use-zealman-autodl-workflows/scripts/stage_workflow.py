#!/usr/bin/env python3
"""Copy one vendor workflow to a writable location with a provenance sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = (SKILL_ROOT / "assets" / "vendor" / "zealman-autodl-v8.88").resolve()
UI_ROOT = (VENDOR_ROOT / "V9镜像内工作流").resolve()
API_ROOT = (VENDOR_ROOT / "V9面板API-json").resolve()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_source(raw_source: str) -> Path:
    supplied = Path(raw_source).expanduser()
    candidates = []
    if supplied.is_absolute():
        candidates.append(supplied)
    else:
        candidates.extend((VENDOR_ROOT / supplied, UI_ROOT / supplied, API_ROOT / supplied))

    for candidate in candidates:
        if candidate.is_file():
            source = candidate.resolve()
            break
    else:
        by_name = list(VENDOR_ROOT.rglob(supplied.name)) if supplied.name else []
        if len(by_name) == 1:
            source = by_name[0].resolve()
        elif len(by_name) > 1:
            options = "\n".join(f"  - {path.relative_to(VENDOR_ROOT)}" for path in by_name)
            raise SystemExit(f"Ambiguous workflow name; pass a relative path:\n{options}")
        else:
            raise SystemExit(f"Vendor workflow not found: {raw_source}")

    if not is_within(source, VENDOR_ROOT):
        raise SystemExit("Source must be inside the immutable vendor reference root")
    if source.suffix.casefold() != ".json":
        raise SystemExit("Source must be a JSON workflow")
    try:
        json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Source is not valid JSON: {error}") from error
    return source


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_kind(source: Path) -> str:
    if is_within(source, UI_ROOT):
        return "ui"
    if is_within(source, API_ROOT):
        return "api"
    return "unknown"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Vendor-relative path, absolute vendor path, or unique name")
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--name", help="New JSON filename; defaults to the source filename")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = resolve_source(args.source)
    output_directory = args.output_directory.expanduser().resolve()
    if is_within(output_directory, VENDOR_ROOT):
        raise SystemExit("Refusing to stage into the immutable vendor reference root")

    name = args.name or source.name
    if Path(name).name != name:
        raise SystemExit("--name must be a filename, not a path")
    if not name.casefold().endswith(".json"):
        name += ".json"

    output_directory.mkdir(parents=True, exist_ok=True)
    target = output_directory / name
    sidecar = target.with_suffix(target.suffix + ".source.json")
    if target.exists() or sidecar.exists():
        raise SystemExit(f"Refusing to overwrite an existing staged revision: {target}")

    source_hash = sha256(source)
    shutil.copy2(source, target)
    provenance = {
        "schema_version": 1,
        "status": "staged",
        "source_bundle": "zealman-autodl-v8.88-v9-snapshot",
        "source_kind": source_kind(source),
        "source_relative_path": source.relative_to(VENDOR_ROOT).as_posix(),
        "source_sha256": source_hash,
        "staged_path": str(target),
        "staged_sha256": sha256(target),
        "staged_at": datetime.now(timezone.utc).isoformat(),
        "vendor_immutable": True,
        "redistribution_review_required": True,
    }
    sidecar.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(provenance, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
