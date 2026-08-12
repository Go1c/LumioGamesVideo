#!/usr/bin/env python3
"""Execute a staged Zealman panel-API workflow from a run request.

Follows the documented panel sequence: upload file inputs, submit
``POST /api/workflow/generate``, poll ``GET /api/workflow/result`` until
``pending`` is false, then download every ``/output/...`` artifact immediately.
Each variant is appended to the job's decision log and the staged sidecar
status advances from ``staged`` to ``rendered`` or ``failed``.

The panel base URL is session-scoped: pass it via --base-url or the
ZEALMAN_BASE_URL environment variable. It is never written to the sidecar,
the decision log, or any other file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RESULT_TYPE_BY_SUFFIX = {
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
}


def fail(message: str) -> "NoReturn":  # noqa: F821 - runtime string annotation
    raise SystemExit(f"error: {message}")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json_file(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{label} does not exist: {path}")
    except json.JSONDecodeError as error:
        fail(f"{label} is not valid JSON: {error}")
    if not isinstance(data, dict):
        fail(f"{label} root must be a JSON object")
    return data


class PanelClient:
    """Minimal stdlib client for the Zealman panel HTTP API."""

    def __init__(self, base_url: str, timeout: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _open(self, request: urllib.request.Request) -> bytes:
        path = urllib.parse.urlparse(request.full_url).path
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:300]
            fail(f"panel request failed: {error.code} {path} {detail}")
        except urllib.error.URLError as error:
            fail(f"panel is unreachable ({path}): {error.reason}")

    def get_json(self, path: str) -> dict[str, Any]:
        request = urllib.request.Request(self.base_url + path)
        return json.loads(self._open(request).decode("utf-8"))

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        return json.loads(self._open(request).decode("utf-8"))

    def get_bytes(self, path: str) -> bytes:
        request = urllib.request.Request(self.base_url + path)
        return self._open(request)

    def upload_file(self, path: Path) -> str:
        boundary = uuid.uuid4().hex
        head = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
            "Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8")
        tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
        request = urllib.request.Request(
            self.base_url + "/api/comfy/upload/file",
            data=head + path.read_bytes() + tail,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        response = json.loads(self._open(request).decode("utf-8"))
        name = response.get("name")
        if not isinstance(name, str) or not name:
            fail(f"upload returned no file name for {path.name}")
        return name


def check_guards(request: dict[str, Any]) -> None:
    execution = request.get("execution")
    if execution == "plan-only":
        fail(
            "job execution is plan-only; update generation.execution in the job, "
            "revalidate it, and rebuild the run request before rendering"
        )
    if execution not in {"local", "remote"}:
        fail(f"run request has invalid execution: {execution!r}")
    if execution == "remote":
        unapproved = [
            info.get("asset_id", parameter)
            for parameter, info in request.get("file_inputs", {}).items()
            if info.get("remote_upload_approved") is not True
        ]
        if unapproved:
            fail(
                "remote execution requires remote_upload_approved for every uploaded "
                f"asset; missing approval: {', '.join(sorted(unapproved))}"
            )


def ensure_workflow_registered(
    client: PanelClient, workflow_id: str, staged_path: Path, register: bool
) -> None:
    listing = client.get_json("/api/workflow/list")
    known = {
        str(entry.get("id", ""))
        for entry in listing.get("workflows", [])
        if isinstance(entry, dict)
    }
    stem = workflow_id[:-5] if workflow_id.casefold().endswith(".json") else workflow_id
    if workflow_id in known or stem in known or f"{stem}.json" in known:
        return
    if not register:
        fail(
            f"workflow {workflow_id} is not saved on the panel; re-run with --register "
            "or save the staged copy through the panel's API-generation page"
        )
    staged = load_json_file(staged_path, "staged workflow")
    api_config = staged.get("_api_config")
    if not isinstance(api_config, dict):
        fail("staged workflow is not a panel API JSON: missing _api_config")
    template = {key: value for key, value in staged.items() if key != "_api_config"}
    client.post_json(
        "/api/workflow/save",
        {"workflow_id": workflow_id, "workflow_template": template, "api_config": api_config},
    )


def next_candidate_index(log: dict[str, Any]) -> int:
    return len(log.get("candidates", [])) + 1


def load_or_create_log(path: Path, job_id: Any) -> dict[str, Any]:
    if path.exists():
        log = load_json_file(path, "decision log")
        if job_id and log.get("job_id") and log["job_id"] != job_id:
            fail(f"decision log belongs to job {log['job_id']}, not {job_id}")
        return log
    return {"schema_version": 1, "job_id": job_id, "candidates": []}


def write_log(path: Path, log: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def download_results(
    client: PanelClient, results: list[Any], candidate_dir: Path
) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    candidate_dir.mkdir(parents=True, exist_ok=True)
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            continue
        url = str(result.get("url", ""))
        if not url:
            continue
        filename = str(result.get("filename") or Path(urllib.parse.urlparse(url).path).name)
        content = client.get_bytes(url if url.startswith("/") else "/" + url)
        target = candidate_dir / filename
        if target.exists():
            target = candidate_dir / f"{index:02d}-{filename}"
        target.write_bytes(content)
        outputs.append(
            {
                "path": str(target),
                "sha256": sha256_bytes(content),
                "type": result.get("type")
                or RESULT_TYPE_BY_SUFFIX.get(target.suffix.casefold(), "file"),
                "source_url_path": url,
            }
        )
    return outputs


def poll_result(
    client: PanelClient, prompt_id: str, poll_interval: float, timeout: float
) -> list[Any]:
    deadline = time.monotonic() + timeout
    while True:
        response = client.get_json(
            "/api/workflow/result?" + urllib.parse.urlencode({"prompt_id": prompt_id})
        )
        if response.get("pending") is False:
            results = response.get("results")
            return results if isinstance(results, list) else []
        if time.monotonic() >= deadline:
            fail(
                f"timed out waiting for prompt {prompt_id}; the panel keeps history in "
                "memory only, so poll again soon or lower the workload"
            )
        time.sleep(poll_interval)


def update_sidecar(
    staged_path: Path,
    status: str,
    run_record: dict[str, Any],
) -> None:
    sidecar_path = staged_path.with_name(staged_path.name + ".source.json")
    if not sidecar_path.is_file():
        return
    sidecar = load_json_file(sidecar_path, "staged sidecar")
    sidecar["status"] = status
    sidecar.setdefault("runs", []).append(run_record)
    sidecar_path.write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_request", type=Path, help="Run request produced by apply_job.py")
    parser.add_argument("--output-dir", type=Path, required=True, help="Candidate output directory")
    parser.add_argument("--base-url", help="Panel base URL; defaults to ZEALMAN_BASE_URL")
    parser.add_argument("--variants", type=int, help="Override the job's variant count")
    parser.add_argument("--seed-param", help="nodeId:field randomized per variant")
    parser.add_argument("--decision-log", type=Path, help="Defaults to <output-dir>/decision-log.json")
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--timeout", type=float, default=1800.0, help="Per-candidate seconds")
    parser.add_argument("--register", action="store_true", help="Save the staged workflow when missing")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without any network call")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    request_path = args.run_request.expanduser().resolve()
    request = load_json_file(request_path, "run request")
    if request.get("kind") != "zealman-run-request":
        fail("run request must be produced by apply_job.py (kind zealman-run-request)")
    check_guards(request)

    staged_path = Path(request["staged_workflow"])
    if staged_path.is_file() and sha256_file(staged_path) != request.get("staged_sha256"):
        fail("staged workflow changed after the run request was built; re-run apply_job.py")

    workflow_id = str(request["workflow_id"])
    variants = args.variants or int(request.get("variants") or 1)
    if not 1 <= variants <= 12:
        fail("variants must be between 1 and 12")
    seed_param = args.seed_param or request.get("seed_param")
    if variants > 1 and not seed_param:
        fail("multiple variants need a seed parameter; pass --seed-param nodeId:field")

    base_values: dict[str, Any] = dict(request.get("input_values", {}))
    file_inputs: dict[str, dict[str, Any]] = request.get("file_inputs", {})
    output_dir = args.output_dir.expanduser().resolve()

    if args.dry_run:
        plan = {
            "workflow_id": workflow_id,
            "variants": variants,
            "seed_param": seed_param,
            "uploads": {param: info.get("path") for param, info in file_inputs.items()},
            "input_values": base_values,
            "output_dir": str(output_dir),
        }
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    base_url = args.base_url or os.environ.get("ZEALMAN_BASE_URL", "")
    if not base_url:
        fail(
            "no panel base URL; pass --base-url or set ZEALMAN_BASE_URL "
            "(session-scoped, never saved to disk)"
        )
    client = PanelClient(base_url)

    health = client.get_json("/api/health")
    if health.get("success") is False or health.get("status") in {"error", "down"}:
        fail(f"panel health check failed: {json.dumps(health, ensure_ascii=False)[:200]}")
    ensure_workflow_registered(client, workflow_id, staged_path, args.register)

    for parameter, info in file_inputs.items():
        local = Path(info["path"])
        if not local.is_file():
            fail(f"file input does not exist: {local}")
        if sha256_file(local) != info.get("sha256"):
            fail(f"file input changed after the run request was built: {local}")
        base_values[parameter] = client.upload_file(local)

    log_path = args.decision_log or output_dir / "decision-log.json"
    log_path = log_path.expanduser().resolve()
    log = load_or_create_log(log_path, request.get("job_id"))

    candidate_ids: list[str] = []
    prompt_ids: list[str] = []
    failures = 0
    for variant in range(variants):
        candidate_id = f"c-{next_candidate_index(log):03d}"
        candidate_ids.append(candidate_id)
        input_values = dict(base_values)
        seed = input_values.get(seed_param) if seed_param else None
        if seed_param and (variant > 0 or seed in (None, "")):
            seed = secrets.randbelow(2**31)
            input_values[seed_param] = seed
        entry: dict[str, Any] = {
            "candidate_id": candidate_id,
            "created_at": now_iso(),
            "status": "failed",
            "adapter": "zealman-autodl",
            "workflow_id": workflow_id,
            "seed": seed,
            "prompt_id": None,
            "input_values_sha256": sha256_bytes(
                json.dumps(input_values, ensure_ascii=False, sort_keys=True).encode("utf-8")
            ),
            "outputs": [],
            "rejection_reason": None,
            "notes": None,
        }
        try:
            submission = client.post_json(
                "/api/workflow/generate",
                {
                    "workflow_id": workflow_id,
                    "input_values": input_values,
                    "client_id": f"lumio-{request.get('job_id')}-{candidate_id}",
                },
            )
            prompt_id = submission.get("prompt_id")
            if not isinstance(prompt_id, str) or not prompt_id:
                raise SystemExit(
                    f"error: generate returned no prompt_id: "
                    f"{json.dumps(submission, ensure_ascii=False)[:200]}"
                )
            entry["prompt_id"] = prompt_id
            prompt_ids.append(prompt_id)
            results = poll_result(client, prompt_id, args.poll_interval, args.timeout)
            entry["outputs"] = download_results(client, results, output_dir / candidate_id)
            entry["status"] = "generated" if entry["outputs"] else "failed"
            if not entry["outputs"]:
                entry["notes"] = "panel reported completion without downloadable outputs"
        except SystemExit as error:
            entry["notes"] = str(error)
        if entry["status"] == "failed":
            failures += 1
        log["candidates"].append(entry)
        write_log(log_path, log)
        print(
            f"{candidate_id}: {entry['status']}"
            + (f" ({len(entry['outputs'])} files)" if entry["outputs"] else "")
        )

    status = "rendered" if failures < variants else "failed"
    update_sidecar(
        staged_path,
        status,
        {
            "run_at": now_iso(),
            "workflow_id": workflow_id,
            "variants": variants,
            "candidate_ids": candidate_ids,
            "prompt_ids": prompt_ids,
            "output_dir": str(output_dir),
            "decision_log": str(log_path),
            "failures": failures,
        },
    )
    print(
        json.dumps(
            {
                "status": status,
                "candidates": candidate_ids,
                "failures": failures,
                "decision_log": str(log_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
