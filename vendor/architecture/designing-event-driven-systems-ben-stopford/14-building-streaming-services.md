@Domain
These rules are triggered whenever the AI is tasked with designing, architecting, implementing, or refactoring streaming services, stateful stream processing applications, or event-driven microservices using Apache Kafka, Kafka Streams, or KSQL. This includes handling data topologies, event-sourced views, CQRS implementations, stream joins, and concurrent stateful operations.

@Vocabulary
- **Join-Filter-Process**: The standard three-step streaming topology pattern involving preparing streams/tables (Join), removing unneeded data or aggregating (Filter), and executing business logic to produce an output (Process).
- **Event-Sourced View**: A queryable state store (often partitioned over multiple instances) materialized directly from an event stream to serve as the read-side of a CQRS architecture.
- **Interactive Queries**: A Kafka Streams feature used to route HTTP GET requests to the specific service instance holding the correct partition for a requested key.
- **Collapsing CQRS**: The technique of using a blocking read (long polling/nonblocking IO) on a read-model to wait for an asynchronous event to arrive, making the system appear synchronous to the client (allowing clients to "read their own writes").
- **Co-partitioned**: Data arranged such that the records to be joined share the same key and partition, ensuring no additional network access is required during the join.
- **Rekey**: The operation of redistributing data across nodes by changing the message key (e.g., using `selectKey`) to align with a target table's primary key for a join, or to isolate a critical section for concurrency.
- **Staged Execution**: Chaining multiple stream operations where each stage requires a different data distribution profile (key), connected via rekey operations.

@Objectives
- To map synchronous REST/HTTP requests to asynchronous, event-driven workflows seamlessly.
- To implement scalable, concurrent, stateful operations without relying on shared external databases or remote transactions.
- To strictly enforce the Join-Filter-Process pipeline structure for stream processing topologies.
- To correctly manage data partitioning, rekeying, and co-partitioning to enable highly performant, localized stream joins and aggregations.
- To guarantee atomic state mutations by coupling Kafka transactions with partitioned state stores.

@Guidelines
- **Architectural Mapping (REST to Events)**: When integrating synchronous interfaces (e.g., REST endpoints) with streaming systems, MUST map POST requests to event creation (write model) and GET requests to Event-Sourced Views (read model) following the CQRS pattern.
- **Single Writer Retention**: When aggregating validations or parallel processes (e.g., Fraud, Inventory, Details), MUST push the results through a separate intermediary topic (e.g., `Order Validations`) to ensure the primary entity topic (e.g., `Orders`) retains a single writing service.
- **Join-Filter-Process Adherence**: Stream processing logic MUST strictly follow the Join-Filter-Process pattern. Do not perform heavy business logic before joining and filtering.
- **Building Event-Sourced Views**: 
  - MUST use `groupByKey()` and an aggregation/reduce function (e.g., `.reduce((agg, newVal) -> newVal, getStateStore())`) to push streams into partitioned state stores.
  - MUST implement routing logic using Kafka Streams metadata to redirect incoming HTTP GET requests to the correct physical instance hosting the partition for the requested key.
- **Collapsing CQRS (Read-Your-Own-Writes)**: When a client requires immediate confirmation of an asynchronous write, MUST implement a blocking read (via long polling and nonblocking IO) that waits for the corresponding event to propagate into the Event-Sourced View before returning the HTTP response.
- **Scaling Concurrent Operations**: 
  - MUST NOT use shared databases or cross-process coordination/remote transactions to manage concurrent stateful operations.
  - MUST partition the event streams and stored state using a logical business key (e.g., `ProductId`). 
  - MUST ensure all state required for a computation is isolated to a single thread via this partitioning.
  - MUST wrap the state store mutation and the outbound event emission in a Kafka transaction to ensure atomicity.
- **Rekeying for Joins (Foreign Key to Primary Key)**:
  - When joining a stream to a table using an attribute that is NOT the stream's primary key (a foreign key relationship), MUST execute a rekey operation (e.g., `selectKey`) on the stream to match the table's primary key.
  - This ensures data is co-partitioned and the join can execute locally without network calls.
