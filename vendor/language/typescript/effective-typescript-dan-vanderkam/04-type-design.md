# @Domain
These rules MUST be triggered whenever the AI is tasked with creating, refactoring, designing, or reviewing TypeScript type definitions, interfaces, function signatures, state models, classes, or when handling data payloads from external sources/APIs.

# @Vocabulary
- **Valid State Definition**: A type construct that makes impossible or contradictory states unrepresentable at compile time.
- **Tagged/Discriminated Union**: A union of interfaces where each interface shares a common literal property (the "tag" or "discriminant", e.g., `type: 'success'`) used to narrow the type.
- **Postel's Law (Robustness Principle)**: In function signatures, being liberal in what inputs are accepted (broad types) and strict in what outputs are produced (narrow/canonical types).
- **Perimeter Nulls**: A design pattern where nullability is pushed to the outer boundary of a data structure (e.g., returning a completely nullable object rather than an object with multiple independently nullable properties).
- **Stringly Typed**: An anti-pattern where the generic `string` type is used to represent data that actually belongs to a narrower, finite set of specific string values.
- **Uncanny Valley of Type Safety**: An anti-pattern where an overly complex type attempts to be hyper-precise but fails on edge cases, making it inaccurate and worse than a simpler, slightly imprecise type.
- **Anecdotal Data**: Sample JSON payloads or observed data used to guess a type structure, rather than relying on an official specification or schema.

# @Objectives
- Ensure that data structures and state models absolutely CANNOT represent contradictory or invalid states.
- Establish strict, canonical type boundaries for outputs while maintaining flexible, broad type boundaries for inputs.
- Eliminate implicit, undocumented relationships between properties by explicitly grouping them or using unions of interfaces.
- Maximize the utility of the TypeScript compiler to catch errors without degrading the developer experience (DX) via overly complex, inaccurate types.
- Ensure naming conventions leverage exact domain vocabulary rather than generic structural descriptions.

# @Guidelines

## 1. State and Structure Modeling
- **Enforce Valid States**: The AI MUST NOT use multiple independent optional/boolean flags to represent state (e.g., `isLoading` and `error`). The AI MUST use Tagged Unions to explicitly model mutually exclusive states.
- **Unions of Interfaces**: The AI MUST NOT create interfaces containing multiple properties that are independent union types. The AI MUST create a union of distinct interfaces to accurately model the relationship between properties.
- **Group Optional Properties**: If multiple optional properties are related and should either all be present or all be absent, the AI MUST group them into a single optional object property.
- **Push Nulls to the Perimeter**: The AI MUST NOT design objects where multiple internal values are implicitly related by their nullability. The AI MUST push nullability to the perimeter (e.g., `[number, number] | null` instead of `(number | undefined)[]`).
- **Fully Non-Null Classes**: The AI MUST NOT initialize class properties with `null` pending asynchronous data. The AI MUST use static factory methods (e.g., `static async init()`) to construct fully non-null class instances once all data is available.

## 2. API and Function Signatures
- **Apply Postel's Law**: The AI MUST define function parameter types broadly (using optional properties, unions, or `Iterable<T>` instead of `T[]`) and return types strictly (using canonical, exact forms).
- **Avoid Repeated Parameters**: The AI MUST NOT define function signatures with three or more consecutive parameters of the same type. The AI MUST refactor these into an object parameter with named properties or distinct custom types.
- **No Null/Undefined in Type Aliases**: The AI MUST NOT define top-level type aliases that include `| null` or `| undefined` (e.g., `type User = { ... } | null`) unless the type name explicitly communicates this (e.g., `NullableUser`).

## 3. Type Precision vs. Accuracy
- **Eradicate "Stringly Typed" Code**: The AI MUST NOT use `string` for a variable or property if its valid values belong to a known, finite set. The AI MUST use a union of string literal types.
- **Use `keyof T`**: For parameters expecting object properties, the AI MUST use `keyof T` instead of `string` to ensure type safety and enable IDE autocomplete.
- **Use Distinct Types for Special Values**: The AI MUST NOT use in-domain sentinel values (like `-1`, `0`, or `""`) to represent failure or absence. The AI MUST use `null`, `undefined`, or a Tagged Union, forcing the consumer to explicitly handle the special case.
- **Imprecise > Inaccurate**: If a type cannot be modeled with 100% accuracy, the AI MUST prefer a slightly imprecise type (using `unknown` or a broader union) over a hyper-complex, inaccurate type that rejects valid edge cases.
- **Limit Optional Properties**: The AI MUST minimize the use of optional properties (`?`). When handling configuration objects, the AI MUST define a broad input type with optional fields and a strict internal type with required fields, bridging them with a normalization function.
- **Unify over Modeling Differences**: The AI MUST unify slightly varying data structures (e.g., snake_case database rows vs. camelCase application models) at the runtime boundary via an adapter function, rather than writing complex type-level mappers, unless the external types are strictly out of the developer's control.

