# @Domain
These rules MUST be activated whenever the AI is tasked with creating, refactoring, or modifying system architecture boundaries, module dependencies, object instantiation logic, or class inheritance structures. This applies to both statically typed languages (e.g., Java, C#) and dynamically typed languages (e.g., Ruby, Python) where cross-module function calls or object creations are being defined.

# @Vocabulary
- **DIP (Dependency Inversion Principle)**: The architectural principle dictating that the most flexible systems are those in which source code dependencies refer only to abstractions, not to concretions.
- **Concretion / Concrete Module**: Any module or class in which the functions being called are implemented.
- **Volatile Concrete Element**: A concrete module or class that is actively being developed and is undergoing frequent change.
- **Stable Element**: A concrete facility, such as an operating system API or platform standard library (e.g., the `String` class in Java), that rarely changes and is tightly controlled. 
- **Abstract Factory**: A design pattern used to manage the source code dependency of object creation, ensuring the application relies on an interface to create objects rather than the concrete object definition itself.
- **Architectural Boundary**: The dividing line separating the abstract component (high-level business rules) from the concrete component (implementation details). All source code dependencies must cross this boundary pointing in one direction: toward the abstract side.
- **Main Component**: The lowest-level concrete component in the system that houses the `main` function (or initialization equivalent). It is the only component permitted to explicitly instantiate volatile concrete classes and factory implementations.

# @Objectives
- Ensure that source code dependencies (`use`, `import`, `require`, or `include` statements) refer strictly to interfaces, abstract classes, or abstract declarations.
- Prevent high-level policy code from depending on volatile low-level implementation details.
- Reduce interface volatility by adding functionality to implementations without modifying the underlying interfaces.
- Isolate the unavoidable violations of DIP (such as concrete object creation) into a designated, restricted component (Main).

# @Guidelines
- **Abstract Over Volatile**: The AI MUST NOT refer to volatile concrete classes. All references MUST point to abstract interfaces.
- **Language Nuances**: 
  - For statically typed languages: Force the creation of interfaces or abstract classes for all volatile dependencies.
  - For dynamically typed languages: Prevent source code dependencies from referring to concrete modules (modules where functions are actually implemented).
- **Tolerate Stable Concretions**: The AI MAY allow direct dependencies on stable background facilities (e.g., standard library strings, core platform APIs) as they are relied upon not to change.
- **Prohibit Volatile Derivation**: The AI MUST NOT derive from (inherit from) volatile concrete classes. Inheritance is the strongest and most rigid source code relationship; it must be restricted to interfaces or highly stable abstract classes.
- **Prohibit Concrete Overrides**: The AI MUST NOT override concrete functions. Overriding a concrete function inherits its source code dependencies. Instead, the AI MUST make the function abstract and create multiple distinct implementations.
- **Name Hiding**: The AI MUST NEVER mention the name of anything concrete and volatile within high-level or abstract components.
- **Factory Encapsulation**: Whenever the creation of a volatile concrete object is required, the AI MUST handle it via the Abstract Factory pattern to prevent source code dependencies on the concrete definition.
- **Invert Control vs. Dependencies**: The AI MUST structure the system so that the flow of control crosses the architectural boundary in the opposite direction of the source code dependencies.
- **Isolate DIP Violations**: The AI MUST gather all necessary DIP violations (such as the actual instantiation of the factory itself) into a single concrete component, typically named `Main`.

# @Workflow
1. **Volatility Assessment**: When introducing a dependency, evaluate whether the target module is a stable platform facility or a volatile, actively developed concretion.
2. **Abstraction Generation**: If the dependency is volatile, extract its public methods into an interface or abstract class.
3. **Dependency Re-routing**: Change all `import`, `include`, or `require` statements in the calling class to target the newly created abstraction, not the concrete implementation.
4. **Factory Implementation**: If the calling class needs to instantiate the volatile dependency, create a `ServiceFactory` interface with a creation method (e.g., `makeSvc`).
5. **Concrete Factory Provision**: Create a `ServiceFactoryImpl` class that implements the factory interface and instantiates the concrete class. 
6. **Boundary Enforcement**: Move the abstract factory, the abstract service interface, and the calling application logic into the "Abstract Component". Move the concrete implementations into the "Concrete Component".
7. **Main Wiring**: Within the `Main` component (or equivalent startup module), instantiate the `ServiceFactoryImpl` and provide it to the application (via dependency injection or a global variable), allowing the application to create instances without knowing their concrete types.

# @Examples (Do's and Don'ts)

**[DO]**
Provide a flexible architecture where object creation is handled via an Abstract Factory, protecting the Application from concrete dependencies.
```java
// --- ABSTRACT COMPONENT (High-Level Policy) ---
package abstract_component;

public interface Service {
    void execute();
}

public interface ServiceFactory {
    Service makeSvc();
}

public class Application {
    private final ServiceFactory factory;

    // Dependency Injection of the factory abstraction
    public Application(ServiceFactory factory) {
        this.factory = factory;
    }

    public void run() {
        // Application creates the service without knowing the concretion
        Service svc = factory.makeSvc();
        svc.execute();
    }
}

// --- CONCRETE COMPONENT (Implementation Details) ---
package concrete_component;

import abstract_component.Service;
import abstract_component.ServiceFactory;

public class ConcreteImpl implements Service {
    @Override
    public void execute() {
        System.out.println("Executing concrete implementation.");
    }
}

public class ServiceFactoryImpl implements ServiceFactory {
    @Override
    public Service makeSvc() {
        return new ConcreteImpl();
    }
}

// --- MAIN COMPONENT (The Dirty Detail) ---
package main_component;

import abstract_component.Application;
import concrete_component.ServiceFactoryImpl;

public class Main {
    public static void main(String[] args) {
        // DIP violation isolated strictly to Main
        ServiceFactoryImpl factory = new ServiceFactoryImpl();
        Application app = new Application(factory);
        app.run();
    }
}
```

**[DON'T]**
Directly reference, instantiate, or derive from volatile concrete classes within high-level application logic.
```java
// ANTI-PATTERN: Application directly depends on ConcreteImpl
package app;

// DON'T: Importing a volatile concretion directly into high-level policy
import concrete_component.ConcreteImpl; 

public class Application {
    public void run() {
        // DON'T: Mentioning the name of a volatile concrete class
        // DON'T: Instantiating the concrete class directly
        ConcreteImpl svc = new ConcreteImpl();
        svc.execute();
    }
}

// ANTI-PATTERN: Overriding concrete functions
public class SpecializedImpl extends ConcreteImpl {
    // DON'T: Deriving from a volatile concrete class
    @Override
    public void execute() {
        // DON'T: Overriding a concrete function, inheriting its dependencies
        super.execute();
        System.out.println("Specialized execution.");
    }
}
```