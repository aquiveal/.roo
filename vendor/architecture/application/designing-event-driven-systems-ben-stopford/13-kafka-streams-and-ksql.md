# @Domain
These rules MUST activate when the AI is tasked with designing, implementing, or debugging event-driven microservices, real-time analytics, or data processing pipelines using Apache Kafka, Kafka Streams API, or KSQL. This applies to architectural planning, stream-topology definition, and writing code for stateful or stateless stream processors.

# @Vocabulary
- **Kafka Streams API**: The core API for stream processing on the JVM (Java, Scala, Clojure), combining a declarative DSL with functional per-message operations.
- **KSQL**: A SQL-like declarative wrapper for Kafka stream processing, run standalone and accessed remotely, typically used for non-JVM ecosystems.
- **DSL (Domain-Specific Language)**: The declarative interface in Kafka Streams used to slice, dice, join, filter, group, and aggregate event streams.
- **Sidecar Pattern**: An architectural pattern where KSQL runs standalone alongside a non-JVM application (e.g., a Node.js client) to handle stream processing externally.
- **Stream-Stream Join**: A temporal join between two infinite streams that behaves as a logical AND, requiring events in both streams to be present within a defined retention window.
- **State Store**: A local, disk-backed hash table held inside the Kafka Streams API used to overflow buffered streams to disk or store arbitrary application state.
- **Table (KTable)**: A local manifestation of a complete, usually compacted, Kafka topic held in a state store by key. Represents an evolving dataset with infinite retention.
- **Global KTable**: A broadcast table where a complete copy of the entire dataset exists on every node/instance of the service.
- **Partitioned Table (KTable)**: A table where the dataset is spread (partitioned) across all instances of the service.
- **Changelog Topic**: A Kafka topic used to continuously back up the data saved in a local State Store, ensuring fault tolerance and durability upon restart.
- **Repartition / Rekey**: The act of changing the key of a stream or table to allow joining on an attribute other than the original primary key.

# @Objectives
- Build event-driven services that cleanly separate declarative stream preparation (joining/filtering) from functional business execution.
- Select the appropriate Kafka toolset strictly based on the target language ecosystem (JVM vs. non-JVM).
- Manage local state efficiently by deliberately choosing between Streams, KTables, Global KTables, and isolated State Stores.
- Ensure all streaming topologies account for distributed data constraints, specifically regarding partitioning, broadcasting, and join keys.

# @Guidelines

### Language and Ecosystem Selection
- The AI MUST use the **Kafka Streams API** (and its DSL) when building services in JVM languages (Java, Scala, Clojure).
- The AI MUST use **KSQL** combined with the **Sidecar Pattern** and a native Kafka client when building services in non-JVM languages (e.g., Node.js, Python).

### Architecture and Logic Separation
- The AI MUST structure streaming applications into two distinct phases: 
  1. A **declarative preparation phase** (using DSL or KSQL) to join, filter, and aggregate data.
  2. A **functional processing phase** (using `.peek()`, `.map()`, or native consumer logic) to apply arbitrary business logic or side-effects (e.g., sending an email).
- The AI MUST treat Stream-Stream joins as a "logical AND" and configure retention windows to buffer incoming events, ensuring the join can complete regardless of which event arrives first.

### Table and State Management
- The AI MUST use **Tables** instead of Streams when performing lookups or data enrichments.
- The AI MUST enforce the following rules when selecting Table types:
  - Use **Global KTables** for small lookup tables or "star joins". The AI MUST leverage Global KTables when joining on a foreign key (any attribute other than the primary key).
  - Use regular **KTables** for large datasets to enable horizontal scaling. 
- The AI MUST NOT perform a join on a regular KTable using a non-primary key without explicitly inserting a repartition/rekey operation first.
- The AI MUST use **State Stores** to persist application-specific state (e.g., operational statistics, custom aggregations).
- The AI MUST ensure that every State Store is configured with a **Changelog Topic** to inherit Kafka's durability guarantees and allow state restoration upon node failure/restart.

