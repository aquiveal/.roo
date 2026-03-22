@Domain
Triggered when the user requests assistance with designing, implementing, refactoring, or reviewing stream processing applications, event-driven microservices, stateful streaming topologies, time-series event processing, windowing functions, or any task involving the synchronization, ordering, or reprocessing of event streams.

@Vocabulary
*   **Determinism**: The principle that an event-driven microservice must produce the exact same output whether it is processing events in near-real-time or reprocessing historical events from the beginning of time.
*   **Event Time**: The local timestamp assigned to the event by the producer at the exact moment the event occurred.
*   **Broker Ingestion Time**: The timestamp assigned to the event by the event broker upon receipt.
*   **Consumer Ingestion Time**: The wall-clock time at which the event is ingested by the consumer application.
*   **Processing Time**: The wall-clock time at which the event is actively processed by the consumer's business logic.
*   **Event Scheduling**: The process of selecting the correct temporal order of events to process when consuming from multiple input partitions, ensuring deterministic interleaving.
*   **Watermark**: A declaration (used heavily in frameworks like Spark, Flink, Beam) that propagates through a processing topology indicating that all data of a given event time (or earlier) has been processed.
*   **Stream Time**: A time-tracking approach (used heavily in Kafka Streams) where a consumer subtopology maintains a time based on the highest event-time timestamp of the events it has successfully processed.
*   **Out-of-Order Event**: An event whose timestamp is chronologically earlier than events that have already been processed in the stream (often caused by multiple producers, repartitioning, or network delays).
*   **Late-Arriving Event (Late Event)**: An out-of-order event that misses a consumer-specific deadline (e.g., arrives after the watermark or stream time has advanced past the event's timestamp or window boundary).
*   **Tumbling Window**: A time-based aggregation window of fixed size where previous and subsequent windows do not overlap.
*   **Sliding Window**: A time-based aggregation window with a fixed size and an incremental step (slide), reflecting aggregations currently in the window.
*   **Session Window**: A dynamically sized time window that terminates based on a predetermined timeout due to inactivity.
*   **Grace Period**: A specific duration the consumer waits for late-arriving events before finalizing a windowed aggregation.
*   **Reprocessing**: The act of rewinding consumer group offsets to replay and recompute an event stream from an arbitrary point in time (usually the beginning).

@Objectives
*   Achieve best-effort deterministic processing to guarantee identical outputs across near-real-time and historical reprocessing contexts.
*   Strictly decouple application processing logic from volatile wall-clock time, relying instead on canonical event timestamps.
*   Gracefully and explicitly manage out-of-order and late-arriving events according to business-defined thresholds.
*   Prevent nondeterminism caused by improperly interleaving multiple partitions, custom ad-hoc schedulers, or unsafe external request-response calls.

@Guidelines

**1. Timestamp Selection and Extraction**
*   The AI MUST default to using **Event Time** (assigned by the producer) as the authoritative timestamp for processing to accurately reflect real-world occurrences.
*   The AI MUST fallback to **Broker Ingestion Time** ONLY if the producer's local clock is known to be completely unreliable or malicious.
*   The AI MUST implement or configure a "Timestamp Extractor" at the point of consumer ingestion to pull the correct timestamp from the event payload or metadata before routing to the processing topology.
*   The AI MUST explicitly require or assume Network Time Protocol (NTP) synchronization for any distributed timestamping logic.

**2. Event Scheduling across Multiple Partitions**
*   When consuming from multiple partitions or streams, the AI MUST NOT use naive round-robin consumption. 
*   The AI MUST interleave events strictly based on their extracted timestamps (always picking the event with the oldest timestamp across all assigned input partition buffers).
*   The AI MUST avoid implementing custom event schedulers (e.g., `MessageChooser`) unless absolutely necessary, and MUST document that custom schedulers risk destroying determinism.

**3. Preventing Nondeterminism**
*   The AI MUST flag any synchronous request-response calls to external API systems within a stream processing topology as an anti-pattern and a strict violation of determinism.
*   If external calls are unavoidable, the AI MUST document the risk that reprocessing historical data will yield different results if the external state has changed.

**4. Tracking Time (Watermarks vs. Stream Time)**
*   If using Heavyweight Frameworks (Spark, Flink, Beam): The AI MUST configure **Watermarks** to propagate event time downstream and trigger the closing of windows.
*   If using Lightweight Frameworks (Kafka Streams): The AI MUST rely on **Stream Time**, ensuring that time only moves forward based on the highest seen timestamp per subtopology. The AI MUST NOT overwrite event times with wall-clock times during shuffles/repartitioning.

**5. Handling Out-of-Order and Late Events**
*   The AI MUST explicitly ask the user for the business requirement regarding late events: Is latency or completeness more important?
*   The AI MUST implement one of three strict late-event handling policies:
    *   **Drop Event**: Discard the event completely if it misses the window.
    *   **Wait**: Delay the output of the window until a fixed amount of wall-clock/event time has passed (sacrifices latency for determinism).
    *   **Grace Period**: Output the window immediately, but maintain the window state for a set duration. If a late event arrives within the grace period, update the aggregation and emit a new output.
*   The AI MUST account for out-of-order events naturally generated by multiple producers, repartitioning, or temporary producer-to-broker network connection outages.

**6. Windowing Strategies**
*   The AI MUST select the appropriate windowing function based on business logic:
    *   Use **Tumbling Windows** for fixed, non-overlapping reporting (e.g., hourly sales).
    *   Use **Sliding Windows** for rolling computations (e.g., clicks in the past 60 minutes, updated every minute).
    *   Use **Session Windows** for user-activity grouping based on inactivity gaps.

**7. Reprocessing Historical Data**
*   When designing a reprocessing workflow, the AI MUST instruct the microservice to reset consumer offsets to the absolute beginning of the relevant streams.
*   The AI MUST warn the user to implement Quotas to prevent overwhelming the event broker with I/O during massive historical re-reads.
*   The AI MUST verify downstream consumer resilience to the massive surge of output events that a reprocessing run will generate.

@Workflow
1.  **Timestamp Configuration**: Define which timestamp (Event Time vs. Broker Ingestion Time) drives the topology. Implement the Timestamp Extractor.
2.  **Scheduler Initialization**: Configure the framework to schedule event consumption strictly by the oldest timestamp across all input partitions.
3.  **Time-Tracking Definition**: Define the time-tracking mechanism (Watermarks or Stream Time) based on the target framework. Ensure time boundaries are securely passed through shuffles/repartitions.
4.  **Windowing & Aggregation setup**: If the logic is time-sensitive, implement the explicit windowing strategy (Tumbling, Sliding, Session).
5.  **Late Event Policy Enforcement**: Define the specific threshold for lateness. Implement the Drop, Wait, or Grace Period logic.
6.  **Determinism Audit**: Scan the proposed topology for external database queries, external API calls, or wall-clock dependencies (`LocalTime.now()`). Refactor to remove these or heavily document the accepted nondeterminism risk.
7.  **Reprocessing Plan**: Generate the operational runbook for how this microservice will rebuild its state from offset 0, including broker quota configurations and downstream mitigation strategies.

@Examples (Do's and Don'ts)

**Principle: Event Scheduling across Partitions**

[DO] Rely on framework-level timestamp scheduling to ensure strict temporal interleaving.
```java
// DO: Use framework mechanisms that automatically interleave based on extracted Event Time.
// E.g., Kafka Streams automatically buffers and selects the next record with the lowest timestamp.
StreamsBuilder builder = new StreamsBuilder();
KStream<String, Event> streamA = builder.stream("TopicA", Consumed.with(TimestampExtractor.class));
KStream<String, Event> streamB = builder.stream("TopicB", Consumed.with(TimestampExtractor.class));
// The framework will inherently process TopicA and TopicB events in deterministic temporal order.
```

[DON'T] Manually poll multiple partitions in a round-robin loop without inspecting the timestamps.
```java
// DON'T: Round-robin polling destroys determinism if streams progress at different rates.
while(true) {
    Event a = consumerA.poll(); // Might be timestamp 10:05
    process(a);
    Event b = consumerB.poll(); // Might be timestamp 10:01 (Processed out of order!)
    process(b);
}
```

**Principle: Avoiding Nondeterminism (External Calls)**

[DO] Rely entirely on materialized state (internal or external state stores populated by events) for data lookups during stream processing.
```java
// DO: Join against an already materialized state store.
KTable<String, UserProfile> userProfiles = builder.table("user-profiles-stream");
KStream<String, Transaction> transactions = builder.stream("transactions-stream");

transactions.join(userProfiles, (txn, profile) -> {
    // Completely deterministic. Reprocessing will yield the exact same result.
    return enrichTransaction(txn, profile);
});
```

[DON'T] Make synchronous HTTP calls to an external REST API inside the processing loop.
```java
// DON'T: This ruins determinism. If the microservice is rewound to process data from 3 months ago, 
// the REST API will return today's state, corrupting the historical computation.
transactions.mapValues(txn -> {
    UserProfile profile = restClient.get("https://api.external.com/users/" + txn.getUserId());
    return enrichTransaction(txn, profile);
});
```

**Principle: Windowing and Late Event Grace Periods**

[DO] Explicitly define how long a window accepts late-arriving events before finalizing.
```java
// DO: Define a Tumbling Window with a strict Grace Period.
// Events arriving up to 1 hour late will update the window. Events later than 1 hour are explicitly dropped.
stream.groupByKey()
      .windowedBy(TimeWindows.of(Duration.ofMinutes(10)).grace(Duration.ofHours(1)))
      .aggregate(
          () -> 0L,
          (aggKey, newValue, aggValue) -> aggValue + newValue
      );
```

[DON'T] Assume unbounded streams are perfectly ordered and process time-series data without explicit windowing or lateness boundaries.
```java
// DON'T: Aggregating infinitely without windows or grace periods on unbounded streams 
// will lead to memory leaks and inability to handle delayed network events correctly.
stream.groupByKey().aggregate( /* infinite aggregation without temporal bounds */ );
```