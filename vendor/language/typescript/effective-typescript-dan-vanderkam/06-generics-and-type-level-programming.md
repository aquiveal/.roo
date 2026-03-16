@Domain
Activation conditions: Trigger these rules when the user requests assistance with TypeScript generics, type-level programming, conditional types, mapped types, template literal types, type testing, or when creating reusable generic utilities and library type definitions.

@Vocabulary
- **Generic Type**: The type-level equivalent of a function. It takes one or more type parameters and produces a concrete, nongeneric type.
- **Type-Level Programming**: Using TypeScript's type system (which is Turing Complete) to perform logic, branching, and computation on types rather than values.
- **Constraint**: Using the `extends` keyword in a generic type parameter declaration to restrict the domain of allowed types (e.g., `<K extends keyof T>`).
- **Golden Rule of Generics**: Type parameters are for relating the types of multiple values. If a type parameter only appears in one location, it is not relating anything and must be removed.
- **Return-Only Generics**: A dangerous anti-pattern where a type parameter is used only in the return type, acting as an implicit, unsafe type assertion.
- **Conditional Type**: An if-statement in type space (e.g., `T extends string ? string : number`).
- **Distribution (Over Unions)**: The default behavior of conditional types where a union type is evaluated by applying the condition to each constituent of the union individually and unioning the results.
- **Bare Type**: A type parameter that is evaluated directly in a conditional (e.g., `T extends...`), which triggers distribution.
- **Template Literal Type**: A type modeling a structured subset of strings (e.g., `` `pseudo${string}` ``) or domain-specific languages at the type level.
- **Type Display / `Resolve<T>`**: A mapped type helper used to flatten and compute complex intersections or mapped types into a clean, readable object type for the end developer's IDE hover tooltip.
- **Tail-Recursive Generic Type**: A recursive generic type where the recursive instantiation is the absolute last operation, allowing TypeScript to apply Tail Call Optimization (TCO) to avoid instantiation depth limits.
- **Accumulator (`Acc`)**: A type parameter used to carry state through recursive generic type instantiations, enabling tail recursion.
- **Codegen**: Metaprogramming (generating code via scripts in TS, Python, etc.) used as a fallback when type-level programming becomes excessively complex (the "Turing tar-pit").

@Objectives
- Treat generic types as strict functions between types, utilizing constraints (`extends`) to guarantee type safety and prevent invalid inputs.
- Eliminate unnecessary, single-use type parameters to simplify signatures and improve type inference.
- Prevent bugs with union types by utilizing conditional types instead of overload signatures.
- Explicitly control the distribution of conditional types over unions, particularly anticipating the surprising behaviors of `boolean` and `never`.
- Enhance developer experience (DX) by meticulously controlling how complex generic types are displayed in IDE tooltips.
- Prevent compiler stack overflows (instantiation depth limits) by writing deeply recursive types using tail recursion and accumulators.
- Ensure true type safety by testing type equality structurally using dedicated tooling, avoiding naive assignability tests.
- Recognize when type-level complexity outweighs the benefits and pivot to code generation (codegen) strategies.

@Guidelines
- **Constraining Generic Types**: You MUST use `extends` to constrain type parameters. Do NOT use type intersections (e.g., `T & PropertyKey`) to silence type errors inside generic implementations.
- **Generic Parameter Naming & Documentation**: Length of type parameter names MUST match their scope. Use `T`, `K`, `V` for short, concise generics. Use descriptive names (e.g., `TagName`, `Path`) for class-level or broad-scope generics. You MUST document generic type parameters using the TSDoc `@template` tag.
- **Enforce the Golden Rule of Generics**: Evaluate every type parameter. If it appears only once in the signature, you MUST remove it. Note: A type parameter appearing in an inferred return type (e.g., `T[K]`) counts as a second appearance.
- **Eradicate Return-Only Generics**: If a function signature uses a type parameter only as the return type (e.g., `function parse<T>(in: string): T`), replace the return type with `unknown` and force the caller to perform an explicit type assertion.
- **Prefer Conditional Types over Overloads**: When a function accepts multiple types (e.g., `string | number`), use conditional types to define the return signature so that it correctly distributes over union inputs. Only use overloads if the union case is physically implausible or if the function behaves as two completely different entities.
- **Implement Conditional Types Safely**: When implementing a function defined by a conditional type, use a single implementation signature (often utilizing a broader type or internal type assertions) to satisfy the compiler while presenting the strict conditional type to the caller.
- **Control Distribution Explicitly**: 
  - To PREVENT a conditional type from distributing over a union, wrap the bare type and the condition in a one-element tuple: `[T] extends [Date] ? ...`.
  - Be explicitly aware that `boolean` distributes as `true | false`. Prevent this via `[V] extends [true]` if unexpected.
  - Be explicitly aware that distributing over `never` yields `never` unconditionally.
  - To FORCE distribution in nested/accumulator contexts, prepend a tautological conditional: `N extends number ? ... : never`.
