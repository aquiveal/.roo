@Domain
These rules MUST be triggered whenever the AI is tasked with generating, reviewing, refactoring, or modifying TypeScript type definitions, interfaces, function signatures, API schemas, or application state shapes. 

@Vocabulary
- **Valid State:** A combination of properties in a type that accurately reflects a possible real-world or runtime condition.
- **Invalid State:** A combination of properties permitted by a type that cannot logically occur at runtime (e.g., `isLoading: true` and `error: 'failed'`).
- **Tagged Union (Discriminated Union):** A union of interfaces where each interface shares a common literal property (the "tag" or "discriminant") used to distinguish them.
- **Postel’s Law (Robustness Principle):** The practice of being liberal/broad in what a function accepts as input, and strict/narrow in what it produces as output.
- **Stringly Typed:** An anti-pattern where the broad `string` type is used to represent values that actually belong to a smaller, finite set of string literals.
- **In-Domain Special Value:** An anti-pattern where standard domain values (like `-1`, `0`, or `""`) are overloaded to signify missing data or errors.
- **Uncanny Valley of Types:** The point at which a type is highly precise but slightly inaccurate, making it more frustrating and error-prone than a simple, imprecise type.
- **Anecdotal Data:** Specifying types by hand based on sample JSON responses or test data rather than a formal specification.

@Objectives
- Guarantee that types make invalid application states unrepresentable.
- Ensure function signatures maximize caller convenience (broad inputs) while maximizing type-safety for the consumer of the result (narrow outputs).
- Eliminate redundant and conflicting information between types, documentation, and variable names.
- Improve code readability and domain alignment by utilizing precise nomenclature and standardizing type shapes.
- Eliminate "stringly typed" code and unsafe special return values.

@Guidelines

**1. Modeling State and Shape (Items 29, 32, 33, 34)**
- The AI MUST design types such that invalid or conflicting states are completely unrepresentable.
- The AI MUST use Tagged Unions (Discriminated Unions) to explicitly model mutually exclusive states (e.g., Network Requests, UI states) instead of using interfaces with multiple optional or boolean flags.
- The AI MUST NOT define top-level type aliases that include `null` or `undefined` (e.g., `type User = { ... } | null;`). Always define the pure type and union it with `null` explicitly at the usage site (e.g., `function foo(user: User | null)`).
- The AI MUST push `null` values to the perimeter of types. If multiple properties are implicitly related such that if one is null the others are null, the AI MUST extract them into a single sub-object that is either fully defined or entirely null.
- The AI MUST NOT use interfaces containing multiple union properties if those properties are logically linked. Instead, construct a union of precise interfaces.

**2. Function Signatures (Items 30, 38)**
- The AI MUST adhere to Postel's Law: Function parameter types MUST be broad (accepting optional properties, union types, or `Iterable<T>`). Function return types MUST be strict and canonical (no optional properties if avoidable, no broad unions).
- The AI MUST NOT define functions with multiple consecutive parameters of the same type. If a function requires 3 or more parameters (or even 2 of the same type), the AI MUST group them into a named options object parameter. (Exception: purely commutative mathematical functions like `max(a, b)`).

**3. Type Precision and Safety (Items 35, 36, 40)**
- The AI MUST NOT use the `string` type if the acceptable values form a finite set. Use a union of string literal types instead.
- The AI MUST use `keyof T` instead of `string` for function parameters that expect the name of a property belonging to object `T`.
- The AI MUST NOT use In-Domain Special Values (e.g., `-1`, `0`, `""`) to indicate failures or missing cases. The AI MUST use `null`, `undefined`, or a tagged union to force the type checker to enforce safety via `strictNullChecks`.
- The AI MUST prefer imprecise types to inaccurate types. Do not write hyper-complex recursive types if they fail to perfectly model runtime reality; fall back to simpler types, `unknown`, or `any` if accuracy cannot be guaranteed.

**4. Documentation and Naming (Items 31, 41)**
- The AI MUST NOT repeat type information in TSDoc/JSDoc comments (e.g., never write "Returns a string" if the return type is `: string`).
- The AI MUST NOT include type names in variable names (e.g., do not use `ageNum`), with the STRICT EXCEPTION of numeric units (e.g., `timeMs`, `temperatureC`), which are required if unbranded.
- The AI MUST NOT state "Does not modify parameter" in comments. Instead, the AI MUST use the `readonly` modifier on the parameter.
- The AI MUST use the specialized vocabulary of the problem domain.
- The AI MUST NOT use meaningless, generic names such as `data`, `info`, `item`, `object`, or `entity`. Name types for what they represent, not their structural shape.

**5. Optional Properties and Unification (Items 37, 39)**
- The AI MUST strictly limit the use of optional properties. If an API accepts optional properties but requires defaults, the AI MUST split the type into an `InputConfig` (with optionals) and a normalized `Config` (with required properties) and write a normalization function.
- The AI MUST NOT build complex mapped types to translate between minor structural differences (like snake_case vs camelCase) if the types can simply be unified into a single standard type across the codebase.

**6. External Types (Item 42)**
- The AI MUST NOT hand-write types based on anecdotal sample data (like JSON console output). 
- The AI MUST use official community types (`@types`), or generate types directly from a schema (e.g., OpenAPI, GraphQL, JSON Schema) using tooling.

