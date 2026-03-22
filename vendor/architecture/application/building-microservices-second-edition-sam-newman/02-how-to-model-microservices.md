@Domain
This rule file MUST be activated when the AI is assisting with architectural design, analyzing or defining microservice boundaries, refactoring monolithic applications into distributed systems, evaluating coupling and cohesion between system components, modeling business domains using Domain-Driven Design (DDD), or designing inter-process communication contracts and data schemas.

@Vocabulary
- **Information Hiding**: Hiding as many internal implementation details as possible behind a boundary, exposing only what is necessary via external interfaces to reduce the assumptions modules make about each other.
- **Cohesion**: The principle that code that changes together stays together. Optimizing for high cohesion of business functionality over high cohesion of technical functionality.
- **Coupling**: The relationship between things across a boundary. Loosely coupled services can be changed without requiring changes to other services.
- **Constantine’s Law**: A structure is stable if cohesion is strong and coupling is low.
- **Domain Coupling**: When one microservice needs to interact with another to use its functionality. A loose form of coupling, but data shared must be kept to an absolute minimum.
- **Temporal Coupling**: In distributed systems, this occurs when one microservice requires another to be up and available at the exact same time to complete a synchronous operation.
- **Pass-Through Coupling**: When a microservice passes data to another purely because a third downstream service requires it. 
- **Common Coupling**: When two or more microservices make use of a common set of data (e.g., a shared database, shared memory, or shared filesystem).
- **Content Coupling (Pathological Coupling)**: When an upstream service reaches into the internals of a downstream service and changes its internal state directly (e.g., directly accessing and modifying another microservice's database tables).
- **Domain-Driven Design (DDD)**: An approach to software development that centers the architecture around the real-world business domain.
- **Ubiquitous Language**: A common vocabulary shared between the delivery team and domain experts/users, embedded directly into the codebase and service contracts.
- **Aggregate**: A self-contained state machine focusing on a single domain concept (e.g., an Order) that is treated as a single entity with its own lifecycle.
- **Bounded Context**: An explicit organizational and architectural boundary within a business domain that provides specific capabilities while hiding internal complexity.
- **Event Storming**: A collaborative brainstorming exercise using sticky notes to surface a domain model by identifying Domain Events, Commands, and Aggregates.
- **Volatility-Based Decomposition**: Extracting system functionality into separate services based on how frequently the code changes (e.g., isolating fast-changing "Systems of Innovation").

@Objectives
- Define stable, independently deployable microservice boundaries.
- Maximize internal business cohesion and minimize external cross-service coupling.
- Enforce strict Information Hiding to protect external consumers from internal implementation changes.
- Align architectural boundaries with business domains using Domain-Driven Design rather than technical layers.
- Select the appropriate decomposition strategy (Domain, Volatility, Data/Security, Technology, or Organizational) based on the specific operational and business context.

@Guidelines

**1. General Microservice Boundary Rules:**
- The AI MUST prioritize cohesion of business functionality over cohesion of related technology. Horizontal, tiered architectures (e.g., separate Presentation, Application, and Data tier services) MUST NOT be used as microservice boundaries.
- The AI MUST enforce Information Hiding. A microservice's external interface must expose the absolute minimum required information. Internal state, database structures, and technology choices MUST be completely hidden from upstream consumers.
- The AI MUST evaluate Constantine's Law: ensure boundaries represent strong internal cohesion and low external coupling to guarantee stability.

**2. Coupling Mitigation Constraints:**
- **Domain Coupling:** The AI MUST permit Domain Coupling but MUST heavily scrutinize the data payload. Share only what is absolutely necessary.
- **Temporal Coupling:** When evaluating synchronous HTTP/RPC calls, the AI MUST warn about Temporal Coupling (both services must be available). The AI SHOULD suggest asynchronous communication (e.g., message brokers) if temporal decoupling is required.
- **Pass-Through Coupling:** When the AI detects data being passed through an intermediary service solely for a downstream service, the AI MUST propose one of three fixes:
  1. The calling service bypasses the intermediary and talks to the downstream service directly.
  2. The intermediary service completely hides the requirement by constructing the required payload locally.
  3. The intermediary service treats the payload as an opaque blob, ignorant of its internal structure.
- **Common Coupling:** The AI MUST prohibit multiple microservices from reading/writing to the same shared database schema unless it is benign, read-only static reference data. To fix Common Coupling, the AI MUST designate a single microservice as the sole source of truth and state machine for that entity.
- **Content Coupling:** The AI MUST explicitly reject any architecture where an external service directly manipulates the database or internal state of another service. All state changes MUST be requested via the owning microservice's API.

**3. Domain-Driven Design (DDD) Application:**
- **Ubiquitous Language:** Code concepts, service names, and API endpoints MUST use the domain vocabulary of the business users.
- **Aggregates:** 
  - The AI MUST NOT split a single Aggregate across multiple microservices. One Aggregate = Managed by exactly one microservice.
  - State transitions of an aggregate MUST be validated by the aggregate itself. Upstream services send *requests*, which the aggregate is free to reject if invalid. 
  - Cross-service aggregate relationships MUST be modeled explicitly (e.g., using URIs like `/customers/123` or pseudo-URIs like `soundcloud:tracks:123` instead of raw database IDs).
- **Bounded Contexts:**
  - Map initial microservices to coarse-grained Bounded Contexts.
  - Implement **Hidden Models**: Do not leak internal representations to the outside. Create separate, restricted external representations for shared data.
  - Implement **Shared Models**: When concepts exist in multiple bounded contexts, use context-specific naming (e.g., `Customer` in Finance vs. `Recipient` in Warehouse) rather than blindly copying data models.
  - **Turtles all the way down:** When splitting a Bounded Context into smaller microservices, the AI MUST attempt to hide this decomposition from external consumers by providing a coarse-grained API facade.

**4. Alternative Decomposition Strategies:**
- **Volatility:** The AI MAY suggest extracting volatile, frequently changing code into its own service to speed up time-to-market.
- **Data (Security/Privacy):** The AI MUST isolate systems handling highly sensitive data (e.g., PCI credit card data, PII) into separate network "zones" or microservices to limit audit and compliance scope.
- **Technology:** The AI MAY extract specific capabilities into distinct microservices if highly specialized technology or performance characteristics (e.g., Rust for CPU-heavy tasks) are required.
- **Organizational (Conway's Law):** The AI MUST align microservice boundaries with team ownership structures. Cross-team shared ownership of a microservice MUST be avoided.

**5. Anti-Patterns to Reject:**
- **The CRUD Wrapper:** The AI MUST reject microservice designs that are simply thin wrappers around database CRUD operations. This indicates leaked business logic and weak cohesion.
- **Horizontal Slicing:** The AI MUST reject splitting services across technical seams (e.g., a stateless UI service talking to a remote DB-access service). Slices MUST be vertical business capabilities.

@Workflow
When tasked with modeling microservices or defining system boundaries, the AI MUST follow this exact sequence:
1. **Identify the Business Domain:** Establish the Ubiquitous Language. Map out Domain Events, Commands, and Aggregates (simulate Event Storming if starting from scratch).
2. **Assign Aggregates:** Group related Aggregates into cohesive Bounded Contexts. Ensure no Aggregate spans multiple Contexts.
3. **Draft Initial Boundaries:** Define coarse-grained microservices based on Bounded Contexts.
4. **Analyze Coupling:** Evaluate all inter-service communication for Domain, Temporal, Pass-Through, Common, and Content coupling. Refactor the design to mitigate Pass-Through, Common, and Content coupling using the predefined rules.
5. **Apply Non-Domain Constraints:** Check if the architecture needs adjustment based on Volatility, Data Security (PCI/PII isolation), distinct Technology requirements, or Organizational boundaries (Conway's Law).
6. **Define Contracts:** Establish the external APIs. Ensure internal models are hidden, cross-service references use URIs/explicit identifiers, and state transition validation remains inside the owning service.

@Examples (Do's and Don'ts)

**Information Hiding & Internal vs. External Models**
- [DO]: Keep the `ShelfLocation` array inside the Warehouse context. When Finance asks for inventory, expose a specific `StockCount` object that only contains the `item_sku` and `total_quantity`.
- [DON'T]: Return the internal `WarehouseStockItem` database object directly to the Finance service, forcing Finance to calculate the quantity from shelf locations.

**Cross-Service Aggregate Relationships**
- [DO]: Store relationships to external microservices as explicit URIs to communicate that the data lives over a network boundary.
  ```json
  {
    "order_id": "8821",
    "customer_href": "/api/v1/customers/992A"
  }
  ```
- [DON'T]: Store raw integer IDs (e.g., `cust_id: 992`) locally without context, treating distributed architectures like local relational databases.

**Fixing Common & Content Coupling**
- [DO]: Designate the `Order` microservice as the sole owner of the `Orders` table. If the `Warehouse` service needs to update an order to `SHIPPED`, it sends a `POST /orders/123/status` request. The `Order` service validates the state transition locally before writing to the database.
- [DON'T]: Allow both the `Order` microservice and the `Warehouse` microservice to connect directly to the same SQL database and execute `UPDATE orders SET status = 'SHIPPED'` statements.

**Fixing Pass-Through Coupling**
- [DO]: If the `OrderProcessor` must trigger shipping, but the `Shipping` service requires a complex `CustomsDeclaration`, have the `OrderProcessor` pass only standard order data to `Warehouse`. Let the `Warehouse` service generate the `CustomsDeclaration` locally before calling `Shipping`.
- [DON'T]: Force the `OrderProcessor` to gather and construct the `CustomsDeclaration` just to pass it through the `Warehouse` service to the `Shipping` service.

**Microservice Slicing**
- [DO]: Slice architectures vertically. The `CustomerProfile` service encapsulates the Profile UI, Profile Application Logic, and Profile Database.
- [DON'T]: Slice architectures horizontally. Creating a global `WebUI` service, a global `BusinessLogic` service, and a global `DataAccess` service.

**Microservice Abstraction (Turtles all the way down)**
- [DO]: If the coarse-grained `Warehouse` service is split internally into `Inventory` and `Shipping` microservices, keep a `Warehouse` API Gateway/Facade in front of them so external upstream consumers don't have to change their integration points.
- [DON'T]: Split `Warehouse` into two services and immediately force all 15 upstream consumer teams to rewrite their code to point to the two new services.