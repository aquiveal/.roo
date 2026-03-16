# @Domain
These rules MUST trigger when the AI is tasked with designing, analyzing, refactoring, or implementing distributed systems, microservices, event-driven architectures, or data pipelines, specifically those involving message brokers (e.g., Apache Kafka), stream processing frameworks (e.g., Kafka Streams, KSQL), data enrichments, or asynchronous service integrations.

# @Vocabulary
- **Dataflow Programming:** A paradigm where execution is driven by the availability of data inputs (analogous to Unix pipes like `sed` or `awk`), removing hidden state and processing messages continuously.
- **Functional Core, Imperative Shell:** An architectural pattern where the central business logic operates as pure, side-effect-free asynchronous functions (the core), wrapped by code that handles marshaling to/from outward-facing synchronous request-response interfaces like REST or RPC (the shell).
- **Event-Driven Approach:** Processing a single input event stream one message at a time. In this model, enrichments are typically performed via inline remote lookups (e.g., querying an external database or REST API).
- **Pure (Stateless) Streaming Approach:** Blending or joining two or more dynamic event streams together by buffering them locally until matching conditions are met (e.g., a Stream-Stream join), eliminating the need for remote database lookups.
- **Stateful Streaming Approach:** Recasting event streams into local tables and internalizing all necessary data. Whole reference datasets are preloaded into local state stores (disk-resident hash tables), allowing zero-network-latency enrichments.
- **State Store:** A local, disk-resident database/hash table held inside the stream processing API (e.g., Kafka Streams) that acts as an advanced, continually updated cache.
- **Standby Replicas:** Backup state stores kept continually up to date on secondary streaming nodes to ensure instant failover without the need to reload state from the broker.
- **Disk Checkpoints:** Periodic local disk saves of a streaming application's state, allowing it to resume operations quickly after a restart by only fetching missed messages from the event log.
- **Compacted Topics:** Kafka topics that retain only the most recent event for a specific key, drastically reducing the dataset size and minimizing the load time required to rebuild a state store.

# @Objectives
- The AI MUST transition system designs away from imperative, synchronous remote lookups toward dataflow and functional programming styles.
- The AI MUST prioritize data locality by internalizing state inside the stream processing application, treating stateful streaming as an advanced form of caching.
- The AI MUST eliminate temporal coupling and race conditions (e.g., out-of-order event arrivals) by utilizing stream buffering and stream-stream joins instead of application-level polling or blocking.
- The AI MUST mitigate the startup/initialization costs of stateful streaming applications by explicitly enforcing the use of standby replicas, disk checkpoints, and compacted topics.

# @Guidelines

## Architectural Paradigms
- When designing distributed systems that interact with external procedural boundaries (like GUIs or REST clients), the AI MUST apply the **"Functional Core, Imperative Shell"** pattern. Asynchronous event processing must be isolated from synchronous I/O marshaling.
- When an application requires data from multiple sources to perform an action, the AI MUST NOT default to the **Event-Driven Approach** (single stream + external DB lookup) unless explicitly required, as it introduces network latency and ordering vulnerabilities.

## Handling Race Conditions and Asynchronicity
- When encountering two related events that may arrive out of order (e.g., an Order and a Payment), the AI MUST use the **Pure (Stateless) Streaming Approach**. It MUST design a buffering mechanism (Stream-Stream join) that waits for both events to arrive locally rather than failing, skipping, or implementing manual blocking/polling loops.

