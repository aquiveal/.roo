# Node.js Asynchronous Patterns & Concurrency Rules

## Prefer Async/Await over Callbacks
**Context:** Asynchronous code using callbacks (Continuation-Passing Style) often leads to deeply nested code ("Callback Hell") and poor error handling. Promises and Async/Await provide a cleaner, sequential flow and robust error propagation (Chapter 5).
**Directive:** ALWAYS use `async/await` for asynchronous logic flow, reserving callbacks only for event listeners or low-level library interoperability.

### ❌ Anti-Pattern (What to avoid)
```javascript
// Reading a config file, parsing it, and saving to a database using callbacks.
// This structure is hard to read, and error handling is repetitive.
const fs = require('fs');

function processConfig(filePath, dbConnection, callback) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      // Repetitive error handling
      return callback(err);
    }

    let config;
    try {
      config = JSON.parse(data);
    } catch (parseErr) {
      // Synchronous errors inside callbacks must be caught manually
      return callback(parseErr);
    }

    dbConnection.query('INSERT INTO configs SET ?', config, (dbErr, result) => {
      if (dbErr) {
        return callback(dbErr);
      }
      callback(null, result);
    });
  });
}
```

### ✅ Best Practice (What to do)
```javascript
// The same logic using async/await.
// The code reads top-to-bottom, and try/catch handles both sync and async errors.
import { readFile } from 'node:fs/promises';

async function processConfig(filePath, dbConnection) {
  try {
    // Await the promise-based I/O operation
    const data = await readFile(filePath, 'utf8');
    
    // Synchronous parsing happens in the same flow
    const config = JSON.parse(data);

    // Database operation is awaited
    const result = await dbConnection.query('INSERT INTO configs SET ?', config);
    
    return result;
  } catch (err) {
    // Centralized error handling for file IO, parsing, or DB errors
    console.error('Failed to process config:', err);
    throw err;
  }
}
```

## Enforce Consistent Asynchrony (Avoid Zalgo)
**Context:** An API that behaves synchronously under some conditions (e.g., cached data) and asynchronously under others (e.g., disk I/O) creates unpredictable execution order, leading to race conditions known as "Unleashing Zalgo" (Chapter 3).
**Directive:** ALWAYS ensure an API is consistently asynchronous, using `process.nextTick()` or `queueMicrotask()` if a synchronous response is available.

### ❌ Anti-Pattern (What to avoid)
```javascript
// This function behaves inconsistently.
// If the cache is hot, it returns immediately (sync).
// If cold, it returns later (async).
// This breaks the caller's expectation of execution order.
const cache = new Map();

function getData(key, callback) {
  if (cache.has(key)) {
    // PROBLEM: Synchronous callback invocation
    callback(null, cache.get(key));
  } else {
    // Asynchronous callback invocation
    fetchDataFromDb(key, (err, data) => {
      if (err) return callback(err);
      cache.set(key, data);
      callback(null, data);
    });
  }
}

// Caller code
console.log('Before');
getData('user:1', (err, data) => {
  console.log('Data received');
});
console.log('After');
// Output if cached: Before -> Data received -> After
// Output if NOT cached: Before -> After -> Data received
```

### ✅ Best Practice (What to do)
```javascript
// This function guarantees asynchronous behavior.
// Even if data is cached, the callback is deferred to the next tick.
const cache = new Map();

function getData(key, callback) {
  if (cache.has(key)) {
    // CORRECT: Defer execution to ensure consistent async behavior
    process.nextTick(() => callback(null, cache.get(key)));
  } else {
    fetchDataFromDb(key, (err, data) => {
      if (err) return callback(err);
      cache.set(key, data);
      callback(null, data);
    });
  }
}

// Or better yet, using Promises/Async-Await which enforces microtask queuing
async function getDataPromise(key) {
  if (cache.has(key)) {
    return cache.get(key); // Implicitly wrapped in a resolved Promise (async)
  }
  const data = await fetchDataFromDb(key);
  cache.set(key, data);
  return data;
}
```

