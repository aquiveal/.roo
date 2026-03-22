@Domain
The rules in this document trigger when the AI is tasked with architecting, implementing, or refactoring object structures, component relationships, API bridges, or behavioral augmentations in Node.js. This includes implementing access control (Proxy), dynamically adding functionality to existing objects (Decorator), bridging incompatible interfaces (Adapter), or implementing state observation mechanisms (Change Observer).

@Vocabulary
- **Proxy (Surrogate):** An object that controls access to another object (the subject) while exposing an identical interface.
- **Subject:** The original object being wrapped or controlled by a Proxy or Decorator.
- **Object Composition:** A technique where a new object stores a reference to a subject and manually delegates method calls to it.
- **Object Augmentation (Monkey Patching):** Modifying a subject directly by overriding or adding methods.
- **Trap Methods:** Built-in interception methods (e.g., `get`, `set`, `has`) used inside the handler of an ES2015 `Proxy` object.
- **Lazy Initialization:** Delaying the creation of an expensive object until it is explicitly needed.
- **Change Observer:** A pattern (often implemented via ES2015 `Proxy`) that detects and reacts to property mutations on an object, acting as the foundation of reactive programming.
- **Decorator:** A pattern used to dynamically augment the behavior or interface of an existing object instance at runtime without affecting other instances of the same class.
- **Adapter:** A pattern that wraps an object (the adaptee) to expose its functionality through a different, expected interface.
- **Adaptee:** The original object whose interface is being translated by an Adapter.
- **Level / LevelDB:** A fast, lightweight key-value store optimized for Node.js, supporting binary data, batched writes, and streams.

@Objectives
- Define clear relationships between components to enable flexible and efficient Node.js architectures.
- Seamlessly control access to objects (validation, caching, security, observability) without altering their external interface.
- Dynamically augment object behavior at runtime using the most appropriate implementation strategy (Composition, Augmentation, or ES2015 Proxy).
- Bridge incompatible system interfaces accurately, ensuring that error codes and return types precisely match the target interface's expected contract.
- Safely leverage JavaScript's dynamic nature while avoiding destructive side effects (e.g., unsafe monkey patching of shared state).

@Guidelines
- **Proxy Interface Consistency:** When implementing a Proxy, the AI MUST ensure that the proxy object exposes an interface strictly identical to the subject.
- **Technique Selection (Object Augmentation):** The AI MUST NOT use Object Augmentation (Monkey Patching) if the subject object is shared across multiple components or imported globally. Object Augmentation MUST only be used when the subject exists in a tightly controlled, private scope.
- **Technique Selection (Composition vs. ES2015 Proxy):** The AI MUST use Object Composition rather than the ES2015 `Proxy` object when implementing Lazy Initialization, because the ES2015 `Proxy` requires an already-instantiated target object to wrap.
- **ES2015 Proxy Implementation:** When using the ES2015 `Proxy` object, the AI MUST rely on the default fallback behavior for delegated methods/properties instead of manually re-implementing them.
- **Proxy Context Binding:** When writing trap methods (e.g., `get`) in an ES2015 `Proxy` handler that require access to the proxy target via `this`, the AI MUST use regular `function()` syntax. The AI MUST NOT use arrow functions `() => {}` for these traps, as arrow functions inherit `this` from the lexical scope and will fail to bind to the proxy target.
- **Deprecated Libraries:** When implementing Object Composition, the AI MUST NOT use the deprecated `delegates` npm library to auto-generate delegation methods.
- **Change Observer Implementation:** When tasked with observing an object for state mutations (property assignments), the AI MUST use an ES2015 `Proxy` with a `set` trap rather than an `EventEmitter`.
- **Decorator vs. TC39 Syntax:** When implementing the Decorator design pattern (dynamic runtime augmentation of an object), the AI MUST NOT use the TC39 ECMAScript `@decorator` syntax. The `@decorator` syntax is a compile-time class-level modifier requiring transpilation, whereas the design pattern applies to runtime instances.
- **Adapter Fidelity:** When implementing the Adapter pattern, the AI MUST meticulously replicate the target interface's behaviors, including mimicking specific error structures (e.g., transforming a database missing key error into an `ENOENT` filesystem error with the correct `.code` and `.errno` properties).
- **Nomenclature Flexibility:** The AI MUST NOT unnecessarily over-complicate the naming distinction between Proxy and Decorator in JavaScript. If the intent is access control, treat it as a Proxy; if the intent is adding new methods/behavior, treat it as a Decorator. The implementation techniques are interchangeable.

