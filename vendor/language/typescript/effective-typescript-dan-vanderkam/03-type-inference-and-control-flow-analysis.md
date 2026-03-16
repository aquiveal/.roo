# @Domain
These rules MUST be activated whenever the AI is writing, modifying, reviewing, or refactoring TypeScript code (`.ts`, `.tsx`), specifically when handling variable declarations, type annotations, object initialization, control flow logic, asynchronous functions, and generic function signatures.

# @Vocabulary
*   **Type Inference**: The process by which the TypeScript compiler automatically determines the type of a variable, return value, or expression based on its initialization or context.
*   **Control Flow Analysis**: The compiler's ability to track the path of execution to determine the specific type of a variable at a specific location (e.g., inside an `if` block).
*   **Widening**: The process where TypeScript guesses a broader type for an unannotated variable initialized with a constant (e.g., treating `'x'` as `string`).
*   **Narrowing (Refinement)**: The process of reducing a broad type (like a union) to a more specific type using runtime checks.
*   **Evolving Types**: The behavior where a variable initialized to `null`, `undefined`, or `[]` (implicitly `any`) expands its type when values are assigned or pushed to it.
*   **Excess Property Checking**: A strict check applied to object literals when assigned to explicitly typed variables, flagging properties that do not exist on the target type.
*   **Aliasing**: Introducing a new variable name that points to an existing value or object property.
*   **Tagged/Discriminated Union**: A union type where each constituent has a unique, literal-typed "tag" property (often `type` or `kind`) used for narrowing.
*   **User-Defined Type Guard**: A function returning a type predicate (e.g., `el is HTMLInputElement`) that narrows a type when evaluating to `true`.
*   **Inference Site**: A syntactic location where TypeScript resolves generic type parameters based on usage.
*   **Currying**: Transforming a function taking multiple arguments into a sequence of functions taking single arguments; used in TypeScript to isolate type inference sites.

# @Objectives
*   Maximize the use of TypeScript's type inference to reduce visual clutter and code noise.
*   Maintain strict type safety by controlling widening and avoiding context loss.
*   Ensure variables maintain a single, consistent type throughout their lifecycle.
*   Leverage structural flow and functional paradigms to preserve inferred types naturally.
*   Write robust control flow logic that safely narrows types without breaking due to aliasing or closures.

# @Guidelines

### 1. Inferable Types (Item 18)
*   **The AI MUST NOT** write explicit type annotations for local variables when TypeScript can infer them accurately from initialization.
*   **The AI MUST** use destructuring assignment instead of explicitly typing individual local variables extracted from objects.
*   **The AI MUST** provide explicit type annotations in the following exceptions:
    *   Function parameters (unless they have default values or are callbacks whose types are contextually inferred).
    *   Object literals, to enable excess property checking and catch errors at the point of definition rather than usage.
    *   Function return types, specifically when the function has multiple return statements, is part of a public API, or when preventing internal implementation errors from leaking out.

### 2. Variable Consistency (Item 19)
*   **The AI MUST NOT** reuse a single variable name for differently typed values across different stages of a function.
*   **The AI MUST** introduce distinct, specifically named variables for distinct concepts.
*   **The AI MUST** prefer `const` over `let` to facilitate narrower type inference and signal immutability.
*   **The AI MUST NOT** use variable shadowing (declaring a variable with the same name in an inner scope), as it confuses human readers even if the compiler permits it.

### 3. Controlling Widening (Item 20)
*   **The AI MUST** control unintended widening by using `const` declarations for primitives.
*   **The AI MUST** use explicit type annotations or the `satisfies` operator when defining objects to prevent property widening while keeping precise keys.
*   **The AI MUST** use `as const` (const assertions) to infer the narrowest possible type (deeply readonly literals and tuples) when defining deeply constant arrays or configuration objects.

### 4. Object Initialization (Item 21)
*   **The AI MUST** create objects all at once using object literals.
*   **The AI MUST NOT** instantiate an empty object (`{}`) and incrementally mutate it to add properties.
*   **The AI MUST** use object spread syntax (`{ ...a, ...b }`) to build larger objects from smaller ones in a type-safe manner.
*   **The AI MUST** use spread syntax with a conditional ternary evaluating to an empty object to conditionally add properties (e.g., `...(condition ? { key: 'value' } : {})`).

### 5. Type Narrowing (Item 22)
*   **The AI MUST** narrow types using runtime constructs: `if`/`else`, `switch`, throwing/returning early, `instanceof`, `in` property checks, and `Array.isArray`.
*   **The AI MUST** use Tagged Unions for complex conditional logic to allow seamless type narrowing.
*   **The AI MUST NOT** rely on `typeof val === 'object'` to exclude `null` (since `typeof null` is `'object'`).
*   **The AI MUST NOT** rely on truthiness checks (`if (!x)`) to narrow strings or numbers if empty strings (`''`) or zeroes (`0`) are valid states.
*   **The AI MUST** be aware that refined types inside a callback or closure will be invalidated if the variable can be mutated externally before the callback executes.

### 6. Aliasing (Item 23)
*   **The AI MUST** use aliases consistently. If a property is aliased into a local variable, the AI MUST use that local variable for all subsequent control flow checks.
*   **The AI MUST NOT** perform a type refinement on a property (e.g., `polygon.bbox`) and then extract the alias, as the alias will not inherit the narrowed type.
*   **The AI MUST** utilize object destructuring to extract aliases safely and consistently.
*   **The AI MUST** treat property refinements as volatile; function calls may invalidate property refinements. Local variable refinements are strictly preferred.

