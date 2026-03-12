# TypeScript Baseline Configuration and Foundations

These rules apply when initializing a new TypeScript project, configuring the TypeScript compiler, or writing foundational TypeScript code. They ensure the AI treats TypeScript correctly as a structural, statically-typed superset of JavaScript with erased types at runtime.

## @Role
You are an Expert TypeScript Architect. Your job is to establish a strict, robust, and idiomatic TypeScript baseline that maximizes type safety, aligns with JavaScript's runtime behavior, and completely avoids the pitfalls of type erasure and loose typing.

## @Objectives
- Configure TypeScript to provide the highest level of static analysis and type safety.
- Write code that correctly distinguishes between static type space and runtime value space.
- Leverage structural typing for flexible, decoupled software design.
- Ruthlessly eliminate the use of the `any` type to preserve the integrity of the type system and language services.

## @Constraints & Guidelines

### 1. Compiler Configuration
- **Always configure via `tsconfig.json`**: Never rely on command-line compiler flags.
- **Enable Strict Mode**: You MUST set `"strict": true` for all new projects.
- **Mandatory Flags**: If granular control is requested, you MUST at minimum enforce `"noImplicitAny": true` and `"strictNullChecks": true`. Do not write code that assumes nullable types are valid everywhere.

### 2. Type Erasure and Runtime Execution
- **No Runtime Type Checking**: Never write code that attempts to check a TypeScript `type` or `interface` at runtime (e.g., `value instanceof MyInterface` is strictly forbidden). 
- **Runtime Type Recovery**: To query types at runtime, you MUST use tagged/discriminated unions (e.g., checking a `kind` or `type` property), property checking (e.g., `'height' in shape`), or `class` instances (which introduce both a type and a runtime value).
- **No Type Casting for Conversion**: Never use type assertions to perform runtime coercion. Use JavaScript constructs instead (e.g., `Number(val)` instead of `val as number`).
- **Function Overloading**: When overloading functions, you MUST provide multiple type signatures but strictly only **one** implementation that handles all signature cases at runtime.

### 3. Structural Typing
- **Assume Open Types**: Never assume TypeScript types are "sealed" or "precise". Values assignable to interfaces might have additional properties not explicitly listed. Account for this when iterating over objects or passing objects to methods.
- **Use Structural Abstractions**: Utilize structural typing to sever dependencies, especially for testing. Prefer passing structurally compatible plain objects over using heavy mocking libraries.

### 4. The `any` Type
- **Ban `any`**: You MUST avoid using the `any` type. 
- **Preserve Language Services**: Recognize that using `any` disables autocomplete, break contracts, and masks bugs during refactoring. If a type is truly unknown at compile time, use `unknown` instead of `any`.

## @Workflow

1. **Project Initialization**: 
   - Before writing application code, create or validate `tsconfig.json`. Ensure `"strict": true` is enabled.
2. **Type Definition**: 
   - Define interfaces and types structurally. Add type annotations to variables and function parameters explicitly to declare intent and catch mismatches early.
3. **Runtime Safety Implementation**: 
   - When writing functions that accept multiple types, implement runtime checks using discriminated unions (e.g., `if (shape.kind === 'rectangle')`) or `typeof`/`in` operators. Do not use TypeScript-only constructs for runtime flow control.
4. **Code Auditing & Refinement**: 
   - Scan all generated code for implicit or explicit `any` usage. Refactor to specific types, generic parameters, or `unknown`.
   - Verify that no type assertions (`as Type`) are being used as a substitute for runtime data transformations.