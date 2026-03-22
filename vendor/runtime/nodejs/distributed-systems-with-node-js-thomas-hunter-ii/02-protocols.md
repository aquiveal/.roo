# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, implementing, refactoring, or reviewing network protocols, APIs (REST, GraphQL, gRPC), inter-service communication, payload serialization, HTTP server configurations (including TLS and compression), or schema definitions in a Node.js distributed systems environment.

# @Vocabulary
- **OSI Model**: A conceptual framework for network communication. Layer 4 (Transport) handles TCP/UDP delivery guarantees. Layer 7 (Application) handles HTTP. Layer 8 (User) conceptually represents payload formats like JSON or gRPC.
- **Idempotency**: An operation that can be executed multiple times without risk of unintended side effects (e.g., HTTP GET, PATCH, DELETE).
- **Statelessness**: A communication protocol where every request contains all the information needed to set the desired state, without relying on retained server-side session data.
- **Marshalling**: The process of explicitly controlling how an in-memory object is serialized into a format (like JSON) using dedicated methods (e.g., `toJSON()`) to prevent the leakage of private properties.
- **POJO (Plain Ol' JavaScript Object)**: A basic JavaScript object without explicit methods or prototype chains, highly dangerous when serialized directly due to potential data leakage.
- **Facade Service**: A GraphQL pattern where a single service sits in front of multiple other backend services and data sources, hydrating a combined response.
- **Protocol Buffers (Protobufs)**: A binary serialization format used by gRPC that requires a predefined `.proto` schema file and explicitly numbered fields for backward compatibility and reduced payload size.
- **RPC (Remote Procedure Call)**: A pattern where code on one service remotely calls methods on another service as if the methods existed locally.
- **Root Certificate / Chain of Trust**: A cryptographic hierarchy where one certificate vouches for (signs) another. Used for secure inter-service TLS communication.

# @Objectives
- The AI MUST enforce strict adherence to industry-standard protocols (HTTP, GraphQL, gRPC) rather than inventing custom communication formats.
- The AI MUST rigorously protect internal application state and secrets by explicitly marshalling all outbound data structures.
- The AI MUST optimize system performance by utilizing the most efficient protocol for the task and advocating for the offloading of CPU-intensive network tasks (Compression, TLS) to external reverse proxies.
- The AI MUST ensure robust error handling and network resilience by respecting HTTP status code semantics and maintaining strict backward compatibility in RPC schemas.

# @Guidelines

## General HTTP & REST API Architecture
- When designing HTTP APIs, the AI MUST strictly map CRUD operations to HTTP methods: `POST` (Create), `GET` (Read), `PATCH` (Update), and `DELETE` (Delete).
- The AI MUST treat `GET`, `PATCH`, and `DELETE` as idempotent operations.
- The AI MUST return correct HTTP status code ranges:
  - `100-199`: Information
  - `200-299`: Success
  - `300-399`: Redirect
  - `400-499`: Client error (Client MUST NOT retry identical requests).
  - `500-599`: Server error (Client MAY retry idempotent requests).
- The AI MUST NOT implement stateful sessions (e.g., cookies tracking server-side state) in API design. All requests MUST contain required state/authentication information.

## Payload Serialization & Marshalling
- When serializing data for HTTP responses, the AI MUST NEVER pass raw POJOs directly to a response framework (e.g., `res.send(pojo)` or `JSON.stringify(pojo)`).
- The AI MUST define domain entities as ES6 Classes containing a `toJSON()` method that explicitly maps and returns only the safe, public fields (Marshalling).

## Compression & TLS Encryption
- When tasked with adding compression (gzip/brotli) or TLS (HTTPS) to a Node.js process, the AI MUST add a warning comment indicating that Node.js is inefficient at these CPU-heavy tasks and advocate for a Reverse Proxy (e.g., HAProxy).
- If implementing TLS for inter-service communication locally or internally, the AI MUST explicitly generate and load a custom Root CA certificate.
- The AI MUST NEVER use `rejectUnauthorized: false` to bypass self-signed certificate errors. It MUST instead provide the CA certificate to the client using an `https.Agent` with the `ca` option.

## GraphQL Implementations
- When generating GraphQL schemas (`.gql`), the AI MUST explicitly use standard scalars (`Int`, `Float`, `String`, `Boolean`, `ID`).
- The AI MUST use the `!` modifier to denote required fields where appropriate.
- When generating GraphQL clients, the AI MUST NOT use string concatenation to insert dynamic data into queries. The AI MUST use GraphQL query variables (e.g., `query($id: ID)` and pass a `variables` object).
- When implementing GraphQL Resolvers, the AI MUST ensure that resolver function signatures correctly match the query hierarchy, taking advantage of parallel asynchronous data fetching.

## gRPC & Protocol Buffers
- When generating a `.proto` file, the AI MUST use `syntax = "proto3";`.
- The AI MUST assign a unique integer to EVERY field (e.g., `int32 id = 1;`).
- The AI MUST NOT reorder, remove, or re-number existing Protocol Buffer fields to guarantee backward compatibility.
- The AI MUST use appropriate gRPC scalars (`double`, `float`, `int32`, `int64`, `bool`, `string`, `bytes`) and use `repeated` for arrays.
- When writing a Node.js gRPC client using `@grpc/grpc-js`, the AI MUST wrap callback-based client methods using `util.promisify` to allow `async/await` usage.

# @Workflow
When tasked with implementing or interacting with a distributed network service, the AI MUST follow this exact sequence:

1. **Protocol Selection & Schema Definition**:
   - For public-facing endpoints: Default to JSON over HTTP or GraphQL.
   - For internal microservice-to-microservice communication: Default to gRPC/Protobufs.
   - Define the explicit schema (`.gql` file, `.proto` file, or API interface class with `toJSON()`).
2. **Server/Producer Implementation**:
   - Instantiate the server using the designated framework (e.g., `fastify`, `@grpc/grpc-js`).
   - Implement the route handlers or resolvers.
   - If JSON over HTTP, wrap returned data in instances of classes utilizing the `toJSON()` marshalling pattern.
3. **Client/Consumer Implementation**:
   - Instantiate the client (`node-fetch` for HTTP/GraphQL, `@grpc/grpc-js` for gRPC).
   - If GraphQL, extract dynamic query inputs into the `variables` payload.
   - If gRPC, promisify the remote procedure calls.
4. **Security & Configuration Application**:
   - If TLS is required, read the certificate and private key from the filesystem. Apply the internal CA cert to the client's `https.Agent`. Ensure no `rejectUnauthorized: false` shortcuts exist.

# @Examples (Do's and Don'ts)

## Serialization and Marshalling
**[DO]** Use a Class with a `toJSON()` method to prevent leaking private properties.
```javascript
class User {
  constructor(username, email, password) {
    this.username = username;
    this.email = email;
    this.password = password; // Private internal state
  }
  toJSON() {
    return {
      username: this.username,
      email: this.email,
    };
  }
}
const user = new User('alice', 'alice@example.org', 'hunter2');
res.send(user); // Password safely omitted
```

**[DON'T]** Use raw POJOs that risk leaking sensitive data when the object structure is mutated.
```javascript
const user = { username: 'alice', email: 'alice@example.org' };
user.password = 'hunter2'; // Accidentally added deep in the codebase
res.send(user); // FATAL: Password leaked to the consumer
```

## Internal TLS Verification
**[DO]** Load the specific self-signed Certificate Authority (CA) so the client natively trusts the internal server.
```javascript
const https = require('https');
const fs = require('fs');
const fetch = require('node-fetch');

const options = {
  agent: new https.Agent({
    ca: fs.readFileSync(__dirname + '/../shared/tls/ca-certificate.cert')
  })
};
const req = await fetch(`https://internal-service:4000/data`, options);
```

**[DON'T]** Disable unauthorized certificate rejection.
```javascript
const https = require('https');
const fetch = require('node-fetch');

const options = {
  agent: new https.Agent({
    rejectUnauthorized: false // FATAL: Defeats the entire purpose of TLS validation
  })
};
const req = await fetch(`https://internal-service:4000/data`, options);
```

## GraphQL Client Queries
**[DO]** Use GraphQL variables for dynamic data.
```javascript
const complex_query = `query kitchenSink ($id: ID) {
  recipe(id: $id) { name }
}`;

const req = await fetch(`http://target/graphql`, {
  method: 'POST',
  body: JSON.stringify({
    query: complex_query,
    variables: { id: "42" }
  })
});
```

**[DON'T]** Use string concatenation or template literals to inject variables directly into the query string.
```javascript
const id = "42";
const complex_query = `query kitchenSink {
  recipe(id: ${id}) { name } // ANTI-PATTERN: Prone to injection and caching failures
}`;
```

## gRPC Protocol Buffers Definition
**[DO]** Assign explicit, immutable integer tags to fields.
```protobuf
syntax = "proto3";
package recipe;

message Ingredient {
  int32 id = 1;
  string name = 2;
  string quantity = 3;
}
```

**[DON'T]** Leave fields unnumbered or rely on implicit ordering.
```protobuf
syntax = "proto3";
package recipe;

message Ingredient {
  int32 id; // FATAL: Missing integer tag required for binary ordering
  string name;
}
```