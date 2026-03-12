# @Domain
These rules MUST trigger whenever the AI is tasked with designing, architecting, refactoring, evaluating, or scaffolding microservices, distributed systems, domain models, service boundaries, or API contracts. This includes tasks involving database schema design for distributed systems, inter-service communication patterns, and module extraction from monolithic architectures.

# @Vocabulary
- **Information Hiding**: The practice of concealing as much internal implementation detail as possible behind a service boundary, exposing only the absolute minimum required via external interfaces to reduce assumptions between modules.
- **Cohesion**: The principle that "code that changes together, stays together." High cohesion of business functionality is the primary goal.
- **Coupling**: The degree of interdependence between software modules. Loose coupling is mandatory for independent deployability.
- **Constantine's Law**: "A structure is stable if cohesion is strong and coupling is low."
- **Domain Coupling**: A loose form of coupling where one service needs functionality provided by another. Must be minimized to avoid centralizing too much logic.
- **Temporal Coupling**: A tight form of coupling where multiple services must be available and responsive at the exact same time (e.g., synchronous HTTP calls) for an operation to complete.
- **Pass-Through Coupling**: A tight form of coupling where a service passes data it does not use, solely because a downstream service requires it.
- **Common Coupling**: A tight form of coupling where two or more services read and write to the same shared data source (e.g., a shared database table or memory).
- **Content (Pathological) Coupling**: The tightest and worst form of coupling where an upstream service directly reaches into and modifies the internal state/database of a downstream service.
- **Domain-Driven Design (DDD)**: A modeling methodology prioritizing the real-world business domain.
- **Ubiquitous Language**: A shared vocabulary derived directly from business domain experts, which MUST be used identically in code, variables, endpoints, and architecture.
- **Aggregate**: A self-contained collection of objects managed as a single entity with a defined lifecycle/state machine, referring to a real-world concept (e.g., `Order`).
- **Bounded Context**: An explicit organizational and architectural boundary hiding internal models and exposing only necessary shared models.
- **Event Storming**: A collaborative process used to discover domains by identifying Domain Events, Commands, and Aggregates.
- **Delivery Contention**: The friction caused when multiple teams/developers trip over each other trying to deploy changes to the same codebase or layered architecture.

# @Objectives
- Define highly cohesive, loosely coupled microservice boundaries based on business domains rather than technical layers.
- Achieve strict independent deployability for all modeled services.
- Prevent catastrophic architectural coupling (Content, Common, and Pass-Through) by enforcing strict encapsulation and state ownership.
- Apply Domain-Driven Design (DDD) patterns to align software architecture with business realities and organizational structures.
- Prioritize high cohesion of business functionality over high cohesion of related technologies.

# @Guidelines

### 1. Information Hiding and Boundary Design
- The AI MUST encapsulate all internal data storage, technology choices, and local logic behind a network endpoint.
- The AI MUST NOT expose internal database schemas, internal models, or underlying infrastructure details via the API contract.
- When creating shared data models between bounded contexts, the AI MUST define separate representations for internal use and external exposure (e.g., internal `StockItem` with shelf locations vs. external `StockCount` with just the count).

### 2. Coupling Eradication
- **Content Coupling**: The AI MUST NEVER permit a service to directly access or modify the database or internal state of another service.
- **Common Coupling**: The AI MUST actively prevent the design of shared databases for multiple microservices. If shared state is unavoidable, the AI MUST designate a single microservice as the absolute source of truth and state machine manager for that entity, requiring all other services to send *requests* (which can be rejected) to modify that state.
- **Pass-Through Coupling**: The AI MUST resolve pass-through coupling by either:
  1. Having the caller communicate directly with the downstream service.
  2. Having the intermediary service construct the required payload locally so the upstream caller is unaware of the downstream requirement.
  3. Treating the passed data as a completely opaque blob that the intermediary does not parse or validate.
- **Temporal Coupling**: The AI MUST warn against synchronous blocking network calls spanning multiple services and MUST recommend asynchronous communication (e.g., message brokers, events) to reduce temporal coupling.

### 3. Domain-Driven Design (DDD) Implementation
- **Ubiquitous Language**: The AI MUST name variables, classes, database tables, and API endpoints using the specific business terminology provided. Generic technical names (e.g., `Arrangement`, `DataRecord`, `GenericProcessor`) are strictly forbidden.
- **Aggregates**: 
  - The AI MUST map one aggregate to EXACTLY ONE microservice. A microservice may manage multiple aggregates, but an aggregate MUST NOT be split across multiple microservices.
  - The AI MUST design aggregates to reject invalid state transitions. The AI MUST NOT design microservices as thin, logic-less wrappers over database CRUD operations.
  - When linking aggregates across different microservices, the AI MUST NOT use database foreign keys. Instead, the AI MUST use explicit identifiers or pseudo-URIs (e.g., `/customers/123` or `soundcloud:tracks:123`).
- **Bounded Contexts**: The AI MUST use bounded contexts as the primary mechanism for finding microservice seams. Default to larger, coarser-grained contexts first, only sub-dividing ("turtles all the way down") when operational benefits justify it.

