# Layout Rules

## Backend HLD

- Use a left-to-right or top-to-bottom grid. Keep rows meaningful.
- Pair each service with its owned database:
  - Service on the left, DB on the right for service ownership rows.
  - Related service groups can sit in the same horizontal band.
- Keep at least 40 px between database cylinders when stacked vertically.
- Keep at least 40 px between any unrelated shapes. Use 60-100 px around worker services, queues, external dependencies, or service/database pairs with multiple connectors.
- For HLDs with 8+ services or several storage nodes, default to a 2200-2600 px wide canvas before compressing the layout.
- Use orthogonal connectors with explicit waypoints for event/payment lines.
- Route long async/event connectors through side gutters or a bottom lane. Avoid running dashed event lines through the center of service boxes.
- Treat high-fanout nodes as routing problems:
  - Use a shared vertical or horizontal gutter/trunk near API gateways, event buses, fanout workers, orchestrators, and notification dispatchers.
  - Route edges orthogonally into the gutter, then branch horizontally/vertically into target services.
  - Avoid direct diagonal spray from the hub to many targets.
  - Keep producer and consumer lanes visually separate for event buses when space allows.
- Avoid long ownership lines across the canvas. Long lines should usually mean the DB is in the wrong place.

## Shape Choices

- Service: rounded rectangle.
- Database: `shape=mxgraph.flowchart.database`.
- Queue/topic: dashed rounded rectangle.
- External dependency: warm/yellow rounded rectangle.
- Note: small note shape at the bottom or side.

## Connector Choices

- Solid line: direct synchronous call or ownership.
- Dashed line: async event, pub/sub, retry, delayed settlement.
- Thick line: primary happy path.
- Label only important edges. Too many labels make HLDs noisy.

## Anti-Patterns

- Huge containers around every backend component during early iteration.
- Client apps and API gateway in every diagram by habit.
- Database column on the far right with all ownership lines crossing the whole canvas.
- Shared database drawn as a neutral shortcut when service ownership is a stated goal.
- Diagonal lines between many components.
- Lines that pass through boxes or labels, even when Draw.io considers the XML valid.
- High-fanout hubs with many direct diagonal arrows instead of a clear routing trunk/gutter.
- Declaring a diagram done from XML validation alone without checking an editable browser screenshot.
