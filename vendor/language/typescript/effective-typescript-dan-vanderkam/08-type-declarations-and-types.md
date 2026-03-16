# @Domain
This rule file is activated when the AI is modifying `package.json` dependencies, writing or consuming TypeScript type declaration files (`.d.ts`), configuring TypeScript build tools, designing or modifying public APIs, documenting TypeScript code, writing callbacks that bind the `this` context, or managing third-party library typings.

# @Vocabulary
*   **dependencies**: Packages required to run JavaScript at runtime.
*   **devDependencies**: Packages used to develop and test code, not required at runtime, and not installed transitively.
*   **peerDependencies**: Packages required at runtime but managed/selected by the consuming project (e.g., React plugins).
*   **@types**: The npm scope for community-maintained TypeScript type definitions from DefinitelyTyped.
*   **DefinitelyTyped**: A community-maintained collection of type definitions for JavaScript libraries.
*   **Transitive Dependencies**: Dependencies that are automatically installed because a direct dependency requires them.
*   **TSDoc / JSDoc**: Documentation comments prefixed with `/**` and ending with `*/` that surface in IDE tooltips.
*   **Declaration Merging**: A TypeScript feature where repeated definitions of the same interface are merged to form a final result.
*   **Module Augmentation**: Using declaration merging to modify, fix, or enhance third-party or built-in types.
*   **Mirroring Types**: Writing a minimal, custom structural interface to represent a third-party type (like Node's `Buffer`) to avoid forcing users to install transitive `@types` dependencies.
*   **"Knocking Out" Methods**: Using declaration merging to ban problematic methods/constructors by overriding their return type to `void` or an error string literal.

# @Objectives
*   Strictly separate runtime dependencies from development/type dependencies to prevent bloating production builds and forcing transitive type dependencies onto JavaScript users.
*   Maintain strict version synchronization between libraries, their `@types` counterparts, and the TypeScript compiler.
*   Maximize the developer experience (DX) of public APIs by explicitly exporting all referenced types and documenting them thoroughly with TSDoc.
*   Prevent transitive `@types` dependency bleed in published libraries by mirroring structural types.
*   Aggressively patch unsafe built-in or third-party types (e.g., functions returning `any`) using module augmentation.

# @Guidelines

### Dependency Management
*   **TypeScript Installation**: The AI MUST place `typescript` in `devDependencies`. NEVER install TypeScript globally/system-wide. 
*   **@types Placement**: The AI MUST place all `@types/*` packages in `devDependencies`, NEVER in `dependencies`. TypeScript types are erased at compilation and do not exist at runtime.
*   **Version Matching**: The AI MUST ensure that the major and minor versions of a library match the major and minor versions of its corresponding `@types` package. Patch versions may differ.
*   **Synchronized Updates**: If updating a library's version, the AI MUST simultaneously update its `@types` package to match.
*   **Bundling vs. DefinitelyTyped**: If a library is written in TypeScript, the AI MUST bundle its generated `.d.ts` files (`"types": "index.d.ts"`). If the library is written in JavaScript, the AI SHOULD rely on DefinitelyTyped (`@types`).

### Public API Design
*   **Export Referenced Types**: The AI MUST explicitly `export` any type, interface, or alias that appears in the signature of an exported public function or class. Do not hide them; users can extract them anyway using `Parameters<T>` or `ReturnType<T>`.
*   **Callback `this` Context**: If an API dynamically binds the `this` keyword in a callback, the AI MUST declare the type of `this` as the first parameter of the callback's type signature.
*   **Avoid Dynamic `this`**: For newly designed APIs, the AI MUST avoid dynamic `this` binding entirely.

### Documentation (TSDoc)
*   **JSDoc/TSDoc for APIs**: The AI MUST use `/** ... */` block comments for documenting public APIs, functions, classes, and types. NEVER use inline `//` comments for API documentation.
*   **Markdown Formatting**: The AI MUST use Markdown for formatting within TSDoc comments (e.g., bold, italic, code blocks).
*   **Standard Tags**: The AI MUST use `@param` to describe parameters, `@returns` to describe return values, and `@template` to document generic type parameters.
*   **No Types in Comments**: The AI MUST NOT include type information inside TSDoc tags (e.g., avoid `@param {string} name`). Rely strictly on TypeScript's type annotations.
*   **Deprecation**: The AI MUST mark deprecated APIs with the `@deprecated` tag and explicitly document the alternative/replacement.

### Decoupling and Augmentation
*   **Mirror Types**: To prevent transitive `@types` dependencies (e.g., `@types/node` for `Buffer`), the AI MUST use structural typing to declare a minimal "mirrored" interface containing only the required methods, instead of importing the heavy external type.
*   **Declaration Merging for Safety**: The AI MUST use module augmentation/declaration merging to fix unsafe upstream types (e.g., changing `JSON.parse` to return `unknown` instead of `any`).
*   **Knocking out Unsafe Methods**: To ban a dangerous constructor or method (e.g., `new Set(string)`), the AI MUST use declaration merging to overload the method to return `void` or a string literal error message, and annotate it with `@deprecated`.
*   **Maintain Runtime Reality**: When augmenting types, the AI MUST NEVER make the types diverge from the actual runtime behavior. 

# @Workflow
When configuring a project, authoring a library, or writing type declarations, the AI MUST follow this step-by-step algorithm:

1.  **Dependency Audit**:
    *   Read `package.json`.
    *   Move `typescript` and any `@types/*` packages from `dependencies` to `devDependencies`.
    *   Verify that library versions match their `@types` versions at the major and minor semantic versioning level. Fix any mismatches.
2.  **Public API Type Audit**:
    *   Scan all `export function` and `export class` signatures.
    *   Identify any interfaces or type aliases used in parameters or return types.
    *   Ensure all identified types possess the `export` keyword.
3.  **Documentation Pass**:
    *   Convert `//` comments preceding public APIs to `/** ... */` TSDoc comments.
    *   Strip any `{type}` declarations from `@param` and `@returns` tags.
    *   Ensure generic parameters have an `@template` tag.
4.  **Callback `this` Verification**:
    *   Identify callbacks passed to APIs. If the runtime code invokes the callback with `.call(context)` or `.apply(context)`, add a `this: ContextType` parameter to the callback's type signature.
5.  **Type Mirroring (Library Publishing Only)**:
    *   If the code is a published library importing a massive `@types` package (like `@types/node`) merely to type a single parameter (like `Buffer`), delete the import.
    *   Create a local structural interface (e.g., `interface StringEncodable { toString(encoding?: string): string; }`) and use that instead.
6.  **Safety Augmentation**:
    *   If using built-in methods that return `any` (like `JSON.parse` or `Response.json`), create a `d.ts` file.
    *   Implement declaration merging to override the return type to `unknown`.

# @Examples (Do's and Don'ts)

### Dependency Management
[DON'T] Place `@types` in runtime dependencies or mismatch versions.
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "@types/react": "^17.0.0",
    "typescript": "^5.0.0"
  }
}
```

[DO] Place them in `devDependencies` and match major/minor versions.
```json
{
  "dependencies": {
    "react": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.23",
    "typescript": "^5.2.2"
  }
}
```

### Exporting Public Types
[DON'T] Hide types used in public signatures.
```typescript
interface SecretConfig { retries: number; }
export function initialize(config: SecretConfig) { /* ... */ }
```

[DO] Export all types that appear in the public API.
```typescript
export interface SecretConfig { retries: number; }
export function initialize(config: SecretConfig) { /* ... */ }
```

### TSDoc Formatting
[DON'T] Use inline comments or include types in JSDoc.
```typescript
// Generates a greeting
// @param {string} name - The user's name
export function greet(name: string): string { return `Hi ${name}`; }
```

[DO] Use TSDoc block comments without redundant type info.
```typescript
/**
 * Generates a greeting.
 * @param name The user's name
 * @returns A formatted greeting string
 */
export function greet(name: string): string { return `Hi ${name}`; }
```

### Callback `this` Context
[DON'T] Ignore `this` context when the API binds it.
```typescript
export function addClickListener(el: HTMLElement, listener: (e: Event) => void) {
  el.addEventListener('click', e => listener.call(el, e));
}
```

[DO] Explicitly type `this` in the callback signature.
```typescript
export function addClickListener(el: HTMLElement, listener: (this: HTMLElement, e: Event) => void) {
  el.addEventListener('click', e => listener.call(el, e));
}
```

### Mirroring Types to Sever Dependencies
[DON'T] Import heavy external types for simple structural needs in libraries.
```typescript
import { Buffer } from 'node:buffer'; // Forces @types/node on consumers
export function parse(data: string | Buffer) { /* ... */ }
```

[DO] Mirror the structural requirements to sever the dependency.
```typescript
export interface CsvBuffer { toString(encoding?: string): string; }
export function parse(data: string | CsvBuffer) { /* ... */ }
```

### Module Augmentation (Fixing `any` Returns)
[DON'T] Leave unsafe built-in types alone.
```typescript
const data = JSON.parse(input); // Type is any
```

[DO] Use declaration merging to fix unsafe types globally.
```typescript
// safe-json.d.ts
declare global {
  interface JSON {
    parse(text: string, reviver?: (this: any, key: string, value: any) => any): unknown;
  }
}

// usage.ts
const data = JSON.parse(input) as MyExpectedType; // Forced to assert safely
```

### Knocking Out Problematic Constructors
[DON'T] Allow structurally valid but semantically flawed constructors.
```typescript
const s = new Set("abc"); // TypeScript allows this, creates Set {'a', 'b', 'c'}
```

[DO] "Knock out" the bad overload using declaration merging and `@deprecated`.
```typescript
// ban-set-string.d.ts
declare global {
  interface SetConstructor {
    /** @deprecated */
    new (str: string): 'Error! new Set(string) is banned.';
  }
}
```