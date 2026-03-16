# @Domain
These rules MUST be triggered whenever the AI is tasked with generating new code, refactoring existing code, conducting code reviews, establishing project scaffolding, or designing internal/external APIs (including classes, functions, and modules). They activate specifically when the user requests "clean code" implementations, architectural simplification, or improvements to code maintainability, readability, and developer experience.

# @Vocabulary
- **Clean Code**: Code that serves the needs of users and can be cost-effectively changed by developers. It is easy to read, reveals its intended purpose without obfuscation, tells a story about the domain, and is highly testable.
- **Coding Standard (Coding Conventions)**: A collection of rules that pushes code toward a consistent style and approach across a codebase to reduce cognitive load and promote reuse.
- **Simple Design**: A hierarchy of design rules popularized by Extreme Programming (XP). Code must: 1) Run all tests, 2) Contain no duplication, 3) Maximize clarity, 4) Have fewer elements.
- **Emergent Design**: The practice of allowing design decisions and structures to gradually emerge through short feedback loops (like Test-Driven Development and refactoring) rather than relying on Big Design Up Front (BDUF).
- **Structure**: The rules, architectural boundaries, and constraints enforced within a codebase (e.g., Object-Oriented Programming principles, strict typing).
- **Developer Experience (DX)**: The measure of how easily and intuitively a developer can navigate, understand, and safely modify a codebase or API. High DX means a low learning curve and high discoverability.
- **API (Application Programming Interface)**: Any code intended to be used by another developer. This includes public interfaces to abstractions, utility libraries, classes, and exported functions—not just HTTP/REST URLs.
- **Leaky Abstraction**: A poorly designed abstraction that forces the consuming developer to learn its internal details to use it correctly (e.g., remembering to call an initialization method after instantiation).
- **Partial Object Creation**: An anti-pattern where an object is instantiated but is not fully ready to be used until subsequent methods are called.

# @Objectives
- Optimize all code for human understandability; human time is the primary cost of software ownership.
- Eliminate the need for comments by writing code that acts as clear, declarative documentation of its own intent.
- Ensure that every introduced abstraction is fully justified by the rules of Simple Design (Tests -> Deduplication -> Clarity -> Minimization).
- Treat all internal classes, modules, and functions as APIs, designing them to prevent misuse and provide a flawless Developer Experience.
- Balance strict structural rules (to maintain codebase integrity) with high Developer Experience (to keep developers productive).

# @Guidelines

## Clean Code & Understandability
- **Optimize for Humans**: The AI MUST optimize code for human understandability over machine efficiency or developer cleverness. 
- **Self-Explanatory Intent**: The AI MUST write code that reveals its intended purpose natively. If the code requires a comment to explain *how* or *why* it works, the AI MUST refactor the code to be clearer instead of leaving the comment.
- **Domain Metaphor**: The AI MUST use a clear and consistent domain language that tells a story about the business problem being solved.

## Consistency and Coding Standards
- **Enforce Consistency**: The AI MUST identify and adhere strictly to the established coding standard of the project. If no standard exists, the AI MUST establish and apply one uniformly.
- **Reduce Cognitive Load**: The AI MUST prioritize consistency to reduce cognitive load, avoiding varying methods of accomplishing the exact same task within the same codebase.

## Simple Design Constraints
- **Test-Driven Priority**: The AI MUST assume or ensure that code passes all tests before considering it complete.
- **Eradicate Duplication**: The AI MUST actively identify duplicated logic and extract it into appropriate abstractions.
- **Maximize Clarity**: The AI MUST rename variables, functions, and classes to maximize expressiveness immediately after removing duplication.
- **Minimize Elements**: The AI MUST NOT introduce unnecessary design patterns, classes, or layers. Abstractions MUST be justified by duplication removal or clarity enhancement.

