# @Domain
Triggered when the user requests code refactoring, class restructuring, data structure modeling, object boundary definition, or when the AI detects exposed mutable data, complex temporary variables, bloated classes, or tight coupling between objects navigating through delegates.

# @Vocabulary
*   **Encapsulation**: The process of hiding the secrets of a module (data structures, implementations, connections) from the rest of the system.
*   **Record**: A data structure holding grouped fields. Can be explicit (declared structure) or implicit (hashmap/dictionary).
*   **Collection**: An array, list, or set of elements.
*   **Primitive**: A basic data type (string, number, boolean) that lacks domain-specific behavior.
*   **Value Object**: An immutable object whose equality is based on its state rather than its identity.
*   **Temp (Temporary Variable)**: A local variable used to hold the result of a calculation or intermediate step.
*   **Query**: A function that returns a value and has no observable side effects.
*   **Delegate**: An object that another object (the server) relies on to perform a specific task or hold specific data.
*   **Middle Man**: A class whose primary purpose has devolved into merely forwarding requests to a delegate.
*   **Substitute Algorithm**: The process of entirely replacing a complex implementation of a function with a simpler, clearer one.

# @Objectives
*   The AI MUST identify and hide the secrets of every module to minimize systemic coupling.
*   The AI MUST protect mutable data by preventing direct access to internal records and collections.
*   The AI MUST ensure that behavior resides alongside the data it manipulates.
*   The AI MUST eliminate derived temporary variables in favor of reusable query functions.
*   The AI MUST continuously optimize class sizes, breaking apart bloated classes and merging obsolete ones.
*   The AI MUST balance delegation, hiding delegates to prevent coupling, while removing middle men if forwarding becomes excessive.

# @Guidelines
*   **Encapsulate Record**: When encountering widely used mutable data or implicit records (hashmaps/dictionaries), the AI MUST replace them with a dedicated class. The class MUST provide explicit getter/setter methods. For nested records, the AI MUST focus on encapsulating the update points first, potentially returning deep copies or read-only proxies for reads.
*   **Encapsulate Collection**: The AI MUST NEVER allow a getter to return a direct reference to an internal mutable collection. Getters MUST return a copy (e.g., `.slice()`) or a read-only proxy. The AI MUST provide specific modifier methods (e.g., `add()`, `remove()`) on the owning class to control collection alterations.
*   **Replace Primitive with Object**: When a primitive value (e.g., string, number) requires specific formatting, validation, or behavior, the AI MUST wrap it in a dedicated class. If the field represents a conceptual value, the AI MUST transition it to an immutable Value Object with its own behavior.
*   **Replace Temp with Query**: When a temporary variable is calculated once and read subsequently, the AI MUST extract the calculation into a query function. The AI MUST ensure the extracted function is free of side effects. The AI MUST inline the temporary variable to simplify the original function.
*   **Extract Class**: When a class contains a subset of data and methods that frequently change together, or if removing a piece of data makes other fields/methods nonsensical, the AI MUST extract these elements into a separate cohesive child class.
*   **Inline Class**: When a class has been refactored to the point that it is no longer pulling its weight, the AI MUST move its remaining features into the class that uses it most, and delete the obsolete class.
*   **Hide Delegate**: When a client accesses a delegate object by navigating through a server object (e.g., `client -> server -> delegate`), the AI MUST encapsulate the delegate by creating a forwarding method on the server, thereby decoupling the client from the delegate's interface.
*   **Remove Middle Man**: When a server class has too many forwarding methods and acts merely as a pass-through to a delegate, the AI MUST expose the delegate directly via a getter and force the client to call the delegate, thereby removing the middle man.
*   **Substitute Algorithm**: When an algorithm is overly complex or obsolete, the AI MUST isolate the algorithm in a single function, write comprehensive tests, and replace the entire function body with a clearer, simpler implementation (or standard library call).

# @Workflow
1.  **Analyze Module Secrets**:
    *   Scan the target code for exposed data structures, primitives with localized behavior, long functions with complex temporary variables, and deep object navigation chains.
2.  **Protect Mutable Data (Records & Collections)**:
    *   If raw records are exposed, apply **Encapsulate Record**. Replace the variable with a class, define accessors, update clients, and remove raw access.
    *   If collections are exposed, apply **Encapsulate Collection**. Create `add[Item]` and `remove[Item]` methods. Modify the getter to return a copy or proxy. Update clients calling `push()`/`pop()` on the raw collection to use the new modifiers.
