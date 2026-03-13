## @Domain
Building, configuring, optimizing, and publishing TypeScript applications across various target environments (Browser, NodeJS Server, NPM libraries), including managing `tsconfig.json` compiler options, build artifacts, project references, and module resolution.

## @Vocabulary
- **Transpile**: The automatic conversion of newer JavaScript/TypeScript syntax (e.g., `class`, `async/await`) into an older JavaScript version (e.g., ES5) that older platforms can execute natively.
- **Polyfill**: Providing an implementation for standard library features (e.g., `Promise`, `Map`, `Array.prototype.includes`) that are missing in the target JavaScript runtime. 
- **Isomorphic**: JavaScript/TypeScript programs designed to run identically on both the server and the client/browser.
- **Source Maps (`.js.map`)**: Files that link generated JavaScript back to the specific line and column of the original TypeScript source code, essential for debugging.
- **Declaration Maps (`.d.ts.map`)**: Files linking generated type declarations back to their source, used primarily to speed up compilation in project references.
- **Project References**: A TSC feature that splits large TypeScript codebases into smaller, independently compiled subprojects to drastically speed up incremental compile times.
- **Import Elision**: TypeScript's behavior of omitting an import statement from the generated JavaScript if the imported module is only used in a type position.
- **Triple-Slash Directives**: Specially formatted TypeScript comments (`/// <directive ... />`) that serve as direct instructions to the TypeScript Compiler (TSC) for module naming or ambient dependency resolution.

## @Objectives
- The AI MUST configure `tsconfig.json` settings strictly according to the deployment target (Browser, Server, or NPM library).
- The AI MUST separate the concepts of transpilation (`target`) and polyfilling (`lib`); it MUST explicitly provide polyfills for features not supported by the runtime, as TSC does not polyfill automatically.
- The AI MUST enforce a modular project layout that separates source code from generated artifacts.
- The AI MUST optimize build times for large codebases by implementing Project References.
- The AI MUST ensure proper module generation formats (`commonjs`, `esnext`, `umd`, etc.) based on the specific bundler or execution environment.

## @Guidelines

### Project Layout & Artifacts
- The AI MUST organize TypeScript projects with a top-level `src/` directory for source files and a top-level `dist/` directory for compiled artifacts.
- The AI MUST purposefully configure the emission of the four artifact types:
  - `.js`: Generated JavaScript (Controlled by `"emitDeclarationOnly": false`).
  - `.js.map`: Source maps (Controlled by `"sourceMap": true`).
  - `.d.ts`: Type declarations (Controlled by `"declaration": true`).
  - `.d.ts.map`: Declaration maps (Controlled by `"declarationMap": true`).

### Compile Target (`target` and `lib`)
- The AI MUST NOT assume TypeScript will polyfill missing JavaScript APIs. The AI MUST instruct the user to use a polyfill library (e.g., `core-js`, `@babel/polyfill`) when targeting environments that lack modern features.
- The AI MUST use the `lib` array in `tsconfig.json` to inform TSC which JavaScript features and environment APIs (e.g., `"dom"`, `"es2015"`) are guaranteed to be available at runtime.
- The AI MUST select an appropriate `target` version based on the deployment environment (`es5` is the recommended safe default if unknown).
- The AI MUST recognize that TSC cannot transpile ES5 object getters/setters, ES2015 Regex `y` and `u` flags, ES2018 Regex `s` flag, or ESNext `BigInt`.

### Source Maps and Debugging
- The AI MUST enable `"sourceMap": true` for development environments and server/NodeJS production environments.
- The AI MUST explicitly evaluate whether to disable source maps in browser production environments if the user requires security through obscurity for frontend code.
- The AI MUST configure error monitoring tools (e.g., Sentry, Bugsnag) to ingest source maps to trace runtime errors back to TypeScript source.

### Project References (For Large Codebases)
- The AI MUST utilize Project References for codebases with hundreds of files to optimize build times.
- The AI MUST split large projects into folders, each with its own `tsconfig.json`.
- The AI MUST configure subproject `tsconfig.json` files with:
  - `"composite": true`
  - `"declaration": true`
  - `"declarationMap": true`
  - `"rootDir": "."` (or an explicit `outDir` relative to the root).
- The AI MUST use the `"references"` array to define dependencies between subprojects (e.g., `[{"path": "../myReferencedProject"}]`).
- The AI MUST warn against using `prepend: true` for a single subproject referenced by multiple other subprojects, as it will duplicate the output.
- The AI MUST explicitly instruct the use of `tsc --build` or `tsc -b` to compile projects utilizing references.
- The AI MUST NOT use `"noEmitOnError": false` in referenced subprojects, as TSC hardcodes this to `true` for composite projects.
- The AI MUST use the `"extends"` property in subproject configurations to inherit from a base `tsconfig.base.json` to reduce boilerplate.

### Server (NodeJS) Execution
- The AI MUST configure `"module": "commonjs"` and `"target": "es2015"` (or `es5` for legacy Node) for backend applications.
- The AI MUST implement the `source-map-support` NPM package in the NodeJS entry point to ensure stack traces map back to TypeScript code.

