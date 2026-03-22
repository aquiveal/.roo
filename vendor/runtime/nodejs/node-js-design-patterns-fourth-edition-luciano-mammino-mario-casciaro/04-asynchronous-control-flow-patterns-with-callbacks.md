# @Domain

This rule file is triggered whenever the AI is tasked with writing, refactoring, optimizing, or reviewing Node.js code that relies on **Callback-based Asynchronous Control Flow**. It activates specifically when user requests involve managing multiple asynchronous operations, dealing with collections asynchronously, fixing deeply nested callbacks, implementing task queues, or handling race conditions in a single-threaded environment.

# @Vocabulary

*   **Callback Hell / Pyramid of Doom:** An anti-pattern where code grows horizontally with excessive nesting of closures and inline callbacks, resulting in unreadable, unmaintainable, and memory-leaking code.
*   **KISS Principle (Keep It Super Simple):** A design principle prioritizing readability, clear names, and well-known patterns to reduce bugs and simplify maintenance.
*   **Callback Discipline:** A set of best practices to tame callbacks, involving early returns, named functions, and modularization.
*   **Early Return Principle:** Exiting a function immediately upon encountering an error or specific condition (using `return cb(...)`) to avoid deep `if...else` blocks.
*   **Sequential Execution:** Running a set of asynchronous tasks one at a time, where the completion of one triggers the next.
*   **Sequential Iteration:** Processing a dynamic collection of items in sequence using an asynchronous operation.
*   **Parallelism:** Executing multiple tasks simultaneously (e.g., on multiple CPU cores). Not the default for Node.js I/O.
*   **Concurrency:** Efficiently switching between tasks on a single thread to make progress on all of them without blocking.
*   **Unlimited Concurrent Execution Pattern:** Launching all asynchronous tasks at once and waiting for their completion using a counter.
*   **Race Condition:** A defect where the behavior of a program depends on the timing of concurrent operations accessing shared resources.
*   **Limited Concurrent Execution Pattern:** A hybrid algorithm that starts tasks up to a defined limit, then launches a new task only when an active one finishes.
*   **TaskQueue:** A centralized queue entity used to globally limit the concurrency of asynchronous tasks across multiple functional executions.

# @Objectives

*   Eliminate "Callback Hell" by rigorously enforcing Callback Discipline.
*   Prevent event loop blocking and stack overflows when designing asynchronous iterators.
*   Implement robust Control Flow Patterns (Sequential, Concurrent, Limited Concurrent) strictly using plain JavaScript without relying on external libraries where foundational patterns suffice.
*   Prevent race conditions in concurrent asynchronous logic by implementing mutual exclusion mechanisms (e.g., tracking states via `Set`).
*   Protect system resources (e.g., file descriptors, memory) from exhaustion by enforcing limits on concurrent task execution.
*   Ensure resilient error handling in task queues by allowing queues to continue processing even when individual tasks fail.

# @Guidelines

## 1. Callback Discipline
*   **Exit Early:** The AI MUST use `return`, `continue`, or `break` to exit statements immediately upon error or condition fulfillment instead of nesting full `if...else` blocks.
*   **Return on Callback:** The AI MUST explicitly prefix callback invocations with `return` (e.g., `return cb(err)`) when the function's execution must stop, preventing unintended code execution after the callback.
*   **Named Functions:** The AI MUST extract closures and inline callbacks into named functions to provide clearer stack traces and prevent memory leaks caused by retained closure contexts.
*   **Modularize:** The AI MUST break down complex asynchronous workflows into smaller, independent, reusable functions.

## 2. Sequential Execution and Iteration
*   **No Asynchronous `forEach`:** The AI MUST NOT use `Array.prototype.forEach()`, `map()`, or similar synchronous array methods to execute sequential asynchronous operations.
*   **Recursive Iteration:** To execute a dynamic collection of asynchronous tasks sequentially, the AI MUST implement an iterator function that processes the current index and, upon completion, recursively invokes itself with the next index.
*   **Stack Overflow Prevention:** When implementing recursive iterators, if the `task()` being executed is potentially synchronous, the AI MUST account for call stack size limits (e.g., by deferring execution using `process.nextTick()` or `setImmediate()` if necessary).

