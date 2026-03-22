# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, implementing, refactoring, evaluating, or documenting Interprocess Communication (IPC), APIs, message brokers, service discovery, or data replication mechanisms within a Microservice Architecture. This includes work on REST endpoints, gRPC interfaces, asynchronous messaging (publish/subscribe, point-to-point), and database/message transaction synchronization.

# @Vocabulary
- **Interprocess Communication (IPC)**: The mechanism by which services in a distributed system communicate.
- **Synchronous Interaction**: A communication style where the client expects a timely response and may block while waiting (e.g., HTTP, gRPC).
- **Asynchronous Interaction**: A communication style where the client does not block, and responses (if any) are not necessarily immediate (e.g., AMQP, STOMP).
- **One-to-One Interaction**: Each client request is processed by exactly one service instance.
- **One-to-Many Interaction**: Each client request is processed by multiple services.
- **IDL (Interface Definition Language)**: A language used to specify APIs (e.g., OpenAPI for REST, Protocol Buffers for gRPC).
- **API-First Design**: The practice of writing the interface definition and reviewing it with clients BEFORE implementing the service.
- **Semantic Versioning (SemVer)**: A versioning scheme structured as MAJOR.MINOR.PATCH.
- **Robustness Principle**: "Be conservative in what you do, be liberal in what you accept from others." Ensures backward compatibility in API evolution.
- **Remote Procedure Invocation (RPI)**: Synchronous IPC where a client invokes a service (e.g., REST, gRPC).
- **Richardson Maturity Model**: A maturity model for REST APIs consisting of Level 0 (single URI/POST), Level 1 (resources), Level 2 (HTTP verbs), and Level 3 (HATEOAS).
- **Circuit Breaker Pattern**: An RPI proxy that tracks successful and failed requests, immediately rejecting invocations for a timeout period if the error rate exceeds a threshold.
- **Service Registry**: A database containing the network locations of an application's service instances.
- **Self Registration**: Application-level discovery where a service instance registers itself with the registry.
- **Client-Side Discovery**: Application-level discovery where the client queries the registry and load balances.
- **3rd Party Registration**: Platform-provided discovery where the deployment platform (e.g., Kubernetes) registers the service.
- **Server-Side Discovery**: Platform-provided discovery where the client requests a router/DNS that load balances across instances.
- **Message Broker**: An intermediary infrastructure service that buffers and routes asynchronous messages.
- **Point-to-Point Channel**: A message channel that delivers a message to exactly one consumer.
- **Publish-Subscribe Channel**: A message channel that delivers a message to all attached consumers.
- **Sharded (Partitioned) Channel**: A channel divided into shards to allow concurrent consumption while preserving message ordering via a Shard Key.
- **Transactional Outbox Pattern**: A pattern that guarantees atomic database updates and message publishing by inserting messages into a temporary database table (the outbox) as part of the local ACID transaction.
- **Polling Publisher**: A message relay mechanism that repeatedly queries the outbox table for new messages to publish.
- **Transaction Log Tailing**: A highly performant message relay mechanism that reads the database's transaction/commit log (e.g., MySQL binlog) to publish messages.
- **Self-Contained Service**: A service that handles synchronous requests without communicating synchronously with other services (often using CQRS/replicated data or delayed processing).

# @Objectives
- Ensure all services are loosely coupled and independently deployable.
- Maximize system availability by preferring asynchronous messaging over synchronous communication.
- Prevent cascading failures in synchronous interactions by implementing strict timeouts, request limits, and circuit breakers.
- Guarantee reliable and ordered message delivery and processing.
- Maintain atomic consistency between local database updates and outgoing message publishing without relying on distributed (2PC/XA) transactions.
- Future-proof services by defining explicit, versioned, cross-language API contracts before writing implementation code.

# @Guidelines

### 1. API Design & Evolution
- The AI MUST apply API-first design. Generate or update IDL definitions (e.g., OpenAPI, Protocol Buffers) before generating implementation code.
- The AI MUST use cross-language message formats. NEVER use language-specific serialization (e.g., Java serialization). Use JSON/XML for text or Protocol Buffers/Avro for binary.
- The AI MUST manage API evolution using Semantic Versioning.
- The AI MUST implement the Robustness Principle for message parsing. Services must provide defaults for missing optional attributes and ignore unrecognized attributes to support backward-compatible (MINOR) changes.
- For major (breaking) API changes, the AI MUST embed the major version number in the URL (e.g., `/v1/`, `/v2/`) or use HTTP content negotiation via the MIME type.

