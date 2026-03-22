# @Domain
This rule file MUST be activated whenever the AI is tasked with architectural design, system restructuring, repository initialization, refactoring of dependencies, separating business logic from UI/Database details, dividing a monolithic codebase into modules or microservices, or resolving code duplication across different functional boundaries. 

# @Vocabulary
*   **Screaming Architecture**: An architectural state where the top-level structure of the system clearly and immediately reveals the intent and use cases of the application, rather than the frameworks or tools being used.
*   **Conway's Law**: The principle that a system's design will inevitably reflect the communication structures of the organization that builds it.
*   **Immediate Deployment**: A deployment state requiring a single action to deploy, with zero manual configuration scripts, directory creation, or property file tweaks.
*   **Horizontal Layers**: The separation of software components by technical concern and rate of change, specifically: UI, Application-Specific Business Rules, Application-Independent Business Rules, and Database.
*   **Vertical Slices**: The separation of software components by use case (e.g., Add Order vs. Delete Order) cutting through the horizontal layers.
*   **True Duplication**: Code that changes for the exact same reasons and at the exact same rates. Eliminating this is required.
*   **Accidental (False) Duplication**: Code that happens to look identical currently but serves different actors or use cases, and will evolve along different paths. Unifying this is an anti-pattern.
*   **Decoupling Modes**: The physical separation mechanisms of components.
    *   **Source-Level Decoupling**: Components execute in the same address space (a monolith) and communicate via simple function calls. Changes to one module do not force recompilation of others.
    *   **Deployment-Level Decoupling**: Components are partitioned into independently deployable units (jar files, DLLs, shared libraries). Communication is via function calls, interprocess communications, or shared memory.
    *   **Service-Level Decoupling**: Execution units are entirely independent, separated to the level of data structures, and communicate solely via network packets (e.g., micro-services).

# @Objectives
*   Support the use cases and intent of the system by making them the most visible, first-class elements of the architecture.
*   Support system operation by leaving the threading, processing, and service models as options that can be transitioned easily without altering core logic.
*   Facilitate independent development by strictly isolating components so multiple teams can work simultaneously without interference.
*   Achieve "Immediate Deployment" via rigid component partitioning and isolation.
*   Preserve options (databases, web frameworks, delivery mechanisms) for as long as possible by preventing their pollution into the core business logic.
*   Protect the majority of the source code from changes in the chosen decoupling mode (Source, Deployment, or Service).

# @Guidelines

*   **Architecture and Intent Visibility**
    *   When organizing top-level files or directories, the AI MUST use names that describe the use cases and behaviors of the system (e.g., `OrderFulfillment`, `UserAuthentication`), NOT the technical implementation (e.g., `Controllers`, `Models`, `Views`).
*   **Operation and Scaling Constraints**
    *   The AI MUST NOT hardcode assumptions about how components are executed (e.g., single process, multi-threaded, or micro-service). Communication between high-level components MUST be abstracted so the decoupling mode can be swapped later without touching business logic.
*   **Development and Conway's Law**
    *   The AI MUST partition the system into well-isolated, independently developable components that can be handed off to independent teams without causing merge conflicts or cross-team dependencies.
*   **Deployment Independence**
    *   The AI MUST design the system build and deployment pipeline to be a single action. 
    *   The AI MUST ensure that hot-swapping layers and use cases in a running system is possible by preventing hard dependencies between independently deployable components.
*   **Horizontal Layering (Separation of Concerns)**
    *   The AI MUST enforce a strict separation of elements that change for different reasons.
    *   The AI MUST decouple UI logic from business rules.
    *   The AI MUST decouple Application-Specific Business Rules (e.g., input validation) from Application-Independent Business Rules (e.g., interest calculation).
    *   The AI MUST isolate the Database and schema completely from business rules.
*   **Vertical Slicing (Decoupling Use Cases)**
    *   The AI MUST separate the UI, business rules, and database aspects of one use case from the UI, business rules, and database aspects of a different use case.
    *   When adding a new use case, the AI MUST ensure it does not interfere with the code of older use cases.