@Workflow
When architecting or refactoring types, the AI MUST strictly follow this execution order:
1. **Domain Analysis:** Identify the exact real-world concepts the type represents. Select highly specific domain vocabulary (no `data` or `info`).
2. **State Space Validation:** Map out all possible states the entity can be in. If invalid combinations exist in the current interface, immediately convert the architecture to a Tagged Union.
3. **Null & Optional Consolidation:** Scan for related nullable or optional properties. Group them into distinct sub-objects or distinct interfaces in a union to push the nullability to the perimeter.
4. **Parameter Objectification:** Check function signatures. If multiple arguments share a type, bundle them into a strictly named interface.
5. **Input/Output Asymmetry Check:** Ensure the function parameter types are broad (e.g., `Iterable<T>`) and return types are strictly canonical.
6. **Precision Pass:** Replace all `string` types with string literal unions or `keyof T` where applicable. Replace special values (`-1`) with `null` or `undefined`.
7. **Documentation Purge:** Strip all type names and mechanics from comments. Apply `readonly` instead of documenting immutability. Append unit names to numeric variables.

@Examples (Do's and Don'ts)

**Principle: Prefer Types That Always Represent Valid States**
[DON'T]
```typescript
interface RequestState {
  pageText: string;
  isLoading: boolean;
  error?: string;
}
```
[DO]
```typescript
interface RequestPending { state: 'pending'; }
interface RequestError { state: 'error'; error: string; }
interface RequestSuccess { state: 'ok'; pageText: string; }
type RequestState = RequestPending | RequestError | RequestSuccess;
```

**Principle: Be Liberal in What You Accept and Strict in What You Produce**
[DON'T]
```typescript
function viewportForBounds(bounds: LngLatBounds): LngLatBounds { ... }
function sum(xs: number[]): number { ... }
```
[DO]
```typescript
// Broad input (LngLatBounds), strict output (Camera)
function viewportForBounds(bounds: LngLatBounds): Camera { ... }
// Broad input (Iterable)
function sum(xs: Iterable<number>): number { ... }
```

**Principle: Don't Repeat Type Information in Documentation**
[DON'T]
```typescript
/**
 * Gets the foreground color.
 * @param {string} page - The page name.
 * @returns {Color} The color object.
 * Does not modify the page string.
 */
function getForegroundColor(page?: string): Color { ... }
```
[DO]
```typescript
/** Retrieves the foreground color for a specific application area. */
function getForegroundColor(page?: string): Color { ... }
```

**Principle: Avoid Including null or undefined in Type Aliases**
[DON'T]
```typescript
type User = { id: string; name: string; } | null;
function check(user: User) { ... }
```
[DO]
```typescript
interface User { id: string; name: string; }
function check(user: User | null) { ... }
```

**Principle: Push Null Values to the Perimeter of Your Types**
[DON'T]
```typescript
function extent(nums: Iterable<number>): [number | undefined, number | undefined] { ... }
```
[DO]
```typescript
function extent(nums: Iterable<number>): [number, number] | null { ... }
```

**Principle: Prefer Unions of Interfaces to Interfaces with Unions**
[DON'T]
```typescript
interface Layer {
  layout: FillLayout | LineLayout;
  paint: FillPaint | LinePaint;
}
```
[DO]
```typescript
interface FillLayer { layout: FillLayout; paint: FillPaint; }
interface LineLayer { layout: LineLayout; paint: LinePaint; }
type Layer = FillLayer | LineLayer;
```

**Principle: Prefer More Precise Alternatives to String Types**
[DON'T]
```typescript
interface Album { recordingType: string; }
function pluck<T>(records: T[], key: string): any[] { ... }
```
[DO]
```typescript
type RecordingType = 'studio' | 'live';
interface Album { recordingType: RecordingType; }
function pluck<T, K extends keyof T>(records: T[], key: K): T[K][] { ... }
```

**Principle: Use a Distinct Type for Special Values**
[DON'T]
```typescript
interface Product {
  title: string;
  priceDollars: number; // -1 if price is unknown
}
```
[DO]
```typescript
interface Product {
  title: string;
  priceDollars: number | null;
}
```

**Principle: Limit the Use of Optional Properties**
[DON'T]
```typescript
interface AppConfig {
  darkMode: boolean;
  unitSystem?: 'metric' | 'imperial';
}
```
[DO]
```typescript
interface InputAppConfig {
  darkMode: boolean;
  unitSystem?: 'metric' | 'imperial';
}
interface AppConfig extends InputAppConfig {
  unitSystem: 'metric' | 'imperial'; // Required in the normalized state
}
```

**Principle: Avoid Repeated Parameters of the Same Type**
[DON'T]
```typescript
function drawRect(x: number, y: number, w: number, h: number) { ... }
```
[DO]
```typescript
interface Point { x: number; y: number; }
interface Dimension { width: number; height: number; }
function drawRect(topLeft: Point, size: Dimension) { ... }
```

**Principle: Name Types Using the Language of Your Problem Domain**
[DON'T]
```typescript
interface AnimalInfo {
  name: string;
  endangered: boolean;
}
```
[DO]
```typescript
interface Animal {
  commonName: string;
  conservationStatus: 'CR' | 'EN' | 'VU' | 'LC';
}
```