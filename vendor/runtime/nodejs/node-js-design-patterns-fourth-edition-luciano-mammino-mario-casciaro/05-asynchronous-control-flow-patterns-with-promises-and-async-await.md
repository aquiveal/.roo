# @Domain
These rules MUST be activated whenever the AI is tasked with writing, refactoring, reviewing, or debugging asynchronous JavaScript or Node.js code. This includes processing user requests involving Promises, `async/await` syntax, converting legacy callbacks to modern asynchronous paradigms, managing asynchronous control flows (sequential, concurrent, or limited concurrency), handling asynchronous errors, or optimizing memory management in long-running asynchronous processes.

# @Vocabulary
- **Promise**: An object representing the eventual result (or error) of an asynchronous operation.
- **Pending**: The state of a Promise when the asynchronous operation is not yet complete.
- **Fulfilled**: The state of a Promise when the asynchronous operation completes successfully.
- **Rejected**: The state of a Promise when the asynchronous operation terminates with an error.
- **Settled**: The state of a Promise once it is either fulfilled or rejected.
- **Thenable**: A Promise-like object that implements a `then()` method, satisfying the Promises/A+ specification (duck typing).
- **Promisification**: The process of converting a callback-based function (following Node.js error-first conventions) into a function that returns a Promise.
- **Microtask Queue**: The mechanism that schedules Promise callbacks (`onFulfilled`/`onRejected`) to run asynchronously immediately after the current synchronous call stack clears, preventing Zalgo.
- **Top-level Await**: The ability to use the `await` keyword directly at the top level of an ECMAScript Module (ESM), outside of an `async` function.
- **Lazy Promise**: A Promise whose executor function is not invoked immediately upon creation, but deferred until its result is explicitly requested (e.g., via `.then()`, `.catch()`, or `.finally()`).
- **Infinite Recursive Promise Chain**: A memory leak condition occurring when a Promise's resolution depends on the promise returned by its own recursive invocation.

# @Objectives
- The AI MUST eliminate "callback hell" by upgrading code to use Promises and `async/await`.
- The AI MUST ensure asynchronous code readability is indistinguishable from synchronous code whenever possible using `async/await`.
- The AI MUST guarantee robust, unified error handling across both synchronous and asynchronous operations.
- The AI MUST prevent memory leaks caused by infinite Promise resolution chains.
- The AI MUST enforce the correct application of sequential, concurrent, and limited-concurrent execution patterns.

# @Guidelines

## Promise Fundamentals and API Usage
- When interacting with Promises, the AI MUST handle both resolution and rejection. The AI MUST use `.catch(onRejected)` as the standard method for handling rejections.
- The AI MUST use `Promise.resolve()` to instantly wrap a value or thenable into a fulfilled Promise.
- The AI MUST use `Promise.reject()` to instantly create a rejected Promise.
- For concurrent execution where all tasks must succeed, the AI MUST use `Promise.all(iterable)`. The AI MUST acknowledge this fails fast if a single Promise rejects.
- For concurrent execution where failures should be tolerated without interrupting other tasks, the AI MUST use `Promise.allSettled(iterable)`.
- When the first resolved or rejected Promise should determine the outcome, the AI MUST use `Promise.race(iterable)`.
- When external control over a Promise's resolution or rejection is required (e.g., integrating with event-driven code or testing), the AI MUST use `Promise.withResolvers()`.
- The AI MUST use `.finally(onFinally)` to execute cleanup code regardless of whether the Promise fulfills or rejects. The AI MUST NOT expect arguments in the `onFinally` callback.

## Promisification
- When converting legacy Node.js error-first callback APIs to Promises, the AI MUST use the built-in `node:util` `promisify` function rather than creating custom wrappers, unless a custom wrapper is explicitly requested.

## Asynchronous Control Flow
- **Sequential Execution**: To execute tasks sequentially, the AI MUST use `for...of` loops combined with `await`. If using raw Promises, the AI MUST build a dynamic chain using `Array.prototype.reduce()` starting with `Promise.resolve()`.
- **Concurrent Execution**: To execute tasks concurrently, the AI MUST map the tasks to an array of Promises and pass them to `Promise.all()` or `Promise.allSettled()`.
- **Limited Concurrent Execution**: When limiting concurrency, the AI MUST implement a Queue mechanism (e.g., a `TaskQueue` class) that tracks running tasks, enforces a concurrency limit, and uses `.finally()` to decrement the running count and trigger the next task.
- **Lazy Initialization**: If a Promise encapsulates an expensive operation or an operation that might not be needed, the AI MUST wrap the instantiation in a factory function or implement a custom `LazyPromise` class that extends `Promise` and defers executor initialization until `.then()`, `.catch()`, or `.finally()` is called.

