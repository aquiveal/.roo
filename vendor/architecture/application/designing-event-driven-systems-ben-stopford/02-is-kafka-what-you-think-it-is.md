@Domain
- Trigger these rules when designing, refactoring, or reviewing architectures involving Apache Kafka.
- Trigger when evaluating communication protocols between microservices, specifically deciding between messaging, REST/RPC, and event streaming.
- Trigger when integrating legacy systems, building data pipelines, or designing stream processing topologies.

@Vocabulary
- **Broker**: A separate piece of infrastructure in Kafka that broadcasts messages to interested programs and stores them for as long as needed.
- **Enterprise Service Bus (ESB)**: A legacy architectural pattern characterized by ephemeral, low-throughput messaging and centralized teams dictating schemas, flows, and transformations. Treated as an anti-pattern in modern streaming.
- **Streaming Platform**: The holistic ecosystem of Kafka, moving beyond simple messaging to include distributed brokers, stream processing engines (Kafka Streams/KSQL), data integration (Connect), and utilities (Schema Registry).
- **Database Inside Out**: A conceptual model for Kafka where the traditional components of a database (commit log, query engine, caching) are unbundled; it stores data, processes it in real-time, and creates views.
- **Kafka Streams / KSQL**: Database engines for data in flight. APIs used to embed stateful and stateless stream processing directly into application clients.
- **Connect API**: An API and ecosystem of connectors used to pull data from and push data to a wide range of external databases and endpoints.
- **Schema Registry**: A utility used to manage and validate schemas for messages passing through Kafka.
- **Fire-and-forget**: An asynchronous messaging pattern where a producer sends a message to the broker without waiting for a response.

@Objectives
- Prevent the misapplication of Kafka for use cases better served by simple stateless protocols (e.g., synchronous request-response).
- Eradicate ESB anti-patterns by strictly enforcing decentralized stream processing and autonomous service logic.
- Shift architectural focus from data at rest to continuous data in flight.
- Ensure the full Confluent/Kafka platform ecosystem (Connect, Streams, KSQL, Schema Registry) is utilized effectively rather than treating Kafka as a simple message queue.

@Guidelines
- **Avoid Kafka for Pure Request-Response**: DO NOT use Kafka to orchestrate simple synchronous request-response interactions (e.g., fetching a customer record) where broadcast and storage are unnecessary. The AI MUST recommend stateless protocols like HTTP/REST for these scenarios.
- **Acknowledge Kafka's Home Ground**: The AI MUST reserve Kafka for event-based communication where events are business facts that have value to multiple services and require durable storage.
- **Reject ESB Anti-Patterns**: The AI MUST aggressively reject designs that introduce central orchestration teams or centralized components that dictate schemas, message flows, validation, and transformation. 
- **Enforce Decentralization**: The AI MUST instruct services to retain control over their own data and logic. Data manipulation must happen at the edges (in the consuming applications) using Kafka Streams or KSQL.
- **Apply the Core Mantra**: System designs MUST adhere to the principle: "Centralize an immutable stream of facts. Decentralize the freedom to act, adapt, and change."
- **Treat Kafka as a Database Inside-Out**: The AI MUST design Kafka architectures to prioritize real-time processing and continual computation over batch processing. 
- **Utilize the Complete Platform**:
  - Use the **Connect API** to unlock hidden datasets in legacy systems or external databases, turning data at rest into event streams.
  - Use **Kafka Streams** or **KSQL** to allow applications to embed processing logic (filter, join, aggregate, stateful tables) directly over event streams.
  - Use the **Schema Registry** to validate and manage data formats.

@Workflow
1. **Analyze the Interaction Model**: Evaluate the required inter-system communication. If it is a 1-to-1 lookup expecting an immediate response without the need for data retention or broadcasting, explicitly mandate HTTP/REST and halt Kafka implementation for that specific interaction.
2. **Design the Central Nervous System**: If the interaction involves sharing business facts, architect a highly available Kafka broker cluster as the central immutable log.
3. **Integrate External Data**: Assess if data needs to flow in from or out to external databases/legacy systems. If yes, define a Kafka Connect topology to handle the ingestion/egress without writing custom polling scripts.
4. **Distribute the Processing Logic**: Identify where data transformation, filtering, or joining is required. Embed this logic directly into the consuming applications using Kafka Streams or KSQL rather than creating a central processing middleware.
5. **Verify Autonomy**: Conduct a design review against ESB anti-patterns. Ensure no single service or central team is acting as an orchestrator for the entire pipeline. Verify that each service independently subscribes to, processes, and acts upon the data.

@Examples (Do's and Don'ts)

- **Interaction Protocol Selection**
  - [DO]: Use HTTP/REST to implement a `getCustomer(CustomerId)` method that returns a customer document.
  - [DON'T]: Create a `CustomerRequest` Kafka topic and a `CustomerResponse` Kafka topic to simulate a synchronous remote procedure call.

- **Data Transformation and Routing**
  - [DO]: Publish raw "Order Created" events to a central topic. Allow the Shipping Service, Billing Service, and Inventory Service to independently consume the topic, using Kafka Streams internally to filter and transform the data as needed for their specific domain.
  - [DON'T]: Deploy a centralized Kafka routing application that consumes "Order Created" events, transforms them into shipping/billing/inventory formats, and dictates exactly which service receives which formatted message.

- **Data Integration**
  - [DO]: Deploy the Kafka Connect API with a source connector to automatically stream row-level changes from a legacy relational database into a Kafka topic.
  - [DON'T]: Write a custom application that runs `SELECT * FROM table WHERE updated_at > last_run`, manually serializes the data, and pushes it to Kafka.

- **Querying Data**
  - [DO]: Use KSQL to define a continuous query that updates a materialized view in real-time as new events arrive, which your application can then query locally.
  - [DON'T]: Attempt to treat a Kafka topic exactly like a relational database table by submitting ad-hoc batch queries against the raw topic data whenever a user clicks a button.