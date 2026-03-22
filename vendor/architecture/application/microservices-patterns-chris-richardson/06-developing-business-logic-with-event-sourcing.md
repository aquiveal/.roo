# @Domain
These rules MUST be triggered when the user requests tasks, code generation, architectural designs, or refactoring related to **Event Sourcing**, **Domain-Driven Design (DDD) Aggregates**, **Event Stores**, **CQRS (Command Query Responsibility Segregation)**, or **Saga Integration** within a microservice architecture. Activation occurs when handling persistent domain objects as a sequence of events rather than traditional Object-Relational Mapping (ORM) state persistence.

# @Vocabulary
- **Event Sourcing**: A pattern that persists an aggregate as a sequence of domain events representing state changes, rather than persisting the current state.
- **Event Store**: A hybrid database and message broker that stores events by aggregate primary key and allows consumers to subscribe to event streams.
- **Aggregate (DDD)**: A cluster of domain objects treated as a unit, forming a consistency boundary. In Event Sourcing, it is rebuilt by replaying past events.
- **process() method**: A method on an aggregate that accepts a command, validates it, and generates a list of domain events without mutating the aggregate's state.
- **apply() method**: A method on an aggregate that takes a domain event and mutates the aggregate's internal state. It MUST NOT fail.
- **Snapshot**: A periodically saved serialized representation of an aggregate's state used to optimize loading performance by reducing the number of events that must be replayed.
- **Upcasting**: A mechanism to handle event schema evolution by transforming older versions of events into the newest version immediately upon loading from the event store.
- **Idempotency Key**: A unique identifier (usually a message ID) stored within generated events or a dedicated table to detect and discard duplicate messages.
- **Pseudo-event**: An event saved to the event store purely to record a message ID for idempotency or to trigger a side-effect (e.g., `SagaReplyRequested`), rather than representing a domain state change.
- **Event Relay / Transaction Log Tailing**: A mechanism that reads the database transaction log to reliably publish events stored in the database to a message broker (e.g., Apache Kafka).
- **Pseudonymization**: Replacing identifiable data (like an email address) with a UUID token to comply with GDPR's right to erasure in an immutable event store.

# @Objectives
- The AI MUST structure business logic entirely around the production and consumption of domain events.
- The AI MUST eliminate Object-Relational impedance mismatch and traditional CRUD updates, replacing them with event append operations.
- The AI MUST ensure robust idempotent message processing to handle at-least-once delivery semantics from message brokers.
- The AI MUST design event sourcing aggregates to seamlessly participate in and orchestrate Sagas for distributed transactions.
- The AI MUST ensure event schema evolution is safely managed without bloating domain aggregates.
- The AI MUST ensure compliance with data privacy laws (e.g., GDPR) in an immutable event store environment.

# @Guidelines

## 1. Aggregate Structure & Business Logic
- The AI MUST separate aggregate state mutation from business rule validation.
- When generating aggregate logic, the AI MUST define `process([Command])` methods that validate business rules and return a `List<Event>`. `process()` MUST NOT mutate state.
- When generating aggregate logic, the AI MUST define `apply([Event])` methods that take an event and update the aggregate's fields. `apply()` MUST NOT contain business logic validation and MUST NOT throw validation exceptions.
- The AI MUST ensure every state change, including creation, is represented by a specific domain event.
- The AI MUST ensure that domain events contain all data necessary for the `apply()` method to perform the state transition.

## 2. Event Store Interaction & Optimistic Locking
- To load an aggregate, the AI MUST generate code that: 1) loads events from the event store, 2) instantiates the aggregate using a default constructor, and 3) iterates through the events calling `apply()`.
- To handle concurrent updates, the AI MUST implement optimistic locking using an aggregate version number (either explicit or based on the event count) when appending new events.

## 3. Snapshotting for Performance
- For long-lived aggregates, the AI MUST implement snapshots.
- When using snapshots, the AI MUST load the most recent snapshot, instantiate the aggregate from the snapshot, and only replay events that occurred *after* the snapshot version.

## 4. Idempotent Message Processing
- The AI MUST ensure message handlers are idempotent to handle duplicate messages from brokers.
- When using an RDBMS event store, the AI MUST insert the processed message ID into a `PROCESSED_MESSAGES` table within the same transaction as the event insertion.
- When using a NoSQL event store, the AI MUST store the incoming message ID within the newly generated domain events.
- If a message processing step results in no state change, the AI MUST generate a **Pseudo-event** specifically to record the message ID to prevent infinite reprocessing loops on redelivery.

## 5. Event Schema Evolution
- The AI MUST NOT bloat aggregate `apply()` methods with backward-compatibility logic for old event schemas.
- The AI MUST implement **Upcasting** to transform old event formats into the latest event format at the infrastructure tier (during event load) before they reach the aggregate.

## 6. GDPR and Data Deletion
- Because event stores are immutable, the AI MUST NOT attempt to use SQL `DELETE` or hard-delete mechanisms for event records.
- To handle GDPR right to erasure, the AI MUST implement encryption for events containing Personally Identifiable Information (PII) using a per-user encryption key stored in a standard database. Erasure is achieved by deleting the encryption key.
- The AI MUST use **Pseudonymization** (UUIDs) for aggregate primary keys instead of natural keys like email addresses, keeping the lookup mapping in a mutable, easily deleted database table.

