# @Domain

This rule file MUST be activated when the user requests the creation of object instantiation logic, complex object construction, module wiring, dependency management, or structural application design in JavaScript or Node.js. It governs the implementation of Creational Design Patterns, specifically Factory, Builder, Revealing Constructor, Singleton, and Dependency Injection.

# @Vocabulary

- **Creational Patterns**: Design patterns addressing problems related to the creation of objects, separating creation logic from implementation.
- **Factory Pattern**: A pattern that decouples object creation from its implementation, encapsulating the creation within a function to provide flexibility, enforce encapsulation via closures, or expose a smaller surface area.
- **Duck Typing**: A technique of recognizing or typing objects based on their external behavior (methods and properties) rather than their actual class type.
- **Encapsulation**: Controlling access to internal details of a component. In JavaScript, enforced through function scopes, closures, private class fields (`#`), WeakMaps, or conventions.
- **Builder Pattern**: A pattern that simplifies the creation of complex objects by providing a fluent interface to set parameters step-by-step, ensuring the final object is in a consistent state.
- **Fluent Interface**: An object-oriented API that relies extensively on method chaining (returning `this`).
- **Configuration Object**: A single object literal used to aggregate multiple arguments to improve constructor readability.
- **Revealing Constructor Pattern**: A JavaScript-specific pattern that reveals private functionality (mutators) only at the moment of the object's creation via an executor function, leaving the resulting object immutable or restricted.
- **Executor Function**: The function passed into a Revealing Constructor that receives the internal modifier methods.
- **Singleton Pattern**: A pattern enforcing the presence of only one instance of a class, centralizing its access.
- **Dependency Hoisting**: The practice of package managers installing a shared version of a dependency at the top-level `node_modules` to avoid duplication.
- **Dependency Injection (DI)**: A pattern where a component's dependencies are provided as input by an external entity (the injector) rather than hardcoded, improving decoupling and testability.
- **Injector**: The external entity, initialization script, or container that retrieves or creates concrete instances of dependencies and passes them into a service.
- **Inversion of Control (IoC)**: Shifting the responsibility of wiring modules to a third-party entity (like a Service Locator or DI Container).

# @Objectives

- Decouple object creation from concrete implementations to allow runtime flexibility and smaller API surface areas.
- Hide internal state and enforce strict encapsulation using closures or private fields within factories or revealing constructors.
- Eliminate constructors with long parameter lists by implementing step-by-step Builder interfaces.
- Guarantee object consistency and validity at creation time.
- Implement immutable or initialize-once objects using the Revealing Constructor pattern.
- Wire application modules using Node.js module caching for simple state sharing, while understanding its limitations across package dependencies.
- Utilize Dependency Injection to eliminate tight coupling, enabling straightforward mocking and component reusability.

# @Guidelines

- **Factory Pattern Implementation**:
  - The AI MUST use a factory function instead of directly exposing classes with the `new` operator when the instantiation logic depends on environmental variables (e.g., `NODE_ENV`) or requires conditional type returning.
  - The AI MUST utilize closures within factory functions to enforce strict encapsulation of private variables when classes are not strictly required.
  - The AI SHOULD expose only the factory function and keep internal classes private/unexported to maintain a small surface area.
  - The AI MUST apply duck typing to return different internal implementations seamlessly as long as they share the same public interface (e.g., returning a mock/noop object vs. a real functional object).

- **Builder Pattern Implementation**:
  - The AI MUST NOT define constructors with more than three parameters. If an object requires complex configuration, the AI MUST implement a Builder class.
  - The AI MUST return `this` in all setter methods of a Builder to enforce a fluent interface.
  - The AI SHOULD aggregate related parameters into single setter methods (e.g., `setAuthentication(username, password)` instead of separate setters) to enforce proper usage.
  - The AI MUST implement a final `build()` (or `invoke()`) method that validates the collected parameters and constructs the target object or executes the target function in a guaranteed consistent state.
  - The AI MUST separate the Builder from the target class to ensure that the target class can never be accessed in an incomplete or invalid state.

- **Revealing Constructor Pattern Implementation**:
  - The AI MUST use the Revealing Constructor pattern when an object requires internal mutability *only* during its initialization phase (e.g., creating custom immutable buffers, event emitters with locked event definitions, or promises).
  - The AI MUST construct the pattern by accepting an `executor` function as an argument in the constructor.
  - The AI MUST pass modifier/mutator methods as arguments to the `executor` function inside the constructor.
  - The AI MUST expose only read-only methods on the public instance of the class.

- **Singleton Pattern Implementation**:
  - The AI MUST achieve singletons in Node.js by exporting a pre-instantiated object from a module, relying on the Node.js module caching mechanism.
  - The AI MUST acknowledge the dependency tree caveat: if different packages use different versions of a module, Node.js will cache multiple instances.
  - The AI MUST NOT use the `global` object to store singletons unless an absolute, cross-package singleton is unconditionally required, and dependency hoisting cannot be guaranteed.
  - The AI SHOULD export stateless packages for third-party libraries to prevent Singleton fragmentation issues.

