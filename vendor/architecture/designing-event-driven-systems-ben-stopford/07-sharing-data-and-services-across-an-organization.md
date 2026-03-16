# @Domain
These rules MUST trigger when the AI is engaged in tasks involving distributed system architecture, microservices design, inter-team data sharing, API design, event-driven system refactoring, or resolving data integration and coupling issues across multiple organizational boundaries.

# @Vocabulary
*   **Connascence / Coupling**: A measure of the impact a change to one component will have on others. In distributed systems, this is intrinsically linked to organization, software, and data.
*   **Inverse Conway Maneuver**: The practice of changing the organizational structure to allow the software architecture to naturally follow suit.
*   **The Data Dichotomy**: The fundamental architectural conflict where services are designed to hide (encapsulate) data to remain decoupled, while databases/data systems are designed to expose data to make it maximally useful.
*   **God Service Problem**: An anti-pattern where a single data service grows over time to expose an ever-increasing set of query functions, effectively becoming a tightly coupled, homegrown, bottlenecked database.
*   **REST-to-ETL Problem**: An anti-pattern where services periodically poll and extract large amounts of data from another service's REST API because they need the data locally, leading to massive data divergence and operational instability.
*   **Cycle of Data Inadequacy**: The endless cyclical anti-pattern of centralizing data to keep it accurate, only for teams to inevitably extract and hoard it locally for autonomy, leading back to divergence.
*   **Data on the Outside**: Shared, immutable facts and events communicated between services. It is tightly coupled, hard to change, and forms the core ecosystem contract.
*   **Data on the Inside**: Data that a service owns, controls, and manipulates locally. It is mutable and completely under the control of a single team.
*   **Replayable Log**: An event store (like Apache Kafka) that acts as part messaging system and part database, retaining historical data while providing asynchronous decoupling.
*   **Fitness Functions**: Metrics or triggers used in evolutionary architecture to determine when an existing architectural approach has become a constraint and must be evolved.

# @Objectives
*   Prioritize team autonomy and independent evolvability of organization, software, and data when designing systems at company scales.
*   Resolve the tension between code reuse (which increases dependencies) and operational independence.
*   Break the "Data Dichotomy" by refusing to hide core business data behind rigid service encapsulation, instead exposing it via replayable event streams.
*   Eliminate tight point-to-point couplings, shared databases, and ephemeral messaging as the primary methods for inter-service data sharing.
*   Establish "Data on the Outside" as a first-class architectural citizen, utilizing replayable logs to serve as a shared source of truth.

# @Guidelines

*   **Organizational and Architectural Alignment**
    *   The AI MUST evaluate architectural recommendations against their impact on team autonomy. If a proposed design requires lock-step deployments or coordinated schema changes across multiple teams, the AI MUST reject it and propose an asynchronous, decoupled alternative.
    *   The AI MUST NOT prescribe "shared nothing" microservices communicating solely via REST/RPC if the services require broad access to shared core business datasets.

*   **Handling Reuse and Encapsulation**
    *   The AI MUST restrict strict encapsulation (e.g., hiding data behind a rigid API) to strictly bounded, single-purpose utilities (e.g., Single Sign-On, logging).
    *   When dealing with core business domain entities (e.g., Orders, Customers), the AI MUST NOT encapsulate the data behind a service interface that forces other teams to query it synchronously.
    *   The AI MUST warn the user that sharing code/libraries increases coupling. If a shared library dictates cross-domain business logic, the AI MUST recommend duplicating the logic or extracting it into a decoupled service.

*   **Resolving the Data Dichotomy**
    *   When a service relies heavily on data owned by another service, the AI MUST NOT recommend a REST API for data retrieval. Instead, the AI MUST recommend replicating the data asynchronously using a replayable log.
    *   The AI MUST identify and dismantle "God Services." If a service provides complex, declarative, database-like querying capabilities over its API, the AI MUST recommend replacing the API with an event stream that downstream services can consume.

*   **Preventing the REST-to-ETL Problem**
    *   The AI MUST explicitly prohibit polling mechanisms where one service periodically calls another service's HTTP/RPC API to maintain a local cache or database.
    *   When bulk data movement is required for offline use, geographical proximity, or operational stability, the AI MUST dictate the use of a replayable log to push data to the consumer.

