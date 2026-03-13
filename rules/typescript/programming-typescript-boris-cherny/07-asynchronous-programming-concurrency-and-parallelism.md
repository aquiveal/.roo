# @Domain
This rule set applies to any TypeScript or JavaScript code involving asynchronous programming, concurrency, or parallelism. This includes code utilizing callbacks, Promises, `async`/`await`, event emitters, streams, Web Workers, NodeJS child processes, or any inter-thread/inter-process message-passing architectures.

# @Vocabulary
- **Event Loop**: The standard threading model for JavaScript engines where a single thread multiplexes tasks. It continuously checks an event queue for pending tasks when the main call stack is empty.
- **Event Queue**: A queue used by the JavaScript platform for relaying the results of native asynchronous operations back to the main thread.
- **Callback**: A plain old function passed as an argument to another function, invoked when an asynchronous task completes.
- **Callback Pyramid**: Deeply nested callback functions that make sequencing asynchronous operations difficult and error-prone.
- **Promise**: An abstraction over asynchronous work representing a future value, providing methods (`then`, `catch`, `finally`) to sequence and compose asynchronous tasks.
- **Executor**: The function passed into a Promise constructor that takes a `resolve` function and a `reject` function.
- **Async Streams**: Multiple values that become available at multiple points in the future (e.g., streaming network data, UI events).
- **Event Emitter**: A design pattern and API that supports emitting events on a specific channel and listening for events on that channel.
- **Web Worker**: A browser-provided background thread used to run CPU-bound tasks in true parallel without blocking the main UI thread.
- **Message Passing**: The primary safe communication method between threads (main thread and workers or child processes) using `postMessage`, `onmessage`, `send`, or `on('message')`.
- **Protocol**: A strict call-response mapping defining the specific operations a worker/process can perform, alongside their expected `in` and `out` types.

# @Objectives
- Abstract unsafe, untyped asynchronous boundaries (like raw event emitters or web worker message passing) into strictly typed APIs.
- Eliminate callback pyramids by favoring Promises and `async`/`await` for sequencing asynchronous operations.
- Enforce type safety for error handling in asynchronous operations, recognizing that JavaScript rejections can be of any type.
- Guarantee that multithreaded communication relies on strict, mapped type protocols rather than arbitrary string events and `any` payloads.

# @Guidelines
- **Understand the Event Loop**: Never assume synchronous execution for asynchronous APIs. Control returns to the main thread immediately after calling an async API, and callbacks execute only after the call stack empties.
- **Legacy Callbacks**: When interacting with legacy NodeJS APIs, adhere to the convention where the callback's first parameter is `Error | null` and the second is the result `T | null`.
- **Prefer Promises over Callbacks**: Do not use callbacks for sequencing multiple asynchronous operations. Wrap callback-based APIs in Promises to prevent callback pyramids and manual error propagation.
- **Promise Error Typing**: Type promises with a single generic `Promise<T>`. Do not attempt to explicitly type the rejection error as `Promise<T, E>`. Because JavaScript allows throwing any value (not just `Error` instances), the `reject` function parameter must be typed as `error: unknown`.
- **Async/Await**: Use `async`/`await` as syntactic sugar over Promises to write sequential-looking asynchronous code. Always wrap `await` calls in `try`/`catch`/`finally` blocks to handle rejections.
- **Typesafe Event Emitters**: Never use untyped Event Emitters. Map event channels to their expected payload types using a central `Events` type (e.g., `type Events = { eventName: [payloadType] }`). Use generic mapped types (`<E extends keyof Events>`) to enforce correct channel names and listener argument types.
- **Typesafe Multithreading (Web Workers / Child Processes)**: Never use raw, untyped `onmessage` or `postMessage` APIs directly in business logic. Always wrap inter-thread communication in a typed abstraction (like a `SafeEmitter` class) or a discriminated union type.
- **Typesafe Protocols**: When performing call-and-response operations across threads, define a strict `Protocol` type mapping commands to `{ in: unknown[], out: unknown }`. Implement a generic wrapper function to enforce these input and output types over the untyped message-passing boundary.
- **Compiler Configuration for Workers**: Ensure the `tsconfig.json` includes `"lib": ["dom", "es2015"]` for the main thread and `"lib": ["webworker", "es2015"]` for Web Worker scripts. For NodeJS child processes, ensure `@types/node` is installed.

