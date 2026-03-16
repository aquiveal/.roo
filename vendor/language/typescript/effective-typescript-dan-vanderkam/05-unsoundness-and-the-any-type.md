# @Domain
These rules are activated whenever the AI is writing, evaluating, or refactoring TypeScript code, specifically in the following scenarios: 
- Handling unknown or dynamic data structures (e.g., API responses, parsed JSON/YAML).
- Resolving TypeScript compilation errors using type overrides, suppressions, or assertions.
- Extending or modifying global objects or third-party library types (Monkey Patching).
- Designing public-facing function signatures and return types.
- Iterating over arrays or dictionaries where boundary and undefined checks are relevant.
- Implementing callbacks or functions that receive object parameters.

# @Vocabulary
- **Unsoundness**: A condition in the type system where a symbol's static type declaration diverges from its actual runtime value, potentially causing undetected runtime crashes.
- **Top Type**: A type that encompasses all possible values. TypeScript has two: `any` (disables type checking) and `unknown` (enforces type checking via narrowing).
- **Bottom Type**: A type that encompasses no values (e.g., `never`).
- **Contagious `any`**: An `any` type that spreads implicitly throughout a codebase, typically caused by returning `any` from a function or assigning it to a broad variable scope.
- **Return-Only Generic**: A generic type parameter that appears only in the return type of a function signature (e.g., `function get<T>(): T`). It is functionally equivalent to an unsafe `any` assertion and is an anti-pattern.
- **Double Assertion**: Casting a type to a Top Type and then to a specific type to bypass TypeScript's overlapping rules (e.g., `x as unknown as Y`).
- **Declaration Merging / Augmentation**: Extending an existing interface (like `Window` or `Document`) by re-declaring it in the same module or global scope to safely add properties.
- **Bivariance**: A characteristic of TypeScript class hierarchies where function parameters can accept both narrower or broader types, often leading to unsoundness if child class method signatures diverge from the parent.

# @Objectives
- Ruthlessly eliminate the usage of plain `any` to prevent the degradation of static type safety.
- Contain and localize unsafe type assertions to the smallest possible abstract syntax tree (AST) node or function body to minimize their "blast radius."
- Enforce the use of the `unknown` type for dynamic data, forcing consumers to implement runtime validation or explicit narrowing.
- Protect against subtle TypeScript soundness traps, including parameter mutations, refinement invalidation, and unchecked indexed accesses.
- Guarantee that all public API boundaries (function signatures) remain strictly and safely typed, completely hiding any internal unsafe assertions from the caller.

# @Guidelines

## 1. Scoping and Restricting `any`
- The AI MUST NOT use the `any` type for variable declarations (e.g., `const x: any = ...`). If `any` is absolutely unavoidable, the AI MUST scope it to the exact expression being evaluated (e.g., `x as any`).
- The AI MUST NEVER return an `any` type from a function. Doing so creates contagious `any` types that infect the caller's scope.
- When silencing a type error for a specific property in a large object literal, the AI MUST apply `as any` only to the problematic property's value, not to the entire object.

## 2. Utilizing Precise Variants of `any`
- If a value is known to be a specific data structure but its contents are unknown, the AI MUST prefer a more precise variant of `any` over plain `any`:
  - Arrays: Use `any[]` instead of `any`.
  - Objects: Use `{[key: string]: any}` or `Record<string, any>` instead of `any`.
  - Functions: Use `(...args: any[]) => any` instead of `any` or `Function`.

## 3. `unknown` vs. `any`
- The AI MUST use `unknown` instead of `any` for values with an unknown structure (e.g., `JSON.parse` wrappers, API responses, YAML parsers).
- The AI MUST force callers to narrow `unknown` types via `instanceof`, `typeof`, user-defined type guards (`value is Type`), or explicit type assertions.
- When performing a double assertion to cast between entirely unrelated types, the AI MUST use `unknown` as the intermediate type (e.g., `value as unknown as TargetType`), NOT `any`.
- The AI MUST prefer `unknown` over `{}` or `Object` unless explicitly intending to permit any value *except* `null` and `undefined`.

## 4. Avoiding Return-Only Generics
- The AI MUST NOT use generic type parameters solely in a function's return type to automatically cast responses. This provides a false sense of security.
- Instead of `declare function fetchJSON<T>(url: string): Promise<T>`, the AI MUST use `declare function fetchJSON(url: string): Promise<unknown>` and force the caller to assert or validate the type.

## 5. Hiding Unsafe Type Assertions
- The AI MUST prioritize the safety and accuracy of a function's public type signature over the safety of its internal implementation.
- If an unsafe type assertion is necessary to satisfy the compiler, the AI MUST hide the assertion inside the function body and NOT compromise the public return type.
- The AI SHOULD include an explanatory comment whenever utilizing a type assertion, proving why the assertion is safe at runtime.

## 6. Type-Safe Monkey Patching
- The AI MUST NOT use `any` to attach properties to global objects (e.g., `(window as any).myProp = true`).
- To safely monkey-patch globals, the AI MUST use `declare global` to augment the existing interface (e.g., `interface Window { myProp: boolean }`).
- If global augmentation is impossible or undesirable, the AI MUST create a custom interface that intersects with the global type (e.g., `type MyWindow = typeof window & { myProp: boolean }`) and use localized assertions to that specific type.

