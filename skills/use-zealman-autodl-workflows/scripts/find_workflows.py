#!/usr/bin/env python3
"""Search the canonical Zealman UI and panel-API workflow snapshots."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = SKILL_ROOT / "assets" / "vendor" / "zealman-autodl-v8.88"
WORKFLOW_ROOTS = {
    "ui": VENDOR_ROOT / "V9镜像内工作流",
    "api": VENDOR_ROOT / "V9面板API-json",
}

ALIASES = {
    "text to image": ("文生图",),
    "text-to-image": ("文生图",),
    "t2i": ("文生图",),
    "image edit": ("图像编辑", "编辑", "洗图"),
    "image-to-image": ("图像编辑", "编辑", "洗图"),
    "i2i": ("图像编辑", "编辑", "洗图"),
    "image to video": ("图生视频",),
    "image-to-video": ("图生视频",),
    "i2v": ("图生视频",),
    "text to video": ("文生视频",),
    "text-to-video": ("文生视频",),
    "t2v": ("文生视频",),
    "first last frame": ("首尾帧",),
    "first-last-frame": ("首尾帧",),
    "storyboard": ("分镜", "宫格"),
    "lip sync": ("对口型", "数字人"),
    "lip-sync": ("对口型", "数字人"),
    "voice clone": ("声音克隆", "音频克隆"),
    "voice-clone": ("声音克隆", "音频克隆"),
    "motion transfer": ("动作迁移", "姿态迁移"),
    "motion-transfer": ("动作迁移", "姿态迁移"),
    "character replacement": ("人物替换", "角色替换"),
    "character-replacement": ("人物替换", "角色替换"),
    "upscale": ("放大", "超分", "修复"),
    "watermark": ("去水印",),
}

STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "the",
    "to",
    "workflow",
    "workflows",
    "工作流",
}


def search_terms(query: str) -> list[str]:
    normalized = query.casefold().strip()
    terms: list[str] = []
    for alias, expansions in ALIASES.items():
        if alias in normalized:
            terms.extend(expansions)

    raw_terms = [
        part
        for part in re.split(r"[\s,，/|]+", normalized)
        if part and part not in STOP_WORDS
    ]
    terms.extend(raw_terms)

    unique: list[str] = []
    for term in terms:
        folded = term.casefold()
        if folded not in unique:
            unique.append(folded)
    return unique


def workflow_rows(kind: str) -> list[dict[str, str]]:
    kinds = WORKFLOW_ROOTS if kind == "all" else {kind: WORKFLOW_ROOTS[kind]}
    rows: list[dict[str, str]] = []
    for row_kind, root in kinds.items():
        for path in sorted(root.rglob("*.json")):
            relative = path.relative_to(VENDOR_ROOT)
            category = path.parent.name if row_kind == "ui" else "panel-api"
            rows.append(
                {
                    "kind": row_kind,
                    "path": relative.as_posix(),
                    "name": path.name,
                    "category": category,
                }
            )
    return rows


def score_row(row: dict[str, str], terms: list[str]) -> int:
    if not terms:
        return 1
    haystack = f"{row['path']} {row['category']} {row['name']}".casefold()
    stem = Path(row["name"]).stem.casefold()
    score = 0
    for term in terms:
        if term in haystack:
            score += 10
        if stem.startswith(term):
            score += 5
    return score


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="", help="Intent, model, prefix, or filename text")
    parser.add_argument("--kind", choices=("all", "ui", "api"), default="all")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    terms = search_terms(args.query)
    scored = [
        (score_row(row, terms), row)
        for row in workflow_rows(args.kind)
    ]
    matches = [
        {"score": score, **row}
        for score, row in sorted(
            scored,
            key=lambda item: (-item[0], item[1]["kind"], item[1]["path"]),
        )
        if score > 0
    ][: args.limit]

    if args.as_json:
        print(
            json.dumps(
                {
                    "query": args.query,
                    "terms": terms,
                    "kind": args.kind,
                    "count": len(matches),
                    "results": matches,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not matches:
        print("No matching workflows. Try a model name, workflow prefix, or Chinese intent term.")
        return 0

    for match in matches:
        print(f"[{match['kind']}] {match['path']} (score={match['score']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
