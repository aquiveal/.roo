@Domain
When interpreting TypeScript user requests, analyzing TypeScript code files, or generating TypeScript architectures that involve type safety, control flow analysis, object iteration, API design, variadic functions, union types, or primitive type distinction.

@Vocabulary
- **Exhaustiveness Checking**: A static analysis technique using the `never` type to ensure all possible cases of a union type are explicitly handled in code.
- **Bottom Type (`never`)**: A type with an empty domain; no value is assignable to it. Used to flag impossible states or omitted cases.
- **Errors of Omission**: Bugs caused by failing to handle a newly added type case (e.g., adding a case to a union but forgetting to update a `switch` statement).
- **Prototype Pollution**: A security and iteration hazard where properties from `Object.prototype` are inherited and enumerated, requiring safe iteration strategies.
- **Fail Open / Fail Closed**: The dilemma in optimization where a system either updates too frequently (fail open) or drops necessary updates (fail closed).
- **Variadic Functions**: Functions taking a variable number of arguments based on runtime state or generic type resolution.
- **Exclusive Or (XOR)**: A logical construct meaning A or B, but *not* both, contrary to TypeScript's default structural inclusive OR (`|`).
- **Nominal Typing**: A typing discipline where two types are incompatible unless explicitly declared equivalent, contrary to TypeScript's default structural typing.
- **Brands / Branding**: The technique of intersecting a structural type (often a primitive) with a unique marker (e.g., `{ _brand: 'type' }`) to emulate Nominal Typing.
- **Type Guard (Type Predicate)**: A function returning a boolean that refines the type of a variable in the local scope.

@Objectives
- The AI MUST prevent errors of omission by aggressively implementing exhaustiveness checking in control flows.
- The AI MUST implement structurally-safe object iteration techniques based on exactness requirements.
- The AI MUST use the type system to mathematically enforce the synchronization of runtime state/configuration objects with interface definitions.
- The AI MUST model dynamic argument lengths precisely using conditional tuples instead of `any` or function overloads.
- The AI MUST restrict inclusive structural unions to strict Exclusive ORs when modeling divergent properties.
- The AI MUST emulate nominal typing on structurally identical but semantically distinct primitives or objects using the branding pattern.

@Guidelines
- **When performing exhaustiveness checking**, the AI MUST use a `never` type check in the `default` case of `switch` statements or final `else` blocks. The AI MUST implement this via an `assertUnreachable(value: never): never` helper function that throws a runtime error, direct assignment (`const exhaustiveCheck: never = value`), or the `satisfies never` operator.
- **When evaluating exhaustiveness on cross-products of types**, the AI MUST use template literal types (e.g., `${TypeA},${TypeB}`) to force the coverage of all combinatorial cases in a `switch` statement.
- **When a function has multiple branches returning values**, the AI MUST add an explicit return type annotation to ensure TypeScript flags unhandled paths returning `undefined`.
- **When iterating over objects with known keys**, and the AI intends to assume the object has no extra properties, the AI MUST use a type assertion for the key (e.g., `let k = kStr as keyof typeof obj`) or iterate over a `const` array of explicit keys.
- **When iterating over objects that may structurally contain extra properties**, the AI MUST use `Object.entries(obj)` and accept broad key (`string`) and value (`any`) types, or instruct the user to use a `Map` structure if applicable.
- **When syncing a configuration/state object with the keys of an interface**, the AI MUST define the object using a `Record<keyof TheInterface, TargetType>` (e.g., `Record<keyof ScatterProps, boolean>`). The AI MUST NOT use an array of keys (`(keyof TheInterface)[]`) to prevent fail-open/fail-closed dilemmas.
- **When modeling variadic functions where argument signatures depend on another parameter**, the AI MUST use rest parameters combined with a conditional tuple type (e.g., `...args: T extends null ? [] : [params: T]`).
- **When defining tuple elements for variadic functions**, the AI MUST label the tuple elements (e.g., `[params: T]`) to ensure IDE intellisense displays meaningful names to users.
- **When defining a union of types that must be mutually exclusive (XOR)**, and tagged unions are not applicable, the AI MUST define optional `never` properties on each interface to explicitly ban the properties of the opposing interface (e.g., `interface A { a: string; b?: never; }`).
- **When dealing with semantic primitive values (e.g., AbsolutePath vs string, Meters vs Seconds) or requiring runtime proofs (e.g., SortedList)**, the AI MUST implement Nominal Branding. The AI MUST intersect the base type with a branding object (e.g., `string & { _brand: 'abs' }` or a `unique symbol` property).
- **When interacting with branded types**, the AI MUST require users to instantiate the branded type via explicit type guards or wrapper functions, rather than structural assignment.

