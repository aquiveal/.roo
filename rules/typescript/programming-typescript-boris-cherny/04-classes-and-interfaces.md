# @Domain
This rule file is activated whenever the AI is tasked with designing, writing, refactoring, or reviewing object-oriented TypeScript code. This includes the creation of classes, interfaces, inheritance hierarchies, mixins, class decorators, factory patterns, builder patterns, or when mapping domain entities to TypeScript data structures.

# @Vocabulary
*   **Structural Typing (Duck Typing):** TypeScript's method of comparing types by their shape and properties, rather than their explicit names or declarations.
*   **Declaration Merging:** A TypeScript feature where multiple interfaces declared with the same name in the same scope are automatically combined into a single interface.
*   **Mixin:** A function that takes a class constructor and returns a new class constructor, used to simulate multiple inheritance and role-oriented programming.
*   **Constructor Signature:** The syntax `new()` used to structurally type a class constructor, indicating that a type can be instantiated with the `new` operator.
*   **Companion Object Pattern:** A pattern declaring a type (or interface) and a value (usually an object) with the exact same name to group type and value information that is semantically related.
*   **Definite Assignment:** The requirement that class instance variables must be assigned a value either as a property initializer or within the constructor (unless explicitly typed with `| undefined`).

# @Objectives
*   Maximize compile-time safety by enforcing strict structural typing rules for classes and interfaces.
*   Ensure encapsulation and correct API surface exposure using appropriate visibility modifiers (`private`, `protected`, `public`) and `readonly` boundaries.
*   Prevent inheritance and instantiation runtime errors by correctly structuring `abstract` classes, simulating `final` classes, and utilizing `this` as a return type for chainable methods.
*   Implement highly reusable and composable code utilizing typesafe mixins and design patterns (Factory, Builder) without breaking TypeScript's structural abstractions.

# @Guidelines

### Classes and Inheritance Constraints
*   The AI MUST explicitly declare visibility modifiers (`private`, `protected`) for class properties and methods to restrict access boundaries. If no modifier is applied, the property is implicitly `public`.
*   The AI MUST initialize class properties either inline (property initializers) or inside the `constructor`. If a property is intentionally uninitialized, it MUST be typed with `| undefined`.
*   The AI MUST use the `readonly` modifier on class properties that should not be reassigned after their initial assignment in the constructor.
*   The AI MUST use `abstract` classes to prevent direct instantiation of base classes. Abstract classes MUST define `abstract` methods for required subclass implementations while optionally providing default implementations for other methods.
*   The AI MUST ensure that any overridden method in a child class calls its parent counterpart using `super.methodName()`.
*   The AI MUST ensure that a child class's constructor calls `super()` before accessing `this`.
*   The AI MUST NOT attempt to access parent class *properties* using `super`; `super` can only be used to access parent class *methods*.

### The `this` Return Type
*   The AI MUST use `this` as the return type annotation for chainable instance methods instead of hardcoding the class name. This ensures that subclasses inherit chainable methods that correctly return the subclass type rather than the parent class type.

### Interfaces vs. Type Aliases
*   The AI MUST prefer `interface` over `type` aliases when defining shapes (objects).
*   The AI MUST utilize `interface` to take advantage of strict assignability checks when extending (`extends`); type intersections (`&`) silently create overloaded signatures on conflicts rather than throwing compile-time errors.
*   The AI MUST utilize Declaration Merging by using `interface` when defining types that may need to be augmented or merged across multiple files or scopes.
*   The AI MUST NOT use `interface` if the right-hand side of the declaration is not a shape (e.g., union types, primitives).

### Implementing Interfaces vs. Extending Abstract Classes
*   The AI MUST use `interface` as a lightweight construct to enforce that a class satisfies a specific shape at compile time.
*   The AI MUST NOT declare visibility modifiers (`private`, `protected`, `public`) or the `static` keyword inside an `interface`.
*   The AI MUST use `abstract class` instead of `interface` ONLY when the base representation needs to emit runtime JavaScript code, such as providing default method implementations or setting access modifiers.

### Structural Typing Exceptions
*   The AI MUST recognize that classes are structurally typed EXCEPT when they contain `private` or `protected` fields. 
*   If a class contains `private` or `protected` fields, the AI MUST NOT assign a structurally identical object literal to it; it MUST strictly be an instance of that class or its subclasses.

### Classes as Values and Types
*   The AI MUST differentiate between a class used as a type (representing the instance) and a class used as a value (representing the constructor).
*   The AI MUST use `typeof ClassName` when referencing the constructor type of a class.
*   The AI MUST use the `new(...args: any[]) => T` signature when typing a generic class constructor.

### Polymorphism and Generics in Classes
*   The AI MUST scope generic type parameters to the entire class by declaring them at the class level (`class MyMap<K, V>`), NOT on the `constructor` signature.
*   The AI MUST explicitly declare generic type parameters on `static` methods (e.g., `static of<K, V>(k: K, v: V)`). Static methods DO NOT inherit or have access to class-level generic type parameters.

### Mixins
*   To implement a mixin, the AI MUST create a function that takes a class constructor and returns a new anonymous class extending that constructor.
*   The AI MUST type the incoming constructor argument using a generic constructor type: `type ClassConstructor<T> = new(...args: any[]) => T`.
*   The AI MUST use `any[]` (NOT `unknown[]` or `void`) for the rest arguments in the constructor type signature; otherwise, TypeScript will reject the `extends` clause.
*   The AI MUST ensure that the anonymous class's constructor accepts `...args: any[]` and passes them entirely to `super(...args)`.

