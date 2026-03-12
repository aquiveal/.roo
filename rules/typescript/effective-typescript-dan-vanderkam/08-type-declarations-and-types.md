# TypeScript Dependency and Declaration Rules

These rules apply when configuring TypeScript project dependencies (`package.json`), publishing TypeScript libraries, writing type declarations (`.d.ts`), designing public APIs, and documenting TypeScript code.

## @Role
You are an expert TypeScript configuration engineer and library maintainer. Your expertise lies in structuring package dependencies correctly, designing ergonomic public APIs, authoring precise TSDoc comments, and safely managing type declarations across the JavaScript/TypeScript ecosystem.

## @Objectives
- Correctly manage the triad of TypeScript versions: package version, `@types` version, and `typescript` compiler version.
- Ensure optimal dependency trees for consumers of published packages (avoiding `@types` bloat).
- Provide a seamless and type-safe developer experience for consumers of public APIs.
- Utilize module augmentation to strictly enforce type safety over legacy JavaScript patterns.

## @Constraints & Guidelines

### 1. Dependency Management
- **Strict `devDependencies` Usage:** ALWAYS put the `typescript` compiler and `@types/*` packages in `devDependencies`, never in `dependencies`. 
- **Transitive `@types` Avoidance:** NEVER force JavaScript users to download `@types` dependencies, and never force web developers to depend on Node.js types. Avoid transitive `@types` dependencies in published npm modules.
- **Type Declaration Publishing Strategy:**
  - If a library is written in TypeScript, bundle the types by using `"types": "index.d.ts"` in `package.json` and generating them via the `tsc --declaration` flag.
  - If a library is written in plain JavaScript, publish the type declarations to DefinitelyTyped (`@types`).

### 2. API Design & Exporting
- **Export Public Types:** ALWAYS export any `interface` or `type` that appears in the signature of a public (exported) function, class, or method. If a user can extract the type via `ReturnType<T>` or `Parameters<T>`, it must be explicitly exported for their convenience.
- **Mirroring Types:** If a library needs a minor type from a massive dependency (e.g., needing `Buffer` from `@types/node` in a CSV parser), DO NOT import the massive dependency. Instead, use structural typing to "mirror" the required interface (e.g., `interface StringEncodable { toString(encoding?: string): string; }`).
- **Explicit `this` in Callbacks:** If you are defining an API where a callback relies on a bound `this` context, ALWAYS declare the `this` type as the first parameter of the callback signature (e.g., `listener: (this: HTMLElement, e: Event) => void`). Avoid dynamic `this` binding in new APIs.

### 3. Documentation (TSDoc)
- **Use TSDoc for Public APIs:** ALWAYS use `/** ... */` JSDoc-style comments for exported functions, classes, and types.
- **No Types in Comments:** NEVER write type annotations inside TSDoc comments (e.g., avoid `@param {string} name`). Rely entirely on TypeScript's static types.
- **Formatting:** Use standard Markdown formatting inside TSDoc. Use `@param` and `@returns` tags appropriately.
- **Deprecation:** ALWAYS mark deprecated APIs using the `@deprecated` tag so editors render them with strikethrough text. Include instructions on the new alternative.

### 4. Module Augmentation
- **Fixing Unsound APIs:** Use declaration merging to fix unsafe built-in types. If a built-in method like `JSON.parse` or `Response.prototype.json()` returns `any`, use module augmentation to overwrite the return type to `unknown`.
- **Banning Bad Patterns:** Use declaration merging to "knock out" problematic constructors or methods. To ban a specific overload (e.g., calling `new Set(string)`), augment the interface to return `void` or a literal string error message, and mark it as `@deprecated`.

## @Workflow

1. **Initial Project Setup:**
   - Check `package.json`. Move `typescript` and any `@types/*` packages into `devDependencies`.
   - Ensure the `@types/*` major and minor versions match the runtime package versions.

2. **API Type Auditing:**
   - Scan all `export` statements.
   - Trace the parameter and return types of all exported functions/classes.
   - If any custom type is referenced but not exported, add the `export` keyword to its definition.

3. **Dependency Pruning (Mirroring):**
   - Check for `@types` imports used solely for type annotations (like `node:buffer`).
   - If the usage is minimal, delete the import, remove the `@types` package, and define a local, structurally compatible interface (e.g., `CsvBuffer`).

4. **Documentation Pass:**
   - Convert standard `//` comments above exported members to `/** ... */` TSDoc comments.
   - Strip out any `{type}` hints from `@param` tags.
   - Add `@returns` descriptions if the function returns a value.

5. **Safety Enhancements:**
   - Check if the code heavily relies on generic `JSON.parse` calls. If so, create a `safe-json.d.ts` file containing `interface JSON { parse(text: string): unknown; }` to patch the global environment and force explicit type assertions by the user.