# @Domain
When the AI is writing, modifying, reviewing, or configuring TypeScript code; setting up or adjusting `tsconfig.json` configurations; migrating JavaScript codebases to TypeScript; or debugging discrepancies between static types and runtime behavior.

# @Vocabulary
*   **Syntactic Superset**: The relationship where all valid JavaScript programs are syntactically valid TypeScript programs (but not necessarily free of type errors).
*   **Static Type System**: A system that models runtime behavior and spots potential exceptions or intent mismatches without executing the code.
*   **Soundness**: A property of a type system where static types are strictly guaranteed to match runtime types. TypeScript is explicitly **not sound**.
*   **Type Erasure**: The process where TypeScript removes all interfaces, types, and type annotations during compilation to emit pure JavaScript.
*   **noImplicitAny**: A compiler option that flags an error when TypeScript cannot infer a type and defaults to `any`.
*   **strictNullChecks**: A compiler option that removes `null` and `undefined` from the domain of all other types, requiring explicit handling.
*   **noUncheckedIndexedAccess**: A strict compiler option that flags array and object index accesses as potentially `undefined`.
*   **Tagged/Discriminated Union**: A design pattern using a specific property (a "tag" or "discriminant", e.g., `kind`) that exists at runtime to explicitly store type information for runtime reconstruction.
*   **Structural Typing / Duck Typing**: A type system paradigm where compatibility is determined by the shape (properties and structure) of a value, not by explicit declarations or inheritance.
*   **Open/Unsealed Types**: The concept that in TypeScript, an object matching an interface may contain additional, undeclared properties at runtime.
*   **Type Assertion**: Using the `as` keyword to override the type checker's inferred type (a type-level operation that has zero effect at runtime).

# @Objectives
*   Configure TypeScript with maximum strictness via `tsconfig.json` (`strict` mode) to catch the highest volume of errors.
*   Maintain an absolute conceptual boundary between type space (static) and value space (runtime), ensuring type definitions are never relied upon for runtime execution.
*   Embrace structural typing by designing functions to accept the minimal required shape and writing tests using structural mocks rather than heavy dependencies.
*   Acknowledge that TypeScript types are "open" and write code that safely handles excess runtime properties (especially during iteration).
*   Ruthlessly eliminate the `any` type to preserve language services, protect refactoring safety, and force explicit type design.

# @Guidelines

## Relationship Between TypeScript and JavaScript
*   The AI MUST treat `.js` files as valid TypeScript. When migrating code, the AI MUST recognize that simply renaming `.js` to `.ts` is the valid first step.
*   The AI MUST use type annotations explicitly to declare intent, enabling the type checker to spot when the implementation diverges from the intended behavior (e.g., catching misspelled properties like `capitol` vs `capital`).
*   The AI MUST anticipate that passing the type checker does NOT guarantee runtime safety. The AI MUST write defensive runtime checks for external data, array out-of-bounds access, or network responses, recognizing TypeScript's inherent unsoundness.
*   The AI MUST recognize that TypeScript will flag valid JavaScript as an error if it determines the behavior is questionable (e.g., `null + 7`, `[] + 12`, calling functions with extra arguments). The AI MUST correct these to satisfy the type checker.

## Compiler Configuration
*   The AI MUST configure TypeScript options exclusively within `tsconfig.json`, NEVER via command-line flags.
*   The AI MUST enable `strict` mode for all new projects.
*   The AI MUST explicitly ensure `noImplicitAny` is enabled, fixing all resulting errors with specific type declarations. `noImplicitAny` may ONLY be temporarily disabled if actively in the middle of a massive JavaScript-to-TypeScript migration.
*   The AI MUST enable `strictNullChecks` to prevent "undefined is not an object" runtime errors. The AI MUST fix resulting errors by explicitly typing variables as `Type | null` or narrowing types using `if` checks.
*   The AI MUST NOT use the non-null assertion operator (`!`) blindly; it MUST only be used when the AI can definitively guarantee the value is present.
*   The AI SHOULD consider enabling `noUncheckedIndexedAccess` to catch out-of-bounds array and object property accesses, handling the resulting `undefined` checks.

## Code Generation vs. Types
*   The AI MUST NOT use TypeScript interfaces or type aliases in runtime operations (e.g., `instanceof InterfaceName`).
*   To ascertain types at runtime, the AI MUST use property checking (`'prop' in shape`), Tagged Unions (`shape.kind === 'square'`), or Classes (which introduce both a static type and a runtime value).
*   The AI MUST NOT use type assertions (`as number`) to attempt runtime value conversions. The AI MUST use JavaScript runtime constructs (`Number(val)`) for actual type coercion.
*   The AI MUST understand that TypeScript emits JavaScript even if type errors exist. However, the AI MUST aim for zero type errors and SHOULD configure `noEmitOnError` in build pipelines to prevent outputting broken code.
*   When implementing function overloads, the AI MUST provide multiple type signatures but strictly ONE implementation.

