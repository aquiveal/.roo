# @Domain

These rules trigger when the AI is tasked with writing, reviewing, refactoring, or architecting asynchronous JavaScript/Node.js code. Specifically, they apply when handling control flow, designing APIs, implementing the Observer pattern, utilizing the `EventEmitter` class, constructing callback-based interfaces (Continuation-Passing Style), or debugging asynchronous memory leaks and race conditions (e.g., Zalgo).

# @Vocabulary

- **Callback**: A function passed as an argument to another function, invoked to handle the result of an operation once it completes.
- **Continuation-Passing Style (CPS)**: A functional programming style where a result is propagated by passing it to another function (the callback) instead of directly returning it to the caller.
- **Synchronous CPS**: A callback invoked immediately, where the host function completes its execution only when the callback does.
- **Asynchronous CPS**: A callback scheduled to be executed in the future (e.g., using `setTimeout`), allowing the host function to return control to the event loop immediately.
- **Non-CPS Callback**: A callback used for purposes other than propagating an asynchronous result (e.g., the callback in `Array.prototype.map`).
- **Zalgo**: An unpredictable API behavior where a function behaves synchronously under certain conditions and asynchronously under others, leading to race conditions and unpredictable listener execution.
- **Event Loop**: The core mechanism in Node.js that handles asynchronous callbacks, executing them in a specific priority order (timers, microtasks, I/O, immediates).
- **Microtask**: A task deferred using `process.nextTick()`. It executes immediately after the current operation completes, before any pending I/O events.
- **I/O Starvation**: A condition caused by recursively scheduling microtasks (`process.nextTick()`), preventing the event loop from processing I/O callbacks.
- **Observer Pattern**: A pattern defining a subject object that notifies a set of observers (listeners) when a state change occurs. Implemented in Node.js via `EventEmitter`.
- **Fail-Fast**: A resilience strategy where an application exits immediately upon encountering an unrecoverable state (e.g., an `uncaughtException`), rather than continuing with unpredictable behavior.

# @Objectives

- Ensure absolute consistency in asynchronous APIs to prevent Zalgo anti-patterns.
- Enforce strict Node.js callback conventions (Error-first, Callback-last).
- Guarantee safe and robust error propagation across asynchronous boundaries.
- Prevent memory leaks and application crashes caused by unhandled events or lingering closures.
- Strategically select between Callbacks, EventEmitters, or a combination of both based on the multiplicity and nature of the expected results.

# @Guidelines