## 3. Concurrent Execution
*   **Trigger and Track:** To execute tasks concurrently, the AI MUST iterate over the collection, trigger all asynchronous tasks immediately, and track completion using a closure-scoped counter (`let completed = 0`).
*   **Completion Check:** Inside the callback of each concurrent task, the AI MUST increment the counter and check if it equals the total number of tasks to trigger the final `finish()` callback.

## 4. Race Condition Prevention
*   **State Tracking:** When launching concurrent operations that might access or mutate the same external resource (e.g., downloading a file for a specific URL), the AI MUST use a `Set` or similar data structure to track the resource's processing state.
*   **Mutual Exclusion:** Before initiating the async operation, the AI MUST check if the resource identifier exists in the `Set`. If it does, the AI MUST yield (e.g., `return process.nextTick(cb)`). If it does not, the AI MUST add the identifier to the `Set` and proceed.

## 5. Limited Concurrent Execution
*   **Resource Protection:** When a workflow can spawn an uncontrolled number of asynchronous tasks (e.g., crawling links), the AI MUST implement concurrency limits to prevent `ECONNREFUSED` errors or file descriptor exhaustion.
*   **Iterator with While Loop:** The AI MUST implement local concurrency limits using a `while` loop inside an iterator function (`next()`). The loop must continue spawning tasks only while the `running` count is less than the `concurrency` limit and there are tasks remaining.
*   **Global TaskQueues:** For complex applications, the AI MUST implement a global `TaskQueue` class leveraging `EventEmitter`.
*   **Queue Fault Tolerance:** In a `TaskQueue`, when a task yields an error, the AI MUST emit an `error` (or `taskError`) event but MUST NOT halt the queue or clear pending tasks. The queue MUST continue processing.

# @Workflow

When instructed to implement or refactor asynchronous callback-based logic, the AI MUST adhere to the following algorithmic process:

1.  **Analyze the Workload:** Determine if the tasks must be executed in a specific order (Sequential), independently at the same time (Concurrent), or independently but constrained by system resources (Limited Concurrent).
2.  **Apply Callback Discipline:** Refactor the target code to flatten any existing "Callback Hell". Apply the Early Return Principle and abstract inline functions into named, standalone functions.
3.  **Implement the Flow Pattern:**
    *   *If Sequential:* Construct a recursive `iterate(index)` function.
    *   *If Concurrent:* Construct a `for...of` loop launching all tasks, bound by a `++completed === tasks.length` check.
    *   *If Limited Concurrent:* Construct a `next()` function utilizing a `while(running < limit)` loop.
4.  **Inject Race Condition Safeguards:** Analyze the concurrent tasks for shared resource contention. Inject a `Set` to track active identifiers and return early if a task for that identifier is already in flight.
5.  **Queue Centralization (If required):** If the concurrency limit must be enforced globally across multiple functional scopes, abstract the Limited Concurrent pattern into an `EventEmitter`-backed `TaskQueue` class.

# @Examples (Do's and Don'ts)

## Callback Discipline (Early Return)

