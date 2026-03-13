# @Domain
These rules MUST be activated when the AI is tasked with:
- Interoperating between TypeScript and untyped JavaScript files.
- Writing, editing, or maintaining type declarations (`.d.ts` files).
- Migrating a legacy JavaScript codebase to TypeScript.
- Importing and configuring third-party JavaScript modules that lack built-in TypeScript definitions.
- Configuring `tsconfig.json` for mixed JavaScript/TypeScript environments (`allowJs`, `checkJs`, `typeRoots`, `types`).

# @Vocabulary
- **Type Declaration (`.d.ts`)**: A file that contains only types (no implementations) used to describe the shape of JavaScript code to the TypeScript compiler.
- **Ambient Declaration**: A declaration using the `declare` keyword that tells TypeScript a value (variable, class, function) exists somewhere in the global JavaScript environment at runtime.
- **Ambient Module Declaration**: An ambient declaration using `declare module 'module-name'` to provide types for a third-party JavaScript module.
- **DefinitelyTyped**: A community-maintained, centralized repository for ambient module declarations for open source projects, published to NPM under the `@types` scope.
- **JSDoc**: Specially formatted comments (e.g., `/** @param {string} word */`) in JavaScript files that the TypeScript compiler can read to infer types when `checkJs` is enabled.
- **Script-mode File**: A `.ts` or `.d.ts` file that does not contain any top-level `import` or `export` statements. Variables and types declared here are globally available to the entire project.

# @Objectives
- Safely model untyped JavaScript behavior in TypeScript without executing runtime code in declaration files.
- Enable smooth, iterative migrations from JavaScript to TypeScript using incremental configuration flags and tracking aliases.
- Correctly locate or stub type definitions for third-party libraries to eliminate `any` types and prevent compilation errors.
- Preserve explicit boundaries between compile-time type declarations and runtime JavaScript implementations.

# @Guidelines

### Writing Type Declarations (`.d.ts`)
- The AI MUST NOT include any values or runtime implementations (e.g., function bodies, default parameter values, object implementations) inside `.d.ts` files.
- The AI MUST use the `declare` keyword for top-level values (e.g., `declare let`, `declare function`, `declare class`) to affirm that the value exists at runtime.
- The AI MUST NOT use the `declare` keyword for top-level types and interfaces (e.g., use `type Foo = ...` or `interface Bar {...}`).
- The AI MUST ensure ambient variable and type declarations intended for global use are placed in a script-mode file (no top-level `import` or `export` statements).

### Migrating JavaScript to TypeScript
- When performing a quick migration, the AI MUST use an explicit, easily searchable alias for `any` (e.g., `type TODO_FROM_JS_TO_TS_MIGRATION = any`) instead of implicit or explicit `any` types, to track missing types.
- When annotating existing JavaScript files without renaming them to `.ts`, the AI MUST use JSDoc comments (`/** @param {type} name */`) immediately preceding the function or variable.
- To suppress type checking for a specific overly complex JavaScript file during migration, the AI MUST use the `// @ts-nocheck` directive at the top of the file.
- To enable type checking for a single JavaScript file, the AI MUST use the `// @ts-check` directive at the top of the file.

### Handling Third-Party JavaScript
- When a third-party module lacks type definitions, the AI MUST search for and install the corresponding `@types/` package as a `devDependency` (e.g., `npm install @types/lodash --save-dev`).
- If an `@types/` package does not exist, the AI MUST create a `types.d.ts` file and declare an ambient module.
- For a quick bypass of an untyped module, the AI MUST write an empty ambient module declaration: `declare module 'unsafe-module-name'`.
- To safely type an untyped module, the AI MUST write a populated ambient module declaration: `declare module 'safe-module-name' { export function foo(): void; }`.
- When loading non-JavaScript files via bundlers (e.g., JSON, CSS), the AI MUST create a wildcard module declaration (e.g., `declare module '*.css' { let css: CSSRuleList; export default css; }`).
- The AI MUST NOT use `// @ts-ignore` to whitelist untyped imports unless explicitly instructed to perform a quick-and-dirty hot patch, as it types the entire module as `any`.

### Configuring `tsconfig.json`
- The AI MUST configure `typeRoots` (e.g., `["./typings", "./node_modules/@types"]`) if local, global ambient type declarations need to be resolved alongside NPM `@types`.
- The AI MUST configure `types` (e.g., `["react"]`) if the project must strictly limit which third-party global type declarations are loaded.

