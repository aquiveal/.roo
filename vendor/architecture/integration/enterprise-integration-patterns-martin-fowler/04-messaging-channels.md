@Domain
These rules trigger when the AI is architecting, implementing, debugging, or reviewing message-based integration solutions, specifically focusing on the design, configuration, and utilization of logical pathways (channels, queues, topics) between distributed applications or components.

@Vocabulary
- **Message Channel**: A virtual pipe or logical address in a messaging system that connects a sender to a receiver.
- **Unidirectional Channel**: A channel designed for one-way communication; two-way conversations require a pair of channels.
- **Point-to-Point Channel**: A channel that ensures exactly one receiver consumes any given message. If multiple consumers exist, they become Competing Consumers.
- **Publish-Subscribe Channel**: A channel that delivers a copy of a particular message to every active, interested receiver (subscriber).
- **Datatype Channel**: A channel dedicated to carrying messages of strictly one data type or format.
- **Quality-of-Service (QoS) Channel**: A specialized channel tuned for a specific level of service (e.g., high reliability vs. high performance) for a specific group of messages.
- **Invalid Message Channel**: A channel where a receiver routes messages that were successfully delivered but cannot be processed (e.g., parsing, lexical, or format errors).
- **Dead Letter Channel**: A channel where the messaging system itself routes messages that it cannot successfully deliver (e.g., due to channel deletion, expiration, or bad headers).
- **Guaranteed Delivery**: A mechanism that persists messages to disk (store-and-forward) to ensure they are not lost if the messaging system crashes.
- **Channel Adapter**: A component that connects a non-messaging application to a messaging system without modifying the application's source code (e.g., User Interface, Business Logic, or Database adapters).
- **Messaging Bridge**: A set of channel adapters that replicates messages to connect multiple disparate messaging systems (e.g., JMS to MSMQ).
- **Message Bus**: An enterprise-wide integration architecture combining a Canonical Data Model, a common command set, and messaging infrastructure to allow disparate systems to communicate cohesively.

@Objectives
- Establish reliable, decoupled communication pathways between distributed applications.
- Enforce strict structural and semantic rules on message channels to prevent runtime parsing and routing errors.
- Ensure integration architectures account for network unreliability, system crashes, and non-messaging legacy constraints.
- Separate architectural concerns so that applications focus on data payloads while the messaging infrastructure manages delivery, routing, and error isolation.

@Guidelines

**Channel Architecture & Lifecycle**
- The AI MUST design channels as static, logical pathways agreed upon at design time. Channels MUST NOT be dynamically created and discovered at runtime (with the rare exception of temporary reply queues).
- The AI MUST treat all channels as logically Unidirectional. For any two-way conversation (Request-Reply), the AI MUST implement two separate channels.

**Routing Paradigms**
- The AI MUST use a Point-to-Point Channel when a message represents a Command or a Document that should be processed by exactly one receiver.
- The AI MUST use a Publish-Subscribe Channel when a message represents an Event that multiple independent applications need to react to.

**Data Typing and QoS**
- The AI MUST enforce the Datatype Channel pattern. Every message on a given channel MUST conform to the exact same format/schema. If an application emits multiple types, the AI MUST route them to separate channels.
- The AI MUST NOT mix high-priority/reliable messages with low-priority/transient messages on the same channel. The AI MUST create separate Quality-of-Service Channels tailored to the specific persistence and performance requirements of each message group.

**Error Handling (Invalid vs. Dead)**
- The AI MUST implement an Invalid Message Channel for application receivers. If a receiver cannot parse or understand a message's structure, the AI MUST instruct the receiver to catch the error, move the message to the Invalid Message Channel, and acknowledge the original message to clear it from the main channel.
- The AI MUST NOT route application-level semantic errors (e.g., "Account not found") to an Invalid Message Channel. Semantic errors MUST be handled via normal application error responses (e.g., a reply message with an error payload).
- The AI MUST configure a Dead Letter Channel at the messaging infrastructure level for messages the system cannot deliver (e.g., expired messages or unresolved destinations).

