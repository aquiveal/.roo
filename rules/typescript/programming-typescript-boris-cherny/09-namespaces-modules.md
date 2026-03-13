# @Domain
These rules MUST be activated when the AI is writing, refactoring, or analyzing TypeScript/JavaScript files involving encapsulation, imports/exports, dynamic lazy-loading, namespaces, module resolution configurations (`tsconfig.json`), or declaration merging.

# @Vocabulary
- **ES2015 Modules**: The modern standard for JavaScript modularity using `import` and `export` statements. Statically analyzable.
- **CommonJS / AMD**: Legacy module standards. CommonJS uses `require` and `module.exports` (synchronous); AMD uses `define` (asynchronous).
- **UMD**: Universal Module Definition, a mix of CommonJS, AMD, and globals.
- **Dynamic Imports**: Asynchronously loading modules using the `import('path')` function to facilitate code splitting and lazy loading.
- **Module Mode**: A parsing mode where the file contains at least one `import` or `export`. Top-level declarations are scoped locally to the file.
- **Script Mode**: A parsing mode where the file lacks any `import` or `export`. Top-level declarations are exposed to the global namespace.
- **Namespace**: A TypeScript-specific encapsulation mechanism using the `namespace` keyword. Compiles to globally accessible IIFEs (Immediately Invoked Function Expressions).
- **Declaration Merging**: TypeScript's behavior of automatically combining multiple declarations that share the same name within the same scope (e.g., merging a type and a value to form a Companion Object).
- **Companion Object Pattern**: Merging a type and a value under the same name in the same scope, allowing consumers to import both simultaneously.
- **moduleResolution**: A `tsconfig.json` compiler option determining how the compiler locates module files. Supports `node` and `classic` modes.

# @Objectives
- Enforce the use of ES2015 module syntax (`import`/`export`) over legacy module systems or TypeScript namespaces.
- Ensure strict type safety is maintained when utilizing dynamic imports.
- Configure and manage TypeScript's `moduleResolution` and module interoperability settings correctly.
- Safely leverage declaration merging to group related types and values.
- Accurately distinguish and manage the boundaries between Module Mode and Script Mode.

# @Guidelines
- **ES2015 Module Syntax Rules**:
  - The AI MUST use ES2015 `import` and `export` statements for all module interactions.
  - The AI MUST NOT use CommonJS `require()` or `module.exports` unless specifically modifying a legacy NodeJS script that cannot be compiled via TSC.
  - The AI MAY export both a type and a value with the same name from a module; TypeScript will correctly resolve the usage context.
- **Dynamic Imports Rules**:
  - The AI MUST set `"module": "esnext"` in `tsconfig.json` when utilizing dynamic imports.
  - The AI MUST preserve type safety when using `import()` by either passing a static string literal directly OR by manually annotating the module's signature using `typeof import('...')` when passing a computed variable.
- **CommonJS/AMD Interoperability Rules**:
  - When importing a default export from a CommonJS module, the AI MUST either use a wildcard import (`import * as fs from 'fs'`) OR ensure `"esModuleInterop": true` is set in `tsconfig.json` to allow default imports (`import fs from 'fs'`).
- **Module Mode vs. Script Mode Rules**:
  - The AI MUST explicitly add an `import` or `export` statement (even an empty `export {}`) to force a file into Module Mode if it should not leak its top-level variables into the global namespace.
  - The AI MUST ONLY use Script Mode (no imports/exports) for quick browser prototypes (`"module": "none"`) or specific global ambient type declarations.
- **Namespace Rules**:
  - The AI MUST PREFER standard ES2015 modules over `namespace` blocks. Modules provide explicit dependencies, better static analysis, and dead code elimination.
  - If namespaces MUST be used, the AI MUST recognize that they do not respect the `tsconfig.json` module setting and always compile to global variables via IIFEs.
  - When creating namespace aliases for deeply nested namespaces, the AI MUST use the `import alias = A.B.C` syntax. The AI MUST NOT use destructuring syntax for namespace aliasing.
  - The AI MUST NOT define colliding exports within namespaces, EXCEPT for overloaded ambient function declarations.
