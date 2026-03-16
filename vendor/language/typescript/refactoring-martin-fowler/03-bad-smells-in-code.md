@Domain
Trigger these rules when analyzing, reviewing, restructuring, or modifying existing codebases. Specifically, activate when tasked with identifying technical debt, performing code reviews, improving code readability, modularizing architecture, or applying structural refactoring patterns.

@Vocabulary
*   **Bad Smell**: A surface-level indication or structure in the code that usually corresponds to a deeper problem in the system, signaling the need for refactoring.
*   **Mysterious Name**: Variables, functions, or classes with cryptic, confusing, or non-descriptive names.
*   **Duplicated Code**: Identical or highly similar code structures present in multiple locations.
*   **Long Function**: A function whose length or complexity obscures its overall intention.
*   **Long Parameter List**: A function signature requiring excessive arguments, making it hard to use and read.
*   **Global Data**: Data accessible and modifiable from anywhere in the codebase, leading to untraceable state changes.
*   **Mutable Data**: Variables that change state across scopes, causing unpredictable interactions and bugs.
*   **Divergent Change**: A single module or class that must be modified in different ways for different, unrelated reasons.
*   **Shotgun Surgery**: A single conceptual change that requires making small edits to many different modules.
*   **Feature Envy**: A function that spends more time invoking methods or accessing data of a different module than its own.
*   **Data Clump**: A group of data items (usually 3 or more) that frequently travel together as fields or parameter lists.
*   **Primitive Obsession**: Using primitive data types (strings, integers) to represent domain concepts (e.g., currency, telephone numbers) instead of dedicated objects.
*   **Repeated Switches**: Duplicated `switch` statements or `if/else` chains checking the same condition across the codebase.
*   **Lazy Element**: A function, class, or hierarchy that does not do enough work to justify its existence.
*   **Speculative Generality**: Hooks, parameters, or abstract classes built for anticipated future needs that are not currently required.
*   **Temporary Field**: A class field that is only populated and used under specific, limited circumstances.
*   **Message Chain**: A sequence of nested method calls (e.g., `a.getB().getC().getD()`), coupling the client to the navigation structure.
*   **Middle Man**: A class whose primary purpose has devolved into simply delegating calls to another class.
*   **Insider Trading**: Modules that are highly coupled via excessive or secretive data exchange.
*   **Large Class**: A class attempting to do too much, typically evidenced by too many fields or duplicated code.
*   **Alternative Classes with Different Interfaces**: Classes that perform similar functions but use different method signatures.
*   **Data Class**: A class containing only fields and getters/setters, entirely lacking behavioral logic.
*   **Refused Bequest**: A subclass that uses only a tiny fraction of the data or behavior inherited from its parent, or rejects the parent's interface entirely.
*   **Deodorant Comment**: A comment written specifically to explain or mask poorly written, confusing code.

@Objectives
*   Continuously improve the internal structure of the code without altering its external behavior.
*   Ensure the code communicates its *intent* rather than just its *implementation*.
*   Maximize cohesion within modules and minimize coupling between different modules.
*   Eradicate code duplication to ensure the system says everything "once and only once."
*   Transform data structures into robust domain models by combining them with their associated behaviors.

@Guidelines

# 1. Naming & Identification
*   **Eradicate Mysterious Names**: The AI MUST ruthlessly rename functions, variables, and fields to communicate their explicit purpose. If a good name cannot be found, the AI MUST treat this as a symptom of a deeper design flaw and reconsider the element's purpose.
*   **Deodorize Comments**: When encountering a comment explaining a block of code, the AI MUST extract that code block into a function named after the comment's intent. Comments MUST ONLY be used to explain *why* a decision was made, not *what* the code is doing. If a comment specifies a required state, the AI MUST introduce an Assertion.

# 2. Size & Structure Constraints
*   **Eliminate Duplicated Code**: The AI MUST unify duplicate code structures. Extract common logic into separate functions. If variations exist, slide statements to align similar elements, or pull methods up into a common base class.
*   **Shorten Long Functions**: The AI MUST decompose long functions. Base the extraction on the *semantic distance* between what the method does and how it does it. Use `Extract Function`. If temporary variables hinder extraction, use `Replace Temp with Query`. For heavy parameter loads, use `Introduce Parameter Object` or `Replace Function with Command`.
*   **Shrink Parameter Lists**: The AI MUST minimize parameters. If one parameter can be derived from another, use `Replace Parameter with Query`. If parameters belong to a cohesive group, use `Preserve Whole Object` or `Introduce Parameter Object`. The AI MUST remove flag (boolean) arguments using `Remove Flag Argument`.
*   **Break Down Large Classes**: When a class has too many fields or responsibilities, the AI MUST extract classes or superclasses. Group fields with common prefixes/suffixes or those that change together into dedicated components.

# 3. Data Management & Mutability
*   **Quarantine Global Data**: The AI MUST encapsulate global data using `Encapsulate Variable` and restrict its scope and visibility as strictly as the language allows.
*   **Restrict Mutable Data**: The AI MUST strictly control mutability. 
    *   Extract side-effect-free code away from update logic.
    *   Separate queries from modifiers.
    *   Replace derived mutable variables with queries (`Replace Derived Variable with Query`).
    *   For structures, replace mutable references with immutable value objects where applicable.
