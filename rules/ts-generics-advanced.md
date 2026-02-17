# TypeScript Generics & Advanced Types Rules

These rules focus on creating flexible, reusable, and DRY type definitions using advanced features without overcomplicating code.

## Think of Generics as Functions Between Types

**Context:** Generics allow you to transform input types into output types, much like a function transforms values. This mental model helps in composing types effectively. (Effective TypeScript Item 50)

**Directive:** ALWAYS design generics with clear input constraints (`extends`) and predictable outputs, treating them as reusable logic for your type system.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Generic parameter 'T' is unconstrained and used loosely
// It's unclear what 'T' should be (an object? a primitive?)
type APIResponse<T> = {
  data: T;
  error?: string;
};

// When usage occurs, it allows anything
const badResponse: APIResponse<number> = { data: 123 };
// But what if our API always returns objects?
const weirdResponse: APIResponse<undefined> = { data: undefined };

// Implementing a helper without constraints
function getField<T, K>(obj: T, key: K) {
  // Unsafe casting often happens here because TS doesn't know T has K
  return (obj as any)[key]; 
}
```

### ✅ Best Practice (What to do)
```typescript
// Constrain T to object to prevent primitives
// Default to unknown to encourage validation
type APIResponse<T extends object = Record<string, unknown>> = {
  data: T;
  error?: string;
};

// Correct usage ensures structure
const userResponse: APIResponse<{ id: string }> = { data: { id: "1" } };

// Generics with constraints enforce relationships
// 'K' must be a key of 'T', so the return type T[K] is safe and inferred
function getField<T extends object, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## Avoid Unnecessary Type Parameters

**Context:** Adding type parameters that don't relate multiple values or provide constraint inference adds noise. If a type parameter is used only once in a function signature, it is likely unnecessary. (Effective TypeScript Item 51)

**Directive:** ALWAYS follow the "Golden Rule of Generics": if a type parameter appears only once, verify if it can be replaced by a concrete type or `unknown`.

### ❌ Anti-Pattern (What to avoid)
```typescript
// 'T' is used only once. It doesn't relate the input to anything else.
// The caller just specifies a type, but it behaves like an assertion.
function parseJson<T>(content: string): T {
  return JSON.parse(content);
}

// User writes this, thinking it's safe
const result = parseJson<number>("not a number"); 
// Runtime confusion: result is actually NaN or string, not checked.

interface UIWidget {
  render(): void;
}

// 'W' is used only once. We don't return 'W', we don't use 'W' elsewhere.
function renderWidget<W extends UIWidget>(widget: W) {
  widget.render();
}
```

### ✅ Best Practice (What to do)
```typescript
// Return 'unknown' to force the caller to validate
function parseJson(content: string): unknown {
  return JSON.parse(content);
}

const raw = parseJson("123");
if (typeof raw === 'number') {
  // Safe usage
}

interface UIWidget {
  render(): void;
}

// Just use the interface directly
function renderWidget(widget: UIWidget) {
  widget.render();
}
```

## Prefer Conditional Types to Overload Signatures

**Context:** Overloads can be verbose and difficult to maintain. Conditional types (`T extends U ? X : Y`) allow for more expressive and concise type definitions that distribute over unions. (Effective TypeScript Item 52)

**Directive:** ALWAYS consider using conditional types to model return types that depend on input types, as they handle unions better and reduce declaration redundancy.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Verbose overloads
function double(x: string): string;
function double(x: number): number;
function double(x: string | number): string | number {
  if (typeof x === "string") return x + x;
  return x * 2;
}

// If we pass a union, it might fail or return a broad type
const val: string | number = "foo";
// This might infer as string | number, losing specificity if not handled perfectly
const res = double(val); 
```

### ✅ Best Practice (What to do)
```typescript
// Conditional type preserves the relationship
// If T is string, return string. If T is number, return number.
function double<T extends string | number>(
  x: T
): T extends string ? string : number {
  if (typeof x === "string") {
    // Cast needed for implementation, but public API is safe
    return (x + x) as any; 
  }
  return (x * 2) as any;
}

// Distributes over unions automatically
const res1 = double("foo"); // Type: string
const res2 = double(10);    // Type: number
```

## Use Type Operations to Avoid Repetition

**Context:** Repeating types leads to maintenance headaches. TypeScript provides tools (`keyof`, `typeof`, `Pick`, mapped types) to derive new types from existing ones, ensuring consistency (DRY). (Effective TypeScript Item 15)

**Directive:** ALWAYS derive types from a "source of truth" (like a main interface or constant) rather than duplicating definitions.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface UserState {
  userId: string;
  name: string;
  age: number;
}

// Duplicating properties manually
interface UserStateUpdate {
  userId?: string;
  name?: string;
  age?: number;
}

// If UserState changes (e.g., 'email' added), Update is stale
```

### ✅ Best Practice (What to do)
```typescript
interface UserState {
  userId: string;
  name: string;
  age: number;
}

// Derived type updates automatically
type UserStateUpdate = Partial<UserState>;

// Deriving from values
const INIT_OPTIONS = {
  width: 640,
  height: 480,
  color: "#00FF00",
  label: "VGA",
};

// Type definition matches the value exactly
type Options = typeof INIT_OPTIONS;
```

## Use `infer` to Extract Types

**Context:** Sometimes you need access to a type that is buried inside another type (e.g., the return type of a function, the element type of an array). The `infer` keyword within conditional types allows you to "unwrap" these types cleanly. (Programming TypeScript Ch 6)

**Directive:** ALWAYS use `infer` (or utility types like `ReturnType`, `Parameters`) to extract internal types rather than manually redefining them.

### ❌ Anti-Pattern (What to avoid)
```typescript
function createUser(id: string, name: string) {
  return { id, name, createdAt: new Date() };
}

// Manually defining the return type creates duplication
type UserObj = { 
  id: string; 
  name: string; 
  createdAt: Date 
};

// If createUser implementation changes, UserObj is wrong
```

### ✅ Best Practice (What to do)
```typescript
function createUser(id: string, name: string) {
  return { id, name, createdAt: new Date() };
}

// Extract the return type directly from the function
type UserObj = ReturnType<typeof createUser>;

// Extracting from a Promise
type AsyncData = Promise<{ data: string[], status: number }>;

// Custom utility to unwrap Promise
type Unpacked<T> = T extends Promise<infer U> ? U : T;

type Data = Unpacked<AsyncData>; // { data: string[], status: number }
```
