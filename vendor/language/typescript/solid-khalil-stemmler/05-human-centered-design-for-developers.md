@Domain
These rules MUST trigger when the AI is tasked with writing, refactoring, or structuring code, designing public APIs, creating object models, organizing file structures, or evaluating code for readability, maintainability, and developer experience (DX).

@Vocabulary
- **Human-Centered Design (HCD)**: A design philosophy that puts the users' (in this case, other developers/maintainers) needs, behaviors, and pain points first.
- **Discoverability**: The ease with which a developer can figure out what actions are possible within a codebase (The "Gulf of Execution").
- **Understanding**: The ease with which a developer can figure out what happened after an action was taken (The "Gulf of Evaluation").
- **The 7 Stages of Action**: The psychological sequence humans follow: Goal -> Plan -> Specify -> Perform -> Perceive -> Interpret -> Compare.
- **Knowledge in the Head**: Knowledge that must be memorized, learned, or logically deduced (e.g., domain logic, architecture).
- **Knowledge in the World**: Knowledge that is visibly embedded in the environment and requires no learning (e.g., type errors, folder structures, pre-commit checks).
- **Affordances**: Visual cues or physical properties that communicate the intended purpose or possible actions of an object (e.g., TypeScript interfaces/abstract classes, folder structures).
- **Signifiers**: Labels, marks, or explicit sounds/text that communicate *where* and *how* an action should take place (e.g., Design pattern names like `Factory`, descriptive tests).
- **Accidental Signifiers**: Unintentional cues that imply negative system traits (e.g., commented-out code, deep nesting, "Helpers").
- **Constraints**: Physical, cultural, semantic, or logical restrictions that limit possible actions to prevent errors (e.g., static typing, private access modifiers).
- **Mapping (Grouping & Proximity)**: The relationship between controls and the items they control. Grouping related items together and placing controls in close proximity to the data they mutate.
- **Anemic Domain Model**: An anti-pattern resulting from poor Mapping, where data objects have no behavior, and external "Manager" classes manipulate their state.
- **Feedback**: Immediate communication of the results of an action.
- **CQS (Command Query Separation)**: A feedback mechanism in code. A Command mutates state and returns nothing (or an ID/Success state); a Query returns data and mutates nothing.
- **Conceptual Models**: High-level encapsulations of how a system works, allowing developers to predict the effects of their actions without knowing low-level details.
- **Law of Demeter (Principle of Least Knowledge)**: Objects should only talk to their immediate friends; they should not chain methods across unrelated objects.

@Objectives
- Treat code maintainers as the primary users of the codebase; prioritize Developer Experience (DX) over sheer computational brevity.
- Maximize **Discoverability** by embedding "Knowledge in the World" so developers do not have to rely on tribal knowledge ("Knowledge in the Head").
- Maximize **Understanding** by establishing clear Conceptual Models, immediate Feedback mechanisms (strict typing, explicit errors), and standardized constraints.
- Ensure that the code can answer "Yes" to three questions: 1) Is it obvious what this code does? 2) Is it easy to find where to change a feature? 3) Can it be changed without introducing bugs?

@Guidelines

**1. Managing Knowledge (Head vs. World)**
- The AI MUST embed "Knowledge in the World" into the codebase. You must rely on the compiler, strict typing, explicit folder structures, and automated tests to guide developers, requiring ZERO tribal knowledge to navigate the codebase.
- The AI MUST reserve "Knowledge in the Head" exclusively for the business domain and high-level architectural rules.

**2. Designing Affordances (Feedforward)**
- The AI MUST leverage the structural affordances of the chosen language. In TypeScript, explicitly use `interface`, `type`, and `abstract class` to define contracts.
- The AI MUST structure code repositories and folders to provide immediate affordances (e.g., feature-driven folder structures, clear READMEs).
- The AI MUST write BDD-style acceptance tests (Given/When/Then) as high-level affordances to explain *what* the code does.

**3. Applying Signifiers (Intentional vs. Accidental)**
- The AI MUST use Intentional Signifiers. When applying a design pattern, append the pattern name to the class/file name (e.g., `UserFactory`, `StudentController`, `UserRepository`).
- The AI MUST proactively remove Accidental Signifiers. Never leave commented-out code, deeply nested `if/else` statements, or ambiguous "Helper" classes, as these signify technical debt and confusion.

**4. Implementing Constraints**
- The AI MUST restrict illegal states using language-level constraints. Use `readonly`, `const`, and `private` access modifiers to prevent unauthorized mutations.
- The AI MUST use the Factory Pattern with private constructors to enforce validation constraints on Value Objects and Entities. Never allow an object to be instantiated in an invalid state.
- The AI MUST enforce semantic constraints via strictly-typed errors (e.g., returning a specific `Result` or `Either` monad) rather than throwing generic exceptions.

