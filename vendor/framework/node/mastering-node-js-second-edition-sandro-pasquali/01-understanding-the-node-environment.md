@Domain
Node.js systems programming, V8 JavaScript engine optimization, high-concurrency network application architecture, non-blocking I/O handling, and CommonJS module composition. Activate these rules whenever writing or refactoring server-side JavaScript, structuring Node.js applications, or optimizing code for the V8 engine.

@Vocabulary
- **POSIX**: Portable Operating System Interface; the standard Unix APIs that Node.js wrappers emulate for familiarity.
- **Event Loop**: Node's single-threaded control flow mechanism that manages deferred tasks and callbacks.
- **libuv**: The C library underlying Node.js that creates and manages the event loop, thread pools, and asynchronous OS-level I/O operations.
- **V8**: Google's JavaScript engine written in C++ that compiles JavaScript into native machine code using a two-stage speculative optimization process.
- **Full Compiler**: V8's first-pass compiler that executes JavaScript immediately without type analysis.
- **Optimizing Compiler**: V8's secondary compiler that monitors running code, makes assumptions about types based on hot execution paths, and recompiles code for high performance.
- **De-optimization**: The rollback process triggered when V8's type assumptions are violated (e.g., variable type changes), heavily penalizing performance.
- **Hidden Classes**: Internal V8 blueprints created to track object types and properties for memory allocation and fast access.
- **Sparse Arrays**: Arrays with gaps in their indices; forces V8 to use slow hash table storage instead of efficient linear storage.
- **Polymorphic Functions**: Functions that accept varying argument types or counts; breaks V8 optimization.
- **SemVer**: Semantic Versioning (Major.Minor.Patch) used in `package.json` for dependency management.
- **REPL**: Read-Eval-Print-Loop; the interactive Node shell, which can also be programmaticly embedded into networked servers.
- **CommonJS**: The module specification used by Node.js (`require()`, `module.exports`).

@Objectives
- Transform JavaScript from a high-level web scripting language into a robust, high-performance systems language.
- Implement the Unix Design Philosophy: build small, simple, encapsulated modules that do one thing well and communicate via text streams.
- Strictly adhere to V8 speculative optimization rules by maintaining absolute type predictability across numbers, arrays, objects, and functions.
- Eliminate blocking operations entirely; utilize Node's event-driven, asynchronous I/O abstractions.
- Leverage modern JavaScript (ES6+) constructs to create concise, declarative, and easily maintainable code.
- Offload expensive CPU operations to parallel processes, reserving the main Node thread strictly for I/O and event routing.

@Guidelines

- **Unix Philosophy & Architecture**
  - Favor simplicity over complexity.
  - Assemble complex programs from simpler, reusable packages.
  - Handle data using evented text streams; favor text over binary formats.
  - Use familiar POSIX-like APIs provided by Node's standard libraries.
  - Never block the event loop. A waiting process is a wasteful process.

- **V8 Speculative Optimization: Numbers**
  - Use 31-bit signed integers where possible, as V8 optimizes for this internal size.
  - NEVER switch the numeric type of a variable after initialization. Assigning a float to a variable that previously held an integer forces a compiler de-optimization bailout.

- **V8 Speculative Optimization: Arrays**
  - Maintain consistent data types within arrays (e.g., all integers or all strings). Do not mix types.
  - Start all arrays at index zero (`0`).
  - Do not create Sparse Arrays. Never leave gaps in array indices.
  - NEVER use the `delete` keyword on an array element; this inserts an `undefined` value and creates a sparse array, forcing V8 to use slow hash-table storage.
  - Avoid preallocating large arrays. Grow arrays dynamically as you go. If you must preallocate, NEVER exceed the preallocated size.
  - Prevent incomplete external data from populating arrays with empty values.

- **V8 Speculative Optimization: Objects**
  - Define the shape of data structures in a future-proof manner.
  - Initialize all members in constructor functions.
  - Initialize properties in the EXACT SAME ORDER for every instance. (Same properties + same order = same hidden class).
  - DO NOT add properties to an object after it has been instantiated. This destroys the hidden class blueprint and forces V8 to rebuild it.

- **V8 Speculative Optimization: Functions**
  - Avoid polymorphic functions. Ensure functions are called with consistent argument types and counts.
  - Keep `try-catch` blocks out of frequently called (hot) functions, as they are not optimizable by V8.
  - Do not use unpredictable constructs like `with` or `eval`.

- **Modern JavaScript (ES6+) Usage**
  - Use `util.promisify` to seamlessly convert core Node callback-based API functions into Promise-based functions.
  - Use `const` by default for variables that do not change (aids compiler optimization). Use `let` for block-scoped mutation. Never use `var`.
  - Use array and object Destructuring to map structures directly to variables.
  - Use Rest parameters (`...args`) instead of the legacy `arguments` object to avoid V8 de-optimization.
  - Use the Spread operator (`...`) to cleanly merge arrays or expand iterable objects.
  - Use Arrow Functions (`() => {}`) to preserve lexical `this` context, especially within callbacks and timers.
  - Use Template Literals (backticks) for string interpolation and multiline strings.
  - Use `for...of` loops or the spread operator to iterate over strings instead of legacy character-parsing logic.
  - Use modern string search methods: `startsWith`, `endsWith`, and `includes`.

