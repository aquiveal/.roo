@Domain
Code refactoring, readability enhancements, modularization, variable scope management, API modification, and logic decomposition tasks. These rules activate whenever the user requests code cleanup, function extraction, variable renaming, or structural improvements to existing logic.

@Vocabulary
- **Refactoring:** A change made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior.
- **Intent vs. Implementation:** The conceptual separation between *what* a block of code is trying to achieve (Intent) and *how* it mechanically achieves it (Implementation). 
- **Data Clump:** A set of variables or parameters that frequently travel together throughout the codebase (e.g., `startDate` and `endDate`).
- **Parameter Object:** A class or data structure created specifically to group a Data Clump into a single logical unit.
- **Transform Function:** A function that takes source data, performs a deep copy, and enriches it with derived/calculated fields, useful for read-only data pipelines.
- **Intermediate Data Structure:** A specific object bridging two distinct processing phases, carrying only the data the second phase needs from the first phase.
- **Migration Mechanics:** A safe, incremental procedure for changing function signatures by extracting a new function, deprecating the old one, and gradually migrating callers.
- **Overloaded Getter Setter:** An anti-pattern where a single function acts as both getter and setter depending on the presence of an argument.

@Objectives
- Maximize code readability by ensuring names explicitly reveal intent.
- Decompose long functions into small, highly cohesive, single-purpose functions.
- Eliminate unnecessary indirection by inlining functions or variables that add no semantic value.
- Group cohesive data and the functions that operate on them into explicit classes or transform pipelines.
- Minimize the scope of mutable state by strictly encapsulating widely used variables.
- Split multi-stage algorithms into explicit, sequentially executing phases communicating via intermediate data structures.

@Guidelines
- **Extract Function:** The AI MUST extract fragments of code that require effort to understand (or require a comment to explain) into separate functions. The new function MUST be named by its *intent* (what it does), regardless of how short the extracted code is (even a single line).
- **Variable Handling in Extraction:** When extracting functions, the AI MUST pass locally scoped variables as parameters. If an extracted variable is modified and used outside the extracted function, the AI MUST return the modified value.
- **Inline Function/Variable:** The AI MUST inline functions or variables if their body/expression is as clear as their name, or if they act as needless indirection. 
- **Extract Variable:** The AI MUST extract complex, hard-to-read expressions into intermediate variables named after their logical purpose. The AI MUST declare these variables as immutable (e.g., `const` in JS) whenever possible.
- **Change Function Declaration:** When renaming a function or modifying its parameters, if the function is highly coupled or a published API, the AI MUST use "Migration Mechanics": extract the body into the new function, turn the old function into a delegating wrapper, test, update callers incrementally, and finally remove the old function.
- **Encapsulate Variable:** The AI MUST encapsulate mutable data with a scope wider than a single function behind getter and setter functions. The AI MUST strictly avoid the "Overloaded Getter Setter" pattern; getters and setters MUST be distinct functions. To prevent deep mutations, the AI SHOULD return a copy (e.g., deep copy) or a read-only proxy of the data from the getter.
- **Introduce Parameter Object:** When the AI detects a Data Clump (e.g., `min`/`max`, `start`/`end`), it MUST group them into a single Parameter Object (preferably a Value Object class) and update function signatures to accept this new object.
- **Combine Functions into Class:** When multiple functions operate closely on a common body of data (passed as arguments), the AI MUST encapsulate the data into a class and move the functions into that class as methods.
- **Combine Functions into Transform:** If the source data is NOT mutated, the AI MAY group derivation logic into a Transform Function that deep-copies the input and appends derived fields. If the source data IS mutated elsewhere, the AI MUST NOT use a Transform Function and MUST use a Class instead to prevent data inconsistency.
- **Split Phase:** When code deals with two distinct, sequential topics (e.g., parsing input, then executing logic), the AI MUST split the code into two phases. The AI MUST create an Intermediate Data Structure populated by the first phase and consumed by the second phase.