- **Callback Positioning Constraint**: The AI MUST always place the callback function as the absolute last argument in any asynchronous API signature, even when optional arguments are present (e.g., `readFile(filename, [options], callback)`).
- **Error-First Callback Enforcement**: The first argument of a CPS callback MUST always be reserved for errors. If the operation succeeds, the AI MUST pass `null` or `undefined` as the first argument.
- **Strict Error Instance Rule**: Errors passed to callbacks or emitted via `EventEmitter` MUST always be instances of the `Error` class. The AI MUST NOT pass simple strings or numbers as errors.
- **Return on Callback Rule**: When propagating an error or result via a callback, the AI MUST use the `return` statement to immediately halt the function's execution (e.g., `return cb(err)`).
- **Synchronous Exception Isolation**: When wrapping synchronous code that might throw (e.g., `JSON.parse`) inside an asynchronous function, the AI MUST use a `try...catch` block. The AI MUST propagate caught errors to the callback. 
- **Callback Safety within Try-Catch**: The AI MUST NOT invoke the callback from within a `try` block. Doing so risks catching errors thrown by the callback itself, which belongs to the consumer's context.
- **Zalgo Prevention (API Consistency)**: An API MUST be either 100% synchronous or 100% asynchronous. The AI MUST NEVER create a function that invokes a callback synchronously if data is cached, but asynchronously if data must be fetched.
- **Enforcing Asynchronicity**: To convert a synchronous operation into an asynchronous one (e.g., returning cached data in an async API), the AI MUST defer the callback execution using `process.nextTick()`.
- **NextTick vs SetImmediate Usage**: The AI MUST use `process.nextTick()` to guarantee a callback fires before any pending I/O. The AI MUST use `setImmediate()` to queue execution after I/O events. The AI MUST avoid recursive `process.nextTick()` calls to prevent I/O starvation.
- **Uncaught Exception Handling**: Uncaught exceptions inside async callbacks jump to the event loop and crash the application. The AI MUST NOT attempt to catch these with a wrapping `try...catch`. If utilizing `process.on('uncaughtException')`, the AI MUST force a process exit (`process.exit(1)`) after cleanup, enforcing the Fail-Fast principle.
- **EventEmitter Error Handling**: The AI MUST always register a listener for the `'error'` event on any `EventEmitter` instance. Unhandled `'error'` events will automatically throw an exception and crash the Node.js process.
- **Inheriting EventEmitter**: When creating observable objects, the AI MUST extend the `EventEmitter` class (`class MyClass extends EventEmitter`) and MUST invoke `super()` inside the constructor.
- **EventEmitter Memory Management**: The AI MUST unsubscribe listeners (using `removeListener` or `off`) when observing objects with a long lifespan to prevent memory leaks caused by retained closures. If an event is only expected once, the AI SHOULD use `.once()`, but MUST account for the listener leaking if the event never fires.
- **Sync/Async Event Emission Constraint**: The AI MUST NOT mix synchronous and asynchronous event emissions within the same `EventEmitter`. If emitting asynchronously, listeners can be attached after the triggering method is called. If emitting synchronously, listeners MUST be attached before the trigger is invoked. Deferred sync emissions MUST use `process.nextTick()`.
- **Callbacks vs. EventEmitters Selection**: The AI MUST use Callbacks when an asynchronous operation returns exactly one result. The AI MUST use an `EventEmitter` when an operation can trigger an event multiple times, or when there are multiple heterogeneous events to communicate.
- **Combining Callbacks and Events**: For long-running operations (e.g., downloads), the AI MUST use a hybrid pattern: accept a callback for the final result/error, and return an `EventEmitter` to broadcast intermediate progress events.

# @Workflow

1.  **API Paradigm Selection**: 
    *   Analyze the expected outcome of the asynchronous task.
    *   If returning a single final result/error, use the Callback Pattern.
    *   If broadcasting state changes, streams of data, or multiple occurrences, use the Observer Pattern (`EventEmitter`).
    *   If requiring both progress tracking and a final completion notification, use the Hybrid Pattern.
2.  **Signature Formulation**: 
    *   Define the function signature. If using a callback, place the callback parameter at the extreme end of the parameter list.
3.  **Consistency Verification (Anti-Zalgo)**:
    *   Trace all logical branches within the function.
    *   If any branch invokes the callback asynchronously (e.g., fetching data), ensure all other branches (e.g., cache hits) defer their callback invocation using `process.nextTick()`.
4.  **Implementation & Error Boundary Enforcement**:
    *   Implement the core logic. 
    *   Wrap volatile synchronous operations (e.g., JSON parsing) in a `try...catch` block.
    *   Return errors immediately (`return cb(err)`).
    *   Ensure the callback is executed *outside* the `try...catch` scope to avoid swallowing consumer exceptions.
5.  **Event Emission & Lifecycle Management (If applicable)**:
    *   Extend `EventEmitter` and call `super()`.
    *   Emit errors exclusively via `this.emit('error', new Error(...))`.
    *   Attach listeners safely. Ensure cleanup (`removeListener`) is implemented for long-living emitters to prevent memory leaks.

# @Examples (Do's and Don'ts)