- **Dependency Injection (DI) Implementation**:
  - The AI MUST NOT hardcode `import` statements of stateful dependencies (e.g., database connections) directly inside a module's business logic if the module requires high testability or dynamic configuration.
  - The AI MUST implement DI by passing dependencies into the module via constructor arguments, function arguments, or property assignment.
  - The AI MUST define an external "injector" (an index or initialization script) responsible for instantiating dependencies and passing them into the dependent services.

# @Workflow

1. **Analyze the Instantiation Requirement**: Determine the complexity, statefulness, and lifecycle of the object or module being created.
2. **Apply Factory for Abstraction**: If the client does not need to know the specific class being instantiated, or if you must toggle implementations based on the environment (e.g., testing vs. production), implement a Factory function.
3. **Apply Builder for Complexity**: If the class requires numerous parameters, replace the constructor parameters with a configuration object. For stricter validation and step-by-step construction, create a standalone `[Name]Builder` class with fluent setter methods and a terminal `build()` method.
4. **Apply Revealing Constructor for Immutability**: If the object must be immutable after creation, define a constructor taking an `executor`. Isolate mutating methods, pass them into the `executor`, and assign only safe, read-only methods to `this`.
5. **Determine Module Wiring Strategy**: 
   - For simple, tightly-coupled internal state sharing, instantiate the class in a module and `export const instance = new ClassName()`.
   - For modules that require testing with mock databases/services, or need to be highly reusable, apply Dependency Injection by refactoring the class to accept its dependencies as constructor arguments.
6. **Construct the Injector**: If using DI, create a top-level script that instantiates the dependencies (e.g., `db`), instantiates the services, and explicitly injects the dependencies into the services.

# @Examples (Do's and Don'ts)

## Factory Pattern
- **[DO]** Use a factory to decouple creation and enforce closure-based encapsulation:
  ```javascript
  function createPerson(name) {
    const privateProperties = {};
    const person = {
      setName(newName) {
        if (!newName) throw new Error('Name cannot be empty');
        privateProperties.name = newName;
      },
      getName() {
        return privateProperties.name;
      }
    };
    person.setName(name);
    return person;
  }
  ```
- **[DON'T]** Expose classes that rely on environment checks inside their methods when a factory could swap the implementation seamlessly:
  ```javascript
  // Anti-pattern: Hardcoded environment checks inside the class
  class Profiler {
    start() {
      if (process.env.NODE_ENV === 'production') return; 
      this.lastTime = process.hrtime();
    }
  }
  ```

## Builder Pattern
- **[DO]** Create a separate builder with fluent interfaces and grouped logic:
  ```javascript
  export class UrlBuilder {
    setProtocol(protocol) {
      this.protocol = protocol;
      return this;
    }
    setAuthentication(username, password) {
      this.username = username;
      this.password = password;
      return this;
    }
    build() {
      if (!this.protocol) throw new Error('Protocol required');
      return new Url(this.protocol, this.username, this.password);
    }
  }
  ```
- **[DON'T]** Use mega-constructors that require null-padding and break readability:
  ```javascript
  // Anti-pattern: Mega-constructor
  const url = new Url('https', null, null, 'example.com', null, null, null, null);
  ```

## Revealing Constructor Pattern
- **[DO]** Reveal mutators only through the executor:
  ```javascript
  export class ImmutableBuffer {
    constructor(size, executor) {
      const buffer = Buffer.alloc(size);
      const modifiers = {
        write: buffer.write.bind(buffer)
      };
      this.readInt8 = buffer.readInt8.bind(buffer);
      executor(modifiers);
    }
  }
  ```
- **[DON'T]** Add mutating methods to the class instance and rely on convention to prevent modification:
  ```javascript
  // Anti-pattern: Mutable instance that should be immutable
  export class ImmutableBuffer {
    constructor(size) {
      this.buffer = Buffer.alloc(size);
    }
    _write(data) { // Can still be easily accessed from the outside
      this.buffer.write(data);
    }
  }
  ```

## Singleton Pattern
- **[DO]** Export an initialized instance for a simple app-wide singleton:
  ```javascript
  // dbInstance.js
  import { Database } from './Database.js';
  export const dbInstance = new Database('my-app-db');
  ```
- **[DON'T]** Assume a cached module is a perfect singleton if your package might be required across different versions in `node_modules` (dependency tree duplication).

## Dependency Injection (DI)
- **[DO]** Pass dependencies into the constructor, decoupling the module:
  ```javascript
  // blog.js
  export class Blog {
    constructor(db) {
      this.db = db;
    }
    getPosts() {
      return this.db.query('SELECT * FROM posts');
    }
  }
  // injector.js
  const db = createDb('data.sqlite');
  const blog = new Blog(db);
  ```
- **[DON'T]** Hardcode module imports inside the class making it impossible to inject a mock during testing:
  ```javascript
  // Anti-pattern: Tight coupling
  import { db } from './db.js';
  export class Blog {
    getPosts() {
      return db.query('SELECT * FROM posts');
    }
  }
  ```