## Limit Concurrency
**Context:** Spawning unlimited parallel tasks (e.g., `Promise.all` on a massive array) can exhaust system resources (file descriptors, memory) or overwhelm downstream services. Limiting concurrency ensures stability (Chapter 4/11).
**Directive:** ALWAYS limit concurrent asynchronous operations using patterns like task queues or libraries like `p-limit` when processing collections.

### ❌ Anti-Pattern (What to avoid)
```javascript
// Downloading 10,000 files simultaneously.
// This will likely cause EMFILE errors (too many open files) or memory crashes.
const filesToDownload = getListOfTenThousandFiles();

async function downloadAll() {
  // DANGEROUS: Starts all requests at once
  const promises = filesToDownload.map(async (fileUrl) => {
    const content = await fetch(fileUrl);
    await saveToFile(content);
  });

  await Promise.all(promises);
}
```

### ✅ Best Practice (What to do)
```javascript
// Using a concurrency limit (e.g., p-limit or a custom queue)
// to ensure only 5 downloads happen at a time.
import pLimit from 'p-limit';

const limit = pLimit(5); // Concurrency limit of 5
const filesToDownload = getListOfTenThousandFiles();

async function downloadAll() {
  // Maps the array to "limited" promises
  const promises = filesToDownload.map((fileUrl) => {
    // The limit wrapper ensures this task waits for a slot
    return limit(async () => {
      const content = await fetch(fileUrl);
      await saveToFile(content);
    });
  });

  await Promise.all(promises);
}
```

## Handle Errors Correctly
**Context:** Unhandled errors in asynchronous flows can leave the application in an undefined state or crash the process. Errors must be propagated correctly through the chain (Chapter 3/5).
**Directive:** ALWAYS explicitly handle errors; propagate them in callbacks, use `try/catch` in async functions, and never ignore rejected promises.

### ❌ Anti-Pattern (What to avoid)
```javascript
// A "fire-and-forget" approach where errors are swallowed.
// If json parsing fails, the error is logged but the caller never knows.
// If saveToDb fails, the promise chain is broken or unhandled.
function processUserData(jsonString) {
  Promise.resolve().then(() => {
    const data = JSON.parse(jsonString); // May throw SyntaxError
    return saveToDb(data);
  }).catch(err => {
    console.log('Something went wrong', err);
    // Error is swallowed here; the function ostensibly succeeds
  });
}
```

### ✅ Best Practice (What to do)
```javascript
// Errors are propagated to the caller, allowing them to handle the failure.
// Structured error handling ensures resources are cleaned up.
async function processUserData(jsonString) {
  try {
    const data = JSON.parse(jsonString);
    await saveToDb(data);
    return { success: true };
  } catch (err) {
    // Enhance error context before re-throwing or handling
    const wrappedError = new Error(`Failed to process user data: ${err.message}`);
    wrappedError.cause = err;
    throw wrappedError; 
  }
}
```

## Offload CPU-bound Tasks
**Context:** Node.js is single-threaded. Long-running synchronous calculations block the Event Loop, making the server unresponsive to new I/O events (requests) (Chapter 11).
**Directive:** NEVER block the Event Loop with heavy computations; offload them to Worker Threads or separate child processes.

### ❌ Anti-Pattern (What to avoid)
```javascript
// Calculating Fibonacci sequence synchronously on the main thread.
// While this runs, no other HTTP requests can be handled.
import { createServer } from 'node:http';

function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

const server = createServer((req, res) => {
  // Blocks the event loop for seconds/minutes if n is large
  const result = fibonacci(45); 
  res.end(`Result: ${result}`);
});

server.listen(3000);
```

### ✅ Best Practice (What to do)
```javascript
// Offloading the calculation to a Worker Thread.
// The main thread remains responsive to other requests.
import { createServer } from 'node:http';
import { Worker } from 'node:worker_threads';
import { join } from 'node:path';

function runFibonacciWorker(n) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(join(__dirname, 'fib-worker.js'), {
      workerData: { n }
    });
    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
    });
  });
}

const server = createServer(async (req, res) => {
  try {
    // Main thread yields; worker computes in parallel
    const result = await runFibonacciWorker(45);
    res.end(`Result: ${result}`);
  } catch (err) {
    res.statusCode = 500;
    res.end('Calculation error');
  }
});

server.listen(3000);
```
