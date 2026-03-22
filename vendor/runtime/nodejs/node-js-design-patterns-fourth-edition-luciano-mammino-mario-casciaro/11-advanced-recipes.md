# @Domain

Advanced Node.js asynchronous programming tasks, including asynchronous component initialization, high-load API request handling (batching and caching), execution of cancelable asynchronous flows, and processing of CPU-intensive (CPU-bound) computations. 

# @Vocabulary

- **Pre-initialization Queue:** A pattern that combines a queue with the Command pattern to temporarily store method invocations while an asynchronous component is initializing, executing them automatically once the component is ready.
- **Promise Piggybacking:** The practice of attaching multiple `.then()` handlers to a single, already-pending Promise to share the result of an ongoing asynchronous operation among identical concurrent requests.
- **Asynchronous Request Batching:** Grouping concurrent identical requests so they share a single underlying asynchronous operation, preventing duplicated work.
- **Zalgo:** An anti-pattern describing an API that inconsistently returns values either synchronously or asynchronously.
- **AbortController / AbortSignal:** Standard JavaScript APIs used to signal and respond to cancellation requests in asynchronous workflows.
- **CPU-bound Task:** A computationally expensive, synchronous algorithm that consumes high CPU cycles and blocks the Node.js event loop.
- **Interleaving:** Yielding control of the CPU back to the event loop during a long-running synchronous algorithm to process pending I/O, achieved using `setImmediate()`.
- **Worker Threads / Child Processes:** Mechanisms to offload CPU-bound tasks into isolated Node.js environments (`node:worker_threads` and `node:child_process`) to preserve the responsiveness of the main event loop.
- **Process/Thread Pool:** A stateful manager that limits, acquires, and releases instances of child processes or worker threads to prevent resource exhaustion and denial-of-service (DoS) vulnerabilities.

# @Objectives

- Ensure components with asynchronous initialization phases can be consumed transparently without forcing consumers to perform manual connection checks or delay application startup.
- Optimize API endpoints by implementing asynchronous request batching and caching to eliminate redundant backend/database operations.
- Enforce standard interoperability for task cancellation using native `AbortController` and `AbortSignal` interfaces.
- Protect the main event loop from being blocked by CPU-intensive algorithms using interleaving or dedicated worker pools.

# @Guidelines

### Asynchronously Initialized Components
- You MUST NOT burden the consumer with checking the initialization state (Local Initialization Check) before invoking component APIs.
- You SHOULD NOT use the Delayed Startup pattern (delaying application execution until all services initialize) if it severely impacts startup time or fails to handle reconnect/re-initialization scenarios.
- You MUST implement **Pre-initialization Queues** to transparently queue operations if the component is not yet connected.
- When using Pre-initialization Queues, you MUST wrap requested operations in Promises, push them to an internal queue array, and process the array sequentially once the connection establishes.
- For maximum modularity, you MUST utilize the **State Pattern** to toggle the component between a `QueuingState` (queues requests) and an `InitializedState` (executes logic directly).

### Asynchronous Request Batching and Caching
- You MUST implement **Asynchronous Request Batching** for high-load, slow APIs to prevent identical concurrent requests from triggering duplicate processing.
- To batch requests, you MUST maintain a `Map` of currently running operations, keyed by the request parameters.
- If a request arrives and its key exists in the `Map`, you MUST return the existing Promise (Promise Piggybacking) instead of creating a new one.
- You MUST remove the Promise from the `Map` in a `.finally()` block when the operation completes, unless you are combining batching with caching.
- When adding caching, you MUST leave the Promise in the `Map` after completion and use `setTimeout` to implement a Time To Live (TTL) cache invalidation strategy.
- You MUST ALWAYS return cached values asynchronously (inherent when returning a Promise) to avoid the Zalgo anti-pattern.

### Canceling Asynchronous Operations
- You MUST use the standard `AbortController` and `AbortSignal` APIs for canceling asynchronous operations to ensure interoperability with third-party code.
- You MUST pass the `signal` property of an `AbortController` instance to the target asynchronous function.
- Inside the cancelable function, you MUST explicitly invoke `signal.throwIfAborted()` after every `await` boundary to yield control and check for cancellation.
- You MUST handle the thrown `AbortError` gracefully in the calling context's `try...catch` block.
- You MUST NOT use custom object flags (e.g., `cancelObj.cancelRequested`) or custom wrapper factories for cancellation.

### Running CPU-Bound Tasks
- You MUST NOT execute long-running, synchronous `while` or `for` loops in the main thread, as this blocks the event loop and exposes the application to DoS attacks.
- For moderate CPU-bound tasks, you MUST implement **Interleaving** by wrapping steps or batches of steps in `setImmediate()`.
- You MUST NOT use `process.nextTick()` for interleaving, as it runs before pending I/O and will cause I/O starvation.
- For heavy CPU-bound tasks, you MUST offload computation using `node:child_process` (via `fork()`) or `node:worker_threads` (via `Worker`).
- When offloading tasks, you MUST implement a **Pool** pattern (`ProcessPool` or `ThreadPool`) to enforce a maximum concurrency limit (`poolMax`) to prevent resource exhaustion.
- For production-grade thread/process management, you SHOULD prefer established libraries like `workerpool` or `piscina` over manual pool implementations.

# @Workflow

When dealing with advanced asynchronous or intensive operations, strictly follow this evaluation logic:

