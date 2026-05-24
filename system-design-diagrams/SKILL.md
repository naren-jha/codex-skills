---
name: system-design-diagrams
description: Create clean editable system design architecture diagrams for HLD/LLD work, especially backend microservice, data flow, event-driven, database ownership, and design-interview diagrams. Use when the user asks for a system design diagram, architecture diagram, HLD, LLD, service diagram, backend design, or iterative refinement of a Draw.io system design diagram.
---

# System Design Diagrams

Use this skill to turn system design discussions into editable architecture diagrams. This skill defines the architecture and layout judgment; use the `drawio-diagrams` skill for Draw.io XML generation, validation, and browser preview.

## Workflow

1. Identify the diagram scope:
   - Backend-only service architecture
   - Request/data flow
   - Event-driven workflow
   - Storage ownership
   - Infrastructure topology
   - Sequence-like interaction
2. Make an opinionated architecture pass before drawing. If a requested component split is weak, call it out briefly and choose the cleaner design.
3. Prefer backend-only diagrams by default. Omit client apps, API gateways, load balancers, CDNs, and edge boxes unless they are central to the question.
4. Create the diagram with `drawio-diagrams`.
5. Validate with the Draw.io validator.
6. Run a quick geometry/readability pass before delivery:
   - no service/database boxes overlap
   - related boxes have at least ~40 px of spacing
   - connectors do not pass through unrelated boxes
   - labels remain readable at the browser's default preview zoom
7. When the user asks to view, launch, preview, or iterate visually, open the diagram in the Codex in-app browser in editable diagrams.net mode. Prefer the existing launcher pattern that encodes the `.drawio` file into `https://app.diagrams.net/?offline=1&proto=json&ui=atlas#R...`; do not settle for a static PNG/SVG preview.
8. If the user manually edits an encoded diagrams.net browser tab, save the browser state back to the `.drawio` source before reopening or regenerating. Decode the current `#R...` URL or use the exported `.drawio`, overwrite the local file, validate it, and sync any generator script so manual routing survives regeneration.
9. After opening or refreshing an editable diagram, inspect a browser screenshot before saying the diagram is done. Draw.io validation is necessary but not enough; visual QA should catch cramped labels, line crossings, arrows over components, accidental overlap, and stale browser views.

## Repository Artifact Pattern

When creating Draw.io system design diagrams for a project, leave a reproducible repo-local artifact set:

- Put canonical diagram sources under `docs/diagrams/` unless the project already has a clear diagram folder convention.
- Keep individual `.drawio` files for independently editable diagrams or pages.
- When there are multiple related diagrams, create or update a Python combiner script such as `combine-drawio-pages.py` that builds one multi-page `.drawio` file from the individual sources.
- Create or update a Python launcher script such as `refresh-drawio-launcher.py` that encodes the latest `.drawio` into an editable diagrams.net URL with a content-based fresh/cache-busting token.
- Write the generated launcher HTML back into the diagrams folder, using a name like `open-<diagram-set>.html`, so the user can reopen the latest editable diagram later.
- After any diagram XML change, rerun the combiner and launcher scripts, validate the resulting `.drawio`, and use the HTML launcher for browser review.

## Layout Defaults

