# @Domain

These rules MUST be triggered when the user requests assistance with designing, implementing, configuring, scaling, or debugging event-driven microservices that utilize Lightweight Frameworks (e.g., Apache Kafka Streams, Apache Samza in Embedded Mode). This includes tasks involving stream processing topologies, state materialization, stream-table joins, event shuffling via internal streams, and deploying JVM-based stream processors via a Container Management System (CMS).

# @Vocabulary

*   **Lightweight Framework**: A stream processing framework that lacks a dedicated resource cluster, instead relying on a Container Management System (CMS) for compute scaling and an event broker for state durability and inter-instance communication.
*   **CMS (Container Management System)**: The external orchestrator (e.g., Kubernetes) responsible for managing the deployment, horizonal scaling, and failure recovery of lightweight microservice containers.
*   **Internal Event Stream**: A private, intermediate event stream used to repartition/shuffle data to ensure data locality for downstream key-based operations (like joins or aggregations).
*   **Changelog**: An event stream stored in the event broker that acts as a durable, compacted backup of a microservice's internal state.
*   **Shuffling**: The process of repartitioning data by key to ensure all events with the same key are processed by the same instance, achieved strictly via internal event streams in lightweight frameworks.
*   **State Restoration Phase**: The initialization period where a newly spun-up instance loads state from a changelog before it is permitted to process any new events.
*   **Hot Replica**: A standby copy of a state store materialized from a changelog on an alternate instance, used to minimize downtime during scaling, rebalancing, or failure recovery.
*   **Copartitioning**: Ensuring that multiple streams have the exact same partition count and partitioner algorithm so they can be accurately joined.
*   **KStream**: A high-level abstraction representing a stateless event stream.
*   **KTable**: A high-level abstraction representing a materialized table/state store created from an event stream.
*   **Tombstone**: An event with a null value indicating the deletion of the associated key.

# @Objectives

*   Eliminate the use of dedicated, heavyweight stream processing clusters by delegating application deployment/scaling to the CMS and data locality/state durability to the event broker.
*   Enforce strict data locality for stateful operations by utilizing internal event streams for event shuffling.
*   Guarantee fault tolerance and rapid dynamic scaling by utilizing internal state stores backed by changelogs and hot replicas.
*   Execute deterministic relational event data operations (e.g., primary-key, foreign-key, stream-table-table joins) utilizing high-level MapReduce-style APIs (e.g., Kafka Streams).

# @Guidelines

*   **Architectural Dependencies**: The AI MUST NEVER provision or design dedicated framework-specific resource clusters (like Spark or Flink clusters) for lightweight applications. The AI MUST rely strictly on the CMS for scaling/deployment and the event broker for state.
*   **Event Shuffling**: To shuffle data (e.g., for `groupByKey`, aggregations, or joins), the AI MUST design the topology to write events to an internal event stream. The AI MUST NEVER implement direct instance-to-instance communication or external shuffle services.
*   **State Management**: 
    *   The AI MUST configure the framework to use internal state stores (e.g., RocksDB) for fast local access.
    *   The AI MUST ensure every internal state store is durably backed by a changelog stream located in the event broker.
*   **Scaling and State Restoration**:
    *   The AI MUST ensure that the state restoration phase is strictly prioritized. An instance MUST consume and load all internal stateful data from the changelog *before* processing any new events to avoid nondeterministic results.
    *   The AI SHOULD configure **hot replicas** (standby replicas) whenever high availability and seamless dynamic scaling (up or down) are required to bypass lengthy state rematerialization delays.
*   **Copartitioning for Joins**: Before applying any join operations between streams or tables, the AI MUST ensure all inputs are copartitioned. If inputs have different partition counts or keys, the AI MUST explicitly map/re-key the data into a new internal stream to match the target partition parameters.
*   **Handling Relational Data (Joins)**:
    *   The AI MUST leverage the table-stream duality by materializing entity streams into `KTable` abstractions for table-table or stream-table joins.
    *   When implementing join functions, the AI MUST anticipate `null` values for outer, left, right, or foreign-key joins.
    *   The AI MUST implement tombstone generation: if a join operation detects a `null` indicating a deletion upstream, the join function MUST return a `null` to emit a tombstone to downstream consumers.