- **Model String DSLs Cautiously**: Use template literal types combined with `infer` to model string subsets (e.g., converting `snake_case` to `camelCase`). However, avoid the "uncanny valley" of type safety: if a DSL parser (like CSS selectors) cannot be modeled 100% accurately, provide a broad escape hatch overload rather than a broken, overly precise type.
- **Flatten Type Display**: You MUST wrap complex mapped types, `Pick`, `Omit`, and intersections in a `Resolve<T>` helper (`type Resolve<T> = T extends Function ? T : {[K in keyof T]: T[K]}`) so the end-user sees a clean, computed object. NEVER use `DeepResolve` as it destroys classes like `Date`. Handle special cases (e.g., `[K] extends [never] ? T`) to yield concise base types.
- **Implement Tail Recursion**: If a generic type is recursive, it MUST be tail-recursive. Introduce an `Acc` (accumulator) type parameter (e.g., `Acc extends string = ""`) and pass the computed state into the next recursive call. Do NOT perform union or string concatenation operations *after* the recursive call.
- **Test Types Structurally**: You MUST test types. Do NOT test types by simply assigning to a typed variable (this tests assignability, which allows extra properties and missing function parameters). Use structural equality tools like `expect-type` (`expectTypeOf`), `eslint-plugin-expect-type`, `tsd`, or the Type Challenges `Equals` helper. When testing callbacks, explicitly test the inferred type of `this`.
- **Fallback to Codegen**: If modeling a system (like a SQL parser) requires excessively complex type-level programming that harms compiler performance and readability, you MUST recommend code generation (e.g., `PgTyped`) instead of Type-Level TypeScript.

@Workflow
1. **Analyze the Type Requirement**: Determine if a generic type is actually needed. Can the relationship be expressed without type parameters? If yes, remove the generic.
2. **Draft the Signature**: Write the generic signature. Count the appearances of each type parameter. If count < 2, remove the type parameter.
3. **Constrain and Document**: Apply `extends` constraints to all type parameters to limit domains. Add TSDoc `@template` comments describing what the generic does.
4. **Evaluate Branching**: If the return type depends on the input type, write a conditional type. 
5. **Analyze Distribution**: Evaluate how the conditional type handles unions, `boolean`, and `never`. Wrap in `[T] extends [Condition]` if distribution is unwanted.
6. **Optimize Recursion**: If the type loops over strings or tuples, add an `Acc` parameter and structure the logic to be strictly tail-recursive.
7. **Optimize Display**: Wrap complex mapped/intersected outputs in a `Resolve<T>` helper to ensure IDE hover tooltips are readable.
8. **Write Type Tests**: Create structural equality tests for the generic using `expectTypeOf` or the `Equals` type helper to guarantee exact type behavior, including edge cases.
9. **Assess Complexity**: If the resulting generic type resembles a Turing tar-pit (unreadable, hundreds of lines of type logic, sluggish compiler performance), halt and implement a code generation script instead.

@Examples (Do's and Don'ts)

