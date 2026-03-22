# RooCode Rule File: Object-Oriented Programming Architecture

## @Domain
This rule file is activated when the AI is tasked with designing system architecture, structuring object-oriented code, managing source code dependencies, creating or refactoring modules/components, defining class relationships, or isolating high-level business rules from low-level details (e.g., UI, Database, I/O devices).

## @Vocabulary
*   **Object-Oriented Programming (OO):** The ability, through the use of polymorphism, to gain absolute control over every source code dependency in the system, imposing discipline on indirect transfer of control.
*   **Encapsulation:** The drawing of a line around a cohesive set of data and functions, hiding the data and exposing only necessary functions. (Note: OO languages actually weakened the perfect encapsulation that existed in C).
*   **Inheritance:** The redeclaration of a group of variables and functions within an enclosing scope. OO makes this data structure masquerading significantly safer and more convenient.
*   **Polymorphism:** An application of pointers to functions that allows interchangeable behavior. OO provides safe and convenient polymorphism, eliminating the dangers of manual function pointer conventions.
*   **Plugin Architecture:** A system structure where low-level details (like I/O, Database, or UI) are relegated to separate modules that plug into independent high-level policy modules.
*   **Dependency Inversion:** The practice of using polymorphic interfaces to force source code dependencies to point in the opposite direction of the flow of control, ensuring they always point toward high-level policies.
*   **Independent Deployability:** The capability to compile and deploy separate components (e.g., UI, Database, Business Rules) independently because their source code dependencies have been decoupled.
*   **Independent Developability:** The capability for different teams to work on different modules (e.g., UI vs. Business Rules) independently, made possible by Independent Deployability.

## @Objectives
*   The AI MUST reject the notion that OO is merely "the combination of data and function" or "a way to model the real world."
*   The AI MUST utilize OO specifically to gain absolute control over every source code dependency in the system.
*   The AI MUST leverage polymorphism to create plugin architectures.
*   The AI MUST isolate high-level business rules from low-level details, ensuring that the Business Rules never mention the UI or the Database in their source code.

## @Guidelines
*   **Enforce Encapsulation:** Even though modern OO languages (like Java, C#, C++) have weakened the perfect encapsulation of C, the AI MUST rely on developer discipline to not circumvent encapsulated data. The AI MUST strictly use access modifiers (`private`, `protected`) to hide data and expose only intended behaviors.
*   **Utilize Safe Polymorphism:** When encountering the need for device-independent behavior or interchangeable components, the AI MUST use OO polymorphism (interfaces/abstract classes/virtual methods) rather than manual function pointers or complex `switch`/`if-else` chains.
*   **Invert Dependencies Against Control Flow:** When a high-level module needs to call a low-level module, the AI MUST NOT create a direct source code dependency. Instead, the AI MUST introduce an interface in the high-level module that the low-level module implements.
*   **Protect High-Level Policies:** The AI MUST arrange all source code dependencies so that UI, Database, and other detail components depend on Business Rules, not the other way around.
*   **Implement Plugin Architectures:** The AI MUST design the UI and Database as plugins to the Business Rules. The source code of the Business Rules MUST NEVER mention the UI or the Database.
*   **Ensure Independent Deployability:** The AI MUST structure the code into components (e.g., jar files, DLLs, Gem files) such that changes to the UI or Database source code only require the redeployment of those specific components, leaving the Business Rules component untouched and un-recompiled.

## @Workflow
When tasked with designing a new feature, refactoring an existing system, or resolving architectural coupling, the AI MUST follow this rigid, step-by-step algorithmic process:
1.  **Identify Components by Level:** Segregate the requested features into High-Level Policies (Business Rules) and Low-Level Details (UI, Database, I/O devices).
2.  **Trace the Flow of Control:** Determine the execution path at runtime (e.g., Main calls UI, UI calls Business Rule, Business Rule calls Database).
3.  **Analyze Source Code Dependencies:** Evaluate if the natural source code dependencies follow the flow of control. If a High-Level Policy has an import, include, or using statement pointing to a Low-Level Detail, flag it as an architectural violation.
4.  **Apply Dependency Inversion:** For every flagged violation, generate an Interface. 
    *   Place the Interface in the same component/module as the calling High-Level Policy.
    *   Define the Interface based on the needs of the High-Level Policy.
    *   Move the implementation of that Interface into the Low-Level Detail component.
5.  **Establish Plugin Architecture:** Verify that the Database and UI modules act strictly as plugins. Confirm that the Business Rule component can be compiled entirely independently of the UI and Database components.
6.  **Enforce Encapsulation:** Review all created data structures. Ensure that internal variables are hidden and that components only communicate through the newly established polymorphic interfaces.

## @Examples (Do's and Don'ts)

### Polymorphism and Dependency Inversion
*   **[DON'T]** Allow the flow of control to dictate the source code dependency, causing Business Rules to depend on Database details.
```java
// Anti-pattern: Business Rule depends on low-level SQL database directly
import java.sql.Connection;

public class PayrollCalculator {
    public void calculatePay() {
        // High-level policy directly referencing low-level detail
        SqlDatabase db = new SqlDatabase(); 
        EmployeeData data = db.getEmployee();
        // ... calculation ...
    }
}
```

*   **[DO]** Use polymorphism to invert the dependency, placing the interface in the high-level component and the implementation in the low-level plugin.
```java
// Core Business Rule Component (Independent Developability/Deployability)
package core.business;

// Interface is owned by the high-level policy
public interface EmployeeGateway {
    EmployeeData getEmployee();
}

public class PayrollCalculator {
    private final EmployeeGateway gateway;

    public PayrollCalculator(EmployeeGateway gateway) {
        this.gateway = gateway;
    }

    public void calculatePay() {
        EmployeeData data = gateway.getEmployee();
        // ... calculation ...
    }
}

// Low-Level Detail Component (Plugin)
package plugins.database;

import core.business.EmployeeGateway;
import core.business.EmployeeData;

// Implementation depends on the Business Rule component
public class SqlEmployeeGateway implements EmployeeGateway {
    public EmployeeData getEmployee() {
        // ... SQL specific implementation ...
        return new EmployeeData();
    }
}
```

### Encapsulation and Data Hiding
*   **[DON'T]** Expose internal data simply because the language's lack of header/implementation separation makes it easy to do so.
```java
// Anti-pattern: Broken encapsulation
public class Point {
    public double x; // Exposed data
    public double y; // Exposed data
}
```

*   **[DO]** Strictly hide data and expose only behaviors, simulating the perfect encapsulation that existed in C's forward-declared header structures.
```java
// Correct: Data is hidden, only behavior is exposed
public class Point {
    private double x;
    private double y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double distance(Point p) {
        double dx = this.x - p.x;
        double dy = this.y - p.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
}
```