*   **Managing Data on the Outside vs. Inside**
    *   The AI MUST design system interactions such that "Data on the Outside" is published as immutable events.
    *   The AI MUST ensure that downstream consumers read "Data on the Outside" and immediately convert it to "Data on the Inside" (local state/storage) before manipulating, enriching, or querying it.
    *   The AI MUST NOT use traditional message brokers (which delete messages after consumption) for sharing core datasets, as they lack the historical reference needed to bootstrap new applications.
    *   The AI MUST NOT use shared databases for inter-service communication, as they concentrate use cases into a single tightly coupled point.

*   **Evolutionary Architecture**
    *   The AI MUST allow for architectural evolution. If a user is starting a small project, the AI MUST permit a monolithic approach.
    *   If the user indicates that an existing monolithic or synchronous microservice architecture is becoming a constraint (e.g., team coordination delays, 3 a.m. cascading outages), the AI MUST trigger the transition to an event-streaming architecture.

# @Workflow

When tasked with designing, reviewing, or refactoring how data is shared across services or organizational boundaries, the AI MUST follow this rigid algorithmic process:

1.  **Dependency and Autonomy Audit**:
    *   Identify all services involved and the teams that own them.
    *   Map the synchronous calls (REST/RPC) between them.
    *   Identify any shared databases or shared domain libraries.
2.  **Identify the Data Dichotomy**:
    *   Locate core business datasets (e.g., Orders, Customers, Product Catalog) currently hidden behind service APIs.
    *   Check for the "God Service" anti-pattern: Is one service exposing a massive, complex querying API to satisfy multiple downstream teams?
    *   Check for the "REST-to-ETL" anti-pattern: Are downstream services polling/scraping APIs to build local caches?
3.  **Define Data on the Outside**:
    *   For every tightly coupled data retrieval path identified in Step 2, define an immutable event stream (e.g., `OrderCreated`, `CustomerUpdated`).
    *   Specify a Replayable Log (e.g., Apache Kafka) to hold these events long-term, forming the shared source of truth.
4.  **Design Localized Data on the Inside**:
    *   For each consuming service, design a local datastore or event-sourced view.
    *   Route the Replayable Log events into this local datastore.
    *   Instruct the consuming service to execute its queries strictly against its local "Data on the Inside."
5.  **Apply Evolutionary Triggers**:
    *   Define the fitness functions that prove the new design works (e.g., "Service B can deploy and query data even if Service A is down").
    *   Ensure the implementation allows for teams to regenerate their local data from the Replayable Log's history.

# @Examples (Do's and Don'ts)

### Principle: Avoiding the God Service and Data Encapsulation
*   **[DON'T]** Build a central `OrderService` that exposes endpoints like `GET /orders?customerId=123`, `GET /orders?status=shipped`, and `GET /orders?date>X` to satisfy every other department's querying needs.
*   **[DO]** Build an `OrderService` that publishes an immutable `OrderStateChanged` event to a replayable log. Allow the Shipping Department and Customer Success Department to consume this log and build their own local databases optimized for their specific querying needs.

### Principle: Solving the REST-to-ETL Anti-Pattern
*   **[DON'T]** Write a cron job in the `AnalyticsService` that calls `GET /users/all` on the `UserService` every night at 2:00 AM, transforms the JSON, and loads it into a local data warehouse.
*   **[DO]** Configure the `UserService` to stream `UserCreated` and `UserUpdated` events to a Kafka topic. Have the `AnalyticsService` continuously consume this topic to maintain a real-time, perfectly synced local data warehouse without ever querying the `UserService` directly.

### Principle: Data on the Outside vs. Data on the Inside
*   **[DON'T]** Allow `Service B` to directly mutate a database table owned by `Service A` because "they both need to update the customer's address."
*   **[DO]** Treat the customer's address update as an immutable event ("Data on the Outside"). `Service A` publishes `AddressUpdated`. `Service B` consumes it and updates its own isolated local representation of the customer ("Data on the Inside") to use for its own internal operations.

### Principle: Choosing the Right Data Sharing Infrastructure
*   **[DON'T]** Use RabbitMQ, ActiveMQ, or an Enterprise Service Bus (ESB) to distribute the company's core product catalog, because when a newly built service spins up six months later, the historical catalog data will have already been deleted from the queue.
*   **[DO]** Use Apache Kafka (or an equivalent replayable log) with infinite or long-term retention so that any new service can connect, rewind to offset 0, and replay the entire history of the product catalog to bootstrap its local state.