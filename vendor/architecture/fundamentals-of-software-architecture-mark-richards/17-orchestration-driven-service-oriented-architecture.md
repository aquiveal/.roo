# @Domain
These rules MUST trigger when the AI is tasked with designing, analyzing, refactoring, or discussing an **Orchestration-Driven Service-Oriented Architecture (SOA)**, Enterprise Service Bus (ESB) architectures, highly technically partitioned distributed architectures, or legacy enterprise integration patterns focused on extreme code reuse and centralized orchestration.

# @Vocabulary
The AI MUST adopt and use the following precise terminology when analyzing or designing systems within this domain:
*   **Business Services**: Top-level entry points of the architecture that contain no implementation code, only input, output, and schema information. Defined by business users (e.g., `ExecuteTrade`, `PlaceOrder`).
*   **Enterprise Services**: Fine-grained, shared implementations representing atomic behavior around particular business domains (e.g., `CreateCustomer`, `CalculateQuote`). Designed as reusable building blocks.
*   **Application Services**: One-off, single-implementation services owned by a single application team (e.g., geo-location services), not intended for enterprise-wide reuse.
*   **Infrastructure Services**: Services supplying operational concerns such as monitoring, logging, authentication, and authorization. Owned by a shared infrastructure team.
*   **Orchestration Engine**: The central component (often an ESB) that stitches together business service implementations, handles distributed transactional coordination, executes message transformations, and acts as the integration hub.
*   **Technical Partitioning**: The practice of separating an architecture based on technical capabilities (the driving philosophy of this SOA style) rather than by domains or bounded contexts.
*   **Single Quantum**: Despite being a distributed architecture, Orchestration-Driven SOA is a single architectural quantum because the orchestration engine and shared relational databases act as giant, synchronous coupling points.

# @Objectives
When applying Orchestration-Driven SOA principles, the AI MUST achieve the following goals:
*   Enforce a strict, layered service taxonomy (Business, Enterprise, Application, Infrastructure).
*   Ensure all request flows and integrations are routed through the centralized Orchestration Engine.
*   Maximize enterprise-level reuse of services as dictated by the architecture's philosophy, while explicitly calculating and warning the user about the resulting system-wide coupling.
*   Treat the architecture as a single architectural quantum with a shared relational database.
*   Explicitly highlight the negative trade-offs of this style (poor performance, disastrous deployability and testability) when evaluating it against modern requirements.

# @Guidelines
To properly design or interact with an Orchestration-Driven SOA, the AI MUST adhere to the following granular rules:

*   **Service Taxonomy Enforcement**: The AI MUST categorize every service into one of the four defined layers. It MUST NOT place business implementation code inside a Business Service. 
*   **Centralized Orchestration**: The AI MUST explicitly map all communication between services to flow through the Orchestration Engine. It MUST NOT allow direct point-to-point, service-to-service communication.
*   **Transaction Management**: The AI MUST utilize the Orchestration Engine to define transaction boundaries and declarative transactional behavior rather than handling distributed transactions directly inside the service code.
*   **Extreme Reuse Mandate**: When defining entities (e.g., Customer), the AI MUST consolidate all attributes required by all distinct business units into a single canonical Enterprise Service to satisfy the SOA reuse philosophy.
*   **Coupling & Ripple Effect Awareness**: When making a change to a shared Enterprise Service, the AI MUST explicitly map and report the "ripple effect" of that change across all other services and tiers that depend on it.
*   **Performance Constraints**: The AI MUST flag any requirement for "high performance" as a severe architectural mismatch, noting that requests split across the orchestration engine and multiple enterprise tiers inherently cause poor performance.
*   **Deployment & Testing Constraints**: The AI MUST recommend coordinated deployments and holistic system testing, recognizing that the high degree of semantic and structural coupling makes independent service deployment nearly impossible.

# @Workflow
When tasked with designing or analyzing an Orchestration-Driven Service-Oriented Architecture, the AI MUST execute the following algorithmic process:

1.  **Business Process Identification**: Identify the overarching business workflow using the litmus test: "Are we in the business of [Workflow Name]?" Define this as a code-less **Business Service** (inputs/outputs only).
2.  **Taxonomy Decomposition**: Break down the business workflow into reusable, atomic domain behaviors. Define these as **Enterprise Services**.
3.  **Application Specifics**: Identify any non-reusable, context-specific behaviors needed by the workflow and define them as **Application Services**.
4.  **Operational Mapping**: Delegate all cross-cutting security, logging, and monitoring tasks to **Infrastructure Services**.
5.  **Orchestration Routing**: Design the message flow so that the Business Service calls the Orchestration Engine, which in turn sequentially or conditionally invokes the Enterprise and Application services.
6.  **Transaction Boundary Definition**: Define the transaction boundaries within the Orchestration Engine, linking the required Enterprise Services to the shared relational database.
7.  **Trade-Off Analysis**: Output a formal warning to the user detailing the costs of this design: identify the specific coupling points created by the shared Enterprise Services, predict the deployment friction, and note the performance overhead of the Orchestration Engine.

# @Examples (Do's and Don'ts)

*   **Service Communication**
    *   [DO]: Route a request from `CreateQuote` to the ESB, which then orchestrates sequential calls to the `CreateCustomer` Enterprise Service and the `CalculateQuote` Application Service.
    *   [DON'T]: Have the `CreateQuote` service make a direct HTTP REST call to the `CreateCustomer` service.

*   **Service Definition**
    *   [DO]: Define a Business Service as an abstract contract (e.g., WSDL or OpenAPI spec) that contains zero business logic, delegating all logic to the orchestration layer.
    *   [DON'T]: Embed SQL queries, domain logic, or routing logic inside the `PlaceOrder` Business Service.

*   **Entity Modeling for Reuse**
    *   [DO]: Create a single, canonical `Customer` Enterprise Service that includes driver's license data (for auto insurance) and medical history (for disability insurance) to maximize enterprise reuse.
    *   [DON'T]: Create separate bounded contexts (e.g., `AutoInsuranceCustomer` and `DisabilityCustomer`). While better for decoupling, this violates the Orchestration-Driven SOA philosophy of extreme reuse.

*   **Transaction Handling**
    *   [DO]: Rely on the Orchestration Engine to declaratively wrap the invocations of `UpdateInventory` and `ProcessPayment` in a single distributed transaction using a shared relational database.
    *   [DON'T]: Attempt to implement a Saga pattern or compensating transaction framework inside the individual Enterprise Services.