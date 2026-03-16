# @Domain
These rules MUST be activated when the AI is tasked with designing system architecture, creating package or folder structures, defining module boundaries, setting access modifiers (e.g., `public`, `private`, `internal`, `package-protected`), refactoring monolithic codebases, or implementing separation of concerns in object-oriented programming languages (specifically Java, C#, or similar languages with package/assembly level visibility).

# @Vocabulary
- **Package by Layer**: A horizontal slicing of code based on technical function (e.g., web, business logic, persistence). 
- **Package by Feature**: A vertical slicing of code based on related features, domain concepts, or aggregate roots, placing all related types into a single package.
- **Ports and Adapters (Hexagonal Architecture)**: An architecture comprising an "inside" (domain concepts) and an "outside" (infrastructure, UI, database), where the outside strictly depends on the inside.
- **Package by Component**: A hybrid architectural approach that bundles related business logic and persistence code into a single package behind a clean, coarse-grained public interface, hiding the implementation details.
- **Component**: A grouping of related functionality behind a nice clean interface, which resides inside an execution environment like an application.
- **Relaxed Layered Architecture**: An anti-pattern where higher layers bypass their immediate adjacent lower layer to directly access deeper layers (e.g., a Web Controller directly accessing a Database Repository).
- **Ubiquitous Domain Language**: Naming conventions used in the domain "inside" that reflect business concepts rather than technical implementation (e.g., naming an interface `Orders` instead of `OrdersRepository`).
- **Organization vs. Encapsulation**: The distinction between using packages merely as folders (grouping public types) versus using them as true encapsulation boundaries (hiding types using restrictive access modifiers).
- **Périphérique Anti-pattern**: An architectural failure occurring when all infrastructure code (web, database) is grouped in a single source tree, allowing infrastructure elements to bypass the domain and call each other directly (e.g., Web calling Database without traversing the Domain).

# @Objectives
- The AI MUST bridge the gap between high-level architectural intent and low-level implementation details.
- The AI MUST use the programming language's compiler to enforce architectural boundaries via strict access modifiers, rather than relying on developer discipline or post-compilation static analysis tools.
- The AI MUST prevent "Relaxed Layered Architectures" and "Big Balls of Mud" by hiding repositories and persistence implementations from web/presentation controllers.
- The AI MUST map intended design paradigms directly to source code structures, ensuring packages act as encapsulation boundaries, not just organizational folders.

# @Guidelines

## Access Modifiers and Encapsulation
- The AI MUST NOT apply the `public` access modifier instinctively or by default to classes, interfaces, or structs.
- The AI MUST default to the most restrictive access modifier available (e.g., `package-private` in Java, `internal` in C#).
- The AI MUST ONLY use the `public` modifier when a type MUST be consumed by a class outside of its immediate package/assembly boundary.
- If all types in a system are public, the AI MUST recognize this as an architectural failure, as the packaging provides no encapsulation.

## Architectural Styles & Implementations
- **When using Package by Layer**: The AI MUST make service and repository interfaces `public`, but MUST make the implementation classes (e.g., `OrdersServiceImpl`, `JdbcOrdersRepository`) `package-protected`/`internal`.
- **When using Package by Feature**: The AI MUST make the entry point (e.g., the Web Controller) `public`, but MUST make all other types in the package (services, repositories, entities) `package-protected`/`internal` to prevent external coupling.
- **When using Ports and Adapters**: The AI MUST use Ubiquitous Domain Language for the "inside" (e.g., use `Orders`, not `OrdersRepository`). The domain interfaces MUST be `public`, but infrastructure implementation classes MUST be `package-protected`/`internal` and injected at runtime.
- **When using Package by Component (Preferred for Monoliths)**: The AI MUST expose ONLY a single coarse-grained interface (e.g., `OrdersComponent`) as `public`. All inner workings, including business logic interfaces, persistence interfaces, and their implementations, MUST be `package-protected`/`internal`.

## Preventing Anti-Patterns
- **Prevent Relaxed Layers**: The AI MUST NOT allow Web Controllers or UI elements to directly inject or access Repositories or Data Access Objects. All interactions MUST route through the designated Component interface or Service layer.
- **Prevent the Périphérique Anti-pattern**: If using a two-tree structure (Domain and Infrastructure), the AI MUST ensure that infrastructure code in one area (e.g., web) CANNOT directly invoke infrastructure code in another area (e.g., database). 

## Decoupling Modes
- The AI MUST evaluate the use of Module Frameworks (e.g., Java 9 module system, OSGi) to explicitly distinguish between `public` types and `published` (exported) types.
- If appropriate for project complexity, the AI MUST decouple dependencies at the source code level by splitting code across different source code trees/build modules (e.g., separate Maven/Gradle projects for Domain, Web, and Persistence).

# @Workflow
When tasked with creating or refactoring a feature, the AI MUST follow this exact algorithmic process:

1. **Determine Architectural Context**: Identify whether the system uses Package by Layer, Package by Feature, Ports and Adapters, or Package by Component. (If unstated, recommend Package by Component for monolithic structures).
2. **Define the Ubiquitous Language**: Name the domain concepts based on business terminology, omitting technical jargon from the core domain (e.g., `Catalog` instead of `CatalogDataService`).
3. **Map the Structures**: Group the classes into packages/namespaces according to the chosen architectural style.
4. **Apply Default Encapsulation**: Mark EVERY class and interface as `package-private` (Java) or `internal` (C#) by default.
5. **Selectively Expose Boundaries**: Identify the specific entry points required by consumers outside the package. Change ONLY those specific entry points to `public`.
6. **Compiler Enforcement Check**: Analyze the dependency graph. Ensure that a junior developer attempting to inject a database repository directly into a web controller would receive a compilation error due to access modifiers.
7. **Anti-Pattern Check**: Scan for the Périphérique Anti-pattern. If infrastructure components reside in the same source tree, verify that access modifiers prevent cross-infrastructure communication.

# @Examples (Do's and Don'ts)

## Encapsulation in Package by Component
[DO]
```java
package com.mycompany.myapp.orders;

// PUBLIC: The only entry point exposed to the outside world (e.g., Web Controllers)
public interface OrdersComponent {
    void placeOrder(OrderRequest request);
}

// PACKAGE-PRIVATE: Implementation is hidden
class OrdersComponentImpl implements OrdersComponent {
    private final OrdersRepository repository;
    // ...
}

// PACKAGE-PRIVATE: Persistence interface hidden from the Web Controller
interface OrdersRepository {
    void save(Order order);
}

// PACKAGE-PRIVATE: Persistence implementation hidden
class JdbcOrdersRepository implements OrdersRepository {
    // ...
}
```

[DON'T]
```java
package com.mycompany.myapp.orders;

// ANTI-PATTERN: Everything is public. Packages are just folders. Encapsulation is completely broken.
public interface OrdersComponent { ... }
public class OrdersComponentImpl implements OrdersComponent { ... }
public interface OrdersRepository { ... }
public class JdbcOrdersRepository implements OrdersRepository { ... }
```

## Relaxed Layered Architecture
[DO]
```java
package com.mycompany.myapp.web;

import com.mycompany.myapp.orders.OrdersComponent;

public class OrdersController {
    private final OrdersComponent ordersComponent; // Controller depends strictly on the coarse-grained component boundary

    public OrdersController(OrdersComponent ordersComponent) {
        this.ordersComponent = ordersComponent;
    }
}
```

[DON'T]
```java
package com.mycompany.myapp.web;

import com.mycompany.myapp.orders.OrdersService;
import com.mycompany.myapp.orders.OrdersRepository; // ANTI-PATTERN: Bypassing business logic

public class OrdersController {
    private final OrdersService ordersService;
    private final OrdersRepository ordersRepository; // Direct access to persistence violates layer constraints

    public OrdersController(OrdersService ordersService, OrdersRepository ordersRepository) {
        // ...
    }
}
```

## Ubiquitous Domain Language (Ports & Adapters)
[DO]
```java
package com.mycompany.myapp.domain;

// The Domain speaks in business terms
public interface Orders {
    Order findById(String id);
}
```

[DON'T]
```java
package com.mycompany.myapp.domain;

// ANTI-PATTERN: The Domain is polluted with technical/infrastructure terminology
public interface JdbcOrdersRepository {
    Order findById(String id);
}
```

## The Périphérique Anti-Pattern
[DO]
```text
Project Structure (Source Trees decoupled via build tool):
├── module-domain/          (Has NO dependencies)
├── module-web/             (Depends ONLY on module-domain)
└── module-persistence/     (Depends ONLY on module-domain)

The web controller CANNOT physically import the persistence implementation.
```

[DON'T]
```text
Project Structure:
├── module-infrastructure/
│   ├── web/OrdersController.java
│   └── persistence/JdbcOrdersRepository.java

ANTI-PATTERN: OrdersController can directly instantiate JdbcOrdersRepository if access modifiers are lax, skipping the domain entirely.
```