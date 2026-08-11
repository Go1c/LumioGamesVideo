#!/usr/bin/env python3
"""Summarize a ComfyUI UI graph or Zealman panel-API workflow JSON."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


MODEL_SUFFIXES = (
    ".bin",
    ".ckpt",
    ".gguf",
    ".onnx",
    ".pt",
    ".pth",
    ".safetensors",
)
FILE_FIELD_HINTS = ("audio", "file", "image", "path", "video")
INPUT_NODE_HINTS = ("audio", "image", "input", "load", "text", "video")
OUTPUT_NODE_HINTS = ("combine", "output", "preview", "save")


def walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_strings(child)


def model_references(data: Any) -> list[str]:
    references = {
        value
        for value in walk_strings(data)
        if value.casefold().endswith(MODEL_SUFFIXES)
    }
    return sorted(references, key=str.casefold)


def compact_default(value: Any) -> Any:
    if isinstance(value, str):
        return value if len(value) <= 160 else value[:157] + "..."
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return "connected" if isinstance(value, list) else type(value).__name__


def inspect_ui(data: dict[str, Any], path: Path) -> dict[str, Any]:
    nodes = data.get("nodes", [])
    node_types = Counter(str(node.get("type", "unknown")) for node in nodes)

    inputs = []
    outputs = []
    for node in nodes:
        node_type = str(node.get("type", "unknown"))
        folded = node_type.casefold()
        summary = {
            "id": node.get("id"),
            "type": node_type,
            "title": node.get("title"),
        }
        if any(hint in folded for hint in INPUT_NODE_HINTS):
            inputs.append(summary)
        if any(hint in folded for hint in OUTPUT_NODE_HINTS):
            outputs.append(summary)

    return {
        "path": str(path),
        "format": "ui",
        "node_count": len(nodes),
        "link_count": len(data.get("links", [])),
        "node_types": dict(sorted(node_types.items())),
        "likely_input_nodes": inputs,
        "likely_output_nodes": outputs,
        "model_references": model_references(data),
    }


def inspect_api(data: dict[str, Any], path: Path) -> dict[str, Any]:
    config = data.get("_api_config", {})
    nodes = {key: value for key, value in data.items() if key != "_api_config"}
    node_types = Counter(
        str(node.get("class_type", "unknown"))
        for node in nodes.values()
        if isinstance(node, dict)
    )

    labels = config.get("customLabels", {}) if isinstance(config, dict) else {}
    enabled = config.get("enabledParams", {}) if isinstance(config, dict) else {}
    enabled_parameters = []
    for parameter, is_enabled in enabled.items():
        if not is_enabled:
            continue
        node_id, _, field = parameter.partition(":")
        node = nodes.get(node_id, {})
        value = node.get("inputs", {}).get(field) if isinstance(node, dict) else None
        enabled_parameters.append(
            {
                "parameter": parameter,
                "label": labels.get(parameter, parameter),
                "node_type": node.get("class_type") if isinstance(node, dict) else None,
                "default": compact_default(value),
            }
        )

    file_inputs = []
    for node_id, node in nodes.items():
        if not isinstance(node, dict):
            continue
        for field, value in node.get("inputs", {}).items():
            if any(hint in field.casefold() for hint in FILE_FIELD_HINTS):
                file_inputs.append(
                    {
                        "parameter": f"{node_id}:{field}",
                        "node_type": node.get("class_type"),
                        "default": compact_default(value),
                    }
                )

    return {
        "path": str(path),
        "format": "api",
        "node_count": len(nodes),
        "node_types": dict(sorted(node_types.items())),
        "enabled_parameters": enabled_parameters,
        "likely_file_inputs": file_inputs,
        "model_references": model_references(data),
    }


def inspect(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SystemExit(f"Workflow not found: {path}") from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON at {path}: {error}") from error

    if not isinstance(data, dict):
        raise SystemExit("Workflow root must be a JSON object")
    if isinstance(data.get("nodes"), list):
        return inspect_ui(data, path)
    if "_api_config" in data:
        return inspect_api(data, path)
    raise SystemExit("Unrecognized workflow JSON: expected UI nodes[] or panel _api_config")


def print_text(report: dict[str, Any]) -> None:
    print(f"Format: {report['format']}")
    print(f"Nodes: {report['node_count']}")
    if "link_count" in report:
        print(f"Links: {report['link_count']}")

    if report.get("enabled_parameters"):
        print("Enabled parameters:")
        for item in report["enabled_parameters"]:
            print(f"  - {item['parameter']}: {item['label']} ({item['node_type']})")

    if report.get("likely_file_inputs"):
        print("Likely file inputs:")
        for item in report["likely_file_inputs"]:
            print(f"  - {item['parameter']} ({item['node_type']})")

    if report["model_references"]:
        print("Model references:")
        for model in report["model_references"]:
            print(f"  - {model}")

    print("Node types:")
    for node_type, count in report["node_types"].items():
        print(f"  - {node_type}: {count}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = inspect(args.workflow.expanduser().resolve())
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
