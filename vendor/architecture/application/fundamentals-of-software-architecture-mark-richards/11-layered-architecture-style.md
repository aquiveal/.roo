# @Domain
These rules are activated when the AI is instructed to design, implement, refactor, or analyze a Layered Architecture (also known as n-tiered architecture style). Triggers include working on monolithic applications separated by technical roles (e.g., user interface, backend, database), bootstrapping a new application without a predefined architecture, migrating legacy monoliths, or addressing issues related to layer bypasses, tight coupling between technical boundaries, and "Architecture Sinkhole" anti-patterns. 

# @Vocabulary
*   **Layered Architecture (n-tiered)**: A monolithic architecture style where components are organized into logical horizontal layers, each performing a specific technical role.
*   **Technical Partitioning**: Grouping application components by their technical role (e.g., presentation, business logic) rather than by their business domain.
*   **Presentation Layer**: The topmost layer responsible for handling all user interface and browser/client communication logic.
*   **Business Layer**: The layer responsible for executing specific business rules associated with a request.
*   **Persistence Layer**: The layer responsible for managing data access and encapsulating database interactions (SQL, ORM).
*   **Database Layer**: The external or embedded physical database/filesystem where data resides.
*   **Services Layer**: An optional layer typically containing shared objects or common utility functionality used by business components.
*   **Closed Layer**: A layer that a request cannot skip; as a request moves top-down, it must go through the layer immediately below it to reach the next layer.
*   **Open Layer**: A layer that a request is allowed to bypass to directly access the layer beneath it.
*   **Layers of Isolation**: The concept where changes made in one closed layer of the architecture do not impact or affect components in other layers, provided the contracts between layers remain unchanged.
*   **Architecture Sinkhole Anti-Pattern**: An anti-pattern occurring when requests move from layer to layer as simple pass-through processing with no business logic performed within each layer.
*   **Architecture by Implication / Accidental Architecture**: Anti-patterns referring to default architectures that emerge when teams "just start coding" without a formal architectural plan, usually resulting in a layered style due to Conway's Law.
*   **Fast-Lane Reader Pattern**: An outdated 2000s pattern where the presentation layer directly accesses the database for simple retrieval, breaking the layers of isolation.

# @Objectives
*   **Enforce Technical Separation of Concerns**: Ensure components within a specific layer only deal with the logic pertaining to that layer (e.g., Presentation layer must not contain SQL).
*   **Maintain Layers of Isolation**: Use closed layers for the primary request flow to ensure that swapping or changing one layer (e.g., upgrading from JSF to React.js) does not break adjacent layers.
*   **Control Architectural Access Boundaries**: Explicitly document and enforce whether a layer is open or closed to prevent brittle, tightly coupled applications.
*   **Prevent Unnecessary Pass-Throughs**: Monitor the architecture to ensure the Architecture Sinkhole anti-pattern does not dominate the request flow.
*   **Support Evolutionary Bootstrapping**: When using Layered Architecture as a starting point for an unknown future architecture, keep object hierarchies shallow and reuse minimal to facilitate later migration to modular styles.

# @Guidelines
*   **Layer Organization**: You MUST organize components horizontally based on technical capabilities (Presentation, Business, Persistence, Database). Do NOT partition the root architecture by domain.
*   **Deployment Topologies**: You MAY design the physical deployment in one of three variants:
    1.  Presentation, Business, and Persistence combined in a single deployment unit connecting to an external Database.
    2.  Presentation separated into its own deployment unit; Business and Persistence combined into a second unit; Database external.
    3.  All layers, including an embedded/in-memory database, combined into a single deployment unit.