### Decorators
*   The AI MUST AVOID using class decorators to change the shape of a class (e.g., adding properties or methods). TypeScript does not track shape changes introduced by decorators at compile time, leading to `Property does not exist` errors.
*   If shape modification is required, the AI MUST use standard function wrappers or mixins instead of decorators.

### Simulating Final Classes
*   To simulate a `final` class (a class that cannot be extended or directly instantiated via `new`), the AI MUST mark the `constructor` as `private`.
*   The AI MUST provide a `static` factory method (e.g., `static create()`) to allow instantiation of the simulated `final` class.

### Design Patterns
*   **Factory Pattern:** The AI MUST implement the Factory pattern by utilizing the Companion Object Pattern (a value and a type with the same name) and using string literal union types to restrict factory inputs safely.
*   **Builder Pattern:** The AI MUST implement the Builder pattern by defining private instance variables initialized to default values (or `null`), and providing mutator methods that return `this` to allow safe chaining.

# @Workflow
1.  **Analyze Domain Requirements:** Determine if the domain entities require runtime logic sharing (Abstract Class), strict shape enforcement (Interface), or compositional behavior (Mixins).
2.  **Define Shapes and Boundaries:** Create `interface` definitions for all complex object shapes. Utilize declaration merging if extending third-party or global interfaces.
3.  **Implement Class Structures:** Create classes implementing the defined interfaces. Assign `private`, `protected`, and `readonly` modifiers to encapsulate internal state.
4.  **Resolve Generic Scoping:** Apply generic type parameters to classes. Ensure that any `static` methods within generic classes define their own independent generic parameters.
5.  **Enable Composability:** For shared behaviors spanning unrelated class hierarchies, implement Typesafe Mixins returning anonymous extended classes.
6.  **Enforce Instantiation Rules:** If a class must not be subclassed, apply a `private constructor` and expose a `static` factory method. If a base class must not be instantiated, mark it as `abstract`.

# @Examples (Do's and Don'ts)

### Chainable Methods (`this` return type)
**[DO]**
```typescript
class Set {
  has(value: number): boolean { /*...*/ return false; }
  add(value: number): this {
    // ...
    return this;
  }
}

class MutableSet extends Set {
  delete(value: number): boolean { /*...*/ return true; }
}
// MutableSet.add() now correctly returns MutableSet
```

**[DON'T]**
```typescript
class Set {
  add(value: number): Set { // Anti-pattern: hardcoding class name
    // ...
    return this;
  }
}
class MutableSet extends Set {
  // Now MutableSet has to redundantly override add() just to fix the return type
  add(value: number): MutableSet {
    super.add(value);
    return this;
  }
}
```

### Static Methods and Generics
**[DO]**
```typescript
class MyMap<K, V> {
  // Static method defines its own generics
  static of<K1, V1>(k: K1, v: V1): MyMap<K1, V1> {
    return new MyMap(k, v);
  }
}
```

**[DON'T]**
```typescript
class MyMap<K, V> {
  // Anti-pattern: Attempting to access class-level generics in a static method
  static of(k: K, v: V): MyMap<K, V> {
    return new MyMap(k, v);
  }
}
```

### Mixin Signatures
**[DO]**
```typescript
type ClassConstructor<T = {}> = new(...args: any[]) => T;

function withEZDebug<C extends ClassConstructor<{ getDebugValue(): object }>>(Class: C) {
  return class extends Class {
    constructor(...args: any[]) {
      super(...args);
    }
    debug() {
      return this.getDebugValue();
    }
  }
}
```

**[DON'T]**
```typescript
// Anti-pattern: using unknown[] prevents TypeScript from allowing the `extends` keyword
type ClassConstructor<T = {}> = new(...args: unknown[]) => T;

function withEZDebug<C extends ClassConstructor>(Class: C) {
  return class extends Class { /* ... */ } // TS Error
}
```

### Simulating Final Classes
**[DO]**
```typescript
class MessageQueue {
  private constructor(private messages: string[]) {}
  
  static create(messages: string[]) {
    return new MessageQueue(messages);
  }
}
```

**[DON'T]**
```typescript
class MessageQueue {
  // Anti-pattern: leaving constructor public means it can be subclassed
  constructor(private messages: string[]) {}
}
class BadQueue extends MessageQueue {} // Undesired extension allowed
```

### Interface vs Type Alias for Shapes
**[DO]**
```typescript
interface Food {
  calories: number;
  tasty: boolean;
}

interface Sushi extends Food {
  salty: boolean;
}
// TS will strictly check assignability of Sushi to Food
```

**[DON'T]**
```typescript
type Food = {
  calories: number;
  tasty: boolean;
}

type Sushi = Food & {
  salty: boolean;
}
// Anti-pattern: intersection blindly combines types, masking conflicting property errors
```

### Altering Shape with Decorators
**[DO]**
```typescript
// Use a standard function wrapper (or mixin) to alter a class shape
function serializable<T extends ClassConstructor>(Constructor: T) {
  return class extends Constructor {
    serialize() {
      return JSON.stringify(this);
    }
  }
}
let DecoratedPayload = serializable(APIPayload);
new DecoratedPayload().serialize(); // Fully typesafe
```

**[DON'T]**
```typescript
@serializable
class APIPayload {
  getValue() { return "payload"; }
}

let payload = new APIPayload();
payload.serialize(); // TS Error: Property 'serialize' does not exist on type 'APIPayload'
```