@Domain
Trigger these rules when tasked with refactoring data structures, managing variable assignments, defining or renaming class/record fields, handling mutable/derived state, or designing object relationships (specifically choosing between value and reference semantics).

@Vocabulary
- **Collecting Variable**: A variable used to build up a value iteratively over time, such as sums, string concatenations, or stream writes.
- **Derived Variable**: A variable whose value can be entirely calculated from other existing data within the system.
- **Value Object**: An immutable object or data structure whose identity is based on its structural fields (value-based equality) rather than its memory reference.
- **Reference Object**: An object designed to be shared across multiple elements, where a state change in the object must be visible to all collaborators.
- **Repository / Registry**: A central store or lookup mechanism used to guarantee that only a single instance of a Reference Object exists for a given entity identifier.

@Objectives
- Ensure every variable and field has exactly one clear responsibility.
- Minimize the scope and existence of mutable data.
- Replace redundant or derivable state with functions/queries.
- Guarantee that shared logical entities are treated consistently as either immutable Values or shared References, based on their update lifecycle.

@Guidelines
- **Single Responsibility Variables**: When encountering a variable assigned to more than once (excluding loop counters and Collecting Variables), the AI MUST split it into multiple distinct variables, one for each responsibility.
- **Immutability by Default**: When splitting variables or creating Value Objects, the AI MUST declare the new variables/objects as immutable (e.g., using `const` or removing setter methods).
- **Input Parameter Integrity**: The AI MUST NEVER assign new values to input parameters. If an input parameter requires modification, the AI MUST split it by assigning the initial parameter to a new internal variable and mutating the internal variable instead.
- **Field Naming**: The AI MUST rename fields whenever their purpose changes or their current name lacks clarity. For widely used records, the AI MUST encapsulate the record first to safely transition the field name across getters, setters, and constructors.
- **Eradicate Derived State**: If a variable's value can be calculated from other existing data, the AI MUST replace the variable with a calculation (query/function). The only exception is if the source data and the resulting data structure are both strictly immutable.
- **Assertion Validation**: Before removing a derived variable, the AI MUST use an assertion to verify that the derived variable matches the calculated value.
- **Change Reference to Value**: If a nested object is never updated (or its updates should not affect shared collaborators), the AI MUST convert it to a Value Object. To do so, the AI MUST remove all setter methods and implement a value-based equality method (e.g., `equals()`).
- **Change Value to Reference**: If multiple physical copies of a logical data structure exist and require synchronized updates, the AI MUST convert them to a single Reference Object. The AI MUST route the creation and retrieval of this object through a Repository.

@Workflow
When analyzing and refactoring data structures, the AI MUST follow these specific algorithmic steps based on the identified code smell:

1. **Splitting Variables**:
   - Step 1: Scan for variables assigned more than once.
   - Step 2: Verify the variable is not a loop counter or a Collecting Variable.
   - Step 3: Change the name of the variable at its declaration and first assignment. Declare it as immutable (`const`).
   - Step 4: Change all references to this variable up to its second assignment.
   - Step 5: At the second assignment, declare a new variable with a new name.
   - Step 6: Repeat until all assignments belong to uniquely named, immutable variables.

2. **Renaming Fields**:
   - Step 1: If the record has limited scope, rename all accesses directly.
   - Step 2: If widely used, apply `Encapsulate Record` to hide the data structure.
   - Step 3: Add support for the new name in the constructor while retaining the old name temporarily.
   - Step 4: Rename the internal private field and update internal accessors.
   - Step 5: Update all external callers to use the new accessor names.
   - Step 6: Remove support for the old name.

3. **Replacing Derived Variables with Queries**:
   - Step 1: Identify all points of update for the variable.
   - Step 2: Create a function/getter that calculates the value dynamically.
   - Step 3: Insert an assertion to check that the stored variable equals the dynamically calculated value. Test the code.
   - Step 4: Replace all readers of the variable with calls to the new calculation function.
   - Step 5: Remove the original variable declaration and all its update assignments (Remove Dead Code).

