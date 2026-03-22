@Domain
Triggered when the AI is tasked with designing, implementing, or refactoring data storage layers, streaming pipelines, database views, ETL processes, or microservice data integrations within an event-driven or Apache Kafka-based architecture.

@Vocabulary
- **Lean Data**: The practice of services extracting and storing only the strictly necessary, minimal subset of data required for their specific use case at a given point in time, discarding all other fields.
- **Event-Sourced View**: A read-optimized, lightweight database, cache, or state store that is populated entirely by consuming an immutable event log. It can be dropped and completely regenerated at any time.
- **Source of Truth**: The central, immutable event log (e.g., Kafka topic) that holds the authoritative record of facts, rendering downstream databases as mere derivative caches.
- **Data Divergence**: The degradation of data quality and accuracy that occurs when data is copied, mutated, and passed through multiple intermediate services or mutable databases (the "game of telephone" effect).
- **Deterministic Rebuild**: The process of recreating a database or view perfectly from scratch by replaying the immutable event log from offset zero.

@Objectives
- Treat downstream databases and caches as completely ephemeral and easily replaceable.
- Minimize the data footprint and schema coupling of services by enforcing aggressive data stripping and filtering upon ingestion.
- Eradicate Data Divergence by ensuring all views tie directly back to the central, immutable event log rather than chaining off of intermediate mutable stores.
- Guarantee that infrastructure deployments and schema migrations rely on deterministic rebuilds from the log rather than stateful database migrations.

@Guidelines
- **Enforce Ephemeral Persistence**: The AI MUST NEVER treat a downstream microservice database as the Source of Truth. If the messaging layer retains data, the downstream database DOES NOT need to.
- **Aggressive Truncation**: When generating consumption logic, the AI MUST explicitly drop all unused fields from incoming event documents. Retain only the exact fields required for the service's immediate business logic to maximize storage efficiency and minimize schema coupling.
- **Prefer View Regeneration over Migration**: When handling schema changes or environment promotions (e.g., moving from UAT to PROD), the AI MUST strongly prefer recreating views directly from the log rather than using database migration scripts (e.g., `ALTER TABLE`) or copying database files between environments.
- **Storage Technology Selection**: When provisioning an Event-Sourced View, the AI MUST recommend write-optimized, memory-optimized, or log-structured datastores (e.g., RocksDB, Redis, MemSQL, Hazelcast, Couchbase, Cassandra) to ensure worst-case complete rebuilds are highly performant.
- **Mitigate Rebuild Latency**: For large datasets, the AI MUST implement parallel view generation. Create the new view in the background while the old view serves traffic, cutting over only when the new view has fully caught up with the event log.
- **Prevent Data Divergence**: The AI MUST explicitly prohibit architectures that extract data, mutate it in a database, and expose it via synchronous APIs for other services to copy. Instead, route consumers directly to the central event log.

@Workflow
1. **Identify Required Data**: Analyze the target service's business logic to determine the absolute minimum set of fields required.
2. **Implement Truncation**: Write stream processing code (Kafka Streams DSL, KSQL, or Connect SMTs) to filter and map the incoming fat event into a Lean Data structure.
3. **Provision Ephemeral Storage**: Select a write-optimized database or embedded state store to hold the resulting Lean Data. Explicitly configure it without extensive backup mechanisms, as the log is the backup.
4. **Establish Rebuild Mechanics**: Document and implement the capability to seamlessly drop the local datastore and reset the consumer offset to 0 (e.g., via Kafka Streams Reset tool) to trigger a Deterministic Rebuild.
5. **Design Deployment/Cutover**: For schema migrations or application updates requiring new data shapes, script the infrastructure to stand up the new view in parallel, rehydrate it from the log, and swap routing once caught up.

@Examples (Do's and Don'ts)

[DO]
```java
// DO: Aggressively truncate data to keep the view lean and loosely coupled.
KStream<String, WarehouseEvent> rawEvents = builder.stream("warehouse-inventory");

KTable<String, LeanInventory> inventoryView = rawEvents
    // Strip the massive WarehouseEvent down to just ProductId and StockCount
    .mapValues(event -> new LeanInventory(event.getProductId(), event.getStockCount()))
    .groupByKey()
    .reduce((oldVal, newVal) -> newVal, Materialized.as("lean-inventory-store"));
```

[DON'T]
```java
// DON'T: Ingest the entire fat event into a local database and treat it as a durable asset.
KStream<String, WarehouseEvent> rawEvents = builder.stream("warehouse-inventory");

// Anti-pattern: Storing the entire object tightly couples the service to the full schema
// and bloats the local database, making deterministic rebuilds slow and expensive.
rawEvents.toTable(Materialized.<String, WarehouseEvent, KeyValueStore<Bytes, byte[]>>as("fat-inventory-store"));
```

[DO]
```sql
-- DO: Use KSQL to create a lean, purpose-built view directly from the central source of truth.
CREATE STREAM lean_orders AS 
  SELECT order_id, customer_id, total_amount 
  FROM raw_fat_orders_topic;
```

[DON'T]
```bash
# DON'T: Use database dump/restore tools to move state between environments.
# Anti-pattern: Treating the database as the source of truth instead of the log.
pg_dump -U admin -d uat_orders_db > uat_orders.sql
psql -U admin -d prod_orders_db < uat_orders.sql
```

[DO]
```bash
# DO: Use native stream reset tools to drop the local database and reconstruct the view from the immutable log.
kafka-streams-application-reset.sh --application-id inventory-service --input-topics warehouse-inventory
```