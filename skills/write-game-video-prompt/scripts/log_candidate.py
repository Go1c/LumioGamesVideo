#!/usr/bin/env python3
"""Maintain a Gate 4 candidate decision log for a game-video job.

Subcommands:
  init    create an empty decision-log.json for a validated job
  add     record one generated or failed candidate with its outputs
  reject  mark a candidate rejected with a mandatory reason
  select  mark a generated candidate as selected
  show    print a summary or the raw JSON

The log format is defined by assets/decision-log.schema.json and is shared
with adapter runners such as use-zealman-autodl-workflows/scripts/run_workflow.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
OUTPUT_TYPE_BY_SUFFIX = {
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
    ".gif": "image",
    ".mp4": "video",
    ".mov": "video",
    ".webm": "video",
    ".wav": "audio",
    ".mp3": "audio",
    ".flac": "audio",
    ".txt": "text",
    ".srt": "text",
}


def fail(message: str) -> "NoReturn":  # noqa: F821 - runtime string annotation
    raise SystemExit(f"error: {message}")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_log(path: Path) -> dict[str, Any]:
    try:
        log = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"decision log does not exist: {path} (run init first)")
    except json.JSONDecodeError as error:
        fail(f"decision log is not valid JSON: {error}")
    if not isinstance(log, dict) or not isinstance(log.get("candidates"), list):
        fail("decision log must be an object with a candidates array")
    return log


def write_log(path: Path, log: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_candidate(log: dict[str, Any], candidate_id: str) -> dict[str, Any]:
    for candidate in log["candidates"]:
        if isinstance(candidate, dict) and candidate.get("candidate_id") == candidate_id:
            return candidate
    fail(f"candidate not found: {candidate_id}")


def cmd_init(args: argparse.Namespace) -> int:
    job_path = args.job.expanduser().resolve()
    try:
        job = json.loads(job_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"job does not exist: {job_path}")
    except json.JSONDecodeError as error:
        fail(f"job is not valid JSON: {error}")
    job_id = job.get("job_id") if isinstance(job, dict) else None
    if not isinstance(job_id, str) or not ID_RE.fullmatch(job_id):
        fail("job has no valid job_id")
    log_path = args.log.expanduser().resolve()
    if log_path.exists():
        fail(f"refusing to overwrite an existing decision log: {log_path}")
    write_log(log_path, {"schema_version": 1, "job_id": job_id, "candidates": []})
    print(f"initialized decision log for {job_id}: {log_path}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    log_path = args.log.expanduser().resolve()
    log = load_log(log_path)
    if not ID_RE.fullmatch(args.candidate_id):
        fail("candidate id must use lowercase ASCII letters, digits, and single hyphens")
    if any(c.get("candidate_id") == args.candidate_id for c in log["candidates"]):
        fail(f"candidate already logged: {args.candidate_id}")

    outputs = []
    for raw in args.outputs:
        output_path = Path(raw).expanduser().resolve()
        if not output_path.is_file():
            fail(f"output file does not exist: {output_path}")
        outputs.append(
            {
                "path": str(output_path),
                "sha256": sha256_file(output_path),
                "type": OUTPUT_TYPE_BY_SUFFIX.get(output_path.suffix.casefold(), "file"),
            }
        )
    if args.status == "generated" and not outputs:
        fail("a generated candidate needs at least one --output file")

    log["candidates"].append(
        {
            "candidate_id": args.candidate_id,
            "created_at": now_iso(),
            "status": args.status,
            "adapter": args.adapter,
            "workflow_id": args.workflow_id,
            "model": args.model,
            "seed": args.seed,
            "prompt_revision": args.prompt_revision,
            "prompt_id": args.prompt_id,
            "input_values_sha256": None,
            "outputs": outputs,
            "rejection_reason": None,
            "notes": args.note,
            "cost": args.cost,
        }
    )
    write_log(log_path, log)
    print(f"{args.candidate_id}: {args.status} ({len(outputs)} files)")
    return 0


def cmd_reject(args: argparse.Namespace) -> int:
    log_path = args.log.expanduser().resolve()
    log = load_log(log_path)
    candidate = find_candidate(log, args.candidate_id)
    if not args.reason.strip():
        fail("a rejection needs a non-empty --reason")
    candidate["status"] = "rejected"
    candidate["rejection_reason"] = args.reason.strip()
    write_log(log_path, log)
    print(f"{args.candidate_id}: rejected")
    return 0


def cmd_select(args: argparse.Namespace) -> int:
    log_path = args.log.expanduser().resolve()
    log = load_log(log_path)
    candidate = find_candidate(log, args.candidate_id)
    if candidate.get("status") not in {"generated", "selected"}:
        fail(f"only a generated candidate can be selected; status is {candidate.get('status')}")
    candidate["status"] = "selected"
    write_log(log_path, log)
    selected = [
        c["candidate_id"] for c in log["candidates"] if c.get("status") == "selected"
    ]
    print(f"{args.candidate_id}: selected (total selected: {len(selected)})")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    log_path = args.log.expanduser().resolve()
    log = load_log(log_path)
    if args.as_json:
        print(json.dumps(log, ensure_ascii=False, indent=2))
        return 0
    counts: dict[str, int] = {}
    for candidate in log["candidates"]:
        counts[candidate.get("status", "?")] = counts.get(candidate.get("status", "?"), 0) + 1
    print(f"job: {log.get('job_id')}  candidates: {len(log['candidates'])}  {counts}")
    for candidate in log["candidates"]:
        reason = candidate.get("rejection_reason")
        print(
            f"  {candidate.get('candidate_id')}: {candidate.get('status')}"
            f" seed={candidate.get('seed')}"
            f" outputs={len(candidate.get('outputs', []))}"
            + (f" reason={reason}" if reason else "")
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create an empty decision log for a job")
    init.add_argument("--job", type=Path, required=True)
    init.add_argument("--log", type=Path, required=True)
    init.set_defaults(handler=cmd_init)

    add = sub.add_parser("add", help="Record one candidate")
    add.add_argument("--log", type=Path, required=True)
    add.add_argument("--candidate-id", required=True)
    add.add_argument("--adapter", required=True, help="e.g. zealman-autodl, minimax-h3, host-tool")
    add.add_argument("--status", choices=["generated", "failed"], default="generated")
    add.add_argument("--workflow-id")
    add.add_argument("--model")
    add.add_argument("--seed", type=int)
    add.add_argument("--prompt-revision")
    add.add_argument("--prompt-id")
    add.add_argument("--cost", type=float)
    add.add_argument("--note")
    add.add_argument("--output", action="append", default=[], dest="outputs", metavar="FILE")
    add.set_defaults(handler=cmd_add)

    reject = sub.add_parser("reject", help="Reject a candidate with a reason")
    reject.add_argument("--log", type=Path, required=True)
    reject.add_argument("--candidate-id", required=True)
    reject.add_argument("--reason", required=True)
    reject.set_defaults(handler=cmd_reject)

    select = sub.add_parser("select", help="Mark a generated candidate as selected")
    select.add_argument("--log", type=Path, required=True)
    select.add_argument("--candidate-id", required=True)
    select.set_defaults(handler=cmd_select)

    show = sub.add_parser("show", help="Print the log")
    show.add_argument("--log", type=Path, required=True)
    show.add_argument("--json", action="store_true", dest="as_json")
    show.set_defaults(handler=cmd_show)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
