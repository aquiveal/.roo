# @Domain
These rules MUST be activated when the AI is tasked with designing, writing, reviewing, or modifying stateless event-driven microservices, specifically focusing on event processing topologies, consuming and producing events, applying data transformations (filtering, mapping, routing), branching/merging event streams, and configuring partition assignments, repartitioning, or copartitioning strategies.

# @Vocabulary
*   **Topology**: The internal data-driven operations performed on incoming events within a single microservice, including transformation, branching, merging, and emission.
*   **Transformations**: Operations applied to a single event that emit zero or more output events.
    *   *Filter*: Evaluates an event against criteria and drops it if it fails. Emits zero or one event.
    *   *Map*: Modifies the key and/or value of an event. Emits exactly one event.
    *   *MapValue*: Modifies only the value of an event, leaving the key completely intact. Emits exactly one event.
*   **Branching**: Applying logical operators to an event to route it to different output streams (e.g., routing based on geographic region, or sending to a dead-letter stream on error).
*   **Merging**: Consuming events from multiple separate input streams and combining them into a single output stream.
*   **Repartitioning**: Creating a new event stream with a different partition count, a different event key, or a different partitioner logic to ensure specific data locality downstream.
*   **Copartitioning**: Repartitioning an event stream so it has the exact same partition count, partition assignor logic, and key distribution as another stream, allowing the two streams to be securely joined.
*   **Data Locality**: The guarantee that all events sharing the same key are routed to the same partition and subsequently processed by the same single consumer instance.
*   **Partition Assignor**: The algorithm/component responsible for distributing event stream partitions across the active consumer instances within a consumer group.
*   **Round-Robin Assignment**: A partition assignment strategy where partitions are cyclically distributed to consumer instances to balance load.
*   **Static Assignment**: A partition assignment strategy where specific partitions are strictly mapped to specific consumers (useful for large materialized states).
*   **Custom Assignment**: Leveraging external signals (like input lag) to dynamically distribute partition assignments.

# @Objectives
*   Implement a robust, at-least-once event processing loop utilizing a strict consume-process-produce-commit lifecycle.
*   Design efficient, stateless stream processing topologies utilizing the correct transformation functions (`Map` vs. `MapValue`).
*   Ensure strict data locality by correctly utilizing repartitioning whenever an event's key is modified.
*   Guarantee the safety of stream joins by strictly enforcing copartitioning rules (identical keys, algorithms, and partition counts).
*   Manage consumer group workloads intelligently through appropriate partition assignment strategies and graceful handling of rebalances.

# @Guidelines
*   **The Microservice Loop**: The AI MUST structure the core of the event-driven microservice using the following sequential lifecycle: poll events -> apply topology/business logic -> produce output events -> commit offsets.
*   **Offset Committing**: The AI MUST ensure offsets are committed ONLY after the successful processing and production of downstream events to guarantee at-least-once processing.
*   **Transformation Selection**: 
    *   When altering the payload but keeping the key intact, the AI MUST use `MapValue` to avoid unnecessary downstream repartitioning overhead.
    *   When altering the key of an event, the AI MUST use `Map`.
*   **Mandatory Repartitioning**: If a `Map` transformation alters the event key, the AI MUST immediately repartition the stream based on the new key using a deterministic hash function to restore data locality.
*   **Branching Rules**: The AI MUST implement branching logic to handle exceptions, specifically routing malformed or unprocessable events to a dedicated dead-letter stream rather than dropping them silently or halting the entire processor.
*   **Merging Rules**: If the AI merges multiple streams, it MUST define a new unified schema representing the merged domain. The AI MUST NOT merge streams if a unified domain schema logically cannot be created.
*   **Copartitioning Strictness**: Before joining two streams, the AI MUST enforce copartitioning. The AI MUST write validation checks to ensure both streams have the exact same partition count. If the counts differ, the AI MUST throw a fatal exception or force a repartitioning of one stream to match the other.
*   **Consumer Instance Assignment**: The AI MUST assign copartitioned partitions to the exact same consumer instance to ensure successful data locality during processing.
*   **Handling Reassignments**: The AI MUST momentarily suspend processing logic while partitions are being reassigned or revoked to prevent race conditions and duplicate event processing.
*   **Stateless Recovery**: When an instance fails in a stateless topology, the AI MUST NOT write logic to restore state. The AI MUST rely solely on the partition assignor to reallocate the partition to a healthy instance, which will resume processing from the last committed offset.

