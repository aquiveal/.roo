# @Domain
This rule set activates when the AI is tasked with architectural design, system partitioning, use case analysis, component architecture definition, deployment unit planning, or managing source code dependencies for a new or existing software product.

# @Vocabulary
*   **Actor**: A primary source of change for the system, representing a specific user role or stakeholder (e.g., Viewer, Purchaser, Author, Admin).
*   **Use Case**: A specific action or feature performed by an Actor within the system.
*   **Abstract Use Case**: A base use case that sets a general policy, which is then inherited and fleshed out by more specific concrete use cases.
*   **Single Responsibility Principle (SRP)**: The architectural principle dictating that the system must be partitioned so that a change requested by or for one Actor does not affect the components of any other Actor.
*   **Dependency Rule**: The architectural rule stating that all source code dependencies must cross boundary lines in one direction only, always pointing toward the components containing the higher-level policy (e.g., Interactors).
*   **Open-Closed Principle (OCP)**: The principle used to ensure dependencies flow in the right direction (using inheritance) so that changes to low-level details do not ripple upward to affect high-level policies.
*   **Flow of Control**: The execution path of the system, typically proceeding from Controllers -> Interactors -> Presenters -> Views.
*   **Using Relationship**: A dependency that points in the same direction as the flow of control (represented by an open arrow in UML).
*   **Inheritance Relationship**: A dependency that points against the flow of control (represented by a closed arrow in UML) to invert the source code dependency.
*   **Component**: A potential independently deployable unit (e.g., a `.jar` or `.dll` file) containing a logically grouped set of architectural elements.

# @Objectives
*   To partition the system along two primary dimensions of separation: by Actors (reasons for change) and by Policy Level (rates of change).
*   To protect high-level business policies from changes in low-level details.
*   To maintain ultimate flexibility in how the system is deployed by keeping components independently deployable.
*   To ensure all cross-boundary dependencies strictly adhere to the Dependency Rule.

# @Guidelines
*   **Actor-Based Partitioning (SRP)**: The AI MUST identify all Actors during the initial analysis phase. The AI MUST strictly partition the system's use cases and components by these Actors so that a change to one Actor's workflow never impacts another Actor.
*   **Abstract Use Cases**: When the AI encounters highly similar use cases requested by different Actors (e.g., "View Catalog as Viewer" and "View Catalog as Purchaser"), the AI MUST create an Abstract Use Case (e.g., "View Catalog") to unify the shared general policy early in the analysis.
*   **Component Segregation**: The AI MUST categorize the system's architecture into distinct functional boundaries: Views, Presenters, Interactors, and Controllers. Furthermore, the AI MUST subdivide each of these categories by Actor.
*   **Abstract Components**: For Abstract Use Cases, the AI MUST create dedicated abstract components (e.g., "Catalog View", "Catalog Presenter") containing abstract classes that inheriting components will implement.
*   **Deployment Flexibility**: The AI MUST design each component as a potential independent deployable unit (e.g., an individual `.jar` or `.dll`). The AI MUST NOT prematurely hard-couple these deliverables; it MUST keep options open to deploy them independently, group them by architectural type (all views in one file, all interactors in another), or bundle them together based on how the system changes over time.
*   **Flow of Control Management**: The AI MUST route the flow of control from right to left: Input occurs at Controllers -> processed by Interactors -> formatted by Presenters -> displayed by Views.
*   **Strict Dependency Rule Enforcement**: Regardless of the flow of control, the AI MUST ensure that all source code dependencies point toward the higher-level policy (Interactors).
*   **Dependency Inversion via OCP**: When the flow of control points away from the higher-level policy (e.g., from Interactors to Presenters), the AI MUST use an Inheritance Relationship (interfaces/abstract classes) to invert the dependency, ensuring the source code dependency continues to point toward the Interactor.
*   **Using Relationships**: The AI MUST use standard Using Relationships only when the flow of control naturally points toward the higher-level policy (e.g., Controllers calling Interactors).

# @Workflow
1.  **Use Case Analysis**: Identify all Actors interacting with the system. List all concrete use cases associated with each Actor.
2.  **Abstraction Identification**: Review the list of use cases. Identify any functional overlaps or similarities between different Actors. Extract these shared behaviors into Abstract Use Cases.
3.  **Preliminary Component Architecture**: Create a matrix of components divided by architectural type (Controllers, Interactors, Presenters, Views) and by Actor. Assign abstract classes to Abstract Use Cases in their own dedicated components.
4.  **Flow of Control Routing**: Map the execution path from the user's input at the Controller, through the Interactor, to the Presenter, and out to the View.
5.  **Dependency Management**: Draw dependency lines between components. Force ALL dependencies to point toward the Interactor. If the execution path flows outward from the Interactor, introduce an interface inside the Interactor's component that the outer component (e.g., Presenter) implements.
6.  **Deployment Strategy Definition**: Define the theoretical deployment units (e.g., `.jar` files). Group components into deployable deliverables while preserving the ability to separate them later if independent deployment is required by system evolution.

# @Examples (Do's and Don'ts)

**Principle: Abstract Use Cases for Shared Policy**
*   [DO]: Create a `ViewCatalog` abstract base class/interface. Create `ViewerCatalogInteractor` and `PurchaserCatalogInteractor` that both inherit from/implement `ViewCatalog`.
*   [DON'T]: Duplicate the catalog viewing logic separately inside both the Viewer and Purchaser components without a shared abstraction, or force both actors to use the exact same concrete class, violating SRP.

**Principle: The Dependency Rule and OCP**
*   [DO]: To pass data from the `PurchaserInteractor` to the `PurchaserPresenter`, define a `PurchaserOutputBoundary` interface *inside* the Interactor component. Have the `PurchaserInteractor` call this interface. Have the `PurchaserPresenter` (in the Presenter component) implement this interface. The dependency arrow points from Presenter to Interactor.
*   [DON'T]: Have the `PurchaserInteractor` directly import and call the `PurchaserPresenter` class. This forces a high-level policy to depend on a low-level detail, violating the Dependency Rule.

**Principle: Deployment Flexibility**
*   [DO]: Architect the solution so that `Viewer_Views.jar`, `Viewer_Presenters.jar`, `Viewer_Interactors.jar`, and `Viewer_Controllers.jar` can be built entirely independently, allowing the team to later combine them into `Viewer_Frontend.jar` and `Viewer_Backend.jar` via build scripts if desired.
*   [DON'T]: Introduce cyclical dependencies or hardcoded paths between Views and Interactors that force the entire system to always be compiled and deployed as a single, inseparable monolithic file.

**Principle: Actor Isolation (SRP)**
*   [DO]: Separate `Business_Streaming_Controller` from `Individual_Streaming_Controller` if businesses get quantity discounts and individuals get download options.
*   [DON'T]: Create a single `Streaming_Controller` with `if (user == business) { ... } else { ... }` blocks that will require modification every time either the business or individual streaming rules change.