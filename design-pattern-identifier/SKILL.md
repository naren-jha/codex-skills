---
name: design-pattern-identifier
description: Analyze code modules for design-pattern opportunities that simplify implementation and low-level design. Use when Codex is asked to identify, compare, recommend, or implement patterns such as Strategy, Factory, Builder, Template Method, State, Chain of Responsibility, Command, Observer, Decorator, Adapter, Facade, Proxy, Composite, Visitor, Mediator, or Singleton-like lifecycle choices; when refactoring conditionals, duplicated algorithms, object creation, event notifications, state transitions, wrappers, tree structures, tangled collaborations, or bloated service APIs; or when reviewing LLD/code for extensibility and maintainability.
---

# Design Pattern Identifier

## Core Rule

Recommend a design pattern only when it removes visible complexity or protects a credible near-term change. Prefer the smallest useful design over a textbook-perfect pattern.

Do not recommend more than two candidate patterns unless the user explicitly asks for a broad survey. Make one clear primary recommendation, name the tradeoff, and say when no pattern is worth adding.

## Workflow

1. Inspect the module before naming patterns:
   - Identify current responsibilities, public entry points, data types handled, dependencies, and change hotspots.
   - Look for repeated conditionals, duplicated object construction, parallel class hierarchies, temporal coupling, event fan-out, state flags, wrapper chains, or bloated APIs.
   - Check existing project conventions before introducing new abstractions.

2. Load references based on the task:
   - Read `references/pattern-signals.md` first when diagnosing a module from code smells.
   - Read `references/pattern-catalog.md` when choosing among candidate patterns or explaining the recommendation.
   - Use the references as filters, not checklists.

3. Score candidates with evidence:
   - **Fit**: Does the code smell match the pattern's intent?
   - **Payoff**: Does it remove branching, duplication, or unstable dependencies?
   - **Cost**: How many new types, interfaces, registrations, or tests does it introduce?
   - **Change pressure**: Is a new variant, algorithm, state, notification, or integration likely?

4. Choose the recommendation:
   - Prefer Strategy for varying algorithms behind the same operation.
   - Prefer Factory or Builder for messy construction, not for simple `new`.
   - Prefer State over scattered state flags and mode conditionals.
   - Prefer Facade when callers know too much about a subsystem.
   - Prefer no pattern when the module is small, stable, and readable.

5. Present the result in this shape:
   - **Recommendation**: one pattern, or "No pattern yet".
   - **Evidence**: concrete classes, methods, branches, or duplication from the code.
   - **Why this pattern**: the simplification it buys.
   - **Sketch**: small language-appropriate structure. For Java, prefer interfaces, records, enums, sealed types, and dependency injection where they fit the existing codebase.
   - **Migration plan**: 2-5 safe steps.
   - **Avoid**: one warning about overengineering or a competing pattern that would be worse.

## Implementation Guidance

When asked to refactor, implement the smallest vertical slice first: introduce the new abstraction, migrate one representative branch or variant, run tests, then finish the remaining variants.

For Java code, avoid hand-rolled service locators and global singletons. If a single shared instance is needed, prefer dependency injection scope or a well-contained factory/provider.

For LLD output, include class responsibilities and relationships. Keep diagrams or pseudocode focused on the pattern boundary, not the entire system.
