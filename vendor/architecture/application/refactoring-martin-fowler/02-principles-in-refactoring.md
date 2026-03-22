# @Domain
These rules MUST be triggered whenever the AI is tasked with modifying existing code, adding new features to an established codebase, addressing technical debt, improving code readability, reorganizing system architecture, or specifically instructed to "refactor," "clean up," or "restructure" code.

# @Vocabulary
- **Refactoring (Noun)**: A change made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior.
- **Refactoring (Verb)**: To restructure software by applying a series of refactoring steps without changing its observable behavior.
- **Observable Behavior**: The external functionality of the system as experienced by a user or calling client. This MUST remain completely unchanged during refactoring.
- **The Two Hats**: A metaphor for the two distinct modes of programming: "Adding Functionality" (adding features/tests without changing structure) and "Refactoring" (restructuring without adding features/tests).
- **Design Stamina Hypothesis**: The principle that putting effort into a good internal design increases the stamina of the software effort, allowing developers to add features faster for a longer period.
- **Rule of Three**: A trigger for refactoring. The first time you do something, do it. The second time, wince but do it. The third time you do something similar, you refactor.
- **Preparatory Refactoring**: Restructuring the code *before* adding a new feature to make the feature's implementation trivial or significantly easier.
- **Comprehension Refactoring**: Refactoring code simply to understand it better, moving the understanding from the developer's head directly into the code (e.g., renaming variables, extracting functions).
- **Litter-Pickup Refactoring**: The practice of cleaning up poorly designed code opportunistically when encountered, adhering to the "campsite rule" (always leave the code cleaner than you found it).
- **Published Interface**: An API or code boundary used by clients independent of the developers who declare it. These require special migration strategies when refactored.
- **Continuous Integration (CI) / Trunk-Based Development**: The practice of integrating code into a shared mainline frequently (daily) to avoid semantic merge conflicts caused by long-lived feature branches.
- **Yagni ("You Aren't Going to Need It")**: The practice of designing software only for currently understood needs without adding speculative flexibility mechanisms.
- **Parallel Change (Expand-Contract)**: A safe migration strategy for databases and published interfaces where a new structure is added alongside the old, writers update both, readers migrate to the new, and finally, the old is removed.

# @Objectives
- **Preserve Observable Behavior**: Ensure that the system does exactly what it did before the refactoring process began.
- **Eliminate Duplication**: Ensure the code says everything once and only once to minimize the risk of inconsistent modifications.
- **Increase Readability**: Structure the code so that its intent is immediately obvious to future human readers.
- **Facilitate Feature Addition**: Adapt the codebase's internal architecture to smoothly accept incoming functional requirements.
- **Isolate Changes**: Create well-defined modular boundaries so that future modifications require understanding only a small subset of the codebase.

# @Guidelines

## 1. The Two Hats Principle
- The AI MUST strictly separate "Adding Functionality" from "Refactoring".
- **Refactoring Hat**: When refactoring, the AI MUST NOT add any new features or behaviors. It MUST NOT add new tests (unless a missing case is discovered). It MUST only restructure existing code.
- **Adding Functionality Hat**: When adding a feature, the AI MUST NOT restructure existing code. It MUST only add new capabilities and the corresponding tests.
- If a user requests a new feature in a messy codebase, the AI MUST first propose putting on the "Refactoring Hat" to perform Preparatory Refactoring, and only after that is complete, switch to the "Adding Functionality Hat".

## 2. Execution Mechanics & Small Steps
- The AI MUST perform refactoring in tiny, discrete, semantics-preserving steps.
- The AI MUST verify that the code compiles and tests pass after EVERY single step.
- If a test fails during a refactoring step, the AI MUST immediately revert the code to the last known working state and attempt the change again using even smaller steps.
- The AI MUST NEVER leave the code in a broken state for an extended period.

## 3. When to Refactor (Triggers)
- **The Rule of Three**: If the AI detects that a similar logic structure is being written for the third time, it MUST extract it into a shared function or module.
- **Preparatory Trigger**: Before implementing a requested change, the AI MUST evaluate if parameterizing a function or extracting a class would make the requested change easier. If so, execute the refactoring first.
- **Comprehension Trigger**: If the AI encounters variables or functions with misleading or unclear names while analyzing a codebase, it MUST rename them to reflect their true intent.
- **Litter-Pickup Trigger**: If the AI spots convoluted logic or unnecessary complexity while working on an unrelated task, it MUST clean it up if it is a quick fix, or isolate it into a clearly named function if it requires more effort later.
- The AI MUST treat refactoring as a continuous, integrated activity, not a scheduled, separate phase of work.

## 4. When NOT to Refactor
- The AI MUST NOT refactor messy code if that code does not need to be modified or understood for the current task (e.g., a black-box API that works fine).
- The AI MUST NOT refactor code if it determines that rewriting the code from scratch would be significantly easier and faster.

## 5. Architectural Principles (Yagni)
- The AI MUST NOT introduce speculative flexibility mechanisms (e.g., adding parameters for hypothetical future use cases, creating abstract base classes for single implementations).
- The AI MUST build software that excellently solves ONLY the currently understood needs.
- If a new need arises, the AI MUST use refactoring to adapt the architecture to that specific need at that specific time.

