# @Domain
This rule file is triggered when the AI is tasked with designing, implementing, refactoring, or debugging Enterprise Application Integration (EAI) solutions, Service-Oriented Architectures (SOA), distributed business processes, or asynchronous messaging systems. It activates whenever requests involve routing, transforming, monitoring, or decoupling data exchanges between disparate applications, legacy systems, or B2B partners.

# @Vocabulary
*   **Information Portal**: An integration style that aggregates information from multiple sources into a single user display without duplicating the data in a backend database.
*   **Data Replication**: An integration style that copies data from one system's data store to another's so each application can operate on its own local copy.
*   **Shared Business Function**: Reusable business logic exposed as a service that multiple applications can invoke, avoiding redundant code.
*   **Distributed Business Process**: A single business transaction orchestrated across multiple independent systems.
*   **Loose Coupling**: An architectural principle where communicating systems make minimal assumptions about each other regarding platform, location, availability (time), and internal data formats.
*   **Message**: An atomic, self-contained packet of data used to transmit information asynchronously over a channel.
*   **Message Channel**: A logical, addressable pathway connecting programs to convey messages.
*   **Point-to-Point Channel**: A channel guaranteeing that exactly one consumer will receive a specific message.
*   **Publish-Subscribe Channel**: A channel that broadcasts a copy of a message to all active, subscribed consumers.
*   **Datatype Channel**: A channel dedicated strictly to carrying messages of a single, uniform type.
*   **Invalid Message Channel**: A designated channel for messages that a receiver cannot process due to formatting, validation, or semantic errors.
*   **Message Endpoint**: A layer of code connecting an application to the messaging system.
*   **Messaging Gateway**: An endpoint that encapsulates messaging-specific APIs, exposing a domain-specific, synchronous or asynchronous interface to the application logic.
*   **Channel Adapter**: A component that connects a legacy or packaged application to a messaging system without altering the application's source code (e.g., via database triggers or UI scraping).
*   **Message Router**: A component that consumes a message from one channel and publishes it to a different channel based on specific conditions.
*   **Content-Based Router**: A router that inspects message content to determine its ultimate destination.
*   **Message Filter**: A router that inspects a message and passes it to an output channel only if it matches specific criteria; otherwise, it discards the message.
*   **Recipient List**: A router that inspects a message, computes a list of desired recipients, and forwards the message to each recipient's channel.
*   **Dynamic Recipient List**: A Recipient List coupled with a Dynamic Router that allows recipients to set their subscription preferences dynamically via a control channel.
*   **Splitter**: A router that breaks a single composite message into a series of individual messages containing data related to one item.
*   **Aggregator**: A stateful filter that collects individual messages and combines them into a single message once a completeness condition is met.
*   **Composed Message Processor**: A composite pattern consisting of a Splitter, a Message Router, and an Aggregator.
*   **Process Manager**: A central component that manages the flow of messages through a sequence of steps, maintaining state and determining the next step based on intermediate results.
*   **Message Translator**: A filter that converts a message from one format to another.
*   **Canonical Data Model**: A standard, application-independent data format agreed upon by all participating systems to eliminate N-to-N translation dependencies.
*   **Content Enricher**: A translator that accesses an external data source to augment a message with missing information.
*   **Claim Check**: A pattern that temporarily stores a large message payload in a persistent store, passing only a reference key (the claim check) through the messaging system to reduce overhead.
*   **Return Address**: A message header property indicating where the replier should send the reply message.
*   **Smart Proxy**: An intermediary component that intercepts request messages, replaces the Return Address with its own, and forwards replies back to the original address, often used for monitoring.
*   **Control Bus**: A dedicated messaging subsystem used to transmit configuration, heartbeat, exception, and metrics data to a central management console.
*   **Wire Tap**: A fixed Recipient List inserted into a channel to route a copy of a message to a secondary channel for inspection without altering the primary message flow.
*   **Test Message**: A specifically tagged message injected into the live message stream to verify the health and accuracy of message processing components.

# @Objectives
*   Achieve true Loose Coupling by eliminating platform, location, temporal, and data-format dependencies between integrated applications.
*   Ensure reliable communication across unreliable networks using asynchronous store-and-forward messaging.
*   Isolate integration mechanics (routing, transformation, protocol handling) from core business application logic.
*   Prevent the exponential explosion of integration connections (N-squared problem) by enforcing a Canonical Data Model and centralizing routing decisions.
*   Maintain comprehensive visibility and control over distributed asynchronous systems without disrupting the primary business data flow.

# @Guidelines
*   **Coupling & Communication Style**
    *   The AI MUST NOT use tightly coupled communication mechanisms (like basic TCP/IP sockets or synchronous RPC) for long-running, distributed business processes.
    *   The AI MUST employ Asynchronous Messaging for robust, send-and-forget communication.
    *   The AI MUST use File Transfer integrations ONLY for infrequent, bulk data replication (e.g., quarterly catalog updates).
*   **Endpoints & Integration Boundaries**
    *   The AI MUST use Channel Adapters to integrate packaged or legacy applications where source code cannot be modified.
    *   The AI MUST encapsulate messaging APIs inside a Messaging Gateway, exposing only domain-specific methods to the application logic.
*   **Channel Strategy & Naming**
    *   The AI MUST define separate Datatype Channels for different types of messages; do not mix message types on a single channel.
    *   The AI MUST name application-specific (private) channels with the application name prefix (e.g., `WEB_NEW_ORDER`).
    *   The AI MUST name Canonical (public) channels strictly by their intent without application prefixes (e.g., `NEW_ORDER`).
    *   The AI MUST implement an Invalid Message Channel for every system to gracefully handle malformed or undecipherable messages.
