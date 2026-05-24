#!/usr/bin/env python3
"""Validate and lightly normalize uncompressed Draw.io .drawio XML files."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SAFE_MXFILE_DEFAULTS = {
    "host": "app.diagrams.net",
    "type": "device",
}

SAFE_MODEL_DEFAULTS = {
    "dx": "1200",
    "dy": "800",
    "grid": "1",
    "gridSize": "10",
    "guides": "1",
    "tooltips": "1",
    "connect": "1",
    "arrows": "1",
    "fold": "1",
    "page": "1",
    "pageScale": "1",
    "pageWidth": "1600",
    "pageHeight": "1000",
    "math": "0",
    "shadow": "0",
}


def parse_xml(path: Path) -> ET.ElementTree:
    try:
        return ET.parse(path)
    except ET.ParseError as exc:
        raise ValueError(f"invalid XML: {exc}") from exc


def normalize(root: ET.Element) -> list[str]:
    changes: list[str] = []
    for key, value in SAFE_MXFILE_DEFAULTS.items():
        if not root.get(key):
            root.set(key, value)
            changes.append(f"added mxfile {key}")

    for model in root.findall("./diagram/mxGraphModel"):
        for key, value in SAFE_MODEL_DEFAULTS.items():
            if not model.get(key):
                model.set(key, value)
                changes.append(f"added mxGraphModel {key}")
    return changes


def is_number(value: str | None) -> bool:
    if value is None:
        return False
    try:
        float(value)
    except ValueError:
        return False
    return True


def validate(root: ET.Element) -> list[str]:
    errors: list[str] = []
    if root.tag != "mxfile":
        return ["root element must be mxfile"]

    diagrams = root.findall("diagram")
    if not diagrams:
        errors.append("mxfile must contain at least one diagram")

    for diagram_index, diagram in enumerate(diagrams):
        diagram_label = f"diagram[{diagram_index}]"
        if not diagram.get("id"):
            errors.append(f"{diagram_label} missing id")
        if not diagram.get("name"):
            errors.append(f"{diagram_label} missing name")

        models = diagram.findall("mxGraphModel")
        if len(models) != 1:
            errors.append(f"{diagram_label} must contain exactly one mxGraphModel")
            continue
        model = models[0]
        root_cell = model.find("root")
        if root_cell is None:
            errors.append(f"{diagram_label} mxGraphModel missing root")
            continue

        cells = root_cell.findall("mxCell")
        ids: set[str] = set()
        for cell in cells:
            cell_id = cell.get("id")
            if not cell_id:
                errors.append(f"{diagram_label} mxCell missing id")
                continue
            if cell_id in ids:
                errors.append(f"{diagram_label} duplicate mxCell id {cell_id!r}")
            ids.add(cell_id)

        if "0" not in ids:
            errors.append(f"{diagram_label} missing root mxCell id '0'")
        if "1" not in ids:
            errors.append(f"{diagram_label} missing default layer mxCell id '1'")

        for cell in cells:
            cell_id = cell.get("id", "<missing>")
            is_vertex = cell.get("vertex") == "1"
            is_edge = cell.get("edge") == "1"

            if is_vertex and is_edge:
                errors.append(f"{diagram_label} cell {cell_id} cannot be both vertex and edge")
            if is_vertex:
                geometry = cell.find("mxGeometry")
                if geometry is None:
                    errors.append(f"{diagram_label} vertex {cell_id} missing mxGeometry")
                    continue
                for key in ("x", "y", "width", "height"):
                    if not is_number(geometry.get(key)):
                        errors.append(f"{diagram_label} vertex {cell_id} missing numeric geometry {key}")
                if geometry.get("as") != "geometry":
                    errors.append(f"{diagram_label} vertex {cell_id} mxGeometry must have as='geometry'")
            if is_edge:
                source = cell.get("source")
                target = cell.get("target")
                if not source or source not in ids:
                    errors.append(f"{diagram_label} edge {cell_id} has missing or unknown source")
                if not target or target not in ids:
                    errors.append(f"{diagram_label} edge {cell_id} has missing or unknown target")
                geometry = cell.find("mxGeometry")
                if geometry is None:
                    errors.append(f"{diagram_label} edge {cell_id} missing mxGeometry")
                    continue
                if geometry.get("relative") != "1":
                    errors.append(f"{diagram_label} edge {cell_id} mxGeometry should have relative='1'")
                if geometry.get("as") != "geometry":
                    errors.append(f"{diagram_label} edge {cell_id} mxGeometry must have as='geometry'")
    return errors


def write_xml(path: Path, tree: ET.ElementTree) -> None:
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--write", action="store_true", help="write safe missing defaults")
    args = parser.parse_args()

    try:
        tree = parse_xml(args.path)
        root = tree.getroot()
        changes = normalize(root)
        errors = validate(root)
    except Exception as exc:  # noqa: BLE001 - keep validator output simple for agents.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.write and changes:
        write_xml(args.path, tree)
    if changes and not args.write:
        print("OK with normalizable issues:")
        for change in changes:
            print(f"- {change}")
    else:
        print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
