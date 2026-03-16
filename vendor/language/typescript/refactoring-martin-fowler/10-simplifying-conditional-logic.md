# @Domain

These rules MUST be triggered whenever the AI is tasked with analyzing, writing, or refactoring conditional logic (`if/else` statements, `switch/case` statements, nested conditionals), handling special or `null` values, or addressing unstated program state assumptions.

# @Vocabulary

- **Decompose Conditional**: The practice of extracting the conditional expression, the `then` block, and the `else` block into individual, well-named functions.
- **Consolidate Conditional Expression**: The practice of combining multiple conditional checks that yield the exact same result into a single logical expression using `and` (`&&`) or `or` (`||`) operators.
- **Guard Clause**: An early `return` statement used to handle unusual conditions or edge cases, exiting the function immediately rather than wrapping the primary logic in nested `if/else` blocks.
- **Polymorphism (Conditional)**: Using object-oriented class hierarchies and overridden methods to handle branching logic based on types, rather than using `switch/case` or `if/else` on type codes.
- **Special Case (Null Object)**: A distinct object, literal, or data transform created to handle a recurring specific value (such as `null` or `"unknown"`) that currently requires repetitive conditional checks across a codebase.
- **Assertion**: A conditional statement assumed to always be true, used to explicitly state a programmer's assumption about the state of the program (e.g., a number being positive). 

# @Objectives

- Replace the "what" of complex conditional statements with the "why" by extracting them into well-named functions.
- Linearize execution flow and eliminate nested conditional blocks by utilizing guard clauses for edge cases.
- Eliminate duplicated conditional logic centered around type codes by leveraging polymorphic class hierarchies.
- Standardize the handling of recurring absent or special values by introducing Special Case objects, preventing scattered `null` or value checks.
- Make unstated program assumptions explicit, visible, and strictly verifiable via assertions.

# @Guidelines

- **Decompose Complex Conditionals**: The AI MUST extract complex conditional checks, as well as their corresponding `then` and `else` execution blocks, into separate functions named after their intent.
- **Use Ternary Operators**: After decomposing conditionals, the AI SHOULD format the conditional using a ternary operator if it simply assigns or returns a value.
- **Consolidate Identical Outcomes**: If a sequence of conditional checks or nested `if` statements results in the exact same action or return value, the AI MUST combine them into a single conditional expression.
- **No Side Effects in Conditionals**: Before consolidating conditionals, the AI MUST ensure that none of the conditional checks have side effects.
- **Favor Guard Clauses for Edge Cases**: The AI MUST NOT use nested `if-else` blocks when one leg is the "normal" behavior and the other is an "unusual" condition. The AI MUST use a guard clause to return early for the unusual condition. The AI MUST ignore the outdated "one exit point per function" rule.
- **Reverse Conditions for Clarity**: When introducing guard clauses, the AI SHOULD consider reversing the conditional logic (e.g., `if (a > 0)` becomes `if (a <= 0) return`) if it simplifies the extraction of the guard clause.
- **Replace Type-Switching with Polymorphism**: Whenever the AI encounters `switch` statements or `if/else` chains that branch based on a type code or variant state, it MUST create subclasses for each case, override the method in the subclasses, and use a factory function to instantiate the correct subclass.
- **Introduce Special Cases**: If the AI detects multiple places in the code reacting the exact same way to a specific value (e.g., `null`, `"unknown"`), it MUST create a Special Case object or literal that encapsulates this default behavior, modifying the source to return this Special Case instead of the raw value.
- **Assert Preconditions**: The AI MUST explicitly state required preconditions (e.g., a required parameter presence, a positive number) using assertions. 
- **Restrict Assertion Usage**: The AI MUST ONLY use assertions to catch programmer errors (things that should never fail). Assertions MUST NOT be used for validating external input or data from untrusted sources.

# @Workflow

1. **Side-Effect Check**: Analyze all conditional expressions. If any condition alters state, separate the query from the modifier before proceeding.
2. **Type-Code Evaluation**: Check the logic for `switch/case` or `if/else` structures branching on a `type` property. If found, generate a base class, create subclasses for each type, move the conditional logic to the overriding subclass methods, and introduce a factory function.
3. **Special Value Check**: Scan the codebase for repetitive checks against a specific value (e.g., `if (customer === "unknown")`). If found, construct a Special Case class or object literal that implements the default responses for that value, and update the data provider to return the Special Case.
4. **Guard Clause Flattening**: Identify nested conditionals where one branch represents the primary logic and others represent edge cases. Flatten the structure by converting the edge cases into early `return` guard clauses.
5. **Consolidation**: Identify adjacent conditionals or nested `if` statements that execute the exact same block of code. Combine them using `&&` or `||` operators, then extract the combined expression into a named function.
6. **Decomposition**: For any remaining `if/else` statements that are complex or difficult to read, extract the condition, the `then` logic, and the `else` logic into individually named helper functions.
7. **Assumption Declaration**: Review the final logic for unstated dependencies (e.g., a variable that must not be zero). Insert assertions to make these assumptions explicit.