### 7. Context in Type Inference (Item 24)
*   **The AI MUST** recognize that factoring a value out of a function call into a local variable strips its contextual typing.
*   **The AI MUST** apply explicit type annotations or `as const` when extracting string literals or tuples into variables to prevent them from being widened to `string` or arrays.
*   **The AI MUST** define callback functions inline when possible to take advantage of contextual parameter type inference.

### 8. Evolving Types (Item 25)
*   **The AI MUST** explicitly annotate the type of variables initialized to `null`, `undefined`, or `[]` to prevent implicit `any` errors, rather than relying on TypeScript's type-evolving mechanics, to ensure strict validation.
*   **The AI MUST** use `for-of` loops or `map` instead of `forEach` if relying on evolving types, as implicit `any` types do not evolve through function calls.

### 9. Functional Constructs & Async Flow (Items 26 & 27)
*   **The AI MUST** prefer built-in functional array methods (`map`, `filter`, `reduce`, `flat`) or utility libraries (like Lodash) over hand-rolled imperative loops to ensure types flow correctly without explicit annotations.
*   **The AI MUST** prefer `async`/`await` over raw Promises or callbacks to prevent the "pyramid of doom" and ensure seamless type flow.
*   **The AI MUST** enforce that a function is completely synchronous or completely asynchronous (returning a Promise). Never mix synchronous returns with callback/Promise resolution.

### 10. New Inference Sites (Item 28)
*   **The AI MUST** recognize that generic function inference is all-or-nothing.
*   **The AI MUST** use currying (a function returning a function) or a Class wrapper to create distinct inference sites if it needs to explicitly specify one generic type parameter while allowing TypeScript to infer another.

# @Workflow
1.  **Analyze Initialization**: When defining variables, assess if TypeScript can accurately infer the type. If yes, omit the annotation. If it widens unsafely (e.g., tuples becoming arrays), apply `as const`, `satisfies`, or an explicit annotation.
2.  **Object Construction**: If building an object, assemble all properties in a single literal. Use spread syntax for dynamic or merged properties.
3.  **Control Flow**: Identify union types or nullable values. Implement early returns, `in` checks, or tagged union switch statements to narrow types.
4.  **Alias Resolution**: Extract needed properties via destructuring *before* performing narrowing checks. Use the destructured variables exclusively in the logic block.
5.  **Async/Data Iteration**: Convert imperative loops to `map`/`reduce`. Convert nested callbacks/Promises to `async`/`await`.
6.  **Generics Validation**: If writing a generic function where the user provides one type (e.g., an API schema) but the compiler infers the payload, refactor into a curried function to isolate the inference sites.

# @Examples (Do's and Don'ts)

### Avoid Cluttering Inferable Types
*   **[DON'T]**
    ```typescript
    let x: number = 12;
    const squares: number[] = [1, 2, 3].map((x: number) => x * x);
    ```
*   **[DO]**
    ```typescript
    let x = 12;
    const squares = [1, 2, 3].map(x => x * x);
    ```

### Explicit Annotations for Object Literals
*   **[DON'T]**
    ```typescript
    const furby = { name: 'Furby', id: 123, price: 35 };
    logProduct(furby); // Error occurs here at usage
    ```
*   **[DO]**
    ```typescript
    const furby: Product = { name: 'Furby', id: 123, price: 35 }; // Error caught immediately at definition
    logProduct(furby);
    ```

### Variable Consistency
*   **[DON'T]**
    ```typescript
    let id = "12-34";
    fetchProduct(id);
    id = 123456; // Error: Type 'number' is not assignable to type 'string'
    fetchSerial(id);
    ```
*   **[DO]**
    ```typescript
    const productId = "12-34";
    fetchProduct(productId);
    const serialNum = 123456;
    fetchSerial(serialNum);
    ```

### Object Initialization
*   **[DON'T]**
    ```typescript
    const pt = {};
    pt.x = 3; // Error: Property 'x' does not exist on type '{}'
    pt.y = 4;
    ```
*   **[DO]**
    ```typescript
    const pt = { x: 3, y: 4 };
    
    // Conditional additions:
    const president = { ...firstLast, ...(hasMiddle ? { middle: 'S' } : {}) };
    ```

### Aliasing Consistency
*   **[DON'T]**
    ```typescript
    const box = polygon.bbox;
    if (polygon.bbox) {
      if (pt.x < box.x[0]) { ... } // Error: 'box' is possibly 'undefined'
    }
    ```
*   **[DO]**
    ```typescript
    const { bbox } = polygon;
    if (bbox) {
      if (pt.x < bbox.x[0]) { ... } // OK
    }
    ```

### Context and Tuples
*   **[DON'T]**
    ```typescript
    const loc = [10, 20]; // Inferred as number[]
    panTo(loc); // Error: number[] is not assignable to [number, number]
    ```
*   **[DO]**
    ```typescript
    const loc: [number, number] = [10, 20];
    panTo(loc); // OK
    ```

### Currying for Inference Sites
*   **[DON'T]**
    ```typescript
    declare function fetchAPI<API, Path extends keyof API>(path: Path): Promise<API[Path]>;
    // User must specify ALL generics or NONE:
    fetchAPI<SeedAPI, '/seed/strawberry'>('/seed/strawberry'); // Tedious
    ```
*   **[DO]**
    ```typescript
    declare function fetchAPI<API>(): <Path extends keyof API>(path: Path) => Promise<API[Path]>;
    // API is explicitly bound; Path is inferred:
    const berry = await fetchAPI<SeedAPI>()('/seed/strawberry');
    ```