4. **Changing Reference to Value**:
   - Step 1: Ensure the candidate class can become immutable.
   - Step 2: Remove all setter methods. Adjust the constructor to accept all necessary initial values.
   - Step 3: Implement a value-based `equals(other)` method that compares the fields of the object. (Implement a hashcode generator if required by the language).

5. **Changing Value to Reference**:
   - Step 1: Create a Repository (or use an existing one) to hold instances of the target object.
   - Step 2: Modify the host object's constructor to look up the correct instance from the Repository using an ID, rather than creating a new instance.
   - Step 3: Update all creation logic to rely on the Repository.

@Examples (Do's and Don'ts)

**Principle: Split Variable**
[DON'T] Reuse a variable for different computational steps.
```javascript
function distanceTravelled(scenario, time) {
  let acc = scenario.primaryForce / scenario.mass;
  let result = 0.5 * acc * time * time;
  
  // Reusing 'acc' for a different concept
  acc = (scenario.primaryForce + scenario.secondaryForce) / scenario.mass;
  result += 0.5 * acc * time * time;
  return result;
}
```

[DO] Split the variable into multiple immutable variables with specific names.
```javascript
function distanceTravelled(scenario, time) {
  const primaryAcceleration = scenario.primaryForce / scenario.mass;
  let result = 0.5 * primaryAcceleration * time * time;
  
  const secondaryAcceleration = (scenario.primaryForce + scenario.secondaryForce) / scenario.mass;
  result += 0.5 * secondaryAcceleration * time * time;
  return result;
}
```

**Principle: Input Parameter Integrity (Split Variable)**
[DON'T] Reassign input parameters.
```javascript
function discount(inputValue, quantity) {
  if (inputValue > 50) inputValue = inputValue - 2;
  return inputValue;
}
```

[DO] Assign the parameter to a new internal variable.
```javascript
function discount(inputValue, quantity) {
  let result = inputValue;
  if (inputValue > 50) result = result - 2;
  return result;
}
```

**Principle: Replace Derived Variable with Query**
[DON'T] Maintain redundant derived state that must be manually kept in sync.
```javascript
class ProductionPlan {
  constructor() {
    this._adjustments = [];
    this._production = 0; // Derived state
  }
  applyAdjustment(anAdjustment) {
    this._adjustments.push(anAdjustment);
    this._production += anAdjustment.amount; // Manual sync required
  }
  get production() { return this._production; }
}
```

[DO] Calculate the derived state dynamically.
```javascript
class ProductionPlan {
  constructor() {
    this._adjustments = [];
  }
  applyAdjustment(anAdjustment) {
    this._adjustments.push(anAdjustment);
  }
  get production() { 
    return this._adjustments.reduce((sum, a) => sum + a.amount, 0); 
  }
}
```

**Principle: Change Reference to Value**
[DON'T] Expose setters on objects that should be treated as interchangeable structural values.
```javascript
class TelephoneNumber {
  get areaCode() { return this._areaCode; }
  set areaCode(arg) { this._areaCode = arg; } // Mutability implies reference identity
  get number() { return this._number; }
  set number(arg) { this._number = arg; }
}
```

[DO] Remove setters to enforce immutability and add value-based equality checking.
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

**Principle: Change Value to Reference**
[DON'T] Instantiate multiple physical copies of the same logical entity.
```javascript
class Order {
  constructor(data) {
    this._number = data.number;
    // Creates a new copy of the customer for every order
    this._customer = new Customer(data.customerID); 
  }
}
```

[DO] Route instantiation through a shared repository.
```javascript
class Order {
  constructor(data) {
    this._number = data.number;
    // Retrieves the shared reference from a Repository
    this._customer = customerRepository.registerOrFindCustomer(data.customerID); 
  }
}
```