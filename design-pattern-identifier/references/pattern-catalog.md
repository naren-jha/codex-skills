# Pattern Catalog

Use this catalog after reading code signals. Pick the smallest pattern that explains the smell and reduces future modification.

## 1. Strategy

- **Use when**: A family of algorithms share the same input/output contract and callers choose one by type, context, tenant, channel, or configuration.
- **Code smell**: Large `switch`/`if` block over data type, payment method, file format, scoring rule, pricing rule, parser, exporter, or provider.
- **Simplifies by**: Moving each algorithm behind a common interface so adding a new variant adds a class, not a branch.
- **Java sketch**: `interface PaymentStrategy { Receipt pay(PaymentRequest request); }` plus a registry keyed by payment method.
- **Avoid when**: There are only two tiny branches and no real extension pressure.

## 2. Factory Method / Abstract Factory

- **Use when**: Object creation varies by environment, product family, provider, or runtime type.
- **Code smell**: Constructors and setup logic duplicated across services; callers know too much about concrete classes.
- **Simplifies by**: Centralizing creation and keeping callers dependent on an interface.
- **Java sketch**: `NotificationSender sender = senderFactory.forChannel(channel);`
- **Avoid when**: The caller can cleanly call one constructor.

## 3. Builder

- **Use when**: Creating an object requires many optional fields, validation, defaults, or readable staged construction.
- **Code smell**: Long constructor argument lists, telescoping constructors, repeated setup blocks in tests.
- **Simplifies by**: Making construction explicit and preventing invalid partially built objects.
- **Java sketch**: Prefer records for simple immutable values; use builders for complex aggregate creation.
- **Avoid when**: A record, constructor, or static factory is already clear.

## 4. Template Method

- **Use when**: Multiple classes follow the same algorithm skeleton but override specific steps.
- **Code smell**: Repeated `validate -> transform -> persist -> notify` flow with small differences.
- **Simplifies by**: Keeping the invariant sequence in one place.
- **Java sketch**: Abstract base class with final orchestration method and protected hooks.
- **Avoid when**: Composition would be clearer or inheritance is already causing rigidity.

## 5. State

- **Use when**: An object's behavior changes according to lifecycle state and transitions matter.
- **Code smell**: `status` checks scattered across methods; invalid flag combinations; transition rules duplicated.
- **Simplifies by**: Moving state-specific behavior into state objects and making transitions explicit.
- **Java sketch**: `OrderState` interface with `Pending`, `Paid`, `Shipped`, `Cancelled` implementations.
- **Avoid when**: The state is only display data or a simple enum with no behavior.

## 6. Chain of Responsibility

- **Use when**: A request passes through a sequence of handlers and each handler may handle, modify, reject, or pass it on.
- **Code smell**: Long validation/routing/fallback method; nested checks where order is meaningful.
- **Simplifies by**: Isolating each handler and enabling handler composition.
- **Java sketch**: `interface Handler { Optional<Result> handle(Request request, Chain next); }`
- **Avoid when**: Every step always runs; a simple pipeline/list of functions may be clearer.

## 7. Command

- **Use when**: Operations need to be stored, queued, retried, logged, authorized, undone, or scheduled.
- **Code smell**: Methods pass action names plus parameter maps; queue payloads require special-case dispatch.
- **Simplifies by**: Encapsulating an action as an object with its inputs and execution behavior.
- **Java sketch**: `interface Command { CommandResult execute(); }`
- **Avoid when**: The operation is invoked immediately and never needs identity.

## 8. Observer / Event Publisher

- **Use when**: One change should notify multiple independent listeners.
- **Code smell**: Core service directly sends email, writes audit logs, updates metrics, invalidates cache, and calls webhooks.
- **Simplifies by**: Decoupling the event source from side effects.
- **Java sketch**: Publish `OrderPlacedEvent`; subscribers handle email, analytics, fulfillment.
- **Avoid when**: Side effects are required for the transaction to be valid and must stay explicit.

## 9. Decorator

- **Use when**: Optional behavior should wrap a core interface without changing the core implementation.
- **Code smell**: Subclass explosion for combinations like cached, logged, retried, metered, validated.
- **Simplifies by**: Composing behavior layers around the same interface.
- **Java sketch**: `CachingPriceClient implements PriceClient` and delegates to another `PriceClient`.
- **Avoid when**: One wrapper is enough and a named helper is clearer.

