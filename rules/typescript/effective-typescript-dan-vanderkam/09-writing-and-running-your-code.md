# @Domain
The rules in this file are activated whenever the AI is tasked with generating, refactoring, or reviewing TypeScript code, configuring TypeScript compiler options (`tsconfig.json`), configuring build tools or bundlers (e.g., webpack, Vite, ts-node), writing DOM-manipulation logic, setting up unit tests for TypeScript modules, or optimizing build and editor performance.

# @Vocabulary
- **Transpiler**: A tool that takes modern JavaScript/TypeScript and converts it to an older, more widely supported version of JavaScript.
- **Source Map**: A file (`.js.map`) that maps positions and symbols in generated JavaScript back to the original TypeScript source code, essential for debugging.
- **Declaration Map**: A file (`.d.ts.map`) mapping type declarations back to the original source, enhancing editor language services like "Go to Definition".
- **Runtime Type Reconstruction**: The practice of validating erased TypeScript types at runtime using external schemas (OpenAPI, GraphQL) or validation libraries (Zod, Ajv).
- **DOM Hierarchy**: The taxonomic structure of browser DOM elements and events (e.g., `EventTarget` -> `Node` -> `Element` -> `HTMLElement` -> `HTMLParagraphElement`).
- **Ambient Symbols**: Variables, libraries, or assets (like images or CSS) that exist in the execution environment but require manual type declaration (`declare global`, `declare module`) to be understood by the TypeScript compiler.
- **Transpile-Only Mode**: A build configuration that strips TypeScript types without running CPU-intensive type checking, deferring type checking to a separate CI/batch process.
- **Project References**: A TypeScript feature utilizing multiple `tsconfig.json` files to split large codebases into independent, incrementally compilable subprojects.
- **Dead Code Elimination**: The process of pruning unused symbols and dependencies (via `noUnusedLocals` or tools like `knip`) to improve compiler and editor performance.

# @Objectives
- Maintain a strict boundary between standard ECMAScript runtime features and TypeScript's type space by avoiding historical, non-standard TypeScript features.
- Ensure all generated TypeScript code is fully debuggable via source maps.
- Guarantee that erased static types are accurately validated at runtime when ingesting external data or handling API payloads.
- Strictly adhere to the precise DOM typing hierarchy to avoid runtime exceptions and false-positive type safety assumptions.
- Construct and maintain a perfectly accurate static model of the execution environment (browser, Node.js, loaded globals) using `tsconfig.json` and ambient declarations.
- Optimize the division of labor between unit tests and static type checking to eliminate redundant validation.
- Maximize compiler (`tsc`) and language service (`tsserver`) performance through configuration, structural simplifications, and build tool optimizations.

# @Guidelines

## 1. ECMAScript Features over TypeScript Features
- The AI MUST NOT use TypeScript enums (`enum` or `const enum`). Instead, use unions of string literal types to guarantee structural typing and matching runtime behavior.
- The AI MUST NOT use TypeScript parameter properties (e.g., `constructor(public name: string)`). Explicitly declare properties and assign them in the constructor body to preserve class design visibility.
- The AI MUST NOT use TypeScript namespaces or triple-slash imports (`/// <reference path="..." />`). Use ECMAScript standard modules (`import`/`export`).
- The AI MUST NOT use the `--experimentalDecorators` flag or legacy decorators. Use standard ECMAScript decorators (Stage 3+).
- The AI MUST NOT use TypeScript visibility modifiers (`private`, `protected`, `public`). For private properties, use ECMAScript standard `#` private fields, which are enforced at runtime.

## 2. Source Maps and Debugging
- The AI MUST configure `sourceMap: true` in `tsconfig.json` for any executable code generation.
- The AI MUST configure `declarationMap: true` whenever `declaration: true` is utilized, particularly when configuring project references.
- The AI MUST ensure build chains map all the way back to the original `.ts` source, not the intermediate generated JavaScript.
- The AI MUST NOT deploy inline source maps to production environments to prevent exposing source code and internal comments.

## 3. Reconstructing Types at Runtime
- The AI MUST implement a runtime validation strategy for external data (e.g., API requests) to compensate for type erasure.
- If an external schema (GraphQL, OpenAPI) exists, the AI MUST use it as the single source of truth and generate TypeScript types from it.
- If defining types manually, the AI MUST use a runtime validation library (like Zod) to establish the runtime schema, and derive the static type using inference (e.g., `z.infer<typeof schema>`).
- Alternatively, the AI MAY write the static TypeScript `interface` and use tools like `typescript-json-schema` to generate a runtime validation schema.

## 4. DOM Hierarchy and Typing
- The AI MUST differentiate between `EventTarget`, `Node`, `Element`, and `HTMLElement`. 
- The AI MUST NOT assume an `EventTarget` (like `e.currentTarget`) has properties like `classList`.
- The AI MUST use precise DOM element types (e.g., `HTMLInputElement`, `HTMLImageElement`) when attempting to access specific properties (e.g., `.value`, `.src`).
- The AI MUST assert types for DOM retrieval functions that return generic types (e.g., `document.getElementById('id') as HTMLDivElement`) when the specific type is known, and MUST handle the possibility of `null`.
- The AI MUST specify exact event types (e.g., `MouseEvent`, `KeyboardEvent`) instead of generic `Event` to safely access properties like `clientX` or `key`.

## 5. Accurate Environment Modeling
- The AI MUST accurately specify the `lib` array in `tsconfig.json` to match the target execution environment (e.g., `["dom", "es2021"]`).
- The AI MUST define ambient types using `declare global { interface Window { ... } }` for any variables injected into the execution environment at runtime via HTML `<script>` tags.
- The AI MUST provide `declare module` statements for non-JavaScript assets (like `.jpg`, `.css`) when working in bundler environments (e.g., webpack) that permit importing them.

