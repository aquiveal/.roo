# Node.js Module System & Architecture Rules

## Named Exports over Default
**Context:** Named exports provide explicit contracts, better IDE refactoring support, and avoid "magic" import names. Default exports can lead to inconsistency and are harder to statically analyze (Chapter 2).
**Directive:** ALWAYS prefer Named Exports for modules; avoid Default Exports unless mandated by a framework or specific compatibility requirement.

### ❌ Anti-Pattern (What to avoid)
```javascript
// logger.js
// Default export makes it unclear what is being exported without reading docs.
// Consumers can rename this arbitrarily (e.g., import Foo from './logger').
export default class Logger {
  log(msg) { console.log(msg); }
}

// app.js
import MyLogThing from './logger.js'; // Ambiguous naming
```

### ✅ Best Practice (What to do)
```javascript
// logger.js
// Explicit export. The consumer must import { Logger }.
export class Logger {
  log(msg) { console.log(msg); }
}

export function createLogger() {
  return new Logger();
}

// app.js
// Clear intent. IDE auto-imports work perfectly.
import { Logger, createLogger } from './logger.js';
```

## Small Surface Area
**Context:** Modules that expose their internal implementation details are brittle and hard to refactor. A small surface area (exposing only what is necessary) promotes loose coupling and information hiding (Chapter 2).
**Directive:** Expose only the minimal necessary interface (functions/classes) from a module; keep implementation details private or internal.

### ❌ Anti-Pattern (What to avoid)
```javascript
// user-service.js
// Exposing internal constants and helpers that the consumer shouldn't rely on.
export const DB_TABLE = 'users'; // Internal detail leaked
export function validateEmail(email) { /* ... */ } // Internal helper leaked

export class UserService {
  constructor() {
    this.table = DB_TABLE;
  }
  // ...
}
```

### ✅ Best Practice (What to do)
```javascript
// user-service.js
// Internal details are not exported.
const DB_TABLE = 'users';

function validateEmail(email) { 
  // ... implementation ...
}

// Only the primary public interface is exported.
export class UserService {
  async createUser(email) {
    if (!validateEmail(email)) throw new Error('Invalid email');
    // ... logic ...
  }
}
```

## Async Initialization
**Context:** Some modules (like database clients) require asynchronous setup (connection). Exporting a Promise or using a queue prevents race conditions where the module is used before it's ready (Chapter 11).
**Directive:** Handle asynchronous module initialization explicitly, either by exporting a `init()` function, using Top-Level Await (in ESM), or using pre-initialization queues.

### ❌ Anti-Pattern (What to avoid)
```javascript
// db.js
import { MongoClient } from 'mongodb';

const client = new MongoClient(process.env.MONGO_URI);
let db;

// Fire-and-forget connection.
// If 'db' is imported and used immediately, it might be undefined.
client.connect().then(() => {
  db = client.db('my_db');
});

export { db }; // EXPORTING UNDEFINED INITIALLY!
```

### ✅ Best Practice (What to do)
```javascript
// db.js
// Using Top-Level Await (ESM) to ensure the module is ready before usage.
import { MongoClient } from 'mongodb';

const client = new MongoClient(process.env.MONGO_URI);

// The module import will block until connection is established.
// Consumers are guaranteed a connected client.
await client.connect();
const db = client.db('my_db');

export { db };

// ALTERNATIVE (Factory Pattern):
// export async function getDb() { ... }
```

## Core Module Prefixes
**Context:** Node.js has moved to using the `node:` protocol for core modules. This makes imports unambiguous (distinguishing core modules from npm packages of the same name) and is now the standard (Chapter 2).
**Directive:** ALWAYS use the `node:` prefix when importing Node.js built-in modules (e.g., `node:fs`, `node:path`, `node:http`).

### ❌ Anti-Pattern (What to avoid)
```javascript
// Ambiguous. Is 'fs' the core module or a package named 'fs' in node_modules?
import fs from 'fs';
import path from 'path';

const data = fs.readFileSync(path.join(__dirname, 'file.txt'));
```

### ✅ Best Practice (What to do)
```javascript
// Explicit and future-proof.
// Clearly indicates these are Node.js built-ins.
import fs from 'node:fs';
import path from 'node:path';
import { createServer } from 'node:http';

// Or for specific submodules
import { readFile } from 'node:fs/promises';
```
