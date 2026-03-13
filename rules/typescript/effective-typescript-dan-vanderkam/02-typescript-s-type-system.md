# @Domain
These rules MUST be triggered whenever the AI is writing, refactoring, or reviewing TypeScript code. This specifically applies to tasks involving data modeling, interface/type definition, function signature design, type casting/assertions, object initialization, and resolving TypeScript compiler errors.

# @Vocabulary
*   **Domain (of a type)**: The infinite or finite set of all possible values that can be assigned to a type.
*   **Type Space**: The context in which TypeScript static types exist. Symbols here are erased at compile time.
*   **Value Space**: The context in which JavaScript runtime values exist.
*   **Bottom Type (`never`)**: The empty set (∅). A type with no values.
*   **Top Type (`unknown`)**: The universal set. All values belong to this type.
*   **Excess Property Checking**: A strict check applied *only* to object literals when assigned directly to a variable with a declared type, preventing undeclared properties.
*   **Weak Type**: An object type consisting entirely of optional properties. Assigning to it requires at least one matching property.
*   **Declaration Merging**: A feature unique to `interface` allowing it to be augmented by defining it multiple times in the same module.
*   **Homomorphic Mapped Type**: A mapped type (like `Pick` or `Partial`) that preserves the modifiers (`readonly`, `?`) and TSDoc comments of the original type.
*   **Structural Typing (Duck Typing)**: TypeScript's system where assignability is determined by shape/structure, not nominal declarations.
*   **Type Annotation**: Specifying a type explicitly (e.g., `: Type`) to enforce structural compliance.
*   **Type Assertion**: Overriding the type checker (e.g., `as Type` or `!`) without verifying structural compliance.

