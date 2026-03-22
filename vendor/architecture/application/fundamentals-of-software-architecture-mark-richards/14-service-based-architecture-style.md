@Domain
Trigger these rules when the user requests the design, implementation, analysis, or refactoring of a "Service-Based Architecture", a distributed macro-layered architecture, a pragmatic distributed system with coarse-grained domain services, or a system requiring architectural modularity without the high complexity, cost, and orchestration overhead of a fine-grained microservices architecture.

@Vocabulary
*   **Service-Based Architecture**: A pragmatic, distributed architecture style consisting of a separately deployed user interface, a small number (typically 4 to 12) of separately deployed coarse-grained remote domain services, and a monolithic centrally shared database.
*   **Domain Service**: A coarse-grained, independently deployed portion of an application scoped to a specific business domain (e.g., OrderService, CustomerService), typically encompassing multiple related sub-domains.
*   **API Access Facade**: The top layer within a domain service responsible for receiving requests from the user interface and orchestrating the business request internally across the service's underlying business and persistence layers.
*   **Macro Layered Structure**: The overarching topology of a service-based architecture, typically divided into a User Interface tier, a Domain Services tier, and a Database tier.
*   **Federated Shared Libraries**: Domain-scoped custom libraries (e.g., JARs, DLLs) containing database entity objects and SQL code that strictly match logical database partitions, used to prevent global coupling.
*   **ACID Transactions**: Atomicity, Consistency, Isolation, Durability. Traditional database transactions using commits and rollbacks, highly supported in service-based architecture due to coarse-grained service boundaries.
*   **BASE Transactions**: Basic Availability, Soft State, Eventual Consistency. Distributed transactions utilized in microservices, which the AI MUST generally avoid in service-based architecture.
*   **Orchestration**: The coordination of a business process by a central mediator. In service-based architecture, this occurs *internally* within the API Facade of a single service rather than externally across multiple services.
*   **Choreography**: The decentralized coordination of multiple services communicating with one another. Service-based architecture actively minimizes this to avoid complex inter-service dependencies.
*   **Architecture Quantum**: An independently deployable artifact with high functional cohesion and synchronous connascence. Service-based architectures usually consist of a single quantum (due to a shared database), but can have multiple if the UI and databases are federated.

@Objectives
*   **Pragmatism over Purity**: Deliver a highly pragmatic distributed architecture that balances the benefits of microservices (agility, testability, deployability) with the simplicity and lower cost of monolithic architectures.
*   **Optimize Granularity**: Maintain coarse-grained service boundaries to preserve data integrity, enable standard ACID transactions, and eliminate the need for complex inter-service orchestration or choreography.
*   **Mitigate Database Coupling**: Intelligently partition the centrally shared database using logical domains and federated shared libraries to isolate schema changes.
*   **Maximize ACID**: Keep related transactional updates within the boundary of a single domain service to utilize standard database commits and rollbacks.
*   **Prevent Stamp Coupling**: Ensure remote access contracts pass only the exact data required between the UI and services or (rarely) between services.

@Guidelines

*   **Topology Rules**:
    *   The AI MUST structure the architecture into a distributed macro-layered topology: separately deployed UIs, remotely accessed coarse-grained services, and a monolithic database.
    *   The AI MUST target between 4 and 12 domain services for the entire application context. If the design exceeds 12 services, the AI MUST consolidate boundaries to prevent accidental microservices architecture.
    *   The AI MUST allow services to scale independently. Multiple instances of a single service MUST be supported via a load balancer.

*   **Service Internal Design**:
    *   The AI MUST design the internal structure of each domain service using either a layered architecture style (API Facade -> Business Layer -> Persistence Layer) or domain-partitioned sub-domains.
    *   The AI MUST place an API Access Facade at the entry point of every domain service.
    *   The AI MUST instruct the API Access Facade to orchestrate the business request *internally* across the service's internal classes, strictly avoiding external orchestration across multiple remote services.

*   **Transaction and Data Integrity Rules**:
    *   The AI MUST utilize traditional ACID database transactions (commit/rollback) within a single domain service to guarantee data integrity.
    *   The AI MUST NOT use distributed transactional sagas or BASE transactions unless absolutely forced by external system integrations.

