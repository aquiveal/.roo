# @Domain
The AI MUST apply these rules whenever executing tasks involving TypeScript (TS), including but not limited to writing new TypeScript code, refactoring JavaScript to TypeScript, configuring TypeScript environments (`tsconfig.json`), debugging runtime versus static type discrepancies, and writing unit tests for TypeScript modules.

# @Vocabulary
- **Superset**: TypeScript is a syntactic superset of JavaScript. All syntactically valid JS is valid TS, but TS adds type-specific syntax that is invalid in plain JS.
- **Type Inference**: TypeScript's ability to automatically deduce the type of a variable from its initial value or usage without explicit annotations.
- **Static Type System**: A system that analyzes code before it runs to detect code that will throw exceptions or mismatch developer intent.
- **Soundness**: A property of a type system where it guarantees the accuracy of its static types at runtime. TypeScript is *not* entirely sound (e.g., array out-of-bounds access).
- **Erasable Types**: TypeScript types, interfaces, and annotations are removed entirely during compilation to JavaScript and do not exist at runtime.
- **Tagged Union / Discriminated Union**: A design pattern using a specific literal property (a "tag" or "discriminant", e.g., `kind: 'square'`) on an object to safely recover its type at runtime.
- **Type Assertion**: An explicit, erasable override of a type using the `as Type` syntax (or `<Type>`), distinct from a runtime type cast.
- **Non-null Assertion**: The postfix `!` operator, used to assert to the type checker that a value is not `null` or `undefined`.
- **Structural Typing (Duck Typing)**: TypeScript determines type compatibility based on the shape (structure/properties) of a value, not its explicit declaration or inheritance tree.
- **Open / Unsealed Types**: The concept that structurally typed values may contain additional, undeclared properties beyond what is strictly defined in their interface.
- **Implicit Any**: The unsafe fallback type `any` assigned by TypeScript when it cannot infer a type.
- **Weak Type**: An interface or type consisting *only* of optional properties.

# @Objectives
- The AI MUST strictly separate the mental models of static type analysis (TypeScript) and runtime execution (JavaScript).
- The AI MUST configure TypeScript to maximize strictness, catching intent mismatches and runtime exceptions at compile-time.
- The AI MUST leverage structural typing to create decoupled, easily testable abstractions.
- The AI MUST treat types as open and unsealed, anticipating the presence of excess properties at runtime.
- The AI MUST eradicate the use of the `any` type to preserve type safety, IDE language services, and refactoring confidence.

# @Guidelines

## Configuration and Compiler Options
- The AI MUST configure TypeScript via a `tsconfig.json` file rather than command-line flags.
- The AI MUST enable the `strict` compiler option for all new projects or codebases.
- The AI MUST enable `noImplicitAny` to prevent variables from falling back to unchecked types. Disabling this is ONLY permitted temporarily during a JS-to-TS migration.
- The AI MUST enable `strictNullChecks` to prevent `null` and `undefined` from being implicitly assignable to every type.
- The AI MUST NOT rely on type checking to halt code generation by default; code with type errors still emits JavaScript. If strict halting is required, the AI MUST explicitly enable `noEmitOnError`.

## Distinguishing Type Space from Value Space
- The AI MUST NEVER attempt to check TypeScript types (interfaces, type aliases) at runtime (e.g., `value instanceof MyInterface` is strictly forbidden).
- To perform runtime type checking, the AI MUST use native JavaScript runtime constructs:
  - Property presence checks (e.g., `'height' in shape`).
  - Tagged unions / discriminant properties (e.g., `shape.kind === 'square'`).
  - Classes, because the `class` keyword introduces both a TypeScript type and a JavaScript runtime value (constructor function).
- The AI MUST NEVER use type assertions (`as Type`) to coerce or convert runtime values. If data transformation is needed, the AI MUST use JavaScript runtime operations (e.g., `Number(val)` instead of `val as number`).
- The AI MUST recognize that runtime types may diverge from declared static types (e.g., API responses or unsafe external inputs) and handle validation accordingly.
- The AI MUST NOT attempt to write multiple function implementations for overloaded signatures. Overloading in TS consists of multiple type-only signatures followed by a single, generic or loosely typed implementation block.

## Structural Typing Rules
- The AI MUST design functions to accept interfaces based on the minimum required structure (duck typing) rather than relying on explicit class inheritance or massive concrete implementations.
- The AI MUST recognize that TypeScript types are "open". When iterating over an object's keys (e.g., using `Object.keys()`), the AI MUST handle the keys as generic `string`s, acknowledging that the runtime object may possess properties not defined in the interface.
- The AI MUST use structural typing to sever dependencies in unit tests. Instead of using complex mocking libraries to mock heavy concrete classes (like a specific DB client), the AI MUST define a minimal interface of the required methods and pass simple object literals in tests.
- The AI MUST recognize that classes are evaluated structurally. An object literal that matches the property and method structure of a class is considered assignable to that class, even if it did not pass through the class's constructor.

