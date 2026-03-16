# @Domain
These rules MUST activate when the AI is tasked with designing, evaluating, or refactoring Object-Oriented code, creating domain models, structuring business logic, addressing code quality/architecture, or performing code reviews in JavaScript/TypeScript projects.

# @Vocabulary
- **Code Smell**: An unideal characteristic of code that signifies a larger design problem. It is not a bug and does not stop compilation, but if unaddressed, turns a codebase into an unmaintainable state.
- **Anti-Pattern**: A full-blown, deliberate approach to a commonly occurring problem that has severely negative long-term consequences. It is a fundamentally wrong approach for the given context.
- **Data Clump**: A code smell where multiple variables or parameters are frequently passed together, indicating they should be grouped into a single object.
- **Lazy Class**: A code smell where a class does too little to justify its existence (often caused by blindly following a "one component per file" rule).
- **God Object**: A code smell where a single file or class contains too much functionality. (Note: May be acceptable/ideal in microcontroller development for performance, but is an anti-pattern in web development).
- **Soft-Code**: An anti-pattern where business logic is stored in configuration files (e.g., YAML) rather than source code, making the system overly abstract and hard to maintain.
- **Interface Bloat**: An anti-pattern where an interface is so robust and contains so many attributes/methods that it becomes challenging to implement.
- **Anemic Domain Model**: An anti-pattern (in web development) where models are merely data containers, and all business/domain logic is handled by external services, controllers, or helpers.
- **Entity Component System (ECS)**: An architectural pattern commonly used in game development that favors composition over inheritance and intentionally uses anemic models by separating data (components) from behavior (systems).
- **Overengineering**: An anti-pattern caused by aggressively applying the DRY (Do Not Repeat Yourself) principle to the point where the abstraction becomes harder to understand and change than the repetitive code would have been.

# @Objectives
- Optimize software design for human readability and maintainability over strict adherence to abstract programming dogmas.
- Eliminate code smells through strategic refactoring and grouping of parameters/data.
- Prevent the creation of Anemic Domain Models in web applications by richly encapsulating business rules directly inside domain objects.
- Adapt architectural choices strictly based on the technical context (e.g., Web vs. Game vs. Microcontroller).
- Utilize native language constructs for encapsulation (e.g., `private`/`protected` in TypeScript) rather than relying on loose naming conventions (e.g., underscore prefixes).

# @Guidelines
- **Context-Aware Design Constraints:**
  - The AI MUST evaluate the context of the project before declaring a pattern "good" or "bad".
  - If the context is **Web Development**, the AI MUST NOT use Anemic Domain Models. Business logic and validation MUST be encapsulated within the Domain Models themselves, not in external "Services" or "Controllers".
  - If the context is **Game Development**, the AI MUST favor an Entity Component System (ECS) where models are anemic and behavior is separated.
  - If the context is **Microcontroller Development**, the AI is permitted to use God Objects if it yields necessary performance increases.
- **Parameter and Method Refactoring:**
  - The AI MUST NOT generate methods with long lists of parameters (the "Too Many Parameters" smell).
  - The AI MUST refactor long parameter lists into configuration objects or domain models.
  - The AI MUST break down large methods into smaller, single-responsibility methods when extracting parameter objects.
- **Language-Specific Conventions:**
  - In TypeScript/Java, the AI MUST use explicit access modifiers (`private`, `protected`) to enforce scope.
  - In TypeScript, the AI MUST NOT use the underscore prefix convention (`_`) to denote private variables; it must use native language constructs.
  - In untyped languages (JavaScript, Python), the AI MAY use the underscore prefix convention.
  - The AI MUST NOT use the `eval()` function in JavaScript/TypeScript due to security risks.
  - The AI MUST NOT use labeled breaks (the JavaScript equivalent of `goto`) as they make code too hard to debug and trace.
- **Anti-Pattern Prevention:**
  - The AI MUST NOT extract business logic into configuration files (preventing the `Soft-code` anti-pattern).
  - The AI MUST NOT create massive interfaces. If an interface requires implementing unrelated attributes, the AI MUST split it into several smaller, single-responsibility interfaces (preventing `Interface Bloat`).
- **DRY vs. Overengineering (The Human-First Rule):**
  - The AI MUST prioritize human readability over the DRY (Do Not Repeat Yourself) principle.
  - The AI MUST NOT overengineer abstractions simply to deduplicate code if the resulting abstraction is difficult to understand. 
  - If repetitive code is easier to understand and change than a heavily abstracted utility, the AI MUST choose the repetitive code.

