# @Domain
These rules MUST be triggered when the AI is tasked with designing system architecture, determining component boundaries, establishing top-level system partitioning, refactoring monolithic applications into distributed systems, or evaluating the granularity and physical packaging of software modules.

# @Vocabulary
*   **Module**: A logical grouping of related code (e.g., classes, functions) used as a general organizational concept.
*   **Component**: The physical manifestation and packaging of a module (e.g., `.jar` files in Java, `.dll` in .NET, `.gem` in Ruby, or standalone services). It is the fundamental building block of an architecture.
*   **Library**: A simple component wrapper that runs in the same memory address as the calling code and communicates via language function calls (compile-time dependency).
*   **Service**: A component that runs in its own address space and communicates via low-level networking protocols (TCP/IP) or higher-level formats (REST, message queues).
*   **Technical Partitioning**: A top-level architectural organization based on technical capabilities or layers (e.g., Presentation, Business Rules, Persistence).
*   **Domain Partitioning**: A top-level architectural organization based on business workflows or domains (e.g., `CatalogCheckout`, `UserManagement`), common in Domain-Driven Design (DDD) and Microservices.
*   **Entity Trap**: An architectural anti-pattern where components are incorrectly designed as simple Object-Relational Mappings (CRUD wrappers) around database entities rather than being modeled around business workflows.
*   **Actor/Actions Approach**: A component discovery technique that identifies system users (actors) and the activities they perform (actions).
*   **Event Storming**: A component discovery technique utilized in DDD and message-based architectures that builds components around events and message handlers.
*   **Workflow Approach**: A generic component discovery technique that models components around business activities and roles without the explicit constraints of message-based systems.
*   **Architecture Quantum**: An independently deployable artifact with high functional cohesion and synchronous connascence. The number of unique quanta dictates whether an architecture should be monolithic or distributed.

# @Objectives
*   Define the architecture by structuring physical components, rather than solely organizing logical classes or functions.
*   Select the appropriate top-level partitioning strategy (Technical vs. Domain) based on the organization's goals, existing coupling, and target architecture style.
*   Derive components iteratively using established discovery techniques rather than relying on database schema mappings.
*   Align component boundaries with business workflows and differing operational architecture characteristics (e.g., scalability, availability).
*   Determine the overarching architecture style (Monolithic vs. Distributed) based on the architectural quanta identified during component design.

# @Guidelines
*   **Component Abstraction Level**: The AI MUST define components at a macro-level (coarse-grained). The AI MUST NOT dictate micro-level class design or internal design patterns during the component-based thinking phase; those are implementation details delegated to developers.
*   **Partitioning Selection**: The AI MUST explicitly declare and justify the top-level partitioning strategy.
    *   Use **Domain Partitioning** when the system benefits from modular monoliths or microservices, cross-functional teams, and isolated business workflows.
    *   Use **Technical Partitioning** when strict separation of technical concerns (e.g., UI vs. DB access) or layer-based decoupling is the primary goal.
*   **Avoid the Entity Trap**: The AI MUST NEVER design components that simply mirror database tables (e.g., `CustomerManager`, `OrderManager`). Components MUST encompass workflows and actions, not just CRUD entities.
*   **Granularity Tuning**: The AI MUST balance component granularity. Components MUST NOT be so fine-grained that they require excessive inter-component communication to achieve a single task, nor so coarse-grained that they introduce high internal coupling and hinder deployability.
*   **Architecture Characteristics as Boundaries**: The AI MUST split a single functional component into multiple components if different parts of that component require conflicting or significantly different architecture characteristics (e.g., separating `BidCapture` from `AuctioneerCapture` because the latter requires strictly higher reliability/availability, while the former requires extreme scalability).
*   **Quanta-Driven Distribution**: The AI MUST count the architectural quanta resulting from the component design. If all components share the same characteristics, the AI MUST recommend a Monolithic architecture. If components require differing architecture characteristics, the AI MUST recommend a Distributed architecture.

# @Workflow
When tasked with component design and architecture structuring, the AI MUST strictly follow this algorithmic sequence:

1.  **Select Top-Level Partitioning Strategy**: 
    *   Evaluate the problem domain and explicitly select either Technical Partitioning or Domain Partitioning. Justify the choice based on trade-offs (e.g., customization needs, data coupling, team structure).
2.  **Select Discovery Technique**: 
    *   Choose a discovery technique based on the system paradigm: *Event Storming* (for message-driven/DDD systems), *Actor/Actions* (for generic/traditional systems), or *Workflow Approach* (for non-messaging domain-driven systems).
3.  **Identify Initial Components**: 
    *   Generate the first draft of coarse-grained components based on the selected discovery technique.
4.  **Assign Requirements**: 
    *   Map functional requirements (user stories) to the initial components. Consolidate or break apart components to ensure all requirements fit logically.
5.  **Analyze Roles and Responsibilities**: 
    *   Verify that component granularity matches the identified actors and business behaviors.
6.  **Analyze Architecture Characteristics**: 
    *   Evaluate the operational characteristics (e.g., performance, elasticity, availability) required by each component. 
    *   Split components that contain conflicting architecture characteristics (e.g., separating a high-volume read stream from a low-volume transactional write process).
7.  **Restructure and Refine**: 
    *   Iterate on the component boundaries based on the findings from steps 4, 5, and 6 to produce a finalized component diagram.
8.  **Evaluate Architectural Quanta**: 
    *   Assess the refined components to determine the number of architectural quanta. Output a final decision recommending either a Monolithic or Distributed architecture based on whether the components share a single quantum or require multiple quanta.

# @Examples (Do's and Don'ts)

## Component Discovery and the Entity Trap
*   **[DON'T]**: Create a component design that perfectly mirrors the ERD (Entity-Relationship Diagram), resulting in components like `CustomerManager`, `OrderManager`, `ItemManager`. This is the Entity Trap and represents a framework-to-database mapping, not an architecture.
*   **[DO]**: Create components based on the Actor/Actions or Workflow approach, resulting in workflow-based components like `VideoStreamer`, `BidTracker`, `AuctionSession`, `PaymentProcessor`.

## Partitioning
*   **[DON'T]**: Smear a single business workflow (e.g., `CatalogCheckout`) across tightly coupled `Presentation`, `BusinessRules`, and `Persistence` layers if the goal is to build a microservices or domain-driven system.
*   **[DO]**: Use Domain Partitioning to group everything required for `CatalogCheckout` (UI logic, rules, data access) into a single, cohesive `Purchase` or `Checkout` component, minimizing the impact of workflow changes.

## Analyzing Architecture Characteristics for Component Splitting
*   **[DON'T]**: Bundle the auctioneer's bid entry processing and the general public's bid entry processing into a single `GlobalBidCapture` component simply because they share the same functional logic.
*   **[DO]**: Split `GlobalBidCapture` into `AuctioneerCapture` and `PublicBidCapture` because the public capture requires extreme elasticity (handling thousands of sudden requests), whereas the auctioneer capture requires absolute reliability (cannot drop the connection) with low scale.

## Architectural Quanta Evaluation
*   **[DON'T]**: Default to a distributed microservices architecture for a simple, internal HR tool with 50 predictable users where all components require standard, low-level availability and scale.
*   **[DO]**: Recognize that the HR tool represents a single architectural quantum and recommend a Monolithic Architecture (e.g., Modular Monolith) to save infrastructure costs and reduce accidental complexity.