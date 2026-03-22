@Domain
These rules are triggered whenever the AI is tasked with designing, modifying, or reviewing event-driven data schemas, Kafka topics, payload structures, schema migrations, message error-handling mechanisms, or data deletion/GDPR compliance strategies in a streaming architecture.

@Vocabulary
- **Schema-on-Read**: A pattern where the application layer translates or handles multiple, potentially incompatible data schemas coexisting in the same topic, rather than forcing a strict database-level migration.
- **Backward Compatibility**: A schema evolution state where programs using a NEW schema can successfully read messages written using the OLD schema.
- **Forward Compatibility**: A schema evolution state where programs using an OLD schema can successfully read messages written using the NEW schema (ignoring unrecognized new fields).
- **Schema Registry**: A centralized repository (e.g., Confluent Schema Registry) that stores, versions, and validates schemas (like Avro) to enforce compatibility contracts between producers and consumers.
- **Dual Schema Upgrade Window**: A migration pattern for non-backward-compatible changes involving two concurrent topics (v1 and v2) and an intermediate translation layer (e.g., Kafka Streams) to provide clients time to upgrade.
- **Dead Letter Queue (DLQ) / Error Queue**: A dedicated topic used to hold messages that consumers cannot read or process due to semantic errors or payload corruption, ensuring the main processing loop is not blocked.
- **Tombstone Message**: A message sent to a compacted topic consisting of an existing key and a `null` value, which flags the record for physical deletion during the next compaction cycle.
- **Compacted Topic**: A Kafka topic retention policy that retains only the most recent message for a specific key, enabling key-based updates and deletes.
- **Crypto Shredding**: A data deletion strategy where data is encrypted, and the decryption key is deleted, rendering the data permanently unreadable (an alternative to physical deletion).
- **CDC (Change Data Capture)**: A mechanism that monitors database write-ahead logs to propagate inserts, updates, and deletes directly into Kafka.

@Objectives
- Guarantee that consumers and producers never break due to unexpected or incompatible payload structures.
- Safely manage the lifecycle of data across time, handling both backward-compatible and breaking schema changes with zero downtime.
- Ensure strict compliance with data privacy regulations (e.g., GDPR) by implementing bulletproof physical data deletion mechanisms.
- Maintain continuous system availability by isolating corrupted or semantically invalid messages from the main processing pipeline.
- Enforce strict security and access boundaries between internal (private) and shared (public) event streams.

@Guidelines

### Schema Format & Evolution Rules
- The AI MUST define all event schemas using evolvable formats such as Avro, Protobuf, or JSON Schema.
- The AI MUST NEVER use Java serialization or any other non-evolvable format for messages crossing independent service boundaries.
- To maintain backward compatibility, the AI MUST ONLY apply additive changes (e.g., adding new optional fields).
- The AI MUST NEVER remove, rename, or change the type of existing fields in an active schema. If a move is required, the AI MUST simulate it by cloning the field and maintaining both until a breaking change is scheduled.
- The AI MUST mandate the use of a Schema Registry to validate messages on publication, ensuring incompatible messages are rejected before entering the log.

### Breaking Changes (Non-Backward-Compatible) Rules
- When a breaking change is unavoidable, the AI MUST NOT apply the change to the existing topic.
- The AI MUST implement the **Dual Schema Upgrade Window** pattern by creating a new topic (e.g., `[topic-name]-v2`).
- To handle historical data (back-population), the AI MUST connect the v1 and v2 topics using a stream processing job (e.g., Kafka Streams) that up-converts v1 messages to v2, or down-converts v2 to v1, depending on the migration strategy.

### Collaboration & Governance Rules
- The AI MUST treat schemas as code. All schema definitions MUST be version-controlled in Git.
- The AI MUST require Pull Requests (PRs) for any schema changes to establish consensus and provide an audit trail across affected teams.

### Error Handling Rules (Unreadable Messages)
- The AI MUST NOT allow a consumer application to crash or stall when encountering semantic errors (e.g., negative quantities) or parsing errors (e.g., corrupted bytes).
- The AI MUST implement an Error Queue (Dead Letter Queue) pattern. Unprocessable messages MUST be caught, wrapped with context/metadata, and published to the error topic so the consumer can advance its offset.

