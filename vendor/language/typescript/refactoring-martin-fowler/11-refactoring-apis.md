# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, reviewing, or refactoring Application Programming Interfaces (APIs), function signatures, class interfaces, object instantiation logic, or parameter lists. This includes tasks involving the separation of logic, dependency management between modules, and the conversion between object-oriented and functional paradigms for specific operations.

# @Vocabulary
- **Command-Query Separation**: The principle that a function should either return a value (Query) or produce an observable side effect (Modifier/Command), but never both.
- **Observable Side Effect**: A change in state that alters the behavior of subsequent operations. Caching a value internally is NOT considered an observable side effect.
- **Flag Argument**: A function parameter (often a boolean, enum, or string) set by the caller as a literal value to dictate which internal control flow the function should execute.
- **Referential Transparency**: The property of a function where it consistently yields the same output given the same input parameters, free from reliance on mutable external state.
- **Command Object (Command)**: An object that encapsulates a function or request, typically built around a single execution method, allowing for complex lifecycles, undo operations, or detailed state sharing.
- **Factory Function**: A standard function that wraps the instantiation of an object, free from the constraints of class constructors (e.g., fixed naming, obligatory return of the exact class, required `new` keyword).
- **Type-Instance Homonym**: A modeling error where a class representing a type of thing is incorrectly used or extended to represent a physical instance of that thing.

# @Objectives
- Ensure APIs are explicit, predictable, and easy to consume for callers.
- Enforce strict Command-Query Separation to maximize referential transparency and testability.
- Minimize parameter list size and complexity by passing whole objects and deriving values internally where appropriate.
- Maximize immutability by removing unnecessary setting methods and locking down object state post-construction.
- Decouple modules by carefully evaluating whether a function should resolve its own dependencies or receive them as parameters.
- Utilize the appropriate level of abstraction for operations (simple functions vs. Command Objects) based on complexity.

# @Guidelines

## API Structure and Side Effects
- When encountering a function that returns a value AND produces an observable side effect, the AI MUST separate it into two distinct functions: a Query (returning the value) and a Modifier (performing the side effect).
- The AI MAY permit internal side effects (like lazy initialization or caching) within a Query ONLY IF the state change is not observable to the caller and subsequent queries return identical results.

## Parameter Management
- When encountering multiple functions executing similar logic but varying only by literal values, the AI MUST unify them using Parameterize Function.
- When encountering a function that accepts a Flag Argument (a literal boolean, enum, or string used to trigger different internal logic), the AI MUST remove the flag argument and expose an explicit function for each logic path.
- When encountering code that extracts multiple values from a record/object solely to pass them into a function, the AI MUST pass the whole object instead (Preserve Whole Object), UNLESS passing the whole object introduces an unwanted dependency across module boundaries.
- When encountering a function receiving a parameter that it could easily derive itself from another parameter without breaking referential transparency, the AI MUST remove the parameter and let the function query the value internally (Replace Parameter with Query).
- When encountering a function that queries a global variable or external module element (breaking referential transparency or introducing tight coupling), the AI MUST replace the internal query with a parameter, forcing the caller to provide the dependency (Replace Query with Parameter).

## Object Lifecycle and Immutability
- When encountering a class field that should not change after object instantiation, the AI MUST remove the setting method, initialize the field exclusively via the constructor, and ensure the field is immutable.
- When encountering object instantiation logic that is limited by constructor constraints (e.g., inability to return subclasses, unclear naming), the AI MUST replace the constructor with a Factory Function.
- The AI MUST restrict the visibility of constructors when Factory Functions are introduced, forcing clients to use the explicit factory methods.

## Function vs. Command Object
- When encountering an excessively complex function that requires tracking multiple interrelated local variables or implementing lifecycle hooks (e.g., undo), the AI MUST extract the function into a Command Object.
- When transforming a function to a Command Object, the AI MUST pass necessary context through the constructor and execute the behavior via a parameterless method (e.g., `execute()`).
- When encountering a simple Command Object that does not utilize advanced lifecycle features, the AI MUST replace the Command Object with a standard function to reduce unnecessary complexity.

# @Workflow
When evaluating or refactoring an API or function, the AI MUST execute the following algorithmic process:

1. **Side-Effect Audit**: 
   - Does the function return a value AND alter state?
   - *Action*: Duplicate the function. Strip side effects from the first (Query). Strip the return value from the second (Modifier). Update callers to call the Query, then the Modifier.