*   **Language and Tooling Selection**: The AI MUST default to JVM-based languages (Java/Scala) and MapReduce-style functional APIs (or SQL-like wrappers like KSQL) when implementing Kafka Streams or Apache Samza in Embedded Mode.

# @Workflow

When generating a lightweight framework microservice implementation, the AI MUST follow this rigid sequence:

1.  **Define the Infrastructure Model**: Specify that the microservice will be deployed as an independent container managed by a CMS (e.g., Kubernetes) and connected to an event broker (e.g., Apache Kafka).
2.  **Define the Topology Inputs**: Instantiate the input streams (`KStream`) and materialize any required entity streams into state stores (`KTable`).
3.  **Implement Data Shuffling**: For any operations requiring key locality (aggregations, counts, joins), apply transformations to extract the required key, and explicitly use grouping (`groupByKey`) to force the framework to route data through an internal repartition stream.
4.  **Implement Aggregations & Materializations**: Chain aggregation functions (`aggregate`, `reduce`) to the grouped streams to build materialized state. Ensure these operations are mapped to a changelog for durability.
5.  **Execute Joins & Enrichments**: Implement the `join()` logic between the copartitioned `KStream` and/or `KTable` objects. 
6.  **Implement Join Safety (Tombstones)**: Write the explicit `joinFunction` logic to check for `null` values on both sides of the join. Instruct the function to return a `null` object to propagate tombstones when an upstream deletion is detected.
7.  **Define Outputs**: Sink the final enriched data to the output event stream (`to()`).
8.  **Configure Scalability**: Provide the configuration parameters necessary to enable hot replicas (standby tasks) and ensure changelog state restoration prioritization.

# @Examples (Do's and Don'ts)

### [DO]

**Do** implement a stream-table join using a lightweight framework (Kafka Streams API) that forces shuffling via `groupByKey()`, materializes state, and handles tombstones in the join function:

```java
KStream<WindowKey, Actions> userSessions = builder.stream("Advertisement-Sessions");

// Transform and shuffle data to ensure data locality by AdvertisementId
KTable<Long, Long> conversions = userSessions
    .flatMap((key, value) -> extractConversions(value)) // flatMap changes key
    .groupByKey() // Forces an internal event stream shuffle for copartitioning
    .aggregate(
        () -> 0L,
        (aggKey, newValue, aggValue) -> aggValue + newValue,
        Materialized.as("Total-Advertisement-Conversions") // Backed by a changelog
    );

// Materialize the entity stream into a KTable
KTable<Long, Advertisement> advertisements = builder.table("Advertisements");

// Join the copartitioned tables
conversions.join(advertisements, (sum, ad) -> {
    // Safely handle nulls and emit tombstones for deletions
    if (sum == null || ad == null) {
        return null; // Return tombstone
    }
    return new EnrichedAd(sum, ad.name, ad.type);
}).toStream().to("Enriched-Advertising-Engagements");
```

### [DON'T]

**Don't** attempt to shuffle data using external HTTP calls, direct instance-to-instance RPCs, or external shuffle services when using a lightweight framework.

```java
// ANTI-PATTERN: Attempting to shuffle data by making direct API calls to other instances
KStream<String, Event> stream = builder.stream("Input-Stream");

stream.mapValues(value -> {
    // NEVER DO THIS in a lightweight framework. 
    // Data locality must be achieved via internal event streams (groupByKey), not direct network calls.
    ExternalInstanceClient.sendToCorrectInstance(value.getNewKey(), value);
    return value;
});
```

### [DON'T]

**Don't** ignore `null` values in a join function, as this will crash the application when upstream deletions (tombstones) occur.

```java
// ANTI-PATTERN: Failing to check for nulls in a join function
conversions.join(advertisements, (sum, ad) -> {
    // If an advertisement was deleted, 'ad' will be null, and ad.name will throw a NullPointerException
    return new EnrichedAd(sum, ad.name, ad.type); 
});
```

### [DON'T]

**Don't** process new events before state restoration is complete.

```java
// ANTI-PATTERN: Bypassing changelog restoration to immediately process new events
// Lightweight frameworks MUST strictly prioritize consuming from the changelog to rebuild internal state stores BEFORE processing new events to prevent nondeterministic results. Do not override this lifecycle behavior.
```