**[DON'T]** Use `if...else` blocks that cause deep nesting and forget to halt execution after the callback.
```javascript
function readAndProcess(filename, cb) {
  exists(filename, (err, exists) => {
    if (err) {
      cb(err);
    } else {
      if (exists) {
        // ... deep nesting
      }
    }
  });
}
```

**[DO]** Use early returns to keep the code shallow and explicitly `return cb(...)`.
```javascript
function readAndProcess(filename, cb) {
  exists(filename, (err, exists) => {
    if (err) {
      return cb(err);
    }
    if (exists) {
      return cb(null, true);
    }
    // Proceed with processing...
  });
}
```

## Sequential Iteration

**[DON'T]** Use `forEach` for asynchronous sequential execution, as it executes synchronously and initiates all tasks concurrently.
```javascript
function processSequentially(tasks, cb) {
  tasks.forEach(task => {
    asyncOperation(task, () => {
      console.log('Processed');
    });
  });
  cb(); // Fires before tasks complete
}
```

**[DO]** Use a recursive iterator pattern to guarantee sequential execution.
```javascript
function processSequentially(tasks, cb) {
  function iterate(index) {
    if (index === tasks.length) {
      return cb();
    }
    const task = tasks[index];
    asyncOperation(task, (err) => {
      if (err) {
        return cb(err);
      }
      iterate(index + 1);
    });
  }
  iterate(0);
}
```

## Concurrent Execution

**[DON'T]** Assume concurrent tasks will resolve in order, or fail to track completion accurately.
```javascript
function processConcurrently(tasks, cb) {
  for (const task of tasks) {
    asyncOperation(task, () => {});
  }
  // No way to know when all are done
}
```

**[DO]** Use a closure-scoped counter to track completions and trigger the final callback.
```javascript
function processConcurrently(tasks, cb) {
  let completed = 0;
  let hasErrors = false;

  for (const task of tasks) {
    asyncOperation(task, (err) => {
      if (err && !hasErrors) {
        hasErrors = true;
        return cb(err);
      }
      if (++completed === tasks.length && !hasErrors) {
        return cb();
      }
    });
  }
}
```

## Fixing Race Conditions in Concurrent Tasks

**[DON'T]** Allow multiple concurrent tasks to query and mutate the same resource simultaneously without mutual exclusion.
```javascript
function download(url, cb) {
  // If called concurrently twice for the same URL, both will pass this check
  exists(url, (err, exists) => {
    if (!exists) {
      performDownload(url, cb); 
    }
  });
}
```

**[DO]** Use a synchronous tracking mechanism (like a `Set`) to exclude duplicate operations on the same resource.
```javascript
const downloading = new Set();

function download(url, cb) {
  if (downloading.has(url)) {
    return process.nextTick(cb);
  }
  downloading.add(url);
  
  performDownload(url, (err) => {
    // Optionally remove from Set if necessary, or keep to prevent future downloads
    cb(err);
  });
}
```

## Limited Concurrent Execution

**[DON'T]** Spawn an unlimited number of tasks that can overwhelm system resources (memory, file descriptors, network ports).

**[DO]** Implement a `while` loop that checks against a `concurrency` limit and dynamically schedules the next task upon completion.
```javascript
function processWithLimit(tasks, concurrency, cb) {
  let running = 0;
  let completed = 0;
  let index = 0;

  function next() {
    while (running < concurrency && index < tasks.length) {
      const task = tasks[index++];
      task((err) => {
        if (err) {
          return cb(err); // Or handle error resiliently
        }
        if (++completed === tasks.length) {
          return cb();
        }
        running--;
        next();
      });
      running++;
    }
  }
  next();
}
```

## Global Task Queue

**[DO]** Abstract limited concurrency into a reusable `TaskQueue` class when concurrency must be controlled globally across multiple application components.
```javascript
import { EventEmitter } from 'events';

export class TaskQueue extends EventEmitter {
  constructor(concurrency) {
    super();
    this.concurrency = concurrency;
    this.running = 0;
    this.queue = [];
  }

  pushTask(task) {
    this.queue.push(task);
    process.nextTick(this.next.bind(this));
    return this;
  }

  next() {
    if (this.running === 0 && this.queue.length === 0) {
      return this.emit('empty');
    }
    
    while (this.running < this.concurrency && this.queue.length > 0) {
      const task = this.queue.shift();
      task((err) => {
        if (err) {
          this.emit('error', err); // Do not halt the queue on error
        }
        this.running--;
        process.nextTick(this.next.bind(this));
      });
      this.running++;
    }
  }
}
```