### Data Deletion & Privacy Rules (GDPR)
- For standard retention topics, the AI MUST rely on expiration to remove data. If explicit removal is needed before expiration, the AI MUST write a new message with a "delete marker" field (soft delete).
- For strict physical deletion (e.g., GDPR "Right to be Forgotten"), the AI MUST route the data to a **Compacted Topic**.
- To physically delete a record, the AI MUST instruct the producer to emit a Tombstone Message (the target `key` paired with a `null` payload).
- If deletion is required by a secondary identifier (e.g., deleting by `CustomerId` when the topic is keyed by `ProductId`), the AI MUST design a composite key (`[ProductId][CustomerId]`), use a custom partitioner to partition strictly by `ProductId`, and issue tombstones using the full composite key.
- If data originates from an external database, the AI MUST utilize CDC connectors to ensure database deletes automatically propagate as tombstones in Kafka.

### Topic Segregation Rules
- The AI MUST explicitly separate internal/private topics (used for internal service state/Event Sourcing) from public/shared topics (used for inter-service communication).
- The AI MUST enforce this boundary using Kafka's authorization interfaces (ACLs) and TLS/SASL to prevent unauthorized coupling to private streams.

@Workflow
When tasked with creating or modifying an event schema or data lifecycle process, the AI MUST follow this algorithmic process:

1. **Assess the Change Type**: Determine if the requested schema modification is additive (backward-compatible) or destructive (breaking).
2. **Handle Additive Changes**:
   - Update the schema file (.avsc, .proto, etc.) by appending the new fields as optional/nullable.
   - Instruct the user to open a Git PR for cross-team review.
   - Deploy the schema to the Schema Registry.
3. **Handle Breaking Changes (Dual Schema Upgrade Window)**:
   - Create a `v2` topic definition alongside the `v1` topic.
   - Write a Kafka Streams topology to up-convert historical `v1` records into the `v2` topic, OR down-convert `v2` records to the `v1` topic.
   - Instruct the producer service (the single writer) to point to the new configuration.
   - Output instructions for consumers to migrate to the `v2` topic over a defined window.
4. **Implement Resilience**:
   - Wrap the consumer's deserialization and processing logic in a try-catch block.
   - In the catch block, construct an error payload and route the failed message to `[topic-name]-error-dlq`.
5. **Configure Deletion Mechanics**:
   - If the data contains PII or falls under GDPR, ensure the target topic is configured with `cleanup.policy=compact`.
   - Provide the code/command to issue a `null` payload tombstone for a given key to execute a physical delete.

@Examples (Do's and Don'ts)

### Schema Compatibility
[DO] Add a new optional field to an existing Avro schema to maintain backward compatibility.
```json
{
  "type": "record",
  "name": "Order",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "returnCode", "type": ["null", "string"], "default": null} 
  ]
}
```

[DON'T] Rename or remove a field in an existing schema used by multiple services.
```json
// Anti-pattern: Renaming "amount" to "totalAmount" breaks existing consumers.
{
  "type": "record",
  "name": "Order",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "totalAmount", "type": "double"} 
  ]
}
```

### Breaking Changes
[DO] Use Kafka Streams to map a v1 topic to a v2 topic to handle back-population during a Dual Schema Upgrade Window.
```java
// Up-convert v1 to v2
KStream<String, OrderV1> v1Orders = builder.stream("orders-v1");
KStream<String, OrderV2> v2Orders = v1Orders.mapValues(v1 -> {
    return new OrderV2(v1.getOrderId(), v1.getAmount(), "DEFAULT_RETURN_CODE");
});
v2Orders.to("orders-v2");
```

[DON'T] Force a breaking change onto an active topic and expect consumers to handle the deserialization failures.

### Error Handling
[DO] Catch parsing/semantic exceptions and route them to an error topic (DLQ).
```java
try {
    processOrder(record.value());
} catch (SemanticException | SerializationException e) {
    producer.send(new ProducerRecord<>("orders-dlq", record.key(), record.value()));
    // Offset advances safely
}
```

[DON'T] Allow the consumer to throw an unhandled exception, causing it to crash, restart, and enter an infinite crash-loop on the same offset.

### Data Deletion (GDPR)
[DO] Issue a tombstone message to a compacted topic to permanently delete a user's record.
```java
// Emitting a null value for the specific CustomerId key
producer.send(new ProducerRecord<>("customers-compacted", "customer-12345", null));
```

[DON'T] Rely on infinite retention for PII without configuring compaction, or attempt to issue a "soft delete" (e.g., `{"status": "deleted"}`) when physical removal is legally required.

### Composite Keys for Deletion
[DO] Combine keys to allow deletion by a secondary ID while maintaining strict ordering for the primary ID.
```java
// Key: [ProductId]-[CustomerId] -> "prod99-cust12"
// Custom partitioner ensures routing is based ONLY on "prod99"
producer.send(new ProducerRecord<>("orders-compacted", "prod99-cust12", null));
```

[DON'T] Key the topic solely by `ProductId` and then attempt to iterate through and manually delete or overwrite specific customer data within the payload.