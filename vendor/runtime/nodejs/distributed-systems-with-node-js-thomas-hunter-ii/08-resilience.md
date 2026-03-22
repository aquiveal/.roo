@Domain
These rules MUST trigger when the AI is working on Node.js backend services, handling process lifecycle events, managing database connections, writing schema migrations, implementing caching mechanisms, performing network requests, or implementing error and retry logic.

@Vocabulary
- **Resilience**: The ability of an application to survive and gracefully recover from situations that might otherwise lead to failure (e.g., network drops, database crashes).
- **Graceful Shutdown**: The process of catching termination signals (e.g., SIGTERM), stopping new incoming requests, finishing existing requests, transmitting final metrics, and safely closing database connections before exiting.
- **Exception**: An error that has been thrown using the `throw` keyword, halting the current stack.
- **Rejection**: A failed Promise or an error thrown inside an `async` function.
- **Error Swallowing**: The anti-pattern of catching an error and completely disregarding the outcome without logging or handling it.
- **Single Source of Truth**: The architectural philosophy that a specific piece of data must have exactly one authoritative storage location (usually an external database), never inside an ephemeral Node.js process memory.
- **LRU Cache**: Least Recently Used cache; an in-memory data structure that limits memory consumption by automatically evicting the oldest unused items.
- **Cache Invalidation**: The methodology of determining when to update or remove entries from a cache so they do not drift from the source of truth.
- **Connection Pooling**: Maintaining a fixed number of open database connections that are reused for multiple queries, rather than opening and closing a connection per query.
- **Schema Migration**: An incremental, reversible code-based change to a database schema checked into version control.
- **Live Migration**: A multi-stage database migration that applies schema changes and backfills data without requiring application downtime.
- **Backfill**: The process of retroactively populating missing data in a newly created database column.
- **Idempotency**: The property of a network request where executing it multiple times yields the same result and side effects as executing it once (e.g., `PUT`, `DELETE`).
- **Circuit Breaker Pattern**: A strategy where a client temporarily stops making requests to a failing upstream service to prevent network flooding and allow the service to recover.
- **Exponential Backoff**: A retry strategy where the wait time between subsequent retry attempts increases exponentially (e.g., 100ms, 250ms, 500ms, 1000ms).
- **Thundering Herd**: A system failure occurring when a downed service comes back online and all clients simultaneously retry their pending requests, immediately overwhelming the service again.
- **Jitter**: A random variance applied to retry intervals or scheduled tasks (e.g., ±10%) to spread out network traffic and prevent the Thundering Herd problem.
- **Chaos Engineering**: The practice of intentionally and randomly introducing failures (crashes, latency, async drops) into a system to enforce and validate resilience.

@Objectives
- Ensure the Node.js process manages its own lifecycle safely, shutting down gracefully upon OS signals and terminating immediately upon unknown/uncaught exceptions to avoid compromised states.
- Maintain absolute process statelessness; never use the Node.js memory as the Single Source of Truth.
- Prevent memory leaks by strictly bounding any in-process data structures (e.g., using LRU algorithms based on byte size).
- Guarantee database connectivity resilience through automatic reconnections, connection pooling, and appropriate sizing limits.
- Ensure database schema updates are non-destructive and achieve zero-downtime using Live Migration strategies.
- Protect external service communication using idempotent requests, exponential backoff, jitter, and circuit breakers.

@Guidelines

### Process Lifecycle and Error Handling
- The AI MUST NOT use `process.exit()` within reusable npm packages or library code.
- The AI MUST use a status code of `0` for healthy exits and `1` through `255` for error exits when utilizing `process.exit()`.
- The AI MUST NOT swallow errors. If an error is caught, it MUST be logged, handled, or re-thrown.
- The AI MUST NOT differentiate error types by parsing the `.message` property (e.g., `e.message.startsWith(...)`). The AI MUST differentiate errors using `instanceof`, checking a `.code` property (e.g., `ERR_INVALID_URI`), or checking a `.name` property.
- The AI MUST attach a listener to `process.on('uncaughtException')` and `process.on('unhandledRejection')`. Inside these listeners, the AI MUST log the error and then synchronously execute `process.exit(1)`. The AI MUST NOT allow the process to continue running after an uncaught exception or unhandled rejection.
- The AI MUST attach an `'error'` event listener to all instantiated `EventEmitter` objects. Unhandled emitter errors crash the process with `ERR_UNHANDLED_ERROR`.
- The AI MUST implement graceful shutdown logic by listening for `SIGTERM` and `SIGINT`. Upon receiving these signals, the application MUST stop accepting new connections, finish active requests, close database connections, and then explicitly terminate.

