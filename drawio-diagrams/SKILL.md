---
name: drawio-diagrams
description: Generate, edit, validate, and preview editable Draw.io diagrams as .drawio XML for system design and software architecture. Use when Codex is asked to create diagrams.net or Draw.io files, system design diagrams, architecture diagrams, network diagrams, cloud diagrams, flowcharts, sequence-like flows, data-flow diagrams, dependency maps, or to update an existing .drawio file.
---

# Draw.io Diagrams

Create editable Draw.io diagrams for system design and software architecture. Prefer uncompressed `.drawio` XML so Codex can inspect, edit, diff, and validate diagrams directly.

## Workflow

1. Determine the output mode:
   - Standard: save `<name>.drawio` as uncompressed diagrams.net XML.
   - Existing file: preserve the file's format and local style unless a redesign is requested.
   - Browser preview: open `https://app.diagrams.net/?offline=1&proto=json` or a local preview helper when the user asks to view it in the Codex browser.
2. Read the source material. For codebase or system design diagrams, inspect relevant files before drawing.
3. Choose a diagram pattern from `references/diagram-patterns.md`.
4. Use colors and style strings from `references/style-guide.md` unless the user provides a brand or cloud-provider style.
5. Generate valid Draw.io XML with stable ids, readable geometry, and connected edges.
6. Run `scripts/validate_drawio.py <file> --write` on saved `.drawio` files.
7. Report the saved file path, validation result, and any meaningful assumptions.

## Design Rules

- Make the diagram useful for an engineering discussion. Boxes named only "service", "database", or "queue" are too vague; use concrete service names, APIs, topics, tables, caches, jobs, and external dependencies.
- Use a grid-like layout. Favor left-to-right for request/data flow, top-to-bottom for lifecycle/process flow, and grouped swimlanes for ownership or runtime boundaries.
- Use containers for major zones: Client, Edge, API, Services, Workers, Data, External, Observability, Security.
- Put the happy path in the center with the strongest arrows. Put retries, failures, async processing, and monitoring below or to the side.
- Label important edges with protocol, event, topic, route, or data shape, such as `POST /checkout`, `OrderCreated`, `CDC stream`, or `read-through cache`.
- Add small evidence artifacts where they help: sample JSON, table names, endpoint lists, queue names, or SLA notes.
- Avoid decorative complexity. Draw.io can become a landfill of icons; use icons only when they identify a technology boundary faster than text.
- Keep at least 24 px between sibling shapes and 48 px between major groups.

## File Requirements

Write uncompressed XML in this shape:

```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram id="page-1" name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Use one `mxCell` per shape or edge:

- Shape cells require `id`, `value`, `style`, `vertex="1"`, `parent="1"`, and child `mxGeometry` with numeric `x`, `y`, `width`, `height`, and `as="geometry"`.
- Edge cells require `id`, `value`, `style`, `edge="1"`, `parent="1"`, `source`, `target`, and child `mxGeometry` with `relative="1"` and `as="geometry"`.
- Container cells are vertex cells with swimlane or rounded rectangle styles. Child shapes may use the container id as `parent` when useful.
- Escape XML special characters in labels: `&amp;`, `&lt;`, `&gt;`, `&quot;`.

## Editing Existing Diagrams

- Preserve ids, pages, styles, and compression format unless the user asks for a clean rewrite.
- For compressed Draw.io files, either use diagrams.net tooling if available or make a careful uncompressed copy and tell the user the format changed.
- Add or update the smallest useful set of cells, then validate.
- Follow the existing diagram's local color, icon, and spacing choices when they are coherent.

## Browser Workflow

When the user wants to open diagrams in the in-app Codex browser:

1. Open diagrams.net with `https://app.diagrams.net/?offline=1&proto=json`.
2. The user can choose Device and import the generated `.drawio` file.
3. If a local HTML preview helper exists for the generated diagram, prefer opening that file in the in-app browser for quick inspection, then use diagrams.net for editing.

Do not use macOS `open` for this; use the Browser Use plugin or in-app browser tool when available.

## Validation

Run:

```bash
python3 /Users/narendrajha/.codex/skills/drawio-diagrams/scripts/validate_drawio.py path/to/diagram.drawio --write
```

Use `--write` to add missing safe top-level defaults. If validation reports XML, geometry, duplicate id, or missing endpoint problems, fix the diagram before delivering it.
