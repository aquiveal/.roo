# @Domain
These rules MUST trigger whenever the AI is tasked with writing tests, debugging code, profiling Node.js applications, analyzing memory/CPU usage, or setting up/modifying test frameworks (including native `assert`, `vm`, Mocha, Chai, Sinon, Nightmare, or Puppeteer).

# @Vocabulary
- **Unit Test**: A fast, isolated test evaluating a single, small set of code paths (e.g., a single function). Ignores external dependencies and application state.
- **Functional Test**: A test validating a piece of functionality combining multiple units (e.g., logging in a user). Abstract models of product needs, often using mock contexts.
- **Integration Test**: A test ensuring the entire system is wired correctly. Runs in a realistic environment with actual domain data, servers, and distributed filesystems.
- **Strict Equality / Identity (`===`)**: Comparison without type coercion. Enforced by `assert.strictEqual`.
- **Deep Equality**: Comparison of object shape (same keys and equivalent values), not strict object identity. Enforced by `assert.deepEqual`.
- **Execution Context**: The runtime environment within V8. Delineated in the `vm` module between local scope, global scope, and sandboxed scope.
- **Spy**: A Sinon function that records arguments, return values, `this` context, and exceptions for all its calls, without altering the original function's behavior.
- **Stub**: A Sinon spy with preprogrammed behavior (e.g., forcing an HTTP 404 response). Prevents the original function from executing.
- **Mock**: A Sinon fake method with preprogrammed behavior AND preprogrammed expectations (e.g., must be called exactly 5 times).
- **Headless Browser**: A scriptable browser environment without a GUI, used for UI automation (e.g., Nightmare, Puppeteer).
- **V8 Profiling**: Generating runtime logs of V8 compilation and execution ticks using the `--prof` flag.
- **Heap Snapshot**: A memory dump (`.heapsnapshot`) recording V8 memory allocation, generated via the `heapdump` module for tracking memory leaks.

# @Objectives
- Implement robust, multi-layered testing strategies (Unit, Functional, Integration) with clear boundaries.
- Utilize native Node.js debugging (`node inspect`), profiling (`--prof`), and inspector (`--inspect`) tools for performance analysis.
- Prevent test pollution and memory leaks through rigid setup/teardown lifecycles and context isolation.
- Enforce predictable asynchronous control flows in testing via Promises, `async/await`, and accurate `done()` callbacks.
- Ensure all function definitions are traceable in CPU profiles by avoiding anonymous functions.

# @Guidelines

### Native Debugging & Console
- The AI MUST use `console.error` to print to `stderr` and `console.dir(Object)` to run `util.inspect` and write to `stdout`.
- When tracking execution time, the AI MUST use `console.time('label')` and `console.timeEnd('label')` with the EXACT same string label.
- When formatting strings, the AI MUST use `util.format` with `%s` (string), `%d` (number), or `%j` (JSON).
- When logging deeply nested or hidden objects, the AI MUST use `util.inspect(obj, { showHidden: true, depth: null, colors: true })`.
- When setting breakpoints in code, the AI MUST insert the `debugger;` directive and instruct the user to run the script via `node inspect <script>`.

### Assertions (`assert` module)
- The AI MUST prefer `assert.strictEqual` over `assert.equal` to prevent unintended type coercion (e.g., `1 == "1"`).
- When comparing objects or arrays, the AI MUST use `assert.deepEqual` to validate shape rather than instance identity.
- The AI MUST pass an explicit failure message as the final argument to assert functions for better error readability.
- The AI MUST use `assert.fail(actual, expected, message, operator)` within `try/catch` blocks to trap execution paths that should never be reached.

### Sandboxing (`vm` module)
- When executing untrusted code or strictly isolating test scopes, the AI MUST use `vm.runInNewContext(code, sandbox)`.
- When executing code that requires access to global Node variables but isolated local variables, the AI MUST use `vm.runInThisContext(code)`.
- When executing the same script multiple times, the AI MUST compile it first using `new vm.Script(code)` and run it via `script.runInNewContext(sandbox)` to optimize V8 compilation.

### Mocha & Chai
- The AI MUST organize tests using nested `describe` blocks for domains/components and `it` blocks for specific assertions.
- The AI MUST use `before`, `beforeEach`, `after`, and `afterEach` hooks to set up and tear down test states.
- For asynchronous Mocha tests, the AI MUST either return a Promise or invoke the `done(err)` callback precisely once.
- When configuring Chai, the AI MUST enable stack traces via `chai.config.includeStack = true`.
- The AI MUST use Chai's `expect` BDD syntax (e.g., `expect(x).to.be.a('string').and.equal('foo')`).

### Test Doubles (Sinon)
- The AI MUST use Spies (`sinon.spy()`) when the objective is solely to verify how a function was called (`calledOnce`, `calledWith`) without altering its execution.
- The AI MUST use Stubs (`sinon.stub().yields()` or `.returns()`) to fake responses (e.g., API failures, HTTP 404) and prevent network I/O during unit tests.
- The AI MUST use Mocks (`sinon.mock().expects().exactly(n)`) when the test's purpose is to strictly verify the implementation contract.
- The AI MUST call `mock.verify()` at the end of a mock test.
- The AI MUST ALWAYS call `.restore()` on any spy, stub, or mock within an `afterEach` or `after` hook to prevent test pollution.

