# Payload Collections and Globals

This document outlines the rules for defining Collections and Globals in Payload CMS.

## Consistent Naming Conventions

**Context:** Consistent naming makes code predictable and easier to navigate. Using PascalCase for files matching the export name is a standard React/TypeScript pattern that works well for Payload configs.
**Directive:** ALWAYS use PascalCase for collection filenames and directory names, and ensure they match the exported constant name.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/collections/users.ts (lowercase file)
export const UsersCollection = { // Name mismatch
  slug: 'users',
  // ...
}
```

### ✅ Best Practice (What to do)
```typescript
// src/collections/Users.ts (PascalCase file)
import type { CollectionConfig } from 'payload'

export const Users: CollectionConfig = { // Matches filename
  slug: 'users',
  // ...
}
```

## Explicit Type Definitions

**Context:** TypeScript types provide autocomplete and error checking for the vast Payload Config API. Without types, you might misspell properties or use invalid options.
**Directive:** ALWAYS explicitly type your collection and global configurations using `CollectionConfig` and `GlobalConfig`.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Missing type definition
export const Pages = {
  slug: 'pages',
  admin: {
    useAsTitle: 'title', // No validation if this property exists
    defaultColumns: ['title', 'slug'],
  },
  fields: [],
}
```

### ✅ Best Practice (What to do)
```typescript
import type { CollectionConfig } from 'payload'

// Explicit type ensures 'admin', 'access', etc. are valid
export const Pages: CollectionConfig = {
  slug: 'pages',
  admin: {
    useAsTitle: 'title',
    defaultColumns: ['title', 'slug', 'updatedAt'],
  },
  fields: [],
}
```

## Field Organization and Splitting

**Context:** Collection files can easily grow to thousands of lines if all fields are defined inline. This makes the code unreadable and hard to maintain.
**Directive:** ALWAYS extract complex field groups or repeated patterns into separate files or reusable field functions when a collection definition exceeds 150-200 lines.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/collections/Pages.ts
export const Pages: CollectionConfig = {
  slug: 'pages',
  fields: [
    {
      name: 'hero',
      type: 'group',
      fields: [
        // ... 50 lines of hero fields defined inline
        { name: 'title', type: 'text' },
        { name: 'image', type: 'upload', relationTo: 'media' },
        // ...
      ]
    },
    {
      name: 'content',
      type: 'blocks',
      blocks: [
        // ... 100 lines of block definitions defined inline
      ]
    }
  ]
}
```

### ✅ Best Practice (What to do)
```typescript
// src/collections/Pages.ts
import { HeroField } from '../../fields/Hero'
import { ContentBlocks } from '../../blocks/Content'

export const Pages: CollectionConfig = {
  slug: 'pages',
  fields: [
    HeroField, // Imported field definition
    {
      name: 'content',
      type: 'blocks',
      blocks: ContentBlocks, // Imported blocks
    }
  ]
}
```
