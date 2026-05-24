# Excalidraw Diagram Palette

Use these colors unless the user provides a brand palette or an existing diagram already has a stronger local style.

| Purpose | Stroke | Fill | Text |
|---|---:|---:|---:|
| Primary system/service | `#1d4ed8` | `#dbeafe` | `#0f172a` |
| User/client | `#047857` | `#d1fae5` | `#064e3b` |
| Data/store/state | `#7c3aed` | `#ede9fe` | `#3b0764` |
| External dependency | `#b45309` | `#fef3c7` | `#78350f` |
| Risk/error/failure | `#be123c` | `#ffe4e6` | `#881337` |
| Success/output | `#15803d` | `#dcfce7` | `#14532d` |
| Neutral group/region | `#64748b` | `#f8fafc` | `#334155` |
| Evidence artifact | `#334155` | `#0f172a` | `#e2e8f0` |
| Secondary note | `#475569` | `#f1f5f9` | `#475569` |

## Usage

- Pair light fills with darker strokes. Avoid transparent fills for primary structure.
- Use dark evidence artifacts for code, JSON, logs, SQL, endpoint examples, and config snippets.
- Use neutral group regions behind components sparingly; keep their fill light enough that child elements remain dominant.
- Use red/pink only for actual failures, risks, alerts, or blocked states.
- Keep arrows neutral (`#334155`) unless color is needed to distinguish competing flows.
