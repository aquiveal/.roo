# @Domain
These rules MUST trigger when the AI is writing, modifying, debugging, or analyzing TypeScript code, configuring TypeScript build tools (`tsconfig.json`, Webpack, Vite, `ts-node`), authoring tests for TypeScript projects, implementing runtime data validation, or writing code that interacts with the browser DOM or Node.js runtime environment.

# @Vocabulary
- **TC39**: The standards body defining the JavaScript runtime. TypeScript defers runtime feature innovation to TC39.
- **TranspileOnly**: A compiler mode that strips TypeScript types to emit JavaScript without performing CPU-intensive type checking.
- **Source Maps**: Files (`.js.map`) mapping compiled JavaScript positions back to original TypeScript source code, essential for debugging.
- **Declaration Maps**: Files (`.d.ts.map`) mapping `.d.ts` type declarations back to the original `.ts` source.
- **EventTarget / Node / Element / HTMLElement**: The strict hierarchy of the browser DOM. `EventTarget` is the base, `Node` adds text/comments, `Element` adds SVGs/tags, `HTMLElement` adds HTML-specific properties.
- **Project References**: A TypeScript feature (`references` array in `tsconfig.json` combined with `composite: true`) to split large codebases into independently compiled sub-projects.
- **Parameter Properties**: A TypeScript-specific class feature where constructor arguments are prefixed with visibility modifiers (e.g., `constructor(public name: string)`) to automatically create properties.
- **Zod / Ajv**: Runtime schema validation libraries used to bridge the gap between static TypeScript types and runtime values.

# @Objectives
- Ensure TypeScript acts purely as a type-level system and does not inject non-standard runtime features into emitted JavaScript.
- Maximize TypeScript compiler and language server performance through optimized configurations, precise typings, and strict project structures.
- Construct perfectly accurate static models of the execution environment, preventing false positives and false negatives in type checking.
- Eliminate duplicate sources of truth between static TypeScript types and runtime validation logic.
- Safely and accurately navigate the browser DOM hierarchy using precise type casting and runtime narrowing.
- Differentiate the role of the static type checker from runtime unit tests to prevent redundant testing of invalid types.

# @Guidelines

## Prefer ECMAScript Features to TypeScript Features
- The AI MUST NOT use TypeScript `enum`. When encountering an enum requirement, the AI MUST use a union of string literal types (e.g., `type Flavor = 'vanilla' | 'chocolate'`). If numeric values are strictly required, use strings instead to avoid runtime mapping confusion.
- The AI MUST NOT use TypeScript parameter properties (e.g., `constructor(public name: string)`). The AI MUST explicitly declare class properties and assign them in the constructor body to preserve class design visibility.
- The AI MUST NOT use TypeScript's `private`, `protected`, or `public` visibility modifiers for runtime encapsulation. The AI MUST use standard ECMAScript `#private` fields for runtime privacy. `readonly` is permitted as it is a type-level construct.
- The AI MUST NOT use `namespace`, `module`, or triple-slash imports (`/// <reference path="..." />`). The AI MUST use ECMAScript 2015-style `import` and `export`.
- The AI MUST NOT use non-standard decorators (`experimentalDecorators: true`). If decorators are required, the AI MUST use standard ECMAScript decorators (stage 3+).

## Use Source Maps to Debug TypeScript
- When generating TypeScript configuration for debugging, the AI MUST ensure `sourceMap: true` is set in `tsconfig.json`.
- When configuring bundlers (e.g., Webpack, Vite), the AI MUST ensure source maps map back to the original `.ts` sources, not the transpiled `.js`.
- The AI MUST NOT serve inline source maps in production environments to avoid leaking source code or comments.
- When configuring libraries or packages that emit `.d.ts` files, the AI MUST set `declarationMap: true` to enable "Go to Definition" in editors.
- When configuring Node.js debug scripts, the AI MUST use `node --inspect-brk` in conjunction with source maps.