- **Events and Streams**
  - Implement I/O operations as asynchronous, evented data streams.
  - Use `events.EventEmitter` to build asynchronous interfaces for object methods.
  - Use `.pipe()` to seamlessly connect Readable streams to Writable streams.

- **Modules and Ecosystem**
  - Encapsulate code into CommonJS modules.
  - Respect SemVer strictly when publishing or consuming packages.
  - Treat packages as directories containing a `package.json` file.

@Workflow
1. **Analyze Requirements**: Determine if the task is I/O-bound (network, file system) or CPU-bound.
2. **Task Delegation**: Route I/O tasks through Node.js native asynchronous event APIs. If the task is heavily CPU-bound, spawn separate child processes to prevent blocking the event loop.
3. **Data Shape Definition**: Define precise object and array structures upfront. Establish exact initialization orders for constructors to satisfy V8 Hidden Class rules.
4. **Implementation**:
   - Write logic using modern ES6+ (arrow functions, template literals, destructuring).
   - Promisify legacy callback APIs.
   - Attach event listeners (`.on()`) for stream processing.
5. **Optimization Check**: Review the code specifically for V8 anti-patterns (mixed array types, late object property additions, variable type switching, `arguments` object usage).
6. **Modularization**: Export clean interfaces via `module.exports`.

@Examples (Do's and Don'ts)

**V8 Object Initialization**
- [DO]: Initialize all properties in the constructor in a strict order.
  ```javascript
  function User(name, age) {
    this.name = name;
    this.age = age;
    this.isActive = true;
  }
  const u1 = new User("Alice", 30);
  const u2 = new User("Bob", 25);
  ```
- [DON'T]: Add properties after instantiation or initialize in varying orders.
  ```javascript
  const u1 = new User("Alice", 30);
  u1.isActive = true; // DE-OPTIMIZED: Alters hidden class after instantiation

  function UserBad(name, age, type) {
    if (type === 'admin') {
      this.role = 'admin';
      this.name = name;
    } else {
      this.name = name;
      this.role = 'user'; // DE-OPTIMIZED: Properties initialized in different order
    }
  }
  ```

**V8 Array Management**
- [DO]: Keep types consistent and push sequentially.
  ```javascript
  let arr = [1, 2, 3];
  arr.push(4);
  ```
- [DON'T]: Create sparse arrays, mix types, or use `delete`.
  ```javascript
  let arr = [];
  arr[2] = 'foo'; // DE-OPTIMIZED: Creates a sparse array
  arr[3] = 42;    // DE-OPTIMIZED: Mixes types (string and number)
  delete arr[3];  // DE-OPTIMIZED: Inserts undefined, makes array sparse
  ```

**V8 Number Variables**
- [DO]: Keep number types strictly consistent.
  ```javascript
  let a = 7;
  a = 8; // OK: Remains an integer
  ```
- [DON'T]: Switch a numeric variable from an integer to a float.
  ```javascript
  let a = 7;
  a = 7.77; // DE-OPTIMIZED: V8 speculated integer, forced to roll back
  ```

**Handling Function Arguments**
- [DO]: Use ES6 Rest parameters for variable arguments.
  ```javascript
  function process(a, b, ...args) {
    // args is a true Array, safe and optimizable
    args.forEach(arg => console.log(arg));
  }
  ```
- [DON'T]: Slice the legacy `arguments` object.
  ```javascript
  function process(a, b) {
    // DE-OPTIMIZED: Interacting with 'arguments' object in this way kills V8 optimization
    let args = Array.prototype.slice.call(arguments, 2);
  }
  ```

**Converting Callbacks to Promises**
- [DO]: Use `util.promisify` for clean asynchronous flows.
  ```javascript
  const { promisify } = require('util');
  const fs = require('fs');
  const readFileAsync = promisify(fs.readFile);

  readFileAsync('target.txt', { encoding: 'utf8' })
    .then(console.log)
    .catch(err => console.error(err));
  ```
- [DON'T]: Deeply nest manual callbacks (Callback Hell).
  ```javascript
  const fs = require('fs');
  fs.readFile('target.txt', { encoding: 'utf8' }, (err, data) => {
    if (err) {
      console.error(err);
    } else {
      console.log(data);
    }
  });
  ```

**Context Tracking (Lexical `this`)**
- [DO]: Use Arrow functions to automatically bind lexical scope.
  ```javascript
  setInterval(() => {
    console.log(this.count++); // `this` is correctly inherited
  }, 1000);
  ```
- [DON'T]: Use standard functions inside callbacks expecting outer context.
  ```javascript
  setInterval(function() {
    console.log(this.count++); // FAILS: `this` points to the Timeout object
  }, 1000);
  ```