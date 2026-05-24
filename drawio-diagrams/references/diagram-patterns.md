# Diagram Patterns

Choose the pattern that matches the user's system design task. Keep one dominant layout grammar so the result feels intentional.

## System Architecture

Use for services, deployments, codebases, cloud systems, and product architecture.

- Arrange the happy path left-to-right: client, edge, API, services, data, external systems.
- Place async workers, queues, retries, and schedulers below the synchronous path.
- Place observability and security controls in a separate lower or side lane.
- Use containers for runtime or ownership boundaries.
- Label critical edges with protocol, route, event, queue/topic, or data shape.

## Data Flow

Use when the user's focus is ingestion, transformation, analytics, replication, or consistency.

- Put sources on the left, transformations in the middle, and sinks/consumers on the right.
- Use cylinders for durable storage and dashed edges for async or eventual consistency.
- Add artifact notes for schema names, table names, retention, partitioning, or SLA.

## Network / Cloud Topology

Use when infrastructure boundaries matter.

- Group by VPC, subnet, region, account, cluster, or environment.
- Show public entry points clearly.
- Separate control plane and data plane when relevant.
- Use security or policy nodes only where they affect flow.

## Flowchart

Use for user journeys, operational procedures, business logic, and state machines.

- Use rounded rectangles for start/end, rectangles for actions, diamonds for decisions.
- Keep one dominant direction.
- Label branches with concise conditions: `valid`, `invalid`, `timeout`, `retry`, `approved`.

## Sequence-Like Interaction

Use when order matters but a formal sequence diagram is unnecessary.

- Arrange actors as vertical lanes or columns.
- Stack numbered arrows top-to-bottom.
- Put payload, error, or retry details next to the relevant arrow.

## Dependency Map

Use for modules, packages, ownership, build systems, or service dependencies.

- Place upstream dependencies on the left/top and dependents on the right/bottom.
- Use thicker or colored edges for critical or risky dependencies.
- Add annotations for version locks, shared databases, cyclic dependencies, or migration risks.
