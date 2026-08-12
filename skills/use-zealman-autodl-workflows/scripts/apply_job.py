#!/usr/bin/env python3
"""Map an approved game-video job onto a staged Zealman API workflow.

Produces a run-request JSON that scripts/run_workflow.py can execute. The staged
workflow itself is never modified; parameter values are collected as panel
``input_values`` (``nodeId:field`` keys) plus a list of local files that must be
uploaded at run time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FILE_FIELD_HINTS = ("audio", "file", "image", "path", "video")


def fail(message: str) -> "NoReturn":  # noqa: F821 - runtime string annotation
    raise SystemExit(f"error: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{label} does not exist: {path}")
    except json.JSONDecodeError as error:
        fail(f"{label} is not valid JSON: {error}")
    if not isinstance(data, dict):
        fail(f"{label} root must be a JSON object")
    return data


def job_lookup(job: dict[str, Any], dotted: str) -> Any:
    value: Any = job
    for part in dotted.split("."):
        if isinstance(value, list):
            try:
                value = value[int(part)]
            except (ValueError, IndexError):
                fail(f"job path not found: {dotted}")
        elif isinstance(value, dict) and part in value:
            value = value[part]
        else:
            fail(f"job path not found: {dotted}")
    if isinstance(value, (dict, list)):
        fail(f"job path {dotted} is not a scalar value")
    return value


def find_asset(job: dict[str, Any], asset_id: str) -> dict[str, Any]:
    for asset in job.get("inputs", {}).get("assets", []):
        if isinstance(asset, dict) and asset.get("id") == asset_id:
            return asset
    fail(f"asset not found in job: {asset_id}")


def parse_mapping(raw: str) -> tuple[str, str]:
    parameter, separator, source = raw.partition("=")
    if not separator or not parameter or not source:
        fail(f"--map must look like nodeId:field=source, got: {raw}")
    if ":" not in parameter:
        fail(f"--map parameter must look like nodeId:field, got: {parameter}")
    return parameter, source


def resolve_source(
    source: str,
    job: dict[str, Any],
    job_dir: Path,
) -> tuple[Any, dict[str, Any] | None, bool]:
    """Return (value, file_input, is_seed) for one mapping source."""
    kind, separator, rest = source.partition(":")
    if not separator:
        fail(f"mapping source must look like kind:value, got: {source}")
    if kind == "text":
        return rest, None, False
    if kind == "prompt":
        prompt_path = (job_dir / rest).resolve() if not Path(rest).is_absolute() else Path(rest)
        try:
            return prompt_path.read_text(encoding="utf-8").strip(), None, False
        except FileNotFoundError:
            fail(f"prompt file does not exist: {prompt_path}")
    if kind == "job":
        return job_lookup(job, rest), None, False
    if kind == "asset":
        asset = find_asset(job, rest)
        raw_source = str(asset.get("source", ""))
        asset_path = Path(raw_source)
        if not asset_path.is_absolute():
            asset_path = (job_dir / asset_path).resolve()
        if not asset_path.is_file():
            fail(f"asset file does not exist: {asset_path} (asset {rest})")
        file_input = {
            "path": str(asset_path),
            "asset_id": rest,
            "sha256": sha256(asset_path),
            "remote_upload_approved": asset.get("remote_upload_approved") is True,
        }
        return None, file_input, False
    if kind == "seed":
        if rest == "random":
            return secrets.randbelow(2**31), None, True
        try:
            return int(rest), None, True
        except ValueError:
            fail(f"seed must be an integer or 'random', got: {rest}")
    if kind == "int":
        try:
            return int(rest), None, False
        except ValueError:
            fail(f"invalid int value: {rest}")
    if kind == "float":
        try:
            return float(rest), None, False
        except ValueError:
            fail(f"invalid float value: {rest}")
    if kind == "bool":
        if rest not in {"true", "false"}:
            fail(f"bool value must be true or false, got: {rest}")
        return rest == "true", None, False
    fail(f"unknown mapping source kind: {kind}")


def enabled_parameters(workflow: dict[str, Any]) -> dict[str, dict[str, Any]]:
    config = workflow.get("_api_config")
    if not isinstance(config, dict):
        fail("staged workflow is not a panel API JSON: missing _api_config")
    labels = config.get("customLabels", {}) if isinstance(config.get("customLabels"), dict) else {}
    enabled = config.get("enabledParams", {}) if isinstance(config.get("enabledParams"), dict) else {}
    nodes = {key: value for key, value in workflow.items() if key != "_api_config"}
    report: dict[str, dict[str, Any]] = {}
    for parameter, is_enabled in enabled.items():
        if not is_enabled:
            continue
        node_id, _, field = parameter.partition(":")
        node = nodes.get(node_id, {})
        default = node.get("inputs", {}).get(field) if isinstance(node, dict) else None
        report[parameter] = {
            "label": labels.get(parameter, parameter),
            "node_type": node.get("class_type") if isinstance(node, dict) else None,
            "default": default,
            "looks_like_file": any(hint in field.casefold() for hint in FILE_FIELD_HINTS),
        }
    return report


def parameter_exists(workflow: dict[str, Any], parameter: str) -> bool:
    node_id, _, field = parameter.partition(":")
    node = workflow.get(node_id)
    return isinstance(node, dict) and field in node.get("inputs", {})


def print_parameter_list(parameters: dict[str, dict[str, Any]]) -> None:
    print("Enabled parameters:")
    for parameter, info in parameters.items():
        marker = " [file]" if info["looks_like_file"] else ""
        default = info["default"]
        if isinstance(default, str) and len(default) > 60:
            default = default[:57] + "..."
        print(f"  - {parameter}: {info['label']} ({info['node_type']}){marker} default={default!r}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staged_workflow", type=Path, help="Staged panel API workflow JSON")
    parser.add_argument("--job", type=Path, help="Validated game-video-job.json")
    parser.add_argument(
        "--map",
        action="append",
        default=[],
        dest="mappings",
        metavar="PARAM=SOURCE",
        help=(
            "Map one workflow parameter. SOURCE kinds: text:<literal>, prompt:<file>, "
            "asset:<job asset id>, job:<dotted.path>, seed:<int|random>, int:<n>, "
            "float:<x>, bool:<true|false>"
        ),
    )
    parser.add_argument("--output", type=Path, help="Run-request path; defaults next to the staged workflow")
    parser.add_argument("--workflow-id", help="Panel workflow id; defaults to the staged filename")
    parser.add_argument("--allow-disabled", action="store_true", help="Allow params outside enabledParams")
    parser.add_argument("--list", action="store_true", dest="list_only", help="List enabled parameters and exit")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    staged_path = args.staged_workflow.expanduser().resolve()
    workflow = load_json(staged_path, "staged workflow")
    parameters = enabled_parameters(workflow)

    if args.list_only:
        print_parameter_list(parameters)
        return 0

    if args.job is None:
        fail("--job is required unless --list is used")
    if not args.mappings:
        fail("at least one --map is required; use --list to see enabled parameters")

    job_path = args.job.expanduser().resolve()
    job = load_json(job_path, "job")
    job_dir = job_path.parent
    generation = job.get("generation", {}) if isinstance(job.get("generation"), dict) else {}

    input_values: dict[str, Any] = {}
    file_inputs: dict[str, dict[str, Any]] = {}
    seed_param: str | None = None
    for raw in args.mappings:
        parameter, source = parse_mapping(raw)
        if parameter in input_values or parameter in file_inputs:
            fail(f"parameter mapped twice: {parameter}")
        if parameter not in parameters and not args.allow_disabled:
            fail(
                f"parameter {parameter} is not in enabledParams; "
                "pass --allow-disabled to map it anyway"
            )
        if not parameter_exists(workflow, parameter):
            fail(f"parameter {parameter} does not exist in the staged workflow nodes")
        value, file_input, is_seed = resolve_source(source, job, job_dir)
        if file_input is not None:
            file_inputs[parameter] = file_input
        else:
            input_values[parameter] = value
        if is_seed:
            if seed_param is not None:
                fail("only one seed: mapping is allowed")
            seed_param = parameter

    workflow_id = args.workflow_id or staged_path.name
    variants = generation.get("variants") if isinstance(generation.get("variants"), int) else 1
    request = {
        "schema_version": 1,
        "kind": "zealman-run-request",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "job_id": job.get("job_id"),
        "job_path": str(job_path),
        "job_sha256": sha256(job_path),
        "workflow_id": workflow_id,
        "staged_workflow": str(staged_path),
        "staged_sha256": sha256(staged_path),
        "execution": generation.get("execution"),
        "variants": variants,
        "seed_param": seed_param,
        "input_values": input_values,
        "file_inputs": file_inputs,
    }

    output = args.output
    if output is None:
        output = staged_path.with_name(staged_path.stem + ".run-request.json")
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_request": str(output), **request}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
