# @Domain
These rules are activated whenever the AI is writing, refactoring, or reviewing TypeScript code (`.ts`, `.tsx`), specifically during tasks involving complex type definitions, object iteration, switch/if control flow analysis, variadic functions, data structure state modeling, type synchronization, or when strictly constraining the assignability of structurally identical types.

# @Vocabulary
- **Exhaustiveness Checking**: A technique using the type checker to ensure every possible case in a union type is explicitly handled, turning errors of omission into type errors.
- **Bottom Type (`never`)**: A type whose domain is the empty set. No value is assignable to `never`. Used to flag unreachable code or disallow properties.
- **Errors of Omission**: Bugs caused by forgetting to handle a specific case (e.g., adding a new type to a union but failing to update a `switch` statement).
- **Structural Typing**: TypeScript's default type system where types are compatible if their shapes match, regardless of explicit declarations.
- **Nominal Typing**: A type system where compatibility is determined by explicit declarations or names rather than structure.
- **Brand / Tag**: A purely type-level property (e.g., `_brand: 'abs'`) intersected with a primitive or object type to simulate nominal typing within a structural type system.
- **Variadic Function**: A function that accepts a variable number of arguments.
- **Inclusive OR**: TypeScript's default union `|` operator, meaning a value can be Type A, Type B, or structurally both.
- **Exclusive OR (XOR)**: A custom type pattern ensuring a value strictly matches one type in a union and contains NO properties from the other.
- **Fail Open / Fail Closed**: The dilemma when adding properties where code either passively ignores new properties (potentially causing stale behavior) or proactively blocks execution (potentially causing unnecessary redraws/re-evaluations).

# @Objectives
- Eradicate errors of omission by leveraging the `never` type to enforce exhaustive control flow.
- Ensure safe, predictable object iteration that acknowledges structural typing and prototype pollution.
- Synchronize related objects and types automatically by leveraging `Record` types to force developer intervention when properties are added or removed.
- Create strictly typed variadic functions whose argument counts and types dynamically shift based on inferred generics.
- Override structural typing when necessary by explicitly prohibiting overlapping properties (XOR) or simulating nominal typing (Branding).

# @Guidelines

## 1. Exhaustiveness Checking
- **MUST** enforce exhaustive handling of all union members in `switch` and `if` statements using an assignment to `never`.
- **MUST** implement an `assertUnreachable(value: never): never` helper function (or use `value satisfies never`) in the `default` case of a `switch` statement to force a compile-time type error if a union member is unhandled, and to throw a runtime error for unsound JavaScript integrations.
- **MUST** explicitly annotate return types on functions with multiple return branches to ensure TypeScript warns if a newly added union case implicitly returns `undefined`.
- **MUST** consider using template literal types (e.g., `${TypeA},${TypeB}`) combined with exhaustiveness checking to validate every possible cross-product pair of two union types.
- **MAY** utilize the `switch-exhaustiveness-check` linter rule if applicable.

## 2. Iterating Over Objects Safely
- **MUST NOT** expect `for (const k in obj)` to infer `k` as `keyof typeof obj`. TypeScript correctly infers `string` due to structural typing (extra properties may exist) and prototype pollution.
- **MUST** use `Object.entries(obj)` to safely iterate over keys and values when the object might contain additional structurally compliant properties.
- **MUST** use a literal array `as const` and iterate over it (e.g., `for (const k of ['a', 'b', 'c'] as const)`) if you need precisely typed keys and know the exact shape of the object.
- **MUST** explicitly assert the key (`const k = kStr as keyof T`) inside a `for...in` loop ONLY if the object is strictly known to contain only the declared keys.
- **MUST** consider using `Map` instead of standard objects for associative arrays, as `Map` iteration yields precise key-value types safely.

## 3. Keeping Values in Sync with Records
- **MUST** resolve the "fail open vs. fail closed" dilemma by mapping values to a `Record<keyof T, ValueType>` when an object must maintain parity with an interface.
- **MUST** require all keys of an interface in the tracking object to trigger an "Excess Property" type error whenever the interface is updated.

## 4. Modeling Variadic Functions
- **MUST** use generic rest parameters and conditional tuple types to construct functions where the number and types of arguments depend on the first argument.
- **MUST** format the conditional rest parameter as: `...args: (T extends null ? [] : [params: T])`.
- **MUST** explicitly label tuple elements (e.g., `[params: T]`) to ensure the generated function signatures display meaningful parameter names in editor tooltips (avoiding `args_0`).

## 5. Modeling Exclusive OR (XOR)
- **MUST NOT** assume TypeScript's `|` union operator acts as an Exclusive OR. It is inclusive.
- **MUST** use an optional `never` type (`property?: never`) to explicitly disallow a property from appearing on an interface when distinguishing between two structurally overlapping types.
- **MUST** prefer Tagged Unions (discriminated unions) to separate types where possible. If adding a tag is impossible or undesirable, construct an XOR type by mapping excluded keys to `?: never`.

## 6. Nominal Typing via Brands
- **MUST** use "Brands" (intersecting a type with a unique metadata property) to differentiate types that are structurally identical but semantically distinct (e.g., absolute vs. relative paths, specific units of measure, sorted vs. unsorted arrays).
- **MUST** define brands using intersections: `type BrandType = string & { _brand: 'BrandName' }`.
- **MUST** consider using a `unique symbol` for the brand key to completely prevent users from forging the branded type.
- **MUST** implement user-defined type guards (e.g., `function isSorted<T>(arr: T[]): arr is SortedArray<T>`) to validate and legally "cast" unbranded data into branded types at runtime.

