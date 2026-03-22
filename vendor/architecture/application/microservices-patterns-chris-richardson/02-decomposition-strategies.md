# @Domain
These rules MUST trigger whenever the AI is tasked with software architecture design, application decomposition, migrating a monolithic application to a microservice architecture, defining service boundaries, identifying system operations, or refactoring large, tangled dependencies (e.g., "god classes").

# @Vocabulary
- **Software Architecture**: The high-level structure of a system consisting of software elements, relations among them, and properties of both, which dictates the system's quality attributes (-ilities).
- **4+1 View Model**: A framework for describing architecture using four views (Logical, Implementation, Process, Deployment) animated by a set of Scenarios.
- **Hexagonal Architecture**: An architectural style (Ports and Adapters) that places business logic at the center, decoupled from presentation and data access logic. Inbound adapters invoke the business logic via inbound ports; business logic invokes external systems via outbound ports and adapters.
- **Monolithic Architecture**: An architectural style that structures the implementation view as a single deployable or executable component.
- **Microservice Architecture**: An architectural style that functionally decomposes the implementation view into a set of loosely coupled, independently deployable services.
- **Service**: A standalone, independently deployable software component that implements narrowly focused functionality and exposes an API encapsulating its internal implementation.
- **Loose Coupling**: A design constraint where services interact strictly via APIs and maintain private databases, ensuring implementation details and state remain isolated.
- **System Operation**: An abstraction of a request the application must handle, categorized as either a Command (updates data) or a Query (retrieves data).
- **Business Capability**: A concept from business architecture defining what a business does to generate value (e.g., "Order Management").
- **Subdomain**: A concept from Domain-Driven Design (DDD) representing a specific part of the overall application problem space.
- **Bounded Context**: A DDD concept representing the explicit scope (boundary) of a domain model, mapping directly to a service or set of services in a microservice architecture.
- **God Class**: A bloated, centralized class that bundles state and behavior for many disparate aspects of an application, acting as a massive obstacle to decomposition.
- **Distributed Monolith**: An anti-pattern resulting from incorrect decomposition where tightly coupled services must be deployed together.
- **SRP (Single Responsibility Principle)**: A principle stating that a software element (class or service) should have only one reason to change.
- **CCP (Common Closure Principle)**: A principle stating that components changing for the same reason should be packaged in the same service.

# @Objectives
- Architect systems to optimize for development-time quality attributes: maintainability, testability, and deployability.
- Decompose applications around business concepts (capabilities or subdomains) rather than technical layers.
- Enforce strict boundaries, ensuring services are autonomous, loosely coupled, and independently scalable.
- Untangle monolithic data models by eliminating global domain models and God Classes in favor of service-specific bounded contexts.
- Abstract and define application behavior as technology-agnostic system operations before committing to specific IPC (Inter-Process Communication) protocols.

# @Guidelines
- **Architectural Views**: The AI MUST evaluate and document architectures using the 4+1 View Model dimensions (Logical, Implementation, Process, Deployment).
- **Service Design**: The AI MUST enforce Hexagonal Architecture for individual services. Business logic MUST NOT depend on adapters (e.g., UI or Database logic); adapters MUST depend on the business logic via ports.
- **Database Encapsulation**: The AI MUST assign a strictly private datastore to each service. Services MUST NEVER directly read or write to another service's database.
- **Shared Libraries Constraint**: The AI MUST restrict the use of shared libraries to functionality that is highly unlikely to change (e.g., a generic `Money` class). The AI MUST NEVER put business concepts (e.g., an `Order` object) in a shared library to avoid coupled redeployments.
- **Service Sizing**: The AI MUST NOT use line-of-code metrics to size a service. The AI MUST size services based on team autonomy, minimizing lead time, and minimizing required cross-team collaboration.
- **Decomposition Strategies**: When decomposing a system, the AI MUST use either the **Decompose by business capability** pattern or the **Decompose by subdomain (DDD)** pattern.
- **Decomposition Principles**: 
  - Apply **SRP** to ensure a service has only one reason to change.
  - Apply **CCP** to group functionalities that change for the same underlying business rule into the same service to avoid distributed monoliths.
