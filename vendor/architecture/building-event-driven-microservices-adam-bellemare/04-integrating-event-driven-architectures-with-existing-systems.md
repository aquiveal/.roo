# @Domain
These rules MUST be triggered when the AI is tasked with integrating legacy systems, monolithic applications, or existing relational databases into an event-driven architecture. This includes requests involving data extraction, data liberation, Change-Data Capture (CDC), Outbox table implementation, event sourcing from existing data stores, or sinking event data into external/legacy databases.

# @Vocabulary
- **Data Liberation**: The process of identifying and publishing cross-domain data sets from existing/legacy data stores to corresponding event streams to act as a single source of truth.
- **Unidirectional Event-Driven Architecture**: A compromise pattern for legacy systems where the legacy system publishes internal state changes to an event stream but does not rebuild its own state from that stream.
- **Query-Based Liberation**: Extracting data by actively querying the underlying state store using bulk loads, incremental timestamps, or autoincrementing IDs.
- **Log-Based Liberation (CDC Logs)**: Extracting data by trailing the append-only change-data capture logs of a database (e.g., MySQL binary logs, PostgreSQL write-ahead logs).
- **Outbox Table Pattern**: Pushing data changes to a dedicated database table (the "outbox") within the same transaction as the internal state change, to be subsequently read and published to an event stream by a separate process.
- **Eventification**: The process of denormalizing highly relational internal data models into easy-to-consume, public-facing single event updates prior to or during event publication.
- **Bootstrapping**: The process of taking a snapshot (bulk query) of existing data before starting log-based change-data capture to ensure no historical data is missed.
- **Hard Deletion**: Removing a record completely from a database, which cannot be natively tracked by query-based liberation patterns.
- **Soft Deletion**: Flagging a record as deleted (e.g., `is_deleted = true`) to allow query-based patterns to capture the deletion event.
- **Sinking**: The process of consuming event data from a stream and inserting it into a destination data store (often to integrate non-event-driven applications).

# @Objectives
- **Establish the Single Source of Truth**: The AI MUST extract cross-domain data from legacy systems into event streams, making the broker the canonical source of truth and eliminating point-to-point database queries.
- **Enforce Decoupling**: The AI MUST isolate internal legacy data models from downstream consumers. Consumers MUST couple only to the public data contracts (schemas) of the event streams.
- **Ensure Eventual Consistency**: The AI MUST guarantee that the liberated event stream accurately reflects the source data set through reliable, ordered, and schema-validated capture mechanisms.
- **Promote Event-First Ownership**: The AI MUST encourage architectures where teams manage their own data liberation (e.g., via the Outbox pattern) rather than becoming overly reliant on centralized CDC connector frameworks.

# @Guidelines

## General Data Liberation Rules
- **Schema Enforcement**: The AI MUST apply explicit schemas (e.g., Avro, Protobuf) and schema evolution rules to liberated data. Implicit or plain-text schemas MUST be rejected.
- **Timestamp Accuracy**: The AI MUST assign the event timestamp based on the source record's occurrence time (e.g., the `updated_at` field or trigger execution time), NOT the wall-clock time of the event broker publication.
- **Data Isolation**: The AI MUST NOT expose raw, highly normalized internal data models directly to public event streams. Data MUST be denormalized ("eventified") into public data contracts.

## Query-Based Liberation Rules
- **Incremental Keys**: When implementing query-based updates, the AI MUST utilize either an `updated_at` timestamp column or an autoincrementing ID to track incremental progress.
- **Bulk Load Initialization**: The AI MUST implement a single bulk load of the existing data set before enabling incremental query updates.
- **View-Based Isolation**: The AI MUST utilize SQL Views or materialized views to shield internal domain models and only expose the necessary public data contract to the querying framework.
- **Deletion Handling**: The AI MUST explicitly account for deletions. Since query-based patterns cannot track hard deletions, the AI MUST require soft deletions (e.g., `is_deleted` boolean) if tracking deletions is a business requirement.
- **Race Condition Prevention**: The AI MUST define polling intervals that are longer than the query execution time to prevent older data queries from overwriting newer data queries.

## Log-Based Liberation Rules (CDC)
- **Bootstrapping Requirement**: The AI MUST enforce a bootstrapping phase (snapshot) before initiating tailing of binary/write-ahead logs, ensuring an overlap between the snapshot and the log to prevent data loss.
- **Checkpointing**: The AI MUST ensure the log-capture mechanism checkpoints its progress to provide at-least-once delivery in case of failure.
- **External Denormalization**: Because logs expose raw table data, the AI MUST implement a downstream event processor dedicated to eventification (denormalizing foreign keys) before pushing the data to the organization's public namespace.

## Outbox Table Pattern Rules
- **Transactional Atomicity**: The AI MUST wrap the updates to the internal application tables AND the insertion into the outbox table within a single, atomic database transaction.
- **Ordering Identifiers**: The AI MUST assign an autoincrementing ID and a `created_at` timestamp to outbox records to guarantee strict ordering upon publication.
- **Pre-Publication Denormalization**: The AI MUST design the outbox table to reflect the intended public data contract (denormalized), rather than a 1:1 mapping of the internal relational table.
- **Serialize Before Write**: The AI MUST validate and serialize the event data against the required schema *before* committing the transaction to the outbox table. If serialization fails, the entire database transaction MUST roll back. The AI MUST NOT implement "serialize after write" (where raw data is written to the outbox and serialized by the publisher), as this leads to unpublishable data blocking the outbox queue.