# @Workflow
When tasked with building or modifying an event-driven processing topology, the AI MUST follow this exact algorithmic process:
1.  **Initialize Clients**: Instantiate the consumer client (assigning it to the correct consumer group) and the producer client.
2.  **Start Polling Loop**: Create an infinite loop that polls for new events from the input event stream(s).
3.  **Construct Topology Pipeline**: For each consumed event, apply the necessary sequence of transformations:
    *   Apply `Filter` functions first to drop irrelevant events early and save compute resources.
    *   Apply `MapValue` functions for data enrichment or payload transformation.
    *   Apply `Map` functions if the business logic requires a new key.
4.  **Enforce Locality**: If step 3 included a `Map` function that altered the key, inject a Repartitioning step using a deterministic partitioner to route the event to the correct partition based on the new key.
5.  **Apply Routing/Branching**: Evaluate branching conditions. Route valid events to the primary logic path and invalid/failed events to a dead-letter stream.
6.  **Validate Copartitioning (If Joining)**: If the topology requires joining with another stream, execute a validation check asserting `streamA.partitionCount == streamB.partitionCount`. If false, trigger a repartitioning topology.
7.  **Produce Output**: Send the fully processed events to their respective output event stream(s) via the producer client.
8.  **Commit Offsets**: Issue the offset commit command to the consumer client ONLY after step 7 successfully completes.

# @Examples (Do's and Don'ts)

### The Core Processing Loop
**[DO]** Commit offsets only after full processing and production:
```java
while(true) {
    InputEvent event = consumerClient.pollOneEvent(inputEventStream);
    OutputEvent output = processEvent(event);
    producerClient.produceEventToStream(outputEventStream, output);
    // At-least-once processing guarantee
    consumerClient.commitOffsets();
}
```

**[DON'T]** Commit offsets immediately upon consumption, risking data loss on crash:
```java
while(true) {
    InputEvent event = consumerClient.pollOneEvent(inputEventStream);
    consumerClient.commitOffsets(); // DANGER: Crash here means the event is lost forever
    OutputEvent output = processEvent(event);
    producerClient.produceEventToStream(outputEventStream, output);
}
```

### Transformations & Repartitioning
**[DO]** Use `MapValue` when the key is unchanged, and use `Map` followed by a repartition when the key changes:
```java
// Modifying only the payload
stream.mapValue(event -> formatPayload(event))
      .to(outputStream);

// Modifying the key requires repartitioning for data locality
stream.map((key, value) -> new KeyValue(extractNewKey(value), value))
      .repartition(new CustomPartitioner()) // Mandatory
      .to(outputStream);
```

**[DON'T]** Change a key using a basic transform without explicitly repartitioning the stream, which destroys data locality:
```java
stream.map((key, value) -> new KeyValue(extractNewKey(value), value))
      .to(outputStream); // DANGER: Events with the same new key are now scattered across random partitions
```

### Copartitioning
**[DO]** Validate partition counts before applying logic that requires data locality from multiple streams:
```java
if (streamA.getPartitionCount() != streamB.getPartitionCount()) {
    throw new IllegalStateException("Cannot join streams: Partition counts do not match. Copartitioning required.");
}
streamA.join(streamB, ...);
```

**[DON'T]** Assume streams can be safely merged or joined just because they share the same key type:
```java
// DANGER: If streamA has 10 partitions and streamB has 12, 
// events with the same key will be assigned to different consumer instances.
streamA.join(streamB, ...); 
```

### Branching
**[DO]** Branch errors to a dead-letter stream:
```java
OutputEvent output;
try {
    output = processEvent(event);
    producerClient.produceEventToStream(primaryStream, output);
} catch (ProcessingException e) {
    producerClient.produceEventToStream(deadLetterStream, event);
}
```

**[DON'T]** Discard failed events silently, breaking the immutable history of the workflow:
```java
try {
    output = processEvent(event);
    producerClient.produceEventToStream(primaryStream, output);
} catch (ProcessingException e) {
    // DANGER: Event is swallowed and lost
    continue; 
}
```