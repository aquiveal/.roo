# @Domain
These rules MUST be triggered whenever the AI is tasked with:
- Designing, refactoring, or reviewing distributed systems and microservice architectures.
- Defining service boundaries, API contracts, or inter-process communication protocols.
- Migrating or decomposing existing monolithic applications into finer-grained services.
- Configuring databases, logging, monitoring, or deployment topologies for distributed services.
- Advising on organizational structures, repository layouts, or team topologies related to software architecture.
- Evaluating the trade-offs of architectural patterns (e.g., monoliths vs. microservices).

# @Vocabulary
- **Microservice**: An independently releasable service modeled around a business domain that encapsulates state and behavior, exposing functionality via networked endpoints.
- **Information Hiding**: Hiding internal implementation details (e.g., database schemas, language choices) inside a component and exposing as little as possible via external, stable interfaces.
- **Hexagonal Architecture**: A design pattern that keeps internal implementation strictly separate from external interfaces, allowing interaction over different types of interfaces.
- **Independent Deployability**: The defining characteristic of a microservice; the ability to make a change, deploy it, and release it without requiring any other service to be deployed or updated in lockstep.
- **Service-Oriented Architecture (SOA)**: An approach where multiple services collaborate over a network to provide capabilities. Microservices are a specific, opinionated execution of SOA.
- **Domain-Driven Design (DDD)**: Modeling software explicitly around the real-world business domain it operates in, prioritizing high cohesion of business functionality.
- **Conway’s Law**: The principle that organizations design systems that mirror their own communication structures.
- **Stream-Aligned Team**: A poly-skilled team aligned to a single, valuable stream of work with end-to-end responsibility (UI, logic, and data) for customer-facing functionality.
- **Delivery Contention**: The friction and delays caused when multiple developers or teams attempt to change the same codebase, deploy at the same time, or navigate confused lines of ownership.
- **Single-Process Monolith**: A system where all code is deployed as a single operating system process.
- **Modular Monolith**: A single-process monolith divided into strict, independent modules, though usually still sharing a single database.
- **Distributed Monolith**: An anti-pattern consisting of multiple services that are so tightly coupled they must be deployed together.
- **Bulkhead**: An architectural isolation mechanism (like watertight compartments in a ship) ensuring that a failure in one component does not cascade to others.
- **Correlation ID**: A unique identifier injected into a related chain of network calls to enable tracing a single transaction across multiple microservices and log files.
- **Saga**: A pattern used to manage state changes across multiple microservices without using distributed database transactions.
- **Eventual Consistency**: A data consistency model used in distributed systems where state updates propagate across services over time, rather than atomically.
- **Function as a Service (FaaS) / Serverless**: Cloud deployment models that abstract away underlying machines, allowing code to be deployed and scaled on demand.

# @Objectives
- **Prioritize Independent Deployability**: The AI MUST ensure that any proposed microservice architecture allows teams to deploy and release changes in total isolation from other services.
- **Enforce Business Domain Slicing**: The AI MUST organize systems into end-to-end vertical slices of business functionality, rejecting horizontal technological layering.
- **Guarantee Information Hiding**: The AI MUST completely hide the internal state, technology stack, and database of every microservice behind stable networked contracts.
- **Prevent Distributed Monoliths**: The AI MUST aggressively identify and eliminate tight coupling, shared databases, and lockstep deployment requirements.
- **Mitigate Distributed System Complexity**: The AI MUST proactively introduce patterns for observability, failure isolation, and asynchronous workflows to handle the inherent chaos of networks.
- **Ensure Context-Aware Adoption**: The AI MUST critically evaluate if microservices are actually justified, pushing back on microservice adoption for early-stage startups, rapidly changing domains, or teams lacking operational automation.

# @Guidelines

## Architectural Boundaries & Design
- The AI MUST define microservice boundaries based on business domains (e.g., "Customer Profile", "Inventory"), NOT technical functions (e.g., "Presentation", "Database Layer").
- The AI MUST prioritize high cohesion of business functionality over high cohesion of technical functionality.
- The AI MUST treat the size of a microservice (e.g., lines of code) as irrelevant. The AI MUST focus instead on minimizing the size of the external interface and ensuring the service fits in the developers' heads.
- The AI MUST NOT use three-tiered horizontal architectures (UI team, Backend team, DBA team) when designing microservice topologies.
- The AI MUST enforce the Hexagonal Architecture pattern, ensuring business logic is never tightly coupled to the transport protocol or database driver.
- The AI MUST ensure that changes to a microservice's internal implementation do not cause backward-incompatible changes to its external network contract.

## Data & State Management
- The AI MUST explicitly forbid the use of shared databases between microservices.
- If Microservice A requires data owned by Microservice B, the AI MUST route the request through Microservice B's networked API. Microservice A MUST NEVER query Microservice B's database directly.
- The AI MUST encapsulate the database within the microservice boundary.
- The AI MUST NOT use or recommend distributed ACID transactions across microservices.
- To manage cross-service business processes, the AI MUST recommend the Saga pattern and eventual consistency models.
- For cross-service reporting requirements, the AI MUST recommend data pumping/streaming to a dedicated reporting database or data lake, rather than joining across live microservice databases.