## Trigger-Based Capture Rules
- **Last Resort Usage**: The AI MUST avoid database triggers for CDC unless the legacy system cannot support log-based or outbox-based patterns.
- **Schema Synchronization**: If triggers are used to populate an audit/change-data table, the AI MUST ensure the change-data table schema is kept strictly in sync with the output event schema, using after-the-fact validation prior to event publication.

## Data Definition Language (DDL) Changes
- **Outbox/Trigger Patterns**: The AI MUST handle DDL changes by updating the intermediate change-data tables to ensure compatibility with the downstream event schema BEFORE applying changes to production.
- **Query/Log Patterns**: The AI MUST configure the framework to infer schemas dynamically and block publication if the inferred schema violates the downstream event stream's compatibility rules.

## Sinking Event Data
- **Independent Operation**: When sinking data from an event stream to a legacy data store, the AI MUST configure the sink process to operate completely externally to the destination system, independently tracking its own consumer offsets.

# @Workflow
When tasked with integrating an existing/legacy system into an event-driven architecture, the AI MUST follow this rigid step-by-step algorithm:

1.  **Assess System Modifiability**:
    *   Can the application codebase be modified? If YES, strongly recommend the **Outbox Table Pattern**.
    *   If NO, can the database logs (binlog/WAL) be securely accessed? If YES, recommend **Log-Based Liberation (CDC)**.
    *   If NO to both, recommend **Query-Based Liberation**.
    *   Only if all above fail, recommend **Trigger-Based Capture**.
2.  **Define the Public Data Contract**:
    *   Determine the schema (Avro/Protobuf) for the target event stream.
    *   Identify the gap between the legacy system's normalized internal database tables and the flattened, public data contract.
3.  **Implement Data Isolation (Eventification)**:
    *   *If Outbox*: Write code to map internal domain objects to the serialized public event schema *within* the application transaction before inserting to the outbox.
    *   *If Query*: Generate SQL `CREATE VIEW` statements to join and format the data to match the public schema.
    *   *If Log-Based*: Design an intermediary stream processor to consume raw CDC events, join them with necessary reference data, and output the public events.
4.  **Configure Historical Data Capture**:
    *   Define the script or process to perform a Bulk Load (Query pattern) or Bootstrap Snapshot (Log pattern) to initially populate the event stream.
5.  **Establish Timestamping and Ordering Strategy**:
    *   Identify the field that will dictate event time (`updated_at`, transaction commit time, or outbox `created_at`).
6.  **Handle Deletions**:
    *   If using Query-based, explicitly prompt the user to implement soft-deletes in the legacy schema if deletions must be propagated.
7.  **Review DDL Change Process**:
    *   Output warnings detailing how future database column changes will impact the newly defined event schemas.

# @Examples (Do's and Don'ts)

## Outbox Table Pattern

[DO] Wrap state changes and outbox inserts in a single transaction, and serialize *before* insertion.
```java
@Transactional
public void updateUserProfile(User user) {
    // 1. Update internal state
    userRepository.save(user);
    
    // 2. Map to public data contract (Eventification)
    UserUpdatedEvent event = new UserUpdatedEvent(user.getId(), user.getFullName(), user.getPublicLocation());
    
    // 3. Serialize BEFORE write to ensure schema compatibility
    byte[] serializedEvent = schemaSerializer.serialize(event);
    
    // 4. Save to outbox
    OutboxRecord outbox = new OutboxRecord();
    outbox.setAggregateId(user.getId());
    outbox.setPayload(serializedEvent); // Guaranteed to match schema
    outbox.setCreatedAt(Instant.now()); // Accurate event time
    outboxRepository.save(outbox);
}
```

[DON'T] Write raw JSON to an outbox table without serialization validation, risking unpublishable data getting stuck in the queue.
```java
@Transactional
public void updateUserProfile(User user) {
    userRepository.save(user);
    
    // ANTI-PATTERN: Writing raw JSON. The publishing thread might crash 
    // later if this JSON violates strict Avro/Protobuf schema rules.
    String rawJson = "{\"id\":\"" + user.getId() + "\"}"; 
    
    OutboxRecord outbox = new OutboxRecord();
    outbox.setPayload(rawJson);
    outboxRepository.save(outbox);
}
```

## Query-Based Liberation (Isolating Models)

[DO] Query from a dedicated View that hides internal complexity.
```sql
-- Create a View for the Query-based CDC connector
CREATE VIEW public_user_events AS
SELECT 
    u.id as user_id, 
    u.name as full_name, 
    c.name as country_name,
    u.updated_at as event_timestamp
FROM internal_users u
JOIN internal_countries c ON u.country_code_id = c.id
WHERE u.is_deleted = false; -- Handling soft deletes
```

[DON'T] Point a Query-based CDC connector directly at highly normalized internal tables.
```sql
-- ANTI-PATTERN: Exposing internal foreign keys and normalized structures to public event streams.
SELECT id, name, country_code_id, internal_status_flag, updated_at FROM internal_users;
```

## Timestamp Usage

[DO] Configure the event publisher to extract and use the source record's time.
```json
{
  "name": "jdbc-source-connector",
  "config": {
    "timestamp.column.name": "updated_at",
    "transforms": "ExtractTimestamp",
    "transforms.ExtractTimestamp.type": "org.apache.kafka.connect.transforms.InsertField$Value",
    "transforms.ExtractTimestamp.timestamp.field": "event_time"
  }
}
```

[DON'T] Allow the event broker to default the event time to the moment the liberation script publishes the message, destroying historical accuracy.