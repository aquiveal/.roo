# TypeScript API Design Rules

These rules focus on designing clean, usable, and robust function and module interfaces that are easy for clients to use and hard to misuse.

## Be Liberal in What You Accept and Strict in What You Produce

**Context:** APIs should be easy to consume. Accepting broad input types (e.g., `ArrayLike` instead of `Array`, or optional properties) makes functions flexible. However, return types should be precise to avoid forcing consumers to perform extra checks. (Effective TypeScript Item 30)

**Directive:** ALWAYS accept the widest possible valid type for inputs (using unions or interfaces) but return the most specific, narrow type possible for outputs.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface CameraOptions {
  center?: { x: number; y: number };
  zoom?: number;
}

// Strictly requires a specific object shape as input
// Returns a loose partial type that is hard to use
function calculateViewport(
  bounds: { min: { x: number; y: number }; max: { x: number; y: number } }
): Partial<CameraOptions> {
  // ... calculation
  return { zoom: 10 };
}

// Consumer has to match exact input structure manually
// Consumer has to check if 'center' exists in return value
const view = calculateViewport({ min: { x: 0, y: 0 }, max: { x: 100, y: 100 } });
if (view.center) { /* ... */ }
```

### ✅ Best Practice (What to do)
```typescript
interface Point { x: number; y: number; }
interface Camera { center: Point; zoom: number; }

// Accepts any object with x/y properties (structural typing)
// Returns a concrete Camera object (strict output)
function calculateViewport(
  bounds: { min: Point; max: Point }
): Camera {
  // ... calculation
  return { center: { x: 50, y: 50 }, zoom: 10 };
}

// Consumer gets a guaranteed Camera object
const view = calculateViewport({ min: { x: 0, y: 0 }, max: { x: 100, y: 100 } });
console.log(view.zoom); // Safe
```

## Avoid Repeating Parameters of the Same Type

**Context:** Functions with multiple parameters of the same type (e.g., `(x: number, y: number, w: number, h: number)`) are prone to argument swapping bugs which the compiler cannot catch. (Effective TypeScript Item 38)

**Directive:** ALWAYS refactor functions with multiple same-type parameters into a single object parameter (options bag) or use distinct nominal types (branding) to prevent ordering mistakes.

### ❌ Anti-Pattern (What to avoid)
```typescript
// It's easy to swap width and height, or x and y
// The compiler sees (number, number, number, number) and thinks it's fine
function drawRect(
  x: number, 
  y: number, 
  width: number, 
  height: number,
  color: string
) {
  // ...
}

// Is this x, y, w, h? Or x, y, h, w?
drawRect(10, 20, 100, 50, "blue"); 
```

### ✅ Best Practice (What to do)
```typescript
interface RectOptions {
  x: number;
  y: number;
  width: number;
  height: number;
  color: string;
}

// Using a destructured object makes the call site self-documenting
// Order no longer matters
function drawRect({ x, y, width, height, color }: RectOptions) {
  // ...
}

drawRect({
  x: 10,
  y: 20,
  width: 100,
  height: 50,
  color: "blue"
});
```

## Don't Repeat Type Information in Documentation

**Context:** Types *are* documentation. Adding comments that duplicate type information (e.g., `@param {string} url`) creates a maintenance burden where comments drift from the actual code. (Effective TypeScript Item 31)

**Directive:** ALWAYS omit type information from JSDoc/comments. Use comments only to explain *why* or *how*, not *what* (which the type system handles).

### ❌ Anti-Pattern (What to avoid)
```typescript
/**
 * Fetches data from the server.
 * @param {string} url - The URL to fetch from (must be a string)
 * @param {number} [timeout] - Optional timeout in milliseconds
 * @returns {Promise<string>} - A promise that resolves to the response body
 */
function fetchData(url: string, timeout?: number): Promise<string> {
  // ...
}
```

### ✅ Best Practice (What to do)
```typescript
/**
 * Fetches data from the server.
 * @param url - The fully qualified endpoint URL.
 * @param timeout - Aborts the request after this duration.
 * @returns The raw response text.
 */
function fetchData(url: string, timeout?: number): Promise<string> {
  // ...
}
```

## Use `async` Functions Instead of Callbacks

**Context:** Callbacks are hard to compose and type inference often fails or becomes verbose inside nested callbacks. `async/await` provides cleaner control flow and better type inference for return values. (Effective TypeScript Item 27)

**Directive:** ALWAYS use `async` functions returning `Promise<T>` instead of callback-style APIs.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Callback style is hard to chain and type safely
function loadUser(
  id: string, 
  cb: (err: Error | null, user?: User) => void
) {
  // ... implementation
}

loadUser("123", (err, user) => {
  if (err) { /* handle error */ }
  else {
    // We have to check 'user' again or rely on the type definition being perfect
    console.log(user?.name);
  }
});
```

### ✅ Best Practice (What to do)
```typescript
// Async/Await creates a linear flow and return types are inferred automatically
async function loadUser(id: string): Promise<User> {
  // ... implementation (throws on error)
  return { id, name: "Alice" };
}

async function init() {
  try {
    const user = await loadUser("123");
    console.log(user.name); // 'user' is definitely User here
  } catch (err) {
    // Error handling is standard
  }
}
```

## Know the Differences Between `type` and `interface`

**Context:** Interfaces support declaration merging (useful for library authors) and are generally cleaner for object shapes. Types are more flexible (unions, primitives). Consistency is key. (Effective TypeScript Item 13)

**Directive:** ALWAYS use `interface` for defining public API object shapes (to allow extension), and use `type` for unions, intersections, and aliases.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Using type for a simple object structure that might need to be extended
// Users cannot augment this easily if it's in a library
type UserConfig = {
  apiKey: string;
  timeout: number;
};

// Mixing usage inconsistently
interface AdminConfig {
  permissions: string[];
}
```

### ✅ Best Practice (What to do)
```typescript
// Use interface for extensible object shapes
interface UserConfig {
  apiKey: string;
  timeout: number;
}

// Library users can now add properties via declaration merging if needed
// interface UserConfig {
//   debugMode?: boolean;
// }

// Use type for unions or complex transformations
type Config = UserConfig | AdminConfig;

type InputIds = string | number;
```
