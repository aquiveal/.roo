# @Domain
Trigger these rules when writing, reviewing, refactoring, or debugging TypeScript code. Specifically activate when handling dynamic or un-typed data (e.g., API responses, parsed JSON), resolving compiler type errors, monkey-patching global variables or DOM elements, mitigating unsafe type assertions, or mitigating strictness configurations (like `noImplicitAny`).

# @Vocabulary
- **Unsoundness**: A state where a symbol's static type assigned by the TypeScript compiler does not match its actual value at runtime, leading to uncaught runtime exceptions.
- **Top Type**: A type that sits at the top of the type hierarchy; every type is assignable to it (e.g., `unknown`).
- **Bottom Type**: A type with an empty domain; no values are assignable to it (e.g., `never`).
- **any**: A dangerous type that effectively disables the type checker. It is paradoxically both a supertype and a subtype of all other types.
- **unknown**: A type-safe alternative to `any`. It is a top type that requires explicit narrowing (via type guards or assertions) before its properties can be accessed or called.
- **Type Assertion**: A type-level construct (using the `as` keyword) that overrides the compiler's inferred type, forcing the compiler to trust the developer.
- **Double Assertion**: Casting a value to `unknown` and then to a target type (e.g., `value as unknown as Target`) to bypass overlapping type constraints.
- **Monkey Patching**: The practice of attaching arbitrary data or methods to built-in runtime objects (like `window`, `document`, or `RegExp.prototype`) at runtime.
- **Bivariance**: A soundness trap in TypeScript where method parameters in class hierarchies accept both supertypes and subtypes, potentially masking hierarchy mismatch errors.
- **Type Coverage**: The percentage of symbols in a codebase that have a statically analyzed type other than `any`.

# @Objectives
- Ruthlessly minimize the presence and scope of `any` to prevent contagious loss of type safety across the codebase.
- Prefer `unknown` over `any` when dealing with data of an unspecified shape, forcing consumers to validate or narrow the data.
- Isolate and hide unavoidable type assertions within the implementation details of strictly typed function boundaries.
- Avoid runtime crashes caused by TypeScript soundness traps (e.g., mutating function parameters, assuming array bounds are safe, or trusting that function calls preserve type refinements).
- Utilize type-safe mechanisms (like interface augmentation) instead of `any` when augmenting global or external environments.

# @Guidelines
- **Narrow the Scope of `any`**: 
  - Never return an `any` type from a function, as it silently destroys type safety for all downstream callers.
  - Apply `any` using inline type assertions (e.g., `param as any`) rather than assigning it to variable declarations (`const x: any`). 
  - When suppressing an error within a large object literal, cast only the offending property to `any`, not the entire object.
- **Use Precise Variants of `any`**:
  - When the general structure is known but the exact type is not, use structural variants: prefer `any[]` or `unknown[]` for arrays, `{[key: string]: any}` or `Record<string, any>` for objects, and `(...args: any[]) => any` for functions.
- **Handle Unknown Data with `unknown`**:
  - Always type parsed dynamic data (like `JSON.parse` or YAML parsers) as `unknown`.
  - Understand the distinct nuances: use `unknown` for any value, `object` for any non-primitive type, and `{}` for any value except `null` and `undefined`.
- **Hide Unsafe Type Assertions**:
  - Do not compromise a public function's return type signature just to satisfy internal compiler errors. 
  - Hide `as Type` assertions, double assertions (`as unknown as Type`), or `@ts-expect-error` directives inside the function body so the consumer relies on a safe, strictly-typed API.
- **Prefer `@ts-expect-error` over `@ts-ignore`**:
  - When forced to suppress a compiler error, use `@ts-expect-error` so the compiler alerts you if the underlying issue is fixed in the future.
- **Type-Safe Monkey Patching**:
  - Never use `(window as any).prop = value`.
  - Prefer `declare global { interface Window { prop: Type; } }` (Module Augmentation) to add global properties safely.
  - Alternatively, create a narrowed local intersection type: `type MyWindow = typeof window & { prop: Type | undefined };`. Account for `undefined` if the property is populated at runtime to avoid race conditions.
