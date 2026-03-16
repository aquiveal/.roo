# @Domain
These rules are triggered whenever the AI is tasked with designing software architecture, scaffolding new projects, adding new features, refactoring existing codebases, evaluating code quality, or resolving code complexity and maintainability issues. 

# @Vocabulary
*   **Complexity (Entropy)**: Randomness, uncertainty, or a state of disorder in software. Anything that makes a system hard to understand and modify.
*   **Essential Complexity**: Complexity inherent to the problem itself that cannot be removed (e.g., user stories, required data/state, business logic, application rules).
*   **Accidental Complexity**: Complexity introduced by implementation decisions and design choices (e.g., specific classes, functions, loops). This is the complexity that must be ruthlessly controlled.
*   **Dependency**: A component needed for another component to work.
*   **Concretions**: A literal object created using the `new` keyword (as opposed to abstractions like interfaces or types).
*   **Coupling**: A measure of how intertwined two components are.
*   **Concrete Coupling**: Passing or creating literal objects (concretions) as dependencies, preventing isolated testing.
*   **Subclass Coupling**: When a child class is tightly connected to its parent class (`SomeClass extends BaseClass`).
*   **Temporal Coupling**: Bundling actions together simply because they happen at the same time (e.g., `CreateUserAndSendEmail`).
*   **Dynamic Coupling**: When the execution order of operations is rigidly important but not structurally enforced (e.g., calling `send()` before `setSubject()`).
*   **Cohesion**: A measure of how related components are within a particular module. High cohesion means components belong together; low cohesion implies obscurity.
*   **Ripple**: A symptom of complexity where a simple change requires modifications in several other parts of the codebase.
*   **Cognitive Load**: The number of elements a developer must hold in their brain to complete a task.
*   **Discoverability**: The ability to quickly identify where things are, what things are, and what capabilities exist in the codebase.
*   **Understandability**: The ease of knowing how to perform an action, knowing if it's being used correctly, and confirming it worked.
*   **Leaky Abstraction**: An abstraction that fails to hide its internal details, forcing the developer to learn the underlying implementation to use it correctly.
*   **Tactical Programming**: Brute-forcing a solution until it works, ignoring maintainability (acceptable *only* for proof-of-concepts).
*   **Strategic Programming**: A 50/50 split between writing code for users and writing code for future maintainers.
*   **Extreme Programming (XP)**: An Agile development methodology formalizing practices for shipping high-quality code.
*   **Simple Design**: Code that runs all tests, contains no duplication, maximizes clarity, and minimizes the number of elements.

# @Objectives
*   **Achieve the Primary Goal of Software**: Build products that serve the needs of the users and can be cost-effectively changed by developers over time.
*   **Eradicate Accidental Complexity**: Prevent the codebase from being strangled by disorder. Ensure new features can be added without an exponential increase in effort.
*   **Maximize Understandability and Maintainability**: Treat future developers (and the AI itself in future iterations) as the primary audience for the code.
*   **Implement Strategic Programming**: Refuse to write tactical, brute-force code for production systems. Every design decision must consider long-term maintainability.
*   **Enforce Extreme Programming (XP) Values**: Rely heavily on Feedback (TDD, short loops), Simplicity (simplest working thing), and Communication (code as declarative documentation).

# @Guidelines

### Complexity Mitigation & Requirement Mapping
*   The AI MUST clearly separate Essential Complexity (what to build) from Accidental Complexity (how it is built).
*   The AI MUST correctly translate non-functional requirements (conversations/prompts) into functional requirements (user stories and acceptance tests) before writing implementation code.
*   The AI MUST NOT introduce premature optimization. Do not add non-essential state, caches, database tricks, or complex infrastructure unless mathematically proven absolutely necessary by the essential complexity of the system.

### Dependency and Coupling Rules
*   The AI MUST strive for loose coupling between components (routines, methods, classes, modules, architecture).
*   The AI MUST avoid Concrete Dependencies. Do not instantiate concrete objects (using the `new` keyword for external services/infrastructure) directly inside a class. Use Dependency Injection (passing dependencies via constructor).
*   The AI MUST enable isolated testing. If a class relies on a database connection or external logger, it MUST be structured so those dependencies can be mocked or stubbed.
*   The AI MUST avoid Subclass Coupling where possible; favor composition or interfaces over deep inheritance trees.
*   The AI MUST avoid Temporal Coupling. Do not bundle unrelated actions into a single function just because they occur sequentially (e.g., do not write `CreateUserAndSendEmail`).
*   The AI MUST avoid Dynamic Coupling. Design APIs so that execution order is structurally enforced, making it impossible to perform operations out of order (e.g., prevent sending an email before the recipient is set).

### Cohesion and Clarity Rules
*   The AI MUST strive for High Cohesion. Group only related components within a module.
*   The AI MUST strictly avoid creating "Helper" classes. If a class is named `Helper` or `Util` and overloaded with unrelated methods, the AI MUST refactor it into cohesive, domain-specific modules.
*   The AI MUST NOT leave dead code, useless comments, or redundant information, as these cause obscurity.
*   The AI MUST clearly name variables, methods, and classes using terms from the domain to prevent ambiguity.

