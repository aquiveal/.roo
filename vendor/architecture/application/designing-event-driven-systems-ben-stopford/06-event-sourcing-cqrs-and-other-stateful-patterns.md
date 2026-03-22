@Domain
These rules MUST be activated when the AI is tasked with designing, reviewing, or implementing event-driven architectures, Kafka-based stream processing, stateful services, distributed data synchronization, data persistence strategies, or migrating legacy CRUD databases to modern event-centric models.

@Vocabulary
*   **Event Sourcing**: The architectural pattern of storing every state change as an immutable event appended to a sequence (log), serving as the comprehensive audit and exact narrative of system execution.
*   **Command Sourcing**: A variant of Event Sourcing where the raw, unvalidated input commands/requests are recorded as events before any business logic is applied, allowing for complete rewind-and-replay of inputs.
*   **CQRS (Command Query Responsibility Segregation)**: A pattern that strictly separates the write path (command model) from the read path (query model) using an asynchronous channel, allowing each side to be optimized independently.
*   **Event-Sourced View**: A queryable endpoint (database, memory image, or state store) built inside one service using data authored by another, derived directly from an event log, which can be regenerated at any time.
*   **Materialized View**: A precomputed query result continuously updated by an underlying event stream to optimize read performance.
*   **Polyglot Views**: Multiple, distinct event-sourced views powered by different database technologies (e.g., Elasticsearch for search, Redis for key/value) but driven by the exact same central event log.
*   **Whole Fact**: A complete record of an entity's state at a point in time, stored immutably exactly as it was received, as opposed to a calculated delta.
*   **State Store**: A local, disk-resident hash table built into the Kafka Streams API that acts as an embedded database, backed up by a Kafka changelog topic.
*   **CDC (Change Data Capture)**: A technique/connector that captures database modification operations directly from a database's write-ahead log and translates them into an event stream.
*   **MemoryImage**: A pattern for caching an entire dataset into memory directly from a compacted topic for high-performance, disk-free querying.

@Objectives
*   Eliminate update-in-place data corruption by treating the event log as an immutable version control system for data.
*   Guarantee that the state a service communicates and the state it saves internally are exactly the same by making the event log the absolute single source of truth.
*   Maximize read and write performance by decoupling them via CQRS and provisioning use-case-specific polyglot views.
*   Ensure systems are fundamentally recoverable by designing read models to be safely droppable and deterministically reconstructable from the event log.
*   Prevent the dual-write / atomic failure problem inherent in legacy microservice notification patterns.

@Guidelines
*   **Log as the Source of Truth**: The AI MUST design systems so that the immutable event log is the primary source of truth. Databases and internal caches MUST be treated strictly as derived, disposable views.
*   **Apply Command Sourcing for Recovery**: The AI MUST ensure raw input events are logged *before* processing. If a bug is introduced, the system must be recoverable by fixing the bug, rewinding the log, and replaying the original commands.
*   **Embrace CQRS**: The AI MUST physically segregate write operations from read operations. Ensure writes append quickly to the log and reads query a separate, asynchronously updated view. The AI MUST acknowledge and architect for the resulting eventual consistency (read models lagging behind writes).
*   **Record Whole Facts over Deltas**: When receiving an event, the AI MUST journal the whole fact exactly as it arrived. The AI MUST NOT perform external database lookups to combine partial events/deltas into a single aggregate before writing to the log. Merging and combining must be deferred to the read/query side.
*   **Avoid Atomic Dual-Writes**: The AI MUST NEVER design a flow that writes to a CRUD database and subsequently emits an event to a broker in a sequential, non-transactional manner. Instead, write to the log first and derive the database state, or use CDC to guarantee event emission from a database write.
*   **Implement Polyglot Persistence**: The AI MUST utilize multiple read models for different access patterns. Do not force a single database to handle full-text search, relational queries, and fast key/value lookups if an event stream can seamlessly feed specialized databases.
*   **Utilize Kafka Streams State Stores for In-Process Views**: For lightweight microservices, the AI MUST leverage Kafka Streams `KTable` and state stores to materialize views natively within the application process, eliminating external database network calls.
*   **Use CDC for Legacy Integration**: When unlocking legacy systems, the AI MUST recommend Change Data Capture (CDC) to extract an event stream directly from the legacy database's write-ahead log instead of using application-level dual-writes or periodic polling queries.
*   **Apply the MemoryImage Pattern Appropriately**: If a dataset fits cleanly in memory and requires ultra-fast access, the AI MUST load the entire compacted topic into memory on startup rather than maintaining an external database.

@Workflow
1.  **Ingest & Record (Command Sourcing)**: Receive the incoming request/action and immediately append it to an immutable command topic.
2.  **Process & Validate**: Execute business logic against the incoming command.
3.  **Journal State Change (Event Sourcing)**: Append the resulting successful state change as a new, immutable "Whole Fact" event to a separate entity topic.
4.  **Derive Read Models (CQRS)**: Determine the required query access patterns for the data. Select the optimal storage mechanism for the event-sourced view (e.g., Kafka Streams State Store, Elasticsearch via Kafka Connect, or MemoryImage).
5.  **Consume & Materialize**: Route the entity event stream asynchronously into the selected read models to continuously update the materialized views.
6.  **Provide Recovery Mechanism**: Document and implement the procedure to drop the read model, reset consumer offsets to zero, and cleanly re-derive the entire state from the event log in case of schema changes or data corruption.

@Examples (Do's and Don'ts)

**Example 1: Establishing the Source of Truth**
*   [DO]: Write the `OrderValidated` event to Kafka immediately. Have an asynchronous process (or Kafka Streams topology) read that event from Kafka and update the local querying database.
*   [DON'T]: Update the local database's `orders` table and then fire an `OrderValidated` HTTP/Kafka notification. (This causes divergent data if the notification fails after the database commits).

**Example 2: Storing Facts vs. Deltas**
*   [DO]: Upon receiving a request to cancel a specific line item, log the exact `LineItemCancelled` event immutably. Reconstruct the total order state later in the CQRS read model.
*   [DON'T]: Receive a `LineItemCancelled` event, perform a synchronous database lookup to fetch the parent order, mathematically apply the cancellation to the order, and save a brand new aggregated `OrderUpdated` event to the log.

**Example 3: Integrating Legacy Databases**
*   [DO]: Deploy a Kafka Connect CDC connector (e.g., Debezium) attached to the legacy Postgres database. Convert committed row changes automatically into a reliable event stream.
*   [DON'T]: Add a cron job or scheduled thread inside the application to run `SELECT * FROM legacy_table WHERE updated_at > last_run` to manually synthesize events.

**Example 4: Building Local Materialized Views**
*   [DO]: Use `builder.table("customer-topic")` in Kafka Streams to create an in-process, disk-resident state store (`KTable`) of customers that can be queried instantly by the local application without network latency.
*   [DON'T]: Perform a synchronous REST call to a central "Customer Service" database for every single incoming event that needs to validate a customer ID.