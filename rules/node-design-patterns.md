# Node.js Design Patterns Implementation Rules

## Factory over Classes
**Context:** Classes in JavaScript can be rigid and don't offer true privacy (without `#private` fields). Factory functions provide a flexible mechanism to create objects, enforce encapsulation via closures, and separate instantiation from implementation (Chapter 7).
**Directive:** Prefer Factory functions to create objects, especially when encapsulation or flexible instance creation (e.g., returning different implementations) is needed.

### ❌ Anti-Pattern (What to avoid)
```javascript
// A typical Class structure.
// 'db' is exposed; internal logic is hard to hide completely.
// Callers are bound to 'new DatabaseService', making it harder to swap implementations.
class DatabaseService {
  constructor(connectionString) {
    this.connectionString = connectionString;
    this.db = connect(connectionString);
  }

  query(sql) {
    return this.db.query(sql);
  }
}

const service = new DatabaseService('postgres://...');
```

### ✅ Best Practice (What to do)
```javascript
// A Factory function.
// 'db' is truly private within the closure.
// The factory can return any object that satisfies the interface (duck typing).
function createDatabaseService(connectionString) {
  // Private scope
  const db = connect(connectionString);

  // Public interface
  return {
    query(sql) {
      return db.query(sql);
    },
    // We can conditionally expose methods or return different objects
    // based on the connection string (e.g., MockDB vs RealDB)
  };
}

const service = createDatabaseService('postgres://...');
```

## The Revealing Constructor
**Context:** Sometimes you need to allow an object's internal state to be mutated *only during creation* but remain immutable to consumers afterward. The Revealing Constructor pattern (used by `Promise`) achieves this (Chapter 7).
**Directive:** Use the Revealing Constructor pattern when an object requires complex initialization logic that should be inaccessible after instantiation.

### ❌ Anti-Pattern (What to avoid)
```javascript
// The user can modify the buffer at any time via 'write'.
// This makes the object mutable and potentially thread-unsafe or inconsistent.
class ImmutableBuffer {
  constructor(size) {
    this.buffer = Buffer.alloc(size);
  }

  write(string) {
    this.buffer.write(string);
  }

  read() {
    return this.buffer.toString();
  }
}

const buf = new ImmutableBuffer(10);
buf.write('Hello'); // State can be changed here
buf.write('World'); // ...and changed again here
```

### ✅ Best Practice (What to do)
```javascript
// The 'write' capability is passed ONLY to the executor function.
// Once the constructor finishes, the instance is effectively read-only.
class ImmutableBuffer {
  constructor(size, executor) {
    const buffer = Buffer.alloc(size);
    
    const modifiers = {
      write: (str) => buffer.write(str)
    };

    // The logic to populate the buffer runs now
    executor(modifiers);
    
    // Public interface only exposes read methods
    this.read = () => buffer.toString();
  }
}

const buf = new ImmutableBuffer(10, ({ write }) => {
  write('Hello'); // Mutated only during creation
});
// buf.write('World'); // Error: buf.write is not a function
```

## Dependency Injection
**Context:** Hardcoding dependencies (like `require('./db')` inside a module) makes testing difficult and creates tight coupling. Dependency Injection allows modules to receive their dependencies from the outside (Chapter 7).
**Directive:** Inject dependencies as arguments (Constructor or Factory Injection) rather than importing singletons directly, to improve testability and modularity.

### ❌ Anti-Pattern (What to avoid)
```javascript
// The database dependency is hardcoded.
// To test this, you must mock the module system (e.g., jest.mock).
import db from './db.js';

export class UserService {
  async getUser(id) {
    // Tightly coupled to the specific './db.js' module instance
    return db.query('SELECT * FROM users WHERE id = ?', id);
  }
}
```

### ✅ Best Practice (What to do)
```javascript
// The dependency is injected via the constructor/factory.
// Tests can easily pass a mock database.
export class UserService {
  constructor(db) {
    this.db = db;
  }

  async getUser(id) {
    return this.db.query('SELECT * FROM users WHERE id = ?', id);
  }
}

// Composition Root (wiring everything up)
import { createDb } from './db.js';
const db = createDb();
const userService = new UserService(db);
```

## Proxy for Access Control
**Context:** Modifying objects directly to add logging, validation, or lazy loading is risky (monkey patching). The `Proxy` object allows you to intercept operations cleanly without altering the original object (Chapter 8).
**Directive:** Use `Proxy` to wrap objects for cross-cutting concerns like logging, validation, or lazy initialization, preserving the original object's integrity.

### ❌ Anti-Pattern (What to avoid)
```javascript
// Monkey patching the service to add logging.
// This mutates the original object, which might break other parts of the app.
const service = new DataService();
const originalGetData = service.getData;

service.getData = function(id) {
  console.log(`Fetching ${id}`);
  return originalGetData.call(this, id);
};
```

### ✅ Best Practice (What to do)
```javascript
// Using a Proxy to intercept calls transparently.
// The original 'service' remains untouched.
const service = new DataService();

const loggedService = new Proxy(service, {
  get(target, prop, receiver) {
    if (prop === 'getData') {
      return function(...args) {
        console.log(`Fetching ${args[0]}`);
        return target[prop].apply(this, args);
      };
    }
    return target[prop];
  }
});
```

## Middleware Pattern
**Context:** When a request or data stream needs to pass through multiple independent processing steps (validation, auth, parsing), a monolithic function becomes unmanageable. The Middleware pattern creates a flexible processing pipeline (Chapter 9).
**Directive:** Implement the Middleware pattern for request processing or data pipelines to allow easy plugin registration and separation of concerns.

### ❌ Anti-Pattern (What to avoid)
```javascript
// A monolithic function handling everything.
// Adding a new step (e.g., logging) requires modifying this core function.
function handleRequest(req) {
  if (!req.user) throw new Error('Unauthorized'); // Auth logic
  if (!req.body) throw new Error('No body');      // Validation logic
  
  const data = JSON.parse(req.body);              // Parsing logic
  // ... business logic ...
}
```

### ✅ Best Practice (What to do)
```javascript
// A middleware manager allows dynamic composition of steps.
// 'ZmqMiddlewareManager' from Chapter 9 is a great example.
class MiddlewareManager {
  constructor() {
    this.middlewares = [];
  }

  use(func) {
    this.middlewares.push(func);
  }

  async execute(data) {
    let result = data;
    for (const mw of this.middlewares) {
      result = await mw(result);
    }
    return result;
  }
}

const manager = new MiddlewareManager();
manager.use(async (req) => { /* auth logic */ return req; });
manager.use(async (req) => { /* parsing logic */ return req; });
// ...
```
