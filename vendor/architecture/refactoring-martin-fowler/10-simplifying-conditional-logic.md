@Domain
These rules activate when the AI is tasked with refactoring, analyzing, or writing code that involves conditional logic, control flow operations (`if`/`else`, `switch`), repeated checks for specific values (e.g., `null` or `"unknown"`), deeply nested branching, or implicit state assumptions.

@Vocabulary
- **Decompose Conditional**: The process of extracting the condition, the `then` branch, and the `else` branch of a conditional statement into distinct, well-named functions.
- **Guard Clause**: An early `return` or `throw` statement used to handle unusual, edge, or error cases immediately, exiting the function and preventing deep nesting of the "happy path" logic.
- **Polymorphism**: In this context, utilizing class hierarchies (or object implementations) and overriding methods to handle type-specific or variant-specific logic, removing the need for `switch` or `if/else` chains based on type codes.
- **Special Case Object (Null Object)**: An object or frozen literal that encapsulates the default or common behavior for a specific edge-case value (e.g., an `UnknownCustomer` object replacing the string `"unknown"` or `null`), eliminating repeated value checks across the codebase.
- **Assertion**: A conditional statement assumed to always be true, used to make programmer assumptions explicit. Failure indicates a programmer error, not an anticipated runtime exception.
- **Type-Instance Homonym**: A modeling error where a class representing a type or catalog item is mistakenly inherited by an instance of that item (e.g., `Scroll` inheriting from `CatalogItem`).

@Objectives
- The AI MUST prioritize intention over implementation by extracting complex conditional logic into clearly named functions.
- The AI MUST eliminate nested conditional logic for edge cases by utilizing early-return Guard Clauses.
- The AI MUST consolidate identical conditional actions into single expressions using logical `AND` and `OR` operators.
- The AI MUST replace widespread type-checking or state-checking conditionals with Polymorphism or Special Case Objects.
- The AI MUST use Assertions strictly to communicate and enforce programmer assumptions, never for external data validation.

@Guidelines

**1. Decomposing Conditionals**
- When encountering complex conditional logic, the AI MUST `Extract Function` on the `if` condition, the `then` leg, and the `else` leg.
- The extracted functions MUST be named based on their intention (why they happen), not their implementation (how they work).
- After decomposing, the AI SHOULD format the conditional using a ternary operator (`condition() ? thenAction() : elseAction()`) if applicable.

**2. Consolidating Conditional Expressions**
- When encountering a sequence of conditional checks that result in the exact same action, the AI MUST consolidate them into a single condition using logical `OR` (`||`) or `AND` (`&&`) operators.
- After consolidating, the AI MUST extract the combined condition into a well-named function.
- **Constraint**: The AI MUST NOT consolidate conditionals if the checks represent truly independent concepts that should not be conceptually merged.
- **Constraint**: The AI MUST ensure no consolidated conditionals have side effects. If they do, the AI MUST separate the query from the modifier first.

**3. Replacing Nested Conditionals with Guard Clauses**
- The AI MUST NOT strictly adhere to the "one exit point per function" rule. Clarity supersedes this rule.
- When conditional legs do not carry equal weight (one is the "happy path" and others are edge cases), the AI MUST use Guard Clauses to handle the edge cases and return early.
- The AI MUST safely remove mutable accumulator variables (e.g., `let result;`) if their only purpose is to hold a return value deferred to the end of the function.
- The AI MUST frequently reverse conditional expressions (e.g., `if (x > 0)` becomes `if (x <= 0) return;`) to implement Guard Clauses effectively.

**4. Replacing Conditionals with Polymorphism**
- When encountering complex conditional logic (e.g., `switch` statements) that branches based on type codes or variant states, the AI MUST introduce subclasses or strategy objects for each variant.
- The AI MUST establish a base case (via a superclass) and implement variants as subclasses that override the base behavior.
- The AI MUST utilize a factory function to instantiate the correct polymorphic object.
- **Constraint**: The AI MUST NOT replace *all* conditionals with polymorphism. It MUST only be used when conditional logic is complex, duplicated, or organized around explicit types/variants.
- **Warning**: A function name containing "And" (e.g., `voyageAndHistoryLengthFactor`) is a bad smell indicating multiple responsibilities. The AI MUST extract these into separate functions before applying polymorphism.

**5. Introducing Special Cases (Null Objects)**
- When multiple parts of the codebase check a variable for a specific value (e.g., `"unknown"` or `null`) and perform the same fallback behavior, the AI MUST introduce a Special Case Object or literal.
- The AI MUST create an `isUnknown` (or similar) property/method on both the standard object (returning `false`) and the Special Case object (returning `true`).
- The Special Case Object MUST implement the common fallback behavior (e.g., returning `"occupant"` for a name).
- **Constraint**: Special Case Objects MUST behave as Value Objects and MUST be immutable. If using object literals, the AI MUST freeze them or ensure they cannot be mutated.
- **Constraint**: If a Special Case Object must return a related object, the returned object MUST ALSO be a Special Case Object (e.g., an `UnknownCustomer` returning a `NullPaymentHistory`).

