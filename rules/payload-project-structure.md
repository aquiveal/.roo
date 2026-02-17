# Payload Project Structure and Organization

This document defines the standard directory structure and file organization for Payload CMS projects.

## Standard Directory Structure

**Context:** A consistent directory structure ensures that any developer can easily navigate the project, locate files, and understand the project's organization. It separates concerns like business logic, configuration, and presentation.
**Directive:** ALWAYS follow the defined `src` directory structure for all source code.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Putting everything in the root or mixing concerns
/src
  /my-components
  /utils
  payload.config.ts
  Users.ts // Collection definition at root
  helpers.js // Mixed JS/TS
  server.ts
```

### ✅ Best Practice (What to do)
```typescript
// src directory organization
src/
├── access/         # Global access control functions (e.g., isAdmin.ts)
├── app/            # Next.js App Router files (pages, layouts, API routes)
├── collections/    # Collection definitions (e.g., Users.ts, Pages/index.ts)
├── components/     # Custom React components (e.g., CustomDashboard.tsx)
├── fields/         # Reusable field definitions (e.g., link.ts, richText.ts)
├── globals/        # Global config definitions (e.g., MainMenu.ts)
├── hooks/          # Shared hooks (e.g., formatSlug.ts)
├── hatchet/        # Hatchet workflows and worker configuration
│   ├── workflows/  # Workflow definitions (e.g., onboarding.ts)
│   ├── client.ts   # Shared Hatchet client instance
│   └── worker.ts   # Worker entry point
├── migrations/     # Database migrations and seed scripts
├── utilities/      # Helper functions (e.g., extractID.ts)
└── payload.config.ts # Main Payload configuration
```

## Clean Configuration File

**Context:** The `payload.config.ts` file is the central nervous system of the application. Cluttering it with inline definitions makes it hard to read and maintain, and prevents code splitting/reuse.
**Directive:** NEVER define collections, globals, or complex logic inline within `payload.config.ts`; ALWAYS import them from their respective files.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/payload.config.ts
import { buildConfig } from 'payload'

export default buildConfig({
  // Inline collection definition - Hard to read and maintain
  collections: [
    {
      slug: 'users',
      fields: [
        {
          name: 'email',
          type: 'email',
        }
      ],
      hooks: {
        beforeChange: [
           // Inline hook logic - untestable and messy
          ({ data }) => {
            if (data.email) {
              return { ...data, email: data.email.toLowerCase() }
            }
            return data
          }
        ]
      }
    }
  ],
})
```

### ✅ Best Practice (What to do)
```typescript
// src/payload.config.ts
import { buildConfig } from 'payload'
import { Users } from './collections/Users'
import { Pages } from './collections/Pages'
import { MainMenu } from './globals/MainMenu'

export default buildConfig({
  // Clean, imported definitions
  collections: [Users, Pages],
  globals: [MainMenu],
  // ... other config
})
```

## Modular Collection Definitions

**Context:** Complex collections often require specific hooks, access control, and custom components. Keeping everything in a single file leads to massive, unreadable files.
**Directive:** ALWAYS use a directory structure for complex collections to separate config, access, and hooks.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/collections/Pages.ts
// A single file containing config, access logic, and hook logic
export const Pages = {
  slug: 'pages',
  access: {
    // Inline access logic
    read: ({ req: { user } }) => Boolean(user),
  },
  hooks: {
    // Inline hook logic
    beforeChange: [({ data }) => { /* 50 lines of code */ }]
  },
  fields: [ /* 100 lines of fields */ ]
}
```

### ✅ Best Practice (What to do)
```typescript
// src/collections/Pages/index.ts
import { loggedIn } from './access/loggedIn'
import { formatSlug } from './hooks/formatSlug'

export const Pages: CollectionConfig = {
  slug: 'pages',
  access: {
    read: loggedIn, // Imported access control
  },
  hooks: {
    beforeChange: [formatSlug('title')], // Imported hook
  },
  fields: [
    // ... fields
  ],
}
```
