# @Domain
These rules must be triggered when the user requests the creation, refactoring, or documentation of TypeScript types, particularly when utilizing generics, utility types, conditional types, template literal types, mapped types, or type testing. This applies to any task involving type-level programming, complex type relationships, or library type declarations.

# @Vocabulary
- **Type-Level Programming**: Using TypeScript's type system (which is Turing Complete) as an independent programming language to compute types from other types.
- **Generic Type**: The type-level equivalent of a function; it takes one or more type parameters and produces a concrete, nongeneric type (instantiation).
- **Golden Rule of Generics**: A type parameter should appear at least twice in a function signature. If it only appears once, it is not relating anything and should be removed.
- **Return-Only Generics**: A dangerous anti-pattern where a type parameter only appears in the return type, acting as an implicit, unsafe type assertion.
- **Conditional Type**: An if-statement in type space (`T extends U ? X : Y`).
- **Bare Type**: A type parameter that is not wrapped in another construct (e.g., `T extends string`), which automatically distributes over union types.
- **Distribution over Unions**: The behavior where a conditional type applied to a union evaluates the condition for each member of the union independently.
- **Template Literal Type**: Types that model structured subsets of string types using template literal syntax (e.g., `` `pseudo${string}` ``).
- **Resolve / Simplify**: A type-level helper (`type Resolve<T> = T extends Function ? T : {[K in keyof T]: T[K]}`) used to flatten and clarify the display of complex intersected or mapped types.
- **Tail-Recursive Generic**: A recursive type alias that uses an accumulator to perform its recursive call as the absolute final step, preventing "Excessively deep" stack overflow errors in the compiler.
- **Codegen**: Generating TypeScript code/types from an external source (like a database schema or OpenAPI spec) as a simpler alternative to excessively complex type-level programming.

# @Objectives
- Treat generic types as strict, well-documented functions operating on sets of values.
- Minimize type parameters, ensuring they are only used to strictly relate inputs to outputs.
- Prefer conditional types to overloads to naturally handle union types.
- Explicitly control when and how union types distribute across conditional types.
- Optimize developer experience (DX) by ensuring complex types display legibility in IDE tooltips.
- Optimize compiler performance by transforming recursive types into tail-recursive structures.
- Implement robust type tests that verify structural equality, not just assignability.
- Avoid the "Turing tar-pit" by stepping out of the type system and using Codegen when type parsing becomes overly complex.

# @Guidelines

## Generics as Functions Between Types
- **Constrain Parameters**: Use the `extends` keyword to constrain the domain of type parameters, just as you would constrain a function's arguments.
- **Naming**: The length of a type parameter name should match its scope. Use short names (`T`, `K`) for simple generics, and descriptive names for broader scopes (like generic classes).
- **Documentation**: Use the `@template` TSDoc tag to document type parameters.
- **Inference**: Prefer generic functions and classes where TypeScript can infer the type parameters from usage over forcing the user to explicitly define them.

## Type Parameter Minimization
- **Enforce the Golden Rule**: Review all generic functions. If a type parameter `T` is only used once (e.g., only in the arguments or only in the return type), remove it.
- **Eliminate Return-Only Generics**: Never use generic type parameters solely for casting a return type (e.g., `declare function parse<T>(input: string): T;`). Return `unknown` instead and force the caller to perform an explicit type assertion.
- **Replace with `unknown`**: Extraneous type parameters can usually be replaced with `unknown` or specific constraints (e.g., `keyof T`).

## Conditional Types vs. Overloads
- **Prefer Conditionals**: Use conditional types instead of overloaded type signatures. Conditional types analyze the expression globally and automatically distribute over union types, whereas overloads fail when passed a union of the overloaded types.
- **Implementation Masking**: When implementing a function with a conditional return type, use a single overload to present the conditional signature externally, while using a simpler, looser signature for the internal implementation.

