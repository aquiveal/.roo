@Domain
These rules MUST trigger when the AI is tasked with designing, refactoring, evaluating, or implementing system architectures, microservices, distributed systems, inter-service communication layers, domain-driven design models, or data access patterns.

@Vocabulary
- **Domain**: The problem space that a business occupies and provides solutions to, existing regardless of the business itself.
- **Subdomain**: A granular component of the main domain reflecting specific business responsibilities (e.g., Sales, Engineering).
- **Domain Model**: An abstraction of the domain used as a construct to solve business problems, highlighting the most important pieces of the domain.
- **Bounded Context**: The logical boundaries (inputs, outputs, events, requirements, processes, data models) relevant to a subdomain.
- **Business Communication Structure**: The hierarchical organization of teams, departments, and people driven by business requirements.
- **Implementation Communication Structure**: The data and logic pertaining to the subdomain model (e.g., the application code, monolith databases).
- **Data Communication Structure**: The formalized process through which data is communicated across the business and between implementations.
- **Conway's Law**: The principle that organizations design systems mirroring their own communication structures.
- **Event-Driven Microservices (EDM)**: Small, purpose-built, highly cohesive applications built to fulfill a specific bounded context that communicate exclusively by asynchronously issuing and consuming events.
- **Event Stream**: A continuous, canonical narrative detailing everything that has happened in an organization, serving as the Data Communication Structure.
- **Single Source of Truth**: The definitive, immutable record of statements of fact maintained within event streams.
- **Synchronous Microservices**: Services that communicate directly via request-response APIs, creating point-to-point couplings.
- **Distributed Monolith**: An anti-pattern created when microservices act tightly coupled through intertwining synchronous calls, blurring bounded contexts.

@Objectives
- The AI MUST design architectures that fully decouple the production and ownership of data from the access and consumption of that data.
- The AI MUST align service boundaries exclusively around business requirements, completely avoiding alignment based on technical requirements or layers.
- The AI MUST establish Event Streams as the organization's single source of truth and primary Data Communication Structure.
- The AI MUST ensure that downstream consumer services take sole responsibility for their own data modeling, querying, and state materialization.
- The AI MUST eliminate synchronous point-to-point data fetching between internal microservices, preventing the creation of distributed monoliths.

@Guidelines
- **Alignment on Business Contexts**: When defining microservices, the AI MUST align them to business subdomains (e.g., Billing, Inventory) and MUST NEVER align them to technological layers (e.g., Database Service, Frontend API Service). A single team/service MUST own the complete vertical slice from application code to its local database layer.
- **High Cohesion and Loose Coupling**: The AI MUST design bounded contexts so that internal operations are intensive and closely related (high cohesion), while connections between different contexts are minimal and asynchronous (loose coupling).
- **Event-Based Inter-Service Communication**: When Service A requires data owned by Service B, the AI MUST NOT design a request-response API for Service A to query Service B. Instead, the AI MUST require Service B to continuously publish state changes as events to an Event Stream, which Service A consumes asynchronously.
- **Shift Querying to the Consumer**: The AI MUST NOT implement complex cross-domain query APIs on the producer side. The AI MUST instruct the consumer service to ingest necessary events, create its own local state/models, and perform its own querying locally.
- **Mitigating Conway's Law**: The AI MUST recognize that traditional Implementation Communication Structures restrict data access. To prevent scope creep of existing monoliths, the AI MUST mandate a formalized Data Communication Structure (Event Streams) to share domain data openly across team boundaries.
- **Avoiding Stale Data Copies**: The AI MUST NOT use batch-based database replication or ad-hoc scheduled queries to copy data between services. State sharing MUST occur in near-real-time via continuous event consumption.
- **Synchronous Microservice Restrictions**: The AI MUST aggressively limit the use of synchronous point-to-point microservices. Synchronous calls MUST only be implemented for specific exceptions: authenticating users, integrating with external/third-party APIs, or serving UI/mobile client requests.
- **Preventing Distributed Monoliths**: When refactoring monoliths, the AI MUST NOT simply replace in-memory function calls with synchronous remote procedure calls (REST/gRPC) over the network. The AI MUST fundamentally redesign the communication to be asynchronous and event-driven.
- **Microservice Sizing**: The AI MUST size microservices such that they fulfill exactly one granular bounded context, typically small enough to be conceptually held within a single developer's head or written within two weeks.
- **Testability**: The AI MUST leverage the decoupled nature of EDMs to design unit and integration tests that mock the input/output event streams rather than spinning up elaborate, cascading dependency graphs of synchronous services.

@Workflow
1. **Domain Decomposition**: Analyze the overarching business problem space. Decompose the domain into granular, actionable subdomains (e.g., Ordering, Shipping, Customer Support).
2. **Bounded Context Definition**: For each subdomain, establish strict bounded contexts. Define the exact inputs, outputs, and internal business logic. Ensure no technical cross-cutting layers exist.
3. **Data Communication Layer Design**: Identify domain data that needs to be shared across bounded contexts. Define immutable Event Streams to carry this data. Establish these streams as the Single Source of Truth.
4. **Producer Implementation**: Design the producer microservice to encapsulate its internal operations. Upon any state change, the producer MUST emit a statement-of-fact event to the assigned Event Stream. The producer MUST NOT provide querying endpoints for other services.
5. **Consumer Implementation**: Design consumer microservices to subscribe to the necessary Event Streams. The consumer MUST ingest events, materialize the state into its own localized database/model, and perform all queries against this local state.
6. **Validation against Anti-Patterns**: Review the topology. If any service relies on a synchronous network call to retrieve internal domain data from another service, remove the point-to-point connection and replace it with an Event Stream dependency.

@Examples (Do's and Don'ts)

**Principle: Aligning Bounded Contexts with Business Requirements**
- [DO]: Design an `OrderProcessingService` where the team has total, isolated ownership of both the Java application code and the PostgreSQL database storing the orders.
- [DON'T]: Design an `ApplicationLogicService` that handles business rules and makes remote calls to a shared `DatabaseAccessService` owned by a separate DBA team.

**Principle: Event-Driven Data Communication**
- [DO]: When an order is placed, `OrderService` publishes an `OrderCreated` event to the `orders` event stream. The `InventoryService` continuously consumes this stream to decrement its local stock count.
- [DON'T]: When an order is placed, `OrderService` makes a synchronous HTTP POST to `InventoryService` to update the stock. (This creates dependent scaling and failure cascading).

**Principle: Consumers Perform Their Own Modeling**
- [DO]: `ReportingService` subscribes to the `orders` stream, the `shipping` stream, and the `payments` stream. It aggregates this data into a local read-optimized database to serve complex business reports.
- [DON'T]: `ReportingService` issues real-time GraphQL queries to `OrderService`, `ShippingService`, and `PaymentService` to dynamically join data on the fly, overwhelming the implementation communication structures of those services.

**Principle: Single Source of Truth**
- [DO]: All services across the organization agree that the `Customer` event stream is the canonical source of truth for customer states. Any service needing customer data provisions it by replaying the event stream.
- [DON'T]: A team performs a nightly batch SQL dump from the `CustomerService` database into a shared file store, leaving downstream systems operating on stale, unverified, out-of-sync data copies.