## Async/Await Rules
- The AI MUST treat `async/await` as the primary and preferred syntax for asynchronous code over raw Promise chaining.
- The AI MUST leverage **Top-Level Await** in `.mjs` or `"type": "module"` files for asynchronous initialization (e.g., database connections, fetching configurations).
- **Unified Error Handling**: The AI MUST use `try...catch` blocks within `async` functions to catch both synchronous `throw` errors and asynchronous Promise rejections simultaneously.
- **The "return await" Trap**: If a Promise is returned inside a `try` block and the AI intends to catch its rejection within the local `catch` block, the AI MUST explicitly use `return await`. Returning the Promise without `await` will bypass the local `catch` block and return the rejected Promise to the caller.

## Anti-Patterns and Memory Leaks
- **Array.forEach Antipattern**: The AI MUST NOT use `Array.prototype.forEach()` with an `async` callback for sequential execution. This pattern launches all tasks concurrently and ignores the returned Promises. The AI MUST use a `for...of` loop instead.
- **Infinite Recursive Promise Chains**: The AI MUST NOT create recursive functions where a Promise resolves by returning a recursive call to the same Promise-returning function. This strictly violates Promises/A+ memory management and causes memory leaks. To create infinite asynchronous loops, the AI MUST use an `async` function with a `while (true)` loop and `await`.

# @Workflow
1. **Assessment**: Evaluate the asynchronous task. Determine if the execution flow must be sequential, concurrent, or limited concurrent.
2. **Modernization**: If the code uses callbacks, refactor it to `async/await`. If it uses legacy Node.js callbacks, apply `util.promisify`.
3. **Flow Implementation**:
   - *Sequential*: Implement using `for...of` with `await`.
   - *Concurrent*: Implement using `Promise.all()` or `Promise.allSettled()`.
   - *Limited*: Implement a TaskQueue utilizing internal counters and `.finally()`.
4. **Error Handling**: Wrap the `await` calls in a `try...catch` block. If returning the result of an asynchronous operation from within the `try` block, prepend `await` to the `return` statement.
5. **Anti-pattern Check**: Scan the code to ensure `Array.prototype.forEach()` is not used with `async` callbacks, and verify that no infinite recursive Promise chains exist.
6. **Execution Deferral**: If the Promise executes resource-intensive operations that may not be required immediately, convert it to a Lazy Promise.

# @Examples (Do's and Don'ts)

## The "return await" Trap
[DON'T] Return a Promise directly inside a try block if you want to catch its error locally.
```javascript
async function errorNotCaught() {
  try {
    // The rejection escapes this function and is NOT caught by the catch block below
    return delayError(1000) 
  } catch (err) {
    console.error('Error caught locally: ' + err.message)
  }
}
```

[DO] Use `return await` to handle the rejection locally.
```javascript
async function errorCaught() {
  try {
    // The rejection is caught locally
    return await delayError(1000) 
  } catch (err) {
    console.error('Error caught locally: ' + err.message)
  }
}
```

## Sequential Iteration Antipattern
[DON'T] Use `Array.prototype.forEach` with an async callback for sequential execution.
```javascript
async function spiderLinks(links) {
  // This will execute all spider tasks concurrently and ignore the results/errors
  links.forEach(async function iteration(link) {
    await spider(link)
  })
}
```

[DO] Use a `for...of` loop with `await` for guaranteed sequential execution.
```javascript
async function spiderLinks(links) {
  // This executes strictly sequentially
  for (const link of links) {
    await spider(link)
  }
}
```

## Infinite Recursive Promise Chains (Memory Leak)
[DON'T] Return a recursive Promise call inside a `.then()` or `async` function.
```javascript
function leakingLoop() {
  return delay(1).then(() => {
    console.log('Tick')
    // Causes a memory leak due to unresolvable promise chain
    return leakingLoop() 
  })
}
```

[DO] Use a `while (true)` loop inside an `async` function for infinite asynchronous loops.
```javascript
async function nonLeakingLoopAsync() {
  // Safe, garbage collectable, and maintains error propagation
  while (true) {
    await delay(1)
    console.log('Tick')
  }
}
```

## Concurrent Execution
[DON'T] Map over an array and await them individually in a loop if you want them to run concurrently.
```javascript
async function processLinks(links) {
  const promises = links.map(link => spider(link))
  // While this works, it does not fail-fast efficiently for the whole batch
  for (const p of promises) {
    await p;
  }
}
```

[DO] Use `Promise.all` (or `Promise.allSettled`) to manage concurrent execution.
```javascript
async function processLinks(links) {
  const promises = links.map(link => spider(link))
  // Fails fast, clean, and idiomatic
  return Promise.all(promises)
}
```

## Sequential Execution with Raw Promises
[DON'T] Hardcode dynamic chains using external variable tracking poorly.
```javascript
let promise = Promise.resolve()
for (const link of links) {
  promise = promise.then(() => spider(link))
}
return promise
```

[DO] Use `Array.prototype.reduce` for a functional, clean dynamic promise chain.
```javascript
return links.reduce((prev, link) => {
  return prev.then(() => spider(link))
}, Promise.resolve())
```