@Domain
This rule file MUST be triggered when the AI is tasked with designing, implementing, refactoring, or reviewing communication between microservices, defining APIs, selecting integration technologies (e.g., HTTP, gRPC, Message Brokers), handling distributed system errors, defining event schemas, or optimizing inter-process network calls.

@Vocabulary
- **In-Process Call**: A method call within a single process boundary; inherently fast, utilizing memory pointers, with deterministic errors.
- **Inter-Process Call**: A call across a network between separate processes; involves serialization/deserialization overhead, network latency, and unpredictable failure modes.
- **Crash Failure**: A failure mode where a server crashes and requires a reboot.
- **Omission Failure**: A failure mode where a message is sent but no response is received, or a downstream service stops firing expected messages.
- **Timing Failure**: A failure mode where an action happens too late or too early.
- **Response Failure**: A failure mode where a response is received, but the data is incorrect or malformed.
- **Arbitrary/Byzantine Failure**: A failure mode where something goes wrong, but participants cannot agree on whether the failure occurred or why.
- **Synchronous Blocking**: A communication style where a microservice makes a call to a downstream process and halts its own execution thread waiting for a response.
- **Asynchronous Nonblocking**: A communication style where the emitting microservice sends a call and immediately continues its processing regardless of whether the call is received or responded to.
- **Request-Response**: A collaboration style where a service asks another service to do something and expects a response detailing the result.
- **Event-Driven**: A collaboration style where a service broadcasts a factual statement about something that has happened (an event) to anonymous consumers without expecting a specific response.
- **Common Data**: A communication style where microservices collaborate via a shared data source (e.g., a file drop or shared database).
- **Temporal Coupling**: A form of tight coupling where both the calling and receiving microservices must be up and available at the exact same time for an operation to succeed.
- **Message**: The transport medium used over an asynchronous communication mechanism (like a broker).
- **Event**: The factual payload contained within a message.
- **Competing Consumer Pattern**: A pattern where multiple worker instances of the same service pull from a single queue to distribute load.
- **Message Hospital / Dead Letter Queue**: A storage location for messages that continually fail processing, preventing them from infinitely crashing workers.
- **Catastrophic Failover**: A scenario where a malformed message repeatedly crashes competing consumers, eventually taking down the entire worker pool.

@Objectives
- Choose the communication style (sync vs. async, request-response vs. event-driven) BEFORE selecting the specific underlying technology.
- Prevent temporal coupling and cascading failures by avoiding long, synchronous blocking call chains.
- Explicitly acknowledge the reality of the network: account for serialization overhead, latency, and transient failures.
- Favor loose coupling through the use of event-driven architectures and inverted responsibilities where appropriate.
- Ensure all downstream components retain their autonomy to reject invalid requests.
- Protect worker pools from infinite retry loops caused by poison-pill messages.

@Guidelines