@Workflow
1. **Analyze Control Flow:** Identify all `switch` and `if/else` chains operating on union types. Inject `never` assertions in terminal paths to force exhaustiveness.
2. **Audit Iteration Logic:** Scan for `for-in` loops. If the structure is strictly sealed, cast the key to `keyof T`. If structural subtyping allows extra properties, switch to `Object.entries`.
3. **Evaluate Object Syncing:** Locate any configuration, cache, or state maps representing keys of another interface. Refactor their type to `Record<keyof T, boolean>` (or applicable value type) to guarantee 1-to-1 strict synchronization.
4. **Refactor Variadic Functions:** Identify overloads or `params?: any` arguments linked to route/action types. Refactor to a single signature using `...args` and conditional labeled tuples.
5. **Enforce Mutual Exclusivity:** Review unions without discriminant tags. Inject `prop?: never` properties to prevent inclusive structural overlap.
6. **Apply Nominal Brands:** Identify primitives or identical structures representing different physical/logical domains. Inject `_brand` intersections and construct associated type-guard validation functions.

@Examples

**Exhaustiveness Checking**
[DO]
```typescript
function assertUnreachable(value: never): never {
  throw new Error(`Missed a case! ${value}`);
}

function getArea(shape: Shape): number {
  switch (shape.type) {
    case 'box':
      return shape.width * shape.height;
    case 'circle':
      return Math.PI * shape.radius ** 2;
    default:
      return assertUnreachable(shape);
  }
}
```
[DON'T]
```typescript
function getArea(shape: Shape) {
  switch (shape.type) {
    case 'box':
      return shape.width * shape.height;
    case 'circle':
      return Math.PI * shape.radius ** 2;
    // Missing 'line' case silently falls through returning undefined
  }
}
```

**Iterating Over Objects**
[DO]
```typescript
for (const kStr in obj) {
  const k = kStr as keyof typeof obj;
  const v = obj[k];
}
// OR
for (const [k, v] of Object.entries(obj)) {
  console.log(k, v);
}
```
[DON'T]
```typescript
for (const k in obj) {
  const v = obj[k]; // Error: Element implicitly has an 'any' type because type has no index signature
}
```

**Synchronizing Records**
[DO]
```typescript
const REQUIRES_UPDATE: Record<keyof ScatterProps, boolean> = {
  xs: true,
  ys: true,
  xRange: true,
  yRange: true,
  color: true,
  onClick: false,
};
```
[DON'T]
```typescript
const PROPS_REQUIRING_UPDATE: (keyof ScatterProps)[] = [
  'xs', 'ys', 'xRange', 'yRange', 'color'
]; // Fails to alert developer when ScatterProps adds a new key
```

**Variadic Functions with Conditional Tuples**
[DO]
```typescript
function buildURL<Path extends keyof RouteQueryParams>(
  route: Path,
  ...args: RouteQueryParams[Path] extends null ? [] : [params: RouteQueryParams[Path]]
) {
  const params = args[0] ?? null;
  return route + (params ? `?${new URLSearchParams(params)}` : '');
}
```
[DON'T]
```typescript
function buildURL(route: keyof RouteQueryParams, params?: any) {
  return route + (params ? `?${new URLSearchParams(params)}` : '');
} // Permits arbitrary and incorrect parameters for routes
```

**Modeling Exclusive Or (XOR)**
[DO]
```typescript
interface OnlyThingOne {
  shirtColor: string;
  hairColor?: never;
}
interface OnlyThingTwo {
  hairColor: string;
  shirtColor?: never;
}
type ExclusiveThing = OnlyThingOne | OnlyThingTwo;
```
[DON'T]
```typescript
interface ThingOne { shirtColor: string; }
interface ThingTwo { hairColor: string; }
type Thing = ThingOne | ThingTwo; // Inclusive OR allows an object with BOTH properties
```

**Brands for Nominal Typing**
[DO]
```typescript
type AbsolutePath = string & { _brand: 'abs' };

function isAbsolutePath(path: string): path is AbsolutePath {
  return path.startsWith('/');
}

function listAbsolutePath(path: AbsolutePath) { ... }
```
[DON'T]
```typescript
function listAbsolutePath(path: string) { ... } // Structurally accepts any string, regardless of validity
```