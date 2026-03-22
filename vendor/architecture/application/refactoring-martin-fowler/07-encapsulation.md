## @Domain
These rules are activated when the AI performs refactoring tasks aimed at improving information hiding, data protection, and module decomposition. This includes manipulating data structures, collections, primitive values, temporary variables, class boundaries, and object delegations.

## @Vocabulary
- **Encapsulation:** The practice of hiding the internal secrets (data structures and implementations) of a module from the rest of the system.
- **Implicit Record:** Data structures like hashes, maps, or dictionaries that allow arbitrary field assignment without explicitly declaring their structure.
- **Value Object:** An immutable object representing a data value (e.g., a telephone number or coordinate) that relies on value-based equality rather than reference-based equality.
- **Read-only Proxy:** A wrapper around a collection or record that forwards read requests but blocks or throws exceptions on write requests.
- **Deep Copy:** Recursively duplicating a nested data structure so that modifications to the copy do not affect the original source data.
- **Middle Man:** An object whose primary purpose has degraded to merely forwarding or delegating requests to another object without adding value.
- **Query:** A function or method that calculates and returns a value without causing any observable side effects.

## @Objectives
- **Protect Mutable Data:** Hide all mutable data behind well-defined object boundaries and accessors.
- **Prevent Accidental Mutation:** Ensure that getters for collections or nested records do not expose the underlying mutable reference.
- **Elevate Primitives:** Transform primitive data types that attract domain-specific behavior into dedicated classes.
- **Reduce State:** Eliminate temporary variables in favor of query functions to make logic extraction easier.
- **Balance Class Responsibilities:** Continually evaluate whether classes are too large (needing extraction) or too thin (needing inlining).
- **Manage Coupling:** Hide delegates to reduce client coupling, but ruthlessly remove middle men if forwarding becomes excessive.

## @Guidelines

### 1. Encapsulate Record
- The AI MUST favor Objects over implicit records (hashes/maps/dictionaries) for mutable data to hide storage details and support derived values.
- When encapsulating deeply nested records (e.g., parsed JSON), the AI MUST focus on encapsulating the updates (setters) first.
- For nested record readers, the AI MUST return either a deep copy of the data or a read-only proxy to prevent accidental modification of the encapsulated data.
- The AI MAY leave immutable values in basic record structures, as immutability acts as its own preservative.

### 2. Encapsulate Collection
- The AI NEVER MUST return a direct reference to a mutable collection from a getter. 
- Getters for collections MUST return a protected view, either via a copy (e.g., `slice()` in JavaScript) or a read-only proxy.
- The AI MUST provide specific collection modifier methods (e.g., `addCourse`, `removeCourse`) rather than allowing clients to manipulate the collection directly.
- If a collection setter is absolutely required, it MUST assign a copy of the provided collection to the internal field.

### 3. Replace Primitive with Object
- When a primitive value (string, number) requires domain-specific behavior (e.g., formatting, parsing, validation), the AI MUST wrap it in a class.
- The newly created class MUST be treated as a Value Object (it should be immutable and provide value-based equality methods).

### 4. Replace Temp with Query
- The AI MUST replace temporary variables used for holding calculated values with query functions.
- The AI MUST ensure the variable being replaced is calculated only once and the extracted query has no side effects.
- If a temporary variable is reassigned multiple times for different purposes, the AI MUST first use `Split Variable` before replacing it with a query.

### 5. Extract Class and Inline Class
- **Extract Class:** If a class grows to encompass multiple responsibilities or has subsets of data/methods that change together, the AI MUST extract those subsets into a new child class.
- **Inline Class:** If a class no longer pulls its weight (e.g., due to previous refactorings moving its behavior elsewhere), the AI MUST inline its remaining features into the most appropriate consuming class and delete the empty class.

### 6. Hide Delegate and Remove Middle Man
- **Hide Delegate:** If a client accesses a delegate object through a server object (e.g., `aPerson.department.manager`), the AI MUST hide the delegate by creating a forwarding method on the server (e.g., `aPerson.manager`).
- **Remove Middle Man:** If a server class exists primarily to forward requests to a delegate (meaning every new feature requires a boring forwarding method), the AI MUST expose the delegate directly and remove the forwarding methods.

### 7. Substitute Algorithm
- Before replacing a complex algorithm, the AI MUST isolate the algorithm into a single function.
- The AI MUST prepare tests to capture the old algorithm's output and verify the new algorithm's output against it before completely removing the old code.

## @Workflow
When tasked with refactoring data structures or class relationships, the AI MUST execute the following algorithmic steps:

1.  **Identify Secrets:** Scan the target code for exposed mutable data, implicit records, bare collections, calculation-heavy temporary variables, and primitive obsession.
2.  **Encapsulate Access:** 
    - Wrap implicit records and primitives in dedicated classes.
    - Replace public properties with getters/setters.
3.  **Harden Boundaries (Collections & Records):** 
    - Modify collection getters to append `.slice()` or equivalent copy mechanisms. 
    - Implement `add[Item]` and `remove[Item]` methods.
    - Replace nested record getters with deep copy mechanisms (e.g., `_.cloneDeep`).
4.  **Eliminate Temporary Variables:** 
    - Change `let` to `const` for the target temp to ensure it is read-only.
    - Extract the right-hand calculation into a getter or query function.
    - Inline the temporary variable across the function.
5.  **Evaluate Class Cohesion:** 
    - Check if the newly added behaviors bloat the class. If yes, extract a new class.
    - Check if previous extractions left a class hollow. If yes, inline it.
6.  **Evaluate Coupling:** 
    - Check the chain of object calls (Message Chains). If a client reaches through an object, Hide the Delegate. If the object is just a shell of forwarders, Remove the Middle Man.
7.  **Test:** Halt and request/run tests after every single structural change.

## @Examples (Do's and Don'ts)

### Encapsulate Collection
- **[DO]**
```javascript
class Person {
  constructor(name) {
    this._name = name;
    this._courses = [];
  }
  get courses() { return this._courses.slice(); } // Returns a copy
  addCourse(aCourse) { this._courses.push(aCourse); }
  removeCourse(aCourse) { ... }
}
```
- **[DON'T]**
```javascript
class Person {
  get courses() { return this._courses; } // Exposes internal mutable array
  set courses(aList) { this._courses = aList; }
}
```

### Replace Temp with Query
- **[DO]**
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
- **[DON'T]**
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

### Replace Primitive with Object
- **[DO]**
```javascript
class TelephoneNumber {
  constructor(areaCode, number) {
    this._areaCode = areaCode;
    this._number = number;
  }
  get areaCode() { return this._areaCode; }
  get number() { return this._number; }
  toString() { return `(${this.areaCode}) ${this.number}`; }
}

class Person {
  get telephoneNumber() { return this._telephoneNumber.toString(); }
}
```
- **[DON'T]**
```javascript
class Person {
  get telephoneNumber() { 
    // Domain logic leaked into the client class using primitive strings
    return `(${this._officeAreaCode}) ${this._officeNumber}`; 
  }
}
```

### Hide Delegate
- **[DO]**
```javascript
class Person {
  get manager() {
    return this._department.manager; // Hides department from client
  }
}
// Client usage:
const manager = aPerson.manager;
```
- **[DON'T]**
```javascript
// Client usage:
const manager = aPerson.department.manager; // Client knows too much about Person's internals
```