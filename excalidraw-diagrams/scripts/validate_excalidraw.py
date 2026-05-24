#!/usr/bin/env python3
"""Validate and lightly normalize Excalidraw JSON or Obsidian Excalidraw Markdown."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


OBSIDIAN_BLOCK_RE = re.compile(r"```json\n(?P<json>\{.*?\})\n```", re.DOTALL)


def load_scene(path: Path) -> tuple[dict[str, Any], str | None]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".md":
        match = OBSIDIAN_BLOCK_RE.search(text)
        if not match:
            raise ValueError("Markdown file does not contain a ```json Excalidraw block")
        return json.loads(match.group("json")), text
    return json.loads(text), None


def dump_scene(path: Path, scene: dict[str, Any], original_markdown: str | None) -> None:
    serialized = json.dumps(scene, indent=2, ensure_ascii=False) + "\n"
    if original_markdown is None:
        path.write_text(serialized, encoding="utf-8")
        return
    updated = OBSIDIAN_BLOCK_RE.sub("```json\n" + serialized.rstrip() + "\n```", original_markdown, count=1)
    path.write_text(updated, encoding="utf-8")


def normalize_scene(scene: dict[str, Any]) -> list[str]:
    changes: list[str] = []
    defaults: dict[str, Any] = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": [],
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
        "files": {},
    }
    for key, value in defaults.items():
        if key not in scene:
            scene[key] = value
            changes.append(f"added top-level {key}")
    if isinstance(scene.get("appState"), dict):
        app_state = scene["appState"]
        if "viewBackgroundColor" not in app_state:
            app_state["viewBackgroundColor"] = "#ffffff"
            changes.append("added appState.viewBackgroundColor")
        if "gridSize" not in app_state:
            app_state["gridSize"] = None
            changes.append("added appState.gridSize")
    return changes


def validate_scene(scene: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if scene.get("type") not in {"excalidraw", "excalidraw/clipboard"}:
        errors.append("top-level type must be 'excalidraw' or 'excalidraw/clipboard'")
    if scene.get("type") == "excalidraw":
        for key in ("version", "source", "appState", "files"):
            if key not in scene:
                errors.append(f"missing top-level {key}")
    elements = scene.get("elements")
    if not isinstance(elements, list):
        return errors + ["elements must be a list"]

    seen_ids: set[str] = set()
    for index, element in enumerate(elements):
        label = f"elements[{index}]"
        if not isinstance(element, dict):
            errors.append(f"{label} must be an object")
            continue
        element_id = element.get("id")
        if not isinstance(element_id, str) or not element_id:
            errors.append(f"{label} missing string id")
        elif element_id in seen_ids:
            errors.append(f"{label} duplicate id {element_id!r}")
        else:
            seen_ids.add(element_id)

        element_type = element.get("type")
        if not isinstance(element_type, str):
            errors.append(f"{label} missing string type")
        for key in ("x", "y", "width", "height"):
            if not isinstance(element.get(key), (int, float)):
                errors.append(f"{label} missing numeric {key}")

        if element_type == "text":
            for key in ("text", "fontSize", "fontFamily", "textAlign", "verticalAlign"):
                if key not in element:
                    errors.append(f"{label} text element missing {key}")
        if element_type in {"line", "arrow"}:
            points = element.get("points")
            if not isinstance(points, list) or len(points) < 2:
                errors.append(f"{label} {element_type} element needs at least two points")
            if element_type == "arrow" and "endArrowhead" not in element:
                errors.append(f"{label} arrow missing endArrowhead")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--write", action="store_true", help="write normalized top-level defaults")
    args = parser.parse_args()

    try:
        scene, original_markdown = load_scene(args.path)
        if not isinstance(scene, dict):
            raise ValueError("scene JSON must be an object")
        changes = normalize_scene(scene)
        errors = validate_scene(scene)
    except Exception as exc:  # noqa: BLE001 - report validation failures cleanly for agents.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.write and changes:
        dump_scene(args.path, scene, original_markdown)
    if changes and not args.write:
        print("OK with normalizable issues:")
        for change in changes:
            print(f"- {change}")
    else:
        print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
