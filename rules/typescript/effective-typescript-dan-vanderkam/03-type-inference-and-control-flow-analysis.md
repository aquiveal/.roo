# @Domain
TypeScript software development, specifically focusing on type declaration, variable initialization, type inference, control flow analysis, object construction, refactoring, and asynchronous data flows. These rules trigger when writing TypeScript code, handling TypeScript compiler errors, refactoring JavaScript to TypeScript, or designing type-safe functions and variables.

# @Vocabulary
*   **Type Inference**: The process by which the TypeScript compiler deduces the type of a variable based on its initialization or context, removing the need for explicit type annotations.
*   **Control Flow Analysis**: The compiler's ability to track the execution paths of code (e.g., `if` statements, `switch`, `return`, `throw`) to refine and narrow types at specific locations.
*   **Widening**: The process where TypeScript infers a broader type from a literal value (e.g., inferring `string` from `'x'`, or `number[]` from `[1, 2]`) to balance specificity and flexibility.
*   **Narrowing / Refinement**: The process of going from a broader type (like a union) to a more specific type using control flow constructs (e.g., `typeof`, `instanceof`, property checks, or tagged unions).
*   **Tagged Union (Discriminated Union)**: A union of object types that share a common literal property (the "tag" or "discriminant") used to explicitly narrow the type in a `switch` or `if` statement.
*   **Type Guard (User-Defined)**: A function returning a type predicate (e.g., `el is HTMLInputElement`) that instructs the compiler to narrow a variable's type if the function returns `true`.
*   **Evolving `any`**: A special compiler behavior where variables initialized to `null`, `undefined`, or `[]` start as `any` but "evolve" their types based on subsequent assignments or `.push()` operations.
*   **Const Context (`as const`)**: A type assertion that prevents widening, inferring the narrowest possible literal types, deep `readonly` objects, and `readonly` tuples.
*   **Satisfies Operator (`satisfies`)**: An operator that ensures a value matches a type constraint without widening or altering the precisely inferred type of the literal value.
*   **Aliasing**: Introducing a new variable name for an existing value (e.g., an object property), which can decouple the alias from the compiler's control flow analysis on the original property.
*   **Currying**: The technique of translating a function taking multiple arguments into a sequence of functions taking single arguments, used in TypeScript to create separate generic type inference sites.
*   **Transitive Type Loss**: When a value is extracted from its usage context (e.g., passing an inline callback to an external variable), causing the compiler to lose contextual typing and infer `any` or broad types.

# @Objectives
*   Maximize the compiler's ability to infer types automatically to keep code uncluttered, legible, and highly refactorable.
*   Eliminate redundant type annotations that provide no extra safety and increase maintenance overhead.
*   Leverage control flow analysis to narrow types predictably, avoiding the use of dangerous type assertions (`as`).
*   Prevent unintended type widening by correctly utilizing `const`, `as const`, and `satisfies`.
*   Maintain accurate types during asynchronous operations and collection transformations by favoring modern, functional paradigms.
*   Avoid breaking control flow analysis through inconsistent aliasing or unpredictable mutations.

# @Guidelines

## Type Inference & Annotations
*   **Avoid Cluttering**: NEVER annotate local variables with explicit types if TypeScript can correctly infer them from the initial value. 
*   **Destructuring**: USE destructuring assignments to extract variables from objects and arrays; allow the compiler to infer their types automatically.
*   **Function Boundaries**: MUST explicitly annotate function parameters. ONLY annotate return types when a function has multiple `return` branches, is part of a public API, or requires a specific named type to prevent implementation details from leaking.
*   **Contextual Typing**: When extracting inline callbacks or literal objects into separate variables, BE AWARE that they lose contextual inference. MUST explicitly annotate the extracted variable, use `as const`, or prefer keeping the callback/object inline.
*   **No Variable Reuse**: NEVER reuse a variable to hold a differently typed value. MUST introduce a new variable (preferably `const`) with a semantic name to allow the compiler to infer a distinct, accurate type.

