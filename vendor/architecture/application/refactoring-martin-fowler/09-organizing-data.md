# @Domain
Triggered when the user requests code cleanup, refactoring, or restructuring specifically related to data structures, variable declarations, field naming, mutability, object identity (values vs. references), and state management.

# @Vocabulary
* **Split Variable:** The process of taking a variable used for multiple distinct purposes and dividing it into separate, single-purpose variables.
* **Collecting Variable (Accumulator):** A variable whose purpose is to build up a value over time (e.g., sums, string concatenations, stream writes). These are exempt from being split.
* **Derived Variable:** A mutable variable whose value can be entirely computed from other existing data within the system.
* **Value Object:** An object that is defined entirely by its data fields, rather than its memory identity. It is immutable and can be freely copied.
* **Reference Object:** An object that represents a unique, shared entity in a system. Modifications to it must be visible to all components referencing it.
* **Repository:** A centralized lookup mechanism or registry used to store and retrieve Reference Objects, ensuring only a single instance of a logical entity exists.
* **Self-Encapsulation:** The practice of accessing an object's own fields exclusively through its own getter/setter methods.

# @Objectives
* Ensure that every variable, field, and data structure has a single, unambiguous responsibility.
* Minimize mutable state across the code base; strongly prefer immutability.
* Eradicate data duplication, specifically variables that hold data that can be derived or calculated on demand.
* Clarify the architectural intent of objects by strictly defining them as either immutable Values or shared References.

# @Guidelines
* **Splitting Variables:**
  * The AI MUST split any variable that is assigned to more than once, UNLESS it is a loop variable or a Collecting Variable.
  * When splitting a variable, the AI MUST declare the newly separated variables as immutable (`const` in JavaScript/TypeScript) whenever the language permits.
  * The AI MUST NOT assign new values to an input parameter. If an input parameter is modified, the AI MUST declare a new local variable, initialize it with the parameter's value, and perform the modifications on the new variable.
* **Renaming Fields:**
  * The AI MUST rename data structure fields if their current names do not perfectly convey their purpose.
  * For widely used fields (broad scope), the AI MUST first use the `Encapsulate Record` refactoring to wrap the data access in getters/setters before renaming the underlying field.
* **Replacing Derived Variables with Queries:**
  * The AI MUST evaluate if a mutated variable can be calculated from other source data. If so, the AI MUST replace the variable with a calculating function or getter.
  * Before completely removing a derived variable, the AI MUST insert an assertion (e.g., `assert(this._variable === this.calculatedValue)`) to guarantee the replacement logic perfectly matches the old state tracking.
  * EXCEPTION: The AI MAY retain a derived variable if the source data is strictly immutable and calculating the derivation is exceptionally expensive, creating an immutable resultant data structure.
* **Changing Reference to Value:**
  * If an object is nested within another and is not shared across the broader system, the AI MUST convert it into a Value Object.
  * To convert to a Value Object, the AI MUST remove all setter methods to make the object completely immutable.
  * The AI MUST implement a value-based equality method (e.g., `equals(other)`) and a corresponding hashcode generator (if applicable to the language) for the new Value Object.
* **Changing Value to Reference:**
  * If the AI detects multiple identical logical entities (e.g., multiple copies of "Customer 123") being instantiated across different records, it MUST convert them into a single Reference Object.
  * The AI MUST use a Repository or registry pattern to manage Reference Objects.
  * The AI MUST modify constructors to fetch the single shared instance from the Repository using an identifier, rather than instantiating a new duplicate object.

# @Workflow
1. **Data Scope Analysis:** Scan the active function or class. Identify variables assigned multiple times, parameters being mutated, or fields whose names obscure their intent.
2. **Variable Splitting & Lockdown:**
   * For variables repurposed mid-function, rename the first use and declare it as a constant. Declare a new constant for the second use.
   * For mutated parameters, create a local copy (e.g., `let result = originalInputValue;`) and mutate the copy.
3. **State Derivation Elimination:**
   * Scan classes for properties updated via accumulators or external methods alongside other data.
   * Write a query method that calculates this state from raw arrays/records.
   * Add an assertion verifying the existing property equals the query result.
   * Replace all reads of the property with the query.
   * Delete the original property and all assignment operations targeting it.
