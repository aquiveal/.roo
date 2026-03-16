# @Domain
Trigger these rules when writing, refactoring, or reviewing TypeScript/JavaScript code, specifically when dealing with variable declarations, function signatures, class architectures, domain modeling, interface design, or migrating dynamically typed JavaScript to statically typed TypeScript. 

# @Vocabulary
- **Static Typing**: A language feature where variable types are explicitly declared and checked at compile time, preventing runtime assignment errors.
- **Dynamic Typing**: A language feature where types are inferred and checked at runtime.
- **Strong (Strict) Typing**: A compiler rule set that rejects automatic type coercion (e.g., throwing an error when adding a string and an integer).
- **Weak Typing**: A compiler rule set that automatically coerces (converts) conflicting types.
- **Type Coercion**: The automatic or implicit conversion of values from one data type to another.
- **Concretion**: A concrete implementation of an object instantiated using the `new` keyword. 
- **Abstraction**: Defining the contract or intent of code separately from its implementation, typically using `interface` or `abstract class`.
- **Polish Postfix Notation**: The syntax used in TypeScript where the type follows the variable or function (e.g., `variable: type` or `function(): type`).
- **Nominal Typing**: A type system where compatibility is determined by explicit declarations or subclassing (e.g., Java).
- **Duck Typing (Structural Typing)**: A type system where compatibility is determined by the actual structure (shape) of the object rather than its explicit class name.
- **Ambient Types**: Declaration files (often `.d.ts`) used to provide type safety and code intelligence for existing, untyped JavaScript libraries.
- **Value Object**: A domain-specific type that wraps primitive values to enforce validation and make implicit constraints explicit.

# @Objectives
- Eliminate runtime type errors and unpredictable states by enforcing strict compile-time contracts.
- Separate intent from implementation to enable Dependency Inversion, Inversion of Control, and testable plugin architectures.
- Enforce strict instantiation policies that make it impossible to create objects in an illegal state.
- Eradicate "primitive obsession" (string-ly typed code) by making implicit domain concepts explicit through custom types and Value Objects.
- Leverage TypeScript's structural typing (Duck Typing) to maximize flexibility while maintaining type safety.
- Communicate design intent entirely through language constraints (modifiers, abstract keywords) rather than through documentation or naming conventions.

# @Guidelines
- **Enforce Static Contracts**: The AI MUST explicitly declare types for variables, function parameters, and return types using Polish postfix notation (`name: type`).
- **Prevent Type Coercion**: The AI MUST treat TypeScript as a strongly typed language. NEVER rely on implicit type coercion. Always explicitly cast or convert types when mixing strings, numbers, or booleans.
- **Separate Intent from Implementation**: The AI MUST define contracts using `interface` or `abstract class` before writing the concrete implementation. Concrete classes MUST implement or extend these abstractions.
- **Communicate Design Intent Structurally**: The AI MUST use explicit language features (`private`, `protected`, `public`, `abstract`, `readonly`) to define scope and behavior instead of relying on conventions like underscore prefixes (e.g., `_privateVar`) or runtime checks.
- **Enforce Creation Policy**: The AI MUST prevent partial or invalid object creation. Use constructors or `public static create()` factory methods to demand all required dependencies upfront. If a required parameter is missing, the compiler MUST flag it.
- **Make the Implicit Explicit (Avoid Primitives)**: The AI MUST NOT use primitive types (`string`, `number`) to represent complex domain concepts. Create specific Domain Types or Value Objects (e.g., `class EmailAddress`) to encapsulate primitive values and their validation logic.
- **Embrace Duck Typing**: The AI MUST design functions and methods to accept interfaces defining the required structural shape, rather than requiring instances of specific concrete classes. 
- **Declare Ambient Types**: When integrating third-party JavaScript libraries without native types, the AI MUST provide or install ambient type declarations (`.d.ts` files) to maintain absolute type safety.
- **Use Implicit Typing Safely**: The AI MAY omit explicit type annotations ONLY for simple, localized variable initializations where the compiler can completely and safely infer the primitive type (e.g., `const age = 13;`), but MUST use explicit types for all boundaries (parameters, return types, class properties).

# @Workflow
1. **Analyze the Data Flow**: Identify the inputs, outputs, and domain models required for the task.
2. **Define the Abstraction**: Write the `interface` or `abstract class` representing the required behavior before writing any concrete logic.
3. **Identify Domain Primitives**: Scan the required data for primitive types that carry business rules (e.g., passwords, emails, URLs). Wrap these immediately in custom Value Object classes.
4. **Draft the Implementation**: Implement the abstraction in a concrete class. 
5. **Apply Access Modifiers**: Mark internal states as `private` or `protected`. Apply `readonly` to immutable properties.
6. **Enforce Policy**: Write a constructor or a static factory method that accepts strictly typed arguments (using the Value Objects created in Step 3). 
7. **Verify Structural Compatibility**: Ensure that functions consuming these objects rely on the structural interfaces (Duck Typing) rather than the concrete class names.
8. **Check Boundaries**: Ensure all function signatures and class properties have explicit Polish postfix type annotations. 

# @Examples (Do's and Don'ts)

## Abstraction & Communicating Intent
- **[DO]** Use `abstract` classes and interfaces to define contracts and require subclass implementation.
```typescript
abstract class AudioDevice {
  protected isPlaying: boolean = false;
  
  play(): void {
    this.isPlaying = true;
    this.handlePlayCurrentAudioTrack();
  }
  
  abstract handlePlayCurrentAudioTrack(): void;
}

class Boombox extends AudioDevice {
  handlePlayCurrentAudioTrack(): void {
    // Play through speakers
  }
}
```
- **[DON'T]** Rely on runtime errors to enforce subclass implementation.
```javascript
class AudioDevice {
  handlePlayCurrentAudioTrack() {
    throw new Error('Subclass responsibility error');
  }
}
```

## Making the Implicit Explicit (Primitive Obsession)
- **[DO]** Wrap domain concepts in Value Objects with static factory methods to enforce validation.
```typescript
class EmailAddress {
  private constructor(public readonly value: string) {}

  public static create(email: string): EmailAddress {
    if (!email.includes('@')) throw new Error("Invalid email");
    return new EmailAddress(email);
  }
}

function createUser(email: EmailAddress, password: Password): User { ... }
```
- **[DON'T]** Use primitive strings for domain values, which allows invalid states.
```typescript
function createUser(email: string, password: string): User { ... }
// This compiles but is a domain error:
createUser("", ""); 
```

## Enforcing Policy
- **[DO]** Require all necessary properties at instantiation.
```typescript
function createMessage(from: string, to: string, text: string): Message { ... }
const msg = createMessage('khalil', 'bill', 'hello');
```
- **[DON'T]** Allow empty or partial instantiation that leads to unpredictable states.
```typescript
const msg = new Message();
msg.from = 'khalil';
// Missing 'to' and 'text', putting the object in an illegal state
```

## Duck Typing (Structural Types)
- **[DO]** Rely on the structural shape of objects for compatibility.
```typescript
interface Comment {
  id: number;
  name: string;
  content: string;
}

function postComment(comment: Comment): void { ... }

// Accepts any object matching the structure, even if it has extra fields (Reply)
postComment({ id: 2, name: 'Don', content: 'Yes', parentCommentId: 1 });
```
- **[DON'T]** Force strict nominal type checking when structure suffices, or manually check object shapes at runtime.
```javascript
function postComment(comment) {
  if (!comment.hasOwnProperty('id') || isNaN(comment.id)) throw new Error();
  if (typeof comment.name !== "string") throw new Error();
}
```