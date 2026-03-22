# @Domain
Node.js module creation, file resolution, package management, dependency configuration, npm script automation, and package publishing workflows. Activation triggers include tasks involving `require()` statements, module exports, `package.json` modifications, dependency management, npm script creation, and publishing Node.js packages.

# @Vocabulary
- **Module Wrapper**: The IIFE (Immediately Invoked Function Expression) Node.js uses to wrap module code: `(function (exports, require, module, __filename, __dirname) { ... })`.
- **module.exports**: The actual object returned by the `require()` call.
- **exports**: A local scope reference to `module.exports`.
- **Module Caching**: Node.js behavior where subsequent `require()` calls to the same resolved filename return the exact same, cached module object.
- **SemVer**: Semantic Versioning rules (`Major.Minor.Patch`) used by npm to resolve package dependencies.
- **npm Scripts**: Build directives defined in the `scripts` field of `package.json`, used to execute lifecycle hooks or CLI tools without requiring complex build systems like Gulp or Webpack.
- **package-lock.json**: An automatically generated file in npm 5+ that locks the exact downloaded versions and cryptographic hashes (`integrity`) of a `node_modules` tree.
- **npm shrinkwrap**: A command that renames `package-lock.json` to `npm-shrinkwrap.json`, allowing the locked dependency tree to be published with the module.
- **bin property**: A `package.json` field mapping a command name to a local file, enabling global CLI command installation.
- **Dependency Types**: `dependencies` (core), `devDependencies` (development/testing), `bundledDependencies` (locked distribution), and `optionalDependencies` (non-failing fallbacks).

# @Objectives
- Enforce strict and safe module export patterns to avoid broken references.
- Utilize the npm CLI and `package.json` as a comprehensive build, automation, and dependency management system.
- Prevent path resolution errors by adhering to Node.js's specific directory parsing and module lookup algorithms.
- Guarantee reproducible builds and predictable dependency trees using SemVer, lockfiles, and shrinkwrapping.
- Ensure safe package publishing, lifecycle management, and deprecation practices.

# @Guidelines

### Module Exporting and Loading
- The AI MUST use `module.exports` when exposing variables, functions, or classes from a file.
- The AI MUST NOT assign a new value directly to `exports` (e.g., `exports = new MyClass()`), as this overwrites the local reference to `module.exports` but does not expose the value to `require()`.
- The AI MUST use ES6 destructuring assignment to unpack multiple exported functions or objects from a single `require()` statement in one line.
- The AI MUST prefix relative local file imports with `./` or `../`. Node.js will fail to resolve local files if the path does not start with these prefixes, assuming instead that it is a core module or `node_modules` dependency.

### Module Execution and Caching Awareness
- The AI MUST account for module caching. If a module requires dynamic re-evaluation upon multiple imports, the AI MUST export a factory function rather than a static object.
- The AI MUST use the strict equality check `require.main === module` to detect if a module is being executed directly via the command line (e.g., `node module.js`) versus being required by another script.
- The AI MAY use the `require('module')._cache` object for debugging or introspection of the active module cache.

### Package Configuration (`package.json`)
- The AI MUST NOT include the words `js` or `node` in the `name` field of a `package.json`.
- The AI MUST set the `private: true` flag in `package.json` for code/modules that should never be accidentally published to the public npm registry.
- The AI MUST define the entry point of the module using the `main` field.
- The AI MUST define the source control location in the `repository` field and the issue tracker URL in the `bugs` field.
- The AI MUST use the `bin` field to map executable command names to script paths if the module is intended to be used as a CLI tool. If it is strictly a global CLI tool, the AI SHOULD add `"preferGlobal": true`.

### Dependency Management
- The AI MUST properly segregate dependencies:
  - `dependencies`: Code required for the module to run in production.
  - `devDependencies`: Test suites, build tools, and linters.
  - `bundledDependencies`: Dependencies to be packaged into a single tarball to bypass normal npm resolution.
  - `optionalDependencies`: Dependencies that, if they fail to install, should not halt the build process.
