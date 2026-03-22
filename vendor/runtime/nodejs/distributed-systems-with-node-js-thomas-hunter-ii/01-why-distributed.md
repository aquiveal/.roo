# @Domain

These rules MUST be activated when the AI is tasked with architecting, generating, refactoring, or debugging Node.js backend services, specifically when dealing with asynchronous logic, event loop management, concurrency, cross-process communication, or distributed system design (e.g., breaking monolithic apps into producer/consumer services).

# @Vocabulary

- **Call Stack**: A stack of currently running functions. JavaScript executes within a single call stack at a time per isolate.
- **Event Loop**: An infinitely running loop that continuously checks for and executes queued asynchronous work whenever the current call stack completes.
- **Message Passing**: The mechanism of sharing serialized representations of objects/data (e.g., JSON) between separate JavaScript isolates to avoid deadlocks and race conditions.
- **Continuation-Passing Style (CPS)**: A programming pattern utilized extensively in Node.js internal modules where functions are passed around (as callbacks) and invoked by the event loop once a task completes.
- **libuv**: A C++ library underlying Node.js that handles operating system abstractions, I/O operations, and maintains a thread pool for long-running tasks.
- **Userland**: The space outside of the Node.js kernel where user applications and npm packages run.
- **Poll Phase**: The event loop phase that executes I/O-related callbacks. Main application code starts here.
- **Check Phase**: The event loop phase where callbacks triggered via `setImmediate()` are executed.
- **Close Phase**: The event loop phase where callbacks triggered via `EventEmitter` close events are executed.
- **Timers Phase**: The event loop phase where callbacks scheduled via `setTimeout()` and `setInterval()` are executed.
- **Pending Phase**: The event loop phase where special system events (e.g., TCP socket `ECONNREFUSED` errors) are executed.
- **Microtask Queue**: High-priority queues consulted after the current phase completes. Contains the Next Tick queue (`process.nextTick()`) and the Promise queue.
- **Zalgo**: An anti-pattern where a function taking a callback executes that callback synchronously under some conditions and asynchronously under others.
- **Producer / Upstream**: A backend service that provides data or internal APIs, typically not accessed directly by the outside world.
- **Consumer / Downstream**: A public-facing API or service that makes outbound requests to Producer services.

# @Objectives

- Enforce strictly non-blocking architectures to maximize single-threaded CPU efficiency.
- Guarantee predictable asynchronous execution and eliminate the "Zalgo" anti-pattern in callback APIs.
- Explicitly manage the Node.js process lifecycle by controlling asynchronous handles (`.ref()` / `.unref()`).
- Facilitate scalable distributed designs by strictly separating producer and consumer responsibilities and sharing state only via explicit message passing or shared memory.
- Master the precise execution order of the Node.js event loop phases and microtask queues.

# @Guidelines

### Event Loop and Call Stack Constraints
- The AI MUST NOT write recursive synchronous functions that risk exceeding the V8 engine's maximum call stack size (~15,000 frames).
- The AI MUST NOT treat the `time` argument in `setTimeout()` as an exact execution time. It MUST be treated as the *earliest possible time* the callback can be executed, recognizing that running stacks and event loop polling take non-zero time.
- The AI MUST break up CPU-heavy operations (e.g., processing large datasets) across multiple call stacks to prevent event loop starvation. 

### Microtask and Phase Management
- The AI MUST use `setImmediate()` to yield the event loop and process batches of heavy CPU operations. `setImmediate()` correctly adds callbacks to the *next* iteration's check phase queue.
- The AI MUST NOT use `process.nextTick()` to break up heavy CPU work or create recursive loops. Doing so creates a microtask queue that never empties, trapping the application in the current phase forever (creating a zombie process).
- The AI MUST accurately sequence async logic knowing the strict priority: `process.nextTick()` callbacks run first, followed by Promise resolutions, followed by the current Event Loop Phase (Poll -> Check -> Close -> Timers -> Pending).
- The AI MUST treat `async`/`await` operations as syntactic sugar for nested callbacks/Promises, applying the exact same event loop resolution rules to `await` statements.

### Threading and I/O
- The AI MUST leverage the fact that Node.js is multithreaded at the C++ layer (libuv). Network, filesystem, and CPU-heavy tasks (like `crypto` or `zlib`) MUST be executed asynchronously to allow parallel processing in the libuv thread pool.
- The AI MUST account for the libuv thread pool constraints. The default pool size is 4 (maximum 1,024). The AI MUST modify `UV_THREADPOOL_SIZE` only if strictly necessary and after benchmarking.
- When concurrent execution is required at the application level, the AI MUST use `cluster`, `worker_threads`, or `child_process`.
- The AI MUST NOT attempt to share standard object references directly across isolates. State MUST be shared using Message Passing (serialization/deserialization) or explicitly via `SharedArrayBuffer` using `worker_threads`.

