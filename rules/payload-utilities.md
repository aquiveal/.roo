# Payload Utilities

This document defines the rules for implementing business logic and utility functions in Payload CMS.

## Pure Functions for Business Logic

**Context:** Functions that rely on global state or external services are hard to test and debug. Pure functions (deterministic output for given input) are reliable and easy to unit test.
**Directive:** ALWAYS prefer pure functions for logic that doesn't strictly require database access or side effects.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Dependent on external scope or implicit state
let currentTaxRate = 0.2

export const calculateTotal = (order) => {
  // Hard to test because it depends on 'currentTaxRate' variable
  return order.subtotal * (1 + currentTaxRate)
}
```

### ✅ Best Practice (What to do)
```typescript
// Pure function - all dependencies are arguments
export const calculateTotal = (subtotal: number, taxRate: number): number => {
  return subtotal * (1 + taxRate)
}

// Usage
const total = calculateTotal(order.subtotal, 0.2)
```

## Proper Server-Side Data Fetching

**Context:** When fetching data outside of the standard Payload hooks (e.g., in a server component or cron job), you must initialize Payload correctly. Using direct DB calls bypasses Payload hooks and access control.
**Directive:** ALWAYS use the Local API (`payload.find`, `payload.create`) initiated via `getPayload` for server-side operations.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Direct DB access bypassing Payload logic
import mongoose from 'mongoose'

export const getRedirects = async () => {
  // Skips hooks, validation, and access control!
  return await mongoose.connection.db.collection('redirects').find({}).toArray()
}
```

### ✅ Best Practice (What to do)
```typescript
import { getPayload } from 'payload'
import configPromise from '@payload-config'

export const getRedirects = async () => {
  const payload = await getPayload({ config: configPromise })

  // Uses Payload logic (hooks, access control if specified)
  const { docs } = await payload.find({
    collection: 'redirects',
    limit: 0,
  })

  return docs
}
```

## Caching Heavy Operations

**Context:** Frequent database reads for static content (like menus or redirects) can slow down the application.
**Directive:** USE Next.js `unstable_cache` (or standard `cache`) to memoize expensive read operations.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Fetches from DB on every single request
export const getMainMenu = async () => {
  const payload = await getPayload({ config: configPromise })
  return payload.findGlobal({ slug: 'main-menu' })
}
```

### ✅ Best Practice (What to do)
```typescript
import { unstable_cache } from 'next/cache'
import { getPayload } from 'payload'
import configPromise from '@payload-config'

// Cached version
export const getMainMenu = unstable_cache(
  async () => {
    const payload = await getPayload({ config: configPromise })
    return payload.findGlobal({ slug: 'main-menu' })
  },
  ['main-menu'], // Cache key
  { tags: ['global-main-menu'] } // Revalidation tags
)
```
