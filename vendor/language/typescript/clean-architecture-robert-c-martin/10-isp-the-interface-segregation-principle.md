@Domain
This rule file is activated whenever the AI is tasked with designing class structures, defining interfaces, managing source code dependencies, refactoring coupled components, or integrating external architectural frameworks and libraries. It applies equally to micro-level class design and macro-level architectural component selection.

@Vocabulary
- **ISP (Interface Segregation Principle)**: The principle stating that it is harmful to depend on modules, classes, or frameworks that contain more operations or features than are actually needed.
- **Source Code Dependency**: A compile-time dependency created by import, use, or include statements that forces recompilation and redeployment if the targeted code changes.
- **Statically Typed Languages**: Languages (e.g., Java) where type declarations create rigid source code dependencies, making ISP violations a direct cause of unnecessary recompilation.
- **Dynamically Typed Languages**: Languages (e.g., Ruby, Python) where type declarations are inferred at runtime. While they do not suffer from compile-time recompilation cascades, they are still vulnerable to the architectural consequences of ISP violations.
- **Baggage**: Unused operations, features, or transitive dependencies brought into a system by depending on an overly broad module or external framework.
- **Architectural ISP**: The application of the Interface Segregation Principle at the macro-level, protecting a system (S) from the transitive risks and failures of a framework (F) and its underlying dependencies (D).

@Objectives
- Ensure that no software entity is forced to depend on methods or features it does not use.
- Prevent cascading recompilation and redeployment cycles caused by changes to unused code.
- Protect the system's architecture from external "baggage" that could cause unexpected operational failures or deployment burdens.
- Maximize system flexibility by keeping interfaces and components strictly tailored to the specific needs of their consumers.

@Guidelines
- **Class-Level Segregation**: When the AI encounters a class (`OPS`) that provides operations used by multiple different clients (`User1`, `User2`, `User3`), the AI MUST segregate those operations into distinct, client-specific interfaces (e.g., `U1Ops`, `U2Ops`, `U3Ops`).
- **Prevent Unnecessary Recompilation**: In statically typed languages, the AI MUST use segregated interfaces to break direct dependencies on concrete classes. If a client only uses `op1`, it MUST depend on an interface containing only `op1`, ensuring that changes to `op2` do not force the client to recompile or redeploy.
- **Dynamic Language Discipline**: When working in dynamically typed languages, the AI MUST NOT use the lack of strict compile-time checks as an excuse to build bloated components. The AI MUST logically segregate dependencies to prevent runtime coupling and architectural baggage.
- **Architectural Baggage Prevention**: When introducing a new framework or library to a system, the AI MUST evaluate the transitive dependencies of that framework. If the framework (`F`) depends on a heavy external system like a database (`D`) that contains features the primary system (`S`) does not use, the AI MUST warn the user of the architectural ISP violation.
- **Isolate Transitive Failures**: The AI MUST design system boundaries to ensure that failures in unused features of a transitive dependency do not cause failures in the core system. 

@Workflow
1. **Dependency Audit**: Analyze the target component, class, or architectural framework. Identify every client/user that depends on it.
2. **Usage Mapping**: Map exactly which operations, methods, or features each client actually invokes.
3. **Identify Baggage**: Highlight any methods or features within the target component that are NOT used by a specific client but are currently part of that client's dependency tree.
4. **Interface Segregation**: Extract the required operations into isolated, client-specific interfaces.
5. **Dependency Re-routing**: Refactor the clients to depend *only* on their newly created, tailored interfaces. Have the original concrete class implement these separate interfaces.
6. **Macro-Level Review**: If evaluating a framework or library, trace its dependency tree. If it brings in unnecessary external systems (e.g., a database dependency for a non-database task), recommend a leaner alternative or wrap the framework in a strict boundary to isolate the system from the framework's baggage.

@Examples (Do's and Don'ts)

[DO] Segregate operations into client-specific interfaces to prevent recompilation cascades in statically typed languages.
```java
// Segregated Interfaces
public interface U1Ops {
    void op1();
}

public interface U2Ops {
    void op2();
}

// Concrete Implementation
public class OPS implements U1Ops, U2Ops {
    public void op1() { /* implementation */ }
    public void op2() { /* implementation */ }
}

// Client depends ONLY on what it uses
public class User1 {
    private U1Ops ops;
    public User1(U1Ops ops) { this.ops = ops; }
    public void execute() { ops.op1(); }
}
```

[DON'T] Force clients to depend on a single, bloated class containing operations they do not use, causing unnecessary redeployments when unused methods change.
```java
// Bloated Class
public class OPS {
    public void op1() { /* implementation */ }
    public void op2() { /* implementation */ }
    public void op3() { /* implementation */ }
}

// Client is forced to depend on op2 and op3, even though it only uses op1
public class User1 {
    private OPS ops;
    public User1(OPS ops) { this.ops = ops; }
    public void execute() { ops.op1(); }
}
```

[DO] Evaluate architectural frameworks for unnecessary "baggage" before integrating them into the system.
```markdown
# Architecture Decision Record
**Context**: We need a simple routing library (System S).
**Decision**: We will build a custom lightweight router or use a micro-library. 
**Rationale (Architectural ISP)**: Framework F was evaluated, but it mandates a connection to Database D for unused analytics features. A failure in D would crash System S, violating ISP at the architectural level. We reject Framework F to avoid this baggage.
```

[DON'T] Blindly import massive frameworks that drag in unneeded transitive dependencies.
```javascript
// Bringing in an entire enterprise framework just for a string utility
import { StringUtils } from 'massive-enterprise-framework';

// The framework transitively initializes database connections and ORM models (Database D)
// that System S does not care about, risking redeployments and runtime failures
// if the database config is missing or the database goes down.
```