### State and Memory Management
- The AI MUST NOT store mutable application state in global variables or unbounded objects (e.g., `const accounts = new Map()`).
- The AI MUST use a bounded algorithm, such as `lru-cache`, if in-process caching is required.
- The AI MUST configure LRU caches with a `max` size limit and calculate the `length` of items based on string/buffer byte lengths to accurately approximate memory consumption.
- The AI MUST prefix cache keys with a schema version identifier (e.g., `account-info-v2-<ID>`) whenever the underlying data structure representation changes, preventing older deployments from crashing on new data shapes.

### Database Connection Resilience
- The AI MUST implement automatic reconnection logic for standalone database clients. This logic MUST listen for `'end'` or `'error'` events, delay via `setTimeout`, and re-instantiate the connection.
- The AI MUST set an internal `kill` or `disconnect` flag when intentionally closing a database connection to prevent the automatic reconnection logic from firing.
- The AI MUST use Connection Pooling (e.g., `pg.Pool`) instead of single clients (`pg.Client`) for handling concurrent web requests to prevent serial query blocking.
- The AI MUST size database connection pools appropriately. The calculation MUST ensure that `(Pool Size * Number of Node.js Instances) < (Max Database Connections / 2)`.

### Schema Migrations
- The AI MUST generate schema migrations as timestamped files to guarantee execution order and prevent naming collisions.
- The AI MUST implement `up()` and `down()` methods for every migration, ensuring that `down()` perfectly reverses the actions of `up()` wherever possible.
- The AI MUST NEVER execute destructive up/down migrations (e.g., dropping columns with data) in production if they cause data loss.
- The AI MUST implement a 3-step "Live Migration" process for mutating active columns to avoid downtime:
  1. **Commit A**: Create the new column (nullable). Update application code to write to the new column, and read from the new column with a fallback to the old column. Deploy.
  2. **Commit B**: Create a backfill script/query to populate the new column using data from the old column. Run the backfill (chunked into smaller batches if the table is large).
  3. **Commit C**: Update application code to strictly read/write the new column. Add `NOT NULL` constraints to the new column. Drop the old column. Deploy.

### Idempotency and Networking
- The AI MUST evaluate the HTTP method before applying retry logic:
  - `GET`, `PUT`, and `DELETE` are idempotent/safe and MAY be retried.
  - `POST` and `PATCH` are destructive/non-idempotent and MUST NOT be retried automatically unless idempotency keys are used.
- The AI MUST NOT retry HTTP `4XX` errors.
- The AI MUST implement retry logic for `ECONNREFUSED` and `ENOTFOUND` errors.
- The AI MUST implement Exponential Backoff for retries (e.g., 100ms, 250ms, 500ms, 1000ms).
- The AI MUST implement Random Jitter to all exponential backoff algorithms and scheduled intervals (e.g., `setInterval`) to prevent Thundering Herd scenarios.
- The AI MUST implement the Circuit Breaker pattern for external API dependencies to fail fast when an upstream service is down.