- **Handling Decomposition Obstacles**:
  - *Network Latency*: If decomposition introduces excessive round-trips, the AI MUST propose implementing batch APIs or combining the overly chatty services.
  - *Synchronous IPC & Availability*: The AI MUST prioritize asynchronous messaging or self-contained services (via CQRS data replication) to avoid availability drops caused by synchronous service-to-service calls.
  - *Data Consistency*: The AI MUST explicitly prohibit Distributed Transactions (2PC/XA). The AI MUST use the **Saga pattern** (a sequence of local transactions coordinated via asynchronous messaging) for transactions spanning multiple services.
  - *God Classes*: The AI MUST eliminate God Classes by explicitly rejecting a single, unified enterprise data model. The AI MUST define a separate, simplified version of the entity for each service's Bounded Context.

# @Workflow
When tasked with defining a microservice architecture or decomposing an application, the AI MUST strictly follow this 3-step algorithm:

1. **Identify System Operations**
   - Extract nouns from requirements to sketch a high-level, abstract domain model.
   - Extract verbs from requirements to define System Operations.
   - Classify each operation as a Command (updates data) or a Query (reads data).
   - Document the specification for each Command, defining its parameters, return values, preconditions, and post-conditions in terms of the high-level domain model.

2. **Define Services via Decomposition**
   - Apply a decomposition strategy: map the domain to either Business Capabilities or DDD Subdomains.
   - Group the identified capabilities/subdomains into distinct, proposed services.
   - Refine the boundaries by applying the Single Responsibility Principle (SRP) and Common Closure Principle (CCP).

3. **Resolve Obstacles and Define Service APIs**
   - Analyze the proposed services for God Classes. If found, split the God Class into smaller, context-specific classes tailored to each service (e.g., `Order` becomes `Delivery` in Delivery Service, `Ticket` in Kitchen Service).
   - Assign each system operation identified in Step 1 to a specific service as its initial entry point.
   - Determine collaboration requirements: if a system operation requires data/actions from multiple services, define the specific cross-service APIs required (e.g., asynchronous events, REST calls, or Saga participants).
   - Map out Saga requirements for any operations that update data across multiple services.

# @Examples (Do's and Don'ts)

### Loose Coupling & Databases
- **[DON'T]** Point multiple services to a shared global database schema to save time.
- **[DO]** Assign a private database or schema to each service and require services to communicate solely via APIs or asynchronous events.

### Shared Libraries
- **[DON'T]** Create a `common-business-models.jar` containing the `Order`, `User`, and `Product` classes and share it across all services to reduce code duplication.
- **[DO]** Create a `common-utils.jar` for generic, stable elements like currency calculations (`Money`), and duplicate necessary business class representations inside the specific services that need them.

### Eliminating God Classes
- **[DON'T]** Build a monolithic `Order` class containing payment details, delivery schedules, and kitchen prep times, passing it entirely between services.
- **[DO]** Define multiple domain models based on Bounded Contexts: an `Order` class in Order Service (handling billing/approval), a `Ticket` class in Kitchen Service (handling prep times), and a `Delivery` class in Delivery Service (handling routing/pickup).

### Service Architecture
- **[DON'T]** Build layered microservices where the business logic layer depends directly on SQL database DAOs.
- **[DO]** Use Hexagonal Architecture within each microservice, defining repository interfaces (ports) in the business logic layer and implementing them in the surrounding infrastructure adapters.

### Data Consistency
- **[DON'T]** Use `BEGIN TRANSACTION`, update Service A's DB, invoke Service B synchronously, update Service B's DB, and `COMMIT` using two-phase commit.
- **[DO]** Implement the Saga pattern: Service A updates its private database and publishes an asynchronous event; Service B listens for the event and updates its database in a separate local transaction.