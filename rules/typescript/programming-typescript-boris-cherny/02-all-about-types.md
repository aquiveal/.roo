# @Domain

This rule file is activated whenever the AI is tasked with writing, reviewing, or refactoring TypeScript code, specifically focusing on type definitions, type safety, variable declarations, object shapes, collections (arrays/tuples), and handling unknown or absent values. 

# @Vocabulary

- **Type**: A set of values and the things you can do with them.
- **Type Safety**: Using types to prevent programs from doing invalid things.
- **Type Literal**: A type that represents a single specific value and nothing else (e.g., `true`, `27`, `"john"`).
- **Structural Typing**: A style of programming where object compatibility is determined by its shape (properties and methods) rather than its name (also known as duck typing).
- **Index Signature**: A syntax (`[key: T]: U`) used to specify that an object might contain additional keys of a specific type.
- **Type Alias**: A block-scoped declaration (`type MyType = ...`) that points to a specific type, used to DRY up repeated complex types.
- **Union Type**: Defined using `|`, representing a value that can be one type, another type, or both (their sum).
- **Intersection Type**: Defined using `&`, representing a value that possesses the traits of all intersected types (their product).
- **Tuple**: A subtype of an array with a fixed length where the values at each index have specific, known types.
- **Bottom Type**: A type that is a subtype of every other type (e.g., `never`), representing a mathematical proposition that is always false or a state that never occurs.
- **Definite Assignment**: A TypeScript compiler guarantee that a variable declared in one place is explicitly initialized with a value before it is used.

# @Objectives

- Maximize type safety by mapping every variable, function, and object to precise, restrictive types.
- Eliminate implicit and explicit `any` usage entirely to preserve compiler magic and prevent blind execution.
- Rely heavily on TypeScript's type inference for primitives and initialize variables in ways that promote strict inference.
- Enforce strict structural typing for objects and homogeneous constraints for arrays.
- Accurately model the absence of values (`null`, `undefined`, `void`, `never`) without conflating their distinct semantic meanings.

# @Guidelines

### 1. The `any` and `unknown` Types
- **Ban `any`**: You MUST avoid the `any` type at all costs. It acts as regular JavaScript and completely disables the typechecker. Enforce the `noImplicitAny` compiler flag.
- **Use `unknown` for Dynamic Values**: If a value's type is truly unknown ahead of time, you MUST type it as `unknown`. 
- **Refine `unknown`**: You MUST prove to TypeScript what an `unknown` value is using refinements (`typeof`, `instanceof`) before performing type-specific operations on it. You MAY compare (`===`), negate (`!`), or use logical operators (`||`, `&&`, `?`) on `unknown` types without refinement.

### 2. Primitive Types (`boolean`, `number`, `bigint`, `string`, `symbol`)
- **Let TypeScript Infer**: You MUST let TypeScript infer primitive types from their values whenever possible. Do NOT explicitly annotate `let a: number = 1`.
- **Literal Types via `const`**: Use `const` declarations to force TypeScript to infer a narrow type literal (e.g., `const c = true` infers the literal `true`, not `boolean`).
- **Numeric Separators**: You MUST use numeric separators (`_`) when working with long numbers in both value and type positions (e.g., `let a = 1_000_000`).
- **Unique Symbols**: Use `const` to declare symbols so they are inferred as `unique symbol`. A `unique symbol` is always equal to itself and never equal to another `unique symbol`.

### 3. Objects and Structural Typing
- **Use Object Literal Syntax**: You MUST define objects using object literal syntax (shapes) like `{b: number}` or the generic `object` type.
- **Avoid Empty Object Type `{}`**: You MUST NOT type an object as `{}`. Every type except `null` and `undefined` is assignable to `{}`, making it dangerously broad.
- **Avoid `Object`**: You MUST NOT use the capitalized `Object` type.
- **Optional Modifiers**: Use the `?` modifier for properties that may not be present or might be `undefined`.
- **Readonly Modifiers**: Use the `readonly` modifier on object fields that should not be mutated after initialization.
- **Index Signatures**: Use `[key: T]: U` to safely add additional keys to an object. `T` MUST be assignable to `number` or `string`. You MAY use descriptive names for the index key (e.g., `[seatNumber: string]`).
- **Definite Assignment**: You MUST ensure that variables initialized after declaration are definitely assigned a value before they are operated on.
- **Const Object Inference**: Recognize that declaring an object with `const` does NOT infer literal types for its properties because JavaScript objects are mutable. 

### 4. Type Aliases, Unions, and Intersections
- **Block Scoping**: Treat type aliases as block-scoped. Do not declare a type twice in the same scope.
- **Unions (`|`)**: Remember that a union type value can be a member of either type *or both at once*. 
- **Intersections (`&`)**: Use intersections to combine properties of multiple shapes into a single required shape.

### 5. Arrays and Tuples
- **Homogeneous Arrays**: Arrays MUST be kept homogeneous. Do not mix types in a standard array without a specific structural reason.
- **Array Syntax**: You MUST use `T[]` syntax over `Array<T>` for terseness.
- **Any Arrays**: Avoid initializing empty arrays as `let g = []` because they infer as `any[]`. If you do, you MUST populate it within the same scope so TypeScript assigns a final, restricted type when it leaves the scope.
- **Tuples for Fixed-Length / Heterogeneous Data**: You MUST explicitly type tuples (e.g., `[number, string]`). Use tuples over arrays when length is fixed or elements are heterogeneous. 
- **Tuple Modifiers**: Use `?` for optional tuple elements and `...` (rest elements) to define minimum lengths (e.g., `[string, ...string[]]`).
- **Read-only Collections**: Use the `readonly` modifier (`readonly number[]`) or `ReadonlyArray<T>` for immutable arrays. You MUST NOT use mutating methods (`.push`, `.splice`) on read-only arrays; use non-mutating methods (`.concat`, `.slice`) instead.