# @Workflow

### Step-by-Step JS to TS Migration Process
When tasked with migrating a legacy JavaScript codebase to TypeScript, the AI MUST execute the following steps in order:
1. **Enable TS in JS**: Add `{"allowJs": true}` to `tsconfig.json` so the TypeScript compiler can process existing `.js` files.
2. **Enable Typechecking for JS**: Add `{"checkJs": true}` to `tsconfig.json` to allow TypeScript to infer types and read JSDoc comments in `.js` files. (Temporarily set `"noImplicitAny": false` if there is too much noise).
3. **Annotate JS (Optional)**: If renaming is not yet permitted, write JSDoc annotations to create islands of typed JavaScript.
4. **Rename and Fix**: Rename `.js` files to `.ts` one by one. Resolve type errors immediately. For intractable types, use a designated alias like `TODO_FROM_JS_TO_TS_MIGRATION`.
5. **Enforce Strictness**: Once a critical mass of files is migrated, set `"allowJs": false`, `"checkJs": false`, and enable strict mode flags (e.g., `"strictNullChecks": true`, `"noImplicitAny": true`).

### Step-by-Step Third-Party Module Typing
When importing a third-party module throws an implicit `any` error, the AI MUST:
1. **Check Bundled Types**: Verify if the package natively includes `.d.ts` files. If so, ensure `tsconfig.json` module resolution is correctly set to `node`.
2. **Install @types**: Run `npm install @types/<package-name> --save-dev`.
3. **Declare Ambient Module**: If no `@types` exist, create a `types.d.ts` file in the project root/src. Add `declare module '<package-name>' { ... }` and export the necessary types and functions matching the library's API.

# @Examples (Do's and Don'ts)

### Writing Ambient Variable Declarations
- **[DO]**: Use `declare` and omit values.
  ```typescript
  // globals.d.ts
  declare let process: {
    env: {
      NODE_ENV: 'development' | 'production'
    }
  }
  ```
- **[DON'T]**: Include runtime implementations or assignments in a `.d.ts` file.
  ```typescript
  // globals.d.ts
  declare let process = { // Anti-pattern: Cannot assign values in ambient declarations
    env: {
      NODE_ENV: 'production'
    }
  }
  ```

### Writing Ambient Module Declarations
- **[DO]**: Wrap exported types in a `declare module` block for untyped third-party packages.
  ```typescript
  // types.d.ts
  declare module 'nearby-ferret-alerter' {
    export default function alert(loudness: 'soft' | 'loud'): Promise<void>
    export function getFerretCount(): Promise<number>
  }
  ```
- **[DON'T]**: Use `// @ts-ignore` to bypass untyped imports if building for safety.
  ```typescript
  // app.ts
  // @ts-ignore
  import Unsafe from 'nearby-ferret-alerter' // Anti-pattern: Unsafe and entirely 'any' typed
  ```

### JSDoc Typing in JavaScript Files
- **[DO]**: Use JSDoc to type parameters and return values in unmigrated `.js` files.
  ```javascript
  // utils.js
  /**
   * @param word {string} An input string to convert
   * @returns {string} The string in PascalCase
   */
  export function toPascalCase(word) {
    return word.replace(/\w+/g, ([a, ...b]) => a.toUpperCase() + b.join('').toLowerCase())
  }
  ```
- **[DON'T]**: Use inline TypeScript syntax in `.js` files.
  ```javascript
  // utils.js
  export function toPascalCase(word: string): string { // Anti-pattern: Invalid syntax in .js files
    return word.toUpperCase()
  }
  ```

### Quick Migration Type Stubs
- **[DO]**: Use an explicit alias to track where `any` was used as a shortcut during migration.
  ```typescript
  // globals.ts
  export type TODO_FROM_JS_TO_TS_MIGRATION = any;

  // MyUtil.ts
  import { TODO_FROM_JS_TO_TS_MIGRATION } from './globals';
  export function merge(widget: TODO_FROM_JS_TO_TS_MIGRATION) { ... }
  ```
- **[DON'T]**: Leave implicit or raw `any` types scattering the codebase, permanently losing track of migration debt.
  ```typescript
  // MyUtil.ts
  export function merge(widget: any) { ... } // Anti-pattern: Untrackable technical debt
  ```