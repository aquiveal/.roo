# @Domain
These rules MUST trigger when the AI is tasked with making high-level software design decisions, architecting system boundaries, sizing microservices or bounded contexts, selecting business logic implementation strategies, choosing structural architectural patterns, or defining the testing strategy for a specific software component or subdomain.

# @Vocabulary
*   **Heuristic:** A rule of thumb or mental shortcut that focuses on essential properties ("swamping forces") while ignoring noise. It is sufficient for immediate goals but is not a mathematically proven, 100% correct hard rule.
*   **Bounded Context:** The physical and linguistic boundary of a single business domain model.
*   **Transaction Script:** A business logic implementation pattern utilizing simple, straightforward procedural operations.
*   **Active Record:** A business logic implementation pattern utilizing simple procedural logic but operating on complex data structures wrapped in data access objects.
*   **Domain Model:** A business logic implementation pattern utilizing aggregates and value objects to handle complex business rules and invariants.
*   **Event-Sourced Domain Model:** A business logic implementation pattern where changes in state are captured as a series of events.
*   **CQRS (Command-Query Responsibility Segregation):** An architectural pattern representing the system's data in multiple persistent models (segregating read and write responsibilities).
*   **Ports & Adapters:** An architectural pattern that decouples the central business logic from infrastructural dependencies.
*   **Layered Architecture:** An architectural pattern organizing the codebase into horizontal layers (e.g., Presentation, Business Logic, Data Access).
*   **Testing Pyramid:** A testing strategy emphasizing unit tests over integration and end-to-end tests.
*   **Testing Diamond:** A testing strategy focusing heavily on integration tests.
*   **Reversed Testing Pyramid:** A testing strategy attributing the most attention to end-to-end (E2E) tests.

# @Objectives
*   The AI MUST map tactical and strategic software design decisions directly to the specific complexity, needs, and type of the business subdomain.
*   The AI MUST prevent premature decomposition of Bounded Contexts, favoring wider boundaries when domain knowledge is incomplete or highly volatile.
*   The AI MUST select Business Logic Patterns strictly based on the complexity of the domain rules, data structures, and auditing requirements.
*   The AI MUST align Structural Architectural Patterns (e.g., Layered, CQRS) directly with the requirements of the chosen Business Logic Pattern.
*   The AI MUST assign a specific Testing Strategy that best verifies the chosen Business Logic Pattern.

# @Guidelines

## Bounded Context Sizing & Boundaries
*   When designing Bounded Contexts, the AI MUST NOT optimize for small size. The AI MUST treat the size of a bounded context strictly as a function of the model it encompasses.
*   When dealing with a Core Subdomain or an area where business requirements change frequently (high volatility/uncertainty), the AI MUST design broad bounded context boundaries encompassing multiple subdomains.
*   When domain knowledge increases and business logic stabilizes over time, the AI MAY recommend refactoring and decomposing wide bounded contexts into narrower ones.
*   The AI MUST explicitly state that refactoring logical boundaries is significantly less expensive than refactoring physical boundaries.

## Business Logic Implementation Pattern Selection
*   The AI MUST evaluate the business domain using the following heuristic decision tree to select the appropriate pattern:
    *   **Rule 1 (Event-Sourced Domain Model):** If the subdomain tracks money/monetary transactions, requires a legally mandated consistent audit log, or requires deep analysis of its behavior, the AI MUST select the Event-Sourced Domain Model.
    *   **Rule 2 (Domain Model):** If Rule 1 does not apply, but the subdomain's business logic is complex (complicated business rules, invariants, algorithms, or complex ubiquitous language), the AI MUST select the Domain Model pattern.
    *   **Rule 3 (Active Record):** If Rules 1 and 2 do not apply, but the subdomain includes complex data structures requiring mapping to an underlying database, the AI MUST select the Active Record pattern.
    *   **Rule 4 (Transaction Script):** If the business logic is simple (e.g., simple input validation, CRUD operations, ETL processes) and the data structures are simple, the AI MUST select the Transaction Script pattern.
*   If the AI determines a subdomain is "Core" but the decision tree points to Transaction Script or Active Record, the AI MUST flag this discrepancy and prompt the user to re-evaluate whether the subdomain is truly a Core Subdomain.