- **Invariant Keys for Ordering**: When utilizing Staged Execution with multiple rekey steps, the business keys used to partition the event streams MUST remain invariant across all messages relating to that entity to guarantee strict ordering.
- **Waiting for N Events**: When a service must wait for multiple validation events arriving on a single topic, MUST implement the following specific topology:
  1. Group by the key.
  2. Count the occurrences of each key (using an aggregator executed with a window).
  3. Filter the output for the exact required count.
- **Holistic Ecosystem Integration**: When architecting broader systems, leverage the Confluent ecosystem: REST Proxy for external HTTP writes, CDC (Change Data Capture) for legacy database ingestion, Single-Message Transforms for inline reformatting, and Connect Sinks (e.g., Solr, Cassandra, HDFS) for specialized read-optimized views.

@Workflow
1. **Define the Interface**: Establish the synchronous REST boundaries (Command/Write vs. Query/Read).
2. **Design the Topology**: Identify the required streams, tables, and state stores.
3. **Partition & Rekey**: Analyze join conditions and concurrency bottlenecks. Insert `.selectKey()` operations to repartition data by the correct business key to ensure co-partitioning.
4. **Implement Join-Filter-Process**: Write the DSL to join the co-partitioned streams/tables, filter irrelevant data, and route to a processing function.
5. **Manage State**: Define `KeyValueStore` operations for critical sections. Ensure Kafka transactions are enabled to atomically commit state store changes and outbound topic messages.
6. **Materialize the View**: Build the CQRS read-side by grouping by key, reducing into a state store, and exposing via interactive queries with proper partition-aware routing.
7. **Address Synchronicity**: If the client requires synchronous feedback, implement long polling on the materialized view to collapse the CQRS asynchronicity.

@Examples (Do's and Don'ts)

**Principle: Join-Filter-Process Pattern**
- [DO] Structure stream topologies logically by joining, filtering, then processing:
  ```java
  orders.join(customers, Tuple::new) // JOIN
        .filter((k, tuple) -> tuple.customer.level().equals(PLATINUM) && tuple.order.state().equals(CONFIRMED)) // FILTER
        .peek((k, tuple) -> emailer.sendMail(tuple)); // PROCESS
  ```
- [DON'T] Mix business logic or external actions before data is fully joined and filtered, causing unnecessary computation on dropped data.

**Principle: Rekeying for Co-partitioned Joins**
- [DO] Use `selectKey` to repartition a stream by the target table's primary key before joining:
  ```java
  // Rekey stream from OrderId to ProductId to match the Inventory table
  KStream<Product, Order> rekeyedOrders = orders.selectKey((id, order) -> order.getProduct());
  rekeyedOrders.join(inventoryTable, ...);
  ```
- [DON'T] Attempt to join a stream and a KTable on a non-primary key without rekeying, which will fail or require unsupported cross-network lookups.

**Principle: Event-Sourced View Materialization**
- [DO] Use `groupByKey` and `reduce` to materialize a destructive (latest-value) event-sourced view into a state store:
  ```java
  builder.stream(ORDERS.name(), serializer)
         .groupByKey(groupSerializer)
         .reduce((agg, newVal) -> newVal, Materialized.as("orders-state-store"));
  ```
- [DON'T] Rely on external databases for localized, tightly-coupled event-sourced views if Kafka Streams state stores can natively handle the partitioned query workload.

**Principle: Waiting for N Events**
- [DO] Use a windowed count and filter when waiting for a specific number of responses on a single topic:
  ```java
  validationStream
      .groupByKey()
      .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
      .count()
      .filter((key, count) -> count == 3) // Waiting for exactly 3 validations
      .toStream()
      ...
  ```
- [DON'T] Maintain custom in-memory lists or external database counters to track how many validation events have arrived.

**Principle: Scaling Concurrent Operations**
- [DO] Rely on Kafka Streams' thread partitioning and local state stores wrapped in transactions for critical sections:
  ```java
  // Execution is inherently thread-safe per ProductId due to partitioning
  KeyValueStore<Product, Long> store = context.getStateStore(RESERVED);
  Long reserved = store.get(order.getProduct());
  store.put(order.getProduct(), reserved + order.getQuantity());
  ```
- [DON'T] Introduce distributed locks (e.g., Redis locks) or shared external transactional databases to manage concurrent state mutations in a streaming service.