4. **Field Renaming Migration:**
   * Identify poorly named fields. If the data is a bare record accessed globally, encapsulate it into a class.
   * Rename the private backing field first, then update the constructor, then rename the public accessor functions.
5. **Object Identity Resolution:**
   * Evaluate nested objects. Ask: "If a property of this object changes, should the rest of the system see it?"
   * *If NO (Value Route):* Make it a Value Object. Remove all setters. Re-route updates to instantiate entirely new instances. Add an `equals()` method.
   * *If YES (Reference Route):* Create an external Repository map. Alter the parent object's constructor to take an ID, lookup the reference from the Repository, and assign the shared reference.

# @Examples (Do's and Don'ts)

### Splitting Variables
**[DO]**
```javascript
function distanceTraveled(scenario, time) {
  const primaryAcceleration = scenario.primaryForce / scenario.mass;
  let primaryTime = Math.min(time, scenario.delay);
  let result = 0.5 * primaryAcceleration * primaryTime * primaryTime;
  let secondaryTime = time - scenario.delay;
  if (secondaryTime > 0) {
    let primaryVelocity = primaryAcceleration * scenario.delay;
    const secondaryAcceleration = (scenario.primaryForce + scenario.secondaryForce) / scenario.mass;
    result += primaryVelocity * secondaryTime + 0.5 * secondaryAcceleration * secondaryTime * secondaryTime;
  }
  return result;
}
```
**[DON'T]** (Reusing `acc` for two different mathematical concepts)
```javascript
function distanceTraveled(scenario, time) {
  let acc = scenario.primaryForce / scenario.mass;
  // ... calculations ...
  acc = (scenario.primaryForce + scenario.secondaryForce) / scenario.mass;
  // ... more calculations using the new acc ...
}
```

### Mutating Input Parameters
**[DO]**
```javascript
function discount(inputValue, quantity) {
  let result = inputValue;
  if (inputValue > 50) result = result - 2;
  if (quantity > 100) result = result - 1;
  return result;
}
```
**[DON'T]**
```javascript
function discount(inputValue, quantity) {
  if (inputValue > 50) inputValue = inputValue - 2;
  if (quantity > 100) inputValue = inputValue - 1;
  return inputValue;
}
```

### Replacing Derived Variables with Queries
**[DO]**
```javascript
class ProductionPlan {
  get production() {
    return this._adjustments.reduce((sum, a) => sum + a.amount, 0);
  }
  applyAdjustment(anAdjustment) {
    this._adjustments.push(anAdjustment);
  }
}
```
**[DON'T]** (Manually keeping an accumulator field in sync)
```javascript
class ProductionPlan {
  get production() { return this._production; }
  
  applyAdjustment(anAdjustment) {
    this._adjustments.push(anAdjustment);
    this._production += anAdjustment.amount;
  }
}
```

### Changing Reference to Value
**[DO]** (Immutable class with equality test)
```javascript
class TelephoneNumber {
  constructor(areaCode, number) {
    this._areaCode = areaCode;
    this._number = number;
  }
  get areaCode() { return this._areaCode; }
  get number() { return this._number; }
  equals(other) {
    if (!(other instanceof TelephoneNumber)) return false;
    return this.areaCode === other.areaCode && this.number === other.number;
  }
}
```
**[DON'T]** (Value objects possessing mutating setter methods)
```javascript
class TelephoneNumber {
  get areaCode() { return this._areaCode; }
  set areaCode(arg) { this._areaCode = arg; } // BAD: Mutable value
}
```

### Changing Value to Reference
**[DO]** (Using a repository for shared entities)
```javascript
class Order {
  constructor(data) {
    this._number = data.number;
    this._customer = customerRepository.get(data.customerId);
  }
}
```
**[DON'T]** (Blindly instantiating what should be shared domain entities)
```javascript
class Order {
  constructor(data) {
    this._number = data.number;
    // BAD: Creates a disconnected physical duplicate of the same customer
    this._customer = new Customer(data.customerId); 
  }
}
```