3.  **Elevate Primitives**:
    *   Identify strings/numbers that carry domain logic. Apply **Replace Primitive with Object**. Create a new value class, update the source class's accessors to instantiate the value class, and move related behavior into the new class.
4.  **Eliminate Temporary Variables**:
    *   Identify variables holding derived calculations. Apply **Replace Temp with Query**. Ensure the logic is side-effect-free, extract to a getter/query method, and inline the variable at its usage sites.
5.  **Optimize Class Boundaries**:
    *   Evaluate class cohesion. If bloated, apply **Extract Class**: create a new class, link it from the parent, move fields/methods, and update interfaces.
    *   If anemic, apply **Inline Class**: move all fields/methods to the delegating class and delete the source class.
6.  **Tune Object Navigation**:
    *   Evaluate call chains. If clients are tightly coupled to delegates, apply **Hide Delegate** by adding forwarding methods to the server.
    *   If the server is just a bloated proxy, apply **Remove Middle Man** by exposing the delegate.
7.  **Simplify Implementations**:
    *   If a specific implementation is convoluted, isolate it and apply **Substitute Algorithm**.

# @Examples (Do's and Don'ts)

## Encapsulate Collection
*   [DON'T] Return a raw array reference allowing external modification.
```javascript
class Person {
  constructor(name) {
    this._name = name;
    this._courses = [];
  }
  get courses() { return this._courses; }
  set courses(aList) { this._courses = aList; }
}
// Client directly mutates internal state
aPerson.courses.push(new Course("Math"));
```
*   [DO] Return a copy of the collection and provide explicit mutation methods.
```javascript
class Person {
  constructor(name) {
    this._name = name;
    this._courses = [];
  }
  get courses() { return this._courses.slice(); } // Return a copy
  
  addCourse(aCourse) {
    this._courses.push(aCourse);
  }
  removeCourse(aCourse) {
    const index = this._courses.indexOf(aCourse);
    if (index !== -1) this._courses.splice(index, 1);
  }
}
// Client utilizes explicit API
aPerson.addCourse(new Course("Math"));
```

## Replace Temp with Query
*   [DON'T] Store calculations in local variables if they can be extracted to side-effect-free queries.
```javascript
class Order {
  get price() {
    const basePrice = this._quantity * this._item.price;
    let discountFactor = 0.98;
    if (basePrice > 1000) discountFactor -= 0.03;
    return basePrice * discountFactor;
  }
}
```
*   [DO] Extract derivations into queries to reduce function length and enable reuse.
```javascript
class Order {
  get price() {
    return this.basePrice * this.discountFactor;
  }
  get basePrice() {
    return this._quantity * this._item.price;
  }
  get discountFactor() {
    let factor = 0.98;
    if (this.basePrice > 1000) factor -= 0.03;
    return factor;
  }
}
```

## Hide Delegate
*   [DON'T] Force clients to navigate through internal relationships.
```javascript
// Client knows Person has a Department, and Department has a Manager
manager = aPerson.department.manager;
```
*   [DO] Hide the delegate by providing a forwarding method on the host object.
```javascript
class Person {
  // Encapsulates the Department structure from the client
  get manager() { return this._department.manager; }
}
// Client only talks to Person
manager = aPerson.manager;
```

## Replace Primitive with Object
*   [DON'T] Pass complex primitives around and duplicate their validation/formatting logic.
```javascript
class Order {
  constructor(data) {
    this.priority = data.priority; // String
  }
}
// Client duplicates string logic
highPriorityCount = orders.filter(o => "high" === o.priority || "rush" === o.priority).length;
```
*   [DO] Wrap the primitive in a Value Object to centralize its logic.
```javascript
class Priority {
  constructor(value) {
    if (!Priority.legalValues().includes(value)) throw new Error("Invalid priority");
    this._value = value;
  }
  toString() { return this._value; }
  get _index() { return Priority.legalValues().indexOf(this._value); }
  static legalValues() { return ['low', 'normal', 'high', 'rush']; }
  higherThan(other) { return this._index > other._index; }
}

class Order {
  get priority() { return this._priority; }
  set priority(aString) { this._priority = new Priority(aString); }
}
// Client utilizes domain logic
highPriorityCount = orders.filter(o => o.priority.higherThan(new Priority("normal"))).length;
```