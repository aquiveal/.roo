# @Domain

Trigger these rules when the user requests assistance with designing, refactoring, or implementing object behaviors, algorithmic variations, state-driven logic, data iteration, processing pipelines, or deferred execution tasks in JavaScript, TypeScript, or Node.js. This includes implementing any of the following Behavioral Design Patterns: Strategy, State, Template, Iterator (including Generators and Async Iterators), Middleware, or Command.

# @Vocabulary

*   **Context**: The object that delegates a specific part of its logic to an interchangeable underlying strategy or state object.
*   **Strategy**: An interchangeable object encapsulating a specific variation of an algorithm expected by a Context.
*   **State (Pattern)**: A specialization of Strategy where the strategy object dynamically changes during the lifetime of the Context based on internal status transitions.
*   **Template Method**: An undefined or throwing method within an abstract base class (the "skeleton") that must be implemented by concrete subclasses.
*   **Iterator Protocol**: A standardized JavaScript interface for producing a sequence of values, requiring a `next()` method that returns an object with `done` (boolean) and `value` properties.
*   **Iterable Protocol**: A protocol defining that an object must return an Iterator when its `[Symbol.iterator]()` (or `[Symbol.asyncIterator]()`) method is called.
*   **Generator**: A semicoroutine function declared with `function*` that can pause and resume its execution using the `yield` keyword. It returns an object that is both an Iterator and an Iterable.
*   **Generator Delegation**: The `yield* iterable` syntax used to seamlessly flatten or delegate iteration to a nested iterable.
*   **Async Iterator**: An iterator whose `next()` method returns a Promise that resolves to the `{ done, value }` object. Consumed using `for await...of`.
*   **Middleware**: Processing units (functions/objects) organized in a pipeline to perform preprocessing and postprocessing of data.
*   **Command**: An object encapsulating all the information necessary to perform an action at a later time (contains `run`, `undo`, and `serialize` methods).
*   **Task Pattern**: The simplest implementation of a Command, using a closure or bound function to delay execution without complex object structures.
*   **Invoker**: The component responsible for executing, tracking, delaying, or reverting a Command.
*   **Target (Receiver)**: The subject or service upon which the Command invokes its operations.

# @Objectives

*   Adapt object behavior dynamically without cluttering components with complex `if...else` or `switch` statements.
*   Enforce structured, reusable algorithmic skeletons while delegating specific implementation details to subclasses.
*   Decouple the implementation of data traversal algorithms from the consumption of the traversed data using native JavaScript iteration protocols.
*   Prevent memory exhaustion and CPU bottlenecks when processing large datasets by favoring lazy evaluation (Iterators) over eager evaluation (Arrays).
*   Implement highly decoupled, plugin-like data processing pipelines using the Middleware pattern.
*   Materialize function invocations into objects (Commands) to support delayed execution, serialization, remote execution, and undo capabilities.

# @Guidelines

### 1. Strategy Pattern Rules
*   The AI MUST extract variable algorithmic logic into distinct, interchangeable Strategy objects.
*   The AI MUST ensure all Strategies within a family implement the exact same interface/signature.
*   The Context MUST dynamically accept a Strategy (e.g., via constructor injection or parameter) rather than hardcoding conditionals.

### 2. State Pattern Rules
*   The AI MUST use the State pattern when an object's behavior fundamentally changes based on its internal state.
*   The Context MUST delegate the execution of state-dependent methods to a current State object.
*   State transitions MUST be handled by reassigning the Context's active State object (e.g., `this.currentState = new OnlineState(this)`).
*   When transitioning states, the AI MUST gracefully flush or migrate any queued data or pending actions accumulated in the previous state.

### 3. Template Pattern Rules
*   The AI MUST define the common skeleton of an algorithm in a base class.
*   In plain JavaScript, the AI MUST stub abstract Template Methods to throw a runtime error (e.g., `throw new Error('methodName() must be implemented')`) to enforce implementation by subclasses.
*   The AI MUST prefix protected Template Methods with an underscore (`_`) to signify they are for internal/subclass use only.
*   In TypeScript, the AI MUST use the `abstract` keyword for the base class and the template methods.