### 4. Alternative Decomposition Drivers
- **Volatility**: The AI MAY isolate highly volatile (frequently changing) code into its own service to accelerate deployment velocity, provided it does not violate bounded contexts.
- **Data Security/Compliance**: The AI MUST separate services processing highly sensitive data (e.g., PCI-DSS credit card data, GDPR PII) into isolated secure zones to limit audit scope.
- **Technology Seams**: The AI MAY propose service boundaries when specific runtimes or performance characteristics are strictly required (e.g., extracting a Rust service for heavy computation).
- **Organizational Alignment**: The AI MUST slice architectures vertically (business capabilities) rather than horizontally (UI team, Backend team, DB team). Layering MUST ONLY happen *inside* the microservice boundary.

# @Workflow
When tasked with modeling a new microservice or splitting an existing system, the AI MUST follow this rigid sequence:

1. **Domain Discovery (Event Storming Simulation)**:
   - Ask the user for or extract the core business Events (orange sticky notes, e.g., "Order Placed").
   - Identify the Commands triggering them (blue sticky notes, e.g., "Place Order").
   - Group these into Aggregates (yellow sticky notes, e.g., "Order").
2. **Context Mapping**:
   - Cluster the discovered Aggregates into logical Bounded Contexts based on organizational/business lines (e.g., "Warehouse", "Finance").
3. **Boundary Definition**:
   - Define the microservice boundary around the Bounded Context.
   - Define the explicit external API contract, ensuring Information Hiding (strip out internal operational data from external responses).
4. **Coupling Assessment**:
   - Trace the expected communication pathways.
   - Identify and immediately refactor any Pass-Through, Common, or Content coupling.
   - Check for Temporal coupling and propose asynchronous alternatives if stability is threatened.
5. **State Management & Cross-Service References**:
   - Assign complete database ownership to the microservice.
   - Convert all inter-aggregate relationships that cross service boundaries into URI or String-based references.
6. **Refinement via Alternative Drivers**:
   - Assess if data security (PCI/PII), volatility, or specific technological requirements necessitate further splitting within the bounded context. Hide these sub-splits behind a coarse-grained API facade if possible.

# @Examples (Do's and Don'ts)

### Information Hiding & External Models
- **[DO]** Translate internal state into a safe external contract.
  ```json
  // Internal State (Hidden)
  { "itemId": "A1", "shelfId": "X-99", "bin": 4, "quantity": 10 }
  
  // External Contract (Exposed by Warehouse Service)
  { "itemId": "A1", "stockCount": 10 }
  ```
- **[DON'T]** Expose internal tracking logic to external consumers, forcing them to understand your warehouse layout.

### Cross-Service Aggregate References
- **[DO]** Reference external aggregates using URIs or explicit global IDs.
  ```java
  public class LedgerEntry {
      private String transactionId;
      private BigDecimal amount;
      // Loose linking to an external microservice
      private String customerUri; // e.g., "musiccorp:customers:99281"
  }
  ```
- **[DON'T]** Use direct foreign keys to tables managed by other services.
  ```java
  public class LedgerEntry {
      private String transactionId;
      @ManyToOne // BAD: Tightly couples to the Customer DB table
      @JoinColumn(name="customer_id")
      private Customer customer; 
  }
  ```

### Fixing Pass-Through Coupling
- **[DO]** Hide downstream requirements within the domain service.
  ```java
  // Order Processor calls Warehouse with just the Order
  warehouseService.dispatch(orderId, customerId, shippingType);
  
  // Warehouse Service builds the manifest internally and calls Shipping
  ShippingManifest manifest = buildManifest(customerId, shippingType);
  shippingService.ship(manifest);
  ```
- **[DON'T]** Force the upstream caller to build payloads for services it shouldn't know about.
  ```java
  // BAD: Order Processor knows how to build a ShippingManifest just to pass it through Warehouse
  ShippingManifest manifest = new ShippingManifest(customerId, shippingType);
  warehouseService.dispatch(orderId, manifest);
  ```

### Handling Common Coupling (State Transitions)
- **[DO]** Delegate state transitions to a single authoritative microservice that enforces business rules.
  ```java
  // Warehouse Service requests a state change
  orderService.requestStatusChange(orderId, Status.PICKING);
  
  // Order Service validates the transition internally
  public void requestStatusChange(String id, Status newStatus) {
      Order order = repository.findById(id);
      if (order.canTransitionTo(newStatus)) {
          order.setStatus(newStatus);
          repository.save(order);
      } else {
          throw new IllegalStateException("Invalid transition");
      }
  }
  ```
- **[DON'T]** Allow multiple services to write directly to a shared database or use a dumb CRUD wrapper that accepts any state.
  ```sql
  -- BAD: Warehouse service connecting directly to Order database
  UPDATE orders SET status = 'PICKING' WHERE order_id = 123;
  ```

### Team and Architecture Alignment
- **[DO]** Slice features vertically. The "Customer Profile Team" owns the User Interface profile widget, the `CustomerProfile` microservice, and the customer profile database schema.
- **[DON'T]** Slice features horizontally. E.g., Frontend Team builds the UI, Middleware Team builds the gateway, Backend Team builds the DB wrapper.