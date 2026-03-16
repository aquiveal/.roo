# @Domain

This rule set activates whenever the AI is tasked with creating new modules, designing class architectures, refactoring existing source files, reviewing pull requests, or evaluating code cohesion. It is specifically triggered when processing classes or modules that contain multiple methods, handle data structures, or serve requests originating from different types of users, departments, or stakeholders.

# @Vocabulary

*   **SRP (The Single Responsibility Principle)**: The principle stating that a module should be responsible to one, and only one, actor. 
*   **Actor**: A group consisting of one or more people, users, or stakeholders who require a specific change to the system and share the same business needs.
*   **Module**: A cohesive set of functions and data structures. In most languages, this is represented by a single source file.
*   **Cohesion**: The force that binds together the code responsible to a single actor.
*   **Accidental Duplication**: The false coupling of code where two different actors rely on a shared algorithm or function (e.g., a shared helper method), creating a risk that a change for one actor breaks the functionality for the other.
*   **Merge Symptoms**: A signature indicator of an SRP violation occurring when different actors (or developers representing them) modify the same source file for different reasons, resulting in a version control merge conflict.
*   **Facade Pattern**: An architectural pattern used to resolve SRP violations by creating a single class that instantiates and delegates work to separated, actor-specific classes, without containing the business logic itself.

# @Objectives

*   The AI must strictly separate code based on the human actors that depend on it.
*   The AI must eliminate Accidental Duplication by preventing different actors from depending on the same underlying algorithms or helper functions.
*   The AI must architect modules to eliminate the possibility of merge conflicts caused by concurrent changes requested by different departments or stakeholders.
*   The AI must distinguish between the function-level principle ("a function should do one thing") and the module-level SRP ("a module should answer to one actor").

# @Guidelines

*   **Rule of Responsibility**: The AI MUST explicitly identify the "actor" for every method, class, or module it creates or refactors. A module MUST NOT contain methods that serve different actors.
*   **Anti-Definition Constraint**: The AI MUST NOT define the Single Responsibility Principle as "a module should do just one thing." If the AI is optimizing a function to do exactly one thing, it must recognize this as a low-level refactoring principle, NOT the SRP. The SRP solely concerns actors and reasons to change.
*   **Cohesion Constraint**: The AI MUST group functions and data structures together ONLY if they serve the exact same actor.
*   **Accidental Duplication Prevention**: If the AI detects a shared helper method (e.g., calculating regular hours) used by two higher-level methods serving different actors (e.g., Accounting vs. Human Resources), the AI MUST separate this dependency. The AI MUST NOT allow the CFO's requirements to dictate changes to the COO's dependencies.
*   **Data and Function Separation**: To resolve SRP violations, the AI MUST separate the shared data into a pure data structure (with no methods) and create distinct, separate classes for the functions required by each actor.
*   **Facade Implementation**: When separation of data and functions results in too many classes for a client to easily instantiate and track, the AI MUST implement the Facade Pattern to orchestrate the separated classes.
*   **Primary Method Facade**: As an alternative to a pure Facade, if one actor's business rules are significantly more important than the others, the AI MAY keep the most important method within the original class and use that class as a Facade to delegate to the lesser functions.
*   **Private Scope Preservation**: When creating actor-specific classes, the AI MUST encapsulate the specific family of methods required by that actor within that class's private scope, hiding them from the rest of the system.
*   **Architectural Foresight**: The AI should recognize that applying the SRP at the module level scales up to the Common Closure Principle (CCP) at the component level, and forms the Axis of Change for creating Architectural Boundaries.

# @Workflow

When evaluating, refactoring, or generating a module, the AI MUST execute the following step-by-step algorithmic process:

1.  **Actor Identification**: Scan the module's methods and identify the business owner, department, or stakeholder (the "Actor") that specifies the requirements for each method.
2.  **Violation Detection**: Compare the actors identified in Step 1. If more than one distinct actor is found within the same module (e.g., DBA, HR, Accounting), declare an SRP violation.
3.  **Dependency Tracing**: Analyze the module for shared helper algorithms (e.g., shared math or formatting functions). Check if these helpers are invoked by methods belonging to different actors. 
4.  **Data Extraction**: Extract all shared variables and fields into a standalone, method-less data structure (e.g., `[Entity]Data`).
5.  **Functional Segregation**: Create a distinct, separate class for each identified actor. Move the methods belonging to that actor into their respective new classes.
6.  **State Injection**: Modify the new actor-specific classes to accept the method-less data structure (created in Step 4) as a dependency or parameter.
7.  **Facade Construction**: Construct a Facade class using the original module's name. Implement methods matching the original API, but leave them empty of business logic.
8.  **Delegation Routing**: Wire the Facade class to instantiate the actor-specific classes and delegate the method calls to them.

# @Examples (Do's and Don'ts)

**[DON'T]**
Do not group methods serving different actors (CFO, COO, CTO) into a single module, and do not share helper methods across these actor boundaries.

```java
// ANTI-PATTERN: SRP Violation
// This class is responsible to three different actors.
public class Employee {
    private String name;
    private double hourlyRate;
    private double hoursWorked;

    // Specified by Accounting (CFO)
    public Money calculatePay() {
        return regularHours() * hourlyRate;
    }

    // Specified by Human Resources (COO)
    public Report reportHours() {
        return new Report(name, regularHours());
    }

    // Specified by Database Administrators (CTO)
    public void save() {
        Database.save(this);
    }

    // Accidental Duplication: Shared by CFO and COO. 
    // A change requested by the CFO will break the COO's report.
    private double regularHours() {
        return hoursWorked > 40 ? 40 : hoursWorked;
    }
}
```

**[DO]**
Separate the data from the functions, isolate the operations by actor into their own classes, and use a Facade to orchestrate the interactions.

```java
// 1. Pure data structure shared among the classes
public class EmployeeData {
    public String name;
    public double hourlyRate;
    public double hoursWorked;
}

// 2. Class responsible ONLY to Accounting (CFO)
public class PayCalculator {
    public Money calculatePay(EmployeeData data) {
        return calculateRegularHours(data) * data.hourlyRate;
    }
    private double calculateRegularHours(EmployeeData data) {
        return data.hoursWorked > 40 ? 40 : data.hoursWorked;
    }
}

// 3. Class responsible ONLY to Human Resources (COO)
public class HourReporter {
    public Report reportHours(EmployeeData data) {
        return new Report(data.name, calculateRegularHours(data));
    }
    // Safely duplicated or decoupled algorithm, 
    // immune to changes requested by the CFO.
    private double calculateRegularHours(EmployeeData data) {
        return data.hoursWorked > 40 ? 40 : data.hoursWorked;
    }
}

// 4. Class responsible ONLY to Database Administrators (CTO)
public class EmployeeSaver {
    public void save(EmployeeData data) {
        Database.save(data);
    }
}

// 5. Facade orchestrating the decoupled classes
public class EmployeeFacade {
    private EmployeeData data;

    public EmployeeFacade(EmployeeData data) {
        this.data = data;
    }

    public Money calculatePay() {
        return new PayCalculator().calculatePay(data);
    }

    public Report reportHours() {
        return new HourReporter().reportHours(data);
    }

    public void save() {
        new EmployeeSaver().save(data);
    }
}
```