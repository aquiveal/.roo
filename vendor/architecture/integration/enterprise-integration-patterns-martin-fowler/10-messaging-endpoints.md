# @Domain
These rules MUST be activated when the AI is tasked with designing, implementing, refactoring, or debugging code that connects an application to a messaging system. Trigger these rules when working on message endpoints, message consumption, message generation, integrating domain objects with messaging infrastructure, throttling message consumption, or coordinating transactions across messages and data stores.

# @Vocabulary
- **Message Endpoint**: A client layer or custom adapter code that connects an application to a messaging channel, encapsulating the messaging system from the rest of the application.
- **Messaging Gateway**: A class that wraps messaging-specific method calls and exposes domain-specific methods to the application, isolating domain logic from messaging APIs.
- **Messaging Mapper**: A separate class containing mapping logic between the messaging infrastructure and domain objects. Neither domain objects nor the infrastructure knows about the mapper.
- **Transactional Client**: An endpoint that controls messaging transactions externally, allowing the application to group multiple messages or coordinate messages with database updates into a single atomic transaction.
- **Polling Consumer (Synchronous Receiver)**: A consumer that explicitly makes a synchronous call when it wants to receive a message, blocking until a message is available or a timeout occurs.
- **Event-Driven Consumer (Asynchronous Receiver)**: A consumer that is automatically invoked by the messaging system (via a callback or listener) when a message is delivered.
- **Competing Consumers**: Multiple consumers listening to a single Point-to-Point Channel to process multiple messages concurrently and increase throughput.
- **Message Dispatcher**: A single consumer that receives messages from a channel and delegates them to a pool of specialized "performers" for processing.
- **Selective Consumer**: A consumer that specifies selection criteria (e.g., a message selector) to filter messages delivered by its channel, receiving only those that match.
- **Durable Subscriber**: A subscriber on a Publish-Subscribe Channel that causes the messaging system to save messages published while the subscriber is disconnected, delivering them upon reconnection.
- **Idempotent Receiver**: A receiver designed to safely handle the same message multiple times without corrupting system state (e.g., via explicit de-duping or inherently idempotent semantics).
- **Service Activator**: A component that receives an asynchronous message, extracts the data, and invokes a synchronous service (e.g., a domain layer method) on behalf of the message sender.

# @Objectives
- Isolate application domain logic from messaging infrastructure details.
- Translate seamlessly between domain objects and messaging structures without coupling them.
- Ensure reliability and data integrity when processing messages alongside other resources like databases.
- Optimize message consumption rates through deliberate load balancing, dispatching, or polling.
- Ensure applications gracefully handle duplicate messages and temporary disconnections.
- Seamlessly bridge asynchronous messaging networks with synchronous application services.

# @Guidelines
- **Encapsulate Messaging Code**: The AI MUST NEVER mix messaging API calls (like JMS, MSMQ, or RabbitMQ) directly into business/domain logic. The AI MUST create a Messaging Gateway to expose a domain-specific API.
- **Isolate Domain Objects**: The AI MUST NEVER add `toMessage()` or `fromMessage()` methods to domain objects. The AI MUST use a separate Messaging Mapper to transfer data between domain objects and messages.
- **Transaction Coordination**: When an application must update a database and send/receive a message atomically, the AI MUST implement a Transactional Client. 
- **Consumer Transactions**: The AI MUST recognize that Transactional Clients work best with Polling Consumers. If using Event-Driven Consumers, the AI MUST be aware that external transaction control is difficult and often unsupported.
- **Throttling via Polling**: If the receiving application is at risk of being overwhelmed by high message volume, the AI MUST implement a Polling Consumer to control the consumption rate, rather than an Event-Driven Consumer.
- **Parallel Processing**: To process messages concurrently from a single channel, the AI MUST deploy Competing Consumers on a Point-to-Point Channel. The AI MUST NEVER use Competing Consumers on a Publish-Subscribe Channel, as this duplicates work.
- **Coordinated Dispatching**: When multiple consumers on a single channel need to be specialized or explicitly coordinated, the AI MUST use a Message Dispatcher rather than Competing Consumers.
- **Filtering at the Endpoint**: When a consumer only wants specific messages from a shared channel without removing the ignored messages from other consumers, the AI MUST implement a Selective Consumer using header-based selection values.
- **Disconnect Resiliency**: If a Publish-Subscribe consumer cannot afford to miss messages during maintenance or network outages, the AI MUST configure it as a Durable Subscriber.
- **Handling Duplicates**: The AI MUST assume messages may be delivered more than once. The AI MUST design endpoints as Idempotent Receivers by tracking unique Message IDs or designing business actions that yield the same result when applied multiple times.
- **Exposing Synchronous Services**: To expose an existing synchronous application service to a messaging channel, the AI MUST implement a Service Activator that handles the asynchronous reception, invokes the service synchronously, and optionally routes the response.

