# @Domain
Code Refactoring, Legacy Code Modernization, Technical Debt Reduction, and Architectural Restructuring. This rule set activates when the user requests the AI to clean up, restructure, or refactor an existing function, separate calculation from rendering logic, or replace complex conditional switch statements with polymorphic class structures.

# @Vocabulary
*   **Refactoring**: The process of changing a software system in a way that does not alter the external observable behavior of the code, yet improves its internal structure.
*   **Self-Checking Tests**: A solid suite of automated tests that compare new outputs against hand-checked reference data and report successes (green) or failures (red) automatically.
*   **Compile-Test-Commit**: The micro-iteration workflow of Refactoring: make a small change, compile/transpile, run tests, and commit to local version control immediately.
*   **Extract Function**: Taking a cohesive fragment of code and moving it into its own function, named after its intent.
*   **Replace Temp with Query**: Removing a locally scoped temporary variable by replacing it with a function call that derives the same value.
*   **Inline Variable**: Replacing a variable reference with the actual expression used to assign it.
*   **Change Function Declaration**: The process of renaming a function to better match its intent, or modifying its parameters.
*   **Split Loop**: Separating a loop that calculates multiple unrelated things into separate distinct loops to facilitate function extraction.
*   **Slide Statements**: Moving related code (such as variable initializations) closer to where they are actually used.
*   **Split Phase**: Dividing a monolithic process into two sequential phases (e.g., calculation phase and formatting/rendering phase) connected by an Intermediate Data Structure.
*   **Intermediate Data Structure**: A plain object used to pass fully calculated and enriched data from a calculation phase to a rendering/formatting phase.
*   **Move Function**: Shifting a function from one scope or class to another to better group related logic.
*   **Replace Type Code with Subclasses**: Converting a literal type string/code into a dedicated class hierarchy.
*   **Replace Constructor with Factory Function**: Wrapping a constructor call in a standard function to allow for polymorphic instantiation (returning subclasses).
*   **Replace Conditional with Polymorphism**: Replacing `switch` or `if/else` statements that branch on a type code with overridden methods in a class hierarchy.
*   **Camping Rule**: The software engineering adage: "Always leave the code base healthier than when you found it."

# @Objectives
*   Improve code readability and maintainability by structuring it into small, intention-revealing functions and classes.
*   Prepare code for new features by restructuring it first: "When you have to add a feature to a program but the code is not structured in a convenient way, first refactor the program to make it easy to add the feature, then add the feature."
*   Eliminate local temporary variables that cause complex shadowing and scoping issues during code extraction.
*   Separate calculation logic entirely from presentation/formatting logic.
*   Eliminate large `switch` statements by implementing polymorphic dispatch.
*   Maintain 100% behavioral consistency by utilizing atomic, microscopic changes validated by automated tests.

# @Guidelines
*   **Test First**: The AI MUST NEVER begin a refactoring workflow without verifying or establishing a solid, self-checking test suite for the target code.
*   **Micro-Steps**: The AI MUST execute refactorings in tiny, atomic steps. After every structural change, the AI MUST recommend or simulate running the test suite. 
*   **Commit Frequently**: The AI MUST advise committing to local version control after every successful micro-step to easily revert mistakes.
*   **Naming by Intent**: The AI MUST name extracted functions based on *what* they do (their intent), not *how* they work.
*   **Return Variable Naming**: The AI MUST consistently name the primary return variable of any function `result`.
*   **Parameter Naming**: The AI MUST use the type name with an indefinite article for parameters (e.g., `aPerformance`, `anInvoice`) unless a more specific role name is applicable.
*   **Eradicate Temps**: The AI MUST aggressively remove temporary variables using *Replace Temp with Query* and *Inline Variable*. Temps encourage long, complex routines and hinder function extraction.
*   **Loop Duplication**: The AI MUST ignore theoretical performance concerns regarding looping multiple times. If a loop does two things, the AI MUST use *Split Loop* to separate them, even if it means iterating over the same collection twice. Rerunning a loop rarely affects performance, and well-factored code is easier to optimize later.
*   **Data Immutability**: The AI MUST treat data as immutable where practical during phase splitting (e.g., using `Object.assign({}, originalRecord)` to create enriched copies rather than mutating original inputs).
*   **Financial Math**: The AI MUST store and calculate monetary values as integer fractions (e.g., cents) to avoid floating-point errors, dividing by 100 ONLY at the formatting boundary.
*   **Abstracting Conditionals**: When calculation logic depends centrally on a type code, the AI MUST use *Replace Conditional with Polymorphism*.
*   **Base Class Defaults**: When creating polymorphic hierarchies, the AI MUST leave common or default behaviors in the superclass and only push down the specific variant logic into subclasses. Throw explicit errors (e.g., `throw new Error('subclass responsibility')`) for methods that must be overridden.

# @Workflow
To perform a complete refactoring of a monolithic function (based on the "First Example" methodology), the AI MUST follow this rigid, sequential algorithm:

1.  **Test Verification**:
    *   Assert that self-checking tests exist for the current behavior. If absent, generate them.
2.  **Function Deconstruction (Logic Extraction)**:
    *   Identify chunks of logic (e.g., switch statements calculating a value).
    *   Apply *Extract Function*.
    *   Rename internal variables (return values to `result`, parameters to `aType`).