## Integration & Communication
- The AI MUST treat the network as unreliable. All inter-process communication designs MUST account for latency, packet loss, and service failure.
- The AI MUST recommend stable, technology-agnostic communication protocols (e.g., REST, GraphQL, asynchronous event queues).
- The AI MUST design services to be tolerant of failure in downstream dependencies, implementing Bulkheads to prevent cascading failures.
- The AI MUST balance the payload size and serialization/deserialization latency when designing inter-process communications.

## Observability & Operations
- The AI MUST mandate Log Aggregation as a prerequisite for any microservice architecture.
- The AI MUST inject a Correlation ID into every inter-service request and log output to trace workflows across the distributed system.
- The AI MUST recommend incremental adoption of operational technology. Do not introduce Kubernetes or container orchestration until the overhead of managing the services manually justifies it.
- The AI MUST recommend isolated execution environments (e.g., Containers) to ensure one misbehaving microservice does not consume all host resources (CPU/Memory).
- The AI MUST treat security as a layered defense (defense in depth), acknowledging that microservices increase the attack surface area but allow for stricter component-level firewalls.

## Testing & Quality Assurance
- The AI MUST warn against heavy reliance on end-to-end (E2E) testing across multiple microservices due to brittleness and false negatives.
- The AI MUST prioritize consumer-driven contract testing and in-production testing (e.g., canary releases, parallel runs) over massive E2E test suites.

## Organizational Alignment
- The AI MUST align architectural proposals with Conway's Law, ensuring the architecture maps to the communication structures of the organization (Stream-aligned teams).
- The AI MUST design architectures that minimize the need for cross-team coordination when rolling out a new feature.

# @Workflow
When tasked with designing, evaluating, or migrating to a microservice architecture, the AI MUST execute the following algorithm:

1. **Context & Justification Assessment**
   - Evaluate the user's context. Is this a startup searching for product-market fit? If yes, strongly advise a Modular Monolith instead.
   - Determine the specific problem being solved (e.g., delivery contention, need for independent scaling, technology heterogeneity).
   - If the goal is purely cost reduction, advise against microservices.

2. **Domain Modeling & Boundary Definition**
   - Identify the core business domains.
   - Slice the system vertically by business capability (e.g., end-to-end Order Management).
   - Ensure the UI, logic, and data for that capability are logically grouped together.

3. **Data Encapsulation Strategy**
   - Assign discrete databases or schemas to each identified boundary.
   - Identify data dependencies between boundaries and define network APIs (synchronous or asynchronous) to facilitate data sharing.
   - explicitly document that no database sharing is permitted.

4. **Integration & Workflow Design**
   - Define the communication styles between services (e.g., Request-Response for queries, Event-Driven for state updates).
   - Design Sagas for workflows that span multiple domains.
   - Inject Correlation IDs into all network boundaries.

5. **Operational Readiness Check**
   - Define the logging and monitoring strategy (Log Aggregation).
   - Define the deployment topology, ensuring isolated execution (e.g., separate containers) to provide Bulkheads.

6. **Evolutionary Migration Plan (If Applicable)**
   - If migrating from a monolith, define an incremental strategy ("turning the dial").
   - Extract one low-risk business domain first. Establish the operational pipelines, routing, and database separation for that single service before proceeding.

# @Examples (Do's and Don'ts)

## Domain Slicing
- **[DO]**: Structure architecture as: `Team A owns [Customer UI -> Customer API -> Customer DB]`. `Team B owns [Order UI -> Order API -> Order DB]`.
- **[DON'T]**: Structure architecture as: `UI Team owns [Web Frontend]`. `Backend Team owns [Customer API, Order API]`. `DBA Team owns [Shared SQL DB]`.

## Data Management
- **[DO]**: "The Order Service needs to know the customer's shipping address. It will make an HTTP GET request to the Customer Service API to retrieve it."
- **[DON'T]**: "The Order Service needs the customer's shipping address. It will run a SQL JOIN on the `Orders` table and the `Customers` table in the centralized database."

## Inter-Service Workflows
- **[DO]**: "To process an order, the Order Service emits an 'Order Created' event. The Inventory Service listens, updates its local DB, and emits an 'Inventory Reserved' event. If inventory fails, it emits an 'Out of Stock' event, triggering the Order Service to execute a compensating action (Saga)."
- **[DON'T]**: "To process an order, the Order Service initiates a distributed Two-Phase Commit (2PC) locking the Order database row and the Inventory database row until the transaction completes."

## Observability
- **[DO]**: "Include a `X-Correlation-ID` header in the API Gateway. Every microservice must log this ID and pass it as a header in any subsequent downstream network calls."
- **[DON'T]**: "Write logs locally to each container's file system and rely on SSHing into individual machines to troubleshoot failures."

## Testing
- **[DO]**: "Validate the microservice using consumer-driven contracts to ensure its API changes do not break downstream consumers, and utilize Canary releases to test in production."
- **[DON'T]**: "Require a dedicated staging environment where all 50 microservices must be deployed simultaneously to run a 6-hour Selenium end-to-end test suite before approving a deployment."