# @Domain
These rules MUST trigger when the AI is tasked with refactoring code, improving code readability, reducing code duplication, cleaning up poorly named elements, organizing data structures, restructuring function signatures, or modularizing existing logic. They specifically apply when the AI detects long functions, complex expressions, data clumps, repetitive calculations, or tangled logic lacking clear phases.

# @Vocabulary
- **Extract Function**: The process of taking a fragment of code that requires effort to understand and moving it into its own function, named after its intent.
- **Inline Function**: The process of replacing a function call with its body when the body is as clear as the name, or to remove needless indirection.
- **Extract Variable**: The process of assigning a complex expression (or part of it) to a local, well-named, immutable variable to clarify its purpose.
- **Inline Variable**: The process of removing a variable that does not communicate more than its assigned expression and replacing its references with the expression itself.
- **Change Function Declaration**: The process of changing a function's name or its parameters to better reflect its purpose and context.
- **Simple Mechanics**: A refactoring approach where the declaration and all callers are changed in a single step (best for small scope or automated tools).
- **Migration Mechanics**: A refactoring approach for wide-scope APIs where a new function is extracted, the old function is deprecated/forwarded to the new one, callers are migrated gradually, and the old function is eventually inlined/removed.
- **Encapsulate Variable**: The process of routing all access to widely used mutable data through explicit getter and setter functions.
- **Introduce Parameter Object**: The process of grouping data items that frequently travel together (data clumps) into a single object or record.
- **Combine Functions into Class**: The process of grouping a set of functions that operate closely together on a common body of data into a class.
- **Combine Functions into Transform**: The process of grouping related data derivations into a single pipeline/transformation function that reads source data and emits an enriched data record.
- **Split Phase**: The process of dividing logic that does two distinct things into sequential phases, passing an intermediate data structure between them.

# @Objectives
- **Separate Intent from Implementation**: Code MUST clearly state *what* it is doing via names, hiding the *how* in the implementation details.
- **Enhance Readability**: The AI MUST optimize code for human comprehension by ensuring function and variable names are highly descriptive.
- **Minimize Scope of Mutability**: The AI MUST encapsulate mutable data to control access and prevent hidden side effects.
- **Modularize Execution**: The AI MUST break down tangled logic into distinct, sequential phases or distinct classes/transforms.
- **Preserve Observable Behavior**: The AI MUST take small, verifiable steps, ensuring no functionality is broken during the restructuring.

# @Guidelines

## Function Restructuring
- **Extract Function**: When encountering a code fragment that requires effort to understand, the AI MUST extract it into a separate function. The function MUST be named based on its *intent* (what it does), regardless of how short the implementation is (even a single line).
- **Inline Function**: If a function's body is as clear as its name, or if it represents needless indirection, the AI MUST replace the function calls with the body and delete the function. The AI MUST NOT inline polymorphic methods.
- **Change Function Declaration**: The AI MUST rename functions if their current name does not clearly communicate their intent. 
  - If the function scope is local/private, use **Simple Mechanics**.
  - If the function is a published API or widely used, the AI MUST use **Migration Mechanics**.

## Variable and Data Organization
- **Extract Variable**: When encountering complex expressions, the AI MUST extract parts of the expression into immutable local variables (e.g., `const` in JS) named after their purpose.
- **Inline Variable**: The AI MUST inline temporary variables that do not add explanatory value beyond the expression they hold.
- **Encapsulate Variable**: When moving or interacting with data that has a wider scope than a single function, the AI MUST route all access through getter and setter functions. To prevent unintended modifications, getters MUST return a deep copy or read-only proxy of the mutable data.
- **Rename Variable**: The AI MUST ensure variables have clear names. If a variable with a wide scope needs renaming, the AI MUST encapsulate it first before changing the internal name.

