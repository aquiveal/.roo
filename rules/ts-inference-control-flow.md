# TypeScript Inference & Control Flow Rules

These rules focus on writing idiomatic, concise TypeScript by leveraging the compiler's intelligence rather than fighting it.

## Avoid Cluttering Code with Inferable Types

**Context:** TypeScript can infer types for most local variables. Adding explicit types where they are not needed adds noise, makes refactoring harder, and can even prevent better type inference (e.g., precise literals vs. primitives). (Effective TypeScript Item 18)

**Directive:** ALWAYS let TypeScript infer types for local variables and simple initializers; only add annotations when the inferred type is incorrect or for function boundaries (parameters/returns).

### ❌ Anti-Pattern (What to avoid)
```typescript
// Redundant annotations add noise and maintenance burden
function calculateTotal(items: { price: number }[]) {
  // TS knows this is number
  let total: number = 0; 
  
  // TS knows this is { price: number }
  for (const item: { price: number } of items) { 
    total += item.price;
  }
  
  // Explicitly typing this as string prevents it from being the literal "USD"
  const currency: string = "USD"; 
  
  return { total, currency };
}
```

### ✅ Best Practice (What to do)
```typescript
function calculateTotal(items: { price: number }[]) {
  // Type inferred as number
  let total = 0;
  
  // Loop variable type inferred automatically from 'items'
  for (const item of items) {
    total += item.price;
  }
  
  // Inferred as "USD" (literal type) because it's const
  const currency = "USD"; 
  
  // Return type inferred as { total: number, currency: string }
  // (or { total: number, currency: "USD" } if using 'as const')
  return { total, currency };
}
```

## Use Different Variables for Different Types

**Context:** In JavaScript, it's possible to reuse a variable for different types of values. In TypeScript, a variable usually has a fixed type. Reusing variables for different types forces you to use union types (`string | number`) which makes subsequent logic harder to write and understand. (Effective TypeScript Item 19)

**Directive:** ALWAYS use distinct, descriptive `const` variables for different concepts rather than reusing a `let` variable for disparate types.

### ❌ Anti-Pattern (What to avoid)
```typescript
function processResponse(response: string | number) {
  let result; 
  // 'result' implicitly has 'any' type here if noImplicitAny is off
  // or must be typed as 'string | number' if on.

  if (typeof response === "string") {
    // Reusing the variable for a string operation
    result = response.trim();
  } else {
    // Reusing the variable for a number operation
    result = response * 2;
  }
  
  // Now 'result' is 'string | number', so we can't safely do string methods
  // result.toUpperCase(); // Error: Property 'toUpperCase' does not exist on type 'number'
  return result;
}
```

### ✅ Best Practice (What to do)
```typescript
function processResponse(response: string | number) {
  // If response is string, we create a specific variable
  if (typeof response === "string") {
    const trimmedResult = response.trim();
    return trimmedResult; // inferred as string
  } else {
    // Distinct variable for the number logic
    const numericResult = response * 2;
    return numericResult; // inferred as number
  }
}
```

## Create Objects All at Once

**Context:** TypeScript infers the type of an object based on its initialization. Adding properties piece-by-piece to an empty object (`{}`) often requires type assertions or partial types, which weakens type safety. (Effective TypeScript Item 21)

**Directive:** ALWAYS prefer building objects all at once using object literals or the spread operator (`...`) to allow TypeScript to correctly infer the complete shape.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface UserConfig {
  id: string;
  role: string;
  isActive: boolean;
}

// Initializing as empty object requires asserting as 'any' or the type
// This hides missing properties (e.g., we forgot 'isActive')
const config = {} as UserConfig;

config.id = "123";
config.role = "admin";
// We forgot config.isActive! The compiler doesn't warn us here.

// Later usage crashes or behaves unexpectedly
if (config.isActive) { // undefined evaluates to false, logic error
  console.log("Active");
}
```

### ✅ Best Practice (What to do)
```typescript
interface UserConfig {
  id: string;
  role: string;
  isActive: boolean;
}

// Compiler enforces all properties are present immediately
const config: UserConfig = {
  id: "123",
  role: "admin",
  isActive: true, // Error if missing
};

// Merging objects? Use spread
const baseConfig = { id: "123", isActive: true };
const adminConfig = { 
  ...baseConfig, 
  role: "admin" 
}; // Inferred correctly as { id: string; isActive: boolean; role: string; }
```

## Understand Type Narrowing

**Context:** TypeScript's control flow analysis can narrow types within conditional blocks (e.g., `if`, `switch`, `throw`). Leveraging this eliminates the need for manual casting and makes code robust against null/undefined. (Effective TypeScript Item 22)

**Directive:** ALWAYS allow TypeScript to narrow types via control flow checks (returning early, throwing errors) rather than manually asserting types after a check.

### ❌ Anti-Pattern (What to avoid)
```typescript
function getElementWidth(element: HTMLElement | null): number {
  if (element) {
    // Redundant non-null assertion (!)
    // We already checked it exists, but we are telling TS again
    return element!.getBoundingClientRect().width;
  }
  
  // Unnecessary 'else' block indentation
  return 0;
}

function processValue(val: string | number) {
  if (typeof val === 'string') {
    // Good narrowing
    console.log(val.toUpperCase());
  }
  
  // Outside the block, val is still string | number
  // Manually casting because we "know" it's a number here is unsafe if logic changes
  console.log((val as number).toFixed(2)); 
}
```

### ✅ Best Practice (What to do)
```typescript
function getElementWidth(element: HTMLElement | null): number {
  // Eliminate null case early
  if (!element) {
    return 0;
  }
  
  // TypeScript knows 'element' is HTMLElement here
  return element.getBoundingClientRect().width;
}

function processValue(val: string | number) {
  if (typeof val === 'string') {
    console.log(val.toUpperCase());
    return; // Return early
  }
  
  // TypeScript knows 'val' MUST be number here because we returned above
  console.log(val.toFixed(2));
}
```

## Understand Type Widening

**Context:** When you initialize a variable, TypeScript must decide on a set of possible values. For `let`, it widens to the primitive type (e.g., `"foo"` -> `string`). For `const`, it keeps the literal type (`"foo"`). Understanding this prevents type mismatches when specific literals are expected. (Programming TypeScript Ch 6)

**Directive:** ALWAYS use `const` or `as const` for values that should be treated as specific literals rather than mutable primitives, especially for configuration objects and union types.

### ❌ Anti-Pattern (What to avoid)
```typescript
// 'method' is inferred as 'string', not "GET" | "POST"
let requestOptions = {
  url: "https://api.example.com",
  method: "GET" 
};

function fetchUrl(url: string, method: "GET" | "POST") { /* ... */ }

// Error: Argument of type 'string' is not assignable to parameter of type '"GET" | "POST"'
fetchUrl(requestOptions.url, requestOptions.method);
```

### ✅ Best Practice (What to do)
```typescript
// Option 1: Use 'const' assertion for the whole object
// Inferred as { readonly url: "...", readonly method: "GET" }
const requestOptions = {
  url: "https://api.example.com",
  method: "GET" 
} as const;

function fetchUrl(url: string, method: "GET" | "POST") { /* ... */ }

// Works because 'GET' is preserved as a literal type
fetchUrl(requestOptions.url, requestOptions.method);

// Option 2: Explicitly type the property if mutable
/*
interface RequestOptions {
  url: string;
  method: "GET" | "POST";
}
*/
```
