# @Domain
Trigger these rules when the user requests the design, evaluation, refactoring, or implementation of a Microservices Architecture, distributed systems decoupled by domain, bounded contexts, microfrontends, or decentralized service communication topologies.

# @Vocabulary
*   **Microservice**: A highly decoupled, single-purpose service running in its own process (often in a virtual machine or container) that physically models a logical bounded context.
*   **Bounded Context**: A concept from Domain-Driven Design (DDD) where a domain or workflow contains everything it needs to operate independently (classes, subcomponents, database schemas) without coupling to external entities.
*   **Domain-Partitioned Architecture**: An architecture structured around business workflows and domains rather than technical capabilities (like presentation or persistence layers).
*   **Entity Trap**: An anti-pattern where services are modeled to resemble simple, single entities in a database (e.g., creating a Customer service that just does CRUD operations on a Customer table) rather than capturing a full business workflow.
*   **Sidecar Pattern**: A component attached to each service that handles operational concerns (monitoring, logging, circuit breakers) to separate domain logic from operational coupling.
*   **Service Mesh**: A holistic operational network connecting the sidecar components across all microservices to form a consistent, unified control plane.
*   **Service Discovery**: A mechanism (often within the service mesh or API layer) used to monitor, find, and dynamically spin up service instances to handle scale and elasticity.
*   **Microfrontends**: A frontend design pattern where UI components are isolated and aligned with specific backend microservice boundaries, emitting synchronous levels of granularity.
*   **Protocol-Aware Heterogeneous Interoperability**: The communication standard in microservices where services know how to call each other (protocol-aware) across polyglot tech stacks (heterogeneous) via the network (interoperability).
*   **Enforced Heterogeneity**: Mandating different technology stacks for different services to physically prevent developers from accidentally sharing classes and creating coupling points.
*   **Choreography**: A decentralized communication style where services call each other directly as needed (often via events) without a central mediator.
*   **Front Controller Pattern**: A specific choreography scenario where the first service called coordinates across a wide variety of other services, acting as a localized mediator.
*   **Orchestration**: A centralized communication style where a localized mediator service is explicitly created to coordinate a complex business process across multiple services.
*   **Saga Pattern**: A distributed transaction pattern where a mediator coordinates a workflow across services and issues compensating (undo) requests if any part of the transaction fails.
*   **Compensating Transaction Framework**: The specific implementation within a Saga pattern that executes "undo" operations to reverse successful steps if a subsequent step fails.

# @Objectives
*   Achieve extreme decoupling at both the domain and operational levels.
*   Favor duplication over reuse/coupling to ensure services can evolve and deploy entirely independently.
*   Isolate data completely; no single source of truth across shared databases.
*   Maximize scalability, elasticity, testability, and evolutionary deployment capabilities.
*   Address the negative trade-offs of distributed systems (network latency, security verification overhead, data consistency) through deliberate granularity and communication design.

# @Guidelines
*   **Service Granularity Boundaries**: You MUST iterate on service boundaries using three criteria:
    1.  **Purpose**: Ensure the service is highly functionally cohesive, contributing one significant workflow/behavior. Avoid the Entity Trap.
    2.  **Transactions**: Boundary lines MUST encapsulate transactions. Do not split entities that require ACID transactions across different services.
    3.  **Choreography Overhead**: If multiple services require extensive, constant communication to function, you MUST bundle them back into a larger single service to avoid network overhead.
