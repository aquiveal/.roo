@Domain
This rule file is triggered when the AI is asked to restructure code contexts, group related program elements, relocate functions or fields across modules/classes, reorder statements within a function, replace imperative loops with declarative pipelines, or clean up unused code. It specifically applies to requests mentioning "moving code," "extracting logic," "cleaning up loops," "reorganizing variables," or "deleting dead code."

@Vocabulary
- **Move Function:** Relocating a function or method to a context (module or class) where it is used more frequently or fits more naturally.
- **Move Field:** Relocating a data structure or class field to a target that is intrinsically linked to that data.
- **Move Statements into Function:** Consolidating repetitive code found at the call sites of a function into the function body itself.
- **Move Statements to Callers:** Pushing behavior that varies among call sites out of a function and into the calling functions.
- **Slide Statements:** Reordering code fragments within a function to bring related lines of code (like variable declarations and their usage) adjacent to one another.
- **Replace Inline Code with Function Call:** Substituting duplicate inline logic with a call to an existing function that performs the exact same task.
- **Split Loop:** Breaking a single loop that performs multiple independent tasks into separate loops, one for each task.
- **Collection Pipeline:** A declarative sequence of collection operations (e.g., `map`, `filter`, `reduce`, `slice`) that replaces imperative loop iteration.
- **Dead Code:** Code that is no longer executed or referenced anywhere in the active codebase.
- **Command-Query Separation:** The principle that a function should either return a value without observable side effects (a query) or change state without returning a value (a command/modifier).

@Objectives
- Maximize modularity by ensuring that functions and data structures reside in the context where they are most relevant.
- Reduce cognitive load by separating distinct behaviors into discrete, single-purpose functions or loops.
- Clarify abstraction boundaries by migrating code in or out of functions until the function perfectly encapsulates a single, cohesive unit of behavior.
- Transition imperative, state-heavy iterations (loops) into declarative, side-effect-free data transformations (pipelines).
- Eliminate duplication at function call boundaries.
- Keep the codebase pristine by permanently deleting unused logic rather than commenting it out.

@Guidelines

### 1. Moving Functions
- When a function references elements in another context more than its own, the AI MUST use **Move Function** to relocate it.
- **Dependency Analysis:** Before moving a function, the AI MUST examine all program elements used by it. If helper functions or variables solely depend on the moving function, they MUST be moved alongside it.
- **Context Passing:** If the moving function relies on elements from its original context, the AI MUST pass those elements as parameters or pass a reference to the source context itself.
- **Delegation:** When moving a function with existing callers, the AI MUST temporarily turn the source function into a delegating function. If the original context no longer needs the delegating function, the AI MUST apply `Inline Function` to remove it.

### 2. Moving Fields
- The AI MUST use **Move Field** when pieces of data are frequently passed together or when a change in one record necessitates a change in a field of another record.
- **Encapsulation First:** Before moving a field, the AI MUST ensure the source field is fully encapsulated (using getter/setter methods).
- **Target Connection:** The AI MUST ensure a valid reference exists from the source object to the target object.
- **Shared Target Safety:** If moving a field to a shared target object (e.g., from an individual `Account` to a shared `AccountType`), the AI MUST use an assertion (`Introduce Assertion`) to ensure all source objects sharing the target previously had the identical value for the field before finalizing the move.

### 3. Moving Statements
- **Into Function:** If identical statements are executed immediately before or after every call to a function, the AI MUST move those statements into the function.
- **To Callers:** If a cohesive function begins to mix different behaviors based on the caller, the AI MUST move the varying statements out of the function and into the callers.
- **Coincidental Similarity Warning:** The AI MUST NOT replace inline code with a function call if the similarity between the inline code and the function is purely coincidental (i.e., they perform the same mechanics but serve conceptually different purposes).

### 4. Sliding Statements
- The AI MUST slide related statements together, especially moving variable declarations immediately prior to their first usage.
- **Interference Rules:** The AI MUST NOT slide statements if it violates any of the following interference constraints:
  1. A fragment CANNOT slide backward earlier than the declaration of any element it references.
  2. A fragment CANNOT slide forward beyond any element that references it.
  3. A fragment CANNOT slide over any statement that modifies an element it references.
  4. A fragment that modifies an element CANNOT slide over any statement that references the modified element.
