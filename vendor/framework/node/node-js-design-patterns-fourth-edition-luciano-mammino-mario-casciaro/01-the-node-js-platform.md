# @Domain
These rules MUST be activated when the AI is tasked with designing, architecting, or writing Node.js applications, modules, or services. This includes scenarios involving I/O performance optimization, module structuring, asynchronous event handling, TypeScript setup for Node.js, and deciding between core versus third-party dependencies.

# @Vocabulary
- **The "Node way"**: The overarching philosophy guiding Node.js development, characterized by a small core, small modules, small surface area, and pragmatism.
- **Userland / Userspace**: The ecosystem of third-party modules available outside the Node.js core (e.g., the npm registry).
- **Small Core**: The principle of keeping Node.js built-in modules minimal, though recently expanded to include standard web APIs (fetch, WebSockets) and tooling (test runner).
- **Unix Philosophy**: The architectural principle dictating that programs should be small and "do one thing well."
- **Dependency Hell**: A problem solved by Node.js package managers by allowing multiple versions of the same package to be installed in nested `node_modules` trees to prevent conflicts.
- **DRY (Don't Repeat Yourself)**: A principle applied aggressively in Node.js, enabling packages to comprise even a single, focused function.
- **Small Surface Area**: The practice of exposing only a minimal set of functionalities (often just a single function or class) from a module to prevent erroneous usage and reduce maintenance.
- **KISS (Keep It Simple, Stupid) / Worse is Better**: The principle of favoring simple implementations and interfaces over mathematically perfect, complex object-oriented class hierarchies.
- **Blocking I/O**: Operations that block the execution of the thread until the operation completes (e.g., traditional multithreaded server approaches).
- **Non-blocking I/O**: Operations that return immediately without waiting for data, returning a predefined constant if data is unavailable.
- **Busy-waiting**: An inefficient polling technique where a thread actively loops to check if non-blocking resources are ready.
- **Synchronous Event Demultiplexer**: A native OS mechanism (epoll, kqueue, IOCP) that monitors multiple resources and blocks until events (read/write readiness) are available.
- **Reactor Pattern**: The core mechanism of Node.js where I/O operations are submitted to a demultiplexer with a handler (callback); upon completion, events are queued and processed by an event loop.
- **libuv**: The C library serving as the low-level I/O engine of Node.js, responsible for abstracting the OS-specific demultiplexers and implementing the reactor pattern.
- **V8**: The JavaScript engine (originally developed for Chrome) that executes the code, acclaimed for its speed and efficient memory management.
- **Node-API**: The official interface for binding Node.js userland modules to native compiled code (C/C++/Rust).
- **WebAssembly (Wasm)**: A low-level instruction format allowing compilation of non-JavaScript languages into a format executable by JavaScript VMs without native bindings.
- **Transpiler / Polyfill**: Tools used to convert modern code or inject missing features into older environments; largely unnecessary in Node.js due to known runtime targets.
- **Loaders**: Mechanisms (like `tsx`) that intercept and modify module loading, enabling on-the-fly execution of TypeScript.

# @Objectives
- The AI MUST design software that strictly adheres to the "Node way," prioritizing small, hyper-focused modules over monolithic codebases.
- The AI MUST implement non-blocking, event-driven architectures that efficiently manage I/O bottlenecks without relying on synchronous thread-blocking operations.
- The AI MUST define clear, minimalistic boundaries for all modules, exposing only what is absolutely necessary.
- The AI MUST favor simple, pragmatic JavaScript patterns (closures, pure functions) over complex, deeply nested object-oriented class abstractions.
- The AI MUST ensure that TypeScript configurations and native bindings are optimized for the specific Node.js runtime target.

# @Guidelines

## Architectural Philosophy constraints
- **Rule**: The AI MUST enforce the Unix Philosophy. When generating a module, it MUST execute exactly one responsibility. If a module performs multiple unrelated tasks, the AI MUST split it into smaller modules.
- **Rule**: The AI MUST restrict module surface area. A module MUST export a single, unmistakably clear entry point (preferably a single function or a simple class) whenever possible.
- **Rule**: The AI MUST design modules to be used, not extended. Internals MUST be locked down and hidden from the outside world.
- **Rule**: The AI MUST prioritize pragmatism. The AI SHALL NOT use complex Object-Oriented patterns (like deep inheritance, Abstract Factories, or intricate Decorators) if a simple function or closure can achieve a functional approximation with manageable complexity.

## Execution and I/O constraints
- **Rule**: The AI MUST treat I/O (Disk, Network, RAM access) as the primary system bottleneck and NEVER use blocking I/O calls (e.g., `readFileSync`, blocking socket reads) in a concurrent server context.
- **Rule**: The AI MUST rely exclusively on the Reactor Pattern for concurrency. Code MUST express interest in a resource without blocking, provide a handler (callback/promise), and immediately return control to the Event Loop.
- **Rule**: The AI MUST recognize that Node.js is single-threaded for the event loop, but SHALL NOT assume it cannot leverage background threads. The AI MUST delegate heavy CPU-bound workloads to worker threads to prevent blocking the event loop.

## Platform and Ecosystem constraints
- **Rule**: The AI MUST utilize built-in core modules for common interfaces (e.g., parsing CLI arguments, WebSockets, standard web fetch API, native test runner) before suggesting third-party userland modules, reflecting modern Node.js capabilities.
- **Rule**: The AI MUST evaluate the necessity of third-party dependencies meticulously to mitigate supply chain vulnerabilities. If a simple one-liner or native core module achieves the task, the AI MUST avoid adding an external dependency.
- **Rule**: The AI MUST NOT use DOM APIs (`window`, `document`) as they do not exist in Node.js.
- **Rule**: The AI MUST utilize the `process` global strictly for process-level data (e.g., `process.env` for environment variables, `process.argv` for CLI arguments).

## Node.js & TypeScript compatibility constraints
- **Rule**: When generating `package.json`, the AI MUST specify the `engines` field targeting a specific Node.js LTS release (e.g., Node.js 24) to guarantee execution environment predictability.
- **Rule**: When writing TypeScript for Node.js, the AI MUST include `@types/node` as a development dependency to ensure proper static analysis of Node.js-specific globals and APIs.
- **Rule**: The AI MUST utilize `tsx` as a loader or execution tool for on-the-fly TypeScript execution in development environments, OR utilize Node.js 24+ built-in type stripping (for erasable syntax only), acknowledging that type-stripping ignores `tsconfig.json`.
- **Rule**: The AI MUST ensure TypeScript is pre-transpiled before production deployment to avoid the performance penalty of runtime transpilation.

# @Workflow
When instructed to build a Node.js component, the AI MUST strictly follow this sequence:
1. **Analyze the Workload**: Determine if the task is I/O-bound (network/disk) or CPU-bound. If I/O-bound, prepare a non-blocking Reactor-pattern structure. If CPU-bound, prepare to offload to native code (Wasm/Node-API) or worker threads.
2. **Decompose to Minimal Scope**: Break down the requested feature until each file/module does exactly one thing well (Unix philosophy).
3. **Design the Interface**: Define a single, small surface area export for the module (a single function or simple class). Do not expose internal workings.
4. **Draft the Logic**: Implement the logic using pragmatic, simple JavaScript constructs (closures, flat structures) over mathematical OOP modeling. 
5. **Enforce Non-blocking Execution**: Ensure all network and filesystem access is handled asynchronously, yielding control back to the event loop immediately.
6. **Configure the Environment**: Ensure target Node.js version is specified in `package.json` (`engines`) and development tools (`@types/node`, `tsx`) are appropriately structured.

# @Examples (Do's and Don'ts)

## Module Surface Area & Pragmatism
[DO]
```javascript
// is-sorted.js
// Exposes a single, focused function. Internals are hidden. Pragmatic and simple.
export default function isSorted(array) {
  for (let i = 1; i < array.length; i++) {
    if (array[i - 1] > array[i]) return false;
  }
  return true;
}
```

[DON'T]
```javascript
// Over-engineered, violates KISS, exposes too much surface area, meant for extension rather than use.
export class ArraySorterInterface {
  check() { throw new Error('Not implemented'); }
}
export class AbstractArrayValidator extends ArraySorterInterface {
  constructor(array) { 
    super();
    this.array = array; 
  }
}
export class SortedArrayValidator extends AbstractArrayValidator {
  check() {
    // complex validation logic
  }
}
```

## I/O and Concurrency
[DO]
```javascript
// Leverages non-blocking I/O and the Reactor Pattern
import { readFile } from 'node:fs/promises';

async function processFile(filePath) {
  try {
    // Non-blocking call, returns control to the event loop
    const data = await readFile(filePath, 'utf8');
    console.log('File processing complete:', data.length);
  } catch (err) {
    console.error('Error reading file:', err);
  }
}
```

[DON'T]
```javascript
// Violates Node.js philosophy by blocking the main event loop thread
import { readFileSync } from 'node:fs';

function processFile(filePath) {
  // Blocks the thread until the data is available. No other connections can be processed.
  const data = readFileSync(filePath, 'utf8');
  console.log('File processing complete:', data.length);
}
```

## TypeScript Execution in Node.js
[DO]
```json
// package.json utilizing modern tools and specifying engines
{
  "name": "my-pragmatic-node-app",
  "version": "1.0.0",
  "type": "module",
  "engines": {
    "node": ">=24.0.0"
  },
  "scripts": {
    "dev": "node --import=tsx src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "devDependencies": {
    "@types/node": "^24.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0"
  }
}
```

[DON'T]
```json
// Fails to lock engines, executes TypeScript in production without pre-compiling
{
  "name": "my-slow-node-app",
  "version": "1.0.0",
  "scripts": {
    "start": "ts-node src/index.ts"
  }
}
```