# @Workflow
When tasked with designing or implementing a messaging endpoint, the AI MUST follow this algorithmic process:

1.  **Analyze the Application Interface**: Determine if the application exposes a synchronous API, relies on domain objects, or handles database transactions.
2.  **Establish the Gateway**: Create a Messaging Gateway interface that uses strictly domain-specific terminology.
3.  **Map the Data**: Implement a Messaging Mapper to translate between the application's domain objects and the required message format. Ensure no dependencies exist between the domain objects and the messaging API.
4.  **Determine the Consumption Strategy**:
    *   If the application must strictly control its processing rate: Implement a Polling Consumer.
    *   If the application must react immediately and load is manageable: Implement an Event-Driven Consumer.
5.  **Determine Scalability/Concurrency Needs**:
    *   If processing is a bottleneck: Deploy Competing Consumers.
    *   If consumer selection logic is complex or requires specialized threads: Implement a Message Dispatcher.
6.  **Ensure Reliability and Consistency**:
    *   If updating databases simultaneously: Wrap the endpoint logic in a Transactional Client.
    *   If the topic is Publish-Subscribe and data cannot be missed: Configure a Durable Subscriber.
    *   Always design the endpoint processing logic as an Idempotent Receiver.
7.  **Bridge the Gap**: If integrating with an existing synchronous service, wrap the endpoint logic in a Service Activator.

# @Examples (Do's and Don'ts)

## Messaging Gateway
- **[DO]** Create an interface `ICreditBureauGateway` with a method `GetCreditScore(string ssn)`. Implement the interface in a class that internally handles creating the message, accessing the message queue, and correlating the reply.
- **[DON'T]** Pass a `Message` object or a `MessageQueue` reference directly into a `CustomerService` domain class.

## Messaging Mapper
- **[DO]** Create a `CustomerMessageMapper` class that takes a `Customer` domain object, extracts its fields, and constructs a `Message` object. Trigger this mapper via an observer or gateway.
- **[DON'T]** Make the `Customer` domain object inherit from or reference messaging classes, nor implement a `public Message SerializeToMessage()` method on the domain object itself.

## Idempotent Receiver
- **[DO]** Maintain a cache/database of recently processed `MessageID`s. Before processing a new message, check if its ID exists in the cache. If it does, discard the message.
- **[DO]** Design the message payload to set absolute state: "Update account 12345 balance to $150".
- **[DON'T]** Blindly execute relative updates like "Add $50 to account 12345" without validating the unique Message ID, as a duplicate message delivery will falsely add another $50.

## Transactional Client
- **[DO]** Start a transaction, read a message from the queue, update the database, and then commit the transaction. If the database update fails, rollback the transaction so the message remains on the queue.
- **[DON'T]** Read and acknowledge the message automatically before attempting the database update. If the database update fails, the message is permanently lost.

## Service Activator
- **[DO]** Write an asynchronous message listener (Event-Driven Consumer) that extracts the payload, calls `OrderService.ProcessOrder(payload)`, and takes the return value to publish to a reply queue.
- **[DON'T]** Mix the business logic of `ProcessOrder` directly into the `onMessage` event handler. The business logic must remain in a synchronous service callable without the messaging infrastructure.