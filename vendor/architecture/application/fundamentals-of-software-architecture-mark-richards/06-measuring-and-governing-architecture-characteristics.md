@Domain
This rule set triggers when the AI is tasked with assessing, measuring, refactoring, or governing software architecture, including defining architectural metrics, analyzing code complexity, establishing performance budgets, or implementing automated architectural tests (fitness functions) across any codebase.

@Vocabulary
- **Architecture Characteristics**: The critical "-ilities" (performance, scalability, modularity, etc.) that define the success criteria of a system.
- **Composite Characteristics**: High-level, vague characteristics (e.g., "Agility") that must be decomposed into objectively measurable parts (e.g., "Testability" and "Deployability").
- **Performance Budget**: A strict, predefined operational limit for specific application actions (e.g., first-page render < 500ms).
- **K-Weight Budget**: A strict maximum limit on the total byte size of libraries, frameworks, and assets allowed to be downloaded on a single page.
- **Cyclomatic Complexity (CC)**: An objective structural metric measuring the complexity of code by tracking decision points (execution paths). Formula: `CC = E - N + 2P` (Edges - Nodes + 2 * Connected Components).
- **Essential Complexity**: Code complexity derived inherently from a complex problem domain.
- **Accidental Complexity**: Avoidable code complexity resulting from poor code structure, lack of refactoring, or failure to partition logic.
- **Fitness Function**: Any mechanism (metric, monitor, unit test, chaos engineering tool) that provides an objective integrity assessment of some architecture characteristic.
- **Cyclic Dependency**: A damaging structural anti-pattern where components/packages reference each other in a closed loop, destroying modularity.
- **Distance from the Main Sequence**: An architectural metric balancing a component's abstractness against its instability to ensure healthy code structures.
- **Chaos Engineering**: The discipline of continuously and purposefully injecting failures (via tools like Chaos Monkey) into a system to proactively test fault tolerance and governance rules.

@Objectives
- Eradicate vague, subjective definitions of architecture characteristics by enforcing objective, quantifiable measurements.
- Enforce strict operational limits by defining performance budgets and statistical models rather than relying on arbitrary averages.
- Prevent structural degradation by rigorously calculating, evaluating, and restricting Cyclomatic Complexity (CC).
- Automate architectural governance by writing and integrating continuous architectural fitness functions into the CI/CD pipeline.
- Proactively test system resilience and architectural compliance using Chaos Engineering principles.

@Guidelines

**1. Objective Definition of Architecture Characteristics**
- The AI MUST reject vague, subjective definitions of architecture characteristics.
- When encountering a composite characteristic (e.g., "Agility"), the AI MUST decompose it into objectively measurable sub-characteristics (e.g., "Deployability" measured by percentage of successful deployments, and "Testability" measured by code coverage).
- The AI MUST ensure all teams share a ubiquitous language by standardizing concrete, objective definitions for all architecture characteristics.

**2. Operational Measurements and Performance Budgets**
- The AI MUST NOT rely solely on average response times for operational metrics. The AI MUST measure and monitor maximum response times and 95th/99th percentiles to account for boundary conditions and outliers.
- The AI MUST establish exact **Performance Budgets** for UI and API interactions (e.g., enforcing a maximum 500ms threshold for first-page render, first contentful paint, or first CPU idle).
- The AI MUST establish **K-Weight Budgets** to strictly limit the maximum payload size (in bytes) of libraries and frameworks traveling over the network.
- For highly dynamic characteristics like scalability, the AI MUST recommend establishing statistical prediction models that trigger alarms when real-time metrics deviate, rather than relying on static numerical thresholds.

**3. Structural Measurements and Cyclomatic Complexity (CC)**
- The AI MUST calculate Cyclomatic Complexity for methods/functions using the formula `CC = E - N + 2P` or standard static analysis tools.
- The AI MUST flag any function with a `CC > 5` as a warning indicating poor cohesion.
- The AI MUST strictly reject any function with a `CC > 10` as an error, explicitly mandating refactoring.
- The AI MUST differentiate between Essential and Accidental Complexity. If high CC is due to poor partitioning (Accidental), the AI MUST instruct the user to refactor into smaller, logical chunks.
- The AI MUST recommend Test-Driven Development (TDD) as a systemic engineering practice to organically generate smaller, highly cohesive, low-CC methods.
- The AI MUST utilize tools like Crap4J (or equivalent language-specific tools) to evaluate the ratio of CC to code coverage, ensuring highly complex code is not left untested.

