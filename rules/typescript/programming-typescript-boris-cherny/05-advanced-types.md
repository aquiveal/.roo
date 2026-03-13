# @Domain
These rules activate whenever the AI is tasked with creating, refactoring, or analyzing TypeScript types, interfaces, classes, and architectural data models. This includes writing generic functions, manipulating complex object shapes, validating type safety, configuring TypeScript compiler flags related to strictness, or resolving type errors/subtyping constraints.

# @Vocabulary
*   **Subtype (`<:`)**: A type `B` is a subtype of `A` (`B <: A`) if `B` can be safely used anywhere `A` is required.
*   **Supertype (`>:`)**: A type `B` is a supertype of `A` (`B >: A`) if `A` can be safely used anywhere `B` is required.
*   **Invariance**: Requiring exactly a specific type `T`.
*   **Covariance**: Requiring a subtype (`<:T`). Complex types in TS (objects, classes, arrays, function return types) are covariant.
*   **Contravariance**: Requiring a supertype (`>:T`). Function parameter types and `this` types in TS are contravariant.
*   **Bivariance**: Accepting either a subtype or a supertype.
*   **Type Widening**: TS inferring a general base type (e.g., `string`) from a literal value (e.g., `'x'`) when declared with `let` or `var`, or inferring `any` for uninitialized `null`/`undefined`.
*   **Fresh Object Literal Type**: The un-widened type TS infers directly from an inline object literal, which undergoes strict Excess Property Checking.
*   **Refinement**: The process of TS narrowing a type using control flow statements (`if`, `switch`) and type queries (`typeof`, `instanceof`, `in`).
*   **Discriminated Union**: A union of shapes differentiated by a shared, mutually exclusive, non-generic literal tag (usually a string literal).
*   **Totality (Exhaustiveness)**: Ensuring every possible case of a union is handled in control flow structures (preventing missed branches).
*   **User-Defined Type Guard**: A function returning a boolean annotated with `parameterName is Type` to propagate type refinements across scopes.
*   **Conditional Type**: A type-level ternary expression (`T extends U ? A : B`).
*   **Distributive Conditional**: A conditional type that automatically maps over each member of a union type.
*   **Type Branding**: Simulating nominal types in a structural type system by intersecting a base type with a synthetic unique symbol.
*   **Companion Object Pattern**: Exploiting TS's dual namespaces (types and values) to declare a type and a value object with the exact same name to group semantic operations together.

# @Objectives
*   Maximize compile-time safety by preferring precise, narrow types over widened or `any` types.
*   Ensure that type manipulations mathematically reflect the runtime constraints of the data.
*   Eliminate implicit behaviors by enforcing totality and exhaustive pattern matching.
*   Limit the use of unsafe escape hatches (type assertions, non-null assertions).
*   Utilize advanced type-level programming (mapped types, conditionals, inference) to keep types DRY, composable, and synchronized with actual runtime values.

# @Guidelines

## Subtyping and Variance
*   **Covariant Returns**: Treat function return types as covariant. A function returning a subtype can satisfy a signature expecting a supertype return.
*   **Contravariant Parameters**: Treat function parameters as contravariant. For function `A` to be assignable to function `B`, `A`'s parameters must be supertypes of `B`'s parameters.
*   **Compiler Flag Constraint**: YOU MUST assume `"strictFunctionTypes": true` is enabled to enforce parameter contravariance.
*   **Assignability Constraint**: Never rely on enum assignability. Numeric enums are extremely unsafe because any number can be assigned to them. Avoid enums; prefer unions of literal types.

## Type Widening and Narrowing
*   **Prevent Unintended Widening**: Use `const` to prevent literal widening. Use `as const` to recursively mark deeply nested data structures as `readonly` literals.
*   **Preserve Freshness for Validation**: To trigger Excess Property Checking, pass object literals directly to functions or assign them directly to explicitly typed variables. Do not bypass this check by assigning to an untyped variable first unless intentional.
*   **Null Widening**: Never leave variables initialized to `null` or `undefined` un-annotated, as they will aggressively widen to `any`.

