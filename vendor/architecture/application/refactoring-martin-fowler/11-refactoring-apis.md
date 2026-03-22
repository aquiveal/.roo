@Domain
Trigger these rules when designing, modifying, or refactoring module boundaries, class interfaces, function signatures, or application programming interfaces (APIs). Activation occurs whenever the AI is tasked with adding parameters, changing method visibility, splitting logic, or managing object instantiation and state mutation.

@Vocabulary
- **API (Application Programming Interface):** The joints that plug modules together; the function declarations and their parameters.
- **Command-Query Separation:** The principle stating that a function returning a value (Query) must not have observable side effects (Modifier/Command).
- **Observable Side Effect:** A change in state visible outside the function. (Internal transparent caching is not considered an observable side effect).
- **Flag Argument:** A boolean, enum, or string literal passed by a caller to dictate the internal control flow of the called function.
- **Referential Transparency:** A property of a function where it always yields the same result when called with the same parameter values.
- **Command Object:** An object that encapsulates a function/request, typically built around a single execution method, allowing for complex lifecycles, state sharing, or undo operations.
- **Factory Function:** A standard function whose purpose is to invoke a constructor, offering flexibility in naming and returning subclasses.

@Objectives
- Create clear, explicit, and easy-to-understand joints between software modules.
- Strictly separate data retrieval from state mutation.
- Eliminate duplicated logic differing only by literal values.
- Ensure function calls explicitly communicate intent rather than hiding behavior behind literal control flags.
- Optimize parameter lists to balance minimal length with referential transparency.
- Maximize immutability by eliminating unnecessary state mutators.
- Utilize standard functions over complex structural constructs unless advanced lifecycles or state tracking are strictly required.

@Guidelines

**Command-Query Separation**
- The AI MUST NOT combine state mutation and data retrieval in a single function. If a function returns a value, the AI MUST extract any observable side effects into a separate modifier function.
- The AI MAY use internal caching within a query function, provided the cache does not alter the observable state of the object.

**Function Parameterization & Flag Arguments**
- When encountering multiple functions containing nearly identical logic that varies only by literal values, the AI MUST consolidate them into a single parameterized function.
- The AI MUST NOT use Flag Arguments (literals like `true`/`false`, `"premium"`, etc., used to dictate control flow). 
- When encountering a Flag Argument, the AI MUST decompose the function and create explicit, intent-named functions for each variation (e.g., `rushDeliveryDate()` and `regularDeliveryDate()`).
- *Exception:* If the parameter represents dynamic data flowing through the application (not a hardcoded literal) or if it does not dictate internal control flow, it is not a Flag Argument and MAY be retained.

**Object Preservation vs. Unpacking**
- When a function requires multiple values derived from the same record/object, the AI MUST pass the whole object instead of unpacking individual fields.
- *Exception:* The AI MUST NOT pass the whole object if doing so introduces an unwanted architectural dependency between decoupled modules.

**Balancing Parameters and Queries**
- To shorten parameter lists, the AI MUST replace a parameter with an internal query if the called function can easily and safely resolve the value itself.
- *Exception:* The AI MUST NOT replace a parameter with an internal query if the query relies on mutable global state or breaks the function's Referential Transparency.
- Conversely, if a function contains internal queries to global variables or tightly coupled modules, the AI MUST extract those internal queries and replace them with parameters, thereby purifying the function and enforcing Referential Transparency.

**Immutability and Object Construction**
- The AI MUST remove setting methods (setters) for fields that should not change after object creation. The AI MUST pass these values via the constructor and make the fields immutable.
- The AI MUST replace class Constructors with Factory Functions when the initialization requires returning a subclass, returning a proxy, or when a descriptive name is required to clarify the instantiation intent.

**Command Objects**
- The AI MUST encapsulate a function into a Command Object ONLY IF the function is highly complex, requires extensive local state sharing across sub-functions, or requires advanced lifecycles (like `undo` operations).
- The AI MUST default to using first-class functions 95% of the time. If an existing Command Object does not utilize advanced capabilities and is simple enough, the AI MUST revert it back into a standard function.

@Workflow
1. **Analyze Side Effects:** Scan the target function. If it returns a value and mutates state, split it into two functions: one query, one modifier.
2. **Analyze Parameters:** 
   - Check for literal Flag Arguments. If found, split the function into explicit variations.
   - Check for unpacked data clumps. If fields belong to a single object, modify the signature to accept the whole object.
   - Check for unnecessary parameters. If the function can derive the parameter transparently, calculate it internally.
   - Check for hidden dependencies. If the function queries global/mutable state, move that query to the parameter list.
3. **Analyze Mutability:** Review the class properties. Identify fields that are never updated after initialization. Remove their setters and require them in the constructor.
4. **Analyze Instantiation:** Review constructor usage. If the constructor logic relies on type codes or requires descriptive intent, wrap the constructor in a Factory Function.
5. **Analyze Complexity:** Review long functions. If extracting sub-functions is hindered by tangled local variables, convert the function into a Command Object. If a Command Object is trivial, inline it back into a plain function.

@Examples (Do's and Don'ts)

**Separate Query from Modifier**
- [DON'T]: Use a function that finds a value and triggers an action.
  ```javascript
  function findMiscreant(people) {
    for (const p of people) {
      if (p === "Don") {
        setOffAlarms();
        return "Don";
      }
    }
    return "";
  }
  ```
- [DO]: Separate the query from the action.
  ```javascript
  function findMiscreant(people) {
    for (const p of people) {
      if (p === "Don") return "Don";
    }
    return "";
  }
  function alertForMiscreant(people) {
    if (findMiscreant(people) !== "") setOffAlarms();
  }
  ```

**Remove Flag Argument**
- [DON'T]: Pass a literal boolean to alter control flow.
  ```javascript
  aShipment.deliveryDate = deliveryDate(anOrder, true);
  function deliveryDate(anOrder, isRush) {
    if (isRush) { /* rush logic */ } 
    else { /* regular logic */ }
  }
  ```
- [DO]: Provide explicit functions for explicit intent.
  ```javascript
  aShipment.deliveryDate = rushDeliveryDate(anOrder);
  function rushDeliveryDate(anOrder) { /* rush logic */ }
  function regularDeliveryDate(anOrder) { /* regular logic */ }
  ```

**Preserve Whole Object**
- [DON'T]: Unpack fields unnecessarily before calling.
  ```javascript
  const low = aRoom.daysTempRange.low;
  const high = aRoom.daysTempRange.high;
  if (!aPlan.withinRange(low, high)) { ... }
  ```
- [DO]: Pass the whole object.
  ```javascript
  if (!aPlan.withinRange(aRoom.daysTempRange)) { ... }
  ```

**Replace Constructor with Factory Function**
- [DON'T]: Rely on constructors for varied instantiation logic.
  ```javascript
  const leadEngineer = new Employee(document.leadEngineer, 'E');
  ```
- [DO]: Use descriptive factory functions.
  ```javascript
  const leadEngineer = createEngineer(document.leadEngineer);
  function createEngineer(name) {
    return new Employee(name, 'E');
  }
  ```

**Remove Setting Method**
- [DON'T]: Provide setters for properties that form the immutable identity of an object.
  ```javascript
  const martin = new Person();
  martin.id = "1234"; // Setter allows subsequent, unwanted changes
  ```
- [DO]: Initialize via the constructor and remove the setter entirely.
  ```javascript
  const martin = new Person("1234");
  class Person {
    constructor(id) {
      this._id = id;
    }
    get id() { return this._id; }
    // No set id() provided
  }
  ```