**6. Introducing Assertions**
- When a block of code strictly assumes a certain state to function (e.g., a divisor is not zero, an object property is populated), the AI MUST explicitly state this assumption using an Assertion.
- **Constraint**: Assertions MUST ONLY be used to catch programmer errors. The AI MUST NOT use assertions to validate external input data or user input.
- **Constraint**: The code MUST function identically if all assertions are stripped away. Do not place execution logic inside an assertion statement.
- **Constraint**: Do not overuse assertions. Only assert conditions that *must* be true for the code to run correctly, not everything that *might* be true.

@Workflow
When tasked with simplifying conditional logic, the AI MUST follow this algorithmic process:

1. **Analysis Phase**:
   - Identify all `if/else` chains, `switch` statements, and repeated value checks.
   - Determine the semantic intent of the conditionals: Are they independent checks? Are they edge cases? Are they type-dispatchers?

2. **Consolidation & Extraction Phase**:
   - Combine conditionals that yield the exact same result into a single extracted function.
   - Decompose complex `if/then/else` blocks into three separate intention-revealing functions.

3. **Guard Clause Phase**:
   - Identify the "happy path" of the function.
   - Invert conditions if necessary to catch edge cases early.
   - Replace nested `else` blocks with early `return` or `throw` statements.
   - Remove unnecessary mutable variables used merely to track the return state.

4. **Polymorphism & Special Case Phase**:
   - If a `switch` statement is dispatching based on a type code, generate a factory function and subclass hierarchy. Move the specific logic into the overridden methods of the subclasses.
   - If a variable is repeatedly checked for a null or unknown state, extract the check into a function, create a Special Case Object, populate it with the default responses, and route the code to utilize the object polymorphically.

5. **Assertion Phase**:
   - Identify implicit requirements for variables (e.g., `rate >= 0`).
   - Add explicit assertions to document and enforce these programmer assumptions.

@Examples (Do's and Don'ts)

**Decomposing Conditionals**
- [DON'T] Leave complex logic embedded in the conditional structural:
  ```javascript
  if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
    charge = quantity * plan.summerRate;
  } else {
    charge = quantity * plan.regularRate + plan.regularServiceCharge;
  }
  ```
- [DO] Extract into intentionally named functions and use ternary operators:
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

**Consolidating Conditional Expressions**
- [DON'T] Repeat identical return states for conceptually related checks:
  ```javascript
  if (anEmployee.seniority < 2) return 0;
  if (anEmployee.monthsDisabled > 12) return 0;
  if (anEmployee.isPartTime) return 0;
  ```
- [DO] Consolidate and extract into a named query:
  ```javascript
  if (isNotEligibleForDisability()) return 0;

  function isNotEligibleForDisability() {
    return ((anEmployee.seniority < 2) || (anEmployee.monthsDisabled > 12) || (anEmployee.isPartTime));
  }
  ```

**Replacing Nested Conditionals with Guard Clauses**
- [DON'T] Nest the "happy path" using `else` blocks and mutable return variables:
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
- [DO] Use early returns to guard against edge cases, keeping the happy path un-nested:
  ```javascript
  function payAmount(employee) {
    if (employee.isSeparated) return {amount: 0, reasonCode: "SEP"};
    if (employee.isRetired) return {amount: 0, reasonCode: "RET"};
    
    return someFinalComputation();
  }
  ```

**Replacing Conditionals with Polymorphism**
- [DON'T] Use `switch` statements scattered across multiple functions to check type codes:
  ```javascript
  function plumage(bird) {
    switch (bird.type) {
      case 'EuropeanSwallow': return "average";
      case 'AfricanSwallow': return (bird.numberOfCoconuts > 2) ? "tired" : "average";
      default: return "unknown";
    }
  }
  ```
- [DO] Create subclasses and override the methods:
  ```javascript
  class EuropeanSwallow extends Bird {
    get plumage() { return "average"; }
  }
  class AfricanSwallow extends Bird {
    get plumage() { return (this.numberOfCoconuts > 2) ? "tired" : "average"; }
  }
  ```

**Introducing Special Cases**
- [DON'T] Repeat value checks and fallback assignments throughout the codebase:
  ```javascript
  let customerName;
  if (customer === "unknown") customerName = "occupant";
  else customerName = customer.name;
  ```
- [DO] Create a Special Case Object with the default behavior encapsulated:
  ```javascript
  class UnknownCustomer {
    get isUnknown() { return true; }
    get name() { return "occupant"; }
  }
  
  // Usage naturally falls through
  const customerName = customer.name;
  ```

**Introducing Assertions**
- [DON'T] Hide critical assumptions implicitly in the math or logic:
  ```javascript
  applyDiscount(aNumber) {
    return (this.discountRate) ? aNumber - (this.discountRate * aNumber) : aNumber;
  }
  ```
- [DO] Make the assumption explicit with an assertion:
  ```javascript
  applyDiscount(aNumber) {
    if (!this.discountRate) return aNumber;
    assert(this.discountRate >= 0); // Fails fast if programmer error injects negative rate
    return aNumber - (this.discountRate * aNumber);
  }
  ```