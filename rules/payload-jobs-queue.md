# Hatchet Workflows and Queues

This document defines the rules for implementing background jobs and workflows using Hatchet in this project.

## Structured Workflow Definitions

**Context:** Hatchet workflows can become complex. Organizing them into a dedicated directory structure ensures that workers can easily discover them and developers can find business logic.
**Directive:** ALWAYS place Hatchet workflow definitions in `src/hatchet/workflows/` and export the workflow definition object/class.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/app/api/trigger/route.ts
// Defining the workflow inline or in random utility files
const myWorkflow = {
  id: 'my-workflow',
  steps: [
    {
      name: 'step1',
      run: async () => { /* logic */ }
    }
  ]
}
```

### ✅ Best Practice (What to do)
```typescript
// src/hatchet/workflows/onboarding.ts
import { Workflow } from '@hatchet-dev/typescript-sdk'

// Define Input Type for type safety
interface OnboardingInput {
  userId: string
  email: string
}

export const onboardingWorkflow: Workflow = {
  id: 'user-onboarding',
  description: 'Onboards a new user',
  on: {
    event: 'user:created',
  },
  steps: [
    {
      name: 'send-email',
      timeout: '60s', // Best practice: explicit timeouts
      retries: 3,     // Best practice: explicit retries
      run: async (ctx) => {
        // Type-safe input retrieval
        const { userId, email } = ctx.workflowInput<OnboardingInput>()

        await sendEmail(email)

        return { sent: true, userId }
      },
    },
  ],
}
```

## Centralized Hatchet Client

**Context:** Instantiating the Hatchet client in multiple places can lead to connection issues and configuration drift. A singleton instance ensures consistent configuration.
**Directive:** ALWAYS use a shared Hatchet client instance exported from `src/hatchet/client.ts`.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Instantiating client everywhere
import { Hatchet } from '@hatchet-dev/typescript-sdk'

export const trigger = async () => {
  const hatchet = Hatchet.init() // Re-initializing on every call
  await hatchet.admin.run_workflow(...)
}
```

### ✅ Best Practice (What to do)
```typescript
// src/hatchet/client.ts
import { Hatchet } from '@hatchet-dev/typescript-sdk'

export const hatchet = Hatchet.init({
  // Configuration via environment variables is preferred
  // HATCHET_CLIENT_TOKEN, HATCHET_CLIENT_TLS_STRATEGY, etc.
})

// src/utilities/triggerWorkflow.ts
import { hatchet } from '../hatchet/client'

export const triggerWorkflow = async () => {
  // Use the singleton instance
  await hatchet.admin.run_workflow('user-onboarding', {
    userId: '123',
    email: 'test@example.com'
  })
}
```

## Triggering from Collection Hooks

**Context:** The most common use case is triggering a background job when data changes in Payload.
**Directive:** Trigger workflows inside `afterChange` or `afterDelete` hooks using the shared Hatchet client.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Using beforeChange for async side effects
hooks: {
  beforeChange: [
    async ({ data }) => {
      // Slows down the request!
      await hatchet.admin.run_workflow(...)
      return data
    }
  ]
}
```

### ✅ Best Practice (What to do)
```typescript
// src/collections/Users.ts
import { hatchet } from '../hatchet/client'

export const Users: CollectionConfig = {
  slug: 'users',
  hooks: {
    afterChange: [
      async ({ doc, operation }) => {
        if (operation === 'create') {
          // Trigger background job without blocking
          await hatchet.admin.run_workflow('user-onboarding', {
            userId: doc.id,
            email: doc.email,
          })
        }
      }
    ]
  }
}
```

## Using Utilities and Local API in Steps

**Context:** Background workers often need to interact with the database or reuse business logic defined in the main application.
**Directive:** Import `getPayload` and your shared utilities directly into the workflow step files. The worker environment must have access to the database.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Duplicating logic inside the step
run: async (ctx) => {
  // Re-implementing logic that already exists in src/utilities
  const db = await connectToDb() // Manual DB connection
  await db.update(...)
}
```

### ✅ Best Practice (What to do)
```typescript
// src/hatchet/workflows/syncUser.ts
import { getPayload } from 'payload'
import configPromise from '../../payload.config'
import { formatName } from '../../utilities/formatName' // Reusing utility

export const syncUserWorkflow: Workflow = {
  id: 'sync-user',
  steps: [
    {
      name: 'update-profile',
      run: async (ctx) => {
        const { userId, firstName, lastName } = ctx.workflowInput()

        // 1. Reuse Utility
        const fullName = formatName(firstName, lastName)

        // 2. Use Local API
        const payload = await getPayload({ config: configPromise })

        await payload.update({
          collection: 'users',
          id: userId,
          data: { name: fullName }
        })

        return { success: true }
      }
    }
  ]
}
```

## Worker Entry Point

**Context:** The worker process needs to register all workflows. If workflows are scattered or not manually registered, the worker won't pick them up.
**Directive:** ALWAYS maintain a dedicated `src/hatchet/worker.ts` entry point that registers all workflows from `src/hatchet/workflows/`.

### ❌ Anti-Pattern (What to avoid)
```typescript
// Running workers implicitly or without a clear entry file
// package.json: "start-worker": "ts-node some-random-script.ts"
```

### ✅ Best Practice (What to do)
```typescript
// src/hatchet/worker.ts
import { hatchet } from './client'
import { onboardingWorkflow } from './workflows/onboarding'
import { syncUserWorkflow } from './workflows/syncUser'

async function start() {
  const worker = await hatchet.worker('payload-worker')

  // Explicit registration
  await worker.registerWorkflow(onboardingWorkflow)
  await worker.registerWorkflow(syncUserWorkflow)

  worker.start()
}

start()
```