## 7. Evading Soundness Traps
- **Error Directives**: When silencing compiler errors, the AI MUST prefer `@ts-expect-error` over `@ts-ignore`. This ensures the directive is flagged and removed if the underlying type error is eventually resolved.
- **Refinement Invalidation**: The AI MUST recognize that calling a function can theoretically mutate an object, invalidating prior type refinements (e.g., `if (obj.val) { fn(); obj.val.method() }`). To prevent this trap, the AI MUST extract the refined property to a local `const` variable before calling the function.
- **Parameter Mutation**: The AI MUST NOT mutate function parameters. To prevent accidental mutation and variance-related unsoundness (especially with arrays), the AI SHOULD apply the `readonly` modifier to parameters whenever possible.
- **Indexed Access**: The AI MUST account for the fact that array lookups (`arr[3]`) and dictionary lookups (`obj['key']`) might return `undefined` at runtime, even if the static type says otherwise. The AI SHOULD manually handle this possibility or assume the environment may run with `noUncheckedIndexedAccess` enabled.
- **Class Hierarchies**: When extending a class, the AI MUST ensure that overridden methods strictly match the parent method's signature to prevent bivariance soundness traps.

# @Workflow
When tasked with typing dynamic data, handling compiler errors, or refactoring unsafe code, the AI MUST follow this algorithmic process:
1. **Analyze the Value Origin**: Determine where the untyped or problematic value comes from (e.g., DOM, API, internal logic).
2. **Eliminate Plain `any`**: 
   - If the value shape is completely unknown, assign it the `unknown` type.
   - If the value shape is partially known, use a precise `any` variant (`any[]`, `Record<string, any>`).
3. **Localize Assertions**: If the compiler still objects, and you mathematically know the type is safe at runtime, use an `as Type` assertion. Move this assertion to the deepest, most localized expression possible.
4. **Protect the Signature**: Verify that the function's return type is strictly defined and does not leak `any` or use a return-only generic.
5. **Check for Refinement Traps**: If refining object properties, assign the property to a local `const` variable before performing subsequent operations or function calls.
6. **Review for Mutations**: Mark input parameters as `readonly` and ensure no mutations occur on the parameters within the function body.

# @Examples (Do's and Don'ts)

## Scoping `any`
- **[DON'T]** Assign `any` to a variable, allowing it to remain unchecked for its entire lifecycle:
  ```typescript
  function processObject() {
    const config: any = getConfig();
    doSomething(config);
    config.missingMethod(); // Unchecked at runtime
  }
  ```
- **[DO]** Scope `any` assertions inline to the exact parameter that requires it:
  ```typescript
  function processObject() {
    const config = getConfig();
    doSomething(config as any);
    config.missingMethod(); // Properly caught by the type checker
  }
  ```

## Property-Level `any` Assertions
- **[DON'T]** Cast an entire object to `any` just to bypass one missing property:
  ```typescript
  const config: Config = {
    a: 1,
    b: 2,
    c: { key: value }
  } as any;
  ```
- **[DO]** Apply the assertion strictly to the failing property:
  ```typescript
  const config: Config = {
    a: 1,
    b: 2,
    c: { key: value as any }
  };
  ```

## Using Precise Variants of `any`
- **[DON'T]** Use plain `any` for arrays or callbacks:
  ```typescript
  function getLength(arr: any, callback: any) {
    return arr.length;
  }
  ```
- **[DO]** Use `any[]` and precise function signatures:
  ```typescript
  function getLength(arr: any[], callback: (...args: any[]) => any) {
    return arr.length;
  }
  ```

## Handling Unknown Data and Return-Only Generics
- **[DON'T]** Create an illusion of safety using a return-only generic:
  ```typescript
  declare function parseYAML<T>(input: string): T;
  const data = parseYAML<MyType>('...'); // Looks safe, completely unsound
  ```
- **[DO]** Return `unknown` and force the caller to validate or assert:
  ```typescript
  declare function parseYAML(input: string): unknown;
  const data = parseYAML('...') as MyType; // Explicitly marks the assertion
  ```

## Type-Safe Monkey Patching
- **[DON'T]** Cast the global window to `any`:
  ```typescript
  (window as any).currentUser = { name: 'Alice' };
  ```
- **[DO]** Use Module Augmentation to safely add properties:
  ```typescript
  declare global {
    interface Window {
      currentUser?: { name: string };
    }
  }
  window.currentUser = { name: 'Alice' };
  ```
- **[DO]** Use an intersected custom type if augmentation is not possible:
  ```typescript
  type MyWindow = typeof window & { currentUser?: { name: string } };
  (window as MyWindow).currentUser = { name: 'Alice' };
  ```

## Preventing Refinement Invalidation
- **[DON'T]** Rely on an object property refinement after a function call:
  ```typescript
  function process(fact: { author?: string }, fn: () => void) {
    if (fact.author) {
      fn(); // Could theoretically mutate 'fact'
      console.log(fact.author.length); // Soundness trap
    }
  }
  ```
- **[DO]** Extract the property to a local constant before the function call:
  ```typescript
  function process(fact: { author?: string }, fn: () => void) {
    const author = fact.author;
    if (author) {
      fn();
      console.log(author.length); // Safe, 'author' is a local primitive
    }
  }
  ```

## Hiding Unsafe Assertions
- **[DON'T]** Bubble up `unknown` to the public API just to satisfy internal type errors:
  ```typescript
  // Pollutes the consumer's environment with 'unknown'
  export async function fetchPeak(id: string): Promise<unknown> {
    return checkedFetchJSON(`/api/peaks/${id}`); 
  }
  ```
- **[DO]** Maintain the strict public signature and encapsulate the type assertion internally:
  ```typescript
  export async function fetchPeak(id: string): Promise<Peak> {
    // Hidden assertion; API remains clean and strict
    return checkedFetchJSON(`/api/peaks/${id}`) as Promise<Peak>;
  }
  ```