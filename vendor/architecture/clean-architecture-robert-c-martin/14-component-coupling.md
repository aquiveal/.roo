# @Domain

These rules ACTIVATE whenever the AI is tasked with architectural design, module organization, package dependency management, refactoring of existing component structures, resolving circular dependencies, or reviewing system-level build and deployment diagrams. The rules apply specifically to macro-level structural organization (components, packages, namespaces, shared libraries) rather than micro-level class implementation.

# @Vocabulary

*   **Component**: The smallest unit of deployment in a system (e.g., `.jar` files, `.dll` files, `.gem` files, or deployable directories).
*   **The Morning After Syndrome**: The phenomenon where a developer's working code breaks overnight because someone else modified a dependent component.
*   **The Weekly Build**: An anti-pattern where developers work in isolation for four days and pay a massive integration penalty on the fifth day, often leading to lengthening build schedules and delayed integration.
*   **ADP (Acyclic Dependencies Principle)**: The principle stating there must be absolutely no cycles in the component dependency graph.
*   **DAG (Directed Acyclic Graph)**: A directed graph with no directed cycles. The required state of any component dependency structure.
*   **The "Jitters"**: The natural, volatile growth and jittering of a component dependency structure as new requirements are added, requiring constant monitoring and cycle-breaking.
*   **SDP (Stable Dependencies Principle)**: The principle stating that dependencies must always point in the direction of stability.
*   **Stability**: A measure of how much work is required to make a change to a component. A component with many incoming dependencies is highly stable (hard to change); a component with zero incoming dependencies is unstable (easy to change).
*   **Fan-in**: The number of classes outside a component that depend on classes within the component.
*   **Fan-out**: The number of classes inside a component that depend on classes outside the component.
*   **Instability ($I$) Metric**: Calculated as $I = \frac{\text{Fan-out}}{\text{Fan-in} + \text{Fan-out}}$. $I=0$ means maximally stable. $I=1$ means maximally unstable.
*   **SAP (Stable Abstractions Principle)**: The principle stating that a component should be as abstract as it is stable.
*   **Abstractness ($A$) Metric**: Calculated as $A = \frac{N_a}{N_c}$, where $N_a$ is the number of abstract classes/interfaces in the component, and $N_c$ is the total number of classes in the component. $A=0$ means completely concrete. $A=1$ means completely abstract.
*   **The Main Sequence**: The ideal locus of points on an $A/I$ graph (a line connecting $(1,0)$ and $(0,1)$) where a component is neither "too abstract" for its stability nor "too unstable" for its abstractness ($A + I \approx 1$).
*   **Zone of Pain**: The region near $(I=0, A=0)$ representing highly stable, concrete components. Volatile components here cause extreme architectural pain (e.g., rigid database schemas).
*   **Zone of Uselessness**: The region near $(I=1, A=1)$ representing highly abstract, unstable components with no dependents. These are unused, leftover detritus.
*   **Distance ($D$) Metric**: Calculated as $D = |A + I - 1|$. Measures how far a component is from the Main Sequence. Range is $[0, 1]$.

# @Objectives

*   Eliminate the "Morning After Syndrome" by strictly maintaining a Directed Acyclic Graph (DAG) for all component dependencies.
*   Acknowledge that component structures map buildability and maintainability, not functional requirements, and allow them to evolve naturally from the bottom up.
*   Isolate volatile components from stable components to prevent ripple effects during routine maintenance.
*   Ensure that components containing high-level policies are maximally stable and highly abstract.
*   Ensure that components containing low-level details are highly unstable and highly concrete.
*   Balance every component's Abstractness and Instability to keep it on or near the "Main Sequence."

# @Guidelines