### Zalgo / Inconsistent Asynchrony
[DON'T]
```javascript
const cache = new Map();
function inconsistentRead(filename, cb) {
  if (cache.has(filename)) {
    // Anti-pattern: Synchronous callback invocation in an async API
    cb(null, cache.get(filename));
  } else {
    readFile(filename, 'utf8', (err, data) => {
      if (err) return cb(err);
      cache.set(filename, data);
      cb(null, data);
    });
  }
}
```

[DO]
```javascript
import { readFile } from 'node:fs';
const cache = new Map();
function consistentReadAsync(filename, cb) {
  if (cache.has(filename)) {
    // Correct: Guarantee asynchronicity using deferred execution
    return process.nextTick(() => cb(null, cache.get(filename)));
  } else {
    readFile(filename, 'utf8', (err, data) => {
      if (err) return cb(err);
      cache.set(filename, data);
      cb(null, data);
    });
  }
}
```

### Error Propagation and Try-Catch Boundaries
[DON'T]
```javascript
function readJson(filename, cb) {
  readFile(filename, 'utf8', (err, data) => {
    if (err) cb(err); // Anti-pattern: Missing return statement, execution continues
    
    try {
      const parsed = JSON.parse(data);
      // Anti-pattern: Invoking callback inside try block catches consumer errors
      cb(null, parsed); 
    } catch (err) {
      // Anti-pattern: String instead of Error instance
      cb("Parsing failed"); 
    }
  });
}
```

[DO]
```javascript
function readJson(filename, cb) {
  readFile(filename, 'utf8', (err, data) => {
    if (err) {
      return cb(err); // Correct: Early return
    }
    
    let parsed;
    try {
      parsed = JSON.parse(data);
    } catch (err) {
      return cb(err); // Correct: Propagate real Error instance
    }
    
    // Correct: Callback invoked safely outside the try...catch block
    cb(null, parsed);
  });
}
```

### EventEmitter Extension and Error Handling
[DON'T]
```javascript
import { EventEmitter } from 'node:events';

class FindRegex { // Anti-pattern: Not extending EventEmitter
  constructor(regex) {
    this.regex = regex;
    this.emitter = new EventEmitter();
  }
  find(files) {
    for (const file of files) {
      readFile(file, 'utf8', (err, content) => {
        // Anti-pattern: Throwing inside async callback jumps to Event Loop and crashes
        if (err) throw err; 
        
        const match = content.match(this.regex);
        if (match) this.emitter.emit('found', file, match);
      });
    }
    return this.emitter;
  }
}
```

[DO]
```javascript
import { EventEmitter } from 'node:events';
import { readFile } from 'node:fs';

class FindRegex extends EventEmitter { // Correct: Extending EventEmitter
  constructor(regex) {
    super(); // Correct: Must call super()
    this.regex = regex;
    this.files = [];
  }
  
  addFile(file) {
    this.files.push(file);
    return this;
  }
  
  find() {
    for (const file of this.files) {
      readFile(file, 'utf8', (err, content) => {
        if (err) {
          // Correct: Emitting 'error' event instead of throwing
          return this.emit('error', err); 
        }
        
        this.emit('fileread', file);
        const match = content.match(this.regex);
        if (match) {
          for (const elem of match) {
            this.emit('found', file, elem);
          }
        }
      });
    }
    return this;
  }
}
```

### Combining Callbacks and Events
[DON'T]
```javascript
// Anti-pattern: Returning progress directly in a callback meant for a final result
function download(url, cb) {
  const req = get(url, (res) => {
    res.on('data', chunk => cb(null, 'progress', chunk));
    res.on('end', () => cb(null, 'done'));
  });
}
```

[DO]
```javascript
import { EventEmitter } from 'node:events';
import { get } from 'node:https';

function download(url, cb) {
  const eventEmitter = new EventEmitter();
  
  const req = get(url, (res) => {
    const chunks = [];
    let downloadedBytes = 0;
    const fileSize = Number.parseInt(res.headers['content-length'], 10);
    
    res.on('error', err => {
      cb(err);
    });
    
    res.on('data', chunk => {
      chunks.push(chunk);
      downloadedBytes += chunk.length;
      // Emit intermediate progress events
      eventEmitter.emit('progress', downloadedBytes, fileSize);
    });
    
    res.on('end', () => {
      const data = Buffer.concat(chunks);
      // Execute callback for the final single result
      cb(null, data);
    });
  });
  
  req.on('error', err => {
    cb(err);
  });
  
  return eventEmitter; // Return the emitter for tracking occurrences
}
```