**4. Architectural Governance via Fitness Functions**
- The AI MUST NOT rely on manual code reviews for architectural governance. The AI MUST automate governance by writing **Fitness Functions**.
- The AI MUST write fitness functions to explicitly prevent **Cyclic Dependencies** between packages/namespaces (using tools like JDepend, ArchUnit, NDepend, or NetArchTest).
- The AI MUST write fitness functions to enforce **Distance from the Main Sequence**, ensuring classes do not fall into the "Zone of Pain" (too concrete/rigid) or "Zone of Uselessness" (too abstract).
- The AI MUST write fitness functions to strictly enforce layer dependencies in Layered Architectures (e.g., Presentation layer MUST NOT directly access the Persistence layer).
- The AI MUST ensure developers understand the purpose of a fitness function before it is imposed; the AI MUST include descriptive error messages in fitness function tests explaining *why* the architectural rule exists.

**5. Chaos Engineering and Automated Compliance**
- The AI MUST design proactive resilience tests mirroring the "Simian Army" concepts:
  - **Conformity Monkey**: Write tests to ensure all services comply with API standards (e.g., responding correctly to all RESTful verbs).
  - **Security Monkey**: Write automated checks that scan for misconfigurations or unauthorized open ports.
  - **Janitor Monkey**: Implement monitors that identify and flag orphaned/unused services or instances for deletion to prevent resource drain.
- The AI MUST treat architectural governance as a codified checklist, embedding critical reminders into the testing substrate so details do not slip by busy developers.

@Workflow
1. **Characteristic Decomposition**: Upon receiving architectural requirements, identify all composite or vague terms. Prompt the user to decompose them into objective, physics-like measurements (e.g., milliseconds, payload bytes, coverage percentages).
2. **Budget Establishment**: Define hard Performance Budgets (e.g., render times) and K-Weight Budgets (e.g., payload sizes) for the application. Write scripts or configuration files to monitor these budgets.
3. **Complexity Audit**: Scan the target codebase to calculate Cyclomatic Complexity. Output a report highlighting all methods where `CC > 5`. Draft refactoring plans for any method where `CC > 10`.
4. **Governance Automation**: Generate architectural fitness functions using the platform's native tools (e.g., ArchUnit for Java, NetArchTest for C#, dependency-cruiser for .NET, ESLint rules for Node.js).
5. **Structural Enforcement**: Specifically write tests that fail the CI/CD build if (a) cyclic dependencies are detected, or (b) isolated layers are bypassed.
6. **Resilience Engineering**: Define a suite of "Chaos" or conformity monitors that continuously check the production or staging environment for architectural drift, security regressions, and orphaned resources.

@Examples (Do's and Don'ts)

**Characteristic Definition**
- [DO]: "We define Deployability as the ability to deploy to production in under 10 minutes with a deployment success rate of >99% and 0 manual interventions."
- [DON'T]: "The architecture must be Agile and easy to deploy."

**Operational Measurement**
- [DO]: "Measure API response times by tracking the 95th and 99th percentiles to catch latency spikes caused by garbage collection or network drops."
- [DON'T]: "Track the average API response time to ensure the system is fast."

**Cyclomatic Complexity**
- [DO]: 
  ```java
  // Refactored to keep CC < 5
  public void processOrder(Order order) {
      if (!order.isValid()) throw new InvalidOrderException();
      applyDiscount(order);
      chargeCustomer(order);
  }
  ```
- [DON'T]: Create a single `processOrder` method with 15 nested `if/else` and `switch` statements, resulting in a CC of 24.

**Architectural Governance (Fitness Functions)**
- [DO]: 
  ```java
  // ArchUnit fitness function enforcing Layered Architecture
  @Test
  public void persistence_layer_should_only_be_accessed_by_service_layer() {
      layeredArchitecture()
          .layer("Controller").definedBy("..controller..")
          .layer("Service").definedBy("..service..")
          .layer("Persistence").definedBy("..persistence..")
          .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
          .check(importedClasses);
  }
  ```
- [DON'T]: Rely on a Wiki page that says "Please remember not to call the database from the UI controller," leaving it up to manual pull request reviews to catch violations.

**Cyclic Dependencies**
- [DO]: Implement a test using JDepend or equivalent that explicitly fails the build if `jdepend.containsCycles()` evaluates to true.
- [DON'T]: Blindly accept IDE auto-import suggestions that cross domain boundaries and create circular references between `com.app.orders` and `com.app.customers`.