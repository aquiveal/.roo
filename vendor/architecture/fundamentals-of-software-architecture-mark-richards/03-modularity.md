@Domain
These rules MUST trigger when the AI is tasked with architectural design, code refactoring, system restructuring, component extraction, defining namespaces/packages, or when the user explicitly requests analysis of code coupling, cohesion, dependencies, or modularity.

@Vocabulary
*   **Modularity**: A logical grouping of related code (classes, functions) representing an organizing principle to prevent software entropy.
*   **Cohesion**: The measure of how related the internal parts of a module are to one another.
*   **Functional Cohesion**: (Optimal) Every part of a module is related, and the module contains everything essential to its function.
*   **Sequential Cohesion**: Two modules interact, where one outputs data that becomes the input for the other.
*   **Communicational Cohesion**: Modules form a communication chain, operating on shared information or contributing to a shared output.
*   **Procedural Cohesion**: Modules must execute code in a strict, specific order.
*   **Temporal Cohesion**: Modules are related purely based on timing dependencies (e.g., startup initialization tasks).
*   **Logical Cohesion**: Data within modules is logically related but not functionally (e.g., `StringUtils`).
*   **Coincidental Cohesion**: (Worst) Elements in a module are unrelated other than occupying the same source file.
*   **LCOM (Lack of Cohesion in Methods)**: A structural metric identifying incidental coupling within classes, defined conceptually as the sum of sets of methods not shared via sharing fields. 
*   **Afferent Coupling**: The number of incoming connections to a code artifact.
*   **Efferent Coupling**: The number of outgoing connections to other code artifacts.
*   **Abstractness**: The ratio of abstract artifacts (interfaces, abstract classes) to concrete artifacts (implementation).
*   **Instability**: The ratio of efferent coupling to the sum of both efferent and afferent coupling (measures volatility).
*   **Distance from the Main Sequence**: An idealized metric balancing Abstractness and Instability. 
*   **Zone of Uselessness**: Code that is too abstract to be easily used.
*   **Zone of Pain**: Code that has too much implementation and not enough abstraction, making it brittle.
*   **Connascence**: A metric stating that two components are connascent if a change in one requires the other to be modified to maintain system correctness.
*   **Static Connascence**: Source-code-level coupling (Name, Type, Meaning/Convention, Position, Algorithm).
*   **Dynamic Connascence**: Execution-time coupling (Execution, Timing, Values, Identity).
*   **Connascence Strength**: The ease with which a developer can refactor a type of coupling (Static is weaker/better than Dynamic).
*   **Connascence Locality**: How proximal modules are to each other; higher connascence is acceptable within the same module but unacceptable across separate modules.
*   **Connascence Degree**: The size of the impact of the coupling (number of affected classes/modules).

@Objectives
*   **Counteract System Entropy**: The AI MUST proactively inject order into the system by maintaining strict logical and physical separation of related code.
*   **Maximize Cohesion**: The AI MUST drive module design toward Functional Cohesion and eliminate Coincidental and Logical Cohesion.
*   **Optimize Coupling**: The AI MUST balance Abstractness and Instability to keep components near the "Main Sequence," avoiding both the Zone of Pain and the Zone of Uselessness.
*   **Minimize and Localize Connascence**: The AI MUST systematically downgrade the strength of connascence (converting Dynamic to Static) and restrict high-strength connascence strictly to highly localized boundaries.

@Guidelines

### 1. Cohesion Rules
*   The AI MUST group code by related domain functionality, NOT by technical coincidence.
*   When evaluating a class, the AI MUST calculate its conceptual LCOM: If a class has distinct sets of methods that operate on entirely disjoint sets of private fields, the AI MUST propose splitting the class into multiple, highly cohesive classes.
*   The AI MUST NOT create "Utility" classes (e.g., `StringUtils`, `MiscHelpers`) that group methods purely by data type (Logical Cohesion). Utilities MUST be scoped to specific domain functions.
*   When breaking apart a highly cohesive module is proposed, the AI MUST warn the user if doing so would result in increased coupling and decreased readability.

### 2. Coupling and Main Sequence Rules
*   The AI MUST analyze the Afferent (incoming) and Efferent (outgoing) coupling of any generated component.
*   Highly depended-upon components (High Afferent Coupling) MUST be designed with high Abstractness (interfaces, abstract classes) to ensure stability.
*   Components with many outgoing dependencies (High Efferent Coupling) MUST be highly concrete, as their Instability makes them volatile and prone to breakage.
*   The AI MUST NOT generate code that falls into the Zone of Pain (highly concrete AND highly depended upon) or the Zone of Uselessness (highly abstract AND having no incoming dependencies).

### 3. Static Connascence (Source-Level) Rules
*   **Connascence of Name (CoN)**: The AI MUST ensure consistent naming conventions. When renaming a concept, the AI MUST update all corresponding references.
*   **Connascence of Type (CoT)**: The AI MUST strictly enforce type safety. For dynamically typed languages, the AI MUST use selective typing (e.g., JSDoc, TypeScript, Type Hints) to explicitly define expected contracts.
*   **Connascence of Meaning (CoM)**: The AI MUST NEVER generate magic strings or magic numbers. Hard-coded values MUST be extracted into explicitly named constants or enumerations.
*   **Connascence of Position (CoP)**: The AI MUST NOT generate methods or functions with long parameter lists (greater than 3 parameters). The AI MUST convert ordered parameter lists into named parameter objects, dictionaries, or structs.
*   **Connascence of Algorithm (CoA)**: When an algorithm (e.g., hashing, validation) must be agreed upon by multiple components, the AI MUST centralize the algorithm into a single shared module rather than duplicating the implementation.