## Refinement, Totality, and Guards
*   **Flow-based Refinement**: Use `typeof`, `instanceof`, `in`, and truthiness checks to refine types locally.
*   **Scope Boundaries**: Because refinements do not cross function scope boundaries, YOU MUST use User-Defined Type Guards (`arg is Type`) to encapsulate validation logic that needs to propagate type narrowing to the caller.
*   **Tagging Unions**: When creating union types that represent different states or events, implement them as Discriminated Unions. The tag MUST be on the same property for all members, use a literal type, be non-generic, and be mutually exclusive.
*   **Enforce Totality**: All `switch` or `if/else` chains operating on union types must be exhaustive. YOU MUST ensure all code paths return a value. Assume `"noImplicitReturns": true` is active.

## Advanced Object Types
*   **Keying-In**: Use bracket notation (`O[K]`) to look up property types. To get array element types, use `T[number]`. To get tuple element types, use numeric literals `T[0]`.
*   **`keyof` Constraint**: Use `keyof T` to extract keys as a union of string literal types. Assume `"keyofStringsOnly": false`.
*   **Mapped Types**: Use `[K in keyof T]` to map object shapes. Use the `-` operator to explicitly remove modifiers (e.g., `-readonly [K in keyof T]` or `[K in keyof T]-?`).
*   **Built-ins**: Rely on `Record<K, V>`, `Partial<T>`, `Required<T>`, `Readonly<T>`, and `Pick<T, K>` instead of writing custom mapped types for basic transformations.
*   **Companion Object Pattern**: When defining a distinct domain concept, declare a `type` and a `const` with the same name. Export the type for signatures and the `const` object for utility/factory functions related to that type.

## Advanced Function Types
*   **Tuple Inference Constraint**: When creating utility functions that return tuples, and you wish to avoid `as const` to maintain mutability, use a variadic rest parameter constrained to `unknown[]`: `function tuple<T extends unknown[]>(...ts: T): T { return ts; }`.
*   **Overload Contextual Types**: When overloading functions, the implementation signature must be highly specific, preferably using unions of literals (e.g., `Date | string`), rather than `any`, to enforce exhaustive checks inside the function body.

## Conditional Types
*   **Type-Level Ternaries**: Use `T extends U ? A : B` to resolve types dynamically.
*   **Distributive Conditionals**: When operating on union types via generics, rely on the distributive property. Remember that `T extends U ? X : Y` where `T` is `A | B` evaluates to `(A extends U ? X : Y) | (B extends U ? X : Y)`.
*   **The `infer` Keyword**: Use `infer` to extract deeply nested types (e.g., function arguments, array members, promise resolutions) inline within a conditional type clause. Never declare an upfront generic parameter just to hold an extracted type.
*   **Built-ins**: Rely on `Exclude<T, U>`, `Extract<T, U>`, `NonNullable<T>`, `ReturnType<F>`, and `InstanceType<C>`.

## Nominal Types (Branding)
*   **Branding Primitive Types**: When strict differentiation between identical structural types is required (e.g., `UserID` vs `CompanyID`), use Type Branding.
*   **Brand Implementation**: Intersect the base type with an object containing a `unique symbol`. Example: `type UserID = string & { readonly brand: unique symbol }`. Use a factory function companion object to assert values into the branded type.

## Prototype Extension
*   **Safe Extensions**: To extend built-in prototypes (e.g., `Array.prototype`), use declaration merging.
*   **Global Augmentation**: If inside a module, wrap the interface extension in `declare global { interface Target { ... } }`. Then implement the runtime method on `Target.prototype`.

## Escape Hatches
*   **Type Assertions (`as`)**: Strictly limit the use of `as`. If an assertion is absolutely required, use `as` instead of angle brackets (`<Type>`) to avoid JSX parsing clashes. If asserting unrelated types, cast to `any` first (`x as any as Type`), but treat this as an architectural smell.
*   **Non-Null Assertions (`!`)**: Avoid using `!`. If you find yourself using `!`, refactor the types (e.g., split a general type into a `Visible` and `Destroyed` type) to prove to the compiler that the value exists.
*   **Definite Assignment Assertions (`!:`):** Avoid. Use only if a variable is initialized completely out of band and TS cannot statically analyze the initialization flow.

