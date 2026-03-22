# @Domain

This rule set applies to all architecture design, system refactoring, component structuring, and dependency management tasks. It triggers specifically when the AI is asked to add new features, extend system behavior, alter data presentation/storage, or draw boundary lines between business rules and peripheral concerns.

# @Vocabulary

*   **OCP (The Open-Closed Principle)**: The principle stating that a software artifact should be open for extension but closed for modification. The behavior of a software artifact ought to be extendible without having to modify that artifact.
*   **Level**: A conceptual metric used to create a hierarchy of protection. Higher-level concepts contain central policies; lower-level concepts contain peripheral details.
*   **Interactor**: The component containing the highest-level policies and business rules. It is the central concern of the application and must receive the highest level of protection from change.
*   **Controller**: A peripheral component that handles input and directs the Interactor. It is lower-level than the Interactor, but higher-level than Presenters and Views.
*   **Presenter**: A component responsible for formatting data for presentation. It is lower-level than the Controller and Interactor, but higher-level than the View.
*   **View**: One of the lowest-level concepts in the system, dealing strictly with data presentation. It receives the least protection.
*   **Directional Control**: The architectural technique of utilizing interfaces to invert source code dependencies so they point in the correct direction (toward higher-level components) regardless of the flow of control.
*   **Information Hiding**: The architectural technique of introducing interfaces to protect outer, lower-level components from knowing too much about the internals of inner, higher-level components.
*   **Transitive Dependency**: An architectural violation where a software entity is forced to depend on things it does not directly use.

# @Objectives

*   Reduce the amount of existing code that must change when implementing new requirements to the barest minimum (ideally, zero).
*   Ensure that the system is extended strictly by adding new code rather than modifying existing code.
*   Partition processes into distinct classes and separate those classes into independently deployable components.
*   Establish a strict, unidirectional dependency hierarchy where lower-level components are fully dependent upon higher-level components.
*   Protect central business logic (Interactors) completely from changes in peripheral concerns (Views, Presenters, Controllers, Databases).

# @Guidelines

*   **Extension over Modification**: When asked to implement a new feature (e.g., turning web data into a printed report), the AI MUST achieve this by writing new classes and components, NOT by altering existing, functioning business logic.
*   **SRP as a Prerequisite**: The AI MUST first apply the Single Responsibility Principle to separate things that change for different reasons (e.g., calculating data vs. presenting data) before organizing OCP dependencies.
*   **Unidirectional Component Relationships**: The AI MUST assure that all component relationships and boundary lines are crossed in one direction only.
*   **Dependency Direction dictates Protection**: The AI MUST point all source code dependencies toward the components that require protection from change. (e.g., If Component A must be protected from changes in Component B, Component B MUST depend on Component A).
*   **Hierarchy of Protection**: The AI MUST structure dependencies to enforce the following hierarchy, protecting the highest levels most rigorously:
    1.  `Interactor` (Most protected, depends on nothing)
    2.  `Controller` (Protected from Presenters and Views)
    3.  `Presenter` (Protected from Views)
    4.  `View` (Least protected, depends on Presenters)
*   **Directional Control via Interfaces**: If the execution flow requires a high-level component to call a low-level component (e.g., Interactor fetching data from a Database), the AI MUST NOT create a direct source code dependency. Instead, the AI MUST place an interface in the high-level component and have the low-level component implement it.
*   **Information Hiding against Transitive Dependencies**: The AI MUST hide the internals of high-level components from low-level components. If a Controller interacts with an Interactor, the AI MUST provide an interface tailored to the Controller's needs to prevent the Controller from gaining transitive dependencies on internal entities.

# @Workflow

1.  **Analyze the Request**: Evaluate the new feature or change requested. Identify the distinct responsibilities involved (e.g., data calculation vs. data formatting/presentation).
2.  **Partition into Classes**: Divide the processing steps into separate classes based on their distinct responsibilities.
3.  **Group into Components**: Assign the partitioned classes into designated architectural components (`Interactor`, `Controller`, `Presenter`, `View`, `Database`).
4.  **Determine Levels**: Rank the components based on the concept of "level". Assign the core business rules to the highest level (`Interactor`) and the peripheral details (UI, Database) to the lowest levels.
5.  **Draw Unidirectional Dependencies**: Map source code dependencies so that lower-level components depend on higher-level components. Validate that the `Interactor` has zero outbound dependencies.
6.  **Apply Directional Control**: Locate any instances where the runtime flow of control points from a higher-level component to a lower-level component. Inject an interface into the higher-level component to invert the source code dependency.
7.  **Apply Information Hiding**: Locate points where lower-level components trigger higher-level components. Inject an interface to hide the internal data structures of the higher-level component, ensuring the lower-level component only knows what it directly uses.
8.  **Final Validation**: Verify that the new behavior is achieved entirely by the newly added code, leaving the existing high-level components completely unmodified.

# @Examples (Do's and Don'ts)

**Principle: Directional Control (Inverting Dependencies to protect the Interactor)**

*   **[DO]**: Define a `FinancialDataGateway` interface within the `Interactor` component. Have the `FinancialDataMapper` class inside the `Database` component implement this interface. The `Interactor` calls the interface. The `Database` component source code depends on the `Interactor` component.
*   **[DON'T]**: Have the `Interactor` directly call the `FinancialDataMapper` class. This forces the `Interactor` component to have a source code dependency on the `Database` component, violating OCP by forcing the `Interactor` to change if the database implementation changes.

**Principle: Information Hiding (Preventing Transitive Dependencies)**

*   **[DO]**: Create a `FinancialReportRequester` interface that the `FinancialReportController` uses to trigger the `Interactor`. The interface exposes only the exact methods the Controller needs.
*   **[DON'T]**: Allow the `FinancialReportController` to directly access the `Interactor` class and its internal `FinancialEntities`. This gives the Controller a transitive dependency on the entities, coupling the Controller to changes in business objects it does not directly use.

**Principle: Hierarchy of Protection (Presenters and Views)**

*   **[DO]**: Separate the presentation logic into two components: A `Presenter` that formats the data (e.g., making negative numbers red, adding parentheses), and a `View` that renders it (e.g., printing to a web page or a PDF). Make the `View` component depend on the `Presenter` component.
*   **[DON'T]**: Combine the formatting of the financial data and the physical rendering of the web page into a single class or component. This exposes the formatting logic to modifications every time the physical rendering mechanism (e.g., screen vs. print) changes.