## 10. Adapter

- **Use when**: A third-party, legacy, or incompatible API must fit a local interface.
- **Code smell**: Vendor DTOs and method names leak across domain services.
- **Simplifies by**: Keeping the rest of the codebase dependent on a stable local contract.
- **Java sketch**: `StripePaymentAdapter implements PaymentGateway`.
- **Avoid when**: The external API is already isolated at one call site.

## 11. Facade

- **Use when**: Clients must coordinate a subsystem through many low-level calls.
- **Code smell**: Several callers repeat the same orchestration across repositories, clients, validators, and mappers.
- **Simplifies by**: Providing one intention-revealing entry point for common workflows.
- **Java sketch**: `CheckoutFacade.placeOrder(command)` hides inventory, payment, discount, and shipment coordination.
- **Avoid when**: It becomes a dumping-ground service.

## 12. Proxy

- **Use when**: Access to another object needs control: lazy loading, authorization, remote calls, rate limiting, caching, or instrumentation.
- **Code smell**: Callers repeat permission checks, connection setup, caching, or retry around the same dependency.
- **Simplifies by**: Putting access policy at the boundary while preserving the same interface.
- **Java sketch**: `AuthorizedDocumentRepository implements DocumentRepository`.
- **Avoid when**: The wrapper changes behavior compositionally; Decorator may be clearer.

## 13. Composite

- **Use when**: Individual objects and groups should be treated uniformly.
- **Code smell**: Recursive tree logic with separate code paths for leaf and group operations.
- **Simplifies by**: Giving leaves and composites the same interface.
- **Java sketch**: `Rule` implemented by `SingleRule` and `RuleGroup`.
- **Avoid when**: The group behavior is not meaningfully the same as leaf behavior.

## 14. Visitor

- **Use when**: A stable object structure needs many new operations without modifying each class every time.
- **Code smell**: Type checks over a hierarchy for export, validation, reporting, rendering, or pricing.
- **Simplifies by**: Moving operations out of the element classes while keeping double-dispatch type safety.
- **Java sketch**: `Shape.accept(ShapeVisitor visitor)` with `AreaVisitor`, `SvgExportVisitor`.
- **Avoid when**: New element types are more common than new operations.

## 15. Mediator

- **Use when**: Peer objects know too much about each other and coordination rules are spread across them.
- **Code smell**: Many-to-many service calls, UI components toggling each other, workflow steps directly manipulating peers.
- **Simplifies by**: Moving coordination into a dedicated object that expresses the workflow.
- **Java sketch**: `BookingCoordinator` mediates seat hold, payment, ticketing, and notification.
- **Avoid when**: It becomes a god object; keep domain rules near the domain when possible.

## Singleton Guidance

Treat Singleton as a lifecycle constraint, not a default simplification pattern.

- **Consider only when**: There must be exactly one instance per process and the instance is stateless, immutable, or manages a real shared resource.
- **Prefer first**: Dependency injection scopes, application configuration, enum singleton for tiny stateless utilities, or a factory/provider.
- **Avoid for**: Mutable business state, caches without clear invalidation, test-sensitive dependencies, and anything that hides coupling.
- **Java rule of thumb**: In Spring/Guice-style systems, the container's singleton scope is usually better than implementing the Singleton pattern manually.

## Choosing Between Close Patterns

- **Strategy vs State**: Strategy selects an algorithm; State models lifecycle behavior and transitions.
- **Strategy vs Command**: Strategy is chosen and executed; Command is an action object that can be stored, queued, undone, or audited.
- **Factory vs Builder**: Factory chooses which object to create; Builder manages how to assemble a complex object.
- **Decorator vs Proxy**: Decorator adds optional behavior; Proxy controls access to an underlying object.
- **Adapter vs Facade**: Adapter changes an interface; Facade simplifies a subsystem.
- **Template Method vs Strategy**: Template Method uses inheritance to vary steps; Strategy uses composition to vary the whole algorithm or step.
- **Observer vs Mediator**: Observer broadcasts events to independent listeners; Mediator coordinates collaborators in a workflow.