*   **Cure Primitive Obsession**: The AI MUST replace primitives with objects/classes when they represent specific domain concepts (e.g., ZIP codes, coordinates, money). Replace type-codes representing behavior with polymorphic subclasses.
*   **Resolve Data Clumps**: When 3+ data items appear together frequently, the AI MUST extract them into a dedicated Class or Parameter Object. Test by conceptualizing the deletion of one field; if the remaining fields lose meaning, they MUST be clumped into a class.
*   **Enrich Data Classes**: The AI MUST identify code outside a Data Class that manipulates its data, and move that behavior *into* the Data Class. Exception: Immutable result records from a `Split Phase` operation are allowed to remain behaviorless Data Classes.
*   **Evict Temporary Fields**: The AI MUST extract temporary fields (and all code referencing them) into a separate class. Introduce a Special Case (Null Object) if conditional logic relies on the field's validity.

# 4. Modularity & Coupling
*   **Resolve Divergent Change**: If a module changes for multiple separate reasons (e.g., database updates AND business rules), the AI MUST split the module based on those contexts using `Split Phase`, `Extract Class`, or `Move Function`.
*   **Cure Shotgun Surgery**: If a single conceptual change requires edits across multiple modules, the AI MUST move functions and fields to consolidate the related logic into a single module.
*   **Treat Feature Envy**: If a function interacts more with another module's data than its own, the AI MUST move the function to the module where the data resides. (Exception: Deliberate design patterns like Strategy or Visitor).
*   **Shorten Message Chains**: The AI MUST resolve deep navigation chains (`a.b().c().d()`) by either hiding delegates or, preferably, extracting the specific logic the client wants and moving it down the chain.
*   **Eliminate Middle Men**: If a class does little more than delegate to another class, the AI MUST remove the middle man and force clients to call the end-target directly.
*   **Regulate Insider Trading**: The AI MUST sever overly intimate data sharing between modules using `Move Function`/`Move Field`, or introduce a third intermediary module to manage the interaction cleanly.
*   **Standardize Alternative Classes**: If classes provide similar functionality but have different interfaces, the AI MUST rename functions and move behavior until their interfaces match.

# 5. Control Flow & Abstractions
*   **Polymorph Repeated Switches**: The AI MUST replace duplicated `switch` statements or `if/else` chains that pivot on the same condition with polymorphic subclasses.
*   **Pipeline Loops**: Where the language supports it, the AI MUST replace loops with Collection Pipelines (e.g., `map`, `filter`, `reduce`).
*   **Purge Lazy Elements**: If a class, function, or hierarchy is no longer pulling its weight, the AI MUST inline it or collapse the hierarchy.
*   **Eradicate Speculative Generality**: The AI MUST remove abstract classes, unused parameters, or naming hooks that exist solely for unverified future requirements.
*   **Fix Refused Bequests**: If a subclass inherits but ignores the majority of its parent's data/methods, the AI MUST evaluate if the hierarchy is wrong. If the subclass rejects the parent's *interface*, the AI MUST eliminate the inheritance and replace it with delegation (`Replace Subclass with Delegate`).

@Workflow
1.  **Smell Identification**: Scan the provided code block or module. Compare the code structure against the 24 definitions in the `@Vocabulary`.
2.  **Contextual Analysis**: Determine if the structure is a deliberate, justified pattern (e.g., Visitor pattern mimicking Feature Envy) or a genuine Bad Smell.
3.  **Refactoring Selection**: Select the specific, granular refactoring pattern mandated by the `@Guidelines` for the identified smell.
4.  **Step-by-Step Execution**:
    *   Extract isolated logic into temporary/nested functions if necessary.
    *   Apply the structural change (Move, Rename, Replace, Extract, Inline).
    *   Update all caller/client references to use the newly factored code.
5.  **Verification**: Verify that the resulting code eliminates the smell, communicates intention clearly, and introduces no speculative complexity.

@Examples

**Scenario 1: Long Function / Comments**
[DON'T]
```javascript
function calculateOrderTotal(order) {
    let total = 0;
    // Calculate base price
    for (let item of order.items) {
        total += item.price * item.quantity;
    }
    // Add shipping
    if (total > 100) {
        total += 0;
    } else {
        total += 10;
    }
    return total;
}
```
[DO]
```javascript
function calculateOrderTotal(order) {
    return calculateBasePrice(order) + calculateShipping(calculateBasePrice(order));
}

function calculateBasePrice(order) {
    return order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

function calculateShipping(basePrice) {
    return basePrice > 100 ? 0 : 10;
}
```

**Scenario 2: Data Clumps / Primitive Obsession**
[DON'T]
```javascript
function scheduleMeeting(room, startYear, startMonth, startDay, endYear, endMonth, endDay) {
    // ...
}
```
[DO]
```javascript
class DateRange {
    constructor(startDate, endDate) {
        this.startDate = startDate;
        this.endDate = endDate;
    }
    contains(date) { /* ... */ }
}

function scheduleMeeting(room, dateRange) {
    // ...
}
```

**Scenario 3: Loops (Replace with Pipeline)**
[DON'T]
```javascript
const activeUserNames = [];
for (const user of users) {
    if (user.isActive) {
        activeUserNames.push(user.name);
    }
}
```
[DO]
```javascript
const activeUserNames = users
    .filter(user => user.isActive)
    .map(user => user.name);
```