*   **Database Partitioning and Shared Libraries**:
    *   The AI MUST default to a single centrally shared monolithic database across all domain services.
    *   The AI MUST NOT create a single, global shared library containing all database entity objects.
    *   The AI MUST logically partition the shared database by domain (e.g., customer, invoicing, order).
    *   The AI MUST create a discrete, federated shared library (e.g., `invoicing_entities_lib`) for each logical database partition. Services MUST only import the shared libraries matching the domains they interact with.
    *   The AI MUST isolate "common" tables into a locked, strictly governed `common_entities_lib` to mitigate the high impact of changing universally shared schemas.

*   **Interservice Communication Constraints**:
    *   The AI MUST heavily restrict interservice communication. Because services share a database, data synchronization or data lookups MUST be done via the database rather than requesting data from another service.
    *   The AI MUST prevent interservice orchestration. Business transactions must complete within a single service boundary.

*   **Topology Variants**:
    *   *UI Federation*: The AI MAY separate the monolithic UI into domain-scoped UIs (e.g., Customer Facing, Internal Admin) to increase fault tolerance, scalability, and security zone isolation.
    *   *Database Federation*: The AI MAY break the monolithic database into domain-scoped databases IF AND ONLY IF the data is completely isolated and no interservice communication is required to join data.
    *   *API Gateway*: The AI SHOULD insert an API Layer (Reverse Proxy/Gateway) between the UI and Domain Services to consolidate cross-cutting concerns (metrics, security, routing, service discovery).

*   **Security and Network Zoning**:
    *   The AI MUST utilize separate network zones for external-facing operations versus internal operations, employing one-way firewall rules or table mirroring to protect internal data stores.

@Workflow
1.  **Analyze and Partition Domains**: Review the business requirements and divide the system into 4 to 12 coarse-grained macro domains (e.g., Order Management, Customer Management, Fulfillment).
2.  **Establish Service Boundaries**: Map each macro domain to a single, independently deployable Domain Service.
3.  **Design the Database Topology**:
    *   Define a centrally shared monolithic database.
    *   Logically partition the database tables according to the macro domains identified in Step 1.
    *   Extract common tables (e.g., users, basic reference data) into a shared logical partition.
4.  **Define Federated Shared Libraries**: Create a specific shared library for each logical database partition to house entity mapping classes and SQL logic. Map these libraries only to the services that strictly require them.
5.  **Design Service Internals**: Inside each service, define an API Access Facade layer to handle remote requests. Underneath the Facade, define the necessary business logic classes and persistence mechanisms.
6.  **Determine Transaction Boundaries**: Verify that all critical database inserts/updates for a given business workflow occur within the boundaries of a single Domain Service using standard ACID commits.
7.  **Select Topology Variants**: Determine if the UI needs to be federated (e.g., separate web apps for consumers vs. administrators) or if an API gateway is required for security/metrics.
8.  **Evaluate Scale/Throughput**: Identify which specific services require multiple instances to handle spikes in load, leaving low-volume services as single instances to conserve infrastructure resources.

@Examples (Do's and Don'ts)

*   **Database Entity Management**
    *   [DO]: Create domain-scoped shared libraries for database entities (e.g., `CustomerEntities.jar`, `OrderEntities.jar`). Only the `CustomerService` imports `CustomerEntities.jar`.
    *   [DON'T]: Create a single `GlobalAppEntities.jar` that contains all database tables and force every service to import it, causing every service to be impacted by any database schema change.

*   **Transaction Orchestration**
    *   [DO]: Design an `OrderService` with an API Facade that internally orchestrates placing an order, applying a payment, and decrementing inventory by directly interacting with the shared database using a single ACID transaction.
    *   [DON'T]: Design an `OrderService` that makes synchronous REST calls to a `PaymentService` and an `InventoryService`, forcing the use of complex compensating Sagas (BASE transactions) to handle failures. This is a microservices pattern, not a service-based architecture pattern.

*   **Interservice Communication**
    *   [DO]: If `OrderService` needs customer data to complete a database record, query the centrally shared database directly using standard SQL joins.
    *   [DON'T]: Make an HTTP network call from `OrderService` to `CustomerService` just to retrieve a customer's name, which introduces latency, utilizes bandwidth, and degrades reliability (stamp coupling).

*   **Service Granularity**
    *   [DO]: Group closely related sub-domains into a single coarse-grained service (e.g., `AccountingService` handles quoting, invoicing, and receiving).
    *   [DON'T]: Create hundreds of fine-grained, single-purpose services (e.g., `QuoteService`, `InvoiceService`, `ReceiptService`) that must coordinate over a network.