*   **Zero Dependency Cycles**: The AI MUST NEVER introduce a circular dependency between components. If a user request results in a cycle, the AI MUST proactively identify and break it.
*   **Breaking Cycles (Method 1 - DIP)**: To break a cycle between Component A and Component B, the AI MUST apply the Dependency Inversion Principle (e.g., define an interface in A that is implemented by B, thereby inverting the source code dependency).
*   **Breaking Cycles (Method 2 - Extraction)**: Alternatively, the AI MUST create a new Component C, extract the classes that both A and B depend on into C, and make both A and B depend on C.
*   **Top-Down Design Prohibition**: The AI MUST NOT attempt to design the entire component dependency structure upfront. The structure MUST evolve organically to mitigate build/maintenance issues as classes and modules accumulate.
*   **Dependency Direction**: The AI MUST point all dependencies toward components with a lower $I$ metric (higher stability).
*   **High-Level Policy Placement**: The AI MUST place enterprise and business rules into components with $I=0$ (stable).
*   **Abstract Components for Static Languages**: In statically typed languages (Java, C#), the AI MUST utilize Abstract Components (components containing only interfaces/abstract classes) to serve as stable, highly abstract targets for less stable components to depend on.
*   **Dynamic Language Exemption**: In dynamically typed languages (Ruby, Python), the AI MUST recognize that abstract components and formal interfaces do not exist in the same way, making dependency inversion simpler and less strictly tied to interface inheritance.
*   **Avoid the Zone of Pain**: The AI MUST NOT place volatile, frequently changing code into components with $I=0$ and $A=0$. (Exception: Universally used, non-volatile components like the `String` library are permitted here).
*   **Avoid the Zone of Uselessness**: The AI MUST NOT generate interfaces or abstract classes in components with $I=1$ (zero incoming dependencies).
*   **Distance Monitoring**: The AI MUST strive to keep the $D$ metric of any component as close to $0$ as possible.
*   **Historical Tracking**: When auditing architecture over time, the AI MUST calculate the variance and mean of $D$ metrics across components and flag any component whose $D$ metric creeps outward over successive releases.

# @Workflow

When designing, refactoring, or evaluating the component architecture of a system, the AI MUST follow this exact algorithmic process:

1.  **Graph Construction & Cycle Detection**:
    *   Map all components and their source code dependencies.
    *   Traverse the graph to detect cycles.
    *   If a cycle is detected, halt standard processing and immediately apply cycle-breaking techniques (DIP or extraction to a new component).
2.  **Stability Calculation ($I$)**:
    *   For every component, count external classes depending on it (Fan-in).
    *   Count internal classes depending on external classes (Fan-out).
    *   Calculate $I = \frac{\text{Fan-out}}{\text{Fan-in} + \text{Fan-out}}$.
3.  **SDP Verification**:
    *   Check every dependency edge. Ensure that the dependency arrow points from a component with a higher $I$ value to a component with a lower $I$ value.
    *   If $I_{depender} \leq I_{dependee}$, the AI MUST restructure the dependency to protect the stable component.
4.  **Abstractness Calculation ($A$)**:
    *   For every component, count total classes ($N_c$) and abstract classes/interfaces ($N_a$).
    *   Calculate $A = \frac{N_a}{N_c}$.
5.  **SAP & Distance Evaluation ($D$)**:
    *   Calculate $D = |A + I - 1|$ for every component.
    *   If $D > 0.5$ and the component approaches $(0,0)$, flag as "Zone of Pain". Suggest converting concrete classes to interfaces or isolating volatile logic.
    *   If $D > 0.5$ and the component approaches $(1,1)$, flag as "Zone of Uselessness". Suggest removing unused abstractions.
6.  **Continuous Jitter Management**:
    *   As new features are requested, repeat steps 1-5. Accept that the graph will grow and "jitter"; prioritize DAG integrity and Main Sequence proximity over maintaining the original shape.

# @Examples (Do's and Don'ts)

### Principle: Acyclic Dependencies Principle (ADP)
*   **[DO]**: Use an interface to invert a dangerous dependency.
    ```java
    // Component: Entities
    package entities;
    public interface Permissions {
        boolean isAllowed(User u);
    }
    public class User {
        public void doTask(Permissions p) { ... }
    }

    // Component: Authorizer (Depends on Entities)
    package authorizer;
    import entities.Permissions;
    public class AuthorizerImpl implements Permissions {
        public boolean isAllowed(User u) { ... }
    }
    ```
*   **[DON'T]**: Create a circular dependency where Entities depends on a concrete Authorizer, and Authorizer depends on Entities.
    ```java
    // Component: Entities (ANTI-PATTERN: Depends on Authorizer)
    import authorizer.AuthorizerImpl; 
    public class User {
        public void doTask() { new AuthorizerImpl().isAllowed(this); }
    }

    // Component: Authorizer (ANTI-PATTERN: Depends on Entities)
    import entities.User;
    public class AuthorizerImpl {
        public boolean isAllowed(User u) { ... }
    }
    ```

### Principle: Stable Dependencies Principle (SDP)
*   **[DO]**: Ensure a volatile GUI component ($I \approx 1$) depends on a stable core business component ($I \approx 0$).
    ```text
    [GUI Component] (Fan-in: 0, Fan-out: 4 -> I = 1.0)
          |
          v
    [Business Rules Component] (Fan-in: 4, Fan-out: 0 -> I = 0.0)
    ```
*   **[DON'T]**: Allow a stable business component to depend on a highly volatile UI or framework component, forcing the stable component to change when the UI changes.
    ```text
    [Business Rules Component] (Stable)
          |  <-- ANTI-PATTERN: Dependency points to higher instability
          v
    [GUI Component] (Unstable)
    ```

### Principle: Stable Abstractions Principle (SAP)
*   **[DO]**: Make a highly stable component ($I=0$) maximally abstract ($A=1$) by populating it entirely with interfaces and abstract classes, placing it on the Main Sequence ($D=0$).
    ```java
    // Component: BusinessInterfaces (I=0, A=1)
    public interface UseCase { void execute(); }
    public interface Repository { void save(); }
    ```
*   **[DON'T]**: Create a highly stable component ($I=0$) that is entirely concrete ($A=0$), placing it in the Zone of Pain where necessary changes will break all dependent modules.
    ```java
    // Component: CoreBusiness (I=0, A=0) -> ZONE OF PAIN
    // 50 other components depend on this, but it contains volatile concrete SQL queries!
    public class DatabaseInteractor {
        public void saveToDb() {
            executeSql("INSERT INTO users..."); // Highly volatile, impossible to extend
        }
    }
    ```