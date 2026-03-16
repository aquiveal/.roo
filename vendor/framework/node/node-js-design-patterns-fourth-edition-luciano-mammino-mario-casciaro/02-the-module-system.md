# @Domain
Node.js module creation, application structuring, import/export management, interoperability between ECMAScript Modules (ESM) and CommonJS (CJS), and TypeScript module configuration for Node.js environments.

# @Vocabulary
- **Module System**: The syntax and tools used to define, organize, and load modules (e.g., ESM, CommonJS, AMD, UMD).
- **Revealing Module Pattern**: A foundational JavaScript pattern utilizing an Immediately Invoked Function Expression (IIFE) to create a private scope and selectively export a public API.
- **CommonJS (CJS)**: The legacy Node.js module system. Uses `require()` for synchronous/dynamic imports and `module.exports` for exports. 
- **ECMAScript Modules (ESM)**: The modern, standard JavaScript module system. Uses `import` and `export` statements. It is static, asynchronous, and operates implicitly in strict mode.
- **Module Identifier / Specifier**: The string path used in an import statement. Can be a Relative Specifier (`./file.js`), Absolute Specifier (`file:///path`), Bare Specifier (`fastify`), or Deep Import Specifier (`fastify/lib/logger.js`).
- **Namespace Import**: Importing all exported members of a module into a single object namespace (e.g., `import * as logger from './logger.js'`).
- **Dynamic Import (Async Import)**: Using the `import()` operator at runtime. It returns a Promise resolving to the module object.
- **Read-only Live Bindings**: ESM mechanism where imported entities are read-only references to the original exported values. If the exporting module mutates the value internally, the importing module sees the updated value, but the importing module cannot reassign it.
- **Tree Shaking / Dead Code Elimination**: Build-time optimization that removes unused exported code. Hindered by Default Exports.
- **Monkey Patching**: Modifying existing objects or modules at runtime. In Node.js, this refers to altering a loaded module's properties.
- **Top-level Await**: The ability to use the `await` keyword at the top level of an ES module, outside of an async function.
- **Load Phases (ESM)**: The three steps ESM uses to load: Construction/Parsing (building the dependency graph), Instantiation (linking memory references), and Evaluation (executing code).

# @Objectives
- Enforce the use of ECMAScript Modules (ESM) as the default standard for all new Node.js development.
- Maximize code maintainability, static analysis, and tree-shaking compatibility by strictly utilizing Named Exports over Default Exports.
- Guarantee safe interoperability between ESM and legacy CommonJS code without causing syntax or runtime errors.
- Ensure TypeScript is correctly configured to align with modern Node.js module resolution standards.
- Prevent unpredictable side effects and loss of type safety by strictly avoiding monkey patching.

# @Guidelines

## General Module Configuration
- The AI MUST configure new Node.js projects to use ESM by adding `"type": "module"` in the nearest `package.json`.
- When dealing with ambiguous files where `"type": "module"` is absent, the AI MUST use the `.mjs` extension to force ESM, or `.cjs` to force CommonJS.

## Import & Export Syntax
- The AI MUST ALWAYS prefer Named Exports (`export function foo() {}`) over Default Exports (`export default function foo() {}`). Default exports obscure API discoverability, hinder IDE refactoring, and inhibit dead code elimination.
- The AI MUST use the `node:` prefix for all Node.js core modules (e.g., `import { readFile } from 'node:fs'`).
- The AI MUST explicitly include the file extension (e.g., `.js`) for all relative and absolute local imports within ESM files.
- The AI MUST utilize Namespace Imports (`import * as moduleName`) only when the consumer legitimately requires access to the entire module API surface.

## Dynamic Imports & Execution Flow
- The AI MUST use the static `import` syntax at the top level of the file for predictable, standard dependencies.
- The AI MUST use the dynamic `import()` operator only when the module identifier is generated at runtime, or when a module must be loaded conditionally/asynchronously to save resources.
- The AI MUST leverage Top-level `await` in ESM for asynchronous initialization logic (e.g., database connections, fetching configurations) rather than wrapping initialization in async IIFEs.

## CommonJS and ESM Interoperability
- The AI MUST NOT use CommonJS global variables (`require`, `exports`, `module.exports`, `__filename`, `__dirname`) inside an ES Module.
- To replicate `__filename` and `__dirname` in ESM (Node >= 20.11.0), the AI MUST use `import.meta.filename` and `import.meta.dirname`. (For older Node.js versions, use `fileURLToPath(import.meta.url)` and `dirname()`).
- To import a CommonJS module into an ES Module, the AI MUST use the default import syntax and destructure the required properties: `import pkg from './cjs-module.cjs'; const { feature } = pkg;`.
- If an ES Module requires programmatic access to a `require()` function, the AI MUST instantiate it using `import { createRequire } from 'node:module'; const require = createRequire(import.meta.url);`.
- To import an ES Module into a CommonJS module, the AI MUST use the dynamic `import()` operator. `require()` MUST NOT be used to load an ES Module.

