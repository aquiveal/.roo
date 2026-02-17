# Payload Custom Endpoints and Workflows

This document defines how to implement custom endpoints and server-side workflows in Payload CMS (Next.js App Router).

## Standard Route Handler Pattern

**Context:** Custom endpoints in Next.js App Router are powerful but need structure. Mixing auth, validation, and logic makes them hard to read and insecure.
**Directive:** ALWAYS follow the pattern: Authentication -> Validation -> Execution -> Response.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/app/(payload)/api/sync/route.ts
export const POST = async (req: Request) => {
  // No auth check!
  const body = await req.json()

  // Logic mixed with handler
  if (body.action === 'start') {
     // ... complex logic ...
  }

  return Response.json({ success: true })
}
```

### ✅ Best Practice (What to do)
```typescript
// src/app/(payload)/api/sync/route.ts
import { getPayload } from 'payload'
import configPromise from '@payload-config'
import { NextResponse } from 'next/server'

export const POST = async (req: Request) => {
  const payload = await getPayload({ config: configPromise })

  // 1. Authentication
  const { user } = await payload.auth(req)
  if (!user || !user.roles.includes('admin')) {
    return new Response('Unauthorized', { status: 401 })
  }

  // 2. Validation (e.g., check body exists)
  const body = await req.json()
  if (!body.sourceId) {
    return NextResponse.json({ error: 'Missing sourceId' }, { status: 400 })
  }

  // 3. Execution (Delegate to service)
  try {
    await runSync(payload, body.sourceId)
    return NextResponse.json({ success: true })
  } catch (err) {
    return NextResponse.json({ error: 'Failed' }, { status: 500 })
  }
}
```

## Service Layer Extraction

**Context:** Putting all business logic inside the route handler makes it impossible to reuse that logic (e.g., from a Cron job or CLI script) and hard to unit test.
**Directive:** ALWAYS extract complex business logic into a "Service" function in `src/utilities/` or a domain folder, and call it from the route handler.

### ❌ Anti-Pattern (What to avoid)
```typescript
// src/app/api/process-order/route.ts
export const POST = async (req) => {
  // ... auth ...

  // 100 lines of order processing logic right here
  // Cannot be called from anywhere else!
  const order = await payload.create({ ... })
  await stripe.charges.create({ ... })
  await sendEmail({ ... })

  return Response.json({ ok: true })
}
```

### ✅ Best Practice (What to do)
```typescript
// src/utilities/orderService.ts
export const processOrder = async (payload: Payload, data: OrderData) => {
  const order = await payload.create({ ... })
  // ... reusable logic
  return order
}

// src/app/api/process-order/route.ts
import { processOrder } from '../../../utilities/orderService'

export const POST = async (req) => {
  // ... auth & validation ...
  const result = await processOrder(payload, req.json())
  return Response.json(result)
}
```