## Grouping and Modularity
- **Introduce Parameter Object**: When the AI detects a "data clump" (a group of variables repeatedly passed together as function parameters), it MUST group them into a single data structure or class.
- **Combine Functions into Class**: When multiple functions operate on the same common body of data, the AI MUST encapsulate the data and functions into a single class, converting passed parameters into instance data where applicable.
- **Combine Functions into Transform**: When source data is read and multiple derived values are calculated from it across different functions, the AI MUST group these derivations into a single transform function that returns an "enriched" copy of the source data. The AI MUST NOT use this pattern if the source data is mutable within the context; use a Class instead.
- **Split Phase**: When a function performs two distinct sequential operations (e.g., calculating pricing data, then formatting it for rendering), the AI MUST divide the behavior into two separate functions and pass an explicit **intermediate data structure** from the first phase to the second.

# @Workflow
1. **Analyze Dependencies**: Before applying any extraction or inline operation, the AI MUST analyze variable scope. Identify variables that will be out of scope and pass them as parameters.
2. **Take Small Steps**: Refactoring MUST be done in minimal increments.
3. **Encapsulate First**: If modifying widely accessed data or records, apply Encapsulate Variable or Encapsulate Record before manipulating the logic.
4. **Extract and Name**: Apply Extract Function or Extract Variable, assigning temporary searchable names if the final name conflicts with existing scope.
5. **Route/Forward**: Route old calls to the new structure (e.g., in Migration Mechanics, make the old function call the newly extracted function).
6. **Migrate Callers**: Update callers one by one to point to the new structure.
7. **Clean Up**: Apply Inline Function on deprecated wrappers and Remove Dead Code on unused variables or parameters.

# @Examples (Do's and Don'ts)

## Extract Function
- **[DO]** Extract logic into a well-named function to separate intent from implementation.
```javascript
// Before
function printOwing(invoice) {
  let outstanding = 0;
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
  
  for (const o of invoice.orders) {
    outstanding += o.amount;
  }
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}

// After
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
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

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```
- **[DON'T]** Leave complex loops and logging clumped together in a single function, or use Extract Function without passing required out-of-scope variables properly.

## Change Function Declaration (Migration Mechanics)
- **[DO]** Use migration mechanics for widely used functions to ensure a safe transition.
```javascript
// Before
function circum(radius) {
  return 2 * Math.PI * radius;
}

// After (Migration Step 1: Extract and Forward)
function circum(radius) {
  return circumference(radius); // old function routes to new
}
function circumference(radius) {
  return 2 * Math.PI * radius;
}
// After (Migration Step 2: Update callers, then delete 'circum')
```
- **[DON'T]** Change the signature of a widely used, published API directly without providing a forwarding function during the transition.

## Split Phase
- **[DO]** Split logic into sequential phases using an intermediate data structure.
```javascript
// Before
function priceOrder(product, quantity, shippingMethod) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0) * product.basePrice * product.discountRate;
  const shippingPerCase = (basePrice > shippingMethod.discountThreshold) ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = quantity * shippingPerCase;
  return basePrice - discount + shippingCost;
}

// After
function priceOrder(product, quantity, shippingMethod) {
  const priceData = calculatePricingData(product, quantity);
  return applyShipping(priceData, shippingMethod);
}

function calculatePricingData(product, quantity) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0) * product.basePrice * product.discountRate;
  return { basePrice, quantity, discount }; // Intermediate Data Structure
}

function applyShipping(priceData, shippingMethod) {
  const shippingPerCase = (priceData.basePrice > shippingMethod.discountThreshold) ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = priceData.quantity * shippingPerCase;
  return priceData.basePrice - priceData.discount + shippingCost;
}
```
- **[DON'T]** Intertwine product parsing logic and shipping logic in the same processing block if they can be distinctly separated.

## Combine Functions into Transform
- **[DO]** Use an `enrich` function to centralize calculations for read-only data.
```javascript
// Before
const baseCharge = baseRate(reading.month, reading.year) * reading.quantity;
const taxableCharge = Math.max(0, baseCharge - taxThreshold(reading.year));

// After
function enrichReading(original) {
  const result = _.cloneDeep(original);
  result.baseCharge = calculateBaseCharge(result);
  result.taxableCharge = Math.max(0, result.baseCharge - taxThreshold(result.year));
  return result;
}
// Callers now use the enriched record instead of repeating derivations.
```
- **[DON'T]** Use transformation pipelines if the source data is highly mutable and modified elsewhere in the application, which leads to inconsistent state (use a Class instead).