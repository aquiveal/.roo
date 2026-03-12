@Domain
Trigger these rules when the user requests architecture design, code generation, refactoring, or code review related to microservice interactions, inter-process communication (IPC), API design, event-driven architectures, message brokers, or distributed system error handling.

@Vocabulary
- **Inter-Process Communication (IPC)**: Calls made across a network boundary between different operating system processes (microservices), as opposed to in-process method calls.
- **Information Hiding**: The practice of hiding internal implementation details and exposing only what is strictly necessary via external interfaces to decouple clients from server internals.
- **Synchronous Blocking**: A communication style where the caller sends a request and halts execution (blocks) while waiting for the receiver to process the request and return a response.
- **Asynchronous Nonblocking**: A communication style where the caller issues a call and immediately continues its own processing without waiting for the receiver.
- **Request-Response**: A collaboration style where a client asks a server to perform an action and expects a response detailing the outcome.
- **Event-Driven**: A collaboration style where a service broadcasts a fact (an event) about something that happened. The emitter does not know or care who consumes the event.
- **Event**: A factual statement about something that has occurred in the domain. The payload.
- **Message**: The medium or transport envelope used to send data (which could contain an event, a request, or a response) over an asynchronous communication mechanism.
- **Common Data Communication**: An asynchronous communication style where one service writes data to a shared location (e.g., data lake, filesystem) and others read it later.
- **Temporal Coupling**: A form of coupling where both the calling and receiving services must be up, available, and reachable at the exact same time for an operation to succeed.
- **Crash Failure**: A failure where a server/process suddenly halts and stops responding.
- **Omission Failure**: A failure where a request is sent but no response is received, or a downstream service stops emitting expected messages.
- **Timing Failure**: A failure where a response is received, but either too late to be useful or unexpectedly early.
- **Response Failure**: A failure where a response is received, but the data is malformed or incorrect.
- **Arbitrary (Byzantine) Failure**: A failure where the system goes wrong in inconsistent ways, and participants cannot agree on the state or cause.
- **Competing Consumers**: A pattern where multiple instances of a service read from the same queue to distribute processing load.
- **Message Hospital / Dead Letter Queue**: A storage location for messages that continually fail to process after a defined number of retries, allowing for manual inspection and replay.
- **Correlation ID**: A unique identifier attached to an initial request and propagated through all subsequent downstream calls and log entries to trace a single transaction across a distributed system.

@Objectives
- Treat network calls with extreme prejudice, optimizing for payload size, serialization overhead, and network unreliability.
- Choose communication styles (sync vs. async, request-response vs. event-driven) based on business requirements *before* selecting the underlying technology.
- Prevent cascading failures by eliminating long synchronous call chains and enforcing time-outs/circuit breakers.
- Enforce the inversion of responsibility using event-driven architectures to achieve maximum temporal decoupling.
- Standardize distributed error handling to gracefully manage transient network issues, timeouts, and omissions.

@Guidelines

**1. Inter-Process vs. In-Process Differentiation**
- The AI MUST NOT abstract inter-process network calls to look exactly like local method calls. The developer must always be aware that a network call is occurring.
- The AI MUST optimize data payloads for serialization/deserialization. Send the absolute minimum data required. Do not pass large, memory-heavy object graphs across network boundaries unless explicitly required.

**2. Technology Selection**
- The AI MUST select the communication style (e.g., Event-Driven, Sync Request-Response) FIRST. Technology (e.g., Kafka, gRPC, HTTP/REST) MUST be chosen SECOND, based on the selected style.
- The AI MUST NOT use message brokers (e.g., Kafka, RabbitMQ) for tight synchronous request-response needs unless async request-response is explicitly architected.

**3. Synchronous Blocking Constraints**
- The AI MUST NOT create long chains of synchronous blocking calls across multiple microservices.
- When generating synchronous communication code, the AI MUST implement time-outs for every network call.
- The AI MUST evaluate whether intermediate synchronous checks (e.g., Fraud Detection during Payment) can be moved to background asynchronous processes to reduce call chain length.

**4. Asynchronous & Event-Driven Constraints**
- When implementing asynchronous request-response, the AI MUST provide a mechanism to route the response back to the caller (e.g., a reply-to queue) and MUST persist state using Correlation IDs if the response is handled by a different instance.
- The AI MUST distinguish between a Command (telling a service what to do) and an Event (stating a fact). Events MUST be named in the past tense (e.g., `OrderPlaced`, NOT `PlaceOrder`).
- In event-driven collaboration, the AI MUST implement "Fully Detailed Events" (putting all safe, non-PII data required by consumers into the event payload) to prevent consumers from immediately calling back to the emitter to fetch missing data.
- If an event contains PII (Personally Identifiable Information) or excessively large payloads, the AI MUST explicitly raise this trade-off and suggest hybrid approaches (e.g., a lightweight event with a URI for secure data retrieval).

**5. Parallel Execution**
- When a microservice must aggregate data from multiple independent downstream services via request-response, the AI MUST execute these calls in parallel, not sequentially.

**6. Error Handling & Resiliency**
- The AI MUST implement HTTP status codes strictly according to semantics: 4xx for client/request errors (do not retry without modification), and 5xx for server errors (eligible for retry if transient).
- The AI MUST implement a defined Maximum Retry Limit for asynchronous message processing to prevent catastrophic failover loops (poison messages crashing multiple workers).
- The AI MUST output failed asynchronous messages to a Dead Letter Queue (Message Hospital) upon exceeding the retry limit.
- The AI MUST implement Correlation IDs across all generated logs and network request headers.