## Importing JSON in ESM
- The AI MUST import JSON files in ESM using import attributes: `import data from './sample.json' with { type: 'json' };`.
- Alternatively, if dynamic loading is required, use `await import('./sample.json', { with: { type: 'json' } })` or the `createRequire` method.

## Anti-Patterns & Constraints
- The AI MUST NOT use Default Exports as “god objects” that pack multiple disparate functions into a single export. 
- The AI MUST AVOID monkey patching modules (modifying the properties of an imported module). This causes unpredictable side effects, breaks pure ESM read-only live bindings, and destroys TypeScript type safety.
- The AI MUST NOT use static `import` statements inside blocks (e.g., `if` statements). It will cause a SyntaxError.

## TypeScript Configuration for Node.js
- When working with TypeScript in Node.js, the AI MUST configure `tsconfig.json` with `"module": "NodeNext"` and `"moduleResolution": "NodeNext"`.
- The AI MUST enable `"verbatimModuleSyntax": true` in TypeScript to ensure that input imports/exports directly map to the emitted JavaScript without silent transformations.
- The AI MUST use the `@types/node` package as a development dependency to provide standard definitions for the Node.js API.

# @Workflow
1. **Module System Verification**: Check `package.json` for `"type": "module"`. If absent in a new project, insert it.
2. **Import construction**:
   - Prefix all core modules with `node:`.
   - Append `.js` extensions to local relative imports.
3. **Export construction**: Define functionality using explicit `export const` or `export function`. Validate that no `export default` is used unless specifically requested for a framework requirement.
4. **Environment variable replacement**: Scan code for `__dirname` and `__filename`. Replace them with `import.meta.dirname` and `import.meta.filename` if the file is ESM.
5. **Data loading check**: If JSON data is needed, implement the `with { type: 'json' }` syntax.
6. **Interoperability check**: If interacting with CJS code from ESM, wrap the CJS import in a default import and destructure, or use `createRequire`.
7. **TypeScript validation**: If TS is used, enforce `NodeNext` configurations in `tsconfig.json`.

# @Examples (Do's and Don'ts)

### Defining and Importing Modules
[DO]
```javascript
// logger.js
export function log(message) {
  console.log(message)
}

export const LEVELS = { error: 0, info: 1 }

// main.js
import { log } from './logger.js'
import { readFile } from 'node:fs/promises'

log('System initialized')
```

[DON'T]
```javascript
// logger.js
export default {
  log: (message) => console.log(message),
  LEVELS: { error: 0, info: 1 }
}

// main.js
import logger from './logger' // Missing .js extension
import { readFile } from 'fs/promises' // Missing node: prefix

logger.log('System initialized')
```

### Accessing Directory Paths in ESM
[DO]
```javascript
import { join } from 'node:path'

const filePath = join(import.meta.dirname, 'data.txt')
```

[DON'T]
```javascript
import { join } from 'path'

const filePath = join(__dirname, 'data.txt') // ReferenceError: __dirname is not defined
```

### Importing CommonJS into ESM
[DO]
```javascript
import someCjsModule from './legacy.cjs'
const { specificFeature } = someCjsModule
```

[DON'T]
```javascript
import { specificFeature } from './legacy.cjs' // SyntaxError: Named export not found
```

### Importing JSON in ESM
[DO]
```javascript
import config from './config.json' with { type: 'json' }
```

[DON'T]
```javascript
import config from './config.json' // TypeError: Module needs an import attribute
```

### Monkey Patching (Extending Object Functionality)
[DO]
```javascript
// wrapper.js
import { logger } from './logger.js'

export const coloredLogger = {
  ...logger,
  info: (msg) => console.log(`\x1b[32m${msg}\x1b[0m`)
}
```

[DON'T]
```javascript
// monkey-patch.js
import * as loggerModule from './logger.js'

// TypeError: Cannot assign to read only property
loggerModule.logger.info = (msg) => console.log(`\x1b[32m${msg}\x1b[0m`)
```

### TypeScript Configuration (tsconfig.json)
[DO]
```json
{
  "compilerOptions": {
    "target": "es2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "verbatimModuleSyntax": true
  }
}
```

[DON'T]
```json
{
  "compilerOptions": {
    "target": "es6",
    "module": "CommonJS",
    "moduleResolution": "node"
  }
}
```