# @Domain
These rules MUST be activated whenever the AI is requested to design, implement, debug, or maintain the operations, monitoring, testing, or administration infrastructure of an asynchronous enterprise messaging system. This applies to tasks involving message tracking, health monitoring, dynamic routing alterations for debugging, metric collection, and message channel maintenance.

# @Vocabulary
*   **System Management**: The practice of monitoring the health, throughput, and latency of a messaging system (as opposed to inspecting business payload data).
*   **BAM (Business Activity Monitoring)**: The practice of monitoring the business payload data contained within messages (e.g., the dollar value of orders).
*   **Control Bus**: A dedicated messaging subsystem that uses separate channels to transmit configuration, heartbeat, exception, and metric data relevant to the management of components.
*   **Detour**: A Context-Based Router controlled via the Control Bus that dynamically routes messages through additional, optional steps (e.g., validation or logging) before sending them to their ultimate destination.
*   **Wire Tap (Tee)**: A fixed Recipient List with two output channels that consumes a message and publishes the unmodified message to the primary channel and a secondary channel for inspection.
*   **Message History**: A list stored within the message header containing the unique identifiers of all applications or components the message has traversed.
*   **Message Store**: A persistent, central data store that captures information about messages (often fed by a Wire Tap) for offline analysis, reporting, and auditing.
*   **Smart Proxy**: A component that intercepts Request-Reply messages, stores the original Return Address, substitutes its own reply channel address, and upon receiving the reply, forwards it to the original Return Address.
*   **Test Message**: A specifically tagged message injected into a production stream by a Test Data Generator to actively verify the health and correct operation of components.
*   **Channel Purger**: A utility component designed to explicitly remove leftover, unwanted, or stuck messages from a channel to reset the system into a consistent state.
*   **Active Monitoring**: Probing a component's health by injecting actual data (e.g., Test Messages) and verifying the output.
*   **Passive Monitoring**: Observing a component's health by relying on the component to emit information (e.g., Heartbeats, logs) without altering the message flow.

# @Objectives
*   Solve the "architect's dream, developer's nightmare" syndrome by injecting strict observability and debugging capabilities into loosely coupled, asynchronous architectures.
*   Ensure that system management data never interferes with or clutters application data channels.
*   Guarantee that observation components (like Wire Taps) do not alter the primary message payload or semantics.
*   Provide robust mechanisms for tracking asynchronous Request-Reply flows across trust boundaries or when original Return Addresses cannot be easily tracked.
*   Enable active and passive component health monitoring without corrupting business state (e.g., preventing test data from being persisted as business records).
*   Ensure test environments and malfunctioning components can be reset to clean states using targeted purges.

# @Guidelines

### 1. Monitoring and Controlling
*   **Control Bus Separation**: The AI MUST isolate system management traffic from application data traffic. When implementing component administration, the AI MUST design a Control Bus utilizing separate messaging channels.
*   **Control Bus Payloads**: The AI MUST restrict Control Bus payloads to the following types: Configuration updates, Heartbeats, Test Messages, Exceptions, and Statistics.
*   **Detour Routing**: When a user requests the ability to toggle validation, debugging, or logging steps on and off at runtime, the AI MUST implement a Detour using a Context-Based Router listening to a Control Bus channel for state changes.

### 2. Observing and Analyzing Message Traffic
*   **Wire Tap Immutability**: When implementing a Wire Tap, the AI MUST NOT allow the tapping component to modify the message payload. The message MUST be copied exactly.
*   **Wire Tap Correlation Warning**: The AI MUST account for messaging infrastructure assigning new Message IDs to the duplicated message exiting a Wire Tap. The AI MUST NOT use the infrastructure-generated Message ID to correlate the primary and secondary messages; it MUST rely on an explicit Correlation Identifier.
*   **Message History Location**: When tracking a message's path through the system, the AI MUST append the component's unique identifier to the Message History list. This list MUST be stored exclusively in the message header, NEVER in the payload body.
*   **Message Store Storage Strategy**: When designing a Message Store, the AI MUST select an appropriate database schema. If the store handles multiple distinct message types, the AI MUST store the message body as an unstructured text/XML field to avoid schema explosion, while indexing header fields (like Message ID or Correlation ID) for querying.
*   **Message Store Purging**: The AI MUST define a garbage collection or archiving process for any Message Store implementation to prevent disk space exhaustion.
*   **Smart Proxy Return Address Handling**: When tracking messages on a Request-Reply service that utilizes dynamic Return Addresses, the AI MUST implement a Smart Proxy. The Smart Proxy MUST:
    1. Intercept the request.
    2. Store the original Return Address and Correlation ID in a local data store (e.g., memory or DB).
    3. Replace the Return Address with its own reply channel.
    4. Replace the Correlation ID with a newly generated Correlation ID (to prevent mismatching due to intermediary ID assignment).
    5. Upon receiving the reply, restore the original Return Address and Correlation ID, and forward the message.