@Workflow
1. **Analyze the Failure Boundary**: Identify whether the code interacts with the filesystem, a database, an external API, or process memory.
2. **Implement Error Trapping**: Wrap all `async` operations in `try/catch`. Attach `.on('error')` to all streams and event emitters.
3. **Configure Process Handlers**: Ensure `uncaughtException`, `unhandledRejection`, `SIGINT`, and `SIGTERM` are actively managed at the application entry point.
4. **Enforce Backoff & Jitter**: Whenever a network request or database connection is formulated, wrap it in a retry function utilizing an array-based or mathematical exponential backoff schedule multiplied by a jitter variance.
5. **Review State**: Scan the requested code for global variables. If data caching is requested, implement `lru-cache` with `length` calculations, or fall back to an external Redis/Memcached implementation.
6. **Audit Migrations**: If writing SQL migrations, explicitly split column modifications into the 3-step Live Migration pattern. Ensure `down()` migrations do not blindly drop data.

@Examples (Do's and Don'ts)

### Error Handling & Differentiation
[DON'T] Parse `.message` to determine the error type or swallow errors blindly.
```javascript
try {
  await lib.start();
} catch (e) {
  if (e.message.startsWith('Had to fallback')) {
    // silently swallow
  } else {
    throw e;
  }
}
```
[DO] Check `.code` or `instanceof` to differentiate errors.
```javascript
try {
  await lib.start();
} catch (e) {
  if (e.code === 'ERR_CONNECTION_FALLBACK' || e instanceof lib.Errors.ConnectionFallback) {
    logger.warn('Connection fallback triggered');
  } else {
    throw e;
  }
}
```

### Global Exception Handling
[DON'T] Keep the process running after an uncaught exception.
```javascript
process.on('uncaughtException', (err) => {
  console.error('Phew, caught it!', err);
  // Process continues in a potentially compromised state
});
```
[DO] Log the error and explicitly exit with status code 1.
```javascript
process.on('uncaughtException', (err) => {
  logger.send("An uncaught exception has occurred", err, () => {
    console.error(err);
    process.exit(1);
  });
});
```

### Exponential Backoff with Jitter
[DON'T] Retry immediately or use fixed intervals without variance.
```javascript
const redis = new Redis({
  retryStrategy: (times) => {
    return 1000; // Thundering herd risk
  }
});
```
[DO] Use an exponential schedule with a ±10% random jitter.
```javascript
const DEFAULT = 5000;
const SCHEDULE = [100, 250, 500, 1000, 2500];

const redis = new Redis({
  retryStrategy: (times) => {
    const time = SCHEDULE[times] || DEFAULT;
    // Calculate ±10% jitter
    return Math.random() * (time * 0.2) + time * 0.9;
  }
});
```

### In-Process Caching
[DON'T] Use unbounded Maps or Objects for caching data.
```javascript
const cache = new Map(); // Memory leak!

server.get('/account/:id', async (req) => {
  if (!cache.has(req.params.id)) {
    cache.set(req.params.id, await fetchAccount(req.params.id));
  }
  return cache.get(req.params.id);
});
```
[DO] Use a bounded LRU cache estimating byte size.
```javascript
const LRU = require('lru-cache');
const cache = new LRU({
  max: 4096, // Maximum byte size approximation
  length: (payload, key) => payload.length + key.length,
  maxAge: 10 * 60 * 1000 // 10 minutes
});

server.get('/account/:id', async (req) => {
  const id = req.params.id;
  if (!cache.has(id)) {
    const data = await fetchAccount(id);
    cache.set(id, JSON.stringify(data));
  }
  return JSON.parse(cache.get(id));
});
```

### Database Connection Resilience
[DON'T] Send multiple asynchronous queries through a single `pg.Client` without pooling.
```javascript
const { Client } = require('pg');
const db = new Client(config);
await db.connect();
// These execute serially and block the client
await Promise.all([
  db.query("SELECT pg_sleep(2);"),
  db.query("SELECT pg_sleep(2);")
]);
```
[DO] Use `pg.Pool` with an explicitly defined `max` connection limit.
```javascript
const { Pool } = require('pg');
const db = new Pool({
  ...config,
  max: process.env.MAX_CONN || 10 // Safe threshold
});
// These execute in parallel using different connections from the pool
await Promise.all([
  db.query("SELECT pg_sleep(2);"),
  db.query("SELECT pg_sleep(2);")
]);
```