@Workflow
1. **Assessment:** Analyze the target code for smells: long functions, inline comments explaining logic, data clumps, or multi-phase operations entangled in one block.
2. **Scoping & Variable Analysis:** Before extracting or moving code, trace the exact scope and mutability of every variable involved.
3. **Application of Mechanics:**
   - *For Extractions:* Identify inputs (used but not modified), outputs (modified and used later), and local-only variables. Pass inputs as parameters, return outputs.
   - *For Signature Changes:* Use simple replacement for local/private code. Use Migration Mechanics (create new, delegate old, migrate, delete old) for shared/public code.
   - *For Grouping:* Identify common data arguments. Choose between Class (if mutable) or Transform (if immutable). Move functions into the chosen structure.
   - *For Phasing:* Extract the second phase first, feed it mock/temporary parameters, build the intermediate data object, then extract the first phase to populate that object.
4. **Cleanup:** Apply `Inline Variable` or `Remove Dead Code` to clean up leftover temporary variables or deprecated delegating functions. Rename temporary transition functions to their final names.

@Examples (Do's and Don'ts)

**Principle: Extract Function (Separating Intent from Implementation)**
- [DON'T]
```javascript
function printOwing(invoice) {
  let outstanding = 0;
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
  for (const o of invoice.orders) {
    outstanding += o.amount;
  }
  // record due date
  const today = Clock.today;
  invoice.dueDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 30);
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```
- [DO]
```javascript
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  recordDueDate(invoice);
  printDetails(invoice, outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding(invoice) {
  let result = 0;
  for (const o of invoice.orders) {
    result += o.amount;
  }
  return result;
}

function recordDueDate(invoice) {
  const today = Clock.today;
  invoice.dueDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 30);
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

**Principle: Introduce Parameter Object**
- [DON'T]
```javascript
function readingsOutsideRange(station, min, max) {
  return station.readings.filter(r => r.temp < min || r.temp > max);
}
// Caller
alerts = readingsOutsideRange(station, operatingPlan.temperatureFloor, operatingPlan.temperatureCeiling);
```
- [DO]
```javascript
class NumberRange {
  constructor(min, max) {
    this._data = {min: min, max: max};
  }
  get min() {return this._data.min;}
  get max() {return this._data.max;}
  contains(arg) {return (arg >= this.min && arg <= this.max);}
}

function readingsOutsideRange(station, range) {
  return station.readings.filter(r => !range.contains(r.temp));
}
// Caller
const range = new NumberRange(operatingPlan.temperatureFloor, operatingPlan.temperatureCeiling);
alerts = readingsOutsideRange(station, range);
```

**Principle: Split Phase**
- [DON'T]
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0) * product.basePrice * product.discountRate;
  const shippingPerCase = (basePrice > shippingMethod.discountThreshold) ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = quantity * shippingPerCase;
  const price = basePrice - discount + shippingCost;
  return price;
}
```
- [DO]
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const priceData = calculatePricingData(product, quantity);
  return applyShipping(priceData, shippingMethod);
}

function calculatePricingData(product, quantity) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0) * product.basePrice * product.discountRate;
  return {basePrice: basePrice, quantity: quantity, discount: discount};
}

function applyShipping(priceData, shippingMethod) {
  const shippingPerCase = (priceData.basePrice > shippingMethod.discountThreshold) ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = priceData.quantity * shippingPerCase;
  return priceData.basePrice - priceData.discount + shippingCost;
}
```

**Principle: Encapsulate Variable (Preventing hidden mutation of globals/shared data)**
- [DON'T]
```javascript
export let defaultOwner = {firstName: "Martin", lastName: "Fowler"};
// Caller
defaultOwner.lastName = "Parsons"; // Hidden mutation
```
- [DO]
```javascript
let defaultOwnerData = {firstName: "Martin", lastName: "Fowler"};

export function defaultOwner() {
  return Object.assign({}, defaultOwnerData); // Return a copy to prevent mutation
}
export function setDefaultOwner(arg) {
  defaultOwnerData = arg;
}
```

**Principle: Extract Variable**
- [DON'T]
```javascript
function price(order) {
  return order.quantity * order.itemPrice -
    Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
    Math.min(order.quantity * order.itemPrice * 0.1, 100);
}
```
- [DO]
```javascript
function price(order) {
  const basePrice = order.quantity * order.itemPrice;
  const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
  const shipping = Math.min(basePrice * 0.1, 100);
  return basePrice - quantityDiscount + shipping;
}
```