## 4. Naming and Documentation
- **No Type Info in Comments**: The AI MUST NOT write JSDoc/TSDoc comments or variable names that duplicate type information (e.g., avoiding `// Returns a string` or `ageNum`). The TypeScript signature MUST be the sole source of truth.
- **Explicit Units**: The AI MUST append unit indicators to numeric variable or property names if the unit is not obvious from the type (e.g., use `timeMs`, `temperatureC`).
- **Domain-Specific Naming**: The AI MUST name types using precise vocabulary from the problem domain. The AI MUST NOT use vague, structural names like `Data`, `Info`, `Item`, or `Entity`.
- **Use `readonly` for Immutability**: The AI MUST NOT use comments to state that a parameter is not modified. The AI MUST use the `readonly` modifier to enforce it.

## 5. Sourcing Types
- **No Anecdotal Types**: The AI MUST NOT hand-author type declarations by inspecting sample JSON data. The AI MUST import types from official libraries (`@types`), or generate them from official specifications (OpenAPI, GraphQL, JSON Schema).

# @Workflow
1. **Analyze the Domain**: Identify the official terminology and the exact boundaries of valid data states. Determine if official schemas/specs exist to generate types.
2. **Design the State**: Model the data using Tagged Unions. Eliminate independent optional flags. Group related properties. Push nulls to the outer perimeter of the structure.
3. **Refine API Boundaries**: Define input parameters loosely (accepting iterables, partials, or multiple formats). Define outputs strictly (returning canonical, fully-formed, non-null structures).
4. **Enforce Type Precision**: Scan for `string`, `number`, or consecutive identical parameter types. Replace them with string literal unions, `keyof T`, or object parameters.
5. **Audit Documentation and Names**: Strip type definitions out of comments. Append units to numbers. Ensure names reflect domain concepts, not generic programmatic structures.
6. **Verify Accuracy**: Check for "uncanny valley" types. If a type is overly complex and likely to fail on edge cases, simplify it.

# @Examples (Do's and Don'ts)

## Representing Valid States
[DON'T] Use independent flags that allow contradictory states.
```typescript
interface RequestState {
  pageText: string;
  isLoading: boolean;
  error?: string; // What if isLoading is true AND error has a string?
}
```

[DO] Use a Tagged Union to enforce mutually exclusive states.
```typescript
interface RequestPending {
  state: 'pending';
}
interface RequestError {
  state: 'error';
  error: string;
}
interface RequestSuccess {
  state: 'ok';
  pageText: string;
}
type RequestState = RequestPending | RequestError | RequestSuccess;
```

## Postel's Law (Liberal Accept, Strict Produce)
[DON'T] Require strict arrays for inputs or return loose/union types.
```typescript
function getCameraOptions(bounds: LngLatBounds): CameraOptions | undefined { ... }
function sum(numbers: number[]): number { ... }
```

[DO] Accept iterables/loose types and return strict, canonical types.
```typescript
function getCameraOptions(bounds: LngLatBoundsLike): Camera;
function sum(numbers: Iterable<number>): number { ... }
```

## Documentation and Naming
[DON'T] Repeat types in comments or use generic names.
```typescript
/** 
 * Returns the delay as a number.
 * Does not modify the input array.
 */
function calculate(delayNum: number, itemData: string[]): number { ... }
```

[DO] Rely on the type system and use domain names/units.
```typescript
function calculateInterval(delayMs: number, usernames: readonly string[]): number { ... }
```

## Perimeter Nulls
[DON'T] Mix nulls and non-nulls inside an array or object.
```typescript
function extent(nums: number[]): (number | undefined)[] { ... } // returns [undefined, undefined]
```

[DO] Push nullability to the perimeter of the type.
```typescript
function extent(nums: number[]): [number, number] | null { ... }
```

## Unions of Interfaces
[DON'T] Create interfaces with independent union properties.
```typescript
interface Layer {
  layout: FillLayout | LineLayout | PointLayout;
  paint: FillPaint | LinePaint | PointPaint;
} // Allows FillLayout mixed with LinePaint
```

[DO] Create a union of distinct interfaces.
```typescript
interface FillLayer { layout: FillLayout; paint: FillPaint; }
interface LineLayer { layout: LineLayout; paint: LinePaint; }
type Layer = FillLayer | LineLayer;
```

## Stringly Typed Code
[DON'T] Use broad strings for finite sets or object properties.
```typescript
interface Album {
  recordingType: string;
}
function pluck<T>(records: T[], key: string): any[] { ... }
```

[DO] Use literal unions and `keyof T`.
```typescript
type RecordingType = 'studio' | 'live';
interface Album {
  recordingType: RecordingType;
}
function pluck<T, K extends keyof T>(records: T[], key: K): T[K][] { ... }
```

## Special Values
[DON'T] Use in-domain sentinel values to represent failure.
```typescript
interface Product {
  priceDollars: number; // Uses -1 if price is unknown
}
```

[DO] Use null/undefined to force explicit handling.
```typescript
interface Product {
  priceDollars: number | null; 
}
```

## Repeated Parameters
[DON'T] Write functions with consecutive parameters of the same type.
```typescript
function drawRect(x: number, y: number, w: number, h: number, opacity: number) { ... }
```

[DO] Combine parameters into an object with named properties or distinct types.
```typescript
interface Point { x: number; y: number; }
interface Dimension { width: number; height: number; }
function drawRect(topLeft: Point, size: Dimension, opacity: number) { ... }
```