# @Workflow
1. **Determine the Ecosystem**: Identify the programming language of the target application. If JVM, initialize Kafka Streams DSL. If non-JVM, initialize a KSQL script and configure a native consumer client.
2. **Classify the Inputs**: Categorize incoming Kafka topics as either infinite event streams (requiring temporal windows) or complete datasets/reference data (requiring Tables).
3. **Select Table Strategy**: For reference data, analyze dataset size and join requirements. Select Global KTable for small datasets or foreign-key joins. Select KTable for large datasets requiring primary-key joins.
4. **Draft the Topology (Preparation)**: Write the declarative DSL or KSQL statement to join streams/tables and filter out irrelevant events.
5. **Draft the Topology (Execution)**: Append functional per-message operations (`peek`, `map`, `transform`) to the prepared stream to execute the core business logic.
6. **Configure State Resilience**: Whenever custom state is mutated, instantiate a disk-backed State Store and explicitly link it to a changelog topic for recovery.

# @Examples (Do's and Don'ts)

### [DO] Mix Declarative and Functional Styles in Kafka Streams
**DO** prepare the data stream using the DSL, then apply a functional operation for side-effects.
```java
// DO: Join, filter, and process sequentially in Kafka Streams
orders.join(customers, Tuple::new)
      .filter((k, tuple) -> tuple.customer.level().equals(PLATINUM) && tuple.order.state().equals(CONFIRMED))
      .peek((k, tuple) -> emailer.sendMail(tuple));
```

### [DON'T] Implement Complex Stream Logic Inside Consumer Loops
**DON'T** manually buffer and join streams inside a standard Kafka Consumer loop.
```java
// DON'T: Manually hold state and join inside a consumer for JVM applications
while (true) {
    ConsumerRecords records = consumer.poll(100);
    // Manual buffering, checking customer status, and joining logic here (ANTI-PATTERN)
}
```

### [DO] Use KSQL Sidecar for Non-JVM Languages
**DO** offload the declarative join to KSQL when using Node.js, then consume the result.
```sql
-- DO: KSQL preparation
CREATE STREAM platinum_emails AS 
SELECT * FROM orders 
WHERE client_level == 'PLATINUM' AND state == 'CONFIRMED';
```
```javascript
// DO: Node.js consumption of the prepared stream
consumer.subscribe({ topic: 'platinum_emails' });
consumer.run({
    eachMessage: async ({ message }) => {
        emailer.sendMail(message.value);
    }
});
```

### [DON'T] Misconfigure Table Joins
**DON'T** attempt a foreign-key join on a standard partitioned KTable without rekeying.
```java
// DON'T: Joining a KTable on an attribute that is not its primary key
KStream<OrderId, Order> orders = builder.stream("orders");
KTable<CustomerId, Customer> customers = builder.table("customers");

// This will fail or yield incorrect results if the order stream's key is not CustomerId
orders.join(customers, (order, customer) -> new Tuple(order, customer)); 
```

### [DO] Use Global KTable for Foreign Key Joins
**DO** use Global KTable if you need to broadcast reference data for non-primary key lookups.
```java
// DO: Using GlobalKTable for flexible joining
KStream<OrderId, Order> orders = builder.stream("orders");
GlobalKTable<CustomerId, Customer> customers = builder.globalTable("customers");

orders.join(customers, 
    (orderId, order) -> order.getCustomerId(), // foreign key extraction
    (order, customer) -> new Tuple(order, customer)
);
```

### [DON'T] Lose Local State
**DON'T** rely entirely on in-memory variables for state tracking across events.
```java
// DON'T: Using standard in-memory variables that will be lost on crash
int emailsSent = 0;
stream.peek((k, v) -> { emailsSent++; });
```

### [DO] Use State Stores for Custom State
**DO** use Kafka Streams state stores backed by changelog topics for local state.
```java
// DO: Using a disk-backed, replicated state store
stream.process(() -> new Processor<String, Tuple>() {
    private KeyValueStore<String, Integer> statsStore;
    
    public void init(ProcessorContext context) {
        this.statsStore = (KeyValueStore<String, Integer>) context.getStateStore("email-stats-store");
    }
    
    public void process(String key, Tuple value) {
        // Logic using statsStore.put() and statsStore.get()
    }
}, "email-stats-store");
```