@Domain
This rule file is triggered when the AI is tasked with writing, refactoring, or analyzing asynchronous Node.js code. This includes managing concurrency, configuring the event loop, handling I/O operations, writing network or filesystem event listeners, managing timers, handling Node.js errors and exceptions, and implementing flow control utilizing callbacks, Promises, async/await, or Generators.

@Vocabulary
- **Event-Driven Programming**: A paradigm where the flow of the program is determined by events, executed via a main loop divided into event selection and event handling.
- **Event Loop**: A single-threaded execution manager that performs non-blocking I/O operations by offloading tasks to the system kernel (via libuv) and synchronizing results through queued callbacks.
- **Tick**: A single processing cycle of the event loop's instruction queue.
- **libuv**: The C library underlying Node.js that creates and manages the event loop, utilizing OS-level thread pools to execute blocking I/O tasks asynchronously.
- **process.nextTick**: A deferred execution mechanism that places callbacks at the head of the event queue, executing them *before* any I/O or timer events on the next tick.
- **setImmediate**: A deferred execution mechanism that places callbacks in the poll/check phase, executing them *after* pending I/O events.
- **Inter-Process Communication (IPC)**: A mechanism for passing messages between different OS processes, commonly utilizing `child.send()` and `process.on('message')` in Node.js.
- **POSIX Signals**: Standard OS-level asynchronous notifications sent to a process (e.g., `SIGINT`, `SIGUSR1`).
- **Error**: A non-fatal condition in a Node program that should be caught and handled (e.g., bad call signature, failed I/O).
- **Exception**: A fatal, unexpected system error that destabilizes the application, requiring graceful shutdown.
- **Server Sent Events (SSE)**: A unidirectional protocol for broadcasting data from a server to connected clients via an open HTTP connection.

@Objectives
- Maximize system resource utilization by ensuring no I/O operation blocks the single-threaded V8 event loop.
- Guarantee predictable callback execution order by meticulously choosing between synchronous execution, `process.nextTick`, `setImmediate`, and standard timers.
- Prevent memory leaks and infinite loop deadlocks caused by recursive deferred execution or unreferenced timers.
- Maintain application stability by strictly separating the handling of non-fatal errors from fatal exceptions.
- Produce highly readable, maintainable, "shallow" asynchronous code utilizing modern flow control (async/await, Promises) and named functions.

@Guidelines

### Event Loop and Deferred Execution
- The AI MUST NOT write code that blocks the event loop (e.g., infinite synchronous `while` loops waiting for asynchronous variable changes).
- The AI MUST use `process.nextTick()` when it is necessary to postpone the broadcast of events until the current execution stack completes, allowing the caller time to register event listeners.
- The AI MUST NOT use recursive `process.nextTick()` calls, as this starves the event loop of I/O processing.
- The AI MUST use `setImmediate()` to defer execution if the callback must execute *after* I/O events have been processed.

### Timers and Polling
- The AI MUST NOT assume exact millisecond precision for `setTimeout` or `setInterval`. Timers guarantee minimum execution delay, subject to event loop scheduling.
- The AI MUST call `timer.unref()` on background timers (like long-running polling loops) if that timer is the only event source keeping the Node process alive and the process should otherwise exit.
- The AI MUST explicitly clear timers (`clearTimeout`, `clearInterval`, `clearImmediate`) when their execution is no longer required or when a related external event source stops.

### Callbacks and Concurrency
- The AI MUST strictly follow the Node.js callback convention: the callback MUST be the last argument in the function signature, and the first argument passed to the callback MUST be an Error object (or `null` if successful).
- The AI MUST name callback functions instead of using anonymous functions. Named functions ensure distinct and readable stack traces during debugging.
- The AI MUST favor shallow code over deeply nested callbacks (The Pyramid of Doom). Refactor deep nesting using Promises or `async/await`.

### Promises, Async/Await, and Generators
- The AI MUST always reject Promises with true `Error` objects, never plain strings.
- The AI MUST provide a `.catch()` block for Promise chains to prevent unhandled rejections.
- The AI MUST use `Promise.all()` to trigger and manage multiple asynchronous, independent I/O calls in parallel rather than executing them serially.
- The AI MUST use `try...catch` blocks within `async` functions to capture errors from `await` expressions, as this natively captures both synchronous and asynchronous errors within the block.
- The AI MUST utilize Generators (`function*` and `yield`) when managing a sequence of future values or state transitions over time, treating iteration as capturing transition events.

### Processes and IPC
- The AI MUST listen for POSIX signals (e.g., `process.on('SIGINT')`, `process.on('SIGUSR1')`) when implementing graceful shutdown or custom command-line Inter-Process Communication.
- When parallelizing execution, the AI MUST spawn or fork child processes to distribute work across available CPU cores.
- The AI MUST use `child_process.fork()` when creating Node.js child processes to automatically establish an IPC channel, utilizing `child.send()` and `child.on('message')` for communication.

### Error and Exception Handling
- The AI MUST treat expected operational failures (e.g., file not found, bad inputs) as Errors and handle them via callback `err` parameters, event emitter `error` events, or Promise `catch` handlers.
- The AI MUST treat unexpected runtime failures as Exceptions.
- The AI MUST implement `process.on('uncaughtException')` and `process.on('unhandledRejection')` handlers.
- The AI MUST gracefully shut down and restart the Node process upon catching an `uncaughtException`; the AI MUST NOT attempt to continue execution, as the system is in an indeterminate state.
- When an `EventEmitter` instance experiences an error, the AI MUST emit an `error` event. 

