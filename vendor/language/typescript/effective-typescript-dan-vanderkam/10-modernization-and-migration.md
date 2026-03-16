# @Domain
This rule file activates when the user requests assistance with:
- Migrating a legacy JavaScript codebase to TypeScript.
- Modernizing outdated JavaScript syntax (e.g., pre-ES2015) to modern ECMAScript standards.
- Configuring a project to support mixed JavaScript and TypeScript files.
- Analyzing and resolving type errors during a JS-to-TS conversion process.
- Implementing or transitioning away from JSDoc-based type checking (`@ts-check`).
- Enabling stricter TypeScript compiler options (specifically `noImplicitAny`) in an existing codebase.

# @Vocabulary
- **Transpiler**: A tool (like `tsc`) that converts modern JavaScript/TypeScript into older, more widely supported JavaScript (e.g., ES5).
- **ECMAScript Modules (ESM)**: The standard JavaScript module system using `import` and `export` statements, replacing CommonJS (`require`/`module.exports`).
- **@ts-check**: A directive added to the top of a `.js` file to enable loose TypeScript type checking without converting the file extension to `.ts`.
- **JSDoc**: A comment-based syntax used to provide type annotations and assertions in plain JavaScript files.
- **allowJs**: A TypeScript compiler option that permits JavaScript files to be compiled and imported alongside TypeScript files.
- **Dependency Graph**: The hierarchical structure of module imports within a project. 
- **Leaves (Dependency Graph)**: Modules that import no other modules (e.g., utility files, third-party libraries).
- **Roots (Dependency Graph)**: Modules that are imported by no other modules (e.g., entry points, test files).
- **Topological Sort**: An algorithmic ordering of the dependency graph used to determine the exact bottom-up sequence for module migration.
- **noImplicitAny**: A strict TypeScript compiler flag that prohibits variables from implicitly adopting the `any` type, considered the final milestone of a complete TypeScript migration.

# @Objectives
- The AI MUST modernize legacy JavaScript syntax prior to or concurrent with TypeScript adoption to leverage TypeScript's deep understanding of modern ECMAScript.
- The AI MUST establish a safe, gradual migration path using `allowJs` rather than attempting a "stop the world" rewrite.
- The AI MUST migrate modules strictly in a bottom-up order, starting from the leaves of the dependency graph and ending at the roots (tests).
- The AI MUST strictly separate the process of adding types from the process of refactoring architectural design or upgrading frameworks.
- The AI MUST utilize JSDoc and `@ts-check` for initial experimentation and discovery, but aggressively transition these to native TypeScript annotations when converting to `.ts`.
- The AI MUST treat the elimination of all `noImplicitAny` errors as the definitive conclusion of the migration process.

# @Guidelines

### Preparation and Scope Constraints
- When beginning a migration, the AI MUST first eliminate dead code and deprecated features.
- The AI MUST NOT perform structural refactoring (e.g., converting a jQuery app to React) during the TypeScript migration phase. Design flaws discovered during migration MUST be noted via `TODO` comments or bug trackers, but MUST NOT be fixed concurrently with type conversion.

### Syntax Modernization (JS to Modern JS)
- When encountering CommonJS (`require`/`module.exports`) or AMD patterns, the AI MUST convert them to ECMAScript Modules (`import`/`export`).
- When encountering prototype-based object models (`function Person() {...} Person.prototype.getName = ...`), the AI MUST convert them to ES2015 `class` syntax.
- When encountering `var` declarations, the AI MUST replace them with `let` or `const`.
- When encountering C-style `for(;;)` loops, the AI MUST replace them with `for-of` loops or array methods (e.g., `.map()`).
- When encountering callback chains or raw Promises, the AI MUST refactor them to use `async` and `await`.
- When encountering function expressions where `this` binding is required, the AI MUST replace them with arrow functions (`() => {}`).
- When encountering default parameter assignments inside a function body, the AI MUST move them to the function declaration signature (e.g., `function foo(param = 123)`).
- When creating objects or reading properties, the AI MUST utilize compact object literals (`{x}`) and destructuring assignment (`const {x, y} = obj`).
- When encountering associative arrays built using plain objects (`{}`), the AI MUST evaluate if `Map` or `Set` is a more appropriate data structure.
- When encountering guarded property accesses (e.g., `x && x.y`), the AI MUST replace them with optional chaining (`x?.y`).
- When encountering truthiness fallbacks (e.g., `x || 10`), the AI MUST replace them with nullish coalescing (`x ?? 10`) to avoid bugs with falsy values like `0`.
- The AI MUST NOT insert `"use strict"` directives, as TypeScript enforces strict mode automatically in module mode.

### Experimentation and JSDoc (`@ts-check`)
- When experimenting with types in a `.js` file, the AI MUST add `// @ts-check` to the very top of the file.
- When `@ts-check` flags undeclared globals, the AI MUST declare them using `let`/`const` or create a `types.d.ts` file describing the ambient environment.
- When `@ts-check` flags unknown third-party libraries, the AI MUST instruct the user to install the corresponding `@types/` package (e.g., `npm install --save-dev @types/jquery`).
- When DOM type errors occur in JS files (e.g., `getElementById` returning a generic `HTMLElement`), the AI MUST use JSDoc type assertions requiring exact parenthesis syntax: `/** @type {HTMLInputElement} */(document.getElementById('age'))`.
- When converting files from `.js` to `.ts`, the AI MUST migrate all JSDoc type annotations to native TypeScript annotations, and subsequently DELETE the type information from the JSDoc blocks to prevent redundancy and desynchronization.