@Workflow
1. **Analyze the Architectural Requirement:**
   - If the goal is to control access, validate, cache, or observe without changing the interface, select the **Proxy** pattern.
   - If the goal is to add new methods or alter existing behavior of a specific instance at runtime, select the **Decorator** pattern.
   - If the goal is to make an existing API fit into a system expecting a completely different API, select the **Adapter** pattern.
2. **Select the Implementation Strategy (For Proxy/Decorator):**
   - Does the target object creation need to be delayed (Lazy Initialization)? Use **Object Composition**.
   - Do you need to intercept dynamic property access, property deletion, or the `in` operator? Use the **ES2015 Proxy**.
   - Are you modifying a few methods on a strictly isolated, unshared instance for pure pragmatism and performance? Use **Object Augmentation**.
3. **Implement the Pattern:**
   - **For ES2015 Proxy:** Define the `target` and the `handler` object. Implement the necessary traps (`get`, `set`, `has`). Return standard target properties for un-intercepted calls.
   - **For Composition:** Create a new class/factory. Store the subject as an internal variable. Expose the required methods, routing them to the internal subject.
   - **For Adapter:** Define the expected target interface. Internally route the target method arguments to the adaptee's methods. Map the adaptee's return values and specific error objects back to the format expected by the target interface.
4. **Validate Context and Side-effects:**
   - Verify `this` bindings in handler traps.
   - Ensure errors thrown match expected consumer contracts.

@Examples (Do's and Don'ts)

**[DO] Use ES2015 Proxy for non-destructive interception and default delegation:**
```javascript
const safeCalculatorHandler = {
  get: (target, property) => {
    if (property === 'divide') {
      return () => {
        const divisor = target.peekValue()
        if (divisor === 0) {
          throw new Error('Division by 0')
        }
        return target.divide()
      }
    }
    // Automatically delegates all other properties/methods
    return target[property]
  }
}
const safeCalculator = new Proxy(calculator, safeCalculatorHandler)
```

**[DON'T] Use Object Augmentation (Monkey Patching) on shared/global subjects:**
```javascript
// ANTI-PATTERN: Mutating a shared instance affects the entire application
function patchToSafeCalculator(sharedCalculator) {
  const divideOrig = sharedCalculator.divide
  sharedCalculator.divide = () => {
    if (sharedCalculator.peekValue() === 0) throw new Error('Division by 0')
    return divideOrig.apply(sharedCalculator)
  }
  return sharedCalculator
}
```

**[DO] Use regular functions in Proxy traps if `this` binding is required for the target:**
```javascript
const enhancedHandler = {
  get(target, property) {
    if (property === 'add') {
      // Regular function allows contextual binding if needed
      return function add() {
        const addend2 = target.getValue()
        const addend1 = target.getValue()
        const result = addend1 + addend2
        target.putValue(result)
        return result
      }
    }
    return target[property]
  }
}
```

**[DON'T] Use TC39 `@decorator` syntax when the goal is the runtime Decorator pattern in plain Node.js:**
```javascript
// ANTI-PATTERN: This is a compile-time class extension requiring a transpiler, not the runtime Decorator pattern.
@defineElement("my-class")
class C extends HTMLElement {
  @reactive accessor clicked = false;
}
```

**[DO] Replicate exact error structures when implementing the Adapter pattern:**
```javascript
async readFile(filename, options) {
  const value = await db.get(resolve(filename))
  if (typeof value === 'undefined') {
    // Meticulously mimicking the expected `fs` interface error
    const e = new Error(`ENOENT: no such file or directory, open '${filename}'`)
    e.code = 'ENOENT'
    e.errno = 34
    e.path = filename
    throw e
  }
  return value
}
```

**[DON'T] Use an ES2015 Proxy for Lazy Initialization:**
```javascript
// ANTI-PATTERN: Proxy requires the target to already exist, defeating lazy initialization
const expensiveObject = new ExpensiveObject() // Instantiated immediately!
const proxy = new Proxy(expensiveObject, handler)
```

**[DO] Use Object Composition for Lazy Initialization:**
```javascript
class LazyProxy {
  constructor() {
    this.subject = null
  }
  someMethod() {
    if (!this.subject) {
      this.subject = new ExpensiveObject() // Initialized only when needed
    }
    return this.subject.someMethod()
  }
}
```

**[DO] Use a Proxy with a `set` trap to implement a Change Observer:**
```javascript
export function createObservable(target, observer) {
  return new Proxy(target, {
    set(obj, prop, value) {
      if (value !== obj[prop]) {
        const prev = obj[prop]
        obj[prop] = value
        observer({ prop, prev, curr: value })
      }
      return true
    }
  })
}
```