# @Workflow
1.  **Analyze the Domain**: Identify the data structures and their runtime behaviors. 
2.  **Define Base Types**: Start by declaring exact structural types, utilizing literals and `readonly` modifiers to lock down mutability and scope.
3.  **Establish Relationships**: Use conditional types, mapped types, and keying-in to relate types dynamically (e.g., calculating a return type based on an input tag).
4.  **Enforce Refinement**: Create Discriminated Unions for states. Write User-Defined Type Guards for cross-boundary validations.
5.  **Test Totality**: Implement exhaustive `switch`/`if` blocks for all unions. Ensure no implicit `undefined` returns are possible.
6.  **Eradicate Escape Hatches**: Review the codebase for `as`, `!`, and `any`. Refactor the architecture to remove the need for them by utilizing narrow types or branding.

# @Examples (Do's and Don'ts)

## Discriminated Unions and Totality
*   **[DO]**: Use a shared literal tag and exhaustively switch over it.
```typescript
type UserTextEvent = { type: 'TextEvent'; value: string; target: HTMLInputElement };
type UserMouseEvent = { type: 'MouseEvent'; value: [number, number]; target: HTMLElement };
type UserEvent = UserTextEvent | UserMouseEvent;

function handle(event: UserEvent) {
  switch (event.type) {
    case 'TextEvent':
      return event.value; // TS knows this is a string
    case 'MouseEvent':
      return event.value; // TS knows this is [number, number]
  }
}
```
*   **[DON'T]**: Use optional properties or rely on raw property checking without a tag, resulting in overlapping shapes.
```typescript
type UserEvent = 
  | { value: string; target: HTMLInputElement }
  | { value: [number, number]; target: HTMLElement };

function handle(event: UserEvent) {
  if (typeof event.value === 'string') {
    // DON'T: event.target is still HTMLInputElement | HTMLElement here!
    return event.target;
  }
}
```

## Tuple Inference
*   **[DO]**: Use variadic rest parameters bounded by `unknown[]` to infer tuples dynamically.
```typescript
function tuple<T extends unknown[]>(...ts: T): T {
  return ts;
}
const a = tuple(1, true); // Inferred strictly as [number, boolean]
```
*   **[DON'T]**: Rely on default array widening when strict positional types are needed.
```typescript
const a = [1, true]; // Inferred loosely as (number | boolean)[]
```

## User-Defined Type Guards
*   **[DO]**: Return a type predicate (`arg is Type`) to carry type refinement outside the function.
```typescript
function isString(a: unknown): a is string {
  return typeof a === 'string';
}

function parse(input: string | number) {
  if (isString(input)) {
    return input.toUpperCase(); // OK
  }
}
```
*   **[DON'T]**: Return a raw boolean, which discards type refinement in the caller's scope.
```typescript
function isString(a: unknown): boolean {
  return typeof a === 'string';
}

function parse(input: string | number) {
  if (isString(input)) {
    return input.toUpperCase(); // ERROR: Property 'toUpperCase' does not exist on type 'number'.
  }
}
```

## Conditional Types with `infer`
*   **[DO]**: Use `infer` inline to extract nested types without requiring caller-provided type arguments.
```typescript
type ElementType<T> = T extends (infer U)[] ? U : T;
type A = ElementType<number[]>; // resolves to number
```
*   **[DON'T]**: Declare up-front generic parameters for extraction, putting the burden on the caller.
```typescript
type ElementUgly<T, U> = T extends U[] ? U : T;
type C = ElementUgly<number[]>; // ERROR: Requires 2 type arguments
```

## Simulating Nominal Types (Branding)
*   **[DO]**: Use a `unique symbol` intersection to prevent accidental string assignment.
```typescript
type UserID = string & { readonly brand: unique symbol };
const UserID = (id: string) => id as UserID;

function query(id: UserID) {}
query(UserID('123')); // OK
```
*   **[DON'T]**: Use basic type aliases for distinct IDs, allowing silent mix-ups.
```typescript
type UserID = string;
type CompanyID = string;

function query(id: UserID) {}
const companyId: CompanyID = '456';
query(companyId); // UNSAFE: TS allows this
```

## Safely Extending the Prototype
*   **[DO]**: Merge the built-in interface globally before extending.
```typescript
// zip.ts
declare global {
  interface Array<T> {
    zip<U>(list: U[]): [T, U][];
  }
}

Array.prototype.zip = function<T, U>(this: T[], list: U[]): [T, U][] {
  return this.map((v, k) => [v, list[k]] as [T, U]);
};
```
*   **[DON'T]**: Mutate built-in prototypes without informing the type system, bypassing compilation checks.