### 2. Synchronous Communication (RPI, REST, gRPC)
- When implementing REST APIs, the AI MUST target Richardson Maturity Model Level 2 (using proper HTTP verbs like GET, POST, PUT, DELETE) or Level 3 (HATEOAS).
- If an API requires multiple complex update operations that map poorly to HTTP PUT, the AI MUST consider utilizing gRPC or defining clear sub-resources.
- When an RPI invokes a remote service, the AI MUST implement the Circuit Breaker Pattern (e.g., using Resilience4j, Hystrix, or Polly).
- The AI MUST explicitly set Network Timeouts for every synchronous external call.
- The AI MUST configure an upper bound/limit on the number of outstanding requests to a specific remote service.
- The AI MUST define fallback behavior (e.g., returning cached data, default values, or immediate errors) when a Circuit Breaker is open.

### 3. Service Discovery
- The AI MUST default to Platform-Provided Service Discovery (3rd Party Registration + Server-Side Discovery via Docker/Kubernetes) unless explicitly instructed that the application spans multiple deployment platforms.
- The AI MUST NEVER hardcode network IP addresses or ports in client code.

### 4. Asynchronous Messaging
- The AI MUST use Point-to-Point channels for Command messages and Asynchronous Request/Response (utilizing a `reply channel` header and `correlation id`).
- The AI MUST use Publish-Subscribe channels for Domain Event notifications.
- When scaling message consumers, the AI MUST preserve message ordering by configuring Sharded Channels and routing related messages using a consistent Shard Key (e.g., `orderId`).

### 5. Idempotency and Duplicate Messages
- The AI MUST assume the message broker guarantees "at-least-once" delivery, meaning duplicate messages will occur.
- The AI MUST make all message handlers idempotent.
- If the business logic cannot be inherently idempotent, the AI MUST implement a duplicate detection mechanism (e.g., tracking the `messageId` in a `PROCESSED_MESSAGES` SQL table or embedding the `messageId` into NoSQL records updated by the event).

### 6. Transactional Messaging
- The AI MUST NEVER use Distributed Transactions (2PC/XA) to synchronize database updates and message broker publishes.
- The AI MUST implement the Transactional Outbox Pattern for any operation that updates a database and publishes a message.
- The AI MUST insert the business entity and the outgoing message into the database within the SAME local ACID transaction.
- The AI MUST configure a separate mechanism (Polling Publisher or Transaction Log Tailing) to read the outbox and forward messages to the broker.

### 7. Maximizing Availability
- The AI MUST minimize the use of synchronous inter-service communication during client request processing.
- The AI MUST resolve synchronous data dependencies by either:
  1. Replicating necessary data locally via CQRS (subscribing to events from other services).
  2. Modifying the workflow to return an immediate response to the client (e.g., `PENDING` state) and completing the validation asynchronously using message exchanges.

# @Workflow
When tasked with designing or implementing IPC for a microservice, the AI MUST execute the following algorithm rigidly:

1. **Analyze the Interaction Requirement:**
   - Determine if the interaction is 1-to-1 or 1-to-N.
   - Evaluate if the client absolutely requires a synchronous response. If not, default to Asynchronous Messaging.

2. **Define the Interface (API-First):**
   - For REST: Create/update OpenAPI specifications.
   - For gRPC: Create/update `.proto` files.
   - For Messaging: Define the channel names, message headers (e.g., `reply-channel`, `correlation-id`), and payload schemas (JSON Schema or Protobuf).

3. **Implement Communication Adapters:**
   - **If Synchronous (RPI):**
     - Generate HTTP/gRPC clients.
     - Wrap the client execution in a Circuit Breaker.
     - Implement network timeouts.
     - Define the fallback logic (e.g., return empty/cache on failure).
   - **If Asynchronous (Messaging):**
     - Determine the Shard Key for the messages to ensure ordered processing.
     - Implement the Message Producer.