**7. Common Data Communication**
- When using common data stores (e.g., data lakes, shared filesystems) for communication, the AI MUST enforce unidirectional flow (one writer service, multiple reader services).
- The AI MUST NOT generate architectures where multiple microservices read and write to the same tables in a shared operational database.

**8. Async/Await Caution**
- When using `async/await` syntax in languages like JavaScript or C#, the AI MUST add comments clarifying that while the local thread is unblocked, the business flow is still operating in a synchronous, temporal-coupled manner relative to the downstream service.

@Workflow
When tasked with designing or implementing communication between microservices, the AI MUST follow this rigid algorithmic process:

1. **Analyze the Interaction Requirement**: Determine if the caller needs a response to continue its business logic. 
2. **Select the Style**:
   - If the operation is a long-running process (e.g., hours/days): Select *Asynchronous Request-Response* or *Event-Driven*.
   - If the caller needs immediate confirmation but can defer processing: Select *Event-Driven*.
   - If the operation requires a large batch of data without latency sensitivity: Select *Common Data Communication*.
   - If the caller absolutely requires an immediate data read from another service: Select *Synchronous Request-Response*.
3. **Evaluate Call Chains**: If selecting Synchronous Request-Response, analyze the upstream/downstream impact. If the call chain exceeds two hops, aggressively refactor to use parallel calls, caching, or background asynchronous processing.
4. **Define the Payload**:
   - For requests: Include only the minimum viable parameters.
   - For events: Include full context (Fully Detailed Events) to prevent callback barrages, stripping PII if necessary.
5. **Implement Resiliency**: Wrap the generated network calls in timeouts, configure a retry policy for omission/timing failures, and inject Correlation IDs into headers and logs.
6. **Implement Technology**: Generate the specific code (e.g., HTTP fetch, Kafka producer/consumer) matching the selected style and resiliency requirements.

@Examples (Do's and Don'ts)

**Principle: Parallelizing Independent Network Calls**

[DO]
```javascript
// The AI executes independent network calls in parallel to reduce overall latency.
async function fetchOrderDetails(orderId) {
    const correlationId = generateCorrelationId();
    
    // Fire all requests concurrently
    const [customerRes, shippingRes, inventoryRes] = await Promise.all([
        fetch(`http://customer-service/api/customers/${orderId}`, { headers: { 'X-Correlation-ID': correlationId } }),
        fetch(`http://shipping-service/api/shipping/${orderId}`, { headers: { 'X-Correlation-ID': correlationId } }),
        fetch(`http://inventory-service/api/inventory/${orderId}`, { headers: { 'X-Correlation-ID': correlationId } })
    ]);

    return {
        customer: await customerRes.json(),
        shipping: await shippingRes.json(),
        inventory: await inventoryRes.json()
    };
}
```

[DON'T]
```javascript
// The AI executes network calls sequentially, summing the latency of all three calls.
async function fetchOrderDetails(orderId) {
    // Awaiting each call blocks the next one
    const customerRes = await fetch(`http://customer-service/api/customers/${orderId}`);
    const customer = await customerRes.json();

    const shippingRes = await fetch(`http://shipping-service/api/shipping/${orderId}`);
    const shipping = await shippingRes.json();

    const inventoryRes = await fetch(`http://inventory-service/api/inventory/${orderId}`);
    const inventory = await inventoryRes.json();

    return { customer, shipping, inventory };
}
```

**Principle: Event Payload Design (Fully Detailed Events)**

[DO]
```json
// The AI generates an event with enough context so consumers do not need to make synchronous callbacks.
{
  "eventId": "evt-98765",
  "eventType": "CustomerRegistered",
  "correlationId": "txn-12345",
  "timestamp": "2023-10-12T10:00:00Z",
  "payload": {
    "customerId": "cust-555",
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "accountType": "Premium"
  }
}
```

[DON'T]
```json
// The AI generates an ID-only event, forcing every consumer to synchronously call the Customer service.
{
  "eventId": "evt-98765",
  "eventType": "CustomerRegistered",
  "payload": {
    "customerId": "cust-555"
  }
}
```

**Principle: Handling Asynchronous Retries and Poison Messages**

[DO]
```python
# The AI implements a maximum retry limit and routes failures to a Dead Letter Queue.
MAX_RETRIES = 3

def process_message(message):
    try:
        handle_event(message.payload)
        message.ack()
    except Exception as e:
        if message.delivery_count >= MAX_RETRIES:
            log.error(f"Message {message.id} failed {MAX_RETRIES} times. Moving to DLQ.", correlation_id=message.correlation_id)
            dead_letter_queue.publish(message)
            message.ack() # Remove from main queue to prevent catastrophic failover loops
        else:
            log.warning(f"Transient error processing {message.id}. Retrying.", correlation_id=message.correlation_id)
            message.nack() # Return to queue for retry
```

[DON'T]
```python
# The AI infinitely nacks the message on failure, crashing every worker that picks it up.
def process_message(message):
    try:
        handle_event(message.payload)
        message.ack()
    except Exception as e:
        message.nack() # Will be picked up again immediately, potentially forever
```