### 4. Dynamic Connascence (Runtime-Level) Rules
*   **Connascence of Execution (CoE)**: The AI MUST NOT design APIs that require methods to be called in a strict, undocumented order. The AI MUST encapsulate required execution orders inside a single cohesive method or use the Builder pattern to enforce valid states.
*   **Connascence of Timing (CoT)**: The AI MUST explicitly identify and safeguard against race conditions by implementing thread-safe structures, asynchronous locks, or stateless functional designs.
*   **Connascence of Values (CoV)**: When multiple independent values must change together to maintain data integrity (e.g., distributed transactions, geometric coordinates), the AI MUST encapsulate them into a single atomic transaction or immutable data structure.
*   **Connascence of Identity (CoI)**: When components share a common data structure (e.g., a distributed queue), the AI MUST isolate the interaction behind a strict, decoupled interface.

### 5. Connascence Refactoring Rules
*   **Rule of Degree**: The AI MUST actively refactor strong forms of connascence (Dynamic) into weaker forms of connascence (Static).
*   **Rule of Locality**: If two elements are far apart (different modules/packages), the AI MUST restrict their relationship to the weakest possible forms of connascence (Name or Type). Stronger connascence (Meaning, Algorithm, Execution) MUST ONLY be permitted if the elements are placed in the exact same module.

@Workflow
When analyzing or generating architecture, the AI MUST execute the following algorithm:
1.  **Module Identification**: Identify the logical grouping of the code. Ensure the namespace/package exactly reflects the domain purpose, not a generic technical layer.
2.  **Cohesion Assessment**: Evaluate the internal methods and fields. If LCOM is high (disjoint field/method usage), split the module. Eliminate any Temporal, Logical, or Coincidental cohesion.
3.  **Coupling Calculation**: Map the incoming (Afferent) and outgoing (Efferent) connections. 
4.  **Main Sequence Alignment**: Check the Abstractness versus Instability. If a component is widely used by others, convert its public API to abstractions/interfaces.
5.  **Connascence Audit**:
    *   Scan for magic numbers/strings (CoM) -> Convert to Named Constants (CoN).
    *   Scan for long parameter lists (CoP) -> Convert to Parameter Objects (CoN).
    *   Scan for strict temporal call sequences (CoE) -> Encapsulate into a single orchestrating method.
6.  **Locality Enforcement**: Ensure that any remaining high-strength connascence is strictly contained within the smallest possible encapsulation boundary.

@Examples (Do's and Don'ts)

### 1. Connascence of Meaning (CoM) vs. Connascence of Name (CoN)
**[DON'T]** - Magic numbers scattered in code (Connascence of Meaning)
```javascript
function processOrder(status) {
    if (status === 1) { // 1 means "Pending"
        // ...
    } else if (status === 2) { // 2 means "Shipped"
        // ...
    }
}
```

**[DO]** - Upgrading to Connascence of Name
```javascript
const OrderStatus = Object.freeze({
    PENDING: 1,
    SHIPPED: 2
});

function processOrder(status) {
    if (status === OrderStatus.PENDING) {
        // ...
    } else if (status === OrderStatus.SHIPPED) {
        // ...
    }
}
```

### 2. Connascence of Position (CoP) vs. Connascence of Name (CoN)
**[DON'T]** - Function relies on the strict order of arguments
```javascript
// A change in parameter order breaks all callers
function createUser(firstName, lastName, email, role, isActive) {
    // ...
}
createUser("John", "Doe", "john@example.com", "Admin", true);
```

**[DO]** - Function relies on named parameters (Object Destructuring)
```javascript
function createUser({ firstName, lastName, email, role, isActive }) {
    // ...
}
createUser({
    firstName: "John",
    lastName: "Doe",
    email: "john@example.com",
    role: "Admin",
    isActive: true
});
```

### 3. Connascence of Execution (CoE)
**[DON'T]** - Caller must know the exact execution order to prevent failure
```javascript
const email = new Email();
email.setRecipient("foo@example.com");
email.setSender("me@me.com");
email.setSubject("whoops");
// If send() is called before the above are set, it fails
email.send(); 
```

**[DO]** - Encapsulate execution order inside the constructor or a factory method
```javascript
const email = new Email({
    recipient: "foo@example.com",
    sender: "me@me.com",
    subject: "whoops"
});
email.send();
```

### 4. Evaluating LCOM (Lack of Cohesion in Methods)
**[DON'T]** - Low Cohesion (High LCOM). Methods operate on disjoint fields.
```java
class CustomerAndOrderManager {
    private String customerName;
    private String orderId;

    // Only uses customerName
    public void updateCustomerName(String name) { this.customerName = name; }
    public String getCustomerName() { return this.customerName; }

    // Only uses orderId
    public void cancelOrder() { /* logic using orderId */ }
    public String getOrder() { return this.orderId; }
}
```

**[DO]** - High Cohesion (Low LCOM). Split into distinct, functionally cohesive modules.
```java
class Customer {
    private String name;
    public void updateName(String name) { this.name = name; }
    public String getName() { return this.name; }
}

class Order {
    private String orderId;
    public void cancel() { /* logic */ }
    public String getOrderId() { return this.orderId; }
}
```