# @Examples (Do's and Don'ts)

### Decomposing Conditionals

[DON'T] Leave complex logic inline, explaining "what" rather than "why".
```javascript
if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
  charge = quantity * plan.summerRate;
} else {
  charge = quantity * plan.regularRate + plan.regularServiceCharge;
}
```

[DO] Extract the condition and the branches into named functions.
```javascript
charge = isSummer() ? summerCharge() : regularCharge();

function isSummer() {
  return !aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd);
}
function summerCharge() {
  return quantity * plan.summerRate;
}
function regularCharge() {
  return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

### Consolidating Conditional Expressions

[DON'T] Write sequential conditionals that do the exact same thing.
```javascript
function disabilityAmount(anEmployee) {
  if (anEmployee.seniority < 2) return 0;
  if (anEmployee.monthsDisabled > 12) return 0;
  if (anEmployee.isPartTime) return 0;
  // compute the disability amount
}
```

[DO] Consolidate into a single expression and extract to a named function.
```javascript
function disabilityAmount(anEmployee) {
  if (isNotEligibleForDisability()) return 0;
  // compute the disability amount

  function isNotEligibleForDisability() {
    return ((anEmployee.seniority < 2) || 
            (anEmployee.monthsDisabled > 12) || 
            (anEmployee.isPartTime));
  }
}
```

### Replacing Nested Conditionals with Guard Clauses

[DON'T] Use nested if/else blocks that hide the primary execution path.
```javascript
function payAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = {amount: 0, reasonCode: "SEP"};
  } else {
    if (employee.isRetired) {
      result = {amount: 0, reasonCode: "RET"};
    } else {
      result = someFinalComputation();
    }
  }
  return result;
}
```

[DO] Use guard clauses to handle edge cases and return early.
```javascript
function payAmount(employee) {
  if (employee.isSeparated) return {amount: 0, reasonCode: "SEP"};
  if (employee.isRetired) return {amount: 0, reasonCode: "RET"};
  
  return someFinalComputation();
}
```

### Replacing Conditional with Polymorphism

[DON'T] Use switch statements on type codes to dictate behavior.
```javascript
function plumage(bird) {
  switch (bird.type) {
    case 'EuropeanSwallow':
      return "average";
    case 'AfricanSwallow':
      return (bird.numberOfCoconuts > 2) ? "tired" : "average";
    case 'NorwegianBlueParrot':
      return (bird.voltage > 100) ? "scorched" : "beautiful";
    default:
      return "unknown";
  }
}
```

[DO] Use class hierarchies and a factory function.
```javascript
function plumage(bird) {
  return createBird(bird).plumage;
}

function createBird(bird) {
  switch (bird.type) {
    case 'EuropeanSwallow': return new EuropeanSwallow(bird);
    case 'AfricanSwallow': return new AfricanSwallow(bird);
    case 'NorwegianBlueParrot': return new NorwegianBlueParrot(bird);
    default: return new Bird(bird);
  }
}

class EuropeanSwallow extends Bird {
  get plumage() { return "average"; }
}
class AfricanSwallow extends Bird {
  get plumage() { return (this.numberOfCoconuts > 2) ? "tired" : "average"; }
}
class NorwegianBlueParrot extends Bird {
  get plumage() { return (this.voltage > 100) ? "scorched" : "beautiful"; }
}
```

### Introducing Special Case

[DON'T] Repeatedly check for a specific value and execute duplicate fallback logic.
```javascript
const aCustomer = site.customer;
let customerName;
if (aCustomer === "unknown") customerName = "occupant";
else customerName = aCustomer.name;

const plan = (aCustomer === "unknown") ? registry.billingPlans.basic : aCustomer.billingPlan;
```

[DO] Create a Special Case object that inherently returns the fallback logic.
```javascript
// In Site class
get customer() {
  return (this._customer === "unknown") ? new UnknownCustomer() : this._customer;
}

// Special Case Class
class UnknownCustomer {
  get isUnknown() { return true; }
  get name() { return "occupant"; }
  get billingPlan() { return registry.billingPlans.basic; }
}

// Client usage completely removes the conditional
const customerName = aCustomer.name;
const plan = aCustomer.billingPlan;
```

### Introducing Assertions

[DON'T] Leave necessary preconditions unstated and implicit.
```javascript
applyDiscount(aNumber) {
  return (this.discountRate) ? aNumber - (this.discountRate * aNumber) : aNumber;
}
```

[DO] Use assertions to explicitly state assumptions that represent programmer errors if violated.
```javascript
applyDiscount(aNumber) {
  if (!this.discountRate) return aNumber;
  else {
    assert(this.discountRate >= 0); // Explicit assumption
    return aNumber - (this.discountRate * aNumber);
  }
}
```