## Internal API Design & Developer Experience (DX)
- **Treat Everything as an API**: The AI MUST design every exported function, class, or module with the consuming developer in mind.
- **Prevent Leaky Abstractions**: The AI MUST expose public interfaces that are intuitive and hide complex internal machinations.
- **Enforce State via Constructors**: The AI MUST avoid partial object creation. Required dependencies and configuration MUST be injected via constructors or static factory methods, absolutely forbidding the requirement of secondary `.initialize()` or `.setup()` methods.
- **Balance Structure and DX**: When using highly structured paradigms (like Object-Oriented Programming), the AI MUST ensure the structure does not degrade DX. When using highly flexible paradigms (like Functional Programming or React), the AI MUST introduce targeted structure (like TypeScript interfaces) to ensure maintainability.

## Emergent Design
- **No Ivory Tower Architecture**: The AI MUST NOT generate massive, speculative architectural boilerplate upfront.
- **Step-by-Step Evolution**: The AI MUST solve the immediate problem simply, then refactor to introduce structure only as the code demands it based on the Simple Design rules.

# @Workflow
1. **Goal Verification**: Identify the precise functional requirement or business rule to be implemented.
2. **Implementation (Runs Tests)**: Write the simplest possible code to achieve the goal (or make the test pass). Do not introduce preemptive abstractions.
3. **Deduplication Analysis (No Duplication)**: Scan the newly written code and the surrounding context. If logic is duplicated, extract it into a dedicated function or class.
4. **Clarity Pass (Maximizes Clarity)**: Review all names (variables, methods, classes). Rename them to ensure they speak the domain language and eliminate the need for explanatory comments.
5. **Element Minimization (Fewer Elements)**: Review the structural footprint. If a design pattern or class was created that does not strictly remove duplication or improve clarity, delete it and revert to a simpler implementation.
6. **DX & API Audit**: Evaluate the newly created interfaces as a consumer. 
    - Can the object be instantiated in an invalid state? If yes, move required fields to the constructor.
    - Does the consumer need to know internal details to use it? If yes, encapsulate those details.

# @Examples (Do's and Don'ts)

## Internal API Design (Preventing Partial Object Creation)
- **[DON'T]** Create classes that require the consumer to manually initialize them after instantiation (Leaky Abstraction / Poor DX).
```typescript
class UsersService extends HTTPService {
  public getUsers () {
    return this.http.get<User[]>("/users");
  }
}

// Consumer code (Error-prone DX)
const usersService = new UsersService();
// If the developer forgets this next line, the API breaks at runtime.
usersService.initialize("http://movies.com/api"); 
usersService.getUsers(); 
```
- **[DO]** Enforce object completeness and structural constraints via the constructor.
```typescript
class HTTPService {
  http: AxiosInstance;
  // The subclass/consumer is FORCED to provide the baseURL
  constructor (baseURL: string) {
    this.http = axios.create({ baseURL });
  }
}

class UsersService extends HTTPService {
  constructor(baseURL: string) {
    super(baseURL);
  }
  public getUsers () {
    return this.http.get<User[]>("/users");
  }
}

// Consumer code (Flawless DX)
const usersService = new UsersService("http://movies.com/api");
usersService.getUsers(); // Works immediately, impossible to get wrong.
```

## Self-Explanatory Code vs. Comments
- **[DON'T]** Write complex, obscure code and attempt to fix it by adding a comment (Cory House's rule: "Code is like humor. When you have to explain it, it's bad").
```typescript
// Check if the user is old enough and has an active subscription
if (u.age >= 18 && u.subStatus === 'ACTIVE' && u.paymentDef === false) {
  grantAccess();
}
```
- **[DO]** Refactor the code to maximize clarity and speak the domain language, removing the need for the comment.
```typescript
const isAdult = user.age >= 18;
const hasActiveSubscription = user.subscriptionStatus === 'ACTIVE';
const isPaymentUpToDate = user.hasPaymentDefault === false;

if (isAdult && hasActiveSubscription && isPaymentUpToDate) {
  grantAccess();
}
```