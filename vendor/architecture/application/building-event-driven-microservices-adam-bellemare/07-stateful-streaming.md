@Domain
These rules are triggered whenever the AI is tasked with designing, implementing, configuring, reviewing, or refactoring stateful event-driven microservices. This includes tasks involving state materialization, state store selection (internal vs. external), state recovery mechanisms, changelog management, schema evolution for state stores, and the implementation of effectively-once processing logic.

@Vocabulary
- **Materialized State**: An immutable projection of events sourced from an event stream.
- **State Store**: The mutable storage mechanism where a microservice maintains its business state and intermediate computations.
- **Internal State Store**: A state store that coexists within the same container or virtual machine as the microservice's business logic, strictly mapped to the assigned event stream partitions (e.g., RocksDB).
- **External State Store**: A state store hosted outside the microservice's container, typically accessed over a network (e.g., standalone relational or document databases).
- **Global State Store**: A specialized internal state store that materializes data from all partitions of an event stream across every microservice instance, rather than only assigned partitions.
- **Changelog Event Stream**: An event stream representing the table-stream duality that records every state change (insert, update, delete). Used to durably back up and restore state stores.
- **Compaction**: The process performed by the event broker to reduce changelog size by retaining only the most recent event for any given key.
- **Tombstone**: A keyed event with a null value, used to indicate the deletion of a record from a materialized state store.
- **Hot Replica**: A standby copy of a materialized state partition maintained on a different instance to provide zero-downtime failover.
- **Effectively Once Processing**: The guarantee that an event's processing updates the single source of truth consistently, regardless of producer, consumer, or broker failures.
- **Dedupe ID**: A unique, high-cardinality identifier generated for an event to facilitate deduplication when broker transactions are unavailable.
- **Operator State**: The mapping of partition IDs to consumer offsets.
- **Key State**: The actual business data stored as key/value pairs in the state store.

@Objectives
- Abstract event streams into highly performant, resilient, and accurate state stores.
- Guarantee the decoupling of state between independent microservices.
- Ensure state consistency and rapid recovery using changelogs, snapshots, and hot replicas.
- Implement effectively-once processing seamlessly through atomic transactions or robust deduplication patterns.
- Navigate the tradeoffs between internal and external state stores based on data locality, latency, and business requirements.

@Guidelines

**1. State Store Selection and Isolation**
- The AI MUST evaluate performance, latency, and operational requirements when choosing between Internal and External state stores.
- When configuring an Internal State Store, the AI MUST strictly isolate data by partition ID. If a partition is revoked during a consumer group rebalance, the AI MUST ensure the associated local state is safely dropped or ignored to prevent resource leaks and duplicate sources of truth.
- When using an External State Store, the AI MUST explicitly prohibit direct state sharing between microservices. Every microservice MUST materialize its own independent copy of state from the event broker.
- The AI MUST restrict the use of Global State Stores to common data set lookups and dimension tables. Global state MUST NEVER drive event-producing business logic, as this will generate duplicate outputs across instances.

**2. Changelogs and State Recovery**
- The AI MUST back all Internal State Stores with a Changelog Event Stream stored in the event broker.
- The AI MUST configure Changelog Event Streams with compaction enabled to minimize disk footprint and recovery time.
- To handle deletions, the AI MUST implement logic that publishes Tombstone records (a keyed event with a null value) to the changelog.
- When an instance recovers or scales up, the AI MUST prioritize rebuilding the state from the Changelog Event Stream before resuming consumption of new events.
- If zero-downtime failover is a strict requirement, the AI MUST configure Hot Replicas to maintain standby state across instances.

**3. External State Store Integrity**
- If an External State Store is used, the AI MUST account for network latency and ensure the microservice SLA can accommodate the overhead.
- When recovering an External State Store, the AI MUST employ snapshot restoration or completely rebuild from the source streams.
- If using snapshots for an External State Store that requires strict consistency (not naturally idempotent), the AI MUST store the consumer group's Operator State (offsets) alongside the Key State in the snapshot.

