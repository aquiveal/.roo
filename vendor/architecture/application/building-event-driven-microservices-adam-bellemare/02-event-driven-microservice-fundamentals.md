# @Domain
Triggers when the user requests the design, architecture, implementation, review, or debugging of Event-Driven Microservices (EDMs), event streams, event schemas, stream-processing topologies, state materialization, or the integration of containerized event-driven applications with event brokers.

# @Vocabulary
*   **Event-Driven Microservice (EDM)**: A small, completely asynchronous application built to fulfill a specific bounded context by consuming and/or producing events.
*   **Microservice Topology**: The internal data-driven operations performed on incoming events within a single microservice, including transformation, storage, and emission.
*   **Business Topology**: The arbitrary graph-like grouping of multiple microservices, event streams, and APIs that fulfill complex superset business functions.
*   **Event**: A statement of fact formatted as a key/value pair recording what happened within the business scope. Acts as both data storage and the asynchronous communication mechanism.
*   **Unkeyed Event**: An event describing a singular statement of fact with no key involved (e.g., a simple user interaction log).
*   **Entity Event**: An event keyed on a unique ID describing the properties and state of a specific business object at a given point in time.
*   **Keyed Event**: An event containing a key for partitioning and data locality guarantees, but which does not represent a stateful entity.
*   **Table-Stream Duality**: The fundamental concept that a stateful table can be materialized by applying a stream of events in order, and conversely, a table's changes can be emitted as a stream of events.
*   **Upserting**: Inserting a new row if it does not exist in a materialized table, or updating it if it does.
*   **Tombstone**: A keyed event with its value set to `null`, used as a convention to instruct consumers to delete the state associated with that key.
*   **Compaction**: A process performed by the event broker to reduce log size by retaining only the most recent event (or tombstone) for a given key.
*   **Microservice Single Writer Principle**: The rule that each event stream must have one, and only one, producing microservice.
*   **Event Broker**: A clustered system that provides partitioned, strictly ordered, immutable, replayable, and infinitely retainable append-only event logs.
*   **Message Broker**: A system providing publish/subscribe queues that deletes messages after consumption (insufficient for EDM single-source-of-truth architectures).
*   **Consumer Group**: A logical grouping of consumers that tracks reading progress (offsets) independently of other groups and distributes partition assignments horizontally across its instances.
*   **Offset**: The measurement/index of the current event from the beginning of the event stream.
*   **Microservice Tax**: The inescapable systemic costs (financial, manpower, tooling) required to manage, deploy, and operate the underlying microservice infrastructure (event brokers, CMS, pipelines, logging).

# @Objectives
*   Architect microservices that communicate strictly asynchronously via immutable event streams.
*   Establish the event broker as the absolute single source of truth for all business state and communication.
*   Differentiate cleanly between the internal logic of a microservice (Microservice Topology) and the macroscopic system graph (Business Topology).
*   Guarantee deterministic state materialization leveraging the table-stream duality, entity events, and tombstones.
*   Ensure absolute enforcement of the Microservice Single Writer Principle to maintain uncorrupted data lineage.
*   Design highly scalable, independent deployable units (containers) that delegate data scaling to the event broker and compute scaling to the Container Management System (CMS).

# @Guidelines
*   **Event Structure & Design**:
    *   All events MUST be represented in a key/value format.
    *   You MUST explicitly classify every designed event as an Unkeyed Event, an Entity Event, or a Keyed Event.
    *   Do NOT design events as transient signals or semaphores; an event MUST contain the complete details required to accurately describe what happened (the single source of truth).
*   **State Materialization**:
    *   To build stateful microservices, you MUST materialize state by applying Entity Events in strict offset order.
    *   You MUST process Tombstone events (value `null`) by deleting the corresponding record from the local materialized state.
    *   Assume all entity streams are subject to Log Compaction; design the microservice to accurately reconstruct its state using only the latest values per key.