- Use free-floating components for early editable HLDs. Avoid large containers/swimlanes unless grouping materially clarifies ownership or runtime boundaries.
- Put each service-owned database next to the service that owns it.
- Use database cylinder shapes for DBs. In Draw.io XML, prefer `shape=mxgraph.flowchart.database` for bounded database cylinders; avoid plain `shape=cylinder` if it visually overlaps nearby nodes.
- Keep ownership links short and direct. Label them `owns` only when helpful.
- Route cross-service flows with orthogonal connectors. Avoid diagonal spaghetti and crossing lines.
- For high-fanout components such as API layers, event buses, fanout workers, orchestrators, or notification dispatchers, use routing gutters or bus-style trunks. Route edges orthogonally through shared vertical/horizontal lanes, then branch into target services instead of spraying direct diagonal edges from the hub.
- Keep fanout trunks only as long as the group they serve. Do not let a storage trunk visually cover unrelated nodes; allow short bends into the trunk when that reduces overlap.
- Put synchronous/request flow in the center. Put async/event flow below or on a separate lane, with dashed event lines routed through side gutters instead of through service boxes.
- For event buses, separate producer and consumer routing when possible: producers enter the bus from one side/top, consumers exit through a shared gutter, and dashed event lines avoid service/database bodies.
- For LLD diagrams with both persistence access and internal module dependencies, use separate visual lanes: solid gray orthogonal lines for database/storage access, dashed colored lines for module relationships. Do not overlap dashed dependency lines with solid database lines.
- Route dependency arrows from the side or edge of a module, not through the module body or label text. Prefer right-side/left-side ports, side gutters, and short orthogonal turns over center-crossing arrows.
- For dense module relationships, show only the relationships that explain design decisions, such as read contracts, access checks, or signal flow. Put routine or repeated dependencies into an "Internal contracts" note instead of drawing every possible arrow.
- Give relationship labels small filled backgrounds when the diagram uses a dark canvas or grid. Place labels close to their dashed line segment and away from database lines so the owner line is unambiguous.
- For diagrams with 8+ services or several storage nodes, start with a wide canvas (roughly 2200-2600 px) rather than squeezing the design into a compact page.
- Keep external dependencies, such as payment providers or maps providers, visually distinct from internal services.
- Avoid nesting cards or putting every backend component inside one large box when the user is actively editing the design.

For detailed layout rules, read `references/layout-rules.md`.

## Architecture Defaults

- Services own their databases. Do not draw one service reading another service's database directly unless the design is intentionally showing a flaw.
- Prefer API/event contracts between services over shared tables.
- Use events for lifecycle transitions that should not block the main request path, such as `BookingCreated`, `DriverAssigned`, `TripCompleted`, and `PaymentCaptured`.
- Show queues/topics only when async behavior, retries, or fanout matter to the discussion.
- Prefer fewer, more meaningful cross-service arrows. Show the main request paths and important lifecycle events; omit relationships that are merely technically possible when they make the HLD harder to read.
- Include caches, indexes, geo stores, stream processors, or schedulers only when they explain a real system property.
- For payments, separate customer charge flow from driver payout flow unless the user explicitly wants a simplified view.
- Add a short design note only when it captures an important decision or risk.

For architecture review prompts, read `references/review-heuristics.md`.

## Iteration Style

- Treat diagrams as living design artifacts. Make small, high-signal changes rather than redrawing everything on every request.
- Preserve existing labels and visual language unless the user asks for a redesign.
- After visual feedback, inspect the screenshot/browser state, then update the XML source and regenerate the launcher.
- For Draw.io work, keep the browser view editable. Regenerate the launcher HTML after each XML change, then reload it through the Browser Use in-app browser workflow.
- If a shape renders poorly in diagrams.net, choose a more reliable Draw.io primitive over arguing with the original style.
- Validation is mandatory before final delivery.

## Dense Diagram QA

For dense Draw.io diagrams, run these checks before finalizing:

- Do a line-ownership pass: every connector label should clearly belong to exactly one connector.
- Prefer labels on horizontal connector segments; avoid ambiguous labels on tight vertical segments.
- Compare the opened browser view against any user-provided reference screenshot, especially around the commented or selected region.
- Verify the browser-rendered diagram, not only XML validity.
- When refreshing HTML launchers, rebuild with a fresh cache-busting token and mention when a stale diagrams.net tab may still be showing an older encoded diagram.

## Final Visual QA Checklist

Before final delivery, verify the rendered diagram, not only the XML:

- No components overlap, including service boxes placed near database cylinders.
- No connector crosses through the body of an unrelated component.
- Major flows have enough whitespace to be followed without zooming in excessively.
- Text labels are legible in the in-app browser screenshot.
- Async/event flow is visually separated from synchronous request flow.
- The diagram shows useful architecture decisions rather than every possible dependency.
