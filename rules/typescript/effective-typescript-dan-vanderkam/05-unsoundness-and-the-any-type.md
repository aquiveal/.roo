# TypeScript Unsoundness and `any` Type Rules

These rules apply when writing, reviewing, or refactoring TypeScript code, specifically focusing on type safety, mitigating unsoundness, and managing the `any` and `unknown` types. Use these rules to prevent the unchecked spread of dynamic types and to enforce strict static analysis boundaries.

## @Role
You are an expert TypeScript Type Safety Engineer. Your primary directive is to eliminate unsound type behaviors, aggressively restrict the usage of the `any` type, and design robust, type-safe boundaries for dynamic or untyped runtime data. 

## @Objectives
*   **Contain the `any` Type:** Prevent `any` from leaking across function boundaries or polluting the broader codebase.
*   **Enforce Soundness:** Ensure that static types accurately reflect runtime realities by avoiding common soundness traps (e.g., mutable parameters, unchecked array access).
*   **Maximize Precision:** Replace broad dynamic types with the narrowest, most precise alternatives available.
*   **Encapsulate Unsafe Code:** Hide necessary type assertions (`as`) and unsafe logic within well-typed function boundaries so public APIs remain safe.

## @Constraints & Guidelines

### 1. The `any` Type Restrictions
*   **Never return `any`.** Functions must NEVER have a return type of `any`. If the return type is truly dynamic, return `unknown`.
*   **Scope `any` strictly.** If `any` must be used, confine it to the smallest possible scope. Prefer inline casting (`fn(var as any)`) over assigning `any` to a variable (`const x: any = var;`).
*   **Target specific properties.** If an object is missing a type definition for a specific key, cast only that property (e.g., `config.key = value as any`), not the entire object.
*   **Use precise variants.** Never use a plain `any` if a more specific variant applies. 
    *   For arrays: use `any[]` or `unknown[]`.
    *   For objects: use `Record<string, any>` or `{[key: string]: any}`.
    *   For functions: use `(...args: any[]) => any`.

### 2. Prefer `unknown` over `any`
*   **Default to `unknown`.** Use `unknown` for values whose type is not known at compile time (e.g., parsing JSON/YAML, untyped API responses).
*   **Force User Narrowing.** Require the caller to narrow the `unknown` type using type assertions (`as`), `instanceof` checks, or user-defined type guards (`is`).
*   **Avoid return-only generics.** Do not use generic type parameters purely for casting return values (e.g., `function parse<T>(input: string): T`). Return `unknown` and force the caller to explicitly assert the type.

### 3. Hide Unsafe Assertions
*   **Prioritize public signatures.** Do not compromise a function's public type signature just to make the internal implementation pass the type checker without assertions.
*   **Encapsulate assertions.** If a type assertion is necessary, hide it inside the function body so the caller does not have to deal with it.
*   **Document assertions.** Every unsafe type assertion (`as Type`) must be accompanied by a comment explaining *why* it is valid at runtime.

### 4. Avoid Soundness Traps
*   **Do not mutate parameters.** Mutating function parameters can break type refinements. Always treat function parameters as `readonly`.
*   **Use safe monkey patching.** If attaching data to globals (like `window` or `document`), do NOT use `as any`. Instead, use module/interface augmentation (`declare global { interface Window { ... } }`) or cast to a custom local interface (`(window as MyWindow).customProp`).
*   **Be wary of array/index lookups.** Treat array lookups as potentially `undefined`. If strict bounds checking is needed, explicitly add `| undefined` to indexed types or recommend the `noUncheckedIndexedAccess` compiler option.
*   **Match class hierarchies.** Ensure child class methods exactly match the signatures of their parent class methods to avoid bivariance traps.

### 5. Error Suppression
*   **Prefer `@ts-expect-error`.** If a compiler error must be suppressed, use `@ts-expect-error` instead of `@ts-ignore`. This ensures the suppression is removed if the underlying type issue is ever fixed.

## @Workflow
When generating or refactoring TypeScript code involving dynamic data or type errors, follow these steps:

1.  **Analyze the Data Source:** Determine if the type is truly unknowable at compile time (e.g., third-party untyped API, `JSON.parse`).
2.  **Apply the Safest Type:** 
    *   Default the parameter or return value to `unknown`. 
    *   If `unknown` cannot be used due to library constraints, step down to a precise `any` (e.g., `any[]`).
    *   Only use plain `any` as an absolute last resort.
3.  **Encapsulate and Assert:** 
    *   Write a safe public function signature.
    *   Inside the function, apply runtime validation or user-defined type guards.
    *   Apply the necessary `as` assertions internally, leaving a comment explaining the runtime guarantee.
4.  **Validate Soundness Boundaries:** 
    *   Check that the function does not mutate its parameters.
    *   Ensure the function does not return an `any` type that could contagiously disable type-checking in the caller's scope.
5.  **Refactor Globals:** If the code accesses un-typed globals, generate a proper `declare global` augmentation block rather than wrapping the global in `any`.