### Process Lifecycle
- The AI MUST track asynchronous tasks, as pending async tasks keep the Node.js process alive.
- If an object/timer (e.g., a long-running background `setTimeout` or an HTTP server) should NOT keep the process alive, the AI MUST call the `.unref()` method on that object.
- To reverse an `.unref()` call, the AI MUST use the `.ref()` method.

### Anti-Patterns
- **Do Not Introduce Zalgo**: If a function exposes a callback interface, the AI MUST ensure the callback is executed asynchronously in *all* logical branches, using `process.nextTick()` or `setImmediate()` to wrap synchronous returns.
- **Do Not Block the Event Loop**: The AI MUST NOT use synchronous `fs` methods or heavy synchronous `while`/`for` loops in the main thread of a server application responding to network requests.

### Distributed Architecture Basics
- The AI MUST separate architectures into Consumer (public-facing, downstream) and Producer (internal, upstream) services.
- The AI MUST include the process ID (`process.pid`) in distributed response payloads to explicitly track and trace which specific isolated process served the request.

# @Workflow

When designing or refactoring a highly concurrent or distributed Node.js function/service, the AI MUST adhere to the following algorithm:

1. **Analyze Execution Context**: Determine if the task is CPU-bound or I/O-bound.
2. **Offload I/O**: If I/O-bound, utilize standard asynchronous Node.js APIs to push work to the libuv thread pool.
3. **Chunk CPU Work**: If CPU-bound, chunk the dataset. Execute the first chunk synchronously, then schedule the next chunk using `setImmediate()`.
4. **Ensure Asynchronous Consistency**: Check all return paths of the function. If it accepts a callback, ensure every single branch (including fast-fail error branches) executes the callback asynchronously.
5. **Manage Process Lifecycle**: Evaluate if the background task should prevent the Node process from exiting. If no, apply `.unref()`.
6. **Structure for Scale**: If building an API, determine if it is a Producer (connects to DB, handles business logic) or a Consumer (handles internet traffic, aggregates Producers). Expose the `process.pid` in the JSON response for debugging scaling infrastructure.

# @Examples (Do's and Don'ts)

### Zalgo (Inconsistent Asynchrony)
**[DON'T]** Execute a callback synchronously in an error branch and asynchronously in a success branch.
```javascript
// Antipattern: Introduces Zalgo
function fetchUser(id, callback) {
  if (id <= 0) {
    // Runs synchronously!
    return callback(new TypeError('id must be > 0'));
  }
  // Runs asynchronously!
  db.query('SELECT * FROM users WHERE id = ?', [id], callback);
}
```

**[DO]** Wrap synchronous fast-paths in `process.nextTick` or `setImmediate` to ensure predictable stack unwinding.
```javascript
// Correct: Always asynchronous
function fetchUser(id, callback) {
  if (id <= 0) {
    // Runs asynchronously!
    return process.nextTick(() => callback(new TypeError('id must be > 0')));
  }
  // Runs asynchronously!
  db.query('SELECT * FROM users WHERE id = ?', [id], callback);
}
```

### Event Loop Starvation
**[DON'T]** Use `process.nextTick` for recursive looping or chunking, as it will starve the Poll and Timers phases.
```javascript
// Antipattern: Creates an infinite microtask loop
const nt_recursive = () => process.nextTick(nt_recursive);
nt_recursive(); 
// ANY setTimeout or incoming HTTP request will NEVER execute.
```

**[DO]** Use `setImmediate` to queue heavy background work into the Check phase, allowing the Event Loop to process I/O and timers in between.
```javascript
// Correct: Yields the event loop
const si_recursive = () => setImmediate(si_recursive);
si_recursive(); 
// I/O and timers will continue to function normally.
setInterval(() => console.log('I will run!'), 10);
```

### Process Lifecycle Management
**[DON'T]** Allow background maintenance intervals to permanently block process termination.
```javascript
// Antipattern: Process will never exit naturally
setInterval(() => {
  cleanupTempFiles();
}, 60000);
```

**[DO]** Use `.unref()` on timers that perform background tasks.
```javascript
// Correct: Process can exit gracefully when main work is done
const cleanupTimer = setInterval(() => {
  cleanupTempFiles();
}, 60000);

cleanupTimer.unref();
```