# @Workflow
1. **Contextual Assessment**: Determine the application domain (Web, Game, Microcontroller) to establish which architectural patterns apply.
2. **Smell Detection**: Scan the provided code for method-level smells (too many parameters, labeled breaks, `eval()`), class-level smells (interface bloat, lazy classes, anemic models), and application-level smells (soft-coding).
3. **Parameter Consolidation**: If a method has 4 or more parameters, wrap them into a designated configuration type/interface.
4. **Encapsulation Verification**: Inspect models for business logic. If a model only has properties and a `Service` class modifies those properties and performs validation, move the validation and modification logic directly into the model class.
5. **Language Construct Enforcement**: Scan for `_` prefixes in TypeScript. Replace them with `private` keywords and remove the underscores.
6. **Readability Check (Overengineering)**: Review abstractions designed to reduce repetition. Ask: "Can a human easily read and modify this without jumping through complex abstractions?" If no, revert to a simpler, slightly repetitive structure.

# @Examples (Do's and Don'ts)

### Parameter Refactoring
**[DON'T]** Pass primitive lists (Too many parameters smell):
```typescript
export class PaymentCalculator {
  public calculatePayment (
    userType: UserType,
    user: User,
    currency: Currency,
    hours: Hours,
    salary: Salary,
    isContractor: boolean,
    isEmployee: boolean,
    isAdmin: boolean
  ): PaymentDetails {
    // ...
  }
}
```

**[DO]** Group parameters into an object (Data clump refactoring):
```typescript
type CalculatePaymentConfig = {
  userType: UserType,
  user: User,
  currency: Currency,
  hours: Hours,
  salary: Salary,
  isContractor: boolean,
  isEmployee: boolean,
  isAdmin: boolean
}

export class PaymentCalculator {
  public calculatePayment (config: CalculatePaymentConfig): PaymentDetails {
    // ...
  }
}
```

### Anemic Domain Models vs. Rich Domain Models (Web Context)
**[DON'T]** Create Anemic Domain Models where services hold the logic:
```typescript
// user.ts (Anemic Model)
export class User {
  public id: string;
  public name: string;
  public email: string;
  constructor (id: string, name: string, email: string) {
    this.id = id;
    this.name = name;
    this.email = email;
  }
}

// userService.ts (Service holds business logic)
export class UserService {
  public createUser (userFields: UserFields): User {
    if (!this.isValidUserName(userFields.name) || !this.isValidEmail(userFields.email)) {
      throw new Error("Invalid fields for user");
    }
    return new User(this.createId(), userFields.name, userFields.email);
  }
}
```

**[DO]** Encapsulate business logic directly inside the domain model:
```typescript
// user.ts (Rich Domain Model)
export class User {
  private id: string;
  private name: string;
  private email: string;

  private constructor (id: string, name: string, email: string) {
    this.id = id;
    this.name = name;
    this.email = email;
  }

  public static create(userFields: UserFields): User {
    if (!User.isValidUserName(userFields.name) || !User.isValidEmail(userFields.email)) {
      throw new Error("Invalid fields for user");
    }
    return new User(User.createId(), userFields.name, userFields.email);
  }
}
```

### Language Conventions (TypeScript)
**[DON'T]** Rely on untyped language conventions in strictly typed languages:
```typescript
class User {
  public _hash: string; // Anti-pattern in TS: Relying on underscore for privacy
  
  constructor() {
    this._hash = createUniqueObjectHash(); 
  }
}
```

**[DO]** Use proper language constructs:
```typescript
class User {
  private hash: string; 
  
  constructor() {
    this.hash = createUniqueObjectHash(); 
  }
}
```

### DRY vs Overengineering (Readability First)
**[DON'T]** Overengineer to perfectly eliminate repetition if it obscures the code's shape and intention:
```javascript
let {top, bottom, left, right} = Directions;

function createHandle(directions) { /* 20 lines of complex logic */ }

let fourCorners = [
  createHandle([top, left]), createHandle([top, right]),
  createHandle([bottom, left]), createHandle([bottom, right]),
];

function createBox(shape, handles) { /* 20 lines of logic */ }

let Rectangle = createBox(Shapes.Rectangle, fourCorners);
```

**[DO]** Accept structural repetition if it guarantees immediate human readability and easy modification:
```javascript
let Rectangle = {
  resizeTopLeft(position, size, preserveAspect, dx, dy) {
    // 10 repetitive lines of math, but trivially easy to read and modify
  },
  resizeTopRight(position, size, preserveAspect, dx, dy) {
    // 10 repetitive lines of math
  },
  resizeBottomLeft(position, size, preserveAspect, dx, dy) {
    // 10 repetitive lines of math
  },
  resizeBottomRight(position, size, preserveAspect, dx, dy) {
    // 10 repetitive lines of math
  }
};
```