## Reconstruct Types at Runtime
- Because TypeScript types are erased at runtime, the AI MUST NOT rely on static types for API request bodies or external data validation.
- When implementing runtime validation, the AI MUST use one of three centralized source-of-truth architectures:
  1.  **Runtime to Static**: Use a library like `Zod` to define runtime schemas, and derive the static type using `z.infer<typeof schema>`.
  2.  **External to Static/Runtime**: Generate both TypeScript types and validation code (e.g., `Ajv` with JSON Schema) from an external OpenAPI or GraphQL schema.
  3.  **Static to Runtime**: Generate JSON Schemas directly from TypeScript types using `typescript-json-schema`.

## Understand the DOM Hierarchy
- When typing DOM elements, the AI MUST use the most specific type in the hierarchy (`EventTarget` -> `Node` -> `Element` -> `HTMLElement` -> `HTMLParagraphElement`).
- When accessing properties like `classList`, the AI MUST NOT use `EventTarget` or `Node`. The AI MUST narrow the type to `Element` or `HTMLElement`.
- When typing events, the AI MUST NOT use the generic `Event` type if accessing specific properties like `clientX` or `clientY`. The AI MUST use the specific event type (e.g., `MouseEvent`, `TouchEvent`, `KeyboardEvent`).
- When using `document.getElementById`, the AI MUST recognize the return type is `HTMLElement | null`. The AI MUST use an explicit type assertion (e.g., `as HTMLDivElement`) or an `instanceof HTMLDivElement` runtime check to access specific element properties.
- The AI MUST push DOM `null` checks to the perimeter of the function using `if (el)` or non-null assertions (`!`) if existence is guaranteed.

## Create an Accurate Model of Your Environment
- When generating `tsconfig.json`, the AI MUST accurately populate the `lib` array (e.g., `["dom", "es2021"]`) to reflect the exact runtime environment.
- When adding global variables via `<script>` tags, the AI MUST model them using `declare global { interface Window { ... } }`.
- When installing third-party libraries, the AI MUST ensure the `@types/` version strictly matches the runtime library version.
- When importing non-JavaScript assets (CSS, images) via a bundler, the AI MUST declare modules for them (e.g., `declare module '*.jpg'`).
- For full-stack projects, the AI MUST NOT use a single `tsconfig.json`. The AI MUST use multiple `tsconfig.json` files and project references to separate `client` (DOM) and `server` (Node) environments.

## Understand the Relationship Between Type Checking and Unit Testing
- The AI MUST NOT write unit tests to verify that a function rejects incorrect static types (e.g., `test('throws on null', () => add(null, null))`). The AI MUST rely on the TypeScript compiler to catch these errors.
- The AI MUST write unit tests for invalid inputs ONLY IF the function has harmful side effects (e.g., database mutations, security bypasses) that could be triggered by untrusted JavaScript runtime usage.
- When asserting that a specific invalid operation produces a type error in a test, the AI MUST use the `@ts-expect-error` directive.

## Pay Attention to Compiler Performance
- When configuring dev servers, bundlers, or test runners, the AI MUST separate type checking from transpilation by enabling `transpileOnly` mode (or using tools like `swc`).
- The AI MUST remove unused dependencies and dead code. When debugging slow compilation, the AI MUST recommend using `tsc --listFiles` and a treemap visualizer.
- For medium-to-large projects, the AI MUST configure incremental builds (`incremental: true`) and Project References (`composite: true`, `references: [...]`) to prevent re-compiling the entire codebase. Project references MUST be scoped to large functional chunks (e.g., `src` vs `test`), not individual micro-components.
- When defining types, the AI MUST NOT create massive unions (e.g., thousands of string literals).
- When combining object types, the AI MUST use `interface` extension (`extends`) rather than type intersection (`&`) to improve compiler subtyping performance.
- The AI MUST explicitly annotate function return types in public APIs and complex functions to save the compiler from expensive inference calculations.

