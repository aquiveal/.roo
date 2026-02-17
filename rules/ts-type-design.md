# TypeScript Type Design Rules

These rules focus on structuring data models to make invalid states impossible, improving clarity and reducing bugs.

## Prefer Types That Always Represent Valid States

**Context:** Allowing conflicting or inconsistent properties in a type allows the system to enter invalid states. If `isLoading` and `error` can both be true, your UI logic becomes brittle. (Effective TypeScript Item 29)

**Directive:** ALWAYS model state using Tagged Unions (Discriminated Unions) where properties are mutually exclusive, making invalid states unrepresentable.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Common "bag of properties" approach
interface RequestState {
  isLoading: boolean;
  error?: string;
  data?: string[];
}

// It's possible to be loading AND have an error AND have data?
// This requires complex logic to determine what to render
const badState: RequestState = {
  isLoading: true,
  error: "Failed to fetch",
  data: ["Old data"]
};

function render(state: RequestState) {
  if (state.isLoading) {
    return "Loading...";
  } else if (state.error) {
    return `Error: ${state.error}`;
  } else if (state.data) {
    return `Data: ${state.data.join(", ")}`;
  }
  // What if none are true? Or multiple? Logic is ambiguous.
  return "Unknown state";
}
```

### ✅ Best Practice (What to do)
```typescript
// Explicit states using a discriminant 'status' field
interface LoadingState {
  status: 'loading';
}

interface ErrorState {
  status: 'error';
  error: string;
}

interface SuccessState {
  status: 'success';
  data: string[];
}

type RequestState = LoadingState | ErrorState | SuccessState;

// Invalid states are now impossible at the type level
const goodState: RequestState = {
  status: 'error',
  error: "Failed to fetch"
  // data: [] // Error: Object literal may only specify known properties
};

function render(state: RequestState) {
  // TypeScript narrows the type based on 'status'
  switch (state.status) {
    case 'loading':
      return "Loading...";
    case 'error':
      return `Error: ${state.error}`; // Accessing 'error' is safe here
    case 'success':
      return `Data: ${state.data.join(", ")}`; // Accessing 'data' is safe here
  }
}
```

## Push Null Values to the Perimeter of Your Types

**Context:** Mixing `null` values deep inside nested objects creates ambiguity. If an object has multiple nullable properties, it's unclear if they are all null together or independently. (Effective TypeScript Item 33)

**Directive:** ALWAYS push `null` or `undefined` to the outer edges of your types—prefer a nullable object over an object with many nullable properties.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface UserProfile {
  id: string;
  // If settings is implicitly part of the user, why are properties optional?
  // Is it possible to have a theme but no notifications?
  settings?: {
    theme?: 'light' | 'dark';
    notifications?: boolean;
  };
}

function applySettings(user: UserProfile) {
  // Deep checking for every property is tedious and error-prone
  if (user.settings && user.settings.theme) {
    console.log(`Applying ${user.settings.theme} theme`);
  }
}
```

### ✅ Best Practice (What to do)
```typescript
interface UserSettings {
  theme: 'light' | 'dark';
  notifications: boolean;
}

interface UserProfile {
  id: string;
  // The entire settings object is present or absent
  // If present, all required settings are guaranteed
  settings: UserSettings | null; 
}

function applySettings(user: UserProfile) {
  // One check confirms the existence of the entire structure
  if (user.settings) {
    console.log(`Applying ${user.settings.theme} theme`);
  }
}
```

## Prefer Unions of Interfaces to Interfaces with Unions

**Context:** Creating an interface where individual fields are union types (`string | number`) obscures the relationship between those fields. Usually, specific combinations of types go together. (Effective TypeScript Item 34)

**Directive:** ALWAYS create unions of specific interfaces (e.g., `TypeA | TypeB`) rather than a single interface with union properties (`{ x: A | B, y: A | B }`) when properties are correlated.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface Layer {
  // These properties are correlated: 'fill' layout goes with 'fill' paint
  layout: 'fill' | 'line' | 'circle';
  paint: FillPaint | LinePaint | CirclePaint;
}

// This allows invalid combinations
const badLayer: Layer = {
  layout: 'fill',
  paint: { lineWidth: 5 } as LinePaint // Mismatch!
};
```

### ✅ Best Practice (What to do)
```typescript
interface FillLayer {
  layout: 'fill';
  paint: FillPaint;
}

interface LineLayer {
  layout: 'line';
  paint: LinePaint;
}

interface CircleLayer {
  layout: 'circle';
  paint: CirclePaint;
}

type Layer = FillLayer | LineLayer | CircleLayer;

// Error: Type 'line' is not assignable to type 'fill'
/*
const layer: Layer = {
  layout: 'fill',
  paint: { lineWidth: 5 } // Error: missing fill-color, etc.
};
*/
```

## Limit the Use of Optional Properties

**Context:** Optional properties (`?`) can often mask deeper modeling issues. If a property is optional, it means the object is valid without it, which might not be true for all states of your application. (Effective TypeScript Item 37)

**Directive:** ALWAYS consider if an optional property represents a different state (use a Union) or if it's truly optional data. If creating a "partial" update object, use utility types like `Partial<T>` explicitly.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface Product {
  id: string;
  name: string;
  // Is price optional? Or is it unknown? 
  // Or is this interface reused for a "CreateProduct" payload?
  price?: number; 
  currency?: string;
}

function calculateTax(product: Product) {
  // We have to handle undefined everywhere, even if business logic says price exists
  if (product.price !== undefined) {
    return product.price * 0.2;
  }
  return 0;
}
```

### ✅ Best Practice (What to do)
```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  currency: string;
}

// Explicitly separate the "input" type which might lack an ID
type CreateProductInput = Omit<Product, 'id'>;

// Explicitly separate partial updates
type UpdateProductInput = Partial<Product>;

function calculateTax(product: Product) {
  // No checks needed, price is guaranteed
  return product.price * 0.2;
}
```

## Distinguish Excess Property Checking

**Context:** TypeScript allows "excess properties" when assigning to a variable of a broader type (structural typing), but performs "excess property checking" on fresh object literals. Relying on this behavior can be confusing. (Effective TypeScript Item 11)

**Directive:** ALWAYS be aware that `fresh` object literals are checked strictly. If you need to pass an object with extra properties, define an explicit type or usage pattern that allows it, rather than bypassing the check.

### ❌ Anti-Pattern (What to avoid)
```typescript
interface Options {
  title: string;
  darkMode?: boolean;
}

// Typo 'darkmode' is caught here...
// const opts: Options = { title: "App", darkmode: true }; // Error

// ...but NOT here if we pass a variable
const config = {
  title: "App",
  darkmode: true // Typo!
};

// This is accepted because 'config' has at least the required properties of Options
// The 'darkmode' property is effectively ignored and lost
const appOptions: Options = config; 
```

### ✅ Best Practice (What to do)
```typescript
interface Options {
  title: string;
  darkMode?: boolean;
}

// Define the variable with the type immediately to catch errors at definition
const config: Options = {
  title: "App",
  // Compiler catches the typo immediately
  // darkmode: true // Error: 'darkmode' does not exist...
  darkMode: true
};

// If you intentionally need dynamic/extra properties, use an index signature
interface FlexibleOptions {
  title: string;
  [key: string]: unknown; // Explicitly allows extra properties
}

const flexible: FlexibleOptions = {
  title: "Dynamic App",
  extraFeature: 123 // OK
};
```