2. **Parameter Signature Audit**:
   - Check for Flag Arguments: Does the caller pass a literal boolean/string used in a top-level conditional?
   - *Action*: Create explicit functions for each conditional branch. Update callers to use the specific function. Remove the flag parameter.
   - Check for Unpacking: Does the caller extract properties from an object to pass to the function?
   - *Action*: Change the function signature to accept the whole object. Update the function body to extract the properties internally.
   - Check Derivability: Can the function calculate a parameter itself?
   - *Action*: Extract the calculation inside the function, remove the parameter.
   - Check Purity: Does the function access an external/global dependency?
   - *Action*: Extract the dependency into a parameter. Update callers to pass the dependency in.

3. **Immutability and Initialization Audit**:
   - Check Setters: Are there setters used only during an initial creation script or never intended to be updated?
   - *Action*: Move the data injection to the constructor. Delete the setter.
   - Check Constructors: Is the instantiation logic complex, requiring subclass dispatch or clearer naming?
   - *Action*: Wrap the constructor in a Factory Function. Update callers to use the Factory Function.

4. **Complexity Audit**:
   - Is the function monolithic, passing around excessive temporary variables?
   - *Action*: Create a Command class. Move parameters to the constructor. Convert local variables to class fields. Extract logic into smaller internal methods.
   - Is there a Command class that does nothing but hold a few variables and run a simple `execute`?
   - *Action*: Inline the Command class back into a single standard function.

# @Examples (Do's and Don'ts)

## Separate Query from Modifier
- **[DON'T]** Mix returning a value with an observable state mutation.
```javascript
function alertForMiscreant(people) {
  for (const p of people) {
    if (p === "Don") {
      setOffAlarms(); // Modifier
      return "Don";   // Query
    }
  }
  return "";
}
```
- **[DO]** Separate into two distinct functions.
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
// Caller uses:
// const found = findMiscreant(people);
// alertForMiscreant(people);
```

## Remove Flag Argument
- **[DON'T]** Force callers to use literal flag arguments to dispatch logic.
```javascript
function bookConcert(customer, isPremium) {
  if (isPremium) {
    // premium logic
  } else {
    // regular logic
  }
}
// Caller: bookConcert(customer, true);
```
- **[DO]** Provide explicit functions for different behaviors.
```javascript
function premiumBookConcert(customer) {
  // premium logic
}
function regularBookConcert(customer) {
  // regular logic
}
// Caller: premiumBookConcert(customer);
```

## Preserve Whole Object
- **[DON'T]** Unpack an object just to pass its parts to a function (unless avoiding cross-module coupling).
```javascript
const low = aRoom.daysTempRange.low;
const high = aRoom.daysTempRange.high;
if (!aPlan.withinRange(low, high)) {
  alerts.push("room temperature went outside range");
}
```
- **[DO]** Pass the whole object and let the function extract what it needs.
```javascript
if (!aPlan.withinRange(aRoom.daysTempRange)) {
  alerts.push("room temperature went outside range");
}

class HeatingPlan {
  withinRange(aNumberRange) {
    return (aNumberRange.low >= this._temperatureRange.low) && 
           (aNumberRange.high <= this._temperatureRange.high);
  }
}
```

## Replace Parameter with Query
- **[DON'T]** Force the caller to pass a value the function can easily determine itself.
```javascript
get finalPrice() {
  const basePrice = this.quantity * this.itemPrice;
  let discountLevel = (this.quantity > 100) ? 2 : 1;
  return this.discountedPrice(basePrice, discountLevel);
}
discountedPrice(basePrice, discountLevel) {
  switch (discountLevel) { // ... }
}
```
- **[DO]** Let the function query the value itself to reduce parameter load.
```javascript
get finalPrice() {
  const basePrice = this.quantity * this.itemPrice;
  return this.discountedPrice(basePrice);
}
get discountLevel() {
  return (this.quantity > 100) ? 2 : 1;
}
discountedPrice(basePrice) {
  switch (this.discountLevel) { // ... }
}
```

## Remove Setting Method
- **[DON'T]** Provide setters for fields that should only be defined at instantiation.
```javascript
const martin = new Person();
martin.name = "martin";
martin.id = "1234"; // ID shouldn't change after creation
```
- **[DO]** Pass immutable data through the constructor and remove the setter.
```javascript
const martin = new Person("1234");
martin.name = "martin";

class Person {
  constructor(id) {
    this._id = id;
  }
  get id() { return this._id; }
  // No set id() provided
}
```