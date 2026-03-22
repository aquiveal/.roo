@Domain
These rules are activated when the AI is tasked with designing, implementing, refactoring, or troubleshooting asynchronous messaging architectures, particularly those involving real-time data feeds (e.g., financial market data), legacy system integration (e.g., C++ to Java messaging), thick-client UI data binding, high-throughput publish-subscribe systems, or solving messaging performance bottlenecks (e.g., slow consumers, dead-letter queue overflows, UI thread freezing).

@Vocabulary
- **Market Data**: Real-time information regarding the price and properties of a domain entity (e.g., a bond) representing buying/selling states on a free market.
- **Analytics Engine**: A generic mathematical processing component that modifies incoming data streams based on configuration variables.
- **Contribution Server**: A legacy or external-facing component that performs all communication with third-party trading venues or external providers.
- **Thick Client**: A highly responsive desktop application (e.g., Java Swing/UI) that provides an encapsulated user interface for advanced analytics and high-volume data display.
- **Gateway (Pricing/Contribution)**: An intermediate software component that encapsulates the business logic required to communicate with backend legacy servers, shielding the client from integration complexities.
- **TIB (TIBCO Information Bus)**: A publish-subscribe messaging infrastructure often utilizing hierarchical subjects for channel routing.
- **Messaging Bridge**: A connection between two disparate messaging systems (e.g., TIB and JMS) created by combining two Channel Adapters and a cross-language translation protocol (e.g., CORBA).
- **Content-Based Router**: A component that reads a message and routes it to a specific destination channel based on the data contained within the message.
- **Point-to-Point Channel**: A messaging channel guaranteeing that exactly one eligible consumer receives a particular message.
- **Publish-Subscribe Channel**: A messaging channel where a copy of the message is delivered to all active, interested subscribers.
- **Message Filter**: A component that controls message flow by dropping/ignoring messages that do not meet specific criteria (e.g., time-based or content-based).
- **Aggregator**: A stateful component that collects related messages over time and combines them into a single comprehensive message.
- **Polling Consumer**: A consumer that proactively requests messages from a channel at its own pace (synchronous receiver).
- **Event-Driven Consumer**: A consumer whose message-processing logic is triggered automatically by the messaging system as soon as a message arrives (asynchronous receiver).
- **Message Expiration**: A property dictating the time-to-live of a message; if unconsumed in this window, it is routed to the Dead Letter Channel.
- **Dead Letter Channel**: A queue/channel where the messaging system places messages that cannot be delivered or have expired.
- **Slow Consumer**: A message receiver that cannot process incoming messages as fast as they are placed on the channel, causing message timeouts.
- **Message Dispatcher**: A pattern where a single main consumer listens to a channel and delegates processing to a pool of separate worker threads (Performers).

@Objectives
- Achieve strict encapsulation of legacy systems by deploying intermediate Gateway components.
- Select the optimal integration style (RPC vs. Messaging) based on subscriber cardinality, data volatility, and system decoupling requirements.
- Structure message channels to maximize the reusability of generic backend engines while minimizing the channel-listening burden on end-user clients.
- Prevent duplicate transaction processing and ensure synchronized client updates by strategically mixing Point-to-Point and Publish-Subscribe channels based on the direction of communication.
- Protect client UI threads from freezing during high-frequency data bursts by decoupling data arrival from data consumption.
- Prevent catastrophic messaging system crashes caused by slow consumers and expired messages overflowing Dead Letter Channels.

@Guidelines

- **Legacy System Encapsulation**: The AI MUST NOT allow client applications to communicate directly with legacy backend servers. The AI MUST create domain-specific Gateway components (e.g., Pricing Gateway) to encapsulate business logic and protocol translation.
- **Integration Style Selection**: When integrating components where data must be pushed to an unknown or dynamic number of clients simultaneously, the AI MUST use Messaging (Publish-Subscribe) rather than Remote Procedure Invocation (RPC) to avoid complex, multithreaded client-tracking logic in the server.
- **Cross-Platform Messaging Bridges**: When connecting two disparate messaging infrastructures (e.g., C++/TIB and Java/JMS), the AI MUST implement a Messaging Bridge by deploying a Channel Adapter for each messaging system and bridging them with a non-messaging cross-language protocol (e.g., CORBA). The AI MUST NOT attempt to use a standard Message Translator for cross-platform bridging.
- **Generic Engine Channel Structuring**: When designing generic processing engines (e.g., Analytics Engines), the AI MUST keep the engine logic generic by using highly granular input/output channels (e.g., one channel per bond per trader). The AI MUST NOT embed custom routing logic inside generic engines to group channels.
- **Client Channel Consolidation**: To prevent the client application from listening to tens of thousands of channels, the AI MUST position a Content-Based Router inside the Gateway. The Gateway MUST subscribe to the granular backend channels and route the messages to a consolidated, manageable set of channels (e.g., one channel per trader) for the client.
- **Directional Channel Typing**:
  - For **Client-to-Server** communication (e.g., placing trades/commands), the AI MUST use **Point-to-Point Channels** to guarantee that only one server instance processes the request, preventing duplicate execution.
  - For **Server-to-Client** communication (e.g., broadcasting data updates), the AI MUST use **Publish-Subscribe Channels** to ensure that if a user is logged into multiple physical workstations concurrently, all instances receive the data.