3.  **Variable Eradication**:
    *   Identify temporary variables derived from parameters.
    *   Apply *Replace Temp with Query* to turn the derivation into a function.
    *   Apply *Inline Variable* to replace all usages of the temp with the new query function.
    *   Apply *Change Function Declaration* to remove the newly unnecessary parameters from other extracted functions.
4.  **Loop Separation**:
    *   Identify loops accumulating multiple unrelated variables.
    *   Apply *Split Loop* to create one loop per accumulator.
    *   Apply *Slide Statements* to move the accumulator initialization immediately above its respective loop.
    *   Apply *Extract Function* to the isolated loop.
    *   Apply *Inline Variable* to remove the accumulator temp entirely.
5.  **Phase Splitting (Calculation vs. Formatting)**:
    *   Apply *Extract Function* to the entire rendering/formatting block.
    *   Create an empty `Intermediate Data Structure` object.
    *   Pass this object between the calculation phase and the rendering phase.
    *   Iteratively move data attributes from the rendering parameters into the Intermediate Data Structure.
    *   Move calculation functions into the calculation phase, enriching the Intermediate Data Structure with derived properties.
6.  **Polymorphic Restructuring**:
    *   Identify conditional switch statements based on a type code.
    *   Create a base Class (e.g., `PerformanceCalculator`) taking the enriched data object.
    *   Apply *Move Function* to shift the conditional functions into the base class.
    *   Apply *Replace Constructor with Factory Function* to manage instantiation.
    *   Apply *Replace Type Code with Subclasses* by creating a Subclass for each type and updating the Factory Function to return the appropriate Subclass.
    *   Apply *Replace Conditional with Polymorphism* by overriding the methods in the Subclasses with the specific logic, removing the switch statements from the base class.

# @Examples (Do's and Don'ts)

### Variable Naming Inside Functions
*   **[DO]**:
    ```javascript
    function usd(aNumber) {
      let result = 0;
      // ... logic ...
      return result;
    }
    ```
*   **[DON'T]**:
    ```javascript
    function usd(number) {
      let format = 0; // Don't use contextual names for the return value
      // ... logic ...
      return format;
    }
    ```

### Replacing Temps with Queries
*   **[DO]**:
    ```javascript
    // No temporary variables, derived directly via query
    let thisAmount = amountFor(aPerformance, playFor(aPerformance));
    
    function playFor(aPerformance) {
      return plays[aPerformance.playID];
    }
    ```
*   **[DON'T]**:
    ```javascript
    // Keeping temporary variables that clutter the local scope
    const play = plays[perf.playID];
    let thisAmount = amountFor(perf, play);
    ```

### Loop Management
*   **[DO]**:
    ```javascript
    // Split loops to isolate accumulations, enabling function extraction
    for (let perf of invoice.performances) {
      result += ` ${playFor(perf).name}: ${usd(amountFor(perf))}\n`;
    }
    let totalAmount = 0;
    for (let perf of invoice.performances) {
      totalAmount += amountFor(perf);
    }
    ```
*   **[DON'T]**:
    ```javascript
    // Doing two unrelated things in one loop for theoretical performance gains
    let totalAmount = 0;
    for (let perf of invoice.performances) {
      result += ` ${playFor(perf).name}: ${usd(amountFor(perf))}\n`;
      totalAmount += amountFor(perf);
    }
    ```

### Polymorphism over Conditionals
*   **[DO]**:
    ```javascript
    function createPerformanceCalculator(aPerformance, aPlay) {
      switch(aPlay.type) {
        case "tragedy": return new TragedyCalculator(aPerformance, aPlay);
        case "comedy":  return new ComedyCalculator(aPerformance, aPlay);
        default: throw new Error(`unknown type: ${aPlay.type}`);
      }
    }
    class TragedyCalculator extends PerformanceCalculator {
      get amount() {
        let result = 40000;
        if (this.performance.audience > 30) {
          result += 1000 * (this.performance.audience - 30);
        }
        return result;
      }
    }
    ```
*   **[DON'T]**:
    ```javascript
    function amountFor(aPerformance, play) {
      let result = 0;
      switch (play.type) {
        case "tragedy":
          result = 40000;
          if (aPerformance.audience > 30) {
            result += 1000 * (aPerformance.audience - 30);
          }
          break;
        case "comedy":
          // ...
          break;
      }
      return result;
    }
    ```

### Phase Splitting (Intermediate Data Structure)
*   **[DO]**:
    ```javascript
    // Phase 1: Calculate
    function createStatementData(invoice, plays) {
      const statementData = {};
      statementData.customer = invoice.customer;
      statementData.performances = invoice.performances.map(enrichPerformance);
      statementData.totalAmount = totalAmount(statementData);
      return statementData;
    }
    
    // Phase 2: Render
    function renderPlainText(data) {
      let result = `Statement for ${data.customer}\n`;
      for (let perf of data.performances) {
        result += `${perf.play.name}: ${usd(perf.amount)}\n`;
      }
      return result;
    }
    ```
*   **[DON'T]**:
    ```javascript
    // Mixing raw data calculation and string formatting
    function statement(invoice, plays) {
      let result = `Statement for ${invoice.customer}\n`;
      let totalAmount = 0;
      for (let perf of invoice.performances) {
        let thisAmount = calculateAmount(perf, plays);
        totalAmount += thisAmount;
        result += `${plays[perf.playID].name}: ${thisAmount}\n`;
      }
      return result;
    }
    ```