### Server Sent Events (SSE)
- When implementing unidirectional, passive data broadcasts from server to client, the AI MUST use Server Sent Events over WebSockets or AJAX long-polling.
- The AI MUST set the HTTP response headers `Content-Type: text/event-stream`, `Cache-Control: no-cache`, and `Connection: keep-alive` when establishing an SSE connection.

@Workflow
When implementing asynchronous logic or I/O operations, the AI MUST follow this algorithmic process:

1. **Identify the Operation Type**: Determine if the task is CPU-bound (requires a child process) or I/O-bound (requires asynchronous streams/Promises).
2. **Select the Concurrency Model**:
   - If modernizing or writing new code, wrap I/O in Promises and use `async/await`.
   - If integrating with older libraries, adhere to the error-first callback pattern.
   - If generating streams of distinct values over time, use EventEmitters or Generators.
3. **Structure the Execution Order**:
   - If initialization requires emitting an event immediately after instantiation, defer the emission using `process.nextTick()`.
   - If a deferred task is heavy and should yield to I/O, use `setImmediate()`.
4. **Implement Error Boundaries**:
   - Wrap all `await` calls in `try/catch`.
   - Provide standard `Error` objects to callbacks.
   - Bind `.on('error')` to all EventEmitters and Streams.
5. **Optimize Process Lifecycle**:
   - Assign `timer.unref()` to any repeating background intervals.
   - Implement graceful teardown on `process.on('SIGINT')` and `process.on('uncaughtException')`.

@Examples (Do's and Don'ts)

### 1. Synchronizing Event Emission on Instantiation
[DO] Use `process.nextTick` to allow the caller to bind listeners before an event fires.
```javascript
const EventEmitter = require('events');

function getEmitter() {
  let emitter = new EventEmitter();
  process.nextTick(() => {
    emitter.emit('start');
  });
  return emitter;
}

let myEmitter = getEmitter();
myEmitter.on('start', () => {
  console.log('Started');
});
```

[DON'T] Emit events synchronously in the constructor/factory before the caller receives the object.
```javascript
const EventEmitter = require('events');

function getEmitter() {
  let emitter = new EventEmitter();
  emitter.emit('start'); // ANTI-PATTERN: Listener hasn't been attached yet
  return emitter;
}

let myEmitter = getEmitter();
myEmitter.on('start', () => {
  console.log('Started'); // This will never execute
});
```

### 2. Timer Lifecycle Management
[DO] Use `unref()` to prevent a background polling timer from keeping the process alive indefinitely.
```javascript
let intervalId = setInterval(() => {
  // Perform some background polling
  checkStatus();
}, 1000);

// Allow Node to exit if this is the only event source left
intervalId.unref(); 
```

[DON'T] Leave recurring timers active without `unref()` if they are strictly background tasks.
```javascript
setInterval(() => {
  // ANTI-PATTERN: This will keep the Node process running forever
  // even if all main application logic has completed.
}, 1000);
```

### 3. Asynchronous Error Handling
[DO] Use `try/catch` with `async/await` and throw real `Error` objects.
```javascript
async function fetchUser(userId) {
  try {
    let user = await db.getUser(userId);
    if (!user) {
      throw new Error("User not found");
    }
    return user;
  } catch (error) {
    console.error("Failed to fetch user:", error);
    throw error;
  }
}
```

[DON'T] Use string rejection or fail to catch synchronous errors inside Promise chains.
```javascript
function fetchUser(userId) {
  // ANTI-PATTERN: If db.getUser throws synchronously, it bypasses the Promise chain.
  // ANTI-PATTERN: Rejecting with a string instead of an Error object.
  return db.getUser(userId)
    .then(user => {
      if (!user) return Promise.reject("User not found"); 
      return user;
    });
}
```

### 4. Naming Asynchronous Callbacks
[DO] Use named functions for callbacks to ensure legible stack traces.
```javascript
const fs = require('fs');

fs.readFile('data.json', {encoding: 'utf8'}, function onFileRead(err, data) {
  if (err) throw err;
  console.log(data);
});
```

[DON'T] Use deep nesting of anonymous functions.
```javascript
const fs = require('fs');

fs.readFile('data.json', {encoding: 'utf8'}, (err, data) => { // ANTI-PATTERN: Anonymous
  if (err) throw err;
  db.save(data, (err, res) => { // ANTI-PATTERN: Anonymous and nesting
     if (err) throw err;
  });
});
```

### 5. Managing Fatal Exceptions
[DO] Gracefully shut down on uncaught exceptions.
```javascript
process.on('uncaughtException', (err) => {
  console.error('Fatal Exception:', err);
  // Perform synchronous cleanup here if necessary
  process.exit(1); 
});
```

[DON'T] Ignore the exception and attempt to keep the process running.
```javascript
process.on('uncaughtException', (err) => {
  console.log('Caught exception: ' + err);
  // ANTI-PATTERN: Leaving the process running in an indeterminate state
});
```