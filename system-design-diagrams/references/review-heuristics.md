# Review Heuristics

Use these checks before finalizing a system design diagram.

## Ownership

- Does every database have exactly one owning service?
- Are any services bypassing another service by reading its DB?
- Are ledgers, trip state, identity, pricing rules, and allocation attempts clearly owned?

## Flow

- Is the main happy path easy to follow without reading every label?
- Are async events visually distinct from synchronous calls?
- Are retries, fanout, or eventual consistency shown only where relevant?

## Scope

- Did the diagram include only components needed for the current discussion?
- Are clients, API gateways, and infrastructure omitted when the conversation is backend domain design?
- Are external systems shown only when they affect the design?

## Editability

- Are shapes free-floating and easy to move?
- Are containers avoided unless they add clarity?
- Are connectors orthogonal and minimally crossed?
- Are rendered Draw.io shapes visually stable in the browser preview?

## Opinionated Design Notes

- If the user proposes a weak split, say so briefly and choose the cleaner model.
- If the design is missing a core production concern, add it only when it materially affects the diagram.
- Do not force balance between options when one architecture is clearly better for the stated goal.