## Architectural Pattern Selection
*   The AI MUST dictate the architectural pattern based purely on the selected Business Logic Implementation Pattern:
    *   If **Event-Sourced Domain Model**, the AI MUST mandate **CQRS**. (Without CQRS, the system will be extremely limited in its data querying options).
    *   If **Domain Model**, the AI MUST mandate **Ports & Adapters**. (Otherwise, it is too difficult to keep aggregates and value objects ignorant of persistence).
    *   If **Active Record**, the AI MUST mandate **Layered Architecture with an additional Application (Service) Layer**. (The Service layer controls the active records).
    *   If **Transaction Script**, the AI MUST mandate a **Minimal Layered Architecture** (consisting of only three layers: Presentation, Business Logic, Data Access).
*   *Exception:* The AI MAY recommend CQRS for *any* business logic pattern IF the subdomain explicitly requires representing its data in multiple persistent models (e.g., Polyglot persistence).

## Testing Strategy Selection
*   The AI MUST assign testing strategies based on the selected Business Logic Implementation Pattern:
    *   If **Domain Model** or **Event-Sourced Domain Model**, the AI MUST recommend the **Testing Pyramid**, focusing primarily on Unit Tests for aggregates and value objects.
    *   If **Active Record**, the AI MUST recommend the **Testing Diamond**, focusing primarily on Integration Tests to verify the integration between the service layer and business logic layer.
    *   If **Transaction Script**, the AI MUST recommend the **Reversed Testing Pyramid**, focusing primarily on End-to-End (E2E) tests to verify the simple, end-to-end procedural flow.

# @Workflow
When requested to architect a solution or component for a specific business domain, the AI MUST follow this rigid, step-by-step process:

1.  **Subdomain Analysis:** Ask the user for or infer the properties of the subdomain. Determine if it deals with monetary transactions, audit logs, deep analytics, complex invariants, or simple CRUD data entry.
2.  **Pattern Selection (Business Logic):** Traverse the heuristic decision tree. Select Event-Sourced Domain Model, Domain Model, Active Record, or Transaction Script based strictly on Step 1.
3.  **Pattern Selection (Architecture):** Map the result of Step 2 to its required architectural pattern (CQRS, Ports & Adapters, Layered + Service Layer, or Minimal Layered).
4.  **Testing Strategy Assignment:** Map the result of Step 2 to its optimal testing strategy (Testing Pyramid, Testing Diamond, or Reversed Testing Pyramid).
5.  **Boundary Definition:** Formulate the physical boundaries (Bounded Context). If the domain is highly volatile, newly formed, or a Core Subdomain, define wide boundaries encompassing related subdomains.
6.  **Output Generation:** Present the final design recommendations to the user, explicitly justifying each decision using the heuristic rules defined in this document.

# @Examples (Do's and Don'ts)

## Bounded Context Sizing
*   **[DO]** Recommend grouping a volatile Core Subdomain (e.g., "Dynamic Pricing Algorithm") alongside its highly interactive Supporting Subdomains (e.g., "Competitor Price Ingestion") into a single, wide Bounded Context initially to protect against premature, incorrect physical boundaries.
*   **[DON'T]** Recommend splitting a newly discovered, highly complex business process into 5 separate microservices purely to achieve smaller codebases.

## Business Logic Selection
*   **[DO]** Recommend an Event-Sourced Domain Model for a "Wallet/Ledger" feature because it tracks monetary transactions and requires a strict historical audit log.
*   **[DON'T]** Recommend a Domain Model with Aggregates and Value Objects for a "Static Contact Us Page" or "State/City dropdown list" feature. Use Transaction Script instead.

## Architecture and Testing Alignment
*   **[DO]** Pair an Active Record business logic implementation with a Layered Architecture (including a Service Layer) and advocate for a Testing Diamond strategy focused heavily on integration tests.
*   **[DON'T]** Pair a Domain Model business logic implementation with a Testing Diamond. A Domain Model MUST be paired with a Testing Pyramid (heavy unit testing on aggregates) and a Ports & Adapters architecture.