*   **Message Routing**
    *   The AI MUST use a Content-Based Router to abstract the physical implementation of a logical function spread across multiple systems (e.g., routing orders to Widget vs. Gadget inventory systems).
    *   The AI MUST use a Splitter when processing messages containing multiple elements (e.g., order lines) that require independent processing.
    *   The AI MUST use a Content Enricher to append required data to a message (e.g., generating a unique Order ID) BEFORE splitting it, ensuring child messages can be correlated later.
    *   The AI MUST use an Aggregator to recombine split or scattered messages, explicitly defining a correlation mechanism, a completeness condition, and an aggregation algorithm.
    *   The AI MUST use a Dynamic Recipient List instead of a Publish-Subscribe Channel when message distribution must be explicitly controlled to prevent unauthorized listeners or reduce network waste.
*   **State & Flow Management**
    *   The AI MUST use a Process Manager instead of hardcoded channel routing if the sequence of processing steps depends on intermediate results or requires complex state management between asynchronous steps.
    *   The AI MUST NOT carry unnecessarily large payloads through intermediate systems. Implement a Claim Check to store large data centrally and pass a lightweight reference key through the message flow.
*   **Transformation & Data Formats**
    *   The AI MUST design and enforce a Canonical Data Model for all public enterprise messages.
    *   The AI MUST use Message Translators to convert between an application's internal data format and the Canonical Data Model.
*   **System Management & Monitoring**
    *   The AI MUST implement a separate Control Bus for all metrics, monitoring, and heartbeat messages.
    *   The AI MUST use a Wire Tap to inspect messages on a Point-to-Point Channel without consuming them or altering the primary flow.
    *   To track quality of service (e.g., response times) for a Request-Reply service, the AI MUST inject a Smart Proxy to intercept the Return Address, measure elapsed time, and forward the reply.
    *   The AI MUST utilize Test Messages with a Test Data Verifier for active monitoring of external services (e.g., 3rd party credit bureaus).

# @Workflow
1.  **Analyze the Integration Scenario**: Determine if the requirement is an Information Portal, Data Replication, Shared Business Function, Distributed Business Process, or B2B integration.
2.  **Define the Interface Boundary**: Identify whether participating systems can be modified. If not, design Channel Adapters (Database, UI, or Business Logic adapters). If yes, design a Messaging Gateway.
3.  **Establish Data Formats**: Define the Canonical Data Model for the business entities involved. Specify Message Translators to bridge private application formats to the canonical format.
4.  **Determine Channel Topologies**: 
    *   Assign Point-to-Point Channels for Command Messages or Document Messages intended for a single consumer.
    *   Assign Publish-Subscribe Channels for Event Messages.
    *   Define the Invalid Message Channel for exception handling.
5.  **Design the Message Routing**:
    *   If a message contains multiple items, insert a Splitter.
    *   If data is missing for routing, insert a Content Enricher.
    *   If the message must go to specific functional systems, insert a Content-Based Router.
    *   If results must be merged, implement an Aggregator.
    *   If the flow is highly dynamic/stateful, replace simple routing with a Process Manager.
6.  **Instrument for Management**: Apply Wire Taps to critical channels to log messages. Deploy Smart Proxies around Request-Reply services to capture performance metrics. Route all management telemetry to the Control Bus.

# @Examples (Do's and Don'ts)

**Example 1: Connecting Applications (Coupling)**
*   [DON'T] Use low-level TCP/IP sockets transmitting byte arrays with fixed offsets and hardcoded IP addresses. This introduces severe location, platform, and temporal coupling.
*   [DO] Use an asynchronous messaging framework (like JMS, MSMQ, or RabbitMQ) sending self-describing XML/JSON Document Messages to logical channel names.

**Example 2: Abstracting Messaging APIs**
*   [DON'T] Embed messaging API code directly into business logic.
```java
// Anti-pattern: Business logic mixed with messaging infrastructure
public void processOrder(Order order) {
    Connection conn = factory.createConnection();
    Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
    MessageProducer producer = session.createProducer(queue);
    TextMessage msg = session.createTextMessage(order.toXml());
    producer.send(msg);
}
```
*   [DO] Use a Messaging Gateway to separate concerns.
```java
// Correct: Business logic uses a domain-specific interface
public void processOrder(Order order) {
    orderGateway.sendNewOrder(order); 
}
// Gateway implementation handles the messaging APIs separately.
```

**Example 3: Handling Large Messages**
*   [DON'T] Pass multi-megabyte payloads through 10 routing and validation steps that only require the document metadata.
*   [DO] Implement a Claim Check. Store the large payload in a database, generate a unique ID, and pass the ID in the message. Use a Content Enricher right before the final destination to retrieve the payload.

**Example 4: Tracking Response Times**
*   [DON'T] Hardcode the reply channel in the service provider to route through a monitoring tool.
*   [DO] Use a Smart Proxy.
    1. Proxy intercepts Request.
    2. Proxy saves the original Return Address and Timestamp.
    3. Proxy overwrites Return Address with its own Address and forwards Request to Service.
    4. Service replies to Proxy.
    5. Proxy calculates elapsed time, publishes metric to Control Bus, and routes Reply to the saved Return Address.

**Example 5: Channel Naming**
*   [DON'T] Name channels arbitrarily: `queue1`, `my_orders`, `sap_to_oracle`.
*   [DO] Separate canonical channels from application channels:
    *   App-specific: `CALLCENTER_NEW_ORDER`, `WEB_NEW_ORDER`
    *   Canonical: `NEW_ORDER`
    *   Exception: `INVALID_ORDER_CHANNEL`