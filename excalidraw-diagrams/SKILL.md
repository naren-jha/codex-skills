---
name: excalidraw-diagrams
description: Generate, edit, and validate editable Excalidraw diagrams as .excalidraw JSON or Obsidian Excalidraw Markdown. Use when Codex is asked to create architecture diagrams, flowcharts, sequence-like process diagrams, mind maps, concept maps, system designs, dependency maps, whiteboard sketches, or to update an existing Excalidraw file.
---

# Excalidraw Diagrams

Create editable Excalidraw diagrams that communicate structure, flow, and tradeoffs. Prefer standard `.excalidraw` output unless the user asks for Obsidian, Markdown embedding, or an existing `.md` Excalidraw note.

## Workflow

1. Determine the output mode:
   - Standard: save `<name>.excalidraw` with Excalidraw JSON.
   - Obsidian: save `<name>.md` containing Excalidraw frontmatter plus an embedded JSON code block.
   - Clipboard: provide `type: "excalidraw/clipboard"` JSON only when the user asks for paste-ready content.
   - Browser preview: open Excalidraw or a local preview helper when the user asks to view the diagram in the Codex browser.
2. Read the source material. For codebase architecture diagrams, inspect relevant files before drawing.
3. Choose a diagram pattern from `references/diagram-patterns.md`.
4. Use colors from `references/color-palette.md`. Do not invent a new palette unless the user provides one.
5. Generate valid Excalidraw JSON with stable ids, readable layout, and connected arrows.
6. Run `scripts/validate_excalidraw.py <file> --write` on saved `.excalidraw` or Obsidian `.md` files.
7. Report the saved file path, validation result, and any meaningful assumptions.

## Design Rules

- Make the diagram argue visually, not just label boxes. If removing text leaves no visible structure, redesign.
- Use concrete labels for technical diagrams: real service names, APIs, events, tables, commands, or data shapes.
- Boxes named only "service", "database", or "queue" are too vague; use concrete service names, APIs, topics, tables, caches, jobs, and external dependencies.
- Keep layout on a loose 20 px grid. Favor left-to-right for request/data flow, top-to-bottom for lifecycle/process flow, radial for concepts, and grouped regions for architecture.
- Use section boundaries for ownership or runtime boundaries: Client, Edge, API, Services, Workers, Data, External, Observability, Security.
- Put the happy path in the center with the strongest arrows. Put retries, failures, async processing, and monitoring below or to the side.
- Label important arrows with protocol, route, event, topic, command, or data shape, such as `POST /checkout`, `OrderCreated`, `CDC stream`, or `read-through cache`.
- Prefer concise text. Put details in small evidence artifacts such as mini code blocks, sample JSON, table fragments, or endpoint labels.
- Avoid decorative complexity. Excalidraw can get charmingly messy; for technical architecture, use icons only when they identify a technology boundary faster than text.
- Use `roughness: 0` for professional technical diagrams and `roughness: 1` only for informal whiteboard sketches.
- Use `strokeWidth: 2` for shapes, `strokeWidth: 3` for the primary flow, and `strokeWidth: 1` for dividers or secondary links.
- Use `fontFamily: 5` for Excalidraw's default readable handwritten font unless matching an existing file.
- Bind arrows to elements with `startBinding` and `endBinding` when practical. Keep arrow points relative to the arrow origin.
- Avoid overlapping elements. Leave at least 24 px between boxes and 48 px between major groups.

## File Requirements

For standard files, write JSON with:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

Each element should include the Excalidraw fields needed for editability: `id`, `type`, `x`, `y`, `width`, `height`, `angle`, `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `strokeStyle`, `roughness`, `opacity`, `groupIds`, `frameId`, `roundness`, `seed`, `version`, `versionNonce`, `isDeleted`, `boundElements`, `updated`, and `link`.

Text elements also need `text`, `fontSize`, `fontFamily`, `textAlign`, `verticalAlign`, `containerId`, `originalText`, `lineHeight`, and `baseline`.

Line and arrow elements also need `points`, `lastCommittedPoint`, `startBinding`, `endBinding`, `startArrowhead`, and `endArrowhead`.

## Editing Existing Diagrams

- Preserve existing ids, bindings, styles, and file format unless the user asks for a redesign.
- Load the existing file, make the smallest useful change, then validate it.
- If an existing diagram has a clear local style, follow it over this skill's default palette.

## Browser Workflow

When the user wants to open or inspect an Excalidraw diagram in the in-app Codex browser:

1. Prefer a local HTML preview helper if one exists for the generated diagram.
2. Otherwise open Excalidraw and import the generated `.excalidraw` file manually or through available browser automation.
3. For visual QA, inspect the rendered diagram, not only the JSON. Check for overlapping boxes, unreadable text, unbound arrows, and arrows crossing through unrelated elements.

Do not use macOS `open` for this; use the Browser Use plugin or in-app browser tool when available.

## Validation

Run:

```bash
python3 /Users/narendrajha/.codex/skills/excalidraw-diagrams/scripts/validate_excalidraw.py path/to/diagram.excalidraw --write
```

Use `--write` to normalize missing top-level fields and `appState` defaults. If validation reports geometry or required-field problems, fix the diagram before delivering it.
