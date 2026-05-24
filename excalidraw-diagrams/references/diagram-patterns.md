# Diagram Patterns

Choose the pattern that matches the user's source material. Combine patterns when useful, but keep one dominant visual grammar.

## Architecture Map

Use for systems, codebases, deployments, services, and integrations.

- Group by runtime or ownership boundary: Client, Edge, API, Services, Workers, Data, External, Observability, Security.
- Show the main request/data path as the boldest left-to-right arrow chain.
- Put secondary paths, observability, retries, and async jobs below the main path.
- Label critical edges with protocol, route, event, queue/topic, command, or data shape.
- Include concrete evidence labels: endpoint paths, queue names, table names, topic names, package names.

## Data Flow

Use when the focus is ingestion, transformation, analytics, replication, consistency, or lineage.

- Put sources on the left, transformations in the middle, and sinks/consumers on the right.
- Use datastore-colored shapes for durable stores and dashed or lighter arrows for async/eventual consistency.
- Add small artifact notes for schema names, table names, retention, partitions, or SLA.

## Network / Cloud Topology

Use when infrastructure boundaries matter.

- Group by VPC, subnet, region, account, cluster, environment, or trust boundary.
- Show public entry points clearly.
- Separate control plane and data plane when relevant.
- Add security or policy nodes only where they affect flow.

## Flowchart

Use for procedures, business workflows, decision logic, and state transitions.

- Use rectangles for actions, diamonds for decisions, and rounded rectangles for start/end.
- Keep one entry point and one dominant direction.
- Label decision branches with short conditions such as `yes`, `no`, `timeout`, or `invalid`.

## Sequence-Like Flow

Use when timing and message order matter but a formal UML sequence diagram would be too rigid.

- Arrange actors as vertical lanes.
- Show numbered or stacked arrows from top to bottom.
- Put payload examples beside the relevant arrow when they teach something concrete.

## Mind Map / Concept Map

Use for brainstorming, research summaries, feature breakdowns, and strategy.

- Put the core idea in the center or left root.
- Use branches with labels rather than boxing every leaf.
- Group sibling concepts by color or proximity, not heavy containers.

## Dependency Map

Use for modules, packages, data lineage, build pipelines, or ownership.

- Place upstream sources on the left/top and downstream dependents on the right/bottom.
- Use fan-out for one source feeding many consumers.
- Use convergence for many inputs feeding one output.
- Mark risky or high-coupling edges with a stronger stroke and a short annotation, such as version locks, shared databases, cyclic dependencies, or migration risks.

## Evidence Artifacts

For technical diagrams, include at least one artifact when it improves understanding:

- API route or method names.
- Sample JSON event or message.
- Small SQL/table fragment.
- File path or module path.
- Config snippet.
- Error state or retry policy.

Artifacts should be small and legible. They are there to make the diagram specific, not to turn it into a document.