### 3. Testing and Debugging
*   **Test Message Tagging**: When injecting a Test Message into an active system, the AI MUST explicitly tag the message (e.g., via a special header field or specific Return Address) so that stateful components (like databases) do not process the test data as real business data.
*   **Avoid Overloading Dual Semantics**: The AI MUST NOT use legitimate business fields (e.g., `OrderID = 999999`) to indicate a Test Message unless absolutely no other option exists. Header tags MUST be the primary mechanism.
*   **Channel Purger Implementation**: When a component fails and leaves invalid messages stuck in a persistent channel, the AI MUST implement a Channel Purger to clear the queue. The AI MUST offer the user the option to either permanently discard the purged messages or route them to a Message Store for later inspection/replay.

# @Workflow
1.  **Analyze the Management Requirement**: Determine if the user's request pertains to passive monitoring (Wire Tap, Message Store, Message History), active monitoring (Test Message, Heartbeat), control (Detour, Control Bus), or recovery (Channel Purger).
2.  **Separate the Infrastructure**: Before generating application logic, define the dedicated channels that will form the Control Bus.
3.  **Apply the Pattern**:
    *   *For observability*: Insert a Wire Tap before or after the target component. Route the secondary channel to a Message Store.
    *   *For tracing*: Append code to each processing filter to add its ID to the Message History header.
    *   *For Request-Reply tracing*: Wrap the service in a Smart Proxy to safely manage Return Addresses and Correlation IDs.
    *   *For health checking*: Implement a Test Data Generator and Test Data Verifier, utilizing a unique test Return Address to bypass actual business side-effects.
    *   *For dynamic routing*: Insert a Detour and expose its routing logic to the Control Bus.
4.  **Enforce Immutability and State Protection**: Verify that Wire Taps do not change payloads, and Test Messages are strictly prevented from corrupting business databases.
5.  **Provide Cleanup Mechanisms**: Ensure Message Stores have expiration/archiving logic, and define Channel Purgers for fault recovery.

# @Examples (Do's and Don'ts)

### Wire Tap Correlation
*   **[DO]** Use a dedicated Correlation Identifier present in the message payload or header to link messages captured by a Wire Tap.
```csharp
// The Wire Tap duplicates the message. 
// Use an application-specific Correlation ID to track it in the Message Store.
string correlationId = originalMessage.AppSpecificCorrelationId;
primaryQueue.Send(originalMessage);
secondaryStoreQueue.Send(originalMessage);
```
*   **[DON'T]** Rely on the infrastructure's Message ID to correlate the tapped message with the primary message, as the queuing system will assign a new ID to the duplicated message.
```csharp
// ANTI-PATTERN: The Message ID will change when sent to the secondary queue.
string primaryId = primaryQueue.Send(originalMessage).Id;
string secondaryId = secondaryStoreQueue.Send(originalMessage).Id;
// secondaryId != primaryId, correlation is lost.
```

### Smart Proxy Implementation
*   **[DO]** Store the original Return Address and Correlation ID in the Smart Proxy, and map it to a new proxy-generated Correlation ID before forwarding to the actual service.
```csharp
// Intercept Request
MessageData data = new MessageData(request.Id, request.ResponseQueue, request.CorrelationId);
messageDataStore.Add(newProxyCorrelationId, data);
request.ResponseQueue = smartProxyReplyQueue;
request.CorrelationId = newProxyCorrelationId;
actualServiceQueue.Send(request);

// Process Reply
MessageData originalData = messageDataStore[reply.CorrelationId];
reply.CorrelationId = originalData.CorrelationId;
originalData.ResponseQueue.Send(reply);
```
*   **[DON'T]** Pass the original Correlation ID through the proxy to the service, as multiple clients might use conflicting/duplicate Correlation IDs, which will collide in the Smart Proxy's single reply queue.

### Test Message Injection
*   **[DO]** Inject a Test Message using a dedicated header flag so that business applications know to discard the payload before inserting it into a database.
```xml
<SOAP-ENV:Header>
    <sys:TestMessageFlag>TRUE</sys:TestMessageFlag>
</SOAP-ENV:Header>
<SOAP-ENV:Body>
    <order>...</order> <!-- System knows not to process this as a real order -->
</SOAP-ENV:Body>
```
*   **[DON'T]** Overload a business data field to indicate a test, which corrupts business logic semantics.
```xml
<!-- ANTI-PATTERN -->
<SOAP-ENV:Body>
    <!-- 999999 means "Test" - Bad practice! -->
    <orderId>999999</orderId> 
</SOAP-ENV:Body>
```

### Control Bus Usage
*   **[DO]** Use a completely separate channel (Control Bus) to send configuration changes (like toggling a Detour) to a running component.
*   **[DON'T]** Send configuration commands intermixed on the same Data-type channel used for business payloads.