**Constraining Generic Types**
- [DON'T]: Use intersections to silence type errors in implementations.
  ```typescript
  type MyPick<T, K> = { [P in K & PropertyKey]: T[P & keyof T] }; // Anti-pattern
  ```
- [DO]: Use `extends` to constrain the domain of type parameters.
  ```typescript
  /**
   * @template T The original object type
   * @template K The keys to pick
   */
  type MyPick<T extends object, K extends keyof T> = { [P in K]: T[P] };
  ```

**The Golden Rule of Generics**
- [DON'T]: Use type parameters that appear only once, or use return-only generics.
  ```typescript
  declare function parseYAML<T>(input: string): T; // Dangerous: acts as implicit 'as any'
  declare function processUnrelated<A, B>(a: A, b: B): void; // A and B only appear once
  ```
- [DO]: Use `unknown` to force safe assertions, and remove unnecessary generics.
  ```typescript
  declare function parseYAML(input: string): unknown;
  declare function processUnrelated(a: unknown, b: unknown): void;
  ```

**Conditional Types vs Overloads**
- [DON'T]: Use overloads for parameters that can be union types, causing failures on union inputs.
  ```typescript
  declare function double(x: number): number;
  declare function double(x: string): string;
  // Fails when passed: string | number
  ```
- [DO]: Use conditional types that automatically distribute over unions.
  ```typescript
  declare function double<T extends string | number>(
    x: T
  ): T extends string ? string : number;
  ```

**Controlling Distribution**
- [DON'T]: Allow conditional types to distribute when you need to evaluate the exact union or tuple.
  ```typescript
  type Comparable<T> = T extends Date ? Date | number : T extends number ? number : never;
  // isLessThan(Date | string, 'B') passes incorrectly because Date distributes.
  ```
- [DO]: Wrap in one-tuples to prevent distribution.
  ```typescript
  type Comparable<T> = [T] extends [Date] ? Date | number : [T] extends [number] ? number : never;
  ```

**Type Display Optimization**
- [DON'T]: Expose raw utility types that leak implementation details in IDE tooltips.
  ```typescript
  type PartiallyPartial<T, K extends keyof T> = Partial<Pick<T, K>> & Omit<T, K>;
  // Hovering shows: Partial<Pick<BlogComment, "title">> & Omit<BlogComment, "title">
  ```
- [DO]: Use a `Resolve<T>` helper to flatten the display.
  ```typescript
  type Resolve<T> = T extends Function ? T : {[K in keyof T]: T[K]};
  type PartiallyPartial<T extends object, K extends keyof T> = 
    [K] extends [never] ? T : 
    T extends unknown ? Resolve<Partial<Pick<T, K>> & Omit<T, K>> : never;
  // Hovering shows the actual computed object shape.
  ```

**Tail-Recursive Generic Types**
- [DON'T]: Perform operations *after* the recursive call, blowing up the TS instantiation stack limit.
  ```typescript
  type ToSnake<T extends string> = T extends `${infer First}${infer Rest}` 
    ? `${First extends Uppercase<First> ? `_${Lowercase<First>}` : First}${ToSnake<Rest>}` 
    : T;
  ```
- [DO]: Pass state into an accumulator so the generic is tail-recursive.
  ```typescript
  type ToSnake<T extends string, Acc extends string = ""> = string extends T ? string :
    T extends `${infer First}${infer Rest}` 
      ? ToSnake<Rest, First extends Uppercase<First> ? `${Acc}_${Lowercase<First>}` : `${Acc}${First}`>
      : Acc;
  ```

**Testing Types**
- [DON'T]: Test types using variable assignment (tests assignability, not equality).
  ```typescript
  const double = (x: number) => 2 * x;
  const testDouble: (a: number, b: number) => number = double; // Incorrectly passes
  ```
- [DO]: Use structural equality testing tools.
  ```typescript
  export type Equals<X, Y> = (<T>() => T extends X ? 1 : 2) extends (<T>() => T extends Y ? 1 : 2) ? true : false;
  export type Expect<T extends true> = T;
  
  type TestFail = Expect<Equals<typeof double, (a: number, b: number) => number>>; // Correctly fails
  ```