1.  **Component Lifecycle Check**: Does the component require a network handshake or async setup before use?
    *   *Yes*: Abstract the state. Create a `QueuingState` class that pushes operations to a command array. Transition to an `InitializedState` when ready, and flush the queue.
2.  **API Load Optimization**: Is the async function frequently queried with identical parameters?
    *   *Yes*: Create a `Map`. Use the query parameter as the key. Store the execution Promise. Return the stored Promise for subsequent identical calls. Delete from the `Map` on `.finally()`. For caching, set a TTL instead of deleting immediately.
3.  **Cancellation Requirements**: Does the async flow take significant time or require manual abortion?
    *   *Yes*: Accept an `AbortSignal` parameter. Place `signal.throwIfAborted()` after every `await` resumption point.
4.  **CPU Load Assessment**: Does the algorithm execute synchronously for longer than a few milliseconds (O(2ⁿ) complexity, heavy parsing, cryptography)?
    *   *Yes, but lightweight*: Chunk the array/data and schedule the next chunk using `setImmediate()`.
    *   *Yes, and heavy*: Create a separate worker file. Use `node:worker_threads`. Communicate via `parentPort.postMessage`. Wrap the worker instantiation in a `ThreadPool` with an `.acquire()` and `.release()` lifecycle.

# @Examples (Do's and Don'ts)

### Asynchronously Initialized Components

**[DON'T]** Force the consumer to check state or use delayed startup haphazardly.
```javascript
// Consumer code burdened with state checking
import { db } from './db.js'

async function getUsers() {
  if (!db.connected) {
    await db.connect()
  }
  return await db.query('SELECT * FROM users')
}
```

**[DO]** Implement a Pre-initialization Queue transparently inside the component.
```javascript
class Database {
  constructor() {
    this.connected = false;
    this.commandsQueue = [];
  }
  
  async query(queryString) {
    if (!this.connected) {
      return new Promise((resolve, reject) => {
        this.commandsQueue.push(() => {
          this.query(queryString).then(resolve, reject);
        });
      });
    }
    // Execute query immediately if connected
    return await executeRealQuery(queryString);
  }

  async connect() {
    // ... establish connection ...
    this.connected = true;
    while (this.commandsQueue.length > 0) {
      const command = this.commandsQueue.shift();
      command();
    }
  }
}
```

### Asynchronous Request Batching

**[DON'T]** Execute duplicate asynchronous requests concurrently.
```javascript
export function totalSales(product) {
  // Triggers heavy DB query for EVERY call, even if identical request is pending
  return totalSalesRaw(product); 
}
```

**[DO]** Piggyback on the pending Promise using a Map.
```javascript
const runningRequests = new Map();

export function totalSales(product) {
  if (runningRequests.has(product)) {
    return runningRequests.get(product);
  }
  
  const resultPromise = totalSalesRaw(product);
  runningRequests.set(product, resultPromise);
  
  resultPromise.finally(() => {
    runningRequests.delete(product);
  });
  
  return resultPromise;
}
```

### Canceling Asynchronous Operations

**[DON'T]** Use custom boolean flags or proprietary wrapper factories for cancellation.
```javascript
async function cancelable(cancelObj) {
  await asyncRoutine('A');
  if (cancelObj.cancelRequested) throw new Error('Canceled'); // Anti-pattern
}
```

**[DO]** Use standard `AbortController` and `AbortSignal`.
```javascript
async function cancelable(abortSignal) {
  abortSignal.throwIfAborted();
  const resA = await asyncRoutine('A');
  
  abortSignal.throwIfAborted();
  const resB = await asyncRoutine('B');
}

// Consumer usage
const ac = new AbortController();
setTimeout(() => ac.abort(), 100);
try {
  await cancelable(ac.signal);
} catch (err) {
  if (err.name === 'AbortError') console.log('Canceled');
}
```

### Running CPU-Bound Tasks

**[DON'T]** Block the event loop with heavy synchronous processing or `process.nextTick()`.
```javascript
function processHeavyTask(data) {
  for (let i = 0; i < data.length; i++) {
    // Heavy synchronous math blocking the event loop
    compute(data[i]); 
  }
}
```

**[DO]** Interleave processing using `setImmediate` or offload to `worker_threads` via a Pool.
```javascript
// Lightweight interleaving
function processInterleaved(data, index = 0) {
  compute(data[index]);
  if (index + 1 < data.length) {
    setImmediate(() => processInterleaved(data, index + 1));
  }
}

// Heavy task offloading (Conceptual usage of worker threads)
import { Worker } from 'node:worker_threads';

class ThreadPool {
  constructor(file, poolMax) {
    this.file = file;
    this.poolMax = poolMax;
    this.active = [];
    this.pool = [];
    this.waiting = [];
  }

  acquire() {
    return new Promise((resolve, reject) => {
      if (this.pool.length > 0) {
        const worker = this.pool.pop();
        this.active.push(worker);
        return resolve(worker);
      }
      if (this.active.length >= this.poolMax) {
        return this.waiting.push({ resolve, reject });
      }
      const worker = new Worker(this.file);
      worker.once('online', () => {
        this.active.push(worker);
        resolve(worker);
      });
    });
  }
  
  release(worker) {
    if (this.waiting.length > 0) {
      const { resolve } = this.waiting.shift();
      return resolve(worker);
    }
    this.active = this.active.filter(w => w !== worker);
    this.pool.push(worker);
  }
}
```