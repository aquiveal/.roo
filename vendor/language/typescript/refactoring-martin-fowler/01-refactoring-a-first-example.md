# @Domain
These rules are triggered when the AI is asked to edit, refactor, or extend existing code, especially when encountering long functions, tangled conditional logic, mixed data calculation and formatting, or when adding a new feature to an unstructured or legacy code base. 

# @Vocabulary
- **Refactoring**: Changing a software system to improve its internal structure and readability without altering its external, observable behavior.
- **Self-Checking Tests**: Automated tests that evaluate their own output and return a binary pass/fail (green/red) status without requiring human verification.
- **Extract Function**: The process of taking a cohesive block of code, moving it into its own function, and naming that function based on its intent rather than its implementation.
- **Replace Temp with Query**: Removing a temporary variable by extracting its calculation into a dedicated function and calling that function wherever the variable was used.
- **Inline Variable**: Removing a variable that is only assigned once by replacing references to it directly with its assigned expression.
- **Change Function Declaration**: Modifying a function's signature, specifically to remove parameters that the function can calculate itself to reduce dependency.
- **Split Loop**: Dividing a single loop that performs multiple distinct tasks into multiple identical loops that each perform exactly one task.
- **Slide Statements**: Moving a variable declaration closer to its first point of use to group related code together.
- **Split Phase**: Breaking a monolithic process into two distinct phases (e.g., data calculation and data formatting), usually communicating via an intermediate data structure.
- **Replace Conditional with Polymorphism**: Replacing `switch` or `if/else` statements that branch on a type code with a class hierarchy where each subclass overrides a method to provide its specific behavior.
- **Replace Constructor with Factory Function**: Using a standard function to instantiate objects so it can dynamically return the appropriate subclass based on type codes.
- **Camping Rule**: The development philosophy to "always leave the code base healthier than when you found it."

# @Objectives
- **Preparatory Refactoring**: The AI must restructure existing code to make a requested feature easy to add *before* actually adding the feature.
- **Micro-Steps**: The AI must apply structural changes in tiny, self-contained, and testable steps to minimize the chance of introducing bugs.
- **Human Readability**: The AI must prioritize code clarity for human readers over machine execution efficiency.
- **Scope Minimization**: The AI must aggressively eliminate local/temporary variables to reduce the cognitive load and simplify function extraction.
- **Structural Separation**: The AI must strictly separate data processing/calculation from presentation/formatting.
- **Polymorphic Design**: The AI must convert data-driven conditional branching into object-oriented subclass hierarchies.

# @Guidelines

- **Test Verification**: Before modifying structure, the AI MUST verify the existence of self-checking tests or prompt the user to ensure tests are in place. 
- **The "Make it Easy" Rule**: When asked to add a feature to messy code, the AI MUST first refactor the code to accommodate the feature, then add the feature.
- **Aggressive Extraction**: The AI MUST use *Extract Function* on any block of code that requires mental effort to understand. Functions should be named by their *intent* (what they do), not their implementation.
- **Variable Naming Standard**: 
  - The AI MUST name the return variable of any function `result`.
  - In dynamically typed languages, the AI MUST prefix parameter names with an indefinite article matching their type (e.g., `aPerformance`, `anInvoice`) unless a more specific role name is appropriate.
- **Eradicate Temps**: The AI MUST replace local temporary variables with function calls (*Replace Temp with Query*). This reduces local scope and makes subsequent function extraction significantly easier.
- **Parameter Minimization**: If a function can calculate a needed value from another parameter, the AI MUST NOT pass the calculated value as a parameter. It MUST calculate it inside the function (*Change Function Declaration*).
- **Single-Responsibility Loops**: If a loop accumulates two different values or performs two different tasks, the AI MUST duplicate the loop (*Split Loop*) so each loop does exactly one thing.
- **Proximity of Declaration**: The AI MUST move variable declarations to be immediately above their first use (*Slide Statements*).
- **Two-Phase Separation**: When code calculates data and formats a response (e.g., text, HTML), the AI MUST extract the calculation logic into a separate file/function that returns an intermediate data object. The formatting logic MUST accept only this intermediate data object as its parameter (*Split Phase*).
- **Polymorphism over Switches**: When the AI encounters a `switch` statement or chained `if/else` statements checking a `type` property, the AI MUST:
  1. Create a base class.
  2. Create a factory function to return the correct subclass based on the type code (*Replace Constructor with Factory Function*).
  3. Move the conditional logic into overridden methods on the subclasses (*Replace Conditional with Polymorphism*).