## 6. Unit Testing vs. Type Checking
- The AI MUST NOT write unit tests for input combinations that the TypeScript compiler already structurally prevents.
- The AI MUST write unit tests using `@ts-expect-error` to simulate invalid inputs ONLY if those invalid inputs could cause severe security flaws or data corruption when called from untyped JavaScript.
- The AI MUST focus unit testing on runtime behaviors and logic that the type system cannot verify (e.g., integer vs. decimal math operations).

## 7. Compiler Performance Optimization
- The AI MUST separate type-checking from compilation in build pipelines by configuring bundlers or runners (like `ts-node`) with `transpileOnly` mode.
- The AI MUST eliminate dead code and unused third-party dependencies to reduce payload for the compiler and language server.
- For large codebases, the AI MUST configure project references (`composite: true` and `references: [...]`) across multiple `tsconfig.json` files to enable incremental builds.
- The AI MUST simplify types by avoiding massive union types (e.g., 1000+ elements) and MUST prefer extending interfaces (`extends`) over intersecting type aliases (`&`) to improve type-checking efficiency.
- The AI MUST add explicit return type annotations to functions (especially those with complex return types) to save the compiler inference time.

# @Workflow
1.  **Code Assessment**: Upon receiving a task, determine if it involves DOM manipulation, API validation, build configuration, or general TypeScript class/type writing.
2.  **Feature Sanitization**: Scan requested or existing code for non-ECMAScript TypeScript features (`enum`, `namespace`, `private`, parameter properties). Strip them and replace them with standard ES equivalents (unions, standard imports, `#` fields, explicit constructor assignments).
3.  **Environment Sync**: Check or generate `tsconfig.json`. Ensure `lib` accurately reflects the environment. Ensure `sourceMap` is enabled. 
4.  **DOM Safety Check**: If handling DOM elements, trace every `Event` and `Element` back to its precise hierarchy member. Wrap generic retrievals (like `getElementById`) in specific assertions and null-checks.
5.  **Validation Check**: If writing an API endpoint or ingesting data, write a Zod schema (or equivalent) to enforce the shape at runtime, and extract the static type from it.
6.  **Test Scoping**: If generating tests, evaluate the function signature. Generate test cases *only* for mathematically or logically distinct valid values, relying on the type-checker to block invalid primitives.
7.  **Performance Check**: If defining complex objects or return types, explicitly annotate the return type. Use `interface X extends Y` rather than `type X = Y & Z`.

# @Examples (Do's and Don'ts)

### ECMAScript Features over TS Features
- **[DO]** Use union of literal types and ECMAScript private fields:
  ```typescript
  type Flavor = 'vanilla' | 'chocolate' | 'strawberry';
  
  class Person {
      #name: string; // ECMAScript private field
      
      constructor(name: string) {
          this.#name = name;
      }
  }
  ```
- **[DON'T]** Use TypeScript enums and parameter properties:
  ```typescript
  enum Flavor { Vanilla = 'vanilla', Chocolate = 'chocolate' }
  
  class Person {
      constructor(private name: string) {} // TypeScript-only parameter property
  }
  ```

### Reconstructing Types at Runtime
- **[DO]** Use Zod to define a runtime boundary and infer the type:
  ```typescript
  import { z } from 'zod';
  
  const createCommentSchema = z.object({
      postId: z.string(),
      title: z.string(),
      body: z.string(),
  });
  
  type CreateComment = z.infer<typeof createCommentSchema>;
  
  app.post('/comment', (request, response) => {
      try {
          const comment = createCommentSchema.parse(request.body);
          // comment is verified at runtime and strongly typed
      } catch (e) {
          return response.status(400).send('Invalid request');
      }
  });
  ```
- **[DON'T]** Rely solely on type assertions for incoming network payloads:
  ```typescript
  app.post('/comment', (request, response) => {
      const comment = request.body as CreateComment; 
      // DANGEROUS: Type is erased at runtime, payload could be anything
  });
  ```

### DOM Hierarchy
- **[DO]** Use specific Event types and Element assertions:
  ```typescript
  function addDragHandler(el: HTMLElement) {
      el.addEventListener('mousedown', (eDown: MouseEvent) => {
          const dragStart = [eDown.clientX, eDown.clientY];
          // ...
      });
  }
  
  const div = document.getElementById('my-div') as HTMLDivElement | null;
  if (div) {
      addDragHandler(div);
  }
  ```
- **[DON'T]** Attempt to access specific properties on generic DOM/Event types:
  ```typescript
  function handleDrag(eDown: Event) {
      const targetEl = eDown.currentTarget;
      targetEl.classList.add('dragging'); // ERROR: classList does not exist on EventTarget
      const dragStart = [eDown.clientX, eDown.clientY]; // ERROR: clientX does not exist on Event
  }
  ```

### Accurate Environment Modeling
- **[DO]** Model globals injected at runtime via ambient declarations:
  ```typescript
  interface UserInfo {
      name: string;
      accountId: string;
  }
  declare global {
      interface Window {
          userInfo: UserInfo;
      }
  }
  ```
- **[DON'T]** Suppress errors for globals using `any`:
  ```typescript
  alert(`Hello ${(window as any).userInfo.name}!`); // Bypasses type safety
  ```

### Compiler Performance
- **[DO]** Use `extends` for interface performance:
  ```typescript
  interface Base { id: string; }
  interface User extends Base { name: string; }
  ```
- **[DON'T]** Use intersection types for object composition if extending interfaces is possible:
  ```typescript
  type Base = { id: string; };
  type User = Base & { name: string; }; // Slower for the compiler to process
  ```