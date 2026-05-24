# Draw.io Style Guide

Use these styles unless the user provides a brand palette or an existing `.drawio` file already has a coherent style.

## Palette

| Purpose | Stroke | Fill | Text |
|---|---:|---:|---:|
| Primary service | `#1d4ed8` | `#dbeafe` | `#0f172a` |
| Client/user | `#047857` | `#d1fae5` | `#064e3b` |
| Data/store/state | `#7c3aed` | `#ede9fe` | `#3b0764` |
| External dependency | `#b45309` | `#fef3c7` | `#78350f` |
| Risk/error/failure | `#be123c` | `#ffe4e6` | `#881337` |
| Success/output | `#15803d` | `#dcfce7` | `#14532d` |
| Neutral group/region | `#64748b` | `#f8fafc` | `#334155` |
| Evidence artifact | `#334155` | `#0f172a` | `#e2e8f0` |
| Secondary note | `#475569` | `#f1f5f9` | `#475569` |

## Shape Styles

Use compact Draw.io style strings. Keep font sizes readable.

- Primary service:
  `rounded=1;whiteSpace=wrap;html=1;arcSize=10;strokeWidth=2;strokeColor=#1d4ed8;fillColor=#dbeafe;fontColor=#0f172a;fontSize=14;`
- Client/user:
  `rounded=1;whiteSpace=wrap;html=1;arcSize=10;strokeWidth=2;strokeColor=#047857;fillColor=#d1fae5;fontColor=#064e3b;fontSize=14;`
- Data store:
  `shape=cylinder3d;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;strokeWidth=2;strokeColor=#7c3aed;fillColor=#ede9fe;fontColor=#3b0764;fontSize=14;`
- Queue/topic:
  `rounded=1;whiteSpace=wrap;html=1;arcSize=50;strokeWidth=2;dashed=1;strokeColor=#7c3aed;fillColor=#ede9fe;fontColor=#3b0764;fontSize=14;`
- External dependency:
  `rounded=1;whiteSpace=wrap;html=1;arcSize=10;strokeWidth=2;strokeColor=#b45309;fillColor=#fef3c7;fontColor=#78350f;fontSize=14;`
- Group container:
  `swimlane;whiteSpace=wrap;html=1;startSize=32;horizontal=1;rounded=1;arcSize=6;strokeWidth=1;strokeColor=#64748b;fillColor=#f8fafc;fontColor=#334155;fontSize=13;`
- Evidence artifact:
  `rounded=1;whiteSpace=wrap;html=1;arcSize=6;strokeWidth=1;strokeColor=#334155;fillColor=#0f172a;fontColor=#e2e8f0;fontFamily=Courier New;fontSize=12;align=left;spacing=8;`
- Note:
  `shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;strokeColor=#475569;fillColor=#f1f5f9;fontColor=#475569;fontSize=12;align=left;spacing=8;`

## Edge Styles

- Primary request/data flow:
  `endArrow=block;html=1;rounded=0;strokeWidth=3;strokeColor=#334155;fontColor=#334155;fontSize=12;`
- Secondary flow:
  `endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#64748b;fontColor=#475569;fontSize=12;`
- Async/event flow:
  `endArrow=block;html=1;rounded=0;strokeWidth=2;dashed=1;strokeColor=#7c3aed;fontColor=#3b0764;fontSize=12;`
- Failure/retry flow:
  `endArrow=block;html=1;rounded=0;strokeWidth=2;dashed=1;strokeColor=#be123c;fontColor=#881337;fontSize=12;`

## Labeling

- Use line breaks with `<br>` inside labels.
- Keep title text first and concrete details second: `Checkout API<br><font style="font-size: 11px">POST /checkout</font>`.
- Use edge labels for protocols, routes, events, and data shape. Do not label every arrow when the flow is obvious.
