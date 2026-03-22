@Domain
These rules MUST be activated when the AI is tasked with designing, implementing, or refactoring inter-service communication, distributed systems architecture, microservice integration, event schemas, message brokers (e.g., Kafka, RabbitMQ), asynchronous workflows, or when reviewing system coupling and resilience in an event-driven context.

@Vocabulary
- **Event-Driven Architecture (EDA)**: An architectural style where a system's components communicate asynchronously by exchanging event messages. Used for integration *between* services.
- **Event Sourcing**: A pattern for capturing state changes *inside* a service as a series of events. Distinct from EDA.
- **Message**: A generic term for a data record transmitted over a messaging platform. Includes both Events and Commands.
- **Event**: A message describing a change that has *already happened*. It cannot be rejected or canceled; undoing it requires a compensating action.
- **Command**: A message describing an operation that has to be carried out. It is an instruction that can be rejected by the receiver.
- **Event Notification**: A succinct event type that notifies subscribers of a change but lacks full details, requiring the consumer to explicitly query the producer for more information.
- **Event-Carried State Transfer (ECST)**: An event type that includes a snapshot of updated state (or modified fields), used as an asynchronous data replication mechanism to allow consumers to maintain a local cache.
- **Domain Event**: An event type containing all data describing a significant business occurrence, primarily intended for internal business modeling rather than external integration.
- **Temporal Coupling**: An anti-pattern where components depend on a strict order of execution across asynchronous boundaries (e.g., relying on artificial delays).
- **Functional Coupling**: An anti-pattern where multiple subscribing components implement the exact same business logic (e.g., same projection logic) to process raw events.
- **Implementation Coupling**: An anti-pattern where consumers are tightly bound to a producer's internal models, breaking if the producer changes its internal schema.
- **Published Language**: An integration-specific, public-facing model used to decouple a service's internal implementation from its consumers.

@Objectives
- Ensure asynchronous communication between bounded contexts minimizes temporal, functional, and implementation coupling.
- Select the precise event type (Notification, ECST, or Domain Event) based on strict evaluations of consistency, security, and payload requirements.
- Protect internal business models by strictly separating private implementation events from public integration events.
- Design for distributed system failure by enforcing resilient communication patterns (Outbox, idempotency, and compensating actions).

@Guidelines

### 1. Message Classification & Naming
- The AI MUST explicitly classify every asynchronous message as either an **Event** or a **Command**.
- **Event Naming**: The AI MUST name all events using the past tense (e.g., `DeliveryScheduled`, `ShipmentCompleted`).
- **Command Naming**: The AI MUST name all commands using the imperative mood (e.g., `ScheduleDelivery`, `CompleteShipment`).
- The AI MUST NOT design systems that attempt to "reject" an event. If an event causes an error state, the AI MUST issue a new Command as a compensating action (via a Saga or Process Manager).

### 2. Event Schema Structure
- The AI MUST include standard metadata in every event schema. Required fields: `type`, `event-id`, `correlation-id`, `timestamp`, and `payload`.
- The `payload` MUST dictate the structural bounds of the specific event type being used.

### 3. Event Type Selection Heuristics
- **Use Event Notification WHEN**: 
  - The payload contains highly sensitive data (Security), forcing the consumer to authenticate via a synchronous API call to retrieve details.
  - The consumer strictly requires the absolute latest state (Concurrency/Pessimistic Locking), rendering asynchronous eventual consistency unacceptable.
  - *Constraint*: The payload MUST ONLY contain entity IDs and/or URI links to fetch the data.
- **Use Event-Carried State Transfer (ECST) WHEN**:
  - The consumer needs a local cache of the producer's data to improve performance (e.g., Backend-For-Frontend) or fault tolerance (Consumer must operate if Producer is down).
  - The system tolerates eventually consistent data.
  - *Constraint*: The payload MUST contain either a full snapshot of the entity or the explicitly updated fields.
- **Use Domain Events WHEN**:
  - Modeling internal state transitions within a single Bounded Context.
  - *Constraint*: The AI MUST NOT use raw Domain Events for external cross-context integration.

