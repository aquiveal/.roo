# @Domain
Documenting, defining, proposing, or executing code refactorings; creating a refactoring catalog; structuring educational or reference material about code transformations.

# @Vocabulary
- **Refactoring Catalog**: A structured reference collection of the most useful code transformations.
- **Standard Format**: The rigid five-part structure used to document a refactoring: Name, Sketch, Motivation, Mechanics, and Examples.
- **Name / Aliases**: The primary identifier for a refactoring used to build a shared vocabulary, alongside common alternative names.
- **Sketch**: A brief, at-a-glance code transformation example (before and after) serving as a memory-jogger.
- **Motivation**: The rationale explaining *why* a refactoring should be applied, and explicitly describing circumstances in which it *shouldn't* be done.
- **Mechanics**: A concise, step-by-step procedural checklist for safely executing the refactoring in the smallest possible increments.
- **Examples**: Laughably simple, textbook-style code snippets demonstrating only the specific refactoring, stripped of real-world business complexity.
- **Inverse Refactoring**: The logical opposite of a specific refactoring (e.g., Extract vs. Inline). 

# @Objectives
- Structure all refactoring proposals, definitions, and tutorials using the strict five-part standard format.
- Break down execution mechanics into the smallest possible, safest steps.
- Prioritize small, verifiable steps with continuous testing over large, sweeping changes.
- Isolate examples to demonstrate *only* the specific refactoring, intentionally ignoring other code smells if fixing them would distract from the core lesson.

# @Guidelines
- **Mandatory Formatting**: When detailing a refactoring, the AI MUST use the exact five sections in order: Name, Sketch, Motivation, Mechanics, Examples.
- **Vocabulary Building**: The AI MUST include aliases if the refactoring is known by other names in the industry.
- **Minimal Sketching**: The AI MUST keep the Sketch minimal, showing just a brief before/after code snippet without deep explanation.
- **Clear Boundaries**: The AI MUST clearly define both when to use the refactoring and when NOT to use it in the Motivation section.
- **Granular Mechanics**: The Mechanics section MUST be formatted as a step-by-step checklist. The steps MUST be terse and actionable.
- **Continuous Testing**: The Mechanics section MUST explicitly mandate running tests after every single logical modification.
- **Safety Fallback**: If the AI simulates or encounters a bug/test failure during a refactoring process, it MUST back out the last step and break the action down into even smaller baby steps. The trickier the situation, the smaller the steps must be.
- **Trivial Examples**: The AI MUST keep examples intentionally simple ("laughably simple textbook kind"). Do not overcomplicate examples with complex business modeling or deep domain logic.
- **Focused Scope**: In Examples, the AI MUST NOT attempt to fix every code smell present in the snippet. The AI MUST leave unrelated bad code intact if fixing it compromises the self-contained focus of the specific refactoring being demonstrated.
- **Targeted Highlighting**: The AI MUST highlight or specifically point out the exact lines of changed code, but MUST avoid over-highlighting the entire block, as too much highlighting defeats the purpose.
- **Pragmatic Selection**: The AI MUST focus on documenting or proposing "useful" refactorings. Trivial transformations or logically existing but uninteresting inverse refactorings should be omitted from catalog-style outputs unless explicitly requested.

# @Workflow
1. **Identify**: Determine the specific refactoring to be defined or executed.
2. **Naming & Sketching**: State the Name (and aliases). Provide a concise before/after code Sketch to jog the memory.
3. **Motivate**: Write the Motivation. Explicitly detail the "why" and define the boundary conditions of when to avoid it.
4. **Detail Mechanics**: Write the Mechanics as a rigid, step-by-step checklist. Ensure steps are tiny, explicitly include testing steps, and note special edge cases.
5. **Demonstrate**: Provide a simple Example. Show the starting code, walk through the Mechanics step-by-step to transform it, and show the final result. Keep the domain trivial.

# @Examples (Do's and Don'ts)

- **[DO]** Structure a refactoring definition strictly:
  **Name:** Extract Function (aka Extract Method)
  **Sketch:** `code before` -> `code after`
  **Motivation:** Use when intention and implementation are mixed. Do not use if the code is already perfectly clear.
  **Mechanics:** 1. Create new function. 2. Copy code. 3. Pass local variables. 4. Test.
  **Example:** A simple print statement being moved to a `printDetails()` function.

- **[DON'T]** Mix the motivation into the mechanics, or present the refactoring as a single massive code replacement without a step-by-step breakdown.

- **[DO]** Keep examples laughably simple:
  ```javascript
  // Example of Extract Variable
  const basePrice = quantity * itemPrice;
  return basePrice - discount;
  ```

- **[DON'T]** Use a 500-line complex enterprise microservice example that obscures the core refactoring:
  ```javascript
  // Anti-pattern: Too complex for a catalog example
  const basePrice = order.lineItems.reduce((acc, item) => acc + (item.qty * item.fetchDynamicPrice(apiClient)), 0);
  // ... 40 more lines of business logic ...
  ```

- **[DO]** Revert and take smaller steps if an error is assumed or encountered: "Since this step caused a test failure, we will back out the last step, and instead first encapsulate the variable before moving it."

- **[DON'T]** Fix unrelated code smells in a specific refactoring example. If demonstrating `Rename Variable`, do not simultaneously demonstrate `Replace Loop with Pipeline` in the same example block. Leave the ugly loop intact to maintain focus.