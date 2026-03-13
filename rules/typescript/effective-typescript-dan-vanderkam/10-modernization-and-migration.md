@Domain
Tasks involving migrating legacy JavaScript to TypeScript, modernizing older JavaScript codebases, incrementally adding types to JavaScript using JSDoc and `@ts-check`, configuring TypeScript build tools for mixed JS/TS environments, or resolving type errors during a codebase transition.

@Vocabulary
- **Transpiler**: A compiler that takes modern JavaScript/TypeScript and converts it to older, more widely supported JavaScript versions (e.g., ES5).
- **Leaf Nodes**: Modules at the bottom of a dependency graph that do not import any other local modules (often utility files).
- **Ambient Symbols**: Global variables or objects defined outside the current module (e.g., via HTML `<script>` tags) that require a `types.d.ts` declaration file.
- **Aspirational JSDoc**: JSDoc comments intended to describe types but which are factually inaccurate, loosely defined, or misaligned with the actual DOM/runtime implementation.
- **Topological Sort**: A method of ordering a dependency graph from the bottom-up (leaves to roots) to dictate the sequence in which modules should be migrated.
- **Fail Open / Fail Closed**: The dilemma of whether to allow execution with potential missed optimizations/actions (fail closed) or guarantee execution at the cost of performance/redundancy (fail open).

@Objectives
- Execute seamless, incremental migrations from JavaScript to TypeScript without breaking runtime behavior or test suites.
- Modernize legacy JavaScript syntax (ES2015+) as a foundational step to facilitate TypeScript adoption.
- Strictly separate the act of migrating to TypeScript from architectural refactoring; prioritize adding types over fixing code smells.
- Incrementally increase type safety using `@ts-check`, JSDoc, and `allowJs` before fully transitioning to `.ts` files.
- Achieve a strict, fully typed codebase by enforcing `noImplicitAny` as the final milestone of the migration.

@Guidelines
- **Pre-Migration Cleanup**: The AI MUST perform dead code elimination and remove deprecated features before starting a TypeScript migration.
- **Hold Off on Framework Refactors**: The AI MUST NOT perform large architectural refactors (e.g., converting jQuery to React) until the TypeScript migration is fully complete.
- **No Refactoring During Migration**: When converting a `.js` file to `.ts`, the AI MUST NOT fix bad designs, code smells, or architectural flaws. The AI MUST add a `// TODO` comment or use an expedient type assertion (`as any`, `as Type`) or `@ts-expect-error` to push past the issue and maintain migration momentum.
- **Modern Syntax Enforcement**: When writing or modernizing JavaScript/TypeScript, the AI MUST use:
  - ECMAScript modules (`import`/`export`) instead of CommonJS (`require`), AMD, or namespaces.
  - ES2015 `class` syntax instead of prototype-based object models.
  - `let` and `const` instead of `var`.
  - `for-of` loops or array methods (`map`, `filter`) instead of C-style `for(;;)` loops.
  - `async` and `await` instead of callbacks or raw Promises.
  - Arrow functions instead of function expressions to preserve `this` context.
  - Default parameter values in the function signature.
  - Compact object literals and destructuring assignments.
  - `Map` and `Set` instead of plain objects for associative arrays.
  - Optional chaining (`?.`) and nullish coalescing (`??`).