### 4. Preventing Distributed Big Balls of Mud (Coupling)
- **Prevent Temporal Coupling**: The AI MUST NOT introduce artificial delays (e.g., `sleep(300)` or delayed queues) to enforce an order of execution between disparate consumers. Instead, the AI MUST use Event Notifications to trigger subsequent steps explicitly.
- **Prevent Functional Coupling**: The AI MUST NOT force multiple consumers to implement the same projection logic. The producer MUST execute the projection internally and publish the computed result as an integration event.
- **Prevent Implementation Coupling**: The AI MUST NOT expose internal Event-Sourced domain events directly to external consumers. The AI MUST use the Open-Host Service pattern to translate internal events into a Public/Published Language before broadcasting.

### 5. Distributed Resilience (Assume the Worst)
- The AI MUST assume networks will fail, servers will crash, and events will arrive out-of-order or duplicated.
- **Outbox Pattern**: The AI MUST specify the Outbox Pattern (committing the state change and the outgoing event in a single atomic database transaction) when publishing events from an operational database.
- **Consumer Idempotency**: The AI MUST design event consumers to explicitly handle deduplication (using `event-id`) and reordering logic.

@Workflow
When tasked with designing or evaluating an asynchronous integration between components, the AI MUST follow these algorithmic steps:

1. **Identify the Boundary**: Determine if the communication is internal (within a Bounded Context) or external (across Bounded Contexts).
   - If internal: Use Event Sourcing and/or Domain Events.
   - If external: Proceed to step 2.
2. **Determine Message Intent**: Decide if the sender is instructing the receiver (Command) or informing the receiver (Event). Name the message accordingly (Imperative vs. Past Tense).
3. **Evaluate Integration Constraints**:
   - Assess Security: Does the data require strict access control? (If yes -> Event Notification).
   - Assess Concurrency: Does the receiver need to read the last absolute write? (If yes -> Event Notification).
   - Assess Availability/Performance: Does the receiver need to operate if the sender goes offline? (If yes -> ECST).
4. **Design the Schema**: Construct the JSON/schema payload matching the chosen Event Type, ensuring `type`, `event-id`, `correlation-id`, and `timestamp` are present.
5. **Enforce Public/Private Boundaries**: Validate that the event being published is a mapped "Published Language" event, not a raw internal Domain Event.
6. **Apply Resilience Tactics**: Implement the Outbox pattern on the producer side and deduplication logic on the consumer side.

@Examples (Do's and Don'ts)

### Message Naming
- **[DO]**: Name events based on historical facts: `PaymentConfirmed`, `UserRegistered`.
- **[DON'T]**: Name events as instructions: `ConfirmPaymentEvent`, `ProcessUserRegistration`.

### Event Notification Implementation
- **[DO]**: Send a lightweight ping that forces the consumer to fetch data.
  ```json
  {
    "type": "paycheck-generated",
    "event-id": "537ec7c2-d1a1",
    "timestamp": 1615726445,
    "payload": {
      "employee-id": "456123",
      "link": "/api/paychecks/456123/latest"
    }
  }
  ```
- **[DON'T]**: Include highly sensitive or rapidly changing data in a notification meant only to trigger a fetch.

### ECST Implementation
- **[DO]**: Send a comprehensive snapshot to allow consumers to build a local cache.
  ```json
  {
    "type": "customer-updated",
    "event-id": "6b7ce6c6-8587",
    "timestamp": 1615728520,
    "payload": {
      "customer-id": "01b18d56",
      "status": "follow-up-set",
      "version": 8
    }
  }
  ```
- **[DON'T]**: Force consumers to synchronously fetch data when they have strict high-availability requirements that mandate a local cache.

### Preventing Implementation Coupling
- **[DO]**: Use an Open-Host Service proxy to translate an internal event (`OrderSubmitted` + `PaymentProcessed`) into a dedicated public Published Language event (`ReadyForFulfillment`) before placing it on the external message bus.
- **[DON'T]**: Give external services direct access to an aggregate's internal Event Store streams, forcing them to reconstruct the aggregate's state themselves.

### Preventing Temporal Coupling
- **[DO]**: Have Service A publish `DataProcessed`, which explicitly triggers Service B to begin its reporting phase.
- **[DON'T]**: Have Service A and Service B listen to the same raw event, but artificially configure Service B with a `Thread.Sleep(300000)` so that Service A has time to finish writing to the database.