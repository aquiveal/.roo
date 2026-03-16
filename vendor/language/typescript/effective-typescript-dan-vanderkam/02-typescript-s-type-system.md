# @Domain
These rules MUST be activated whenever the AI is writing, refactoring, debugging, or documenting TypeScript code (`.ts`, `.tsx`, `.d.ts` files), or when a user requests assistance with TypeScript type definitions, interfaces, generics, or type-checking errors.

# @Vocabulary
- **Type Space**: The context in a TypeScript AST where symbols represent types (e.g., after a colon `:`, after an `as` keyword, or in type arguments `<T>`). These symbols are erased at runtime.
- **Value Space**: The context in a TypeScript AST where symbols represent runtime values (e.g., after an equals sign `=`, or in `return` statements).
- **Domain (of a Type)**: The set of all possible runtime values that conform to a specific type.
- **Assignability**: A strict subset relationship. Type A is assignable to Type B if and only if the domain of A is a subset of the domain of B.
- **Bottom Type (`never`)**: The empty set. A type with no values.
- **Top Type (`unknown`)**: The universal set. A type containing all possible values.
- **Unit Type**: A literal type containing exactly one value (e.g., `"A"`, `12`).
- **Structural Typing (Duck Typing)**: TypeScript's default compatibility method where assignability is determined by the shape (properties and methods) of a type, not its explicit declaration or name.
- **Excess Property Checking**: A strictness mechanism triggered specifically when assigning fresh object literals to a typed variable, which flags properties that exist in the literal but not in the target type.
- **Declaration Merging**: A feature unique to `interface` (and `namespace`) where multiple definitions of the same name in the same scope are merged into a single definition.
- **Tagged/Discriminated Union**: A union of object types that share a common literal property (the "discriminant" or "tag"), used to narrow the type via control flow analysis.

