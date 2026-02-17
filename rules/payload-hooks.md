# Payload Hooks

This document outlines the rules for implementing Hooks in Payload CMS.

## Separation of Concerns

**Context:** Inline hooks inside collection configs make the file monolithic and hard to unit test. It mixes configuration data with complex business logic.
**Directive:** ALWAYS extract hook logic into separate files in `src/hooks/` (for shared) or `src/collections/[Collection]/hooks/` (for specific).

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/collections/Posts.ts
export const Posts: CollectionConfig = {
  slug: 'posts',
  hooks: {
    beforeChange: [
      // Inline complex logic
      async ({ data, req }) => {
        if (data.status === 'published' && !data.publishedAt) {
          data.publishedAt = new Date()
        }
        if (data.title) {
          // logic to slugify title inline...
          data.slug = data.title.toLowerCase().replace(/ /g, '-')
        }
        // ... more logic
        return data
      }
    ]
  }
}
```

### ✅ Best Practice (What to do)
```typescript
// src/hooks/populatePublishedAt.ts
import type { CollectionBeforeChangeHook } from 'payload'

export const populatePublishedAt: CollectionBeforeChangeHook = ({ data }) => {
  if (data.status === 'published' && !data.publishedAt) {
    return {
      ...data,
      publishedAt: new Date(),
    }
  }
  return data
}

// src/collections/Posts.ts
import { populatePublishedAt } from '../hooks/populatePublishedAt'

export const Posts: CollectionConfig = {
  slug: 'posts',
  hooks: {
    beforeChange: [populatePublishedAt], // Clean and readable
  },
}
```

## Strictly Typed Hooks

**Context:** Payload provides specific types for every hook (`CollectionBeforeChangeHook`, `FieldHook`, etc.). Using these types ensures you access `data`, `originalDoc`, and `req` correctly.
**Directive:** ALWAYS explicitly type your hook functions using Payload's exported hook types.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Implicit types or 'any'
export const myHook = (args) => {
  // TypeScript doesn't know what 'args' contains
  // You might try to access args.doc when it's actually args.originalDoc
  console.log(args.doc.title)
}
```

### ✅ Best Practice (What to do)
```typescript
import type { CollectionAfterChangeHook } from 'payload'
import type { Post } from '../payload-types' // Generated types

// Explicit type allows TS to validate return type and arguments
export const myHook: CollectionAfterChangeHook<Post> = ({ doc, req }) => {
  // 'doc' is typed as Post
  console.log(doc.title)
  return doc
}
```

## Field-Level vs Collection-Level Hooks

**Context:** Using a collection hook to modify a single field (like a slug) makes the collection hook know too much about specific fields. It's better to co-locate logic with the definition.
**Directive:** USE field-level hooks for logic that pertains to a single field (like validation or formatting), and collection-level hooks for logic that involves multiple fields or side effects.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Collection hook managing specific field logic
hooks: {
  beforeChange: [
    ({ data }) => {
      // Logic for 'slug' field buried in collection hook
      if (data.title) data.slug = format(data.title)
      return data
    }
  ]
}
```

### ✅ Best Practice (What to do)
```typescript
fields: [
  {
    name: 'slug',
    type: 'text',
    hooks: {
      // Logic attached directly to the field
      beforeValidate: [formatSlug('title')]
    }
  }
]
```
