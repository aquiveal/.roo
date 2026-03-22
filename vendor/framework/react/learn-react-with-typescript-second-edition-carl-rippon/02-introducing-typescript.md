# @Domain
TypeScript development tasks; activating whenever the AI is requested to write, refactor, or debug TypeScript code (`.ts`, `.tsx`), configure the TypeScript compiler (`tsconfig.json`), or resolve typing errors in a JavaScript/TypeScript codebase.

# @Vocabulary
- **Transpilation**: The process of converting TypeScript code into executable JavaScript.
- **IntelliSense**: Code editor feature that provides context-aware code completion, robust code navigation, and refactoring by leveraging the TypeScript type system.
- **Type Annotation**: Explicitly defining the type of a variable, parameter, or return value using a colon followed by the type (e.g., `: number`).
- **Type Inference**: TypeScript's automatic deduction of a variable's type based on its initially assigned value, negating the need for explicit type annotations.
- **Type Widening/Narrowing**: The process of refining a generic or `unknown` type into a more specific, usable type via runtime checks.
- **Type Predicate**: A special return type syntax (e.g., `variable is Type`) used in validation functions to tell the TypeScript compiler to narrow the type of the passed variable if the function returns `true`.
- **Intersection Type**: Combining multiple types into one using the `&` symbol.
- **Union Type**: A type representing the mathematical union of multiple types (e.g., `"A" | "B" | "C"`), allowing a variable to hold any of the specified values.
- **String Enumeration**: An enumeration (`enum`) where the underlying values are explicitly assigned strings, bypassing the type-safety flaws of default numeric enumerations.

# @Objectives
- Catch potential runtime bugs at compile-time by enforcing strict, accurate typings across the codebase.
- Maximize developer productivity and code readability by leaning on type inference rather than over-annotating code.
- Prevent the circumvention of the type system by actively avoiding the `any` type in favor of strongly-typed alternatives like `unknown`.
- Standardize the definition of complex object shapes and functions using `type` aliases over `interface` declarations.
- Configure the TypeScript compiler to aggressively catch errors and prevent the emission of faulty JavaScript.

# @Guidelines
- **Prioritize Type Inference**: The AI MUST rely on type inference when a variable is initialized with a value. Explicit type annotations MUST ONLY be used when type inference is not possible (e.g., uninitialized variables, function parameters, or enforcing a specific narrower type).
- **Variable Declaration Constancy**: The AI MUST use `const` for variables whose values never change after initial assignment, and `let` for variables that do.
- **Ban the `any` Type**: The AI MUST NOT use the `any` type. If the shape of data is not known ahead of time (e.g., fetching from a third-party API), the AI MUST use the `unknown` type.
- **Narrowing `unknown` Data**: When dealing with `unknown` types, the AI MUST write validation functions utilizing Type Predicates (e.g., `data is ExpectedType`) and the `in` operator to safely widen/narrow the type before interacting with its properties.
- **Proper Use of `void` vs `undefined`**: If a function does not return a value, the AI MUST set the return type to `void`. The AI MUST NOT use `undefined` as a return type for functions that simply lack a `return` statement, as `undefined` expects an explicit return of the `undefined` value.
- **Proper Use of `never`**: The AI MUST use the `never` type exclusively for code areas that are mathematically unreachable (e.g., an infinite loop `while (true)` that lacks a `break` statement).
- **Arrays Definition**: The AI MUST denote arrays either by appending `[]` to the type (e.g., `number[]`) or using the generic syntax `Array<type>` (e.g., `Array<number>`).
- **Object Type Optionality**: The AI MUST use the `?` symbol to denote optional properties in object types and optional parameters in functions.
- **Prefer Type Aliases over Interfaces**: The AI MUST define custom object structures, function signatures, and combined types using type aliases (`type`) rather than `interface`.
- **Type Composition**: The AI MUST use the `&` operator to compose intersection types when extending existing type aliases.
- **Class Property Initialization**: When defining classes, the AI MUST ensure properties are properly typed and initialized to avoid compiler errors. The AI MUST utilize the public constructor shorthand (`constructor(public name: string)`) to automatically create and assign class properties, reducing boilerplate.
- **Avoid Numeric Enums**: The AI MUST NOT use default (numeric) enumerations, as they allow assignment of out-of-range numbers without raising type errors. 
- **Prefer String Unions**: The AI MUST use string union types (e.g., `type Level = "H" | "M" | "L"`) to represent specific sets of meaningful strings. If the strings themselves are not descriptive enough, the AI MUST use a String Enumeration (`enum Level { High = "H" }`).
- **Strict Compiler Configuration**: When generating or modifying `tsconfig.json`, the AI MUST ensure `"strict": true` is enabled, and MUST set `"noEmitOnError": true` to prevent the compiler from generating JavaScript files if type errors are present.