## Eradication of the `any` Type
- The AI MUST NEVER use the `any` type out of laziness, to silence errors, or to quickly satisfy the compiler.
- The AI MUST explicitly define the structural shape of application state and parameters instead of using `any`.
- The AI MUST recognize that using `any` acts as a contagion that silently breaks function contracts, disables refactoring tools, hides poor design, and introduces runtime crashes.

# @Workflow
1. **Environment Initialization**:
   - Locate or generate a `tsconfig.json`.
   - Ensure `"strict": true`, `"noImplicitAny": true`, and `"strictNullChecks": true` are present.
2. **Intent Declaration**:
   - Declare interfaces/types for all variables, function parameters, and return types explicitly to guide the type checker and produce accurate error suggestions.
3. **Structural Design**:
   - When writing a function that accepts an object, define a minimal interface containing only the properties the function uses.
   - Do not tie the parameter to a concrete class unless runtime constructor checks (`instanceof`) are explicitly required.
4. **Runtime Verification**:
   - If branching logic depends on an object's type, verify if the discriminant is available at runtime.
   - If not, refactor the types to form a Tagged Union, or use the `in` operator to check for unique properties.
   - Ensure that no TypeScript-only artifacts (interfaces/types) are used in `if` statements or `instanceof` checks.
5. **Data Coercion Review**:
   - Scan code for the `as` keyword.
   - If `as` is used to change a variable's runtime behavior or format (e.g., string to number), replace it with the appropriate JavaScript function (e.g., `Number()`).
6. **Eliminate `any`**:
   - Scan all definitions for `any`.
   - Replace every instance of `any` with a specific structural interface representing the actual data contract.

# @Examples (Do's and Don'ts)

## Configuration
- **[DO]**:
  ```json
  {
    "compilerOptions": {
      "strict": true,
      "noImplicitAny": true,
      "strictNullChecks": true
    }
  }
  ```
- **[DON'T]**:
  ```json
  {
    "compilerOptions": {
      "strict": false,
      "noImplicitAny": false
    }
  }
  ```

## Checking Types at Runtime
- **[DO]**: Use a tagged union or property check to differentiate types at runtime.
  ```typescript
  interface Square { kind: 'square'; width: number; }
  interface Rectangle { kind: 'rectangle'; width: number; height: number; }
  type Shape = Square | Rectangle;

  function calculateArea(shape: Shape) {
    if (shape.kind === 'rectangle') {
      return shape.width * shape.height;
    } else {
      return shape.width * shape.width;
    }
  }
  ```
- **[DON'T]**: Attempt to use an interface as a runtime value.
  ```typescript
  interface Square { width: number; }
  interface Rectangle extends Square { height: number; }
  type Shape = Square | Rectangle;

  function calculateArea(shape: Shape) {
    // ANTI-PATTERN: 'Rectangle' only refers to a type, but is being used as a value here.
    if (shape instanceof Rectangle) {
      return shape.height * shape.width;
    }
    return shape.width * shape.width;
  }
  ```

## Converting Values
- **[DO]**: Use JavaScript runtime methods to coerce values.
  ```typescript
  function asNumber(val: number | string): number {
    return Number(val);
  }
  ```
- **[DON'T]**: Use type assertions to coerce values (this does nothing at runtime).
  ```typescript
  function asNumber(val: number | string): number {
    // ANTI-PATTERN: This compiles to `return val;` and fails to convert strings to numbers.
    return val as number;
  }
  ```

## Utilizing Structural Typing for Testing
- **[DO]**: Define a narrow interface and use an object literal to mock dependencies.
  ```typescript
  interface DB {
    runQuery: (sql: string) => any[];
  }
  function getAuthors(database: DB) {
    return database.runQuery(`SELECT first, last FROM authors`);
  }

  // In test:
  getAuthors({
    runQuery(sql: string) {
      return [['Toni', 'Morrison']];
    }
  });
  ```
- **[DON'T]**: Depend on a heavy concrete class that requires complex mocking.
  ```typescript
  class PostgresDB {
    connect() { /* ... */ }
    runQuery(sql: string) { /* ... */ }
  }
  function getAuthors(database: PostgresDB) { // Unnecessarily strict dependency
    return database.runQuery(`SELECT first, last FROM authors`);
  }
  ```

## Dealing with Open Types and Iteration
- **[DO]**: Handle iterations safely, acknowledging that keys might be wider than explicitly declared properties.
  ```typescript
  interface Vector3D { x: number; y: number; z: number; }
  function calculateLength(v: Vector3D) {
    return Math.abs(v.x) + Math.abs(v.y) + Math.abs(v.z);
  }
  ```
- **[DON'T]**: Assume `Object.keys` maps exactly to the interface keys, which causes implicit `any` errors.
  ```typescript
  interface Vector3D { x: number; y: number; z: number; }
  function calculateLength(v: Vector3D) {
    let length = 0;
    for (const axis of Object.keys(v)) {
      // ANTI-PATTERN: `axis` is `string`, causing an implicit 'any' error on `v[axis]`.
      // v could be {x: 1, y: 2, z: 3, address: '123 Main St'}
      length += Math.abs(v[axis]);
    }
    return length;
  }
  ```