## Controlling Distribution over Conditional Types
- **Default Distribution**: Understand that `T extends U ? X : Y` will distribute over unions if `T` is a bare type.
- **Blocking Distribution**: To prevent distribution (e.g., you want to evaluate the union as a whole, not individually), wrap the parameter and the constraint in a one-element tuple: `[T] extends [U] ? X : Y`.
- **Forcing Distribution**: If your condition is not a bare type (e.g., `Acc['length'] extends N`) but you need distribution based on `N`, force it by wrapping the logic in an explicitly distributing conditional: `N extends number ? ... : never`.
- **Quirks of `boolean` and `never`**: Remember that `boolean` distributes to `true | false`. The `never` type distributes to an empty union, resulting immediately in `never` regardless of the conditional branches. Use the tuple wrapper `[T]` to avoid this.

## Template Literal Types
- **Model DSLs**: Use template literal types combined with the `infer` keyword to parse and strongly type Domain-Specific Languages (like routing paths, CSS selectors, or snake_case to camelCase converters).
- **Avoid Inaccuracy**: Do not create a template literal type so precise that it incorrectly rejects valid strings. Keep it broad enough to remain accurate.

## Testing Types
- **Test Equality, Not Assignability**: Do not test types merely by assigning them to a typed variable. Use libraries like `expect-type`, `vitest`, or ESLint plugins (`eslint-plugin-expect-type`, `dtslint`) to check structural equality.
- **Test Callbacks**: When testing higher-order functions, explicitly test the inferred types of the callback's parameters, including the `this` context if applicable.

## Type Display
- **Flatten Complex Types**: If you create a mapped type or intersection (e.g., `Partial<Pick<T, K>> & Omit<T, K>`), it will display exactly like that in IDEs. Wrap it in a `Resolve<T>` helper to flatten the display into a clean object representation.
- **Handle Edge Cases for Display**: Add special conditions (like `[K] extends [never]`) to bypass complex logic when the input allows for a much simpler, cleaner type display.

## Tail-Recursive Generic Types
- **Prevent Recursion Limits**: TypeScript limits the instantiation depth of recursive type aliases. Always convert recursive string-parsing or array-building generic types to be tail-recursive.
- **Use Accumulators**: Pass a default empty string `""` or empty array `[]` as an `Acc` parameter. Perform the operation and pass the modified accumulator into the next recursive call, ensuring the generic calls itself as its absolute final action.

## Codegen vs. Complex Types
- **Acknowledge Limits**: If you are building extremely complex type-level parsers (e.g., inferring SQL query results from raw query strings), stop.
- **Use Codegen**: Use standard scripts (Node, Python, etc.) or libraries like `PgTyped` to parse the external source and generate static `.ts` or `.d.ts` files instead of trapping the compiler in a Turing tar-pit.

# @Workflow
1. **Generic Evaluation**: When analyzing or writing a function/class, check if any type parameter violates the Golden Rule (used < 2 times). Remove it or replace it with `unknown`.
2. **Signature Design**: Determine if the function output depends strictly on the input type. If yes, use a conditional type rather than overloads.
3. **Distribution Check**: Analyze conditionals. Do you want `A | B` to yield `F<A> | F<B>`? If yes, use bare types. If no, wrap the conditional in `[T] extends [U]`.
4. **Recursion Optimization**: If writing a recursive type, immediately refactor it to include an `Acc` parameter (e.g., `Acc extends string = ""`) and make it tail-recursive.
5. **Display Optimization**: Once the generic logic works, wrap the output in a `Resolve<T>` type to guarantee clean IDE hover tooltips.
6. **Documentation**: Add `@template` tags explaining what each generic parameter represents.
7. **Testing**: Write type tests asserting exact structural matches using `expectTypeOf`.

# @Examples (Do's and Don'ts)