### 4. Iterator & Iterable Protocol Rules
*   When creating an Iterator, the AI MUST return an object with a `next()` method yielding `{ done: boolean, value: any }`.
*   The AI MUST implement the Iterable protocol by defining a `[Symbol.iterator]()` method.
*   The AI MUST implement BOTH protocols simultaneously on custom iterators by adding `[Symbol.iterator]() { return this; }`. This ensures interoperability with native syntax like `for...of` and spread `[...]` operators.

### 5. Generator Rules
*   The AI MUST favor Generators (`function*`) over custom stateful closures when implementing complex Iterators, utilizing local variables which inherently preserve state between `yield` reentries.
*   The AI MUST use Generator Delegation (`yield*`) to avoid nested loops when an Iterator traverses nested iterable data structures (e.g., `yield* array.flat()`).
*   The AI MUST handle two-way communication in Generators appropriately when the consumer calls `next(value)`, assigning the injected value from the `yield` statement.

### 6. Lazy Evaluation vs. Eager Evaluation Rules
*   The AI MUST strictly AVOID using eager Array methods (`Array.map()`, `Array.filter()`) when processing large or infinite datasets, as they create memory-intensive intermediate arrays.
*   The AI MUST utilize the Iterator prototype (`Iterator.from(iterable).filter(...).map(...)`) to enforce lazy evaluation. Computations MUST only run when the consumer explicitly pulls values.

### 7. Async Iterators & Async Generators Rules
*   The AI MUST use `[Symbol.asyncIterator]()` and return Promises from `next()` when iteration requires asynchronous operations (e.g., HTTP requests, database fetches).
*   The AI MUST use `async function*` for defining Async Generators, yielding values normally while allowing `await` inside the generator body.
*   The AI MUST use `for await...of` to consume Async Iterables.

### 8. Middleware Pattern Rules
*   The AI MUST implement a Middleware Manager to organize and execute a pipeline of functions sequentially.
*   The AI MUST support asynchronous middleware execution (e.g., `await middlewareFunc(data)`).
*   For bidirectional data flow (e.g., ZeroMQ inbound/outbound), the AI MUST ensure inbound middleware is appended (pushed) and outbound middleware is prepended (unshifted) to maintain inverted execution order.

### 9. Command Pattern Rules
*   For simple delayed execution, the AI MUST use the Task Pattern (a closure or `.bind()`).
*   For complex requirements (undo, serialization, remote execution), the AI MUST construct explicit Command objects containing `run()`, `undo()`, and `serialize()` methods.
*   The AI MUST delegate Command execution to an Invoker component, which tracks history for undo operations or manages scheduling.

# @Workflow

When instructed to implement a Behavioral Design Pattern, the AI MUST follow this algorithmic process:

1.  **Analyze the Intent**:
    *   If the goal is to swap algorithms without changing the caller -> **Strategy**.
    *   If the goal is to alter behavior based on lifecycle status -> **State**.
    *   If the goal is to reuse a core algorithm structure but vary specific steps -> **Template**.
    *   If the goal is to traverse a dataset sequentially -> **Iterator / Generator**.
    *   If the goal is to process data sequentially through plugins -> **Middleware**.
    *   If the goal is to queue, undo, or serialize an invocation -> **Command**.
2.  **Define the Interface**: Establish the strict contract (methods, properties, or protocols) that the interchangeable components must adhere to.
3.  **Implement the Context/Manager**: Create the host object that holds the state, manages the pipeline, or tracks the history.
4.  **Implement the Behaviors**: Create the concrete Strategies, States, Template subclasses, Middleware functions, or Command objects.
5.  **Refine for Node.js/JS Idioms**: Apply JavaScript-specific optimizations:
    *   Use `[Symbol.iterator]` or `[Symbol.asyncIterator]`.
    *   Use `function*` or `async function*`.
    *   Leverage `Iterator.from()` for lazy evaluation.
    *   Implement Duck Typing where explicit interfaces do not exist.