- **UI Throttling via Polling Aggregation**: When a client UI is overwhelmed by high-frequency, partial data updates (causing thread freezing), the AI MUST NOT use a Message Filter, as this will drop critical partial data. Instead, the AI MUST use a stateful **Aggregator** on the server/gateway side to compile the latest state, and switch the client to a **Polling Consumer** that fetches the aggregated state via a Command Message/Document Message Request-Reply pattern at a UI-safe interval.
- **Slow Consumer Crash Prevention**: When asynchronous message volume causes messages to expire and crash the messaging server via Dead Letter Channel overflow, the AI MUST NOT use Competing Consumers on a Publish-Subscribe channel (which only duplicates the work). Instead, the AI MUST implement a **Message Dispatcher** that receives the message quickly and hands it off to a pool of background `Performer` threads, ensuring the main listener returns immediately to consume the next message.

@Workflow
1.  **Component Identification**: Identify all legacy sub-systems, UI clients, and messaging buses in the architecture.
2.  **Gateway Injection**: Insert Gateway components between the client tier and the legacy tier.
3.  **Bridge Construction**: If the legacy bus and modern bus differ (e.g., TIB vs JMS), construct a Messaging Bridge using Channel Adapters and an RPC protocol.
4.  **Channel Topology Design**:
    *   Assign granular, entity-specific channels (e.g., per-item) at the backend.
    *   Deploy Content-Based Routers in the Gateways to consolidate channels for the UI.
5.  **Channel Type Assignment**: Assign Point-to-Point for inbound commands (Client->Server) and Publish-Subscribe for outbound data (Server->Client).
6.  **Throttling Analysis**: Evaluate data velocity. If UI thread saturation is a risk, implement an Aggregator and convert the client from an Event-Driven Consumer to a Polling Consumer.
7.  **Throughput/Resiliency Hardening**: Evaluate the consumer's ability to process messages before Message Expiration. If the consumer is a bottleneck, implement a Message Dispatcher with a Performer thread pool to drain the channel rapidly.

@Examples (Do's and Don'ts)

- **Cross-Platform Integration**
  - [DO]: Implement a Messaging Bridge by creating a C++ Channel Adapter for the legacy bus, a Java Channel Adapter for the modern bus, and connect them via CORBA to exchange messages.
  - [DON'T]: Attempt to write a standard Message Translator to convert a proprietary C++ message directly into a Java JMS message within a single runtime.

- **Channel Type Selection for Multi-Session Clients**
  - [DO]: Use a Publish-Subscribe channel for sending price updates to Trader A, ensuring that if Trader A is logged in on both a desktop and a laptop, both screens update synchronously.
  - [DON'T]: Use a Point-to-Point channel or a Recipient List to send price updates to a specific user, as the message will be consumed by the first workstation that polls, leaving the second workstation with stale data.

- **Preventing Duplicate Transactions**
  - [DO]: Use a Point-to-Point channel for sending a "Submit Trade" command from the client to the backend, ensuring only one server node picks up the trade.
  - [DON'T]: Use a Publish-Subscribe channel for submitting trades, which would cause all listening backend server instances to execute the exact same trade simultaneously.

- **Throttling High-Frequency Updates**
  - [DO]: Use an Aggregator to constantly update the latest state of a bond in memory, and have the client run a background loop (Polling Consumer) that requests the aggregated data every 250ms.
  - [DON'T]: Use a time-based Message Filter that simply drops messages arriving within 5ms of the previous message, as this will permanently destroy partial field updates contained in the dropped messages.

- **Fixing Dead Letter Queue Overflows (Slow Consumers)**
  - [DO]: Implement a Message Dispatcher where the primary `onMessage` listener instantly delegates the message payload to a separate `Performer` thread in a pool and returns to the channel to consume the next message.
  - [DON'T]: Add multiple Competing Consumers to a Publish-Subscribe channel, as every consumer will simply receive a duplicate copy of the exact same message, drastically worsening the server load.