## Controlling Widening
*   **Base Types**: RECOGNIZE that `let` declarations widen literal values to their base types (e.g., `'x'` widens to `string`). USE `const` to restrict variables to their literal types when reassignment is not needed.
*   **Const Contexts**: USE `as const` after an object, array, or literal to forcefully prevent widening, producing deep `readonly` properties and tuples instead of arrays.
*   **Satisfies Operator**: USE the `satisfies` operator to validate that an object literal conforms to a specific interface without widening its values or losing its exact keys.

## Object Creation & Evolution
*   **Build All at Once**: NEVER create an empty object `{}` and mutate it piece-by-piece to add properties. MUST build objects all at once using object literals.
*   **Object Spread**: USE the object spread operator (`...`) to merge objects or build them up safely.
*   **Conditional Properties**: USE conditional spread syntax (`...(condition ? { prop: val } : {})`) to add properties in a type-safe manner conditionally.
*   **Evolving Arrays**: WHEN building an array piece-by-piece, initialize it as `[]` and allow TypeScript to evolve its type via `.push()`. AVOID reading from an evolving array before assigning values to it to prevent `implicit any` errors.

## Type Narrowing & Control Flow
*   **Refinement**: USE standard JavaScript control flow (`if`, `switch`, `return`, `throw`) combined with `typeof`, `instanceof`, `in`, and `Array.isArray()` to narrow broad union types naturally.
*   **Tagged Unions**: PREFER tagged/discriminated unions (objects sharing a literal string `type` or `kind` property) for complex state shapes. USE `switch` statements on the tag to allow the compiler to narrow cases easily.
*   **Custom Type Guards**: USE user-defined type guards (functions returning `arg is Type`) to encapsulate complex type-checking logic that TypeScript cannot infer automatically.
*   **Avoid Type-changing Callbacks**: DO NOT assume type refinements on object properties remain valid after calling synchronous or asynchronous callbacks, as callbacks might mutate the object. Pass `readonly` data if guarantees are needed.
*   **Consistent Aliasing**: IF you alias an object property (e.g., `const box = polygon.bbox;`), MUST use that alias consistently for both the type refinement check and the subsequent logic. NEVER mix the alias and the original property path.

## Functional & Asynchronous Type Flows
*   **Functional Constructs**: PREFER built-in array methods (`map`, `filter`, `flat`, `reduce`) or utility libraries (like Lodash) over manual `for` loops. Types flow perfectly through these constructs without manual annotation.
*   **Async/Await over Callbacks**: MUST use `async` and `await` instead of raw Promises or nested callbacks to ensure types flow correctly and execution order is clearly typed.
*   **Async Returns**: IF a function returns a `Promise`, MUST explicitly declare it with the `async` keyword, even if it does not use `await` internally.
*   **Combinators**: USE `Promise.all` and `Promise.race` to combine asynchronous flows; TypeScript natively extracts and infers the correct tuple and union types from them.

## Advanced Inference Control
*   **Partial Inference (Classes/Currying)**: WHEN a generic function requires one type parameter to be provided explicitly but another to be inferred from arguments, MUST restructure the function. USE a generic Class or a Curried function (`fn<Explicit>()(inferredArg)`) because TypeScript evaluates inference strictly as "all or nothing".

# @Workflow
1.  **Initialization**: Define local variables with `const` and omit type annotations, relying on the value to infer the type.
2.  **Object Building**: Group all property initializations into a single object literal. Use spread syntax for combinations and conditional additions.
3.  **Signature Definition**: Add explicit types to function parameters. Decide if a return type annotation is necessary (e.g., for an exported API or complex multi-return logic).
4.  **Refining Unions**: When dealing with union types, use a type guard (`in`, `typeof`, `tag === 'literal'`) to narrow the type before accessing specific properties. 
5.  **Handling Aliases**: If destructuring or extracting a property into a variable, use the newly extracted variable for all subsequent `if` checks and logic.
6.  **Validating inference**: Hover over symbols (or utilize Language Service feedback) to verify that types have not widened to `any` or overly broad base types (`string`, `number[]`).
7.  **Correction**: If unexpected widening occurs, apply `as const`, `satisfies`, or inline the value back into its contextual usage site.

