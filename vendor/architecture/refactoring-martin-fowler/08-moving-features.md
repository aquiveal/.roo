# @Domain
These rules MUST be triggered when the AI is tasked with restructuring code layout, moving functions or fields between classes/modules, consolidating duplicated execution logic, reordering statements for clarity, converting iterative loops to collection pipelines, or cleaning up unused/deprecated code.

# @Vocabulary
- **Context:** The environment in which a function or field resides, typically a class, module, or nested function scope.
- **Delegating Function:** A function left behind in the original context after a move, whose sole purpose is to call the newly moved function in its new context.
- **Encapsulated Field:** A data field that is accessed exclusively through getter and setter functions.
- **Side Effect:** Any observable state mutation that occurs outside of a function's local scope.
- **Collection Pipeline:** A sequence of operations (e.g., `map`, `filter`, `reduce`) that consume and emit collections in a declarative style.
- **Dead Code:** Code that is no longer executed, referenced, or needed by the application.
- **Interference:** When sliding statements, a condition where moving one code fragment over another alters the observable behavior (e.g., sliding over a state modification that the fragment relies on).

# @Objectives
- **Enhance Modularity:** Group related software elements together by ensuring functions and data reside in the context where they are most heavily utilized.
- **Eliminate Duplication:** Combine repetitive statements into functions and replace duplicate inline logic with existing function calls.
- **Improve Readability:** Declare variables and related statements as close as possible to their point of use.
- **Isolate Responsibilities:** Split multi-purpose loops so that each loop performs exactly one calculation or task.
- **Promote Declarative Styles:** Prefer collection pipelines over procedural loops for data transformation.
- **Maintain Codebase Hygiene:** Aggressively delete unused code to reduce cognitive load on future developers.

# @Guidelines

### Move Function & Move Field
- The AI MUST evaluate the dependencies of a function before moving it. If a function references elements in another context more than its own, it MUST be moved to that context.
- When moving a cluster of functions, the AI MUST start with the lowest-level sub-functions (those with the fewest dependencies on the group).
- The AI MUST check if a function is a polymorphic method before moving it. Inheritance and overrides MUST be accommodated.
- The AI MUST encapsulate fields (create getters/setters) BEFORE moving them to a different context.
- When moving a field to a shared target object, the AI MUST update the setter to modify both source and target fields temporarily, use assertions to verify consistency, and only then switch reads to the target.

### Moving Statements (Into Functions or To Callers)
- If the exact same code executes immediately before or after a function call across all callers, the AI MUST use `Move Statements into Function` to absorb that logic into the function.
- If a function performs common behavior but needs to vary slightly across different callers, the AI MUST use `Move Statements to Callers` to push the varying logic out to the calling scope.
- When shifting statements across multiple callers, the AI MUST use a temporary extracted function to isolate the code, convert all callers to use the temporary function, and then inline the original function.

### Replacing Inline Code with Function Call
- The AI MUST replace inline code with a function call if an existing function performs the exact same logic.
- EXCEPT: The AI MUST NOT replace inline code if the structural similarity is purely coincidental and the *semantic intent* of the existing function does not match the inline code's context.

### Slide Statements
- The AI MUST slide related statements together (e.g., sliding variable declarations immediately prior to their first use).
- The AI MUST abort a slide if any **Interference** is detected:
  1. Cannot slide backward before a referenced element is declared.
  2. Cannot slide forward beyond an element that references the sliding fragment.
  3. Cannot slide over any statement that modifies an element the sliding fragment references.
  4. Cannot slide a fragment that modifies an element over any other statement that references that modified element.
- The AI MUST assume functions with return values are side-effect-free (Command-Query Separation) unless analysis proves otherwise.

### Split Loop & Replace Loop with Pipeline
- If a loop performs two or more distinct calculations, the AI MUST split it into multiple loops.
- The AI MUST NOT let performance anxiety prevent splitting a loop. Split for clarity first; optimize later if a true bottleneck is proven.
- The AI MUST transform loops that iterate over collections into Collection Pipelines (e.g., using `slice`, `filter`, `map`, `reduce`).
- The AI MUST remove loop control variables (e.g., `firstLine` flags) when converting to pipelines.