### Headless Browser Testing
- When using **Nightmare**, the AI MUST chain Promises natively, instantiate within `beforeEach`, and MUST ALWAYS call `nightmare.end(done)` in `afterEach`.
- To reuse logic in Nightmare, the AI MUST define custom actions via `Nightmare.action('name', function)`. Inside the action, the AI MUST use `this.evaluate_now()` to prevent queuing issues.
- When using **Puppeteer**, the AI MUST use `async/await` syntax.
- When capturing screenshots in Puppeteer, the AI MUST optimize rendering by intercepting and aborting image requests via `page.setRequestInterception(true)` and `request.abort()` if images are not strictly required for the test.

### Profiling and Memory
- The AI MUST name ALL functions (e.g., `function $myFunction()`) to ensure they appear clearly in V8 profiler logs. Avoid anonymous functions.
- To generate a CPU profile, the AI MUST instruct the user to run `node --prof <script>` followed by `node --prof-process <isolate-log> > profile.txt`.
- To generate a heap snapshot, the AI MUST implement `require('heapdump').writeSnapshot(<path>)` and instruct the user to load the `.heapsnapshot` file into Chrome DevTools Memory tab.
- To live debug or profile CPU/Memory via Chrome DevTools, the AI MUST instruct the user to start the process with `node --inspect <script>` and navigate to `chrome://inspect`.

# @Workflow
1. **Determine Test Scope**: Classify the request as a Unit Test (needs mocks/stubs), Functional Test (needs composition models), or Integration Test (needs live environment).
2. **Environment Setup**: Initialize the Mocha `describe` block. Declare variables in the outer scope.
3. **Lifecycle Management**: Implement `beforeEach` to instantiate objects, inject Sinon spies/stubs/mocks, or launch headless browsers.
4. **Execution & Assertion**: Write the `it` block. Execute the target method. Use `expect` syntax for validation or `mock.verify()`. Ensure async tests resolve via `done()` or returning a Promise.
5. **Teardown**: Implement `afterEach` to call `.restore()` on Sinon objects and `.end()`/`.close()` on headless browsers.
6. **Profiling (If requested)**: Convert all anonymous functions to named functions prefixed with `$` (e.g., `$streamHandler`). Inject `heapdump` or prepare `--inspect` commands.

# @Examples (Do's and Don'ts)

### 1. Timing Execution
- **[DO]**
  ```javascript
  console.time('DB_Query');
  // ... execution ...
  console.timeEnd('DB_Query');
  ```
- **[DON'T]** Use mismatched labels.
  ```javascript
  console.time('DB_Query');
  // ... execution ...
  console.timeEnd('DB_Query_Done'); // Fails to resolve the timer
  ```

### 2. Equality Assertions
- **[DO]** Use strict equality to avoid coercion bugs.
  ```javascript
  assert.strictEqual(actual, "1", "Values must be strictly equal");
  assert.deepEqual(objA, objB, "Object shapes must match");
  ```
- **[DON'T]** Use loose equality.
  ```javascript
  assert.equal(actual, 1); // Passes for "1" == 1, hiding type errors
  ```

### 3. Sinon Cleanup
- **[DO]** Restore stubbed methods in teardown hooks.
  ```javascript
  describe('API calls', () => {
    afterEach(() => {
      http.get.restore();
    });
    it('handles 404', (done) => {
      sinon.stub(http, 'get').yields({ statusCode: 404 });
      // ...test...
    });
  });
  ```
- **[DON'T]** Leave stubs active, which poisons subsequent tests.
  ```javascript
  it('handles 404', () => {
    sinon.stub(http, 'get').yields({ statusCode: 404 });
    // test finishes, http.get remains permanently stubbed!
  });
  ```

### 4. VM Script Compilation
- **[DO]** Precompile scripts when running in a loop.
  ```javascript
  const script = new vm.Script('++x;');
  const context = vm.createContext({ x: 0 });
  for (let i = 0; i < 1000; i++) {
    script.runInNewContext(context);
  }
  ```
- **[DON'T]** Pass raw strings inside a loop, forcing recompilation.
  ```javascript
  const context = { x: 0 };
  for (let i = 0; i < 1000; i++) {
    vm.runInNewContext('++x;', context); // Severe performance penalty
  }
  ```

### 5. Function Naming for Profiling
- **[DO]** Use named functions for clear V8 `--prof` traces.
  ```javascript
  lineReader._transform = function $transform(chunk, encoding, done) { ... };
  ```
- **[DON'T]** Use anonymous functions.
  ```javascript
  lineReader._transform = function(chunk, encoding, done) { ... }; // Appears as <anonymous> in V8 logs
  ```

### 6. Puppeteer Optimization
- **[DO]** Abort image requests to speed up headless tests.
  ```javascript
  await page.setRequestInterception(true);
  page.on('request', request => {
    if (request.resourceType() === 'image') request.abort();
    else request.continue();
  });
  ```
- **[DON'T]** Load full media assets during functional DOM testing unless explicitly testing visual rendering.