## Internalizing State for Enrichments
- When a service requires reference data for enrichments (e.g., looking up a customer's email address), the AI MUST enforce the **Stateful Streaming Approach**. The AI MUST design the system to preload the entire reference event stream into a local Table (State Store) inside the stream processing API.
- The AI MUST explicitly state that interacting with this local state store replaces the network call to the external database.

## Managing the Practicalities of State
- When defining a stateful streaming architecture, the AI MUST explicitly define the mechanisms used to handle the penalty of state initialization.
- The AI MUST specify the use of **Standby Replicas** to ensure high availability and rapid failover.
- The AI MUST specify the use of **Disk Checkpoints** so that restarting nodes only need to read the delta of missed messages from the log.
- The AI MUST specify that underlying reference data topics acting as tables MUST be configured as **Compacted Topics** to prevent infinite growth and ensure rapid state rebuilding.

## General Streaming Rules
- The AI MUST map application types strictly to their definitions:
  - If processing 1 input stream -> Event-Driven Application.
  - If blending >= 1 input streams into >= 1 output streams -> Streaming Application.
  - If recasting streams to tables and storing intermediary state in the log -> Stateful Streaming Application.

# @Workflow
When tasked with designing or refactoring an event processing service, the AI MUST execute the following algorithmic process:

1. **Analyze Inputs and Dependencies:** Identify the primary trigger event (e.g., "Order Created") and all secondary data dependencies required to process the event (e.g., "Payment Status", "Customer Email").
2. **Select Processing Strategy:**
   - If no secondary data is needed: Output a simple Stateless Event-Driven design.
   - If secondary data is dynamic and temporal (e.g., waiting for another transaction): Output a Pure Streaming design using buffered Stream-Stream joins.
   - If secondary data is reference/historical (e.g., Customer Profiles): Output a Stateful Streaming design using Stream-Table joins.
3. **Design the Join/Buffer Mechanism:** Define the exact keys used to join the streams/tables. Ensure the design accounts for events arriving out of order.
4. **Define Local State Stores (If Stateful):** Detail the creation of local tables (e.g., KTable) derived from Kafka topics to eliminate remote network calls.
5. **Apply Practicality/Resilience Constraints:** Document the explicit use of compacted topics for the reference data, and enforce standby replicas and disk checkpoints in the application configuration.
6. **Wrap in Imperative Shell (If needed):** If the system must expose a REST/RPC endpoint, define the imperative shell that translates the synchronous request into an asynchronous event emission and vice versa.

# @Examples (Do's and Don'ts)

## Stream Enrichment (Lookups)
- **[DO]:** Preload reference data into a local state store for zero-latency enrichment.
  ```java
  // Correct: Stateful Streaming Approach
  KTable<String, Customer> customers = builder.table("customers-compacted-topic");
  KStream<String, Order> orders = builder.stream("orders-topic");
  
  orders.join(customers, (order, customer) -> new EnrichedOrder(order, customer))
        .to("enriched-orders-topic");
  ```
- **[DON'T]:** Perform a blocking network call to an external database for every message in a high-throughput event stream.
  ```java
  // Incorrect: Event-Driven Approach with remote lookup
  ordersTopic.subscribe(order -> {
      Customer customer = restClient.get("/customers/" + order.getCustomerId()); // Anti-pattern
      process(order, customer);
  });
  ```

## Handling Temporal Ordering (Race Conditions)
- **[DO]:** Buffer streams locally to handle out-of-order events using a Stream-Stream join.
  ```java
  // Correct: Pure Streaming Approach
  KStream<String, Order> orders = builder.stream("orders");
  KStream<String, Payment> payments = builder.stream("payments");
  
  // Buffers events until both arrive within the specified window
  orders.join(payments, 
      (order, payment) -> new ConfirmedOrder(order, payment), 
      JoinWindows.of(Duration.ofMinutes(5)))
      .to("confirmed-orders");
  ```
- **[DON'T]:** Rely on manual polling or skipping processing if a related event hasn't arrived in an external database yet.
  ```java
  // Incorrect: Fails or blocks if the payment arrives slower than the order
  public void processOrder(Order order) {
      Payment payment = db.getPaymentForOrder(order.getId());
      if (payment == null) {
          throw new RuntimeException("Payment not found yet!"); // Anti-pattern
      }
      sendEmail(order, payment);
  }
  ```

## Configuring Stateful Topics
- **[DO]:** Use compacted topics to back state stores, ensuring the dataset only contains the latest version of each key.
  ```bash
  # Correct: Reference topics used for Tables are compacted
  kafka-topics --create --topic customer-reference --config cleanup.policy=compact
  ```
- **[DON'T]:** Use standard retention-based topics for state store initialization, forcing the application to replay the entire historical change log of every entity on startup.