# @Workflow
When tasked with writing, migrating, or configuring a TypeScript file/project, the AI must execute the following process:
1.  **Environment Audit**: Verify the runtime target (Browser vs Node.js) and ensure the `lib` array and `@types` packages accurately reflect this environment.
2.  **Feature Sanitization**: Scan the request or existing code for non-standard TypeScript features (`enum`, parameter properties, `private` modifier, `namespace`). Strip them out and replace them with standard ECMAScript equivalents.
3.  **DOM Precision**: If interacting with the browser DOM, verify that all event handlers use specific event types (`MouseEvent` instead of `Event`), and that element retrievals are properly cast/narrowed to their specific `HTML*Element` type.
4.  **Runtime Boundary Check**: If the code processes external data (API payloads, JSON), ensure a runtime validation mechanism (Zod/Ajv) is used as the single source of truth, deriving the static type from the schema.
5.  **Performance Optimization**: If designing complex types or modifying `tsconfig.json`, prefer interfaces over intersections, add explicit return types, and ensure `transpileOnly` or incremental compilation is utilized where appropriate.
6.  **Test Scoping**: If writing tests, ensure assertions only validate runtime business logic, completely omitting tests for inputs that the TypeScript compiler already statically rejects (unless specifically requested for security boundaries).

# @Examples (Do's and Don'ts)

## Enums vs Unions
- [DON'T]:
  ```typescript
  enum Flavor { Vanilla = 'vanilla', Chocolate = 'chocolate' }
  ```
- [DO]:
  ```typescript
  type Flavor = 'vanilla' | 'chocolate';
  ```

## Class Properties and Visibility
- [DON'T]:
  ```typescript
  class PasswordChecker {
    constructor(private passwordHash: number, public name: string) {}
  }
  ```
- [DO]:
  ```typescript
  class PasswordChecker {
    #passwordHash: number;
    name: string;

    constructor(passwordHash: number, name: string) {
      this.#passwordHash = passwordHash;
      this.name = name;
    }
  }
  ```

## Runtime Type Validation
- [DON'T]:
  ```typescript
  interface CreateComment { postId: string; body: string; }
  app.post('/comment', (req, res) => {
    const comment = req.body as CreateComment; // Unsafe, erases at runtime
  });
  ```
- [DO]:
  ```typescript
  import { z } from 'zod';
  const commentSchema = z.object({ postId: z.string(), body: z.string() });
  type CreateComment = z.infer<typeof commentSchema>;

  app.post('/comment', (req, res) => {
    const comment = commentSchema.parse(req.body); // Safe, validated at runtime
  });
  ```

## DOM Event and Element Typing
- [DON'T]:
  ```typescript
  function handleDrag(e: Event) {
    const target = e.currentTarget;
    target.classList.add('dragging'); // Error: EventTarget has no classList
    const x = e.clientX; // Error: Event has no clientX
  }
  const el = document.getElementById('my-div');
  el.value = '123'; // Error: HTMLElement has no value
  ```
- [DO]:
  ```typescript
  function handleDrag(e: MouseEvent) {
    const target = e.currentTarget as HTMLElement;
    target.classList.add('dragging');
    const x = e.clientX;
  }
  const el = document.getElementById('my-input') as HTMLInputElement;
  el.value = '123';
  ```

## Type Testing
- [DON'T]:
  ```typescript
  test('fails on invalid input', () => {
    expect(add('a', 'b')).toBeNaN(); // Redundant, TS compiler catches this
  });
  ```
- [DO]:
  ```typescript
  test('prevents updating readonly ID', () => {
    // @ts-expect-error Can't call updateUser to update an ID.
    expect(() => updateUser('123', {id: '234'})).toReject();
  });
  ```

## Type Intersections vs Interfaces for Performance
- [DON'T]:
  ```typescript
  type BaseState = { id: string };
  type ActiveState = BaseState & { isActive: boolean };
  ```
- [DO]:
  ```typescript
  interface BaseState { id: string; }
  interface ActiveState extends BaseState { isActive: boolean; }
  ```