# @Examples

## Inferable Types
**[DO]**
```typescript
// Types are accurately inferred; no noise.
const axis = 'y'; // Type is "y"
const square = (nums: number[]) => nums.map(x => x * x);
const squares = square([1, 2, 3]); // Type is number[]
```

**[DON'T]**
```typescript
// Redundant and less precise type annotations.
const axis: string = 'y'; // Widens literal type unnecessarily
const square = (nums: number[]): number[] => nums.map(x => x * x);
```

## Variable Reuse
**[DO]**
```typescript
const productIdStr = "12-34-56";
fetchProduct(productIdStr);

const productIdNum = 123456;
fetchProductBySerialNumber(productIdNum);
```

**[DON'T]**
```typescript
let productId: string | number = "12-34-56";
fetchProduct(productId);
productId = 123456; // Repurposing variable causes confusion and union complexity
fetchProductBySerialNumber(productId);
```

## Widening and `satisfies`
**[DO]**
```typescript
type Point = [number, number];
// Validates type but keeps keys precise (e.g., 'ny', 'ca' are known)
const capitals = {
  ny: [-73.7562, 42.6526],
  ca: [-121.4944, 38.5816]
} satisfies Record<string, Point>;

const nyLat = capitals.ny[1]; // Type is exactly [number, number]
```

**[DON'T]**
```typescript
const capitals: Record<string, [number, number]> = {
  ny: [-73.7562, 42.6526],
  ca: [-121.4944, 38.5816]
};
// Loses knowledge of exact keys 'ny' and 'ca', widening to any string key.
```

## Object Creation
**[DO]**
```typescript
interface Point { x: number; y: number; }
// Build all at once
const pt: Point = { x: 3, y: 4 };

// Conditional additions
const hasZ = true;
const pt3D = { ...pt, ...(hasZ ? { z: 5 } : {}) };
```

**[DON'T]**
```typescript
const pt = {};
pt.x = 3; // Error: Property 'x' does not exist on type '{}'
pt.y = 4; // Error: Property 'y' does not exist on type '{}'
```

## Type Narrowing and Aliasing
**[DO]**
```typescript
function isPointInPolygon(polygon: Polygon, pt: Coordinate) {
  const { bbox } = polygon; // Destructure alias
  if (bbox) {
    // Consistently use alias `bbox`
    if (pt.x < bbox.x[0] || pt.x > bbox.x[1]) {
      return false;
    }
  }
}
```

**[DON'T]**
```typescript
function isPointInPolygon(polygon: Polygon, pt: Coordinate) {
  const box = polygon.bbox; // Create alias
  if (polygon.bbox) { // Refine original property
    if (pt.x < box.x[0]) { // Error: 'box' is possibly 'undefined' because the alias wasn't refined
      return false;
    }
  }
}
```

## Asynchronous Type Flows
**[DO]**
```typescript
async function fetchPages() {
  try {
    const [res1, res2] = await Promise.all([fetch(url1), fetch(url2)]);
    // res1 and res2 are properly inferred
  } catch (e) {
    // Handle error
  }
}
```

**[DON'T]**
```typescript
function fetchPages() {
  fetch(url1).then(res1 => {
    fetch(url2).then(res2 => {
      // Pyramid of doom, poor type tracking and execution mapping
    });
  });
}
```

## Creating Inference Sites via Currying
**[DO]**
```typescript
// Restructure to allow explicit API type, but infer Path type.
declare function fetchAPI<API>(): <Path extends keyof API>(path: Path) => Promise<API[Path]>;

const fetchSeedAPI = fetchAPI<SeedAPI>(); // Explicit param
const berry = await fetchSeedAPI('/seed/strawberry'); // Inferred param
```

**[DON'T]**
```typescript
declare function fetchAPI<API, Path extends keyof API>(path: Path): Promise<API[Path]>;

// Error: Expected 2 type arguments, but got 1. Cannot partially infer generics.
const berry = await fetchAPI<SeedAPI>('/seed/strawberry'); 
```