*   **Data Isolation**: Every microservice MUST own its own database/schema. You MUST NOT use databases as integration points. You MUST select the most appropriate database type (relational, NoSQL, graph) specifically tailored to the individual service's needs.
*   **Cross-Service Data Synchronization**: Since a single relational database cannot unify values, you MUST handle shared facts by either identifying one domain as the source of truth and coordinating via network calls, or by using asynchronous database replication/caching.
*   **API Layer Usage**: You MAY use an API layer (API Gateway) for proxying, service discovery, or security checks. You MUST NOT place business logic, orchestration, or mediation inside the API layer.
*   **Operational Reuse**: You MUST split operational concerns from domain logic. Implement monitoring, logging, and circuit breakers using the Sidecar pattern. Connect these sidecars via a Service Mesh to provide unified operational control.
*   **Frontend Integration**: You MUST choose between a Monolithic Frontend (connecting via the API layer) or Microfrontends. If using Microfrontends, isolate UI components to match backend service boundaries so a single team owns the entire vertical slice.
*   **Inter-Service Communication**: You MUST default to asynchronous Choreography to preserve the highly decoupled philosophy. You MAY use Orchestration (a localized mediator service) ONLY when a business workflow is inherently complex and requires explicit coordination.
*   **Polyglot Environments**: You SHOULD encourage or enforce heterogeneity. Do not force a single enterprise technology stack on all services; choose the right scale tool for the narrow scope of the problem.
*   **Transactions (CRITICAL RULE)**: You MUST NOT execute distributed transactions across microservices. If an atomic transaction is required, you MUST fix the service granularity by merging the components. If merging is absolutely impossible due to vastly different architectural characteristics, you MUST implement the Saga pattern with a Compensating Transaction Framework (do/undo operations).

# @Workflow
1.  **Domain Decomposition**: Analyze the business requirements using Domain-Driven Design (DDD). Identify the bounded contexts representing distinct business workflows (not just database entities).
2.  **Granularity Assessment**: Evaluate the proposed services. Merge services if they share a transaction boundary or if their separation causes excessive inter-service communication (choreography overhead).
3.  **Data Architecture Definition**: Assign a dedicated datastore to each validated microservice. Define how data will be replicated or cached if multiple services need to read the same information.
4.  **Operational Infrastructure Design**: Attach a sidecar to each microservice for logging, monitoring, and security. Map out the service mesh and configure service discovery.
5.  **API and Frontend Mapping**: Define the API Gateway strictly as a proxy/routing layer. Design the UI strategy (Monolithic Frontend vs. Microfrontends) and wire it to the respective services/API layer.
6.  **Communication Strategy Selection**: Map the workflows between services. Apply Choreography (events/messages) for standard decoupled communication. Apply localized Orchestration (creating a specific mediator service) only for complex, multi-step business coordination.
7.  **Transaction Resolution**: Scan the architecture for any operations requiring atomic cross-service updates. Eliminate them by refactoring service boundaries. If unresolvable, define the exact do/undo states for a Saga pattern implementation.

# @Examples (Do's and Don'ts)

### Bounded Context & Reuse
*   **[DO]**: Duplicate a class definition (e.g., `Address`) in both the `Shipping` service and the `Billing` service so they can evolve independently.
*   **[DON'T]**: Create a shared `CommonUtils.jar` or `EnterpriseDomain.dll` containing the `Address` class that both services must import, thereby coupling their deployment and evolution.

### Data Isolation
*   **[DO]**: Give the `Catalog` service a NoSQL document store for product descriptions, and give the `Payment` service a highly structured Relational DB, with no shared access.
*   **[DON'T]**: Create a massive `EnterpriseDB` and allow both the `Catalog` service and `Payment` service to query the `Customers` table directly.

### API Layer
*   **[DO]**: Configure the API layer to route `/api/orders` to the Order Service, and execute authentication token validation before routing.
*   **[DON'T]**: Program the API layer to receive an order request, call the Inventory service, evaluate the response, and then call the Billing service. (This violates bounded context by putting domain orchestration in the API layer).

### Granularity & The Entity Trap
*   **[DO]**: Create a `CatalogCheckout` service that handles the workflow of processing a cart, verifying basic stock, and initiating the checkout sequence.
*   **[DON'T]**: Create a `Cart` service, a `CartItem` service, and a `CartTotal` service simply because those are three tables in the database.

### Distributed Transactions
*   **[DO]**: Redesign service boundaries so that `OrderPlacement` and `InventoryReservation` are handled within the same service if they strictly require absolute real-time ACID consistency.
*   **[DON'T]**: Use two-phase commits (2PC) over the network to lock the `Order` database and the `Inventory` database simultaneously.

### The Saga Pattern
*   **[DO]**: Create an `AuctionSession` mediator service that calls `Payment`. If `Payment` fails, the `AuctionSession` service sends an explicit "Undo/Cancel" message to the `Fulfillment` service to reverse the previous packing request.
*   **[DON'T]**: Leave the system in a pending, inconsistent state where the order is packed by `Fulfillment` but `Payment` has failed, with no compensating transaction to revert the packed status.