# @Workflow
1. **Variable Initialization**: When declaring a new variable, assign it immediately if possible and omit the type annotation to allow TypeScript to infer it.
2. **Function Definition**: Define function parameters with explicit types. Use explicit return types primarily when inference fails to capture the developer's intent (like returning `void` or `never`).
3. **Defining Custom Shapes**: When creating a new data structure, declare it using the `type` keyword. If it builds upon an existing shape, use the `&` operator to create an intersection type.
4. **Handling API/Dynamic Data**: 
   - Assign fetched data to a variable typed as `unknown`.
   - Create a separate validation function returning a Type Predicate (`data is SpecificType`).
   - Use the `in` and `typeof` operators inside the validation function to verify the presence and types of expected properties.
   - Wrap interactions with the data inside an `if` block that calls the validation function.
5. **Evaluating Value Ranges**: If a variable should only hold a specific set of values, define a string union type. Do not use numeric enums.

# @Examples (Do's and Don'ts)

**[DO] Use type inference for initialized variables.**
```typescript
let flag = false;
let today = new Date();
const numbers = [1, 2, 3];
```

**[DON'T] Over-annotate initialized variables.**
```typescript
let flag: boolean = false;
let today: Date = new Date();
const numbers: number[] = [1, 2, 3];
```

**[DO] Use `unknown` and Type Predicates for dynamic data.**
```typescript
fetch("https://swapi.dev/api/people/1")
  .then((response) => response.json())
  .then((data: unknown) => {
    if (isCharacter(data)) {
      console.log("name", data.name);
    }
  });

function isCharacter(character: any): character is { name: string } {
  return "name" in character;
}
```

**[DON'T] Use `any` to bypass type checking.**
```typescript
fetch("https://swapi.dev/api/people/1")
  .then((response) => response.json())
  .then((data: any) => {
    console.log("name", data.name);
  });
```

**[DO] Use `void` for functions lacking a return statement.**
```typescript
function logText(text: string): void {
  console.log(text);
}
```

**[DON'T] Use `undefined` for functions lacking a return statement.**
```typescript
function logText(text: string): undefined {
  console.log(text);
}
```

**[DO] Use type aliases and intersection types.**
```typescript
type Product = { name: string; unitPrice?: number };
type DiscountedProduct = Product & { discount: number };
type Purchase = (quantity: number) => void;
```

**[DON'T] Use interfaces as the primary method for defining types.**
```typescript
interface Product { name: string; unitPrice?: number; }
interface DiscountedProduct extends Product { discount: number; }
interface Purchase { (quantity: number): void; }
```

**[DO] Use public constructor parameters for clean class definitions.**
```typescript
class Product {
  constructor(public name: string, public unitPrice: number) {}
}
```

**[DON'T] Write redundant boilerplate for class properties.**
```typescript
class Product {
  name: string;
  unitPrice: number;
  constructor(name: string, unitPrice: number) {
    this.name = name;
    this.unitPrice = unitPrice;
  }
}
```

**[DO] Use String Union Types or String Enumerations.**
```typescript
// Preferable: String Union Type
type Level = "H" | "M" | "L";

// Acceptable if names must map to distinct short values: String Enumeration
enum LevelEnum {
  Low = "L",
  Medium = "M",
  High = "H"
}
```

**[DON'T] Use Numeric Enumerations (as they allow invalid numeric assignments).**
```typescript
enum Level {
  Low = 1,
  Medium = 2,
  High = 3
}
let level = Level.Low;
level = 10; // TypeScript will NOT catch this error natively!
```