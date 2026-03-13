# @Domain
These rules activate whenever the AI is writing, refactoring, typechecking, or reviewing TypeScript functions, including function signatures, callbacks, generators, iterators, overloaded functions, and polymorphic (generic) functions.

# @Vocabulary
- **Parameter (Formal Parameter)**: A piece of data a function needs to run, declared as part of the function declaration.
- **Argument (Actual Parameter)**: A piece of data passed to a function when invoking it.
- **Call Signature / Type Signature**: TypeScript syntax representing a function's type, consisting exclusively of type-level code (e.g., `(a: number, b: number) => number`).
- **Type-Level Code**: Code consisting exclusively of types and type operators.
- **Value-Level Code**: Standard JavaScript runtime code.
- **Contextual Typing**: TypeScript's ability to infer types from the context in which a function is used (e.g., inline callbacks).
- **Overloaded Function**: A function with multiple call signatures but a single combined implementation signature.
- **Generic Type Parameter (Polymorphic Type Parameter)**: A placeholder type (`<T>`) used to enforce a type-level constraint in multiple places.
- **Bounded Polymorphism**: Using the `extends` keyword (`<T extends U>`) to constrain a generic type parameter to a specific upper bound.
- **Iterable**: An object containing a `Symbol.iterator` property that returns an iterator.
- **Iterator**: An object defining a `next` method that returns an object with `value` and `done` properties.

# @Objectives
- Enforce absolute type safety for all function inputs and outputs.
- Eliminate unsafe legacy JavaScript patterns (`arguments` object, untyped `this`, the `Function` constructor).
- Utilize TypeScript's inference mechanisms (contextual typing) to avoid redundant annotations.
- Model dynamic JavaScript behaviors safely using overloaded signatures and bounded polymorphism.
- Practice Type-Driven Development: define function type signatures before writing implementations.

# @Guidelines

## Function Declarations & Parameters
- **NEVER** use the `Function` constructor (`new Function(...)`). It is completely unsafe and untyped.
- **MUST** explicitly annotate function parameters unless they are contextually typed (e.g., inline callbacks).
- **MAY** leave return types unannotated to let TypeScript infer them, EXCEPT when creating standalone call signatures or when an explicit return type aids readability.
- **MUST** place required parameters before optional parameters (`?`).
- **MUST** omit the optional `?` modifier when providing a default parameter value (`=`). Let TypeScript infer the type from the default value.

## Rest Parameters vs. `arguments`
- **NEVER** use the magic `arguments` object. It is typed as `any` and bypasses type safety.
- **MUST** use safely typed rest parameters (`...args: T[]`) to model variadic functions.
- **MUST** place the rest parameter at the absolute end of the parameter list.

## Typing `this`
- **MUST** explicitly declare the expected `this` type as the function's very first parameter if the function relies on a specific `this` context.
- **MUST NOT** use `this` dynamically without an explicit annotation (assumes `noImplicitThis` is enabled).

## Generators and Iterators
- **MUST** type generator functions (`function*`) as returning an `IterableIterator<T>`.
- **MAY** let TypeScript infer the `IterableIterator<T>` type from the `yield` statements.
- **CAUTION**: If advising on `downlevelIteration` in `tsconfig.json` for ES5 targets, warn the user that custom iterators generate significantly larger bundle sizes.

## Call Signatures (Type-Level Functions)
- **MUST NOT** use the `Function` type as a catchall. Always use specific call signatures (`(...args: T[]) => U`).
- **MUST** explicitly annotate return types in call signatures (cannot be inferred because there is no function body).
- **MUST NOT** include default values in call signatures (defaults are value-level, not type-level).

## Overloaded Functions
- **MUST** declare all specific call signatures first, followed by a single combined implementation signature.
- **MUST** make the implementation signature broad enough to satisfy all overloads.
- **MUST NOT** make the implementation signature overly broad (e.g., using `any`). Keep types as narrow/specific as possible (e.g., `Date | string`) to enforce strict checking within the function body.
- **MUST** prove to TypeScript which specific overload was invoked within the implementation body using type narrowing/refinement.
- **REMEMBER**: The combined implementation signature is hidden from the caller. Callers can only see the specific overload signatures.