- **Avoid Soundness Traps**:
  - **Mutation Variance**: Never mutate function parameters. Explicitly mark object and array parameters as `readonly` or `Readonly<T>` to prevent unsound array/object assignments.
  - **Refinement Invalidation**: Assume that passing an object to a function might mutate it, thereby invalidating any previous type refinements (e.g., `if (obj.prop)`).
  - **Class Hierarchy Signatures**: Ensure child class methods match parent class method signatures exactly. TypeScript's method bivariance will not catch narrowed parameter types in child methods.
  - **Indexed Access**: Treat object and array lookups with caution. Recognize that accessing `arr[3]` or `obj['key']` might return `undefined` at runtime, even if the type checker implies a strict type.
- **Track Type Coverage**: Use tools like `type-coverage` to continuously monitor the codebase and actively eradicate leaked explicit or third-party `any` types.

# @Workflow
1. **Analyze Context**: When addressing a type error or declaring a new data structure, determine if the data shape is fully known.
2. **Select Top Type**: If parsing external data or writing generic wrappers, initially assign the `unknown` type instead of `any`.
3. **Refine Type (If necessary)**: If a specific operation requires escaping the type system, determine the narrowest possible representation (e.g., `any[]` instead of `any`).
4. **Isolate Unsafe Code**: Push the unsafe assertion or suppression into the smallest possible block (an inline cast or isolated object property).
5. **Protect the Boundary**: Wrap the logic inside a function. Explicitly declare the function's parameter types and return type. Do not let `any` leak into the return type.
6. **Verify Soundness**: Check the implementation for accidental mutation of parameters, unsafe array lookups without null checks, or invalid refinements. Apply `readonly` where mutation is not intended.
7. **Document Deviations**: If a type assertion is entirely unavoidable, leave a comment explaining why the assertion is mathematically or logically sound.

# @Examples (Do's and Don'ts)

**Scope of `any`**
- [DO]:
  ```typescript
  function eatDinner() {
    const pizza = getPizza();
    eatSalad(pizza as any); // Scoped to just this argument
    pizza.slice(); // Still strictly typed as Pizza
  }
  ```
- [DON'T]:
  ```typescript
  function eatDinner() {
    const pizza: any = getPizza(); // Contagious
    eatSalad(pizza);
    pizza.slice(); // Unchecked at compile time
  }
  ```

**Returning `any`**
- [DO]:
  ```typescript
  function parseData(input: string): unknown {
    return JSON.parse(input);
  }
  ```
- [DON'T]:
  ```typescript
  function parseData(input: string): any {
    return JSON.parse(input); // Leaks `any` to all callers
  }
  ```

**Precise Variants of `any`**
- [DO]:
  ```typescript
  function getLength(arr: any[]) {
    return arr.length; // Returns `number`, safe array operations
  }
  ```
- [DON'T]:
  ```typescript
  function getLength(arr: any) {
    return arr.length; // Returns `any`, accepts non-arrays like `/regex/`
  }
  ```

**Hiding Unsafe Assertions**
- [DO]:
  ```typescript
  async function fetchPeak(id: string): Promise<MountainPeak> {
    const response = await fetch(`/api/${id}`);
    // Hide the assertion inside the well-typed boundary
    return response.json() as Promise<MountainPeak>; 
  }
  ```
- [DON'T]:
  ```typescript
  // Changing the signature to `Promise<any>` or `Promise<unknown>` forces the consumer to cast
  async function fetchPeak(id: string): Promise<any> {
    const response = await fetch(`/api/${id}`);
    return response.json(); 
  }
  ```

**Monkey Patching**
- [DO]:
  ```typescript
  declare global {
    interface Window {
      myCustomData: UserData | undefined;
    }
  }
  window.myCustomData = { name: 'Alice' };
  ```
- [DON'T]:
  ```typescript
  (window as any).myCustomData = { name: 'Alice' };
  ```

**Double Assertions**
- [DO]:
  ```typescript
  const target = source as unknown as TargetType;
  ```
- [DON'T]:
  ```typescript
  const target = source as any as TargetType;
  ```

**Avoiding Soundness Traps (Mutation Variance)**
- [DO]:
  ```typescript
  function processAnimals(animals: readonly Animal[]) {
    // Cannot mutate `animals`, preventing invalid covariance states
  }
  ```
- [DON'T]:
  ```typescript
  function processAnimals(animals: Animal[]) {
    // Array mutation can insert a Fox into a Hen[] at runtime without static errors
    animals.push(new Fox());
  }
  ```