- **Ignore Performance During Refactoring**: The AI MUST NOT prematurely optimize for performance (e.g., combining loops to "save cycles") at the expense of structural clarity. Performance tuning occurs only after the code is well-factored.

# @Workflow
1. **Analyze and Isolate**: Review the target code. Identify switch statements, long functions, mixed calculation/formatting, and multi-purpose loops.
2. **Decompose Functions**: 
   - Extract logical chunks into nested or top-level functions.
   - Rename arguments to reflect types.
   - Rename return variables to `result`.
3. **Purge Temporary Variables**:
   - Slide variable declarations next to their usage.
   - Replace right-hand side calculations of temps with query functions.
   - Inline the variables to remove them from the local scope.
4. **Separate Phases**:
   - Identify calculation logic vs. rendering/formatting logic.
   - Extract the calculation logic into a function that populates and returns an `intermediateData` object.
   - Route the `intermediateData` object into the rendering function.
5. **Implement Polymorphism**:
   - If type-based conditionals exist in the calculation logic, create a base `Calculator` class.
   - Create subclasses for each type.
   - Write a factory function to instantiate the correct subclass.
   - Push the conditional branches down into the respective subclasses as overridden methods.
6. **Implement Feature**: Once the architecture cleanly supports the new requirement via phase separation or polymorphic subclasses, implement the requested feature.

# @Examples (Do's and Don'ts)

### Variable Naming
- **[DO]** Name return variables `result` and use types in parameters:
  ```javascript
  function amountFor(aPerformance, aPlay) {
      let result = 0;
      // ... calculation ...
      return result;
  }
  ```
- **[DON'T]** Use arbitrary names for accumulators or generic names for parameters:
  ```javascript
  function amountFor(perf, play) {
      let thisAmount = 0;
      // ... calculation ...
      return thisAmount;
  }
  ```

### Handling Temporary Variables
- **[DO]** Replace temporary variables with query functions to clean up scope:
  ```javascript
  function statement(invoice) {
      let totalAmount = totalAmountFor(invoice);
      let volumeCredits = totalVolumeCredits(invoice);
      // ...
  }
  // Later: Inline the variables completely.
  ```
- **[DON'T]** Calculate multiple temporary variables inline before using them:
  ```javascript
  function statement(invoice) {
      let play = plays[perf.playID];
      let thisAmount = amountFor(perf, play);
      // ...
  }
  ```

### Loop Splitting
- **[DO]** Use separate loops for separate accumulation tasks:
  ```javascript
  let totalAmount = 0;
  for (let perf of invoice.performances) {
      totalAmount += amountFor(perf);
  }
  
  let volumeCredits = 0;
  for (let perf of invoice.performances) {
      volumeCredits += volumeCreditsFor(perf);
  }
  ```
- **[DON'T]** Mix accumulations in a single loop for "efficiency":
  ```javascript
  for (let perf of invoice.performances) {
      volumeCredits += volumeCreditsFor(perf);
      totalAmount += amountFor(perf);
  }
  ```

### Phase Splitting
- **[DO]** Pass an intermediate data structure to a rendering function:
  ```javascript
  function statement(invoice, plays) {
      return renderPlainText(createStatementData(invoice, plays));
  }
  ```
- **[DON'T]** Mix formatting and mathematical calculation in the same block:
  ```javascript
  function statement(invoice, plays) {
      let result = `Statement for ${invoice.customer}\n`;
      let thisAmount = calculateAmount();
      result += ` Amount: ${thisAmount}\n`;
      return result;
  }
  ```

### Conditional Logic vs Polymorphism
- **[DO]** Use a Factory Function and polymorphism to handle type-specific behavior:
  ```javascript
  function createPerformanceCalculator(aPerformance, aPlay) {
      switch(aPlay.type) {
          case "tragedy": return new TragedyCalculator(aPerformance, aPlay);
          case "comedy": return new ComedyCalculator(aPerformance, aPlay);
          default: throw new Error(`unknown type: ${aPlay.type}`);
      }
  }
  // Subclasses TragedyCalculator and ComedyCalculator implement get amount()
  ```
- **[DON'T]** Use massive switch statements inside core calculation functions:
  ```javascript
  function amountFor(aPerformance) {
      let result = 0;
      switch(aPerformance.play.type) {
          case "tragedy":
              // 10 lines of math
              break;
          case "comedy":
              // 15 lines of math
              break;
      }
      return result;
  }
  ```