# @Workflow
1. **Identify the Asynchronous Pattern**: Determine if the task yields a single future value, a stream of future values, or requires parallel CPU computation.
2. **Single Future Value**: 
   - Wrap legacy callback APIs inside a `new Promise((resolve, reject) => {...})`.
   - Ensure the rejection handles `unknown` error types.
   - Use `async` functions and `await` the Promise, wrapping the operation in a `try`/`catch` block.
3. **Stream of Future Values**:
   - Define an `Events` mapping type specifying all valid event channels and their exact tuple payload types.
   - Create a `SafeEmitter` wrapper class around the native `EventEmitter`, utilizing mapped generics to enforce the `Events` schema on `emit` and `on` methods.
4. **Parallelism (Web Workers / Child Processes)**:
   - For simple message passing: Define `Commands` and `Events` mapping types. Instantiate a `SafeEmitter` for incoming messages and outgoing messages on both sides of the boundary.
   - For call-and-response RPC: Define a `Protocol` type containing `in` (arguments array) and `out` (return type) signatures for every valid command.
   - Write a `createProtocol` factory function that encapsulates the `Worker` or `fork` instantiation, handles the internal `postMessage`/`onmessage` wiring, and exposes a strictly typed Promise-based API.

# @Examples (Do's and Don'ts)

### Asynchronous Sequencing
**[DON'T]** Use raw callbacks to sequence multiple async operations (Callback Pyramid):
```typescript
async1((err1, res1) => {
  if (res1) {
    async2(res1, (err2, res2) => {
      if (res2) {
        async3(res2, (err3, res3) => {
          // Unsafe, manual error handling, hard to sequence
        })
      }
    })
  }
})
```

**[DO]** Use `async`/`await` with Promises and standard `try`/`catch` blocks:
```typescript
async function executeSequentially() {
  try {
    let res1 = await async1Promise()
    let res2 = await async2Promise(res1)
    let res3 = await async3Promise(res2)
    // Safe, readable, automatic error propagation
  } catch (error) {
    console.error(error)
  }
}
```

### Typing Promises
**[DON'T]** Attempt to strictly type the Promise rejection error:
```typescript
// Unsafe assumption: JavaScript can throw strings, arrays, or undefined.
type Executor<T, E extends Error> = (
  resolve: (result: T) => void,
  reject: (error: E) => void
) => void;
```

**[DO]** Type the rejection error as `unknown`:
```typescript
type Executor<T> = (
  resolve: (result: T) => void,
  reject: (error: unknown) => void
) => void;
```

### Event Emitters
**[DON'T]** Use untyped Event Emitters with blind `string` channels and `any` payloads:
```typescript
client.on('reconnecting', params => console.info(params)) // params is implicitly any
client.emit('reconnecting', { wrongPayload: true }) // No compiler error
```

**[DO]** Map events to types and use generics to create a Typesafe Event Emitter:
```typescript
type Events = {
  ready: void
  error: Error
  reconnecting: { attempt: number, delay: number }
}

type SafeClient = {
  on<E extends keyof Events>(event: E, f: (arg: Events[E]) => void): void
  emit<E extends keyof Events>(event: E, arg: Events[E]): void
}

// Compiler catches misspelled events and invalid payloads:
client.on('reconnecting', params => console.info(params.attempt))
```

### Multithreading Message Passing
**[DON'T]** Use raw `onmessage` and `postMessage` switching on arbitrary data:
```typescript
// WorkerScript.ts
onmessage = e => {
  if (e.data.type === 'sendMessageToThread') {
    let message = e.data.data[1] // Unsafe, untyped
  }
}
```

**[DO]** Abstract Web Worker message passing into a typesafe Protocol wrapper:
```typescript
// Define the exact protocol mapping
type MatrixProtocol = {
  determinant: {
    in: [number[][]]
    out: number
  }
}

// Define a generic factory to wrap the untyped boundary
function createProtocol<P>(script: string) {
  return <K extends keyof P>(command: K) => 
    (...args: P[K]['in']) => 
      new Promise<P[K]['out']>((resolve, reject) => {
        let worker = new Worker(script)
        worker.onerror = reject
        worker.onmessage = event => resolve(event.data.data)
        worker.postMessage({ command, args })
      })
}

// Consume safely in the main thread
let runWithMatrixProtocol = createProtocol<MatrixProtocol>('MatrixWorkerScript.js')
let parallelDeterminant = runWithMatrixProtocol('determinant')

// Fully typesafe input and output
parallelDeterminant([[1, 2], [3, 4]]).then(determinant => console.log(determinant))
```