### Remove Dead Code
- The AI MUST delete unused code entirely.
- The AI MUST NOT comment out dead code. Version control exists to recover lost code; commented-out code only adds visual clutter.

# @Workflow
When tasked with moving features or restructuring execution flow, the AI MUST follow this step-by-step algorithmic process:

1. **Dependency Analysis:**
   - Map all variables, fields, and sub-functions referenced by the target code.
   - Determine the ideal target context based on highest coupling.
2. **Preparation:**
   - Use `Slide Statements` to group related logic together.
   - Encapsulate data fields if they are about to be moved.
   - Extract sub-functions if they need to travel with a moving parent function.
3. **Execution (The Move):**
   - Copy the target element to the new context.
   - Adjust parameters (pass source context or specific variables as needed).
   - If moving a function with many callers, leave a Delegating Function in the original context temporarily.
4. **Verification & Migration:**
   - Update all callers/references one by one.
   - If splitting a loop, duplicate the loop entirely, then remove the irrelevant side effects from each copy.
5. **Cleanup:**
   - Inline the temporary Delegating Function if it provides no architectural value.
   - Rename functions/fields to fit naturally within their new context.
   - Run `Remove Dead Code` to delete obsolete functions, variables, or original classes.

# @Examples (Do's and Don'ts)

### Slide Statements
- **[DO]** Declare variables right before they are used to improve locality.
  ```javascript
  // DO
  const baseCharge = pricingPlan.base;
  const chargePerUnit = pricingPlan.unit;
  let charge = baseCharge + units * chargePerUnit;
  ```
- **[DON'T]** Declare all variables at the top of a function out of habit, or slide a statement past a state modification.
  ```javascript
  // DON'T
  let charge; // Declared far from use
  const baseCharge = pricingPlan.base;
  charge = baseCharge + units * chargePerUnit;
  ```

### Split Loop
- **[DO]** Split a loop so it calculates exactly one outcome, making it trivial to extract into a dedicated function.
  ```javascript
  // DO
  let totalSalary = 0;
  for (const p of people) { totalSalary += p.salary; }

  let youngest = people[0] ? people[0].age : Infinity;
  for (const p of people) { if (p.age < youngest) youngest = p.age; }
  ```
- **[DON'T]** Calculate multiple unrelated aggregations in a single loop just to save iteration cycles.
  ```javascript
  // DON'T
  let youngest = people[0] ? people[0].age : Infinity;
  let totalSalary = 0;
  for (const p of people) {
    if (p.age < youngest) youngest = p.age;
    totalSalary += p.salary;
  }
  ```

### Replace Loop with Pipeline
- **[DO]** Use declarative collection pipelines to express data transformations.
  ```javascript
  // DO
  function acquireData(input) {
    const lines = input.split("\n");
    return lines
      .slice(1)
      .filter(line => line.trim() !== "")
      .map(line => line.split(","))
      .filter(fields => fields[1].trim() === "India")
      .map(fields => ({city: fields[0].trim(), phone: fields[2].trim()}));
  }
  ```
- **[DON'T]** Use manual `for` loops with control flags and internal `if/continue` logic for array manipulation.
  ```javascript
  // DON'T
  function acquireData(input) {
    const lines = input.split("\n");
    let firstLine = true;
    const result = [];
    for (const line of lines) {
      if (firstLine) { firstLine = false; continue; }
      if (line.trim() === "") continue;
      const record = line.split(",");
      if (record[1].trim() === "India") {
        result.push({city: record[0].trim(), phone: record[2].trim()});
      }
    }
    return result;
  }
  ```

### Remove Dead Code
- **[DO]** Delete unused code blocks entirely.
  ```javascript
  // DO
  function calculateTotal() {
    return price * quantity;
  }
  ```
- **[DON'T]** Leave commented-out logic "just in case we need it later."
  ```javascript
  // DON'T
  function calculateTotal() {
    // const discount = calculateDiscount(); // wait for Q3 feature
    // return (price * quantity) - discount;
    return price * quantity;
  }
  ```