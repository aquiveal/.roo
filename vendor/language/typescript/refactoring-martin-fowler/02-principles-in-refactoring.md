@Domain
Trigger these rules when the user requests code cleanup, code restructuring, technical debt reduction, modernization, code reviews, or when the user asks to add a feature or fix a bug in poorly structured, difficult-to-understand, or duplicated code.

@Vocabulary
- **Refactoring (Noun)**: A change made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior.
- **Refactoring (Verb)**: To restructure software by applying a series of behavior-preserving refactorings.
- **Observable Behavior**: The overall functionality of the program from the user's perspective. It must remain identical before and after refactoring (excluding performance characteristics or fixed latent bugs).
- **The Two Hats**: A metaphor for the strict separation of software development activities into two distinct modes: "Adding Functionality" (changing behavior, adding tests) and "Refactoring" (restructuring only, no new behavior, no new tests).
- **Design Stamina Hypothesis**: The principle that putting effort into good internal design (via refactoring) increases the stamina of the software effort, allowing the team to add new features faster for a longer period.
- **The Rule of Three**: A heuristic stating that the first time you do something, you just do it; the second time, you wince but do it; the third time you do something similar, you MUST refactor.
- **Preparatory Refactoring**: Restructuring code immediately *before* adding a new feature to make the feature addition easier and faster.
- **Comprehension Refactoring**: Refactoring code (e.g., renaming variables, extracting functions) specifically to move the developer's understanding of what the code does from their head into the code itself.
- **Litter-Pickup Refactoring**: The practice of cleaning up bad code opportunistically when encountered during other tasks ("leave the camp site cleaner than when you found it").
- **Self-Testing Code**: A suite of automated tests that run quickly and are self-checking (evaluating their own results), acting as a reliable bug detector.
- **Published Interface**: An API or code boundary used by clients independent of those who declare the interface, making it impossible to confidently change all callers simultaneously.
- **Branch By Abstraction**: A strategy for long-term refactoring where an abstraction layer is introduced to safely switch between old and new implementations over time.
- **Parallel Change (Expand-Contract)**: A database or API refactoring strategy where you first expand the schema (add new structure), migrate data/callers, and finally contract (remove the old structure).
- **Yagni (You Aren't Going to Need It)**: An incremental design approach where speculative flexibility mechanisms are avoided in favor of building exactly what is needed now, relying on refactoring to adapt to future requirements.

@Objectives
- Execute code modifications using a strict separation of concerns (The Two Hats) to ensure safe, predictable evolution.
- Improve the internal design and readability of the codebase without altering its observable behavior.
- Maximize long-term development speed by preventing architectural decay and establishing a healthy codebase (Design Stamina Hypothesis).
- Mitigate the risk of introducing bugs by making micro-changes, testing frequently, and prioritizing self-testing code.
- Ensure that system architecture evolves incrementally (Yagni) rather than relying on up-front, speculative design.

@Guidelines
- **Enforce the Two Hats**: The AI MUST NEVER mix adding new features with refactoring in the same step. If requested to do both, the AI MUST explicitly separate them: first refactor to make the change easy, then add the feature.
- **Respect Observable Behavior**: The AI MUST ensure that any refactoring step leaves the program doing exactly what it did before. 
- **Micro-Steps and Reversion**: The AI MUST take tiny, isolated steps. If a test fails or code breaks during refactoring, the AI MUST immediately revert to the last working state and attempt the change using even smaller steps.
- **Opportunistic Refactoring Over Planned**: The AI MUST proactively suggest Preparatory, Comprehension, or Litter-Pickup refactorings when executing standard feature additions or bug fixes, rather than waiting for a "refactoring phase."
- **Handle Published Interfaces with Care**: When refactoring a Published Interface, the AI MUST NOT immediately delete or change the signature of the original function. It MUST implement the new function and retain the old function as a deprecated pass-through/delegate until all clients are confirmed migrated.
- **Database Refactoring Constraints**: The AI MUST execute database structural changes using the Parallel Change (Expand-Contract) pattern. Data migration must be composed of small, reversible scripts.
- **Legacy Code Constraints**: If asked to refactor code lacking automated tests, the AI MUST prioritize creating testing seams (per *Working Effectively with Legacy Code*) or rely strictly on safe, automated syntax-tree-level transformations.
- **Defer Performance Optimization**: The AI MUST ignore performance concerns during refactoring unless a severe bottleneck is introduced. The AI MUST prioritize clean, well-factored code first, and optimize ONLY later using a profiler to target specific hotspots.
- **Reject Speculative Generality**: The AI MUST NOT introduce parameters, abstractions, or flexibility mechanisms for anticipated future use (Yagni). Only introduce complexity to solve current requirements.
- **Semantic Code Review**: When reviewing code, the AI MUST suggest improvements by actually performing Comprehension Refactorings to see if the proposed design is better, rather than just theorizing.

@Workflow
1. **Hat Identification**: State explicitly which "Hat" is currently being worn ("Refactoring" or "Adding Functionality").
2. **Safety Verification**: Check for the presence of Self-Testing Code. If absent, warn the user and restrict actions to provably safe AST-level transformations.
3. **Trigger Evaluation**: 
   - If adding a feature: Evaluate for *Preparatory Refactoring*. (Can the code be structured to make this feature easier to add?)
   - If reading complex code: Evaluate for *Comprehension Refactoring*. (Can variables be renamed or functions extracted to clarify intent?)
   - If encountering messy adjacent code: Evaluate for *Litter-Pickup Refactoring*.
   - If writing similar code for the third time: Apply the *Rule of Three* and extract the duplication.
4. **Micro-Execution**:
   - Perform the refactoring in the smallest possible increment.
   - Run tests (or instruct the user to run tests).
   - If tests fail, revert immediately. Do not attempt complex debugging while wearing the Refactoring Hat.
5. **Context Check**: Ensure Published Interfaces and Database Schemas utilize gradual migration (Pass-throughs / Parallel Change).
6. **Swap Hats**: Once the codebase is healthy and structured to support the new requirement, switch to the "Adding Functionality" hat and implement the user's primary request.

@Examples (Do's and Don'ts)

**Principle: The Two Hats**
- [DO]: "I will first refactor the `calculateInvoice` function by extracting the discount logic so it is easier to modify. Once tests pass, I will switch hats and add the new 'Summer Discount' feature."
- [DON'T]: "I will restructure `calculateInvoice` and sneak in the new 'Summer Discount' logic at the same time while I'm moving the code around."

**Principle: Preparatory Refactoring**
- [DO]: Recognize that a requested feature requires calling a function with slightly different parameters. First, apply `Parameterize Function` to the existing code. Verify it works. Then, call the newly parameterized function for the new feature.
- [DON'T]: Copy and paste an existing function, change a few literal values in the copy, and use the new duplicated function to deliver the feature quickly.

**Principle: Published Interfaces**
- [DO]: 
  ```javascript
  // New function
  function calculateCircumference(radius) { return 2 * Math.PI * radius; }
  
  // Old published interface retained as a pass-through
  /** @deprecated use calculateCircumference */
  function circum(radius) { return calculateCircumference(radius); }
  ```
- [DON'T]: Simply rename `circum` to `calculateCircumference` and delete `circum`, instantly breaking all external clients who depend on the old API.

**Principle: Performance vs. Refactoring**
- [DO]: Extract a complex loop body into a clearly named function, even if it adds a slight function-call overhead. State: "We will refactor for clarity first. If performance is an issue, we will profile and tune the well-factored code later."
- [DON'T]: Write a monolithic, 500-line function with complex inline bitwise operations because "it runs faster," sacrificing readability and evolvability.

**Principle: Comprehension Refactoring**
- [DO]: Extract a cryptic boolean condition `(age > 65 && yearsEmployed > 10)` into a well-named function `isEligibleForFullPension(employee)`.
- [DON'T]: Leave the complex boolean logic inline and just add a comment `// check if eligible for full pension` above it. Move the understanding into the code itself.