- **Strict Mode**: The AI MUST NOT add `"use strict"` to TypeScript files, as TypeScript naturally enforces strict mode and emits it during module compilation.
- **Experimenting with Types (@ts-check)**: When directed to experiment with typing in a `.js` file, the AI MUST add `// @ts-check` to the top of the file.
- **Ambient Globals**: The AI MUST declare undeclared globals identified by `@ts-check` using `let`/`const` or by creating a `types.d.ts` file containing `declare let globalName: Type;`.
- **Third-Party Types**: The AI MUST install `@types/package-name` for unknown libraries as `devDependencies` to ensure proper type checking.
- **JSDoc Type Assertions**: To assert a type in a `.js` file using `@ts-check`, the AI MUST use the exact JSDoc syntax: `/** @type {TargetType} */(expression)` including the wrapping parentheses.
- **JSDoc to TS Conversion**: When converting a `.js` file with JSDoc to `.ts`, the AI MUST translate the JSDoc types into inline TypeScript annotations and subsequently delete the JSDoc type tags to avoid redundancy.
- **Undeclared Class Members**: When migrating classes to TypeScript, the AI MUST explicitly declare all class properties and their types before the constructor.
- **Values with Changing Types**: If an object is built piecemeal causing type errors, the AI MUST either build the object all at once, or use an expedient type assertion (`const obj = {} as TargetType;`) and leave a TODO to refactor later.

@Workflow
1. **Preparation**: Eliminate dead code, update third-party dependencies, and modernize JS syntax (Prototypes to Classes, CommonJS to ES Modules).
2. **Build Integration**: Enable the `allowJs` compiler option in `tsconfig.json`. Configure the build chain (webpack `ts-loader`, `ts-node`, `ts-jest`, etc.) to process both `.ts` and `.js` files. Ensure all existing tests pass.
3. **External Dependencies**: Identify third-party dependencies and external API calls. Install `@types/` packages for libraries and write explicit type interfaces for external API responses.
4. **Graph Analysis**: Perform a topological sort of the project's dependency graph. Identify leaf nodes (utility modules with no internal imports).
5. **Bottom-Up Migration**: Iterate through the dependency graph from bottom (leaf nodes) to top (entry points). For each file:
    a. Rename `.js` to `.ts`.
    b. Declare missing class members.
    c. Convert JSDoc annotations to TS annotations.
    d. Use expedient type assertions (`as any`) or `@ts-expect-error` to bypass poorly designed code without refactoring it.
6. **Migrate Tests**: Migrate unit tests last. Verify that runtime behavior remains completely unchanged.
7. **Strictness Enforcement**: Once all files are converted, enable `noImplicitAny` in the local `tsconfig.json`. Iteratively fix all surfaced implicit `any` errors going back up the dependency graph. Do not consider the migration complete until `noImplicitAny` generates zero errors.

@Examples (Do's and Don'ts)

**Modernizing Classes**
- [DO]:
```typescript
class Person {
  constructor(first: string, last: string) {
    this.first = first;
    this.last = last;
  }
  getName() {
    return `${this.first} ${this.last}`;
  }
}
```
- [DON'T]:
```javascript
function Person(first, last) {
  this.first = first;
  this.last = last;
}
Person.prototype.getName = function() {
  return this.first + ' ' + this.last;
}
```

**JSDoc Type Assertions in JavaScript (@ts-check)**
- [DO]:
```javascript
// @ts-check
const ageEl = /** @type {HTMLInputElement} */(document.getElementById('age'));
ageEl.value = '12';
```
- [DON'T]:
```javascript
// @ts-check
const ageEl = document.getElementById('age');
ageEl.value = '12'; // Error: Property 'value' does not exist on type 'HTMLElement'
```

**Class Member Declarations in TypeScript**
- [DO]:
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
- [DON'T]:
```typescript
class Greeting {
  constructor(name: string) {
    this.greeting = 'Hello'; // Error: Property 'greeting' does not exist
    this.name = name; // Error: Property 'name' does not exist
  }
}
```

**Handling Poorly Designed Code During Migration**
- [DO]:
```typescript
interface State {
  name: string;
  capital: string;
}
// Expedient assertion to maintain migration momentum without architectural refactoring
const state = {} as State; 
state.name = 'New York';
state.capital = 'Albany';
// TODO: Refactor to build object all at once
```
- [DON'T]:
```typescript
const state = {};
state.name = 'New York'; // Error: Property 'name' does not exist on type '{}'
// (Stopping the migration to embark on a massive architectural refactor to fix this pattern)
```