# @Objectives
- Maximize type safety by aligning the AI's mental model of TypeScript types with set theory (types as sets of values).
- Enforce clear boundaries between Type Space and Value Space to prevent syntax and conceptual errors.
- Prefer compile-time structural guarantees and explicit annotations over runtime hacks or unsafe assertions.
- Adhere strictly to the DRY (Don't Repeat Yourself) principle at the type level by deriving types via type operations.
- Protect data integrity by heavily utilizing immutability (`readonly`) in function signatures.

# @Guidelines

## Type vs. Value Space Separation
- When reading or writing TypeScript, the AI MUST explicitly distinguish between Type Space and Value Space. 
- The AI MUST NOT use value-space `typeof` (which evaluates to one of 8 runtime string values) when a type-space `typeof` (which extracts a TypeScript type) is intended.
- The AI MUST NOT conflate type annotations with object destructuring. When destructuring a parameter, the AI MUST format the type annotation after the entire destructuring pattern, NEVER inside it.

## Type Assignability and Set Theory
- The AI MUST evaluate type compatibility by treating types as sets. When evaluating if `A` is assignable to `B`, the AI MUST ensure that the domain of `A` is a subset of the domain of `B`.
- The AI MUST recognize that structural typing means an object type is open; it may contain additional properties at runtime. 
- The AI MUST NOT assume that the intersection of two object types (`A & B`) results in `never` just because they share no keys. The resulting domain contains objects possessing the properties of both `A` and `B`.

## Annotations over Assertions
- The AI MUST prefer Type Annotations (`const x: Type = y`) over Type Assertions (`const x = y as Type`). 
- The AI MUST use Type Annotations to trigger Excess Property Checking when assigning object literals.
- The AI MUST restrict the use of Type Assertions to scenarios where the AI possesses context impossible for the TS compiler to know (e.g., specific DOM element querying).
- The AI MUST NOT use the non-null assertion operator (`!`) unless logically guaranteed; prefer type narrowing (e.g., `if (x)` or `?.`).

## Primitive Types
- The AI MUST NOT use object wrapper types (`String`, `Number`, `Boolean`, `Symbol`, `BigInt`) as type annotations. 
- The AI MUST strictly use primitive types (`string`, `number`, `boolean`, `symbol`, `bigint`).

## Interfaces vs. Type Aliases
- The AI MUST default to using `interface` when defining object shapes, particularly for public APIs or when extensibility (Declaration Merging) is desired.
- The AI MUST use `type` aliases for unions, intersections, tuples, and complex type mapping (mapped types, conditional types).

## Function Expressions and Signatures
- When defining multiple functions with the same signature, or when providing a callback, the AI MUST define a standalone function type and apply it to the entire function expression (e.g., `const fn: FnType = ...`) rather than typing individual parameters and return values repeatedly.
- The AI MUST use `typeof fn` to match an existing function's signature.
- The AI MUST use `Parameters<typeof fn>` and `ReturnType<typeof fn>` to extract parts of a signature when creating adapted functions.

## Immutability via `readonly`
- When a function accepts arrays or objects that it does not mutate, the AI MUST annotate those parameters with `readonly` (for arrays/tuples) or `Readonly<T>` (for objects).
- The AI MUST recognize that `readonly` is shallow.
- The AI MUST remember that mutable types are assignable to `readonly` types, but `readonly` types are NOT assignable to mutable types.

## DRY Type Operations
- The AI MUST NOT duplicate property definitions across multiple types or interfaces.
- The AI MUST use utility types like `Pick`, `Omit`, `Partial`, and `Required` to derive variations of a base type.
- The AI MUST use Mapped Types (`[K in keyof T]`) to dynamically generate types based on the keys of other types.
- The AI MUST use `typeof VALUE` to derive a type from a constant configuration object or default state, making the value the single source of truth.

## Index Signatures Strictness
- The AI MUST NOT use broad string index signatures (e.g., `[key: string]: string`) if the object's keys are known.
- If keys are dynamic but constrained, the AI MUST prefer `Record<K, V>`, mapped types, or `Map<K, V>`.
- The AI MUST NOT use numeric index signatures (`[key: number]: T`). To represent numerically indexed collections, the AI MUST use `Array<T>`, `[T, T]`, `ArrayLike<T>`, or `Iterable<T>`.

# @Workflow
When tasked with creating or refactoring TypeScript code, the AI MUST execute the following algorithm:
1. **Analyze the Domain:** Determine the set of valid runtime states for the data structures being manipulated.
2. **Define Base Types:** Create `interface` declarations for core object shapes. Ensure these types represent sealed, valid states.
3. **Derive Variants:** If partial, omitted, or picked versions of the base types are needed, generate them using TS utility types (`Pick`, `Omit`, `Partial`) rather than duplicating code.
4. **Enforce Immutability:** Inspect all functions that consume these types. If a function only reads the data, wrap the parameter type in `Readonly<T>` or `readonly T[]`.
5. **Apply Function Types:** If writing function expressions or callbacks, declare the signature as a `type` and apply it to the expression as a whole.
6. **Validate Literal Assignments:** Ensure initializations of objects use explicit Type Annotations (`: Type`) rather than assertions to trigger Excess Property Checking.

# @Examples (Do's and Don'ts)

## Distinguishing Type Space from Value Space in Destructuring
- [DON'T] Conflate value destructuring with type annotations:
  ```typescript
  function sendEmail({ to: Person, subject: string }) { // ERROR: Renames 'to' to 'Person' and 'subject' to 'string'
      // ...
  }
  ```
- [DO] Separate the destructuring pattern from the type annotation:
  ```typescript
  function sendEmail({ to, subject }: { to: Person, subject: string }) {
      // ...
  }
  ```

## Type Annotations vs. Type Assertions
- [DON'T] Use assertions to assign object literals, which bypasses excess property checks:
  ```typescript
  interface Person { name: string; }
  const alice = { name: 'Alice', occupation: 'Developer' } as Person; // No error flagged
  ```
- [DO] Use explicit annotations to catch excess properties:
  ```typescript
  interface Person { name: string; }
  const alice: Person = { name: 'Alice', occupation: 'Developer' }; // TS flags error: 'occupation' does not exist
  ```

## Primitive Wrapper Types
- [DON'T] Use capitalized wrapper objects for types:
  ```typescript
  function getStringLen(str: String): Number {
      return str.length;
  }
  ```
- [DO] Use lowercase primitive types:
  ```typescript
  function getStringLen(str: string): number {
      return str.length;
  }
  ```

## Typing Function Expressions
- [DON'T] Repeat parameter and return types on multiple similar functions:
  ```typescript
  const add = (a: number, b: number): number => a + b;
  const sub = (a: number, b: number): number => a - b;
  const mul = (a: number, b: number): number => a * b;
  ```
- [DO] Define a function type and apply it to the expressions:
  ```typescript
  type BinaryFn = (a: number, b: number) => number;
  const add: BinaryFn = (a, b) => a + b;
  const sub: BinaryFn = (a, b) => a - b;
  const mul: BinaryFn = (a, b) => a * b;
  ```

## Using `readonly` to Prevent Mutation Errors
- [DON'T] Accept mutable arrays if the function does not mutate them:
  ```typescript
  function arraySum(arr: number[]): number {
      return arr.reduce((sum, num) => sum + num, 0);
  }
  ```
- [DO] Use `readonly` to enforce safety and broaden assignability:
  ```typescript
  function arraySum(arr: readonly number[]): number {
      return arr.reduce((sum, num) => sum + num, 0);
  }
  ```

## DRY Type Operations
- [DON'T] Duplicate properties when creating related types:
  ```typescript
  interface State { userId: string; pageTitle: string; recentFiles: string[]; pageContents: string; }
  interface TopNavState { userId: string; pageTitle: string; recentFiles: string[]; }
  ```
- [DO] Derive the subtype using `Pick`:
  ```typescript
  interface State { userId: string; pageTitle: string; recentFiles: string[]; pageContents: string; }
  type TopNavState = Pick<State, 'userId' | 'pageTitle' | 'recentFiles'>;
  ```

## Avoiding Numeric Index Signatures
- [DON'T] Use `number` as an index signature key:
  ```typescript
  type CustomArray<T> = { [index: number]: T };
  ```
- [DO] Use `Array`, `ArrayLike`, or `Iterable`:
  ```typescript
  type CustomArray<T> = ArrayLike<T>;
  ```