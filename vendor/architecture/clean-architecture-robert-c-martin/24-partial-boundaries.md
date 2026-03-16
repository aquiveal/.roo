# @Domain
This rule set is triggered when the AI is tasked with architectural design, creating component boundaries, implementing dependency management, structuring new features where future scaling is anticipated but currently unnecessary, or navigating trade-offs between YAGNI ("You Aren't Going to Need It") and anticipatory design. It specifically applies to tasks involving the creation, modification, or auditing of placeholder or lightweight boundaries between software components.

# @Vocabulary
*   **Full-Fledged Architectural Boundary**: An expensive architectural separation requiring reciprocal polymorphic Boundary interfaces, Input and Output data structures, and the dependency management necessary to isolate both sides into independently compilable and deployable components.
*   **Partial Boundary**: A placeholder architectural structure used when a full-fledged boundary is deemed too expensive but might be needed later. It implements parts of a boundary while avoiding the overhead of separate compilation and deployment.
*   **YAGNI**: "You Aren't Going to Need It." An Agile principle that discourages anticipatory design.
*   **Skip the Last Step**: A partial boundary strategy where reciprocal interfaces and I/O data structures are fully implemented, but they are compiled and deployed together in a single component.
*   **One-Dimensional Boundary**: A partial boundary utilizing the traditional Strategy pattern. It uses a single `ServiceBoundary` interface implemented by `ServiceImpl` classes to isolate the client, avoiding the cost of reciprocal interfaces.
*   **Facade**: The simplest partial boundary. It sacrifices dependency inversion by using a single class to list all services as methods, deploying service calls to classes the client is not supposed to access directly.
*   **Backchannel**: An anti-pattern in partial boundaries where a direct, unauthorized dependency bypasses the established interface, degrading the separation.
*   **Transitive Dependency**: A condition inherent in Facades where the client depends on the Facade, and the Facade depends on the hidden services, meaning a source code change in the services forces the client to recompile (in statically typed languages).
*   **Degradation**: The weakening of a partial boundary over time due to the lack of physical (compilation/deployment) separation, resulting in dependencies crossing the boundary in the wrong direction.

# @Objectives
*   Provide actionable pathways to implement anticipatory architectural boundaries without incurring the overhead of multi-component release management and version tracking.
*   Implement "Skip the Last Step" boundaries to preserve code-level isolation while consolidating deployment.
*   Implement "One-Dimensional Boundaries" (Strategy pattern) to establish dependency inversion with minimal interface overhead.
*   Implement "Facades" to provide a simple, centralized access point to hidden services when dependency inversion is deemed unnecessary.
*   Actively defend against boundary degradation and backchannels by enforcing strict coding discipline, as physical compilation boundaries will not be present to prevent them.

# @Guidelines
*   **Boundary Assessment**: When evaluating the need for an architectural boundary, the AI MUST weigh the cost of a full-fledged boundary (compilation/deployment separation) against the YAGNI principle. If a boundary *might* be needed later, the AI MUST propose one of the three Partial Boundary strategies.
*   **Applying "Skip the Last Step"**:
    *   The AI MUST create the reciprocal polymorphic Boundary interfaces.
    *   The AI MUST create the required Input and Output data structures.
    *   The AI MUST keep all of these structures together in the *same* deployable component (e.g., a single jar, dll, or package) to avoid version number tracking and release management burdens.
    *   The AI MUST strictly enforce dependency directions, as the lack of physical separation allows dependencies to easily cross the line in the wrong direction over time.
*   **Applying "One-Dimensional Boundaries"**:
    *   The AI MUST use the Strategy pattern.
    *   The AI MUST create a single `ServiceBoundary` interface to be used by the Client.
    *   The AI MUST create `ServiceImpl` classes that implement this interface.
    *   The AI MUST explicitly monitor the code for "backchannels" (e.g., the Client instantiating or importing `ServiceImpl` directly) and block them.
*   **Applying "Facades"**:
    *   The AI MUST create a single `Facade` class.
    *   The `Facade` MUST define methods for all required services and delegate the calls to the actual service classes.
    *   The AI MUST hide the actual service classes from the Client.
    *   The AI MUST acknowledge that this pattern sacrifices Dependency Inversion and introduces Transitive Dependencies, meaning changes to the hidden services will force the Client to recompile in static languages.
*   **Preventing Degradation**: Because partial boundaries rely on developer discipline rather than physical deployment barriers, the AI MUST act as the enforcer. The AI MUST flag any PR, code snippet, or refactor that introduces a direct dependency bypassing the partial boundary.