## 7. Integrating Event Sourcing with Sagas
- **Creating an Orchestration Saga**: 
  - In an RDBMS event store, the AI MAY create the saga and the aggregate in the same ACID transaction.
  - In a NoSQL event store, the AI MUST use an event handler reacting to the aggregate's creation event to instantiate the saga. The AI MUST use the event ID or aggregate ID as the Saga ID to prevent duplicate saga instantiations.
- **Saga Participants**: 
  - To atomically send a reply, the participant aggregate MUST emit a `SagaReplyRequestedEvent` (a pseudo-event) alongside its domain events. An external event handler MUST listen for this event and dispatch the actual reply message to the orchestrator.
- **Saga Orchestrators**:
  - The AI MUST model the orchestrator using event sourcing, persisting its state via `SagaOrchestratorCreated` and `SagaOrchestratorUpdated` events.
  - To send commands reliably, the orchestrator MUST emit a `SagaCommandEvent`. A separate handler MUST listen to this event and dispatch the command to the message broker.

# @Workflow
When tasked with creating or refactoring a domain aggregate to use Event Sourcing, the AI MUST execute the following steps strictly in order:

1. **Analyze Domain Commands and Events**: Identify all operations (Commands) the aggregate handles and the resulting state changes (Events). Define strongly typed classes for each Command and Event.
2. **Implement Aggregate Base**: Create the aggregate class extending the framework's base aggregate class (e.g., `ReflectiveMutableCommandProcessingAggregate`).
3. **Implement `process()` Methods**: For every Command, write a `process()` method that verifies invariants and business rules. Return the corresponding instantiated Event(s).
4. **Implement `apply()` Methods**: For every Event, write an `apply()` method that assigns the data from the Event to the aggregate's internal fields.
5. **Implement Snapshotting (Optional but recommended)**: If the aggregate is long-lived, define a state serialization format and implement snapshot loading logic.
6. **Saga Participant Integration**: If the aggregate handles commands from a Saga, implement the emission of `SagaReplyRequested` pseudo-events to handle reply messaging transactionally.
7. **Ensure Idempotency**: Verify that incoming command/message IDs are captured within the generated events or a dedicated tracking table.

# @Examples (Do's and Don'ts)

## Aggregate Business Logic Separation
**[DO]** Separate validation from state mutation using `process` and `apply`:
```java
public class Order extends ReflectiveMutableCommandProcessingAggregate<Order, OrderCommand> {
    private OrderState state;
    private OrderLineItems orderLineItems;

    // Process validates and returns events
    public List<Event> process(ReviseOrder command) {
        OrderRevision revision = command.getOrderRevision();
        if (this.state != OrderState.APPROVED) {
            throw new UnsupportedStateTransitionException(this.state);
        }
        // Business logic validation
        if (revision.getNewTotal().isLessThan(orderMinimum)) {
            throw new OrderMinimumNotMetException();
        }
        return singletonList(new OrderRevisionProposed(revision));
    }

    // Apply mutates state based on the event
    public void apply(OrderRevisionProposed event) {
        this.state = OrderState.REVISION_PENDING;
        // Apply changes from event...
    }
}
```

**[DON'T]** Mutate state within the command processing logic or put business validation inside the apply logic:
```java
public class Order {
    private OrderState state;

    // ANTI-PATTERN: Mutating state directly in command handler, acting like an ORM entity
    public void reviseOrder(OrderRevision revision) {
        if (this.state != OrderState.APPROVED) {
            throw new Exception("Invalid");
        }
        this.state = OrderState.REVISION_PENDING; // Mutating state without an event!
        publishEvent(new OrderRevisionProposed(revision)); // Bolted-on event publishing
    }
}
```

## Saga Participant Reply Handling (NoSQL / Event Store context)
**[DO]** Use a pseudo-event to trigger replies atomically with state changes:
```java
public List<Event> process(AuthorizeCommand command) {
    if (this.creditLimit.isLessThan(command.getAmount())) {
        return Arrays.asList(
            new CreditAuthorizationFailed(command.getAmount()),
            new SagaReplyRequestedEvent(command.getMessageId(), new FailureReply()) // Pseudo-event for reliable reply
        );
    }
    return Arrays.asList(
        new CreditAuthorized(command.getAmount()),
        new SagaReplyRequestedEvent(command.getMessageId(), new SuccessReply())
    );
}
```

**[DON'T]** Attempt to call the message broker or orchestrator directly from the aggregate:
```java
public void process(AuthorizeCommand command) {
    // ANTI-PATTERN: Injecting message brokers into aggregates and breaking transactionality
    if (this.creditLimit.isLessThan(command.getAmount())) {
        messageBroker.sendReply(command.getReplyChannel(), new FailureReply()); 
        throw new Exception("Failed");
    }
}
```

## Handling Immutable Event Deletion (GDPR)
**[DO]** Use pseudonymization and encryption for user data in events:
```java
// Store UUID in event, keep mapping of Email -> UUID in a mutable relational table
// Encrypt sensitive payload with a Key associated with the UUID
public class AccountCreatedEvent implements Event {
    private String userUuid; // Pseudonymized
    private byte[] encryptedPayload; // Encrypted PII
}
```

**[DON'T]** Store raw PII in events and attempt to delete them later:
```java
public class AccountCreatedEvent implements Event {
    // ANTI-PATTERN: Raw PII in an immutable store violates GDPR Right to Erasure
    private String userEmail;
    private String userPlainTextName; 
}
```