*   **Strict Top-Down Flow Rules**: A request MUST flow top-down. Bottom-up requests or cyclical dependencies between layers are explicitly forbidden.
*   **Closed Layer Enforcement**: The Presentation, Business, and Persistence layers MUST default to being "Closed". The Presentation layer MUST NOT access the Persistence or Database layer directly.
*   **Open Layer Exception Handling**: If shared utilities or common business objects (e.g., logging, date utilities) are required, you MUST extract them into a newly created "Services Layer". You MUST mark this Services Layer as "Open" so the Business layer can bypass it to reach the Persistence layer when shared services are not needed.
*   **Documentation of Boundaries**: You MUST explicitly document which layers are open and which are closed, and enforce these boundaries via code reviews, linting, or architectural fitness functions.
*   **The 80-20 Sinkhole Rule**: You MUST analyze the request flow. If more than 20% of requests are "sinkholes" (simple pass-throughs with no logic applied in the middle layers), you MUST evaluate whether to open specific layers or change the architecture style entirely.
*   **Domain-Driven Design (DDD) Incompatibility**: Do NOT attempt to strictly apply Domain-Driven Design in a Layered Architecture. Recognize that business domains (e.g., "customer") will inevitably be smeared across all technical layers.
*   **Architecture Characteristics Acknowledgement**:
    *   Do NOT recommend this architecture if the system requires high Agility, Deployability, Testability, Elasticity, Scalability, or Fault Tolerance.
    *   DO recommend this architecture when the primary drivers are overall cost, simplicity, and a small/simple application footprint.
    *   Expect Performance to be inherently constrained (rated 2/5) due to lack of parallel processing, closed layers, and potential sinkholes.

# @Workflow
1.  **Identify the Standard Layers**: Define the technical boundaries for the application (e.g., Presentation, Business, Persistence, Database).
2.  **Establish Open/Closed States**: Explicitly declare the access rules for every layer. Default all primary flow layers to Closed.
3.  **Implement Isolation Contracts**: Define clear data contracts (DTOs, ViewModels) between layers so that a layer does not leak its internal implementation details (e.g., do not pass an ORM-mapped database entity directly to the Presentation layer if it tightly couples them).
4.  **Extract Shared Concerns**: Identify shared business logic or utilities. Place them in an explicit, documented Open layer (e.g., an Open Services layer below the Business layer).
5.  **Audit the Request Flow**: Trace common business requests from Presentation to Database. Calculate the percentage of requests that undergo no transformations or business logic. 
6.  **Resolve Sinkholes**: If pass-through requests exceed 20%, explicitly open a specific layer for those requests or rethink the architecture style.
7.  **Prepare for Migration (If Applicable)**: If this architecture is being used as a temporary starting point, flatten inheritance trees and avoid creating tightly coupled shared libraries to ensure components can be easily extracted later.

# @Examples (Do's and Don'ts)

*   **[DO]** Enforce Layers of Isolation by requiring the Presentation layer to call the Business layer.
    ```java
    // Presentation Layer Component
    @RestController
    public class CustomerController {
        private final CustomerBusinessService customerService;
        
        public CustomerView getCustomer(String id) {
            // Correct: Presentation calls Business Layer
            return customerService.calculateCustomerProfile(id); 
        }
    }
    ```

*   **[DON'T]** Allow the Presentation layer to bypass the Business layer to directly access the Persistence layer (violating a closed layer).
    ```java
    // Presentation Layer Component
    @RestController
    public class CustomerController {
        private final CustomerRepository customerRepository; // ANTI-PATTERN
        
        public CustomerView getCustomer(String id) {
            // Incorrect: Fast-lane reader pattern bypassing closed layers
            return customerRepository.findById(id); 
        }
    }
    ```

*   **[DO]** Use an Open Services layer for shared objects, allowing the Business layer to bypass it if needed.
    ```java
    // Business Layer Component
    public class OrderBusinessService {
        private final OrderPersistenceService persistenceService;
        private final SharedAuditService openAuditService; // From Open Services Layer
        
        public void processOrder(Order order) {
            // Can use the open layer
            openAuditService.logOrder(order);
            // Can bypass the open layer to go directly to persistence
            persistenceService.saveOrder(order);
        }
    }
    ```

*   **[DON'T]** Build deep, complex inheritance hierarchies across layers if the Layered Architecture is just a starting point for future microservices, as this will trap the code in a monolith.

*   **[DO]** Recognize the Architecture Sinkhole Anti-Pattern and flag it if it represents the majority of the application.
    ```java
    // Business Layer Component
    public class CustomerService {
        // If 80% of methods in the application look exactly like this (doing nothing but delegating), 
        // the architecture is a Sinkhole.
        public Customer getCustomer(String id) {
            return customerRepository.getCustomer(id);
        }
    }
    ```