## The Golden Rule of Generics
- **[DON'T]** Use a return-only generic that acts as an implicit type assertion.
  ```typescript
  declare function parseYAML<T>(input: string): T;
  const w: Weight = parseYAML(''); // Illusion of safety, no runtime check.
  ```
- **[DO]** Return `unknown` and force the user to type-assert explicitly.
  ```typescript
  declare function parseYAML(input: string): unknown;
  const w = parseYAML('') as Weight; // Explicit, intentional assertion.
  ```

- **[DON'T]** Define type parameters that are only used once.
  ```typescript
  function printProperty<T, K extends keyof T>(obj: T, key: K) {
    console.log(obj[key]);
  }
  ```
- **[DO]** Remove extraneous type parameters.
  ```typescript
  function printProperty<T>(obj: T, key: keyof T) {
    console.log(obj[key]);
  }
  ```

## Conditional Types vs. Overloads
- **[DON'T]** Use overloads when inputs could be unions, causing valid calls to fail.
  ```typescript
  declare function double(x: number): number;
  declare function double(x: string): string;

  function f(x: string | number) {
    return double(x); // ERROR: Argument of type 'string | number' is not assignable to 'string'
  }
  ```
- **[DO]** Use conditional types to allow distribution over unions automatically.
  ```typescript
  declare function double<T extends string | number>(
    x: T
  ): T extends string ? string : number;
  
  function f(x: string | number) {
    return double(x); // OK, returns string | number
  }
  ```

## Controlling Distribution
- **[DON'T]** Allow bare types to distribute when you want to compare the whole union.
  ```typescript
  type Comparable<T> = T extends Date ? Date | number : T extends string ? string : never;
  // dateOrStr distributes, allowing cross-comparisons incorrectly.
  ```
- **[DO]** Wrap types in a tuple to prevent distribution.
  ```typescript
  type Comparable<T> = [T] extends [Date] ? Date | number : [T] extends [string] ? string : never;
  ```

- **[DO]** Force distribution on mapped/indexed values by adding a redundant bare-type conditional.
  ```typescript
  // N distributes properly because of 'N extends number ? ...'
  type NTuple<T, N extends number> = N extends number ? NTupleHelp<T, N, []> : never;
  ```

## Template Literal Types
- **[DO]** Use template literal types combined with conditional `infer` to transform strings.
  ```typescript
  type ToCamelOnce<S extends string> = S extends `${infer Head}_${infer Tail}`
    ? `${Head}${Capitalize<Tail>}`
    : S;
  ```

## Type Display (Resolving Intersections)
- **[DON'T]** Leave complex type transformations raw, which makes IDE hover tooltips confusing for users.
  ```typescript
  type PartiallyPartial<T, K extends keyof T> = Partial<Pick<T, K>> & Omit<T, K>;
  // Hovering shows: Partial<Pick<BlogComment, "title">> & Omit<BlogComment, "title">
  ```
- **[DO]** Use a `Resolve` helper to flatten the object output.
  ```typescript
  type Resolve<T> = T extends Function ? T : {[K in keyof T]: T[K]};
  type PartiallyPartial<T, K extends keyof T> = Resolve<Partial<Pick<T, K>> & Omit<T, K>>;
  // Hovering shows: { title?: string; commentId: number; content: string; }
  ```

## Tail-Recursive Generic Types
- **[DON'T]** Perform type operations *after* the recursive call, which risks "Excessively deep" compiler crashes.
  ```typescript
  type ToSnake<T extends string> = T extends `${infer First}${infer Rest}`
    ? `${First extends Uppercase<First> ? `_${Lowercase<First>}` : First}${ToSnake<Rest>}`
    : T;
  ```
- **[DO]** Pass an accumulator to make the generic tail-recursive.
  ```typescript
  type ToSnake<T extends string, Acc extends string = ""> = string extends T
    ? string
    : T extends `${infer First}${infer Rest}`
    ? ToSnake<Rest, First extends Uppercase<First> ? `${Acc}_${Lowercase<First>}` : `${Acc}${First}`>
    : Acc;
  ```