**5. Optimizing Mapping (Grouping and Proximity)**
- **Grouping (Cohesion)**: The AI MUST group related methods, classes, and functions together. Ensure strict adherence to the Single Responsibility Principle and architectural boundaries.
- **Proximity (Coupling)**: The AI MUST place controls (methods) as close to the object they control as possible. State and the behaviors that mutate that state MUST live in the same class.
- The AI MUST strictly avoid Anemic Domain Models. Do not create dumb data objects manipulated by external "Manager" or "Service" classes unless explicitly requested for a specific architectural reason (like ECS in game dev).
- The AI MUST adhere to the Law of Demeter. Design APIs where the returned object contains the methods required to act upon it (e.g., `node.getAttribute()` rather than `NodeManager.getAttribute(node)`).

**6. Providing Feedback**
- The AI MUST implement Command Query Separation (CQS) universally to provide predictable feedback. Commands MUST execute side-effects and return no data (or simply a success/failure state). Queries MUST return data and execute absolutely no side-effects.
- The AI MUST utilize compile-time type checking to provide immediate feedback to the developer. Avoid `any` or loose dynamic typing.

**7. Establishing Conceptual Models**
- The AI MUST encapsulate low-level complexity behind Intention Revealing Interfaces. A developer should understand *what* a class does without reading its implementation details.

**8. Testing for Cleanliness**
- The AI MUST self-evaluate code before delivering it:
  1. *What does it do?* (Is it readable, clear, brief?)
  2. *Where is it?* (Are files small and packaged by feature?)
  3. *Can I change it safely?* (Is it loosely coupled, type-safe, and boundary-enforced?)

@Workflow
1. **Analyze Developer Goals**: Identify the exact task the developer/maintainer needs to accomplish (e.g., run the app, find a feature, add a feature, debug).
2. **Establish the Conceptual Model**: Determine the appropriate design pattern or domain concept required to encapsulate the implementation details.
3. **Optimize Discoverability (Feedforward)**:
   - Define **Affordances**: Create explicit interfaces/types.
   - Add **Signifiers**: Name the classes/variables using domain terms and pattern names.
   - Enforce **Constraints**: Make constructors private where validation is required; use `readonly`.
   - Apply **Mapping**: Co-locate state and behavior; group related files in feature modules.
4. **Optimize Understanding (Feedback)**:
   - Separate methods strictly into Commands or Queries (CQS).
   - Ensure all failure states are explicit and handled by the type system.
5. **Cleanliness Verification**: Review the output against the three human-centered cleanliness questions (Readability, Locatability, Stability).

@Examples (Do's and Don'ts)

**Signifiers and Conceptual Models**
- [DO]: Name constructs explicitly after their domain purpose and design pattern.
  ```typescript
  class UserFactory {
    public static create(props: UserProps): User { ... }
  }
  ```
- [DON'T]: Use accidental signifiers or vague concepts that force the developer to read the entire file to understand its purpose.
  ```typescript
  class UserHelper {
    public static make(props: any): any { ... }
  }
  ```

**Constraints (Preventing Illegal States)**
- [DO]: Use private constructors and static factory methods to constrain creation to valid states only.
  ```typescript
  class EmailAddress {
    private constructor(private readonly email: string) {}

    public static create(email: string): EmailAddress {
      if (!isValid(email)) throw new Error("Invalid email");
      return new EmailAddress(email);
    }
  }
  ```
- [DON'T]: Provide public constructors that allow developers to instantiate illegal/invalid states.
  ```typescript
  class EmailAddress {
    public email: string;
    constructor(email: string) {
      this.email = email; // Developer can pass an invalid string or mutate it later
    }
  }
  ```

**Mapping (Proximity and Avoiding Anemic Models)**
- [DO]: Keep behavior and state in the same class (Good Mapping).
  ```typescript
  class User {
    private state: UserState;
    constructor(state: UserState) { this.state = state; }

    public changeName(newName: string): void {
      this.state.name = newName;
    }
  }
  ```
- [DON'T]: Separate state from behavior, creating an Anemic Domain Model.
  ```typescript
  class User { // Dumb data object
    public name: string;
  }
  
  class UserManager { // Control is separated from the item it controls
    public changeName(user: User, newName: string): void {
      user.name = newName;
    }
  }
  ```

**Feedback (Command Query Separation)**
- [DO]: Strictly separate Commands (mutation, no return) and Queries (no mutation, returns data).
  ```typescript
  class PostService {
    // Command
    public upvotePost(postId: string): void { ... }
    // Query
    public getPost(postId: string): Post { ... }
  }
  ```
- [DON'T]: Mix commands and queries, causing unpredictable feedback and side effects.
  ```typescript
  class PostService {
    // Mixed: Mutates state AND returns data. Violates CQS.
    public upvoteAndReturnPost(postId: string): Post { ... }
  }
  ```