## 6. Managing Boundaries and Published Interfaces
- When renaming or changing parameters of a function that is used by external, unmodifiable clients (a Published Interface), the AI MUST NOT perform a direct rename.
- The AI MUST use **Migration Mechanics**: Create the new function, make the old function delegate to the new function, mark the old function as deprecated, and leave it intact.
- The AI MUST avoid fine-grained strong code ownership boundaries that prevent cross-module refactoring.

## 7. Database Refactoring
- When modifying database schemas, the AI MUST use the **Parallel Change (Expand-Contract)** pattern.
- Step 1: Add the new schema structure (e.g., a new column) alongside the old.
- Step 2: Update application code to write to BOTH the old and new structures.
- Step 3: Update application code to read from the NEW structure.
- Step 4: Remove the old structure and the dual-write logic.

## 8. Performance Optimization vs. Refactoring
- The AI MUST NOT let speculative performance concerns deter it from extracting small functions or creating clear abstractions.
- The AI MUST strictly separate refactoring from performance optimization.
- During refactoring, the AI MUST focus entirely on code clarity and modifiability, even if it introduces slight inefficiencies (e.g., repeating a loop).
- If performance tuning is explicitly requested, the AI MUST first ensure the code is well-factored, and then apply targeted optimizations based ONLY on profiler data, not intuition.

## 9. Testing and Legacy Code
- The AI MUST rely on a suite of self-testing, automated tests to verify refactoring steps.
- If the AI is asked to refactor code that lacks tests (Legacy Code), the AI MUST first establish "seams" in the code and write tests to cover the current observable behavior before altering the internal structure.

# @Workflow
When tasked with modifying a codebase, the AI MUST adhere to the following algorithmic process:

1. **Assess the Goal**: Determine if the user request is to add a feature, fix a bug, or clean up code.
2. **Evaluate the Context (Preparatory Refactoring)**:
   - Does the existing architecture easily support the requested change?
   - If NO: Switch to the "Refactoring Hat". Identify the specific refactorings needed to make the change easy.
3. **Execute Refactoring Loop**:
   - **Step 3a**: Isolate a tiny, behavior-preserving code transformation (e.g., Extract Function, Rename Variable).
   - **Step 3b**: Apply the transformation.
   - **Step 3c**: Run automated tests (or instruct the user to run them).
   - **Step 3d**: If tests fail, REVERT immediately. Break the transformation into a smaller step. If tests pass, commit the change.
   - **Step 3e**: Repeat until the codebase is structurally prepared for the new feature or the cleanup is complete.
4. **Execute Feature Addition Loop** (If applicable):
   - Switch to the "Adding Functionality Hat".
   - Write a failing test for the new feature.
   - Write the simplest code to make the test pass. DO NOT restructure existing code during this step.
5. **Post-Implementation Cleanup (Litter-Pickup)**:
   - Review the newly added code. Does it contain duplication, poor names, or long functions?
   - If YES: Switch back to the "Refactoring Hat" and execute the Refactoring Loop (Step 3) until the new code is perfectly clean.

# @Examples (Do's and Don'ts)

## The Two Hats
- **[DO]** Add a new class to handle a new business rule, write tests for it, and wire it into the existing un-refactored main function. Once tests pass, switch hats and extract the combined logic into smaller, well-named functions.
- **[DON'T]** Change the signature of an existing core function, rewrite its internal logic to be cleaner, AND add a new feature to it in the exact same commit or response.

## Yagni & Speculative Generality
- **[DO]** Write a function `calculateBaseCharge(usage)` that only takes `usage` because that is the only variable currently affecting the charge.
- **[DON'T]** Write a function `calculateBaseCharge(usage, futureDiscountRate, seasonalAdjustment)` where the latter two parameters are ignored or default to zero just in case the business needs them next year.

## Published Interfaces (Migration Mechanics)
- **[DO]** When changing `addClient(client)` to `addClient(client, region)` in a public API:
  ```javascript
  // Retain old function as a pass-through
  /** @deprecated use addClientWithRegion */
  function addClient(client) {
      addClientWithRegion(client, "DEFAULT_REGION");
  }
  function addClientWithRegion(client, region) {
      // new implementation
  }
  ```
- **[DON'T]** Simply change the signature of `addClient(client)` to `addClient(client, region)` and break all external consumers who depend on the old signature.

## Database Expand-Contract (Parallel Change)
- **[DO]** To rename a column from `EMP_ID` to `EMPLOYEE_ID`:
  1. Add `EMPLOYEE_ID` to the table.
  2. Update the app to save to both `EMP_ID` and `EMPLOYEE_ID`.
  3. Migrate historical data from `EMP_ID` to `EMPLOYEE_ID`.
  4. Update the app to read from `EMPLOYEE_ID`.
  5. Drop `EMP_ID`.
- **[DON'T]** Execute `ALTER TABLE RENAME COLUMN EMP_ID TO EMPLOYEE_ID` and simultaneously rewrite all application SQL queries, hoping no data is lost or locked during deployment.

## Comprehension Refactoring
- **[DO]** Read a complex conditional `if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd))` and immediately use Extract Function to replace it with `if (isSummer(aDate, plan))`.
- **[DON'T]** Add a comment above the complex conditional saying `// Check if the date is in summer` and leave the complex code exactly as it is.