- The AI MUST strictly apply SemVer syntax. Use `^` (caret) to allow minor/patch updates, `~` (tilde) for only patch updates, and exact versions (no prefix) when strict determinism is required.
- The AI MAY define dependencies using GitHub repository shortcuts (e.g., `"user/repo"`), tarball URLs, or secure SSH git URLs (`git+ssh://...`) when standard npm registry resolution is not desired.

### Automation and Build Systems (npm scripts)
- The AI MUST prioritize using `package.json` `scripts` for build pipelines over third-party task runners (like Webpack or Gulp) for simple to moderate build steps.
- The AI MUST chain multiple script commands using `&&` (e.g., `"build": "npm run build:minify && npm run build:browserify"`).
- The AI MUST use standard npm lifecycle hooks (`prepublish`, `prepare`, `preinstall`, `postinstall`, `pretest`, `posttest`) to automate environment setup, teardown, and compilation around core npm commands.

### Lockfiles and Publishing
- The AI MUST NOT delete `package-lock.json`. It must be committed to source control to guarantee cryptographic integrity (`integrity` hash) and exact version resolution (`resolved` URL).
- If a locked dependency tree MUST be distributed to end users of a published module, the AI MUST execute `npm shrinkwrap` to generate an `npm-shrinkwrap.json` file prior to publishing.
- The AI MUST use `npm deprecate <name>[@<version>] <message>` rather than `npm unpublish` when invalidating a previously released package that other developers may currently depend upon.

# @Workflow
1. **Module Initialization**: Run `npm init` (or generate `package.json`). Populate `name`, `version`, `main`, `description`, `repository`, `bugs`, and `license`. Set `private: true` if applicable.
2. **Authoring Module**: Write JavaScript code. Expose the public API strictly via `module.exports`.
3. **Internal Testing/Scripts**: Define testing and build commands in the `scripts` object. Use pre/post hooks to automate directory creation, minification, or cleanup.
4. **Dependency Auditing**: Install dependencies using `npm install <pkg> --save` or `--save-dev` to automatically update `package.json` and generate `package-lock.json`.
5. **Executable Mapping (Optional)**: If building a CLI tool, define the `bin` map in `package.json` and prepend `#!/usr/bin/env node` to the target script file.
6. **Shrinkwrapping (Optional)**: If exact dependency distribution is required for the published artifact, run `npm shrinkwrap`.
7. **Publishing**: Use `npm publish` to deploy the package. If deprecation of a version is needed later, use `npm deprecate`.

# @Examples (Do's and Don'ts)

### Module Exports
- **[DO]**
  ```javascript
  function calculate() { /* ... */ }
  module.exports = { calculate };
  ```
- **[DON'T]** (This overwrites the exports reference, but `require` will still return an empty object)
  ```javascript
  function MyClass() { this.foo = 'bar'; }
  exports = new MyClass(); 
  ```

### File Resolution
- **[DO]**
  ```javascript
  const myModule = require('./myModule');
  ```
- **[DON'T]** (Node will search `node_modules` and core libraries, bypassing the local file)
  ```javascript
  const myModule = require('myModule.js');
  ```

### Direct Execution Detection
- **[DO]**
  ```javascript
  if (require.main === module) {
    // File was run directly via `node app.js`
    startServer();
  }
  ```

### Build Scripts
- **[DO]**
  ```json
  "scripts": {
    "build:minify": "mkdir -p dist/js && uglify src/js/**/*.js > dist/js/script.min.js",
    "build:browserify": "browserify src/js/index.js -o dist/app.js",
    "build": "npm run build:minify && npm run build:browserify"
  }
  ```
- **[DON'T]** (Avoid bloated setups if npm scripts can easily handle it natively)
  Writing a 100-line gulpfile.js just to run browserify and uglify on a single file.

### Lockfiles & Publishing
- **[DO]**
  Run `npm shrinkwrap` before publishing if you need consumers of your npm package to receive the exact dependency versions specified in your `package-lock.json`.
- **[DON'T]**
  Use `npm unpublish` if your package has already been downloaded or integrated by others; use `npm deprecate <pkg> <message>` instead.