# @Objectives
*   Think of types mathematically as sets of values, mapping TypeScript operators (`|`, `&`, `extends`) to set theory (union, intersection, subset).
*   Enforce the DRY (Don't Repeat Yourself) principle in Type Space by computing derived types from base types.
*   Maximize type safety by replacing broad types and assertions with precise, structural type annotations.
*   Preserve the integrity of the TypeScript Language Service (autocomplete, refactoring, TSDoc) by defining types correctly.
*   Eliminate implicit mutations and unintended runtime behaviors by leveraging `readonly` and accurate primitive types.

# @Guidelines

### 1. Set Theory and Assignability (Item 7)
*   The AI MUST interpret `A extends B` or "A is assignable to B" as "A is a subset of B".
*   The AI MUST treat union types (`|`) as the union of sets.
*   The AI MUST treat intersection types (`&`) as the intersection of sets. *Note: Intersecting object types results in a type containing the union of all their properties.*
*   The AI MUST recognize that objects can have extra properties not defined in their type (types are "open", not "sealed") unless excess property checking applies.
*   The AI MUST NOT assign tuples of different lengths to each other (e.g., a triple is not assignable to a pair).

### 2. Type Space vs. Value Space (Item 8)
*   The AI MUST distinguish between Type Space and Value Space. `typeof` in Value Space returns JS runtime strings (`"string"`, `"object"`). `typeof` in Type Space returns the TS static type.
*   The AI MUST use `[]` bracket notation to access property types in Type Space (e.g., `Person['first']`). Dot notation (`Person.first`) MUST NOT be used in Type Space.
*   The AI MUST separate types and values in destructuring assignments. NEVER write `function fn({varName: Type})` (this renames the variable). Write `function fn({varName}: {varName: Type})`.
*   The AI MUST recognize that `class` and `enum` introduce symbols into *both* Type and Value spaces.

### 3. Annotations vs. Assertions (Item 9)
*   The AI MUST PREFER type annotations (`: Type`) over type assertions (`as Type` or `<Type>`).
*   The AI MUST NOT use assertions to satisfy the compiler when building objects. Annotations trigger excess property checking; assertions silently bypass it.
*   The AI MUST type arrow function return values cleanly using parentheses: `const arr = items.map((item): Type => ({...}))`.
*   The AI MUST restrict the use of assertions (`as Type`) exclusively to cases where context exists that the type checker lacks (e.g., DOM querying: `e.currentTarget as HTMLButtonElement`).
*   When using a type assertion, the AI MUST include a comment explaining why the assertion is valid.
*   The AI MUST use `!` (non-null assertion) cautiously, treating it as a type assertion that removes `null`/`undefined`. Prefer conditional checking (`if` or `?.`) instead.

### 4. Primitives and Object Wrappers (Item 10)
*   The AI MUST NEVER use capitalized object wrapper types (`String`, `Number`, `Boolean`, `Symbol`, `BigInt`) as TypeScript types.
*   The AI MUST always use lowercase primitive types (`string`, `number`, `boolean`, `symbol`, `bigint`).

### 5. Excess Property Checking (Item 11)
*   The AI MUST understand that excess property checking *only* applies to inline object literals.
*   If the AI needs to bypass excess property checking, it MUST assign the literal to an intermediate variable first (unless it is a Weak Type, which always requires at least one overlapping property).

### 6. Typing Function Expressions (Item 12)
*   The AI MUST PREFER applying types to entire function expressions rather than typing individual parameters and return values (e.g., `const add: BinaryFn = (a, b) => a + b;`).
*   The AI MUST use `typeof fn` to perfectly match the signature of an existing function.
*   If adapting an existing function signature but changing the return type, the AI MUST use `Parameters<typeof fn>` with a rest parameter.

### 7. Interfaces vs. Types (Item 13)
*   The AI MUST default to `interface` for standard object type definitions unless the codebase has a strict pre-existing style preferring `type`.
*   The AI MUST use `interface` when defining types that might need declaration merging (API contracts, global window augments, third-party library extensions).
*   The AI MUST use `type` when defining unions, tuples, primitives, mapped types, or complex conditional types.

### 8. Readonly Modifiers (Item 14)
*   The AI MUST mark function parameters as `readonly Type[]` or `Readonly<Type>` if the function does not mutate them.
*   The AI MUST recognize that `readonly` is shallow.
*   The AI MUST understand that `const` prevents variable reassignment, whereas `readonly` prevents data mutation.

### 9. DRY Principles in Type Space (Item 15)
*   The AI MUST NEVER duplicate property definitions across interfaces if they represent the same domain concept.
*   The AI MUST use `extends` to inherit properties between interfaces.
*   The AI MUST use `Pick<T, K>` or `Omit<T, K>` to extract a subset of properties from an existing object type.
*   The AI MUST use `Partial<T>` to create versions of types where all properties are optional (e.g., for update payloads).
*   The AI MUST use mapped types to synchronize properties between different structures (e.g., `{[K in keyof T]: boolean}`).
*   The AI MUST use `ReturnType<typeof fn>` to extract the return type of a function instead of declaring it manually.

### 10. Index Signatures (Items 16 & 17)
*   The AI MUST AVOID broad index signatures like `[key: string]: any` or `[key: string]: string`.
*   The AI MUST use `Record<'key1'|'key2', Type>` or mapped types if the possible keys are finite or belong to a specific union.
*   The AI MUST consider using the ES6 `Map` object at runtime instead of dynamic objects if keys are truly arbitrary.
*   The AI MUST NEVER use numeric index signatures (`[key: number]: Type`). Use `Array<Type>`, tuples, `ArrayLike<Type>`, or `Iterable<Type>` instead.

# @Workflow
1.  **Analyze Context**: Determine if the code being generated operates in Value Space, Type Space, or both.
2.  **Define Base Models**: Declare foundational models using `interface` (or `type` if unions/tuples are required). Use lowercase primitive types.
3.  **Derive Types (DRY)**: If a new type is a subset, superset, or optional version of a base model, use `extends`, `Pick`, `Omit`, or `Partial` instead of rewriting properties.
4.  **Apply Immutability**: Scan function signatures. If an object/array parameter is not mutated, apply `Readonly<T>` or `readonly T[]`.
5.  **Type Functions**: If defining callbacks or multiple functions with the same signature, define a function type expression and type the variable, rather than inlining parameter types.
6.  **Object Initialization**: When building objects, construct them in a single literal assignment using an explicit Type Annotation `: Type` to trigger excess property checking. Do not use `<Type>` or `as Type`.
7.  **Review Index Signatures**: Replace any `[key: string]` signatures with `Record` or `Map` if possible. Eliminate all `[key: number]` signatures.

# @Examples (Do's and Don'ts)

### Type vs Value Space Destructuring
*   **[DON'T]** Attempt to put type annotations inline with destructured variable names.
    ```typescript
    function email({to: Person, subject: string, body: string}) { /* ... */ } // ERROR: Renames variables to 'Person' and 'string'
    ```
*   **[DO]** Separate the destructuring from the type annotation.
    ```typescript
    function email({to, subject, body}: {to: Person, subject: string, body: string}) { /* ... */ }
    ```

### Annotations vs Assertions
*   **[DON'T]** Use type assertions to satisfy the compiler when initializing objects.
    ```typescript
    const alice = { name: 'Alice', occupation: 'Dev' } as Person; // Bypasses excess property checking
    ```
*   **[DO]** Use type annotations.
    ```typescript
    const alice: Person = { name: 'Alice' }; // Triggers excess property checking and errors on 'occupation'
    ```

### Arrow Function Return Types
*   **[DON'T]** Assert the type inside the map callback.
    ```typescript
    const people = names.map(name => ({name} as Person));
    ```
*   **[DO]** Annotate the return type of the arrow function.
    ```typescript
    const people = names.map((name): Person => ({name}));
    ```

### Primitive Object Wrappers
*   **[DON'T]** Use uppercase wrapper types.
    ```typescript
    function getStringLen(foo: String) { return foo.length; }
    ```
*   **[DO]** Use lowercase primitives.
    ```typescript
    function getStringLen(foo: string) { return foo.length; }
    ```

### Typing Function Expressions
*   **[DON'T]** Repeat parameter types across identical function signatures.
    ```typescript
    const add = (a: number, b: number): number => a + b;
    const sub = (a: number, b: number): number => a - b;
    ```
*   **[DO]** Extract a type for the entire function expression.
    ```typescript
    type BinaryFn = (a: number, b: number) => number;
    const add: BinaryFn = (a, b) => a + b;
    const sub: BinaryFn = (a, b) => a - b;
    ```

### Reusing Signatures with Different Returns
*   **[DO]** Use `Parameters` to inherit parameters but change the return type.
    ```typescript
    async function fetchANumber(...args: Parameters<typeof fetch>): Promise<number> { ... }
    ```

### Readonly Parameters
*   **[DON'T]** Leave parameters mutable if the function does not alter them.
    ```typescript
    function printTriangles(nums: number[]) { ... }
    ```
*   **[DO]** Mark them readonly to prevent unintended side effects and clearly signal intent.
    ```typescript
    function printTriangles(nums: readonly number[]) { ... }
    ```

### DRY Types
*   **[DON'T]** Copy/paste properties from one interface to another.
    ```typescript
    interface State { userId: string; pageTitle: string; recentFiles: string[]; pageContents: string; }
    interface TopNavState { userId: string; pageTitle: string; recentFiles: string[]; }
    ```
*   **[DO]** Use `Pick` to compute the derived type.
    ```typescript
    type TopNavState = Pick<State, 'userId' | 'pageTitle' | 'recentFiles'>;
    ```

### Index Signatures
*   **[DON'T]** Use broad string index signatures if the keys are known.
    ```typescript
    type Vec3D = { [key: string]: number };
    ```
*   **[DO]** Use `Record` to constrain keys precisely.
    ```typescript
    type Vec3D = Record<'x' | 'y' | 'z', number>;
    ```