4. **Implement Transactional Guarantees:**
   - If the service modifies local data AND emits a message, implement the Transactional Outbox.
   - Wrap the business logic and the outbox insertion in a local database transaction.

5. **Implement Consumer Idempotency:**
   - In the message consumer code, extract the `messageId`.
   - Write logic to check the `messageId` against a `PROCESSED_MESSAGES` store.
   - If duplicate, discard. If new, process and record the `messageId` in the same local transaction.

6. **Audit for Availability:**
   - Review the request path. Does it depend on an external service being "up" to return a 200 OK to the client?
   - If yes, refactor to replicate data locally or switch to an asynchronous "finish processing later" model.

# @Examples (Do's and Don'ts)

### API Evolution
- **[DO]** Add optional attributes to a JSON request payload to maintain backward compatibility (MINOR change).
- **[DON'T]** Rename an existing field or change its data type without bumping the MAJOR version in the API URI.

### Handling Partial Failure (Synchronous RPI)
- **[DO]**
```java
// Using resilience4j for Circuit Breaker and Timeout
@CircuitBreaker(name = "orderService", fallbackMethod = "fallbackOrderDetails")
@TimeLimiter(name = "orderService")
public CompletableFuture<OrderDetails> getOrderDetails(String orderId) {
    return CompletableFuture.supplyAsync(() -> restTemplate.getForObject("http://order-service/orders/" + orderId, OrderDetails.class));
}

public CompletableFuture<OrderDetails> fallbackOrderDetails(String orderId, Throwable t) {
    return CompletableFuture.completedFuture(new OrderDetails(orderId, "STATUS_UNAVAILABLE")); // Fallback
}
```
- **[DON'T]** Block a thread indefinitely waiting for a downstream service without a timeout or circuit breaker.
```java
// ANTI-PATTERN
public OrderDetails getOrderDetails(String orderId) {
    // No timeout, no circuit breaker. If order-service hangs, this service hangs.
    return restTemplate.getForObject("http://order-service/orders/" + orderId, OrderDetails.class);
}
```

### Transactional Messaging (Outbox Pattern)
- **[DO]**
```java
@Transactional
public Order createOrder(OrderDetails details) {
    // 1. Save business entity
    Order order = new Order(details);
    orderRepository.save(order);
    
    // 2. Save event to Outbox table in the SAME transaction
    OrderCreatedEvent event = new OrderCreatedEvent(order.getId(), details);
    outboxRepository.save(new OutboxMessage(event.getType(), mapper.toJson(event)));
    
    return order;
}
```
- **[DON'T]** Use a distributed transaction OR publish the message sequentially without an outbox, risking dual-write inconsistencies.
```java
// ANTI-PATTERN
@Transactional
public Order createOrder(OrderDetails details) {
    Order order = new Order(details);
    orderRepository.save(order);
    
    // If the database commits but the message broker is down, the system is permanently inconsistent!
    messageBroker.send("order-channel", new OrderCreatedEvent(order)); 
    return order;
}
```

### Idempotent Message Consumer
- **[DO]**
```java
@Transactional
public void handleOrderCreated(Message message) {
    String messageId = message.getId();
    
    // Check for duplicate
    if (processedMessageRepository.existsById(messageId)) {
        return; // Discard duplicate
    }
    
    // Process business logic
    kitchenService.createTicket(message.getPayload());
    
    // Record message as processed in the SAME transaction
    processedMessageRepository.save(new ProcessedMessage(messageId));
}
```
- **[DON'T]** Assume messages are only delivered once.
```java
// ANTI-PATTERN
public void handleOrderCreated(Message message) {
    // A network blip causes the broker to redeliver this message. 
    // Kitchen creates two tickets for the same order!
    kitchenService.createTicket(message.getPayload());
}
```

### Asynchronous Request/Response
- **[DO]** Include a `reply-channel` and `correlation-id` in the command message headers.
```java
Message command = MessageBuilder.withPayload(new CreateTicketCommand())
    .setHeader("reply-channel", "orderServiceReplyChannel")
    .setHeader("correlation-id", UUID.randomUUID().toString())
    .build();
messageBroker.send("kitchenServiceChannel", command);
```
- **[DON'T]** Hardcode reply destinations or attempt to map async responses without unique correlation IDs.