- **Declaration Merging Rules**:
  - The AI SHOULD utilize declaration merging to group types and values sharing the same name (Companion Object Pattern).
- **moduleResolution Configuration Rules**:
  - The AI MUST set `"moduleResolution": "node"` in `tsconfig.json`.
  - The AI MUST NOT EVER use `"moduleResolution": "classic"`.
  - The AI MUST recognize that in `node` mode, TypeScript looks for files with extensions in the following strict order: `.ts`, `.tsx`, `.d.ts`, `.js`. It also reads the `types` property in a dependency's `package.json`.

# @Workflow
1. **Module System Initialization**: Check `tsconfig.json`. Ensure `"moduleResolution": "node"` and `"esModuleInterop": true` are present. If dynamic imports are required, ensure `"module": "esnext"`.
2. **Encapsulation Selection**: Choose ES2015 modules. Avoid `namespace` constructs entirely unless extending an existing legacy namespace architecture.
3. **Scoping Validation**: Verify the presence of `import` or `export` statements in standard files to guarantee Module Mode execution and prevent global namespace pollution.
4. **Import Construction**:
   - For static dependencies: Use ES2015 `import { x } from 'y'` or `import x from 'y'`.
   - For lazy-loaded dependencies: Use `await import('y')`. If the path is dynamic, scavenge the type using `typeof import('static-path')` to type the dynamically loaded module.
5. **API Exportation**: Export discrete types and values. If a type and a factory/utility object are strongly coupled, export both under the exact same name to utilize declaration merging.

# @Examples (Do's and Don'ts)

**Dynamic Imports**
- [DO]:
  ```typescript
  // Type-safe dynamic import using a string literal
  let locale = await import('locale_us-en');

  // Type-safe dynamic import with a computed path using typeof
  import { locale } from './locales/locale-us'; // Imported only for type scavenging
  async function loadLocale(userLocale: string) {
    let path = `./locales/locale-${userLocale}`;
    let loadedLocale: typeof locale = await import(path);
  }
  ```
- [DON'T]:
  ```typescript
  // Loses type safety because path is computed and not annotated
  async function loadLocale(userLocale: string) {
    let path = `./locales/locale-${userLocale}`;
    let loadedLocale = await import(path); // loadedLocale is typed as 'any'
  }
  ```

**Module Resolution Configuration**
- [DO]:
  ```json
  {
    "compilerOptions": {
      "moduleResolution": "node",
      "esModuleInterop": true
    }
  }
  ```
- [DON'T]:
  ```json
  {
    "compilerOptions": {
      "moduleResolution": "classic"
    }
  }
  ```

**Namespaces vs Modules**
- [DO]:
  ```typescript
  // Prefer ES2015 Modules
  export function get(url: string) { /* ... */ }
  import { get } from './Network';
  ```
- [DON'T]:
  ```typescript
  // Avoid Namespaces for module-like encapsulation
  namespace Network {
    export function get(url: string) { /* ... */ }
  }
  Network.get('...');
  ```

**Namespace Aliasing (If namespaces are strictly required)**
- [DO]:
  ```typescript
  namespace A { export namespace B { export namespace C { export let d = 3; } } }
  import d = A.B.C.d;
  ```
- [DON'T]:
  ```typescript
  namespace A { export namespace B { export namespace C { export let d = 3; } } }
  import { d } from A.B.C; // Destructuring alias is not supported for namespaces
  ```

**CommonJS Interop (Without esModuleInterop)**
- [DO]:
  ```typescript
  import * as fs from 'fs';
  fs.readFile('some/file.txt');
  ```
- [DON'T]:
  ```typescript
  import fs from 'fs'; // Will fail at runtime/compile-time if esModuleInterop is false
  fs.readFile('some/file.txt');
  ```

**Module Mode vs Script Mode**
- [DO]:
  ```typescript
  // module.ts
  export {}; // Forces file into Module Mode, keeping 'foo' local
  const foo = 'bar';
  ```
- [DON'T]:
  ```typescript
  // script.ts
  const foo = 'bar'; // No imports/exports. 'foo' leaks into the global namespace
  ```