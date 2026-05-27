# Pattern Signals

Use this file before choosing a pattern. First identify the code smell, then map it to a small candidate set. Do not recommend a pattern when ordinary extraction, naming, or dependency cleanup would solve the problem.

## Signal Map

| Code signal | Look for | Candidate patterns | Usually avoid |
|---|---|---|---|
| Family of algorithms | `switch`/`if` by type, mode, channel, provider, payment method, export format; same method shape with different internals | Strategy, Template Method, Command | Factory alone; it creates variants but does not remove algorithm branching |
| Shared algorithm skeleton | Same ordered steps with a few varying steps; duplicated validation/process/save flow | Template Method, Strategy | Template Method when inheritance is already painful |
| Complex object creation | Repeated constructor sequences, optional parameter sprawl, environment-specific object graphs | Builder, Factory, Abstract Factory | Builder for simple DTOs or records |
| State-dependent behavior | Flags like `status`, `mode`, `phase`; invalid combinations; methods full of transition checks | State, State Machine, Strategy | Strategy when transitions and lifecycle are the real problem |
| Sequential handlers | Validation, routing, authorization, enrichment, fallback logic, middleware-like stages | Chain of Responsibility, Pipeline, Command | Chain when every handler always runs in a fixed order; use a simple pipeline |
| Work needs to be represented | Queueing, retrying, undo/redo, audit log, scheduled execution, request encapsulation | Command | Strategy when the operation must be stored or replayed |
| Event fan-out | One action triggers emails, logs, metrics, cache invalidation, webhooks, UI refresh | Observer, Event Publisher, Domain Events | Observer for required synchronous core logic |
| Wrapper behavior | Optional logging, caching, compression, validation, authorization, retry, metrics around a core object | Decorator, Proxy | Inheritance stacks for cross-cutting behavior |
| External or incompatible API | Vendor model leaks everywhere; mapping code scattered across services | Adapter, Facade, Anti-Corruption Layer | Adapter if callers already use a clean local interface |
| Bloated subsystem access | Callers must orchestrate many low-level calls in the right order | Facade | Facade that only renames one method |
| Access control or lazy boundary | Expensive object creation, remote call boundary, permission gate, caching, rate limiting | Proxy, Decorator | Proxy when the goal is only to add optional behavior to an object graph |
| Tree-like structure | Parts and wholes share operations: folders/files, org nodes, UI components, rules, expressions | Composite, Visitor | Composite if leaf and group behavior are genuinely unrelated |
| Stable object structure, many operations | Need reports, exports, validations, or calculations across a known class hierarchy | Visitor | Visitor when new element types are frequent |
| Tangled peer interactions | Many objects call each other directly; workflow rules spread across collaborators | Mediator, Facade, Domain Service | Mediator that becomes a new god object |
| Global lifecycle concern | One shared instance, expensive resource, process-wide registry, configuration holder | Dependency injection scope, Factory, Singleton as last resort | Singleton for mutable business state or test-sensitive dependencies |

## Decision Heuristics

- If the pain is **selecting behavior**, consider Strategy first.
- If the pain is **constructing objects**, consider Factory or Builder first.
- If the pain is **changing behavior over time**, consider State.
- If the pain is **communicating change**, consider Observer or Domain Events.
- If the pain is **hiding a messy dependency**, consider Adapter or Facade.
- If the pain is **adding behavior around behavior**, consider Decorator or Proxy.
- If the pain is **workflow orchestration**, consider Command, Chain of Responsibility, or Mediator.
- If the pain is **hierarchical structure**, consider Composite and maybe Visitor.

## Evidence To Collect

Before recommending a pattern, cite at least two of these:

- The branch or duplication that would disappear.
- The new variant likely to be added next.
- The interface boundary that callers should depend on.
- The construction or orchestration knowledge currently leaking to callers.
- The tests that become simpler or more focused after the pattern.
- The code that should remain closed when a new variant is added.

## Negative Signals

Recommend "No pattern yet" when:

- There are only one or two cases and no credible third case.
- The code is readable and unlikely to change.
- A simple helper method, interface extraction, enum method, or map lookup solves the issue.
- The proposed pattern adds more files than the complexity it removes.
- The team or codebase strongly favors a simpler local convention.