- If interference prevents sliding, the AI MUST resolve it first (e.g., by using `Split Variable` to remove mutable state).

### 5. Loop Refactoring
- **Split Loop:** If a loop performs two or more distinct tasks, the AI MUST copy the loop and remove the irrelevant logic from each copy so that each loop performs exactly one task.
- **Ignore Performance Myths:** The AI MUST NOT avoid `Split Loop` due to concerns about iterating multiple times. Refactoring must prioritize clarity; optimization occurs separately.
- **Replace Loop with Pipeline:** The AI MUST convert loops that transform data into collection pipelines using operations like `slice()`, `filter()`, `map()`, and `reduce()`. 
- **Terminal Semicolons:** When writing pipelines, the AI SHOULD format the code logically, placing the terminal semicolon on its own line if the pipeline is long.

### 6. Dead Code
- The AI MUST permanently delete any unreachable, unreferenced, or unused code using **Remove Dead Code**.
- The AI MUST NOT comment out dead code. The AI MUST rely on version control for history retention.

@Workflow

### Moving Statements Across Function Boundaries (Safe Mechanics)
When moving statements into a function or to callers where multiple call sites exist, the AI MUST execute the following algorithm to avoid breaking the codebase:
1. **Isolate Code:** Use `Slide Statements` to get the target code adjacent to the function call.
2. **Extract:** Use `Extract Function` on the statements + the function call, giving it a highly visible, temporary name (e.g., `zz_tempFunction`).
3. **Convert Callers:** Update every original call site to use the temporary function.
4. **Inline:** Use `Inline Function` on the original function, moving its internal logic into the temporary function (or vice versa depending on direction).
5. **Rename:** Use `Change Function Declaration` to rename the temporary function to the final desired name.

### Replacing Loops with Pipelines
1. **Isolate Collection:** Create a new variable to represent the loop's target collection.
2. **Translate Logic Top-to-Bottom:** 
   - If skipping initial items, use `.slice()`.
   - If ignoring specific conditions (e.g., blank lines), use `.filter()`.
   - If transforming data, use `.map()`.
3. **Assign to Accumulator:** Assign the output of the final pipeline operation to the target accumulator.
4. **Clean up:** Delete the imperative loop.

@Examples (Do's and Don'ts)

### Sliding Statements
- **[DO]** Slide variable declarations down to where they are actually used.
```javascript
// DO:
const baseCharge = pricingPlan.base;
const units = order.units;
const chargePerUnit = pricingPlan.unit;
let charge = baseCharge + units * chargePerUnit;
```
- **[DON'T]** Slide statements over code that introduces side-effect interference.
```javascript
// DON'T: Sliding charge modification over code that references it
charge = charge - discount;
let discountableUnits = Math.max(units - pricingPlan.discountThreshold, 0); // INTERFERENCE
```

### Splitting Loops
- **[DO]** Split loops doing multiple independent calculations.
```javascript
// DO:
let totalSalary = 0;
for (const p of people) {
  totalSalary += p.salary;
}
let youngest = people[0] ? people[0].age : Infinity;
for (const p of people) {
  if (p.age < youngest) youngest = p.age;
}
```
- **[DON'T]** Keep unrelated accumulations in the same loop to "save iterations".
```javascript
// DON'T:
let youngest = people[0] ? people[0].age : Infinity;
let totalSalary = 0;
for (const p of people) {
  if (p.age < youngest) youngest = p.age;
  totalSalary += p.salary;
}
```

### Replacing Loops with Pipelines
- **[DO]** Use functional, declarative pipelines.
```javascript
// DO:
function acquireData(input) {
  const lines = input.split("\n");
  return lines
    .slice(1)
    .filter(line => line.trim() !== "")
    .map(line => line.split(","))
    .filter(fields => fields[1].trim() === "India")
    .map(fields => ({ city: fields[0].trim(), phone: fields[2].trim() }))
    ;
}
```
- **[DON'T]** Use highly nested imperative state-tracking loops for data transformation.
```javascript
// DON'T:
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

### Removing Dead Code
- **[DO]** Delete code entirely.
```javascript
// DO:
// (Code is simply removed from the file)
```
- **[DON'T]** Comment out unused methods.
```javascript
// DON'T:
/*
function calculateOldMetric() {
   // I might need this later...
   return x * y;
}
*/
```