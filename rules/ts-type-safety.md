# TypeScript Type Safety Rules

These rules focus on ensuring code soundness and avoiding dangerous escape hatches that compromise the type system.

## Limit Use of `any`

**Context:** The `any` type effectively disables type checking, hiding your type design and masking bugs. It undermines confidence in the type system and harms developer experience by removing language services. (Effective TypeScript Item 5)

**Directive:** ALWAYS use `unknown` or a more specific type instead of `any`, and only use `any` as a last resort when absolutely necessary for interop with untyped libraries.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Using 'any' allows dangerous operations that can crash at runtime
function processUserData(data: any) {
  // We have no idea if 'user' exists or if 'age' is a number
  // This compiles fine but will throw if data is null/undefined
  const ageInYears = data.user.age;
  
  // We can accidentally call methods that don't exist
  // No autocomplete, no type safety
  data.saveToDatabase(); 

  return ageInYears + 10;
}

// 'any' leaks into other parts of the codebase
const result = processUserData({ invalid: "data" }); 
// result is 'any', so this also compiles but crashes
result.toUpperCase(); 
```

### ✅ Best Practice (What to do)
```typescript
// Define a shape for the expected data
interface UserData {
  user?: {
    age?: number;
  };
}

// Use 'unknown' for external data where the shape is not guaranteed
function processUserData(data: unknown): number {
  // We must validate 'data' before using it
  if (typeof data === 'object' && data !== null && 'user' in data) {
    // Narrowing the type safely
    const userData = data as UserData;
    
    if (typeof userData.user?.age === 'number') {
      return userData.user.age + 10;
    }
  }
  
  throw new Error("Invalid user data format");
}

// Or use a validation library like Zod for runtime checks (preferred for APIs)
// const result = UserSchema.parse(data);
```

## Prefer Type Declarations over Type Assertions

**Context:** Type assertions (`as Type`) silence the type checker, telling it you know better. This bypasses validation that type declarations (`: Type`) provide, potentially leading to runtime errors if your assertion is wrong. (Effective TypeScript Item 9)

**Directive:** ALWAYS prefer type declarations (`const x: Type = ...`) over type assertions (`const x = ... as Type`) to ensure value conformity.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

// Using 'as' hides the fact that we are missing required properties
// The compiler trusts us that this empty object is a ButtonProps
const submitButton = {} as ButtonProps;

// Later in the code, this will crash because onClick is undefined
function renderButton(props: ButtonProps) {
  props.onClick(); // Runtime Error: props.onClick is not a function
}

// This also allows adding excess properties without warning
const cancelButton = {
  label: "Cancel",
  onClik: () => {}, // Typo isn't caught!
  style: "red"      // Excess property isn't caught!
} as ButtonProps;
```

### ✅ Best Practice (What to do)
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

// Type declaration enforces that all required properties are present
// Compiler error: Property 'onClick' is missing in type '{ label: string; }'
const submitButton: ButtonProps = {
  label: "Submit",
  onClick: () => console.log("Submitting..."),
};

// Type declaration catches typos and excess properties
// Compiler error: 'onClik' does not exist in type 'ButtonProps'. Did you mean 'onClick'?
const cancelButton: ButtonProps = {
  label: "Cancel",
  onClick: () => console.log("Cancelled"),
  // style: "red" // Error: Object literal may only specify known properties
};
```

## Use `unknown` Instead of `any` for Unknown Values

**Context:** `any` allows you to do anything with a value, which is unsafe. `unknown` is the type-safe counterpart; it encompasses all values but forces you to perform type checks (narrowing) before performing operations on the value. (Effective TypeScript Item 46)

**Directive:** ALWAYS use `unknown` when you don't know the type of a value (e.g., API responses, JSON parsing), forcing validation before use.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Parsing JSON as 'any' is a common source of bugs
function safeParse(json: string): any {
  return JSON.parse(json);
}

const config = safeParse('{"debug": true}');

// The compiler allows this because config is 'any'
// But if the JSON doesn't match this structure, it crashes at runtime
console.log(config.database.host.toUpperCase()); 
```

