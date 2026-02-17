# Payload Fields

This document defines the patterns for creating and using reusable fields in Payload CMS.

## Functional Field Definitions

**Context:** Fields often need to be reused with slight variations (e.g., a "link" field that sometimes requires a label and sometimes doesn't). Static objects don't allow for this flexibility.
**Directive:** ALWAYS export reusable fields as functions that accept an options object, enabling configuration overrides.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/fields/link.ts
import type { Field } from 'payload'

// Static object - hard to customize without mutating
export const link: Field = {
  name: 'link',
  type: 'group',
  fields: [
    { name: 'url', type: 'text' },
    { name: 'label', type: 'text' },
  ]
}

// Usage requires clumsy spreading
// ...
fields: [
  {
    ...link,
    label: 'Custom Link Label' // Might not work as expected for nested properties
  }
]
```

### ✅ Best Practice (What to do)
```typescript
// src/fields/link.ts
import type { Field } from 'payload'
import deepMerge from '../utilities/deepMerge'

type LinkType = (options?: {
  overrides?: Record<string, unknown>
  disableLabel?: boolean
}) => Field

export const link: LinkType = ({ overrides = {}, disableLabel = false } = {}) => {
  const linkResult: Field = {
    name: 'link',
    type: 'group',
    fields: [
      { name: 'url', type: 'text' },
      // Conditional logic inside the function
      ...(disableLabel ? [] : [{ name: 'label', type: 'text' }]),
    ]
  }

  // Merging overrides safely
  return deepMerge(linkResult, overrides)
}

// Usage
// ...
fields: [
  link({
    disableLabel: true,
    overrides: { name: 'externalLink' }
  })
]
```

## Deep Merging Overrides

**Context:** When overriding field properties, shallow merging (`...`) can accidentally wipe out nested configurations (like `admin` properties or sub-fields).
**Directive:** ALWAYS use a `deepMerge` utility when applying overrides to field configurations.

### ❌ Anti-Pattern (What to avoid)
```typescript
const myField = {
  name: 'title',
  admin: {
    position: 'sidebar',
    description: 'Main title'
  }
}

// Overriding 'admin' wipes out 'position' and 'description' if not careful
const newField = {
  ...myField,
  admin: {
    hidden: true
  }
}
// Result: admin is now just { hidden: true }
```

### ✅ Best Practice (What to do)
```typescript
import deepMerge from '../utilities/deepMerge'

const myField = {
  name: 'title',
  admin: {
    position: 'sidebar',
    description: 'Main title'
  }
}

// Deep merge preserves existing nested properties
const newField = deepMerge(myField, {
  admin: {
    hidden: true
  }
})
// Result: admin is { position: 'sidebar', description: 'Main title', hidden: true }
```