### 6. Absence Types (`null`, `undefined`, `void`, `never`)
- **Semantic Distinction**: 
  - Use `undefined` when a variable has not been assigned a value yet.
  - Use `null` to explicitly represent the absence of a value.
  - Use `void` for the return type of a function that does not use an explicit return statement.
  - Use `never` for the return type of a function that never returns (throws an exception or loops forever).
- **Strict Null Checks**: You MUST assume `strictNullChecks` is active. You MUST explicitly check for `null` before operating on a nullable value.

### 7. Enums (WARNING: High Risk)
- **Avoid Enums**: You SHOULD avoid enums entirely and use union types of literals instead. 
- **String Enums Only**: If you MUST use enums, you MUST use string-valued enums. You MUST NOT use numeric enums or allow TypeScript to infer numeric values, as numbers are unsafely assignable to numeric enums.
- **Const Enums**: Use `const enum` to prevent unsafe reverse lookups. However, if publishing code to NPM/third-parties, you MUST avoid `const enum` or enable the `preserveConstEnums` TSC flag to prevent inlining mismatch errors.
- **Explicit Assignment**: If an enum is split across multiple declarations, you MUST explicitly assign a value to every member.

# @Workflow

When defining or refactoring types, follow this algorithmic process:

1. **Primitive Assignment**: Are you declaring a primitive? 
   - If yes, do NOT annotate it. Use `const` if you need a specific type literal, or `let` if you need the general type.
2. **Absence/Unknown**: Is the value genuinely unknown at compile time? 
   - If yes, type it as `unknown`. Immediately implement a type refinement (`typeof`, `instanceof`) before allowing operations on it.
3. **Object Definition**: Are you defining an object?
   - If yes, construct a precise shape using object literal notation. Define `readonly` for immutable fields, `?` for optional fields, and an index signature if dynamic keys are expected. NEVER use `{}` or `Object`.
4. **Collection Definition**: Are you defining a list?
   - Does it have a fixed length or mixed types? Use a Tuple (`[TypeA, TypeB]`).
   - Is it a variable length of a single type? Use an Array (`TypeA[]`).
   - Should it be immutable? Prefix with `readonly`.
5. **Function Returns**: Is this a function without a return value?
   - Does it finish executing? Return `void`.
   - Does it crash or loop infinitely? Return `never`.
6. **Alias/Union Abstraction**: Are you repeating a complex shape or defining a variable that can be multiple things?
   - Extract the shape into a `type` alias. Use `|` (Union) for OR logic and `&` (Intersection) for AND logic.
7. **Enum Audit**: Are you using an `enum`?
   - Refactor to a union of string literals if possible. If impossible, ensure it is a `const enum` with explicitly assigned string values.

# @Examples (Do's and Don'ts)

### The `any` and `unknown` Types
- **[DON'T]** Use `any` or bypass type checks.
  ```typescript
  let a: any = 666;
  let b = a + ['danger'];
  ```
- **[DO]** Use `unknown` and refine the type before usage.
  ```typescript
  let a: unknown = 30;
  if (typeof a === 'number') {
    let d = a + 10;
  }
  ```

### Primitives and Inference
- **[DON'T]** Explicitly annotate primitives unnecessarily or miss literal inference.
  ```typescript
  let a: number = 1;
  const b: boolean = true;
  ```
- **[DO]** Let TypeScript infer types and use `const` for literal types. Use numeric separators for readability.
  ```typescript
  let a = 1_000_000; // number
  const b = true; // true (type literal)
  ```

### Objects and Shapes
- **[DON'T]** Use the empty object type `{}` or `Object`, or assign properties dynamically without declaring them.
  ```typescript
  let danger: {} = {};
  danger = 2; // TS allows this!

  let a: {b: number};
  a = {}; // Error: Property 'b' is missing
  ```
- **[DO]** Use precise shapes, index signatures, and modifiers.
  ```typescript
  let a: {
    readonly b: number;
    c?: string;
    [key: number]: boolean;
  } = { b: 1, 10: true };
  ```

### Arrays and Tuples
- **[DON'T]** Mix types in standard arrays or use mutable methods on read-only arrays.
  ```typescript
  let f = ['red'];
  f.push(true); // Error

  let as: readonly number[] = [1, 2, 3];
  as.push(4); // Error
  ```
- **[DO]** Use tuples for heterogeneous/fixed-length data and arrays for homogeneous data. Use non-mutating methods for read-only arrays.
  ```typescript
  let b: [string, string, number] = ['malcolm', 'gladwell', 1963];
  let friends: [string, ...string[]] = ['Sara', 'Tali', 'Chloe'];
  
  let as: readonly number[] = [1, 2, 3];
  let bs: readonly number[] = as.concat(4);
  ```

### Enums
- **[DON'T]** Use numeric enums or non-const enums that allow reverse lookups or unsafe numeric assignment.
  ```typescript
  enum Flippable { Burger, Chair, Cup }
  function flip(f: Flippable) { return 'flipped it'; }
  flip(12); // TS allows this! 12 is assignable to numeric enums.
  ```
- **[DO]** Use `const enum` with explicit string values.
  ```typescript
  const enum Flippable {
    Burger = 'Burger',
    Chair = 'Chair',
    Cup = 'Cup'
  }
  ```