## Polymorphism and Generics
- **MUST** use generics to model relationships between inputs and outputs instead of using `any` or overly broad unions.
- **MUST** explicitly annotate generic types as "all-or-nothing" if TypeScript cannot infer them; you cannot explicitly annotate just one generic and leave another to be inferred.
- **MUST** use uppercase single-letter names (`T`, `U`, `V`) for generic parameters, or descriptive PascalCase names (e.g., `WidgetType`) if there are many complex generics.
- **MUST** use **Bounded Polymorphism** (`<T extends BaseNode>`) when a function needs to return the exact specific subtype it was passed, rather than returning the generalized base type.
- **MAY** use multiple constraints on a generic by extending an intersection type (`<T extends HasSides & SidesHaveLength>`).
- **MUST** place generic types with defaults (`<T = DefaultType>`) strictly *after* generic types without defaults.

# @Workflow
When tasked with creating or heavily modifying a complex function, the AI MUST follow this **Type-Driven Development** process:
1. **Define the Call Signature**: Sketch out the function's signature strictly at the type-level (`type MyFunc = ...`).
2. **Apply Constraints**: Introduce Generics and Bounded Polymorphism to relate inputs to outputs. Ensure edge cases are handled in the signature.
3. **Implement**: Write the value-level implementation, using type narrowing to satisfy the TypeScript compiler.
4. **Refine**: Ensure parameters don't have redundant annotations if contextual typing can infer them. Remove `any` and replace with `unknown` or a generic constraint.

# @Examples (Do's and Don'ts)

### Variadic Functions
- **[DON'T]** Use the `arguments` object.
```typescript
function sumVariadic(): number {
  return Array.from(arguments).reduce((total, n) => total + n, 0)
}
```
- **[DO]** Use safely typed rest parameters.
```typescript
function sumVariadicSafe(...numbers: number[]): number {
  return numbers.reduce((total, n) => total + n, 0)
}
```

### Typing `this`
- **[DON'T]** Leave `this` untyped in standalone functions.
```typescript
function fancyDate() {
  return `${this.getDate()}/${this.getMonth()}` // Unsafe
}
```
- **[DO]** Declare `this` as the first parameter.
```typescript
function fancyDate(this: Date) {
  return `${this.getDate()}/${this.getMonth()}` // Safe
}
```

### Overloaded Functions
- **[DON'T]** Expose the combined signature to the caller or use `any` unnecessarily in the implementation.
```typescript
type Reserve = {
  (from: Date, to: Date, destination: string): Reservation
  (from: Date, destination: string): Reservation
  (from: Date, toOrDest: Date | string, dest?: string): Reservation // BAD: Leaks to caller
}
```
- **[DO]** Keep the implementation signature hidden and use narrow union types.
```typescript
type Reserve = {
  (from: Date, to: Date, destination: string): Reservation
  (from: Date, destination: string): Reservation
}

let reserve: Reserve = (
  from: Date,
  toOrDestination: Date | string, // DO: Use specific unions, not 'any'
  destination?: string
) => {
  if (toOrDestination instanceof Date && destination !== undefined) {
    // Round trip
  } else if (typeof toOrDestination === 'string') {
    // One-way trip
  }
}
```

### Bounded Polymorphism
- **[DON'T]** Map over a subtype but return the generic base type (losing type information).
```typescript
function mapNode(node: TreeNode, f: (value: string) => string): TreeNode {
  return { ...node, value: f(node.value) } 
  // If passed a LeafNode, it returns a TreeNode. Type info is lost!
}
```
- **[DO]** Use a generic bounded parameter to preserve the exact input subtype.
```typescript
function mapNode<T extends TreeNode>(node: T, f: (value: string) => string): T {
  return { ...node, value: f(node.value) }
  // If passed a LeafNode, it safely returns a LeafNode.
}
```

### Generic Defaults and Ordering
- **[DON'T]** Place a generic with a default before a required generic.
```typescript
type MyEvent<Target extends HTMLElement = HTMLElement, Type extends string> = { ... } // ERROR
```
- **[DO]** Place generics with defaults at the end of the type parameter list.
```typescript
type MyEvent<Type extends string, Target extends HTMLElement = HTMLElement> = {
  target: Target
  type: Type
}
```

### Call Signatures
- **[DON'T]** Use the generic `Function` type to describe a callback.
```typescript
function process(callback: Function) { ... }
```
- **[DO]** Use a precise call signature.
```typescript
function process(callback: (index: number) => void) { ... }
```