**4. Effectively-Once Processing**
- If the target event broker supports client-broker transactions (e.g., Apache Kafka), the AI MUST wrap the offset update, the changelog update, and the output event generation within a single atomic transaction.
- If client-broker transactions are NOT supported, the AI MUST implement a deduplication strategy:
  - Generate a unique Dedupe ID for each event based on high-cardinality fields (e.g., composite of key, timestamps, and specific payload data).
  - Persist processed Dedupe IDs in a local state store.
  - Implement a Time-To-Live (TTL) or maximum cache size for the deduplication store to prevent infinite disk growth.
- Alternatively, for External State Stores without broker transactions, the AI MUST atomically commit the consumer offsets and the state update in a single database transaction to guarantee consistency.

**5. State Evolution: Rebuilding vs. Migrating**
- The AI MUST choose the "Rebuilding" strategy (reset offsets, clear state, re-consume from beginning) when deploying complex topology changes, new aggregations, or business logic alterations that require historical accuracy.
- The AI MUST choose the "Migrating" strategy (e.g., executing a database migration script without reprocessing streams) ONLY for simple, forward-compatible changes (like adding an optional/nullable field) where historical reprocessing is deemed unnecessary by the business.

@Workflow

1. **Evaluate Requirements & Select State Store Type**: Determine if the microservice requires sub-millisecond local processing (Internal State) or access to specialized querying/full data locality (External State). Determine if dimension tables require a Global State Store.
2. **Define State Materialization Logic**: Map incoming event streams to the state store. Implement upsert logic for standard events and deletion logic handling Tombstone records.
3. **Configure Durability and Recovery**: 
   - If Internal: Configure the Changelog Event Stream, enable compaction, and design the initialization phase to block event consumption until the state is fully restored from the changelog. Evaluate the need for Hot Replicas.
   - If External: Configure transactional bounds linking the event offset to the data update, and establish a snapshotting protocol.
4. **Implement Effectively-Once Processing**: 
   - If broker transactions are supported, initiate a transaction block, apply state changes, produce output events, commit offsets, and commit the transaction.
   - If not supported, implement the Dedupe ID generation, verify against the TTL-limited deduplication cache, and apply idempotent processing rules.
5. **Determine Evolution Strategy**: When updating an existing stateful service, analyze the schema and logic changes to explicitly choose between a full state Rebuild (re-consuming the immutable log) or a state Migration (in-place schema update).

@Examples (Do's and Don'ts)

- [DO] Use an Internal State Store (like RocksDB) backed by a compacted Changelog Event Stream for high-performance, partition-isolated aggregations.
- [DON'T] Point two independent microservices to the exact same external PostgreSQL database table to share state. This violates bounded context principles.

- [DO] Use a Global State Store to load a static currency conversion table into every instance's memory for fast, local lookups.
- [DON'T] Use a Global State Store to evaluate order fraud and emit a "FraudDetected" event. Because every instance holds the full state, every instance will emit the same event, causing massive duplication.

- [DO] Wrap the update to the changelog topic, the publication of the downstream business event, and the consumer offset advancement inside a single `producer.beginTransaction()` and `producer.commitTransaction()` block.
- [DON'T] Commit the consumer offset immediately upon reading an event, before the state store has successfully persisted the materialized update.

- [DO] Implement a Dedupe ID using a hash of `transaction_id`, `timestamp`, and `amount` when processing financial events on a broker without transaction support, keeping these hashes in a local cache with a 24-hour TTL.
- [DON'T] Attempt to implement deduplication without a TTL or cache size limit, which will eventually exhaust the microservice's disk/memory resources.

- [DO] Publish a Tombstone record (a message with the customer's ID as the key and `null` as the payload) to the changelog stream when a customer deletes their account, ensuring the state store drops the record.
- [DON'T] Rely on a boolean `is_deleted` flag for deleted entities if the changelog relies strictly on compaction, as the record will physically remain on disk indefinitely.