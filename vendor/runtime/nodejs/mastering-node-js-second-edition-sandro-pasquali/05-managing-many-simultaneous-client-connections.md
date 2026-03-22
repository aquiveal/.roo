# @Domain
Trigger these rules when tasked with designing, refactoring, or managing high-concurrency Node.js network applications, configuring Express routing, implementing session and state management (especially with Redis), designing long-polling communication, or implementing authentication mechanisms including Basic Authentication, Challenge-Response Handshakes, and JSON Web Tokens (JWT).

# @Vocabulary
*   **C10K Problem**: The architectural challenge of confidently and efficiently serving 10,000 simultaneous clients on a single server without degrading performance.
*   **Concurrency**: The structural organization of a program to manage multiple simultaneous operations, allowing developers to reason about non-deterministic control flow explicitly. Concurrency is not parallelism; its goal is good structure.
*   **Parallelism**: The act of executing multiple computations simultaneously across multiple workers or CPU cores (managed in Node by libuv/OS, not directly by the JavaScript thread).
*   **Routes**: URL patterns mapped to specific actions or functions, translating URLs into simple statements of intent (e.g., `GET /listCities/:country/:state`).
*   **Middleware**: Functions in frameworks like Express that chain request-handling routines together, allowing sequential processing (e.g., validating authentication before reaching the data layer).
*   **Redis**: An in-memory Key/Value (KV) database used for lightning-fast reads/writes, session tracking, and Publish/Subscribe (pub/sub) messaging.
*   **Session**: A continuous transactional chain between a client and server, maintaining context across multiple stateless HTTP requests, often tracked via cookies.
*   **Long Polling**: A communication technique where the server holds a client's request connection open until data is available, reducing the redundant network chatter associated with short polling.
*   **Basic Authentication**: A standard HTTP authentication protocol sending credentials as a base64-encoded string. Inherently insecure unless passed over an encrypted HTTPS connection.
*   **Challenge-Response Handshake**: An authentication method preventing plain-text password transmission. The server sends a generated public key (challenge), and the client returns a hashed response (e.g., SHA256 of key + password).
*   **Key Expiry (TTL)**: Time To Live. A feature utilized in Redis via the `setex` command to ensure keys (like authentication challenges) automatically self-destruct after a set number of seconds.
*   **JSON Web Token (JWT)**: A stateless, base64-encoded authentication token consisting of a header, claims, and signature. Eliminates the need for a centralized session database.
*   **Claims (JWT)**: Embedded security definitions in a JWT, such as `iss` (issuer), `aud` (audience), `sub` (subject), `iat` (issued-at time), and `exp` (expiration time).

# @Objectives
*   Design high-concurrency architectures that leverage Node's single-threaded event loop for structural simplicity while relying on the system kernel/libuv for I/O efficiency.
*   Implement clean, expressive, and dynamic HTTP routing using the Express framework and middleware chains.
*   Maintain rapid, stateless server architectures by offloading user session state and data caching to Redis.
*   Facilitate real-time or near-real-time communication for concurrent clients using long-polling combined with Redis pub/sub channels.
*   Implement secure, context-appropriate authentication strategies (Basic Auth over HTTPS, Challenge-Response for non-HTTPS, or JWT for stateless distributed systems).

# @Guidelines
*   **Concurrency Strategy**: Write structured, single-threaded code. Rely on Node's asynchronous event loop to handle high concurrency. Never use synchronous, blocking I/O operations in request handlers, as this forces all concurrent clients to wait.
*   **Routing Design**: Define URLs as semantic expressions of intent rather than filesystem paths. Extract variables directly from the route path using Express parameter syntax (e.g., `:id`).
*   **Middleware Chaining**: Isolate discrete business logic (like user validation or logging) into reusable middleware functions. Pass control to the next handler using `next()`.
*   **In-Memory State Management**: For high-volume concurrent environments, track user state, session IDs, and active connections using Redis instead of traditional file-backed relational databases. Use `hset`, `hgetall`, and `hmset` for managing complex user objects.
*   **Long-Polling Implementation**:
    *   Assign a unique session ID to each client (e.g., via a randomly generated cookie).
    *   Store the unresolved Express `response` object in a memory dictionary indexed by the session ID.
    *   Use a Redis `subscribe` client to listen for global data updates.
    *   Upon receiving a Redis message, iterate through the stored connection dictionary, send the data to the clients, and explicitly end the response.