*   **Data Contracts & Schemas**:
    *   Producers and consumers MUST share a common language.
    *   Always define explicit schemas (e.g., Apache Avro, Protobuf) that support schema evolution and code generation into typed classes.
    *   Never use arbitrary, schemaless key/value maps for core business events.
*   **Microservice Single Writer Principle**:
    *   You MUST assign exactly ONE producing microservice per event stream.
    *   If multiple sources generate similar data, route them to a single microservice responsible for writing to the canonical output stream, or separate the data into distinct, individually-owned streams.
*   **Event Brokers vs. Message Brokers**:
    *   For EDM, you MUST utilize Event Brokers (e.g., Apache Kafka) providing immutable, replayable logs rather than traditional Message Brokers (e.g., RabbitMQ).
    *   Do NOT design architectures that delete events upon consumption if that data represents business state required by multiple independent consumers.
*   **Consumption Models**:
    *   **Event Stream Consumption**: Use this model (tracked via offsets per partition) when strict ordering and multiple independent consumers are required.
    *   **Queue Consumption**: Use this model ONLY when event processing order does not matter and horizontal scaling across an arbitrary number of workers is needed. Warn the user that strict ordering is lost.
*   **Scale and Deployment**:
    *   Deploy every microservice as a single isolated unit using containers (or VMs).
    *   If a microservice requires multiple containers (e.g., an app container + an external data store proxy), package them logically as a single deployable unit (e.g., a Kubernetes Pod).
    *   Do NOT architect custom horizontal scaling logic within the microservice codebase; delegate this to consumer groups and CMS scaling policies.

# @Workflow
1.  **Context & Role Definition**: Identify the specific bounded context the microservice fulfills. Determine if it is a producer, a consumer, or both.
2.  **Event Schema Definition**: Define the inputs and outputs. Specify if events are Unkeyed, Keyed, or Entity events. Draft explicit schemas (Avro/Protobuf) for the data contracts.
3.  **Business Topology Mapping**: Map out the external event streams this microservice reads from and writes to. Validate that the service acts as the *sole* writer to its output streams.
4.  **Microservice Topology Design**: Design the internal processing logic. Map out the ingestion of events, transformations, materialization of local state (including tombstone deletion logic), and output emission.
5.  **State Management Strategy**: If the microservice is stateful, explicitly define the table-stream duality mechanism. Specify how the microservice will rebuild its state from the event broker upon failure or restart.
6.  **Infrastructure & Consumption Configuration**: Select the consumption pattern (Stream vs. Queue). Define the consumer group strategy, partition key assignments, and offset tracking.
7.  **Deployment & CMS Integration**: Draft the containerization strategy (Docker/Kubernetes). Verify that the design accounts for the "Microservice Tax" by ensuring logging, monitoring, and stateless scalability are handled by the environment.

# @Examples (Do's and Don'ts)

**Principle: Microservice Single Writer Principle**
*   [DO]: Create `Microservice A` to solely own and write to `Stream_User_Updates`.
*   [DON'T]: Allow `Microservice A` and `Microservice B` to both publish events directly to `Stream_User_Updates`.

**Principle: State Materialization & Table-Stream Duality**
*   [DO]: Upsert incoming `User` entity events into a local data store by key. When a `User` event arrives with the value `null` (tombstone), immediately delete that key from the local data store.
*   [DON'T]: Emit custom "Delete_User" action events and expect downstream consumers to run complex custom logic to handle data removal without leveraging native broker compaction and tombstones.

**Principle: Event Content and Truth**
*   [DO]: Publish an event: `Key: Order123 | Value: { status: "SHIPPED", items: [...], timestamp: 1620000000 }`.
*   [DON'T]: Publish a transient signal: `Key: null | Value: { message: "Order data is ready, query DB for details" }`.

**Principle: Consumption Strategy**
*   [DO]: Read from an immutable event stream using a Consumer Group that tracks offsets, ensuring that if a new Microservice `C` is spun up, it can replay the log from offset 0 to build its own state.
*   [DON'T]: Use an ephemeral message queue that acknowledges and destroys the event upon first read, preventing any new microservices from accessing historical state.