## @Domain
Triggered when the AI is tasked with designing, implementing, or evaluating asynchronous communication architectures, event-driven systems, stream processing applications, message brokers (e.g., Kafka, RabbitMQ), Event Sourcing, or Command Query Responsibility Segregation (CQRS) pipelines.

## @Vocabulary
- **Stream Processing**: The act of handling events and data changes as soon as they occur, enabling responses (like fraud detection or analytics) on the order of seconds.
- **Event Sourcing**: A data modeling pattern where every state change is captured as an immutable event appended to a sequence (an event log). The log acts as the absolute source of truth.
- **CQRS (Command Query Responsibility Segregation)**: The principle of maintaining separate representations optimized for reading (materialized views) derived from a write-optimized representation (the event log).
- **Command**: A user request to change state that must be validated before it is executed and stored.
- **Fact / Event**: A validated command that has been successfully executed and recorded in the event log. 
- **Materialized View (Projection/Read Model)**: A read-optimized, precomputed cache of data derived from the event log that can be queried by the application.
- **Message Broker (Event Broker / Message Queue)**: An intermediary that temporarily stores messages, buffering them if the recipient is overloaded, enabling asynchronous communication and automated redelivery.
- **Queue**: A message distribution pattern where a message is delivered to exactly one consumer.
- **Topic**: A message distribution pattern where a message is broadcast and delivered to all subscribers.
- **Actor Model**: A programming model for distributed systems where logic is encapsulated in isolated entities (actors) that communicate purely via asynchronous messages.

## @Objectives
- Guarantee that derived data systems (materialized views) are built deterministically and reproducibly from an immutable event log.
- Decouple senders and receivers using message brokers to improve system reliability and tolerate temporary node or network unavailability.
- Prevent data loss during asynchronous message routing by preserving unknown fields across schema evolution.
- Enforce strict separation between command validation and event consumption.

## @Guidelines
- **Event Immutability & Naming**:
  - The AI MUST ensure that events appended to an event log are strictly immutable. They MUST NOT be updated or deleted in place.
  - The AI MUST name all events in the past tense (e.g., `SeatBooked`, `OrderCancelled`) to clearly indicate they represent facts that have already occurred.
- **Command Validation vs. Event Processing**:
  - The AI MUST place all business logic and validation rules in the command handling phase (before an event is written to the log).
  - The AI MUST ensure that consumers of the event log (e.g., stream processors building materialized views) blindly accept and process every event. A consumer MUST NOT reject an event.
- **Determinism in Materialized Views**:
  - The AI MUST ensure that materialized views are entirely reproducible by replaying the event log in the exact same order.
  - When an event's processing depends on external, fast-changing state (e.g., currency exchange rates), the AI MUST either embed that state directly into the event payload at write-time, or use a historically versioned query to guarantee determinism upon replay.
- **Message Broker Configuration**:
  - When the AI implements a feature requiring only one processor to handle a task, it MUST configure the message broker using a *Queue*.
  - When the AI implements a feature requiring multiple independent systems to react to the same event, it MUST configure the broker using a *Topic*.
- **Schema Evolution in Messaging**:
  - The AI MUST use a standard, schema-driven binary encoding format (such as Protocol Buffers or Avro) for messages, avoiding language-specific encodings (like Java `Serializable` or Python `pickle`).
  - The AI MUST assume that senders and receivers may be running different versions of the code. 
  - If a consumer reads a message from one topic and republishes it to another, the AI MUST explicitly preserve any unknown fields to prevent data loss for newer downstream consumers.
- **Handling Deletions**:
  - If personal data deletion (e.g., GDPR compliance) is required, the AI MUST NOT mutate the immutable log. Instead, the AI MUST segregate personal data from the main event log, or use cryptographic erasure (encrypting the payload and deleting the key).

## @Workflow
1. **Analyze Communication Requirements**: Determine if the task requires real-time synchronous RPC or if it can be handled asynchronously. If asynchronous, select a message broker.
2. **Define the Event Schema**: Design the payload using Avro or Protocol Buffers. Name the event in the past tense. Ensure any transient external data required for future processing is embedded directly into the schema.
3. **Implement Command Handlers**: Write the application logic that receives user requests, validates them against current business rules, and appends the resulting immutable fact to the event log.
4. **Configure Message Routing**: Set up the message broker. Use Queues for point-to-point worker distribution and Topics for pub/sub broadcasting.
5. **Implement Stream Processors**: Write consumer processes that read from the event log in strict order to build or update materialized views. Ensure these consumers contain no rejection logic.
6. **Implement Replay Mechanisms**: Provide a mechanism to drop the current materialized view and rebuild it completely from the beginning of the event log to support future schema or query changes.

## @Examples (Do's and Don'ts)

- **Event Naming**
  - [DO]: Name an event `UserRegistered` or `PaymentProcessed`.
  - [DON'T]: Name an event `RegisterUser` or `ProcessPayment` (these are commands, not historical facts).

- **Handling External State**
  - [DO]: `{"event": "ItemPurchased", "price": 10.00, "currency": "USD", "usd_to_eur_rate_at_purchase": 0.95}`
  - [DON'T]: `{"event": "ItemPurchased", "price": 10.00, "currency": "USD"}` (and subsequently making a live API call to an exchange rate service during the stream processing phase, destroying determinism).

- **Event Consumption Logic**
  - [DO]: Write a materialized view updater that reads `BookingCancelled` and immediately sets `active = false` in the read model.
  - [DON'T]: Write a materialized view updater that reads `BookingCancelled`, checks if the booking is older than 30 days, and throws an error rejecting the event (this validation must happen before the event is logged).

- **Schema Evolution and Republishing**
  - [DO]: Deserialize incoming events using a parser that retains unrecognized fields in a catch-all structure, and re-serialize them when forwarding to the next Topic.
  - [DON'T]: Deserialize incoming events into a rigid, outdated object model that silently drops new fields added by upstream services before republishing.

- **Data Encoding for Streams**
  - [DO]: Use Avro or Protocol Buffers in conjunction with a Schema Registry for all events published to the message broker.
  - [DON'T]: Serialize events using `java.io.Serializable` or `pickle.dumps()`.