*   **Basic Authentication**: Always check for the `authorization` header. If absent, respond with a `401` status code and the `WWW-Authenticate: Basic realm="..."` header to trigger the browser's native login dialog. Parse the base64 string to extract the `username:password` pair.
*   **Challenge-Response Security**: When generating an authentication challenge, store the challenge hash in Redis using `setex` (e.g., `client.setex(challenge, 5, username)`). This ensures the challenge is only valid for a strict, short time window (e.g., 5 seconds), mitigating replay attacks and preventing stale data buildup.
*   **JWT Implementation Constraints**:
    *   Do not maintain a session store for JWTs. The token acts as the absolute source of access rights.
    *   Always define `iss`, `aud`, `sub`, `iat`, and `exp` claims.
    *   Ensure custom session data within the JWT payload is manually encrypted if it contains sensitive information, as base64 encoding is easily decoded.
    *   Always calculate the current time in seconds (`Math.floor(Date.now()/1000)`) and explicitly reject the request if the current time exceeds the decoded JWT's `exp` claim.

# @Workflow
1.  **Architecture Initialization**: Instantiate an Express server to handle HTTP requests and route definitions.
2.  **State & Messaging Setup**: Connect to a Redis instance. If implementing live data broadcasts, create two separate Redis clients: one for standard KV storage/publishing (`createClient()`) and one exclusively for subscribing (`createClient().subscribe()`).
3.  **Authentication Layer Routing**:
    *   *For JWT*: Create a `/login` POST route. Validate credentials against the database. If valid, generate a token using a secret key, appending expiration (`exp`) and audience (`aud`) claims. Return the token.
    *   *For Protected Routes*: Implement a middleware function that extracts the `Authorization: Bearer <token>` header, decodes the JWT, verifies the signature, and checks `exp` against the current epoch time.
4.  **API Route Definition**: Map application functionality to Express routes using parameterized URLs (`app.get('/resource/:id', handler)`).
5.  **Connection Holding (Long Polling)**: In the data-fetching route, extract the user's session ID from their cookies. Save the `response` object to a local `connections` dictionary and leave the request pending.
6.  **Event Broadcasting**: In the Redis `message` event listener, loop through the `connections` dictionary, write the updated payload to every active `response` object, call `end()`, and remove the connection from the dictionary.

# @Examples (Do's and Don'ts)

**Routing with Express**
*   [DO] Use parameterized routes to capture variables elegantly.
```javascript
app.get('/listCities/:country/:state', (request, response) => {
    let country = request.params.country;
    let state = request.params.state;
    // Query DB and return response
});
```
*   [DON'T] Hardcode individual routes for every possible data combination.
```javascript
// Anti-pattern
if (url === "/listCities/usa/ohio") { ... }
if (url === "/listCities/usa/arizona") { ... }
```

**Managing Authentication Challenges in Redis**
*   [DO] Use `setex` to assign a Time-To-Live (TTL) to authentication challenges, automatically cleaning up unanswered challenges.
```javascript
let challenge = crypto.createHash('sha256').update(publicKey + data.password).digest('hex');
// Set key to expire in 5 seconds
client.setex(challenge, 5, username);
response.end(challenge);
```
*   [DON'T] Use standard `set` without an expiration mechanism, causing memory bloat if clients abandon the handshake.
```javascript
// Anti-pattern
client.set(challenge, username);
```

**Implementing Basic Authentication**
*   [DO] Prompt the client browser to ask for credentials by returning the correct 401 headers.
```javascript
let auth = req.headers['authorization'];
if(!auth) {
    res.writeHead(401, {'WWW-Authenticate': 'Basic realm="Secure Area"'});
    return res.end('<html><body>Please enter some credentials.</body></html>');
}
// Decode base64 auth header...
```
*   [DON'T] Try to implement Basic Authentication over standard HTTP in a production environment (always use HTTPS to encrypt the base64 string).

**Handling JSON Web Tokens (JWT)**
*   [DO] Always verify the token's expiration time manually against the current server time in seconds.
```javascript
app.post('/tokendata', function(req, res) {
    let token = req.get('Authorization').replace('Bearer ', '');
    let decoded = jwt.decode(token, app.get('jwtSecret'));
    
    let now = Math.floor(Date.now() / 1000);
    if(now > decoded.exp) {
        return res.end(JSON.stringify({ error : "Token expired" }));
    }
    res.send(decoded);
});
```
*   [DON'T] Trust the JWT blindly just because it decoded successfully.

**Long-Polling State Management**
*   [DO] Store open response connections by session ID and resolve them via a Redis Pub/Sub listener.
```javascript
let connections = {};

app.get('/poll', (request, response) => {
    let id = request.cookies.node_poll_id;
    if(id) connections[id] = response; // Hold connection open
});

receiver.on("message", (channel, message) => {
    for(let conn in connections) {
        connections[conn].end(message);
    }
});
```
*   [DON'T] Use a blocking `while` loop to wait for data, which completely freezes the Node event loop and prevents handling other clients.