# @Workflow
1.  **Analyze Context**: Determine if the user request requires a new module or service integration. Evaluate if a full independently deployable component is strictly necessary right now.
2.  **Select Strategy**: If an eventual boundary is anticipated but currently too expensive, select a Partial Boundary strategy based on acceptable overhead:
    *   *High isolation needed, single deployment acceptable*: Choose "Skip the Last Step".
    *   *Medium isolation needed, Dependency Inversion required*: Choose "One-Dimensional Boundary".
    *   *Low isolation needed, Dependency Inversion sacrificed*: Choose "Facade".
3.  **Implement Structure**:
    *   For *Skip the Last Step*: Scaffold Input Data, Output Data, Input Boundary Interface, Output Boundary Interface, and Interactor, but place them in the same build target as the Client.
    *   For *One-Dimensional Boundary*: Scaffold `Client`, `ServiceBoundary` (Interface), and `ServiceImpl`. Inject `ServiceImpl` into `Client` via the interface.
    *   For *Facade*: Scaffold `Client`, `Facade`, `ServiceA`, `ServiceB`. Route `Client` calls strictly through `Facade`.
4.  **Audit for Backchannels**: Scan the resulting implementation to ensure the Client does not directly import or instantiate the concrete implementation details hidden behind the partial boundary.
5.  **Document the Placeholder**: Add comments indicating that the structure is a Partial Boundary designed for future decoupling, explicitly warning human developers not to degrade the boundary.

# @Examples (Do's and Don'ts)

### Skip the Last Step
*   **[DO]** Implement full interface and I/O separation within the same package/component.
```java
// Component: CoreSystem (Single Deployable)
public interface UseCaseInput { void execute(InputData data); }
public interface UseCaseOutput { void present(OutputData data); }
public class InputData { /*...*/ }
public class OutputData { /*...*/ }

public class Interactor implements UseCaseInput {
    private final UseCaseOutput output;
    public Interactor(UseCaseOutput output) { this.output = output; }
    public void execute(InputData data) { /*...*/ }
}
// Client and Interactor are compiled together, skipping the deployment separation step.
```
*   **[DON'T]** Allow dependencies to cross backward just because they share a component.
```java
// ANTI-PATTERN: Degradation of the partial boundary
public class Interactor implements UseCaseInput {
    // DON'T: The interactor is directly depending on the concrete WebPresenter
    // instead of the UseCaseOutput interface, ruining the partial boundary.
    private final WebPresenter presenter; 
    public Interactor(WebPresenter presenter) { this.presenter = presenter; }
}
```

### One-Dimensional Boundaries
*   **[DO]** Use the Strategy pattern to invert dependencies without reciprocal interfaces.
```java
public interface ServiceBoundary {
    void performService();
}

public class ServiceImpl implements ServiceBoundary {
    public void performService() { /* implementation */ }
}

public class Client {
    private final ServiceBoundary service;
    public Client(ServiceBoundary service) { this.service = service; }
    public void doWork() { service.performService(); }
}
```
*   **[DON'T]** Allow the client to bypass the boundary (Backchannel).
```java
// ANTI-PATTERN: Backchannel
public class Client {
    private final ServiceBoundary service;
    public Client(ServiceBoundary service) { this.service = service; }
    
    public void doWork() { 
        service.performService(); 
        
        // DON'T: Client directly accesses the concrete implementation,
        // bypassing the ServiceBoundary.
        ServiceImpl concrete = new ServiceImpl();
        concrete.performService(); 
    }
}
```

### Facades
*   **[DO]** Centralize access to hidden services, accepting transitive dependencies.
```java
class ServiceA { void doA() {} }
class ServiceB { void doB() {} }

public class Facade {
    private ServiceA a = new ServiceA();
    private ServiceB b = new ServiceB();
    
    public void operationA() { a.doA(); }
    public void operationB() { b.doB(); }
}

public class Client {
    private Facade facade = new Facade();
    public void execute() { facade.operationA(); }
}
```
*   **[DON'T]** Expose the hidden services to the client.
```java
// ANTI-PATTERN: Leaking hidden services through the Facade
public class Facade {
    private ServiceA a = new ServiceA();
    
    // DON'T: Returning the actual service class breaks the Facade boundary,
    // allowing the client to couple directly to the hidden service.
    public ServiceA getServiceA() { return a; } 
}
```