6.  **Verify Interoperability**: Ensure iterators work with `for...of`, async functions correctly `await` middleware, and commands successfully separate invocation from execution.

# @Examples (Do's and Don'ts)

### Strategy Pattern
**[DO]** Pass the strategy to the context to abstract the implementation:
```javascript
export class Config {
  constructor(formatStrategy) {
    this.formatStrategy = formatStrategy;
  }
  async load(filePath) {
    this.data = this.formatStrategy.deserialize(await readFile(filePath, 'utf-8'));
  }
}
const jsonStrategy = { deserialize: JSON.parse, serialize: (data) => JSON.stringify(data) };
```

**[DON'T]** Hardcode conditional logic inside the context:
```javascript
export class Config {
  async load(filePath, format) {
    const data = await readFile(filePath, 'utf-8');
    if (format === 'json') this.data = JSON.parse(data);
    else if (format === 'yaml') this.data = YAML.parse(data);
  }
}
```

### Template Pattern
**[DO]** Define a skeleton and explicitly throw errors in missing template methods:
```javascript
export class ConfigTemplate {
  async save(file) {
    await writeFile(file, this._serialize(this.data));
  }
  _serialize() {
    throw new Error('_serialize() must be implemented');
  }
}
```

**[DON'T]** Leave template methods completely undefined without throwing, which leads to silent failures, or mix subclass logic into the base class.

### Iterator Protocol
**[DO]** Return `this` in the `[Symbol.iterator]` to make an iterator iterable:
```javascript
function createIterator() {
  let count = 0;
  return {
    next() {
      if (count >= 5) return { done: true };
      return { done: false, value: count++ };
    },
    [Symbol.iterator]() { return this; }
  };
}
```

**[DON'T]** Create an iterator that lacks the `[Symbol.iterator]` method, as it will crash when used with `for...of` or the spread operator `[...]`.

### Generators & Delegation
**[DO]** Use `yield*` to seamlessly delegate to a nested iterable:
```javascript
class Matrix {
  constructor(data) { this.data = data; }
  *[Symbol.iterator]() {
    yield* this.data.flat();
  }
}
```

**[DON'T]** Write nested loops manually when `yield*` and `.flat()` can handle delegation cleanly.

### Lazy Evaluation (Iterator Helpers)
**[DO]** Use `Iterator.from()` to lazily evaluate large datasets:
```javascript
const doubledEvenIt = Iterator.from(largeDataset)
  .filter(n => n % 2 === 0)
  .map(n => n * 2);
```

**[DON'T]** Use eager Array methods on large datasets, causing massive intermediate arrays and high memory consumption:
```javascript
const doubledEvenArray = largeDataset
  .filter(n => n % 2 === 0)
  .map(n => n * 2);
```

### Async Iterators
**[DO]** Use `async function*` to handle async resolution during iteration:
```javascript
async function* checkUrls(urls) {
  for (const url of urls) {
    const res = await fetch(url);
    yield `${url} status: ${res.status}`;
  }
}
for await (const status of checkUrls(myUrls)) {
  console.log(status);
}
```

**[DON'T]** Use synchronous generators or synchronous `for...of` loops when the yielded results require awaiting asynchronous I/O.

### Command Pattern
**[DO]** Encapsulate context and arguments into an object with standardized `run`, `undo`, and `serialize` methods for complex operations:
```javascript
export function createPostStatusCmd(service, status) {
  let postId = null;
  return {
    run() { postId = service.postUpdate(status); },
    undo() { if (postId) service.destroyUpdate(postId); },
    serialize() { return { type: 'status', action: 'post', status }; }
  };
}
```

**[DON'T]** Pass unstructured functions to a delayed invoker if the system requires reversibility (undo) or network transmission (serialization).