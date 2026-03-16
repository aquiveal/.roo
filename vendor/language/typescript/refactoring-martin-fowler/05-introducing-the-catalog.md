# @Domain
These rules are activated whenever the AI is tasked with explaining, proposing, or executing a code refactoring. They also apply when the user asks the AI to document a code transformation pattern or restructure existing code to improve its internal design without altering its observable behavior.

# @Vocabulary
- **Refactoring Catalog**: The standardized collection of refactoring techniques, defined by a specific vocabulary and structured format.
- **Name**: The canonical identifier for a refactoring (e.g., "Extract Function"), crucial for building a shared developer vocabulary.
- **Sketch**: A brief, minimal "before and after" code snippet used to quickly jog the memory about what the refactoring does.
- **Motivation**: The rationale explaining *why* the refactoring should be applied, and the circumstances under which it *should not* be applied.
- **Mechanics**: A concise, step-by-step checklist detailing the exact procedure to carry out the refactoring safely.
- **Examples**: Laughably simple, textbook-style code snippets designed solely to illustrate the refactoring mechanics without domain complexity distractions.
- **Small Steps**: The foundational principle of safe refactoring; breaking a transformation down into the tiniest possible incremental changes.
- **Inverse Refactoring**: The exact opposite code transformation of a given refactoring (e.g., "Inline Function" is the inverse of "Extract Function").

# @Objectives
- The AI MUST standardize the communication of code transformations by strictly adhering to the 5-part Refactoring Catalog format (Name, Sketch, Motivation, Mechanics, Examples).
- The AI MUST prioritize extreme safety during code execution by utilizing the "Small Steps" methodology.
- The AI MUST decouple the explanation of refactoring mechanics from domain complexity by utilizing isolated, trivially simple examples.
- The AI MUST treat refactorings as self-contained operations, resisting the urge to fix every tangential code smell during a single refactoring exercise.

# @Guidelines
- **Strict 5-Part Presentation**: When proposing or explaining a refactoring to the user, the AI MUST structure its response using exactly these five sections: Name, Sketch, Motivation, Mechanics, and Examples.
- **Vocabulary Standardization**: The AI MUST use the canonical names of refactorings (and list common aliases if applicable) to ensure clear communication.
- **Step-by-Step Execution**: The AI MUST execute refactorings strictly according to a step-by-step "Mechanics" checklist.
- **Micro-Commits / Small Steps**: The AI MUST break down code changes into the smallest possible increments. Large, sweeping rewrites are strictly prohibited.
- **Continuous Testing**: The AI MUST test the code (or instruct the user to run tests) after *every single step* of the Mechanics checklist.
- **Revert and Reduce**: If a test fails or a bug is introduced during a step, the AI MUST immediately revert to the last known working state and break the failed step down into even smaller, safer steps.
- **Explanatory Simplicity**: When generating examples to illustrate a refactoring concept, the AI MUST use textbook-simple scenarios. The AI MUST NOT use complex business logic or real-world domain models that could distract from the mechanics of the code transformation.
- **Self-Contained Focus**: When performing a requested refactoring, the AI MUST NOT attempt to fix other code smells simultaneously. The AI MUST leave the code as it is after the single refactoring is complete, reserving other improvements for separate, subsequent refactorings.
- **Highlighting Change**: When presenting code, the AI MUST clearly highlight or emphasize the specific lines of code that have changed to make the transformation obvious.

# @Workflow
When the AI is tasked with executing a refactoring, it MUST adhere to the following rigid algorithm:
1. **Identify and Propose**: Identify the correct refactoring pattern. Present it to the user using the standard 5-part format (Name, Sketch, Motivation, Mechanics, Example).
2. **Isolate Target**: Identify the exact boundaries of the code to be refactored.
3. **Initiate Small Steps**: Begin executing the first step defined in the "Mechanics" section.
4. **Verify**: Ensure the code syntax is valid and tests pass.
5. **Iterate or Revert**: 
   - If successful, proceed to the next step in the Mechanics checklist.
   - If an error occurs, revert the code to the state before the current step, divide the step into smaller sub-steps, and try again.
6. **Terminate**: Stop modifying the code immediately once the specific refactoring's mechanics are complete. Do not proceed to unrelated cleanups.

# @Examples (Do's and Don'ts)

**Principle: The 5-Part Catalog Format**
- [DO]: Present a proposed refactoring as:
  **Name**: Extract Function (alias: Extract Method)
  **Sketch**: `function printOwing() { printBanner(); printDetails(); }`
  **Motivation**: Separates intention from implementation.
  **Mechanics**: 1. Create new function. 2. Copy code. 3. Pass variables. 4. Replace original code with call.
  **Example**: [Simple code block]
- [DON'T]: Say "I think we should pull this code out into a new method to make it cleaner. Here is the rewritten file."

**Principle: Small Steps Execution**
- [DO]: Change a single variable name, run a test, update the variable's assignment, run a test, update the variable's return statement, run a test.
- [DON'T]: Rewrite an entire 50-line function, changing all variables, extracting three methods, and modifying the return type in a single code generation block.

**Principle: Laughably Simple Examples**
- [DO]: Use an example like calculating the base price of a generic "Order" with `quantity * itemPrice` to demonstrate Extract Variable.
- [DON'T]: Use an example involving a highly complex multi-tenant database query with asynchronous callbacks to demonstrate Extract Variable.

**Principle: Self-Contained Refactoring**
- [DO]: Complete an "Extract Function" request, leaving behind a poorly named variable if that variable was not the target of the current refactoring.
- [DON'T]: Complete an "Extract Function" request and silently "fix" the variable names, restructure a loop, and remove a middle man object just because they were nearby.