*   **Handling Duplication (The Knee-Jerk Elimination Trap)**
    *   When the AI encounters identical blocks of code or identical data structures, it MUST determine if the duplication is True or Accidental before attempting to DRY it out.
    *   If the identical code belongs to two different use cases with different UI screens or different actors, the AI MUST NOT unify them.
    *   The AI MUST NOT pass Database records directly to the UI. The AI MUST create a separate View Model for the UI, even if the fields are currently 100% identical to the Database record.
*   **Decoupling Modes Progression**
    *   The AI MUST default to designing components with the *capacity* to become independent services, but MUST initially leave them in the same address space (Source-Level Decoupling).
    *   The AI MUST NOT introduce Service-Level Decoupling (micro-services, network boundaries) prematurely.
    *   The AI MUST ensure that transitioning from a monolith to micro-services (or vice versa) requires minimal changes to the source code of the business rules.

# @Workflow
1.  **Use Case Extraction**: Identify the actors and the distinct use cases of the system.
2.  **Top-Level Structuring (Screaming Architecture)**: Scaffold the root directories using the names of the identified use cases.
3.  **Horizontal Partitioning**: Within each use case, create strict boundaries for UI, Application-Specific Rules, Application-Independent Rules, and Database access.
4.  **Interface Abstraction**: Define data structures and boundaries (interfaces/ports) between the horizontal layers to ensure dependencies point inward toward business rules.
5.  **Duplication Verification**: Audit the layers for shared data structures. If a database entity is being used as a UI view model, immediately duplicate the structure, decouple them, and introduce a mapping mechanism.
6.  **Decoupling Mode Configuration**: Configure the build system to enforce Source-Level or Deployment-Level decoupling (e.g., separate modules, packages, or assemblies), ensuring no network/service layers are hardcoded into the business logic.
7.  **Deployment Verification**: Ensure the resulting architecture can be built and deployed via a single automated action.

# @Examples (Do's and Don'ts)

**Principle: Screaming Architecture (Use Case Visibility)**
*   [DO] Name top-level directories based on business intent: `/Checkout`, `/Inventory`, `/UserManagement`.
*   [DON'T] Name top-level directories based on frameworks or patterns: `/Controllers`, `/Models`, `/Views`, `/SpringConfigs`.

**Principle: Accidental Duplication (View Models vs. DB Entities)**
*   [DO] Create distinct classes for the Database and the UI, even if they match exactly:
    ```java
    // Database Entity
    public class UserRecord { public String name; public String email; }
    
    // UI View Model
    public class UserProfileView { public String name; public String email; }
    
    // Mapping logic resides in an Interface Adapter layer
    ```
*   [DON'T] Reuse the database entity in the presentation layer to save time:
    ```java
    // Anti-pattern: UI directly importing Database record
    import db.entities.UserRecord;
    public class UserProfileController {
        public void render(UserRecord record) { ... }
    }
    ```

**Principle: Vertical Slicing (Decoupling Use Cases)**
*   [DO] Isolate the UI logic of different use cases so they can evolve independently:
    ```javascript
    // AddOrderUseCase UI
    import { AddOrderPresenter } from './AddOrderPresenter';
    // DeleteOrderUseCase UI
    import { DeleteOrderPresenter } from './DeleteOrderPresenter';
    ```
*   [DON'T] Create a massive, unified "Order UI" component that handles adding, deleting, and modifying, tightly coupling use cases that change at different rates.

**Principle: Decoupling Modes (Leaving Service Options Open)**
*   [DO] Communicate between components using interfaces that can be implemented locally or over a network later:
    ```csharp
    public interface IOrderProcessor {
        OrderResult Process(OrderRequest request);
    }
    // Initially injected as a local class instance (Source-Level)
    // Can later be swapped for an HttpClient implementation (Service-Level) without touching business logic.
    ```
*   [DON'T] Hardcode network/HTTP logic directly into the business rules, forcing the system to always run as a micro-service:
    ```csharp
    // Anti-pattern
    public class OrderManager {
        public void ProcessOrder() {
            var client = new HttpClient();
            client.PostAsync("http://microservice/process", ...);
        }
    }
    ```