### ✅ Best Practice (What to do)
```typescript
// Return 'unknown' to signal that the shape is not verified
function safeParse(json: string): unknown {
  return JSON.parse(json);
}

const config = safeParse('{"debug": true}');

// Compiler error: Object is of type 'unknown'
// console.log(config.debug); 

// Must narrow the type first
interface AppConfig {
  database?: {
    host: string;
  };
  debug?: boolean;
}

// Using a user-defined type guard
function isAppConfig(value: unknown): value is AppConfig {
  return (
    typeof value === 'object' && 
    value !== null && 
    'database' in value
  );
}

if (isAppConfig(config)) {
  // Now safely typed as AppConfig
  console.log(config.database?.host); 
}
```

## Avoid Soundness Traps

**Context:** TypeScript's type system is not fully sound; there are cases where the static type does not match the runtime value (e.g., out-of-bounds array access, `any` leakage). Being aware of these traps prevents runtime crashes. (Effective TypeScript Item 48)

**Directive:** ALWAYS code defensively against potentially unsound operations like array indexing, and enable strict compiler flags like `noUncheckedIndexedAccess`.

### ❌ Anti-Pattern (What to avoid)
```typescript
// TypeScript assumes array access is always safe (without noUncheckedIndexedAccess)
function getUpperNames(names: string[]): string[] {
  const result = [];
  
  // Logic error: accessing index 3 when length might be less
  // TypeScript thinks 'name' is 'string', but it's actually 'undefined' at runtime
  const name = names[3]; 
  
  // Runtime Error: Cannot read properties of undefined (reading 'toUpperCase')
  result.push(name.toUpperCase());
  
  return result;
}

const userNames = ["Alice", "Bob"];
getUpperNames(userNames);
```

### ✅ Best Practice (What to do)
```typescript
// Treat array access as possibly undefined
function getUpperNames(names: string[]): string[] {
  const result: string[] = [];
  
  // Even if TS says it's string, checking existence is safer
  // With 'noUncheckedIndexedAccess: true', TS would correctly infer 'string | undefined'
  const name = names[3]; 
  
  if (name !== undefined) {
    result.push(name.toUpperCase());
  }
  
  // Better: Use iteration methods which are safer
  // return names.map(n => n.toUpperCase());
  
  return result;
}
```

## Use User-Defined Type Guards for Safe Narrowing

**Context:** When standard type narrowing (like `typeof` or `instanceof`) isn't enough, user-defined type guards (functions returning `arg is Type`) allow you to centrally logic for validating types, making consuming code cleaner and safer. (Programming TypeScript Ch 6)

**Directive:** ALWAYS use User-Defined Type Guards to encapsulate complex type validation logic, especially for verifying the shape of external data.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Ad-hoc checks repeated everywhere are error-prone and verbose
function processEvent(event: unknown) {
  if (
    typeof event === 'object' && 
    event !== null && 
    'type' in event && 
    (event as any).type === 'click'
  ) {
    // We still have to cast it to use properties safely
    const clickEvent = event as { x: number, y: number };
    console.log(clickEvent.x, clickEvent.y);
  }
}
```

### ✅ Best Practice (What to do)
```typescript
interface ClickEvent {
  type: 'click';
  x: number;
  y: number;
}

interface HoverEvent {
  type: 'hover';
  elementId: string;
}

// Centralized type guard logic
function isClickEvent(event: unknown): event is ClickEvent {
  return (
    typeof event === 'object' &&
    event !== null &&
    (event as any).type === 'click' &&
    'x' in event &&
    'y' in event
  );
}

function processEvent(event: unknown) {
  // Usage is clean and TypeScript automatically narrows the type
  if (isClickEvent(event)) {
    // event is strictly typed as ClickEvent here
    console.log(event.x, event.y); 
  } else {
    // event is unknown (or other remaining types in a union)
    console.log("Unknown event");
  }
}
```