### Managing Abstractions
*   The AI MUST NOT create Unnecessary or Early Abstractions. Build the simplest possible thing that works first, and abstract only when duplication or testing requires it.
*   The AI MUST NOT create Leaky Abstractions. Tools and wrappers MUST completely encapsulate their underlying complexity.
*   The AI MUST NOT create overly layered architectures that increase Cognitive Load without providing a tangible maintainability benefit.

### Enforcing Extreme Programming (XP) Practices
*   **Feedback**: The AI MUST utilize short feedback loops. Write failing tests first, make them pass, and then refactor (TDD). 
*   **Simplicity**: The AI MUST adhere to the Simple Design rules in strict order: 1. Runs all tests. 2. No duplication. 3. Maximizes clarity. 4. Minimizes the number of elements.
*   **Communication**: The AI MUST use code as the primary mechanism for communication. Write declarative acceptance tests that act as the highest layer of abstraction and document the domain. Push implementation complexity downwards.
*   **Consistency**: The AI MUST establish and strictly follow a uniform coding standard throughout the project to prevent cognitive load explosions.

# @Workflow
When tasked with implementing a new feature or designing a system, the AI MUST follow this rigid algorithm:

1.  **Requirement Extraction (Essential Complexity)**
    *   Analyze the prompt to extract the declarative floor: user stories, necessary data/state, and business rules.
    *   Ignore UI cosmetics and infrastructural details at this stage.
2.  **Test-Driven Foundation (Feedback & Communication)**
    *   Write a high-level, declarative acceptance test that models the domain language and functional requirements.
    *   Write isolated unit tests for the target components.
3.  **Simplest Implementation (Simplicity)**
    *   Write the absolute simplest code to pass the tests. Do not add caches, state, or optimization.
    *   Ensure dependencies are passed in (Dependency Injection) rather than instantiated inside the module.
4.  **Complexity Detection & Refactoring (Mitigating Accidental Complexity)**
    *   Analyze the implementation for Ripple (Are changes contained?).
    *   Analyze for Cognitive Load (Are there too many concepts in one file?).
    *   Analyze for Cohesion (Are there helper files? Split them).
    *   Analyze for Coupling (Is there temporal or dynamic coupling? Fix the API design).
    *   Refactor to maximize clarity and remove duplication while keeping tests passing.
5.  **Review Code Documentation**
    *   Ensure the test code serves as an accurate, readable mounting point for future developers to learn the domain.

# @Examples (Do's and Don'ts)

### Concrete vs. Loose Coupling
**[DON'T]** Instantiating concrete dependencies inside a class, preventing isolated testing.
```typescript
class UserService {
  private db: MySqlConnection;
  private logger: Logger;

  constructor () {
    // ANTI-PATTERN: Concrete dependencies tightly coupled to the class.
    this.db = new MySqlConnection();
    this.logger = new Logger();
  }

  createUser () { /* ... */ }
}
```

**[DO]** Injecting dependencies to allow for isolated testing and loose coupling.
```typescript
class UserService {
  constructor (
    // DO: Dependencies are injected. Interfaces/Abstractions should be used here.
    private db: IDatabaseConnection,
    private logger: ILogger
  ) {}

  createUser () { /* ... */ }
}
```

### Temporal Coupling
**[DON'T]** Bundling actions together just because they happen at the same time.
```typescript
// ANTI-PATTERN: Temporal coupling. Low cohesion.
function createUserAndSendEmail(userData) {
  const user = db.save(userData);
  emailService.sendWelcome(user.email);
  return user;
}
```

**[DO]** Separating concerns so modules have high cohesion.
```typescript
// DO: Separate responsibilities. Let the caller or a domain event coordinate.
const user = userService.createUser(userData);
emailService.sendWelcome(user.email);
```

### Dynamic Coupling
**[DON'T]** Creating APIs where execution order is critical but not structurally enforced.
```typescript
// ANTI-PATTERN: Dynamic coupling. The compiler won't stop you from calling send() too early.
const email = new Email();
email.setRecipient("foo@example.com");
email.setSender("me@mydomain.com");
email.send(); 
email.setSubject("Hello World"); // Error: Called after send()
```

**[DO]** Structuring APIs so invalid states are impossible.
```typescript
// DO: Require necessary state upfront to prevent out-of-order execution.
const email = new Email({
  recipient: "foo@example.com",
  sender: "me@mydomain.com",
  subject: "Hello World"
});
email.send();
```

### High vs. Low Cohesion (Obscurity)
**[DON'T]** Creating generic "Helper" classes that obscure the architecture.
```typescript
// ANTI-PATTERN: Low cohesion "Helper" dumping ground.
class AppHelper {
  static formatDate(date) { /* ... */ }
  static hashPassword(password) { /* ... */ }
  static calculateTax(cart) { /* ... */ }
}
```

**[DO]** Grouping functionality into domain-specific, highly cohesive modules.
```typescript
// DO: High cohesion. Methods belong to focused, domain-specific modules.
class DateFormatter { /* ... */ }
class PasswordEncoder { /* ... */ }
class TaxCalculator { /* ... */ }
```