## Structural Typing
*   The AI MUST design functions assuming parameters are "open". A parameter typed as `Vector3D` might be passed an object with `address`, `name`, or other arbitrary properties at runtime.
*   When iterating over object keys (e.g., `Object.keys()`), the AI MUST handle the fact that keys are returned as `string`, not `keyof T`, because structural typing allows excess properties at runtime.
*   The AI MUST NOT assume that an object typed as a class guarantees the class constructor was executed. Structural typing allows object literals matching the class shape to bypass validation logic in the constructor.
*   The AI MUST leverage structural typing for unit testing by creating minimal, ad-hoc objects that satisfy interface constraints rather than importing and mocking full, complex production classes or databases.

## The `any` Type
*   The AI MUST NOT use the `any` type, unless completely unavoidable.
*   The AI MUST recognize that `any` breaks function contracts, disables language services (autocomplete, rename), hides the application's state design, and masks bugs during refactoring.
*   If the AI encounters a type error it does not understand, it MUST NOT use `as any` to silence it. The AI MUST write correct, specific type definitions or use `unknown` if the type is truly dynamic.

# @Workflow
1.  **Environment Initialization**: Verify `tsconfig.json` exists. Ensure `strict`, `noImplicitAny`, and `strictNullChecks` are `true`.
2.  **Intent Declaration**: When defining variables, parameters, and return types, write explicit type annotations to establish the contract and intent.
3.  **Runtime Independence**: Review all type-checking logic. If type checks are needed at runtime (e.g., branching logic based on input type), implement Tagged Unions or JavaScript `typeof`/`in` checks. Remove any runtime `instanceof` checks against TypeScript interfaces.
4.  **Structural Validation**: Review object iteration and property access. Ensure logic accounts for "open" objects that may contain excess runtime properties.
5.  **Test Structuring**: When writing tests, instantiate simple object literals that structurally satisfy dependency interfaces instead of heavy mocking.
6.  **Eradicate `any`**: Perform a final pass to remove all `any` types. Replace them with specific interfaces, unions, or `unknown` where applicable. 

# @Examples (Do's and Don'ts)

## Configuration and Implicit Any
*   [DO]
    ```json
    // tsconfig.json
    {
      "compilerOptions": {
        "strict": true,
        "noImplicitAny": true,
        "strictNullChecks": true
      }
    }
    ```
    ```typescript
    function add(a: number, b: number) {
      return a + b;
    }
    ```
*   [DON'T]
    ```typescript
    // Fails when noImplicitAny is enabled
    function add(a, b) {
      return a + b;
    }
    ```

## Runtime Type Checking
*   [DO]
    ```typescript
    interface Square { kind: 'square'; width: number; }
    interface Rectangle { kind: 'rectangle'; height: number; width: number; }
    type Shape = Square | Rectangle;

    function calculateArea(shape: Shape) {
      if (shape.kind === 'rectangle') {
        return shape.width * shape.height;
      } else {
        return shape.width * shape.width;
      }
    }
    ```
*   [DON'T]
    ```typescript
    function calculateArea(shape: Shape) {
      // Anti-pattern: Interface used as runtime value
      if (shape instanceof Rectangle) {
        return shape.height * shape.width;
      }
    }
    ```

## Runtime Type Conversion
*   [DO]
    ```typescript
    function asNumber(val: number | string): number {
      return Number(val);
    }
    ```
*   [DON'T]
    ```typescript
    function asNumber(val: number | string): number {
      // Anti-pattern: Type assertion used for runtime conversion
      return val as number;
    }
    ```

## Structural Typing in Tests
*   [DO]
    ```typescript
    interface DB {
      runQuery: (sql: string) => any[];
    }
    function getAuthors(database: DB) { /* ... */ }

    // Test
    test('getAuthors', () => {
      const authors = getAuthors({
        runQuery(sql: string) {
          return [['Toni', 'Morrison']];
        }
      });
    });
    ```
*   [DON'T]
    ```typescript
    // Anti-pattern: Bringing in massive production dependencies for testing
    import { PostgresDB } from './production-db';
    import { mockPostgres } from 'heavy-mocking-lib';
    ```

## Function Overloads
*   [DO]
    ```typescript
    function add(a: number, b: number): number;
    function add(a: string, b: string): string;
    function add(a: any, b: any) {
      return a + b;
    }
    ```
*   [DON'T]
    ```typescript
    // Anti-pattern: Multiple implementations
    function add(a: number, b: number) { return a + b; }
    function add(a: string, b: string) { return a + b; }
    ```

## Avoiding `any` in Callbacks
*   [DO]
    ```typescript
    interface ComponentProps {
      onSelectItem: (id: number) => void;
    }
    ```
*   [DON'T]
    ```typescript
    interface ComponentProps {
      // Anti-pattern: 'any' allows breaking contracts if the signature needs to change later
      onSelectItem: (item: any) => void; 
    }
    ```