### Migration Configuration and Ordering
- When configuring a gradual migration, the AI MUST ensure `allowJs: true` is set in `tsconfig.json`.
- The AI MUST ensure the build chain (webpack, jest, ts-node, etc.) is configured to process both `.js` and `.ts` files prior to code conversion.
- The AI MUST execute module conversion in strict bottom-up order (Leaves to Roots):
  1. Third-party dependencies (installing `@types`).
  2. External API response typings.
  3. Internal utility modules.
  4. Intermediate business logic modules.
  5. Entry points.
  6. Unit Tests.

### Handling Conversion Errors
- When converting a class to `.ts` and encountering missing property errors (`Property 'X' does not exist on type 'Y'`), the AI MUST explicitly declare all member variables at the top of the class. If the type cannot be immediately deduced, the AI MUST temporarily type them as `any` and refine them subsequently.
- When encountering values with changing types (e.g., building an object piecemeal), the AI MUST either refactor the code to build the object all at once, or apply a temporary type assertion (e.g., `const state = {} as State;`).
- When encountering a third-party dependency lacking bundled types, the AI MUST install its `@types` package as a `devDependency` and ensure the major and minor version numbers match the library's version.

### Finalizing Migration (`noImplicitAny`)
- The AI MUST NOT consider a migration complete until `noImplicitAny` is set to `true` in `tsconfig.json` and all resulting errors are resolved.
- When fixing `noImplicitAny` errors, the AI MUST scrutinize variables that implicitly received the `any` type and assign them accurate, precise types (e.g., replacing a presumed `any` index array with `number[]` or `[number, number][]`).

# @Workflow
1. **Prepare and Modernize**: Analyze the JavaScript codebase to remove dead code. Update legacy JS syntax (CommonJS, `var`, prototypes, callbacks) to modern ECMAScript standards (ESM, `let`/`const`, classes, `async`/`await`).
2. **Configure Interoperability**: Update `tsconfig.json` to include `"allowJs": true`. Verify that the project's build and test tooling (e.g., `ts-loader`, `ts-jest`) successfully processes the mixed codebase.
3. **Identify Dependency Graph**: Map the import structure of the project. Identify third-party dependencies and internal leaf nodes (files that do not import any other local files).
4. **Type External Boundaries**: Install `@types` packages for all third-party dependencies. Create TypeScript interfaces/types for external API payloads.
5. **Convert Modules (Bottom-Up)**: Rename `.js` files to `.ts` starting from the leaves. 
    - Resolve missing class property declarations.
    - Translate JSDoc annotations to TS annotations and clean up the JSDoc.
    - Suppress architectural design flaws with `TODO` comments or type assertions rather than refactoring logic.
6. **Convert Tests**: Rename and type-check test files only after all production dependencies they rely on have been converted.
7. **Enforce Strictness**: Enable `"noImplicitAny": true` in `tsconfig.json`. Iteratively resolve all surfaced implicit `any` errors up the dependency graph until the compiler passes cleanly.

# @Examples (Do's and Don'ts)

### ECMAScript Modules over CommonJS
- **[DO]**:
  ```typescript
  import * as utils from './utils';
  export const name = 'Module B';
  ```
- **[DON'T]**:
  ```javascript
  const utils = require('./utils');
  module.exports = { name: 'Module B' };
  ```

### ES2015 Classes over Prototypes
- **[DO]**:
  ```typescript
  class Person {
    first: string;
    last: string;
    constructor(first: string, last: string) {
      this.first = first;
      this.last = last;
    }
    getName() {
      return `${this.first} ${this.last}`;
    }
  }
  ```
- **[DON'T]**:
  ```javascript
  function Person(first, last) {
    this.first = first;
    this.last = last;
  }
  Person.prototype.getName = function() {
    return this.first + ' ' + this.last;
  }
  ```

### Converting JSDoc to TypeScript
- **[DO]**:
  ```typescript
  /**
   * Calculates the double of a number.
   */
  function double(num: number): number {
    return 2 * num;
  }
  ```
- **[DON'T]**:
  ```typescript
  /**
   * @param {number} num
   * @returns {number}
   */
  function double(num: number): number {
    return 2 * num;
  }
  ```

### JSDoc Type Assertions in JS Files (`@ts-check`)
- **[DO]**:
  ```javascript
  // @ts-check
  const ageEl = /** @type {HTMLInputElement} */(document.getElementById('age'));
  ageEl.value = '12';
  ```
- **[DON'T]**:
  ```javascript
  // @ts-check
  const ageEl = document.getElementById('age');
  ageEl.value = '12'; // Error: Property 'value' does not exist on type 'HTMLElement'
  ```

### Resolving Changing Types (Object Creation)
- **[DO]**:
  ```typescript
  interface State { name: string; capital: string; }
  // Approach A: Build all at once
  const state1: State = { name: 'New York', capital: 'Albany' };
  
  // Approach B: Type assertion (if piecemeal is unavoidable during migration)
  const state2 = {} as State;
  state2.name = 'New York';
  state2.capital = 'Albany';
  ```
- **[DON'T]**:
  ```typescript
  const state = {};
  state.name = 'New York'; // Error
  state.capital = 'Albany'; // Error
  ```

### Resolving Undeclared Class Members
- **[DO]**:
  ```typescript
  class Greeting {
    greeting: string;
    name: string;
    constructor(name: string) {
      this.greeting = 'Hello';
      this.name = name;
    }
  }
  ```
- **[DON'T]**:
  ```typescript
  class Greeting {
    constructor(name: string) {
      this.greeting = 'Hello'; // Error: Property 'greeting' does not exist
      this.name = name;        // Error: Property 'name' does not exist
    }
  }
  ```