# @Workflow
1. **Analyze Control Flow**: Identify any function parsing a union type. Insert an `assertUnreachable(value)` block in the `default` fallback to ensure complete coverage.
2. **Review Object Loops**: If iterating over an object's keys, intercept `for...in` loops. Convert to `Object.entries()` or enforce a rigidly typed key array.
3. **Audit Hardcoded Keys**: If an object literal contains boolean flags or default values corresponding to an interface, type it strictly as `Record<keyof TheInterface, Type>` to force compilation failure upon interface changes.
4. **Refactor Overloads**: If multiple function overloads exist solely to omit trailing arguments, collapse them into a single variadic generic function using `...args: (Condition ? [] : [label: Type])`.
5. **Enforce Exclusivity**: Scan union types for overlapping properties. Map disallowed keys to `?: never` to prevent accidental inclusion.
6. **Apply Brands**: For scalar values (strings, numbers) or opaque arrays that require specific validation (e.g., validated emails, sorted arrays), wrap them in an intersection brand and expose a type guard validator.

# @Examples (Do's and Don'ts)

## Exhaustiveness Checking
**[DON'T]** Leave union `switch` statements without a default constraint, risking silent failures when new types are added.
```typescript
type Shape = Box | Circle | Line;

function drawShape(shape: Shape) {
  switch (shape.type) {
    case 'box': // ...
    case 'circle': // ...
    // If 'line' is missing, it fails silently at runtime.
  }
}
```

**[DO]** Use the `never` type to enforce exhaustiveness.
```typescript
type Shape = Box | Circle | Line;

function assertUnreachable(value: never): never {
  throw new Error(`Missed a case! ${value}`);
}

function drawShape(shape: Shape) {
  switch (shape.type) {
    case 'box': return drawBox(shape);
    case 'circle': return drawCircle(shape);
    case 'line': return drawLine(shape);
    default:
      return assertUnreachable(shape); // Type error if any shape is missing
  }
}
```

## Iterating Over Objects
**[DON'T]** Blindly index into an object using `for...in`.
```typescript
interface ABC { a: string; b: string; c: number; }

function foo(abc: ABC) {
  for (const k in abc) {
    const v = abc[k]; // ERROR: Element implicitly has an 'any' type.
  }
}
```

**[DO]** Use `Object.entries` or a strongly typed key array.
```typescript
function foo(abc: ABC) {
  // Option 1: Object.entries
  for (const [k, v] of Object.entries(abc)) {
    console.log(k, v); 
  }

  // Option 2: Explicit Key Array
  const keys = ['a', 'b', 'c'] as const;
  for (const k of keys) {
    const v = abc[k]; // Safely typed as string | number
  }
}
```

## Keeping Values in Sync with Records
**[DON'T]** Hardcode update checks, which silently fail closed when new properties are added.
```typescript
function shouldUpdate(oldProps: Props, newProps: Props) {
  return oldProps.x !== newProps.x || oldProps.y !== newProps.y;
}
```

**[DO]** Use a `Record<keyof T, boolean>` to force the compiler to demand attention when `Props` changes.
```typescript
const REQUIRES_UPDATE: Record<keyof Props, boolean> = {
  x: true,
  y: true,
  // If a 'z' property is added to Props, this object will throw a type error.
};

function shouldUpdate(oldProps: Props, newProps: Props) {
  for (const [k, check] of Object.entries(REQUIRES_UPDATE)) {
    if (check && oldProps[k as keyof Props] !== newProps[k as keyof Props]) {
      return true;
    }
  }
  return false;
}
```

## Variadic Functions
**[DON'T]** Use loose optional parameters that allow invalid arguments for specific routes.
```typescript
function buildURL(route: string, params?: any) { ... }
```

**[DO]** Use rest parameters with conditional tuple types and labels.
```typescript
interface RouteParams {
  '/': null;
  '/search': { query: string };
}

function buildURL<Path extends keyof RouteParams>(
  route: Path,
  ...args: RouteParams[Path] extends null ? [] : [params: RouteParams[Path]]
) {
  const params = args[0];
  return route + (params ? `?${new URLSearchParams(params)}` : '');
}

buildURL('/'); // Valid, expects 1 arg
buildURL('/search', { query: 'hello' }); // Valid, expects 2 args
```

## Exclusive OR with Optional Never
**[DON'T]** Assume union types restrict the presence of cross-properties.
```typescript
interface ThingOne { a: string; }
interface ThingTwo { b: string; }
type Thing = ThingOne | ThingTwo;

const both: Thing = { a: 'A', b: 'B' }; // Valid! TypeScript | is inclusive.
```

**[DO]** Map the opposing properties to `?: never` to enforce mutual exclusivity.
```typescript
interface OnlyThingOne { a: string; b?: never; }
interface OnlyThingTwo { b: string; a?: never; }
type ExclusiveThing = OnlyThingOne | OnlyThingTwo;

const both: ExclusiveThing = { a: 'A', b: 'B' }; // ERROR!
```

## Nominal Typing (Brands)
**[DON'T]** Pass structurally identical primitives around without validation guarantees.
```typescript
function deleteFile(path: string) { ... } // Dangerous: Takes relative OR absolute strings
```

**[DO]** Intersect the primitive with a brand and use type guards to enforce constraints.
```typescript
declare const brand: unique symbol;
type AbsolutePath = string & { [brand]: 'abs' };

function isAbsolutePath(path: string): path is AbsolutePath {
  return path.startsWith('/');
}

function deleteFile(path: AbsolutePath) { ... }

function handle(p: string) {
  if (isAbsolutePath(p)) {
    deleteFile(p); // Valid
  }
  deleteFile(p); // ERROR: string is not assignable to AbsolutePath
}
```