@Domain
Trigger these rules when the user requests assistance with designing, implementing, or debugging event-driven microservices, Kafka producers and consumers, stateful stream processing, or data consistency mechanisms using Apache Kafka or Kafka Streams. This applies specifically to tasks involving deduplication, atomic multi-topic writes, exactly-once processing, and managing distributed application state backed by Kafka topics.

@Vocabulary
- **Exactly-Once Processing**: A guarantee that an event will be processed and its results published exactly one time, despite network glitches, service failures, or retries.
- **Idempotence**: The property of a system to produce the same result regardless of how many times a message is sent or processed. In Kafka, this relies on a producer identifier and a sequence number to discard duplicates at the broker level.
- **Atomic Commit**: Layered on top of idempotence, this ensures that a group of messages sent to multiple topics (including the `consumer_offsets` topic and state store changelogs) succeed or fail as a single, indivisible unit.
- **Transaction Coordinator**: A Kafka cluster component that orchestrates the two-phase commit process, managing the transaction log and acting as the ultimate arbiter for marking a transaction as committed or aborted.
- **Marker Messages**: Invisible control messages (Begin, Commit, Abort) sent through streams to instruct consumers to buffer and release only successfully committed data.
- **State Store**: A disk-resident hash table held inside the Kafka Streams API and backed by a Kafka topic, allowing state to be tied atomically to messaging within a transaction.
- **End-to-End Principle**: The traditional network concept of managing deduplication at the final destination (e.g., a database), which Kafka transactions aim to replace by moving deduplication into the infrastructure layer.

@Objectives
- Abstract the complexities of distributed system failures (duplicates, retries, and partial writes) out of the application code and into the Kafka infrastructure.
- Ensure that Kafka consumers and producers operating in a "read-process-write" loop never process duplicates or output partial results.
- Atomically bind the saving of internal service state (state stores) with the emission of output events.
- Eliminate the need for manual, application-level deduplication tracking or complex event identity generation for intermediary streams.
- Ensure the AI understands the strict boundary of Kafka transactions (they do NOT cover external HTTP calls, stdout, or external databases).

@Guidelines
- **Transaction Scoping**: When the AI implements a "read-process-write" cycle strictly within Kafka, it MUST wrap the output event generation and the consumer offset commit in a single Kafka transaction.
- **Kafka Streams Optimization**: When generating Kafka Streams applications, the AI MUST NOT write manual transaction handling code. Instead, the AI MUST simply enable the exactly-once processing configuration natively provided by the Kafka Streams API.
- **Offset Management**: When writing manual consumer/producer transactional code, the AI MUST explicitly use `producer.sendOffsetsToTransaction(offsets)` to commit the consumer's read position. The AI MUST NOT let the consumer auto-commit offsets when using transactions.
- **State Store Atomicity**: When an application requires managing internal state (e.g., keeping a running balance) alongside emitting events, the AI MUST use a Kafka Streams State Store to ensure that the state update and the event emission are bound in the exact same transaction.
- **Deduplication Delegation**: The AI MUST NOT generate custom databases, manual deduplication caches, or complex identity mapping schemes solely for tracking duplicate events if the workflow is entirely Kafka-in and Kafka-out. Rely completely on Kafka transactions.
- **External System Boundaries**: If a service involves writing to an external database or making an external HTTP/REST call, the AI MUST explicitly warn the user that Kafka transactions do not cover these external systems. The AI MUST NOT assume or imply that a Kafka transaction abort will rollback an external HTTP call.
- **Saga Pattern Consideration**: If cross-service or multi-technology transactionality is required, the AI MUST suggest the Saga pattern, explicitly noting that Kafka transactions cannot be rolled back based on downstream service failures once committed.
- **Consumer Read Guarantees**: The AI MUST correctly design downstream consumers recognizing that transactions do not guarantee *when* an arbitrary consumer will read messages, only that they will be read atomically and exactly once.

@Workflow
1. **Analyze the Topology**: Determine if the requested service workflow is entirely internal to the Kafka ecosystem (Kafka-in, State-Store-process, Kafka-out) or if it touches external APIs/Databases.
2. **Select the Abstraction**:
   - If using Kafka Streams, inject the configuration to enable exactly-once processing. Skip to step 5.
   - If using the raw Producer/Consumer API, proceed to step 3.
3. **Initialize the Transaction**: Instruct the producer to `beginTransaction()` before processing any polled records.
4. **Execute the Atomic Block**:
   - Perform the business logic on the polled records.
   - Send the resulting messages to their respective output topics via the producer.
   - Extract the current offsets from the consumer.
   - Send the offsets to the transaction using `producer.sendOffsetsToTransaction()`.
   - Call `producer.endTransaction()`.
5. **Enforce Boundaries**: Review the business logic for side-effects (e.g., REST calls). If found, isolate them and implement compensation logic, explicitly noting that Kafka transactions will not protect these boundaries.
6. **Refactor Deduplication**: Remove any legacy code or requested logic that attempts to manually deduplicate incoming messages or manually generate synthetic keys specifically for downstream deduplication.

@Examples (Do's and Don'ts)

[DO] Use Kafka Streams exactly-once configuration to implicitly handle all transactions, deduplication, and atomic state store updates.
```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "order-validation-service");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
// Enable exactly-once processing to automatically wrap state and events in transactions
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE_V2);

KafkaStreams streams = new KafkaStreams(topology, props);
streams.start();
```

[DO] Bind consumer offset commits and producer sends into a single atomic transaction when using the raw clients.
```java
// Disable consumer auto-commit
consumerProps.put("enable.auto.commit", "false");
consumerProps.put("isolation.level", "read_committed");

// Initialize producer transactions
producer.initTransactions();

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    if (!records.isEmpty()) {
        producer.beginTransaction();
        try {
            // Process and send outputs
            for (ConsumerRecord<String, String> record : records) {
                String validatedDeposit = validate(record.value());
                producer.send(new ProducerRecord<>("validated-deposits", record.key(), validatedDeposit));
            }
            
            // Atomically commit offsets
            Map<TopicPartition, OffsetAndMetadata> offsets = getOffsets(records);
            producer.sendOffsetsToTransaction(offsets, consumer.groupMetadata());
            
            producer.commitTransaction();
        } catch (Exception e) {
            producer.abortTransaction();
        }
    }
}
```

[DON'T] Implement application-level caching or database tracking for deduplication within a Kafka-to-Kafka workflow.
```java
// ANTI-PATTERN: Manual deduplication leaking into application logic
Set<String> processedMessageIds = new HashSet<>(); // OR an external DB call

for (ConsumerRecord<String, String> record : records) {
    if (processedMessageIds.contains(record.key())) {
        continue; // Unnecessary and brittle. Use Kafka transactions instead.
    }
    processAndSend(record);
    processedMessageIds.add(record.key());
}
```

[DON'T] Assume Kafka transactions will rollback external system state.
```java
// ANTI-PATTERN: Mixing external side-effects inside a Kafka transaction
producer.beginTransaction();
try {
    producer.send(new ProducerRecord<>("OrderValidated", order));
    
    // Danger: If this HTTP call succeeds, but the Kafka transaction fails later, 
    // the HTTP call CANNOT be rolled back by Kafka.
    httpClient.post("https://external-shipping-provider.com/ship", order); 
    
    producer.sendOffsetsToTransaction(offsets, consumerGroup);
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction(); // Will not undo the HTTP POST
}
```