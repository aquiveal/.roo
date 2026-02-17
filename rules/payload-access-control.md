# Payload Access Control

This document defines the patterns for implementing access control in Payload CMS.

## Functional Access Control

**Context:** Access control logic often needs to be reused across multiple collections (e.g., checking if a user is an admin). Inline functions lead to duplication and potential security inconsistencies.
**Directive:** ALWAYS use pure, exported functions for access control and reuse them across collections.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/collections/Users.ts
export const Users: CollectionConfig = {
  access: {
    // Inline logic duplicated in every collection
    read: ({ req: { user } }) => {
      if (user && user.roles.includes('admin')) return true
      if (user && user.id === req.payload.user?.id) return true
      return false
    },
    update: ({ req: { user } }) => {
       // ... same logic again
       if (user && user.roles.includes('admin')) return true
       return false
    }
  }
}
```

### ✅ Best Practice (What to do)
```typescript
// src/access/isAdmin.ts
import type { Access } from 'payload'
import type { User } from '../payload-types'

export const isAdmin: Access<User> = ({ req: { user } }) => {
  return Boolean(user?.roles?.includes('admin'))
}

// src/collections/Users.ts
import { isAdmin } from '../access/isAdmin'

export const Users: CollectionConfig = {
  access: {
    create: isAdmin, // Reused, clean, and consistent
    delete: isAdmin,
    read: isAdmin,
    update: isAdmin,
  }
}
```

## Strict Type Safety

**Context:** The `user` object on the request can be anything or null. Without strict typing using the generated `User` type, you might access properties that don't exist or misspell role names, leading to runtime errors or security holes.
**Directive:** ALWAYS import and use the generated `User` type in your access control functions to ensure property existence and correct types.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Relying on 'any' or implicit types
export const isEditor = ({ req: { user } }) => {
  // 'role' might be undefined, or typo'd (should be 'roles')
  // No warning from TS if user is any
  return user && user.role === 'editor'
}
```

### ✅ Best Practice (What to do)
```typescript
import type { Access } from 'payload'
import type { User } from '../payload-types' // Generated types

export const isEditor: Access<User> = ({ req: { user } }) => {
  // TypeScript knows 'user' has 'roles' (array), not 'role' (string)
  // Autocomplete helps check for 'editor' if roles is a union type
  return Boolean(user?.roles?.includes('editor'))
}
```

## Row-Level Security

**Context:** Often users should only see their own data. Returning a simple `true/false` isn't enough; you need to return a query constraint.
**Directive:** ALWAYS return a Payload query constraint object (Where clause) when implementing granular row-level access control.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Fetching data manually inside access control - inefficient and dangerous
export const ownData = async ({ req: { user, payload } }) => {
  if (!user) return false
  // Don't do this! Access control should return a query, not filter results in memory
  const docs = await payload.find({ ... })
  return docs.length > 0
}
```

### ✅ Best Practice (What to do)
```typescript
import type { Access } from 'payload'

export const ownData: Access = ({ req: { user } }) => {
  if (!user) return false

  // Return a query constraint that the database executes
  return {
    user: {
      equals: user.id,
    },
  }
}
```