- **Network Transparency**: The AI MUST NOT hide the fact that a network call is taking place behind overly opaque abstractions. Remote calls MUST be visually distinct from local calls in the code to ensure developers remain aware of latency and serialization costs.
- **Rich Error Semantics**: The AI MUST implement distinct error handling for distributed failures. The AI MUST differentiate between client-caused request errors (e.g., HTTP 400 series - do not retry) and transient downstream errors (e.g., HTTP 500 series - safe to retry).
- **Style Over Technology**: When asked to implement microservice communication, the AI MUST explicitly define the collaboration style (Request-Response, Event-Driven, or Common Data) and the synchronicity (Sync Blocking vs. Async Nonblocking) BEFORE writing code for a specific technology (e.g., Kafka, REST, gRPC).
- **Mitigating Synchronous Chains**: If designing a Synchronous Blocking flow, the AI MUST identify the length of the call chain. If the chain requires more than two downstream hops, the AI MUST attempt to refactor the architecture by moving non-critical path operations (e.g., fraud detection, notifications) to background asynchronous processes.
- **Parallelizing Independent Calls**: When a service must make multiple synchronous requests to different downstream services, and those requests do not depend on each other, the AI MUST execute these calls in parallel rather than sequentially.
- **Async/Await Traps**: The AI MUST NOT blindly use `await` on asynchronous network calls if multiple independent calls are being made. The AI MUST aggregate promises/futures and resolve them concurrently to prevent artificial blocking.
- **Requests, Not Commands**: The AI MUST treat all directed communication as a "Request" rather than a "Command". The code MUST reflect the downstream service's autonomy to reject the request based on its own internal state machine.
- **Event Payload Design (Fully Detailed Events)**: When designing an event payload, the AI MUST include all state data that would reasonably be requested via a follow-up API call (e.g., include Customer Name and Email, not just Customer ID). This prevents "callback storms" to the emitting service.
  - *Constraint*: Exclude Highly Sensitive/PII data from broad event broadcasts unless explicitly authorized by the security model, or implement a dual-event pattern (one public, one secured).
  - *Constraint*: Respect the message size limits of the chosen broker (e.g., Kafka's default 1MB).
- **Dumb Pipes, Smart Endpoints**: The AI MUST NOT place business logic, routing intelligence, or complex message transformation inside the middleware (message broker). The broker MUST only handle routing and delivery.
- **Message Hospitals / Poison Pill Prevention**: When implementing asynchronous queue consumers, the AI MUST configure a maximum retry limit for message processing. Upon hitting the limit, the code MUST route the failing message to a Dead Letter Queue (Message Hospital) to prevent Catastrophic Failover.

@Workflow
1. **Analyze the Communication Requirement**: Identify the upstream caller, the downstream receiver, the goal of the interaction, and the tolerance for latency.
2. **Select the Collaboration Style**: 
   - Choose *Event-Driven* if the emitting service does not need to know what happens next or who is listening.
   - Choose *Request-Response* if the calling service needs a definitive result to continue its business logic.
   - Choose *Common Data* if passing massive data volumes or interoperating with legacy batch systems.
3. **Determine Synchronicity**: 
   - Choose *Asynchronous Nonblocking* for long-running processes or to eliminate temporal coupling.
   - Choose *Synchronous Blocking* only for fast, critical-path data retrieval where temporal coupling is acceptable.
4. **Architect the Payload**: If Event-Driven, design a "Fully Detailed Event" containing all necessary context to prevent downstream services from querying the emitter.
5. **Implement Failure Handling**: Implement timeouts, bounded retries, and dead letter queues for all network boundaries.

@Examples (Do's and Don'ts)

**Principle: Event Payload Design (Fully Detailed Events vs. Just an ID)**

[DON'T]
```json
// Anti-pattern: Downstream services receiving this event must immediately make a synchronous API call back to the Customer service to get the email address to send a welcome email.
{
  "eventType": "CustomerCreated",
  "customerId": "12345"
}
```

[DO]
```json
// Correct: The event contains all non-sensitive data required for downstream services (like Notifications) to act without calling back to the emitter.
{
  "eventType": "CustomerCreated",
  "customer": {
    "id": "12345",
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
  }
}
```

**Principle: Parallel vs Sequential Synchronous Calls**

[DON'T]
```javascript
// Anti-pattern: Sequential blocking. The total latency is the sum of all three network calls.
async function getComparisonPrices(itemId) {
  const vendorA = await fetchPriceFromVendorA(itemId); // Takes 1s
  const vendorB = await fetchPriceFromVendorB(itemId); // Takes 1s
  const vendorC = await fetchPriceFromVendorC(itemId); // Takes 1s
  // Total time: 3 seconds
  return findBestPrice([vendorA, vendorB, vendorC]);
}
```

[DO]
```javascript
// Correct: Parallel execution. The total latency is equal to the single slowest network call.
async function getComparisonPrices(itemId) {
  const [vendorA, vendorB, vendorC] = await Promise.all([
    fetchPriceFromVendorA(itemId), // Takes 1s
    fetchPriceFromVendorB(itemId), // Takes 1s
    fetchPriceFromVendorC(itemId)  // Takes 1s
  ]);
  // Total time: 1 second
  return findBestPrice([vendorA, vendorB, vendorC]);
}
```

**Principle: Message Hospital (Dead Letter Queue) Configuration**

[DON'T]
```javascript
// Anti-pattern: Infinite retry on failure. If this message payload causes an exception, it will crash the worker, be returned to the queue, picked up by the next worker, and crash it too (Catastrophic Failover).
channel.consume('pricing_queue', async (msg) => {
  try {
    await processPricing(msg.content);
    channel.ack(msg);
  } catch (error) {
    // Neglecting to define a retry limit
    channel.nack(msg); // Puts it right back on the queue infinitely
  }
});
```

[DO]
```javascript
// Correct: Tracking retries and routing to a message hospital/dead-letter queue.
channel.consume('pricing_queue', async (msg) => {
  try {
    await processPricing(msg.content);
    channel.ack(msg);
  } catch (error) {
    const retryCount = msg.properties.headers['x-retry-count'] || 0;
    if (retryCount >= MAX_RETRIES) {
      // Route to message hospital
      channel.publish('dead_letter_exchange', 'pricing_failed', msg.content);
      channel.ack(msg); // Remove from active queue
    } else {
      // Requeue with incremented retry count
      channel.nack(msg, false, false); 
      // (Implementation details depend on specific broker features, e.g., RabbitMQ x-death headers)
    }
  }
});
```