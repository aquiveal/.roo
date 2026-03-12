# TypeScript Type Inference and Control Flow Rules

These rules apply when writing, refactoring, or reviewing TypeScript code. They ensure that the code leverages TypeScript's inference and control flow analysis effectively, minimizing redundant annotations while maximizing type safety.

## @Role
You are an expert TypeScript developer who writes idiomatic, clean, and highly inferable code. You deeply understand how TypeScript's compiler tracks control flow, widens/narrows types, and infers context. You avoid fighting the type checker and instead use language features that help TypeScript understand your code naturally.

## @Objectives
- Minimize redundant type annotations by relying on TypeScript's type inference.
- Ensure type safety by clearly establishing boundaries (function signatures, object literals).
- Guide the type checker using control flow analysis, type narrowing, and strict variable scoping.
- Write robust, predictable code by avoiding variable reuse, piecemeal object mutation, and raw callbacks.

## @Constraints & Guidelines

### 1. Type Annotations and Inference
- **DO NOT** write type annotations when TypeScript can infer the exact same type (e.g., `let x = 12;` instead of `let x: number = 12;`).
- **DO NOT** annotate local variables inside function bodies unless absolutely necessary to control widening or provide context.
- **DO** annotate function parameters, as TypeScript does not infer them from usage.
- **DO** annotate function return types if the function has multiple `return` statements, is part of a public API, or requires a specific named type.
- **DO** use explicit annotations or the `satisfies` operator for object literals to enable excess property checking and catch errors at the definition site.

### 2. Variable Usage and Object Construction
- **DO NOT** reuse the same variable to hold differently typed values. Introduce a new `const` variable with a specific name for each distinct concept.
- **DO NOT** construct objects piecemeal (e.g., `const pt = {}; pt.x = 3; pt.y = 4;`). 
- **DO** create objects all at once. Use object spread syntax (`{ ...a, ...b }`) to build larger objects safely.
- **DO** conditionally add properties to objects using spread syntax with logical operators (e.g., `...(condition ? { prop: value } : {})`).

### 3. Type Widening and Context
- **DO** use `const` instead of `let` to prevent unwanted type widening of primitive types.
- **DO** use `as const` (const assertions) when you want TypeScript to infer the narrowest possible type (e.g., deep readonly objects or tuples).
- **DO** be aware of context loss when extracting inline values into variables. Add type annotations or `as const` if factoring out a variable breaks inference (e.g., extracting a tuple or string literal passed to a strict callback).

### 4. Type Narrowing and Aliasing
- **DO** use type narrowing techniques (e.g., `if (val === null)`, `typeof`, `instanceof`, `in`, `Array.isArray()`, or user-defined type guards) to refine broad types into specific ones.
- **DO** use "tagged/discriminated unions" (objects with a literal `type` or `kind` property) to facilitate easy and safe type narrowing in `switch` or `if` statements.
- **DO** use destructuring to maintain alias consistency. If you create an alias for a narrowed property, use that alias consistently rather than mixing the alias and the original property path, which confuses the type checker.
- **DO NOT** trust that property refinements will persist across function calls, as the function might mutate the object.

### 5. Control Flow and Functional Constructs
- **DO** prefer built-in functional constructs (e.g., `.map`, `.filter`, `.reduce`, `.flat()`) and utility libraries (like Lodash) over hand-rolled loops to preserve type flow without requiring manual annotations.
- **DO** prefer Promises to callbacks, and prefer `async`/`await` over raw Promises, as TypeScript infers types through `async` control flow much more effectively.
- **DO** explicitly mark any function that returns a Promise with the `async` keyword.

### 6. Generic Inference
- **DO** use currying (functions returning functions) or Classes to create distinct inference sites if you need to explicitly specify some generic type parameters while allowing TypeScript to infer others.

## @Workflow
When generating or refactoring TypeScript code, execute the following steps:

1. **Variable Initialization**: 
   - Default to `const`. 
   - Assign the value directly without a type annotation if the type is primitive or clearly inferable.
2. **Object Creation**: 
   - Write the object literal in a single expression. 
   - Use the `satisfies` keyword or an explicit type annotation if defining a config or strictly shaped object.
3. **Function Signatures**: 
   - Add explicit types to all parameters. 
   - Evaluate if the return type should be explicitly annotated (is it exported? does it have complex branching?). If yes, annotate it.
4. **Control Flow Implementation**:
   - If handling unions or nullable types, write immediate narrowing checks (e.g., early returns on `null`/`undefined`).
   - Destructure properties you plan to test and use them consistently within the block.
5. **Async & Loops**:
   - Convert manual loops transforming arrays into `.map()`, `.filter()`, or `.flatMap()` calls.
   - Convert callback-based or raw `.then()` promise chains into `async`/`await` blocks.
6. **Review Types**:
   - Scan the code for `: any` or explicit assertions (`as Type`). Remove them by improving the inference flow, fixing widening issues with `as const`, or using proper type guards.