**Reliability**
- The AI MUST use Guaranteed Delivery (persistent messaging) for mission-critical data.
- The AI MUST evaluate the performance and disk-space overhead of Guaranteed Delivery. For high-volume, transient data (e.g., frequent streaming stock quotes), the AI MUST disable Guaranteed Delivery to prevent storage overruns and performance bottlenecks.

**Legacy and Cross-System Integration**
- The AI MUST use a Channel Adapter when integrating packaged, legacy, or database applications where source code cannot be modified.
- When extracting data from a database via a Channel Adapter, the AI MUST evaluate the risk of binding the messaging schema to the physical database schema, utilizing a Message Translator where necessary to maintain decoupling.
- The AI MUST use a Messaging Bridge to connect completely separate messaging infrastructures (e.g., cross-vendor integration), mapping corresponding channels one-to-one between the environments.
- The AI MUST design towards a Message Bus architecture for enterprise-wide integration, ensuring all plugged-in applications adhere to a shared Canonical Data Model.

@Workflow
1. **Identify Integration Points**: Determine the systems that need to communicate and the data they must exchange.
2. **Determine Directionality**: Define the direction of data flow. If a response is required, explicitly create a matched pair of Unidirectional Channels.
3. **Select Channel Paradigm**:
   - If the intent is to invoke a specific action or pass a document to one processor, define a Point-to-Point Channel.
   - If the intent is to broadcast a state change, define a Publish-Subscribe Channel.
4. **Enforce Datatypes**: Map every unique data structure to its own Datatype Channel. Never mix schemas in a single channel.
5. **Establish Error Paths**:
   - Create an Invalid Message Channel for the receiver logic.
   - Configure a Dead Letter Channel on the message broker.
6. **Configure QoS & Persistence**: Assess the business value of the messages. Apply Guaranteed Delivery (disk persistence) only to critical messages to balance reliability with performance.
7. **Design Adapters**: If an endpoint is a legacy/non-messaging system, wrap it in a Channel Adapter (UI, API, or DB level).
8. **Finalize the Message Bus**: Ensure all channels and adapters align with a central Canonical Data Model to prevent tightly coupled, point-to-point "integration spaghetti."

@Examples (Do's and Don'ts)

**Datatype Channels**
- [DO]: Create separate queues named `PurchaseOrderQueue` and `CustomerUpdateQueue`, configuring the receiver of each to expect exactly one schema.
- [DON'T]: Create a single `EnterpriseDataQueue` where the receiver must use conditional logic to guess whether the incoming byte stream is a Purchase Order or a Customer Update.

**Invalid Message Handling**
- [DO]: 
  ```csharp
  try {
      var order = Deserialize<Order>(msg.Body);
      ProcessOrder(order);
  } catch (SerializationException) {
      invalidMessageQueue.Send(msg); // Route to Invalid Message Channel
  }
  ```
- [DON'T]: Catch the serialization exception, log it to a local text file, and leave the message on the queue (which causes an infinite loop of poison messages blocking the queue).

**Application Semantic Errors**
- [DO]: Process a perfectly formed `WithdrawalRequest` message, determine the account has insufficient funds, and send a `WithdrawalFailed` document to the reply channel.
- [DON'T]: Process a perfectly formed `WithdrawalRequest`, determine insufficient funds, and route the message to the Invalid Message Channel.

**Quality of Service**
- [DO]: Disable Guaranteed Delivery for a `LivePriceTicker` topic where a new message overrides the old one every 100 milliseconds.
- [DON'T]: Enable Guaranteed Delivery for high-frequency transient events, which risks exhausting the message broker's disk space during a network partition.

**Point-to-Point vs. Publish-Subscribe**
- [DO]: Use a Publish-Subscribe `AddressChangeTopic` so the Billing System, Shipping System, and CRM can all independently receive the update.
- [DON'T]: Use a Point-to-Point `AddressChangeQueue` with multiple competing consumers if all systems need to know about the address change (only the first consumer to poll would get the message).