### Browser Execution
- The AI MUST set the `"module"` compiler option based strictly on the bundler used:
  - SystemJS: `"systemjs"`
  - Webpack/Rollup: `"es2015"` or `"esnext"` (Mandatory for dynamic imports).
  - Open Source Libraries: `"umd"` (Maximizes compatibility).
  - Browserify: `"commonjs"`
  - RequireJS: `"amd"`
  - Raw Script Tags: `"none"`
- The AI MUST NOT use the TSC `"outFile"` flag for complex browser bundling; it MUST recommend a dedicated bundler plugin (e.g., `ts-loader`, `tsify`, `@babel/preset-typescript`).
- The AI MUST implement lazy loading using dynamic imports (`await import(...)`) to optimize frontend bundle sizes and network waterfalls.

### NPM Publishing
- The AI MUST configure libraries to compile to `"target": "es5"` and `"module": "umd"` to maximize compatibility.
- The AI MUST enable `"declaration": true` and `"sourceMaps": true`.
- The AI MUST configure `.npmignore` to exclude raw `.ts` files (e.g., `src/`).
- The AI MUST configure `.gitignore` to exclude generated artifacts (e.g., `dist/`).
- The AI MUST define the `"main"` (e.g., `dist/index.js`) and `"types"` (e.g., `dist/index.d.ts`) fields in `package.json`.
- The AI MUST add a `"prepublishOnly": "tsc -d"` script to `package.json` to ensure artifacts are compiled before publishing.

### Triple-Slash Directives
- The AI MUST use the `/// <reference types="..." />` directive to declare a dependency on an ambient type declaration while enforcing import elision (avoiding side-effect generating `import './global'` statements if only types are needed).
- The AI MUST use the `/// <amd-module name="..." />` directive at the top of a file to explicitly name an AMD module when compiling with `"module": "amd"`, avoiding anonymous module generation.

## @Workflow
1. **Analyze Deployment Target**: Determine if the project is for NodeJS, a Browser app, or an NPM library.
2. **Scaffold Directory Layout**: Enforce `src/` for source files and `dist/` for compiled artifacts.
3. **Configure Build Settings**: Generate a `tsconfig.json` defining `target`, `module`, and `lib` specific to the deployment target. Enable `sourceMap` and `declaration` if building a library.
4. **Implement Polyfills**: Identify missing JavaScript features in the target environment and integrate polyfill imports (e.g., `core-js`).
5. **Optimize Large Projects**: If the codebase is large, restructure into subprojects, implement a base `tsconfig.json`, and set up Project References using `"composite": true` and `references`.
6. **Configure Bundler / Runtime Tools**: For Node, apply `source-map-support`. For Browsers, configure the respective bundler (Webpack/Rollup) and set `module` appropriately (e.g., `esnext`).
7. **Finalize Publishing Config**: If publishing to NPM, set up `.npmignore`, `.gitignore`, and `package.json` `main`/`types`/`prepublishOnly` scripts.

## @Examples (Do's and Don'ts)

### Project Layout
- **[DO]**: Keep source code in `src/` and output in `dist/`.
  ```json
  {
    "compilerOptions": {
      "outDir": "./dist",
      "rootDir": "./src"
    }
  }
  ```
- **[DON'T]**: Mix `.ts` source files and compiled `.js` artifacts in the same root directory without an `outDir`.

### Polyfilling
- **[DO]**: Manually import polyfills and specify them in the `lib` array to satisfy the typechecker.
  ```json
  {
    "compilerOptions": {
      "target": "es5",
      "lib": ["es2015", "es2016.array.include", "dom"]
    }
  }
  ```
- **[DON'T]**: Assume setting `"target": "es5"` automatically implements `Promise` or `Array.prototype.includes` at runtime.

### Server (NodeJS) Execution
- **[DO]**: Use `commonjs` for NodeJS execution and include `source-map-support`.
  ```typescript
  import 'source-map-support/register';
  // Node.js backend logic
  ```
  ```json
  {
    "compilerOptions": {
      "target": "es2015",
      "module": "commonjs",
      "sourceMap": true
    }
  }
  ```
- **[DON'T]**: Use `"module": "esnext"` for a raw NodeJS backend unless utilizing experimental ES module flags in Node.

### NPM Publishing
- **[DO]**: Configure `package.json` to publish compiled output and exclude source.
  ```json
  {
    "main": "dist/index.js",
    "types": "dist/index.d.ts",
    "scripts": {
      "prepublishOnly": "tsc -d"
    }
  }
  ```
  And in `.npmignore`:
  ```text
  src/
  ```
- **[DON'T]**: Publish raw `.ts` files to NPM without shipping the compiled `.js` and `.d.ts` artifacts.

### Triple-Slash Directives
- **[DO]**: Use the `types` directive to avoid emitting unnecessary runtime `require`/`import` calls for type-only global extensions.
  ```typescript
  /// <reference types="./global" />
  let myVar: MyGlobalType = 123;
  ```
- **[DON'T]**: Use standard side-effect imports (`import './global'`) if you ONLY need ambient type information, as it will persist in the compiled JavaScript output.

### Project References
- **[DO]**: Use `"composite": true` in subprojects and compile with `tsc -b`.
  ```json
  {
    "compilerOptions": {
      "composite": true,
      "declaration": true,
      "declarationMap": true
    },
    "references": [
      { "path": "../core" }
    ]
  }
  ```
- **[DON'T]**: Configure `"noEmitOnError": false` in a subproject that is used as a project reference.