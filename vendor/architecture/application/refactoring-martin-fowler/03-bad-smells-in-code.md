@Domain
These rules MUST be activated whenever the AI is tasked with reading, analyzing, reviewing, or refactoring existing source code. They are particularly mandatory when the user requests "code cleanup," "technical debt reduction," "improving readability," "code review," or explicit "refactoring."

@Vocabulary
*   **Code Smell**: A surface indication or structure in the code that suggests a deeper problem in system design, requiring refactoring.
*   **Divergent Change**: A smell occurring when a single module or class must be modified in different ways for different, unrelated reasons.
*   **Shotgun Surgery**: A smell occurring when a single functional change requires making lots of small edits across many different classes or modules.
*   **Feature Envy**: A smell where a function spends more time communicating with functions or data inside *another* module than its own.
*   **Data Clump**: Three or more data items (variables or fields) that frequently appear together in classes or parameter lists.
*   **Primitive Obsession**: The overuse of primitive data types (strings, integers) to represent domain concepts instead of using small, dedicated objects (e.g., using a string for a telephone number).
*   **Stringly Typed**: A negative consequence of primitive obsession where strings are used to represent types, states, or complex values.
*   **Message Chain**: A long sequence of method calls navigating through multiple objects (e.g., `client.getA().getB().getC()`).
*   **Middle Man**: A class whose interface consists almost entirely of delegating methods to another class, doing no real work itself.
*   **Data Class**: A class consisting only of fields and getter/setter methods, containing no business behavior.
*   **Refused Bequest**: A subclass that inherits methods and data from a parent class but does not want or use them, violating the intent of inheritance.

@Objectives
*   The AI MUST autonomously identify Code Smells in the provided code without waiting for user prompts.
*   The AI MUST apply the precise refactoring techniques associated with each Code Smell to improve internal code structure without altering external behavior.
*   The AI MUST prioritize code clarity, aiming for small, well-named functions that communicate *intention* rather than *implementation*.
*   The AI MUST ruthlessly eliminate duplication, unused code, and speculative structures.

@Guidelines
*   **Mysterious Name**: When encountering variables, functions, or classes with unclear names, the AI MUST use *Change Function Declaration*, *Rename Variable*, or *Rename Field* to clearly communicate what they do.
*   **Duplicated Code**: When the same code structure exists in multiple places, the AI MUST unify them using *Extract Function*, *Slide Statements* (to group similar items), or *Pull Up Method* (if in subclasses).
*   **Long Function**: When a function is long or requires comments to explain its parts, the AI MUST use *Extract Function* to decompose it. The AI MUST name the extracted functions by their intention, not how they work. To manage temps and parameters during extraction, the AI MUST use *Replace Temp with Query*, *Introduce Parameter Object*, or *Preserve Whole Object*.
*   **Long Parameter List**: When functions have long parameter lists, the AI MUST shorten them by using *Replace Parameter with Query* (if one parameter can be derived from another), *Preserve Whole Object*, *Introduce Parameter Object*, or *Combine Functions into Class*. The AI MUST remove boolean flag arguments using *Remove Flag Argument*.
*   **Global Data**: When data is accessible and mutable from anywhere, the AI MUST use *Encapsulate Variable* to wrap it in a function/class, limiting its scope as much as possible.
*   **Mutable Data**: When data changes frequently, risking unintended consequences, the AI MUST restrict updates using *Encapsulate Variable*, *Split Variable* (for variables storing different things), *Separate Query from Modifier*, and *Remove Setting Method*. If mutable data can be calculated, the AI MUST use *Replace Derived Variable with Query*.
*   **Divergent Change**: When a module changes for different contextual reasons (e.g., database vs. financial processing), the AI MUST split the module using *Split Phase*, *Move Function*, or *Extract Class*.
*   **Shotgun Surgery**: When a change requires edits across many modules, the AI MUST gather the changes into a single module using *Move Function*, *Move Field*, *Combine Functions into Class*, or *Inline Function/Class*.
*   **Feature Envy**: When a function relies heavily on data from another module, the AI MUST use *Move Function* to relocate it next to that data, optionally using *Extract Function* on the envious portion first.
*   **Data Clumps**: When groups of data travel together, the AI MUST group them into an object using *Extract Class*, *Introduce Parameter Object*, or *Preserve Whole Object*.
*   **Primitive Obsession**: When domain concepts are represented by primitives, the AI MUST wrap them using *Replace Primitive with Object*. For type codes controlling conditionals, the AI MUST use *Replace Type Code with Subclasses*.
*   **Repeated Switches**: When the same switch/case or if/else chain appears in multiple places, the AI MUST use *Replace Conditional with Polymorphism*.
*   **Loops**: When iterating over collections, the AI MUST replace loops with pipeline operations (e.g., `filter`, `map`) using *Replace Loop with Pipeline*.
*   **Lazy Element**: When a function or class does not do enough to justify its existence, the AI MUST eliminate it using *Inline Function*, *Inline Class*, or *Collapse Hierarchy*.
*   **Speculative Generality**: When code contains hooks, special cases, or unused parameters created for hypothetical future needs, the AI MUST remove them using *Collapse Hierarchy*, *Inline Function*, *Change Function Declaration*, or *Remove Dead Code*.
*   **Temporary Field**: When a class contains fields only used in certain circumstances, the AI MUST relocate them using *Extract Class* or handle them via *Introduce Special Case*.
*   **Message Chains**: When code navigates through a chain of objects, the AI MUST use *Hide Delegate* or *Extract Function* + *Move Function* to push the behavior down the chain.
*   **Middle Man**: When a class mostly delegates to another object, the AI MUST use *Remove Middle Man* to let the client call the delegate directly, or *Inline Function*.
*   **Insider Trading**: When modules are heavily coupled by trading data, the AI MUST separate them using *Move Function*, *Move Field*, or *Hide Delegate*.
*   **Large Class**: When a class has too many fields or code, the AI MUST split it using *Extract Class*, *Extract Superclass*, or *Replace Type Code with Subclasses*.
*   **Alternative Classes with Different Interfaces**: When different classes do the same thing but have different signatures, the AI MUST unify them using *Change Function Declaration* and *Move Function*.
*   **Data Class**: When a class only contains data and getters/setters, the AI MUST move the behavior that operates on that data into the class using *Move Function* or *Extract Function*, and hide public fields using *Encapsulate Record* and *Remove Setting Method*.
*   **Refused Bequest**: When a subclass does not want or support the interface of its superclass, the AI MUST sever the inheritance hierarchy using *Replace Subclass with Delegate* or *Replace Superclass with Delegate*.
*   **Comments**: When comments are used to explain bad code, the AI MUST view this as a smell. The AI MUST refactor the code (e.g., via *Extract Function* or *Rename Variable*) until the code is self-explanatory and the comment becomes superfluous.

@Workflow
1.  **Smell Detection**: Scan the provided code snippet or file explicitly searching for the 24 Code Smells defined in @Guidelines.
2.  **Target Selection**: Isolate the most disruptive smells first (e.g., Long Functions, Duplicated Code, Mutable Data).
3.  **Refactoring Application**: Apply the specific, named refactoring pattern corresponding to the identified smell.
4.  **Verification Check**: Ensure the refactoring did not alter the observable behavior of the code. Maintain the exact same inputs and outputs.
5.  **Deodorization**: Remove any comments that are no longer necessary because the code now clearly communicates its intent. Delete any dead code left behind by the extraction or inlining processes.

@Examples (Do's and Don'ts)

**Principle: Long Function & Comments (Deodorant)**
*   [DON'T] Keep a long function with a comment explaining what a block does.
```javascript
function printOwing(invoice) {
  let outstanding = 0;
  // print banner
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
  // calculate outstanding
  for (let o of invoice.orders) {
    outstanding += o.amount;
  }
  // ...
}
```
*   [DO] Extract the blocks into well-named functions that state their intent.
```javascript
function printOwing(invoice) {
  printBanner();
  let outstanding = calculateOutstanding(invoice);
  // ...
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding(invoice) {
  let result = 0;
  for (let o of invoice.orders) {
    result += o.amount;
  }
  return result;
}
```

**Principle: Primitive Obsession & Data Clumps**
*   [DON'T] Pass multiple related primitives independently.
```javascript
function readingsOutsideRange(station, min, max) {
  return station.readings.filter(r => r.temp < min || r.temp > max);
}
```
*   [DO] Combine them into an object (Introduce Parameter Object).
```javascript
class NumberRange {
  constructor(min, max) {
    this._data = {min: min, max: max};
  }
  get min() { return this._data.min; }
  get max() { return this._data.max; }
  contains(arg) { return (arg >= this.min && arg <= this.max); }
}

function readingsOutsideRange(station, range) {
  return station.readings.filter(r => !range.contains(r.temp));
}
```

**Principle: Loops**
*   [DON'T] Use traditional loops with accumulators to filter and transform data.
```javascript
const result = [];
for (const line of lines) {
  if (line.trim() === "") continue;
  const record = line.split(",");
  if (record[1].trim() === "India") {
    result.push({city: record[0].trim(), phone: record[2].trim()});
  }
}
return result;
```
*   [DO] Replace the loop with a collection pipeline.
```javascript
return lines
  .filter(line => line.trim() !== "")
  .map(line => line.split(","))
  .filter(fields => fields[1].trim() === "India")
  .map(fields => ({city: fields[0].trim(), phone: fields[2].trim()}));
```

**Principle: Repeated Switches**
*   [DON'T] Use switch statements on type codes.
```javascript
function plumage(bird) {
  switch (bird.type) {
    case 'EuropeanSwallow': return "average";
    case 'AfricanSwallow': return (bird.numberOfCoconuts > 2) ? "tired" : "average";
    default: return "unknown";
  }
}
```
*   [DO] Replace Conditional with Polymorphism.
```javascript
class Bird {
  get plumage() { return "unknown"; }
}
class EuropeanSwallow extends Bird {
  get plumage() { return "average"; }
}
class AfricanSwallow extends Bird {
  get plumage() { return (this.numberOfCoconuts > 2) ? "tired" : "average"; }
}
```