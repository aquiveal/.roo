# @Domain
When configuring TypeScript projects, managing package dependencies (e.g., `package.json`), authoring or publishing type declaration files (`.d.ts`), documenting APIs, modeling dynamic `this` bindings, or modifying third-party/built-in type definitions.

# @Vocabulary
- **dependencies**: npm packages required to run the JavaScript code at runtime. Installed transitively.
- **devDependencies**: npm packages used to develop and test code, but not required at runtime. Not installed transitively.
- **peerDependencies**: npm packages required at runtime but managed by the consumer (e.g., the specific version of React for a component library).
- **DefinitelyTyped (@types)**: A community-maintained collection of type definitions for JavaScript libraries, published on the npm registry under the `@types` scope.
- **Bundled Types**: Type declarations shipped directly within a package, typically indicated by a `"types"` field in `package.json`.
- **TSDoc / JSDoc**: A documentation standard using `/** ... */` block comments that TypeScript surfaces in editors via the Language Service.
- **Transitive Type Dependencies**: When a package's type declarations depend on another package's `@types`, forcing consumers to download additional types.
- **Mirroring Types**: Severing a dependency on a large `@types` package by duplicating (mirroring) just the necessary structural properties into a local interface.
- **Module Augmentation / Declaration Merging**: TypeScript's feature allowing repeated definitions of the same interface to merge, used to modify or fix external type declarations.
- **The Three Versions**: The inherent dependency management complexity in TypeScript involving the library version, the `@types` version, and the TypeScript compiler version.

# @Objectives
- Ensure correct isolation of development tooling and type declarations from production JavaScript runtime dependencies.
- Safely navigate the "Three Versions" problem to prevent mismatches between runtime code, type declarations, and compiler capabilities.
- Provide a pristine developer experience (DX) for API consumers by explicitly exporting all relevant types and documenting them with TSDoc.
- Prevent unwanted transitive dependencies from bloating consumer environments by using structural typing (mirroring).
- Leverage module augmentation to enforce stricter type safety on legacy or overly permissive APIs (like `JSON.parse` or the `Set` constructor).

# @Guidelines

## Dependency Management
- **Isolate TypeScript**: NEVER install TypeScript system-wide. ALWAYS put `typescript` in your project's `devDependencies`.
- **Isolate Type Declarations**: ALWAYS put `@types` dependencies in `devDependencies`, not `dependencies`. Your production JavaScript does not require types to run.
- **Web App Production Images**: For web applications, keeping `@types` in `devDependencies` allows the use of `npm install --production` to drastically reduce image size and improve tooling accuracy (e.g., security scanners).
- **Match Versions**: Ensure that the major and minor version numbers of an `@types` package match the underlying library's version. Patch versions will diverge.
- **Update Synchronously**: When updating a library, ALWAYS remember to update its corresponding `@types` package.
- **Handle Missing/Outdated Types**: If `@types` are outdated, use module augmentation to add missing functions, or contribute to DefinitelyTyped. If `@types` require a newer TypeScript version, upgrade TypeScript, downgrade the `@types` package, or use `declare module` to stub it out.
- **Publishing Types**: If authoring a library in TypeScript, bundle the generated type declarations using the `declaration` compiler option. If authoring a library in JavaScript, publish the handcrafted types to DefinitelyTyped.

## API Design and Documentation
- **Export Public Types**: ALWAYS explicitly export any type that appears in the signature of a public API. Users can extract them anyway using `Parameters` or `ReturnType`, so make it explicit and convenient.
- **Use TSDoc**: ALWAYS use JSDoc/TSDoc block comments (`/** ... */`) instead of inline comments (`//`) for exported functions, classes, and types. Editors only surface block comments in tooltips.
- **Format TSDoc**: Use `@param` and `@returns` tags. Utilize Markdown formatting (bold, italic, lists) within TSDoc, but keep comments concise.
- **Avoid Types in TSDoc**: NEVER write type information in TSDoc (e.g., `@param {string} name`). Rely strictly on TypeScript's type annotations.
- **Mark Deprecations**: ALWAYS use the `@deprecated` tag for deprecated APIs. This renders the symbol with a strikethrough in the consumer's editor. Include alternative usage instructions in the comment.
- **Type `this` in Callbacks**: If a library/API sets the value of `this` dynamically in a callback, model it by declaring a `this` parameter as the first argument in the callback's type signature.
- **Avoid Dynamic `this` in New APIs**: Prefer avoiding dynamic `this` binding in new API designs, as arrow functions make this pattern difficult for modern JavaScript consumers to use.

## Advanced Type Management
- **Mirror Types to Sever Dependencies**: NEVER force JavaScript users to depend on `@types`, and NEVER force web developers to depend on Node.js types (e.g., `@types/node`).
- **Structural Mirroring**: If a library only uses a tiny subset of a massive external type (like Node's `Buffer`), write a local interface that structurally mirrors the required methods (e.g., `toString(encoding?: string): string`) instead of importing the heavy `@types` package into production types. Write unit tests asserting the real type is assignable to your mirrored interface.
- **Module Augmentation for Safety**: Use declaration merging to fix overly permissive built-in or third-party types. For instance, augment the `JSON` interface to make `JSON.parse` return `unknown` instead of `any`.
- **Knocking Out Bad Constructors/Methods**: To ban a problematic built-in overload (e.g., `new Set(string)`), augment the interface to return `void` or an error string literal, and mark it with `@deprecated`.
- **Maintain Runtime Reality**: When using module augmentation, NEVER make the types diverge from reality. Only use it to make types stricter, more precise, or to disallow usage.

# @Workflow
1. **Dependency Installation**: When adding a library, install the library to `dependencies` and its `@types` to `devDependencies`. Verify major/minor versions match.
2. **API Documentation**: Once an API is written, add `/** ... */` TSDoc comments. Strip all type information from the text and add `@param`, `@returns`, and `@deprecated` as needed.
3. **Type Export Check**: Review the API signature. Identify every interface, type alias, or parameter object used. Ensure all are exported from the module.
4. **Callback Context Verification**: If the API accepts a callback, determine if the function binds a specific `this` context. If yes, inject a `this: ContextType` parameter into the callback type definition.
5. **Dependency Severing (Publishing)**: Before publishing a package, run a check on the generated `.d.ts` files. If they import heavy environment-specific `@types` (like `@types/node`), replace those imports with structurally mirrored local interfaces.
6. **Safety Augmentation**: If consuming legacy APIs returning `any` (like `JSON.parse` or `Response.json()`), create a local `.d.ts` file and use declaration merging to override the return type to `unknown`.

# @Examples (Do's and Don'ts)

## Managing Dependencies
**[DO]** Install TypeScript and `@types` as development dependencies.
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

**[DON'T]** Put `@types` or `typescript` in production dependencies.
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "@types/react": "^18.2.23",
    "typescript": "^5.2.2"
  }
}
```

## Exporting Public Types
**[DO]** Export types used in public signatures.
```typescript
export interface SecretName {
  first: string;
  last: string;
}

export interface SecretSanta {
  name: SecretName;
  gift: string;
}

export function getGift(name: SecretName, gift: string): SecretSanta {
  // ...
}
```

**[DON'T]** Hide types used in public signatures, forcing users to use `Parameters` or `ReturnType` to access them.
```typescript
interface SecretName {
  first: string;
  last: string;
}

export function getGift(name: SecretName, gift: string) {
  // ...
}
```

## API Documentation
**[DO]** Use TSDoc formatting without type declarations.
```typescript
/**
 * Generate a greeting.
 * @param name Name of the person to greet
 * @param title The person's title
 * @returns A greeting formatted for human consumption.
 */
export function greetFullTSDoc(name: string, title: string) {
  return `Hello ${title} ${name}`;
}
```

**[DON'T]** Use inline comments or JSDoc type annotations.
```typescript
// Generate a greeting. Result is formatted for display.
/**
 * @param {string} name
 * @param {string} title
 */
export function greetJSDoc(name: string, title: string) {
  return `Hello ${title} ${name}`;
}
```

## Typing `this` in Callbacks
**[DO]** Explicitly type the `this` context if your library binds it.
```typescript
function addKeyListener(
  el: HTMLElement,
  listener: (this: HTMLElement, e: KeyboardEvent) => void
) {
  el.addEventListener('keydown', e => listener.call(el, e));
}
```

**[DON'T]** Leave `this` untyped, which leads to `any` and runtime crashes.
```typescript
function addKeyListener(
  el: HTMLElement,
  listener: (e: KeyboardEvent) => void
) {
  el.addEventListener('keydown', e => listener.call(el, e));
}
```

## Mirroring Types to Sever Dependencies
**[DO]** Extract the structural requirement into a local interface to drop the `@types/node` dependency from your published types.
```typescript
/** Anything convertible to a string with an encoding, e.g. a Node buffer. */
export interface StringEncodable {
  toString(encoding?: string): string;
}

export function parseCSV(contents: string | StringEncodable) {
  if (typeof contents === 'object') {
    return parseCSV(contents.toString('utf8'));
  }
  // ...
}
```

**[DON'T]** Directly use `Buffer` in a published web-compatible package, forcing web users to download Node types.
```typescript
import { Buffer } from 'node:buffer';

export function parseCSV(contents: string | Buffer) {
  // ...
}
```

## Module Augmentation for Safety
**[DO]** Augment global interfaces to fix permissive legacy types like `JSON.parse`.
```typescript
// declarations/safe-json.d.ts
declare global {
  interface JSON {
    parse(
      text: string,
      reviver?: (this: any, key: string, value: any) => any
    ): unknown;
  }
}
```

**[DON'T]** Accept the default `any` return type of `JSON.parse` and let it spread through your application silently.
```typescript
const response = JSON.parse(apiResponse);
// ^? const response: any
const cacheExpirationTime = response.lastModified + 3600; // No error caught!
```