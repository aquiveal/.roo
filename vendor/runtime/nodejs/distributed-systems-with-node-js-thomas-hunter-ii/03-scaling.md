@Domain
Trigger these rules when tasked with scaling Node.js applications, configuring high availability (HA), setting up load balancers or reverse proxies (specifically HAProxy), implementing health checks, managing connection limits/back pressure, or benchmarking and load-testing Node.js services (using tools like Autocannon).

@Vocabulary
- **High Availability (HA)**: The ability of a system to remain accessible to consumers even if individual processes or machines crash, achieved by running redundant copies of a service.
- **Throughput**: The volume of requests an application can handle, typically measured in requests per second (r/s). 
- **Cluster Module**: A built-in Node.js module that allows running multiple copies of a Node.js application on the same machine, dispatching incoming network messages to the copies.
- **Master Process**: In the context of the cluster module, the coordinating process that listens on ports and routes requests to worker processes.
- **Worker Process**: The child processes spawned by the master process that execute the actual application logic.
- **Reverse Proxy**: A tool (e.g., HAProxy) that accepts requests from a client, forwards them to one of several servers, and returns the response to the client. Operates at Layer 4 (TCP) or Layer 7 (HTTP).
- **Load Balancing**: The act of distributing incoming network traffic across multiple backend services (e.g., round-robin, least connections, sticky sessions).
- **Health Check**: A routine endpoint poll (e.g., `GET /health`) performed by a reverse proxy to determine if a backend service is healthy. Unhealthy services are removed from the routing pool.
- **Compression Offloading**: Moving CPU-intensive compression (like gzip) out of the Node.js process and into a reverse proxy.
- **TLS Termination**: Offloading the CPU-intensive encryption/decryption of HTTPS traffic to a reverse proxy.
- **Back Pressure**: Forcing a consuming service or reverse proxy to queue requests when a producing service reaches its maximum concurrent connection limit.
- **SLA (Service Level Agreement)**: Contractual promises made to a customer regarding system performance (e.g., uptime, request latency).
- **SLO (Service Level Objective)**: Individual targets defining an SLA (e.g., "The API will respond in 100ms").
- **SLI (Service Level Indicator)**: The actual measured value of a service's performance (e.g., "The API responds in 83ms").
- **TP95 / TP99 (Top Percentile)**: Performance metrics indicating that 95% or 99% of requests complete within a given latency. Averages must not be used for performance metrics.
- **Noisy Neighbor**: A problem where other services running on the same hardware consume excessive resources, slowing down the target service.

@Objectives
- Ensure Node.js applications are highly available by running redundant service instances.
- Offload CPU-intensive operations (TLS termination, gzip compression) from single-threaded Node.js applications to external, highly optimized reverse proxies.
- Protect Node.js services from being overwhelmed by implementing hard connection limits and reverse proxy back pressure.
- Accurately measure application performance and determine scalability requirements using robust load-testing methodologies and Top Percentile (TP99) metrics.
- Avoid architectural anti-patterns, specifically the misuse of the built-in Node.js `cluster` module for distributed system scaling.

@Guidelines
- **Cluster Module Constraints**:
  - The AI MUST generally AVOID using the built-in `cluster` module for scaling. Rely on reverse proxies to route traffic to independent processes across different machines.
  - If the `cluster` module MUST be used, the AI MUST keep the master process exceptionally simple. The master process MUST NOT load HTTP frameworks, database connections, or heavy modules.
  - The AI MUST consider the underlying protocol before using `cluster`. `cluster` operates at Layer 4; it WILL cause sticky connection issues with long-lived Layer 7 protocols like gRPC/HTTP2 (defeating round-robin load balancing).
  - The AI MUST NOT use the `cluster` module in environments restricted to a single CPU core (e.g., small VMs, constrained Docker containers), as the OS context switching between worker threads will degrade performance.
- **Reverse Proxy Architecture (HAProxy)**:
  - The AI MUST utilize a reverse proxy (e.g., HAProxy) to sit between the Node.js application and the internet.
  - The AI MUST configure health checks in the reverse proxy (e.g., `option httpchk GET /health`) to automatically drop traffic to crashed or unresponsive Node.js processes.
- **Performance Offloading**:
  - The AI MUST NOT perform HTTP compression (e.g., `zlib.createGzip()`) within the Node.js process. Configure the reverse proxy to handle compression (e.g., `compression algo gzip`).
  - The AI MUST NOT perform TLS termination within the Node.js process for production traffic. Configure the reverse proxy to handle SSL/TLS certificates (e.g., `ssl crt`).
- **Rate Limiting & Back Pressure**:
  - The AI MUST configure a hard limit on incoming connections in the Node.js application (e.g., `server.maxConnections = N`) to prevent the event loop from stalling and memory from being exhausted.
  - The AI MUST configure the reverse proxy to enforce a maximum connection limit (`maxconn`) that is lower or equal to the Node.js limit, forcing the reverse proxy to queue excess requests (back pressure) rather than the Node.js server abruptly dropping them.
- **Load Testing & Benchmarking**:
  - The AI MUST completely disable or comment out all `console.log()` statements within request handlers before performing load tests, as synchronous logging severely distorts performance metrics.
  - The AI MUST NOT rely on average latency metrics. The AI MUST evaluate performance using TP95 or TP99 (Top Percentile) metrics.
  - The AI MUST benchmark applications under exact production configurations (e.g., requests MUST be routed through the reverse proxy during the test if a proxy is used in production).

@Workflow
1. **Analyze Scaling Strategy**: Determine if scaling requires single-machine CPU optimization (rarely recommended) or multi-machine horizontal scaling (recommended).
2. **Optimize the Node.js Process**: 
   - Strip out any internal gzip compression or HTTPS/TLS configuration.
   - Set `server.maxConnections` to establish a safe upper bound for concurrent requests.
   - Implement a lightweight, fast `/health` endpoint for external monitoring.
3. **Configure the Reverse Proxy (HAProxy)**:
   - Define a `frontend` block to bind to the public port and handle TLS (`ssl crt`).
   - Define a `backend` block pointing to the redundantly deployed Node.js instances.
   - Enable load balancing (e.g., round-robin).
   - Configure health checks (`option httpchk`).
   - Enable compression (`compression algo gzip`, `compression type application/json text/plain`).
   - Set `maxconn` limits to handle back pressure safely.
4. **Establish SLOs and Load Test**:
   - Ensure all `console.log()` outputs in the request path are disabled.
   - Run a load-testing tool (e.g., Autocannon) against the reverse proxy.
   - Identify the maximum request rate the service can handle while satisfying the TP99 latency SLO.
5. **Scale Horizontally**: Calculate the required number of instances by dividing the target aggregate throughput by the maximum safe throughput of a single instance.

@Examples (Do's and Don'ts)

**Principle: Cluster Master Process Complexity**
- [DO]: Keep the cluster master extremely simple, strictly meant for spawning workers.
```javascript
// DO: Minimal master process
const cluster = require('cluster');
if (cluster.isMaster) {
  cluster.setupMaster({ exec: __dirname + '/worker-app.js' });
  cluster.fork();
  cluster.fork();
  cluster.on('exit', (worker) => cluster.fork());
}
```
- [DON'T]: Load heavy frameworks, database connections, or application logic into the master process.
```javascript
// DON'T: Heavy master process
const cluster = require('cluster');
const fastify = require('fastify')(); // Master loading heavy framework
const db = require('./database'); // Master making DB connections

if (cluster.isMaster) {
  cluster.fork();
} else {
  fastify.listen(3000);
}
```

**Principle: HTTP Compression**
- [DO]: Offload compression to a reverse proxy configuration like HAProxy.
```text
# DO: HAProxy configuration for compression
backend web-api
    compression algo gzip
    compression type application/json text/plain
    server web-api-1 localhost:3001
```
- [DON'T]: Perform gzip compression inside the Node.js event loop.
```javascript
// DON'T: Node.js handling compression
const zlib = require('zlib');
const http = require('http');
const fs = require('fs');

http.createServer((req, res) => {
    res.setHeader('Content-Encoding', 'gzip');
    fs.createReadStream('data.json').pipe(zlib.createGzip()).pipe(res);
}).listen(3000);
```

**Principle: Rate Limiting & Back Pressure**
- [DO]: Enforce `maxConnections` in Node.js, and use HAProxy `maxconn` to queue requests.
```javascript
// DO: Node.js hard connection limit
const server = http.createServer((req, res) => {
  // Handle request
});
server.maxConnections = 100;
server.listen(3000);
```
```text
# DO: HAProxy queuing via maxconn
backend web-api
    option httpclose
    server web-api-1 localhost:3000 maxconn 90
```
- [DON'T]: Allow Node.js to accept infinite concurrent connections without boundaries, leading to memory exhaustion and event loop stalling.
```javascript
// DON'T: Unbounded connections
const server = http.createServer((req, res) => {
  // Heavy async/DB operation. If 10,000 requests hit at once, the app crashes.
});
server.listen(3000);
```

**Principle: Load Testing Preparation**
- [DO]: Remove or comment out synchronous `console.log` statements before benchmarking to measure true performance.
```javascript
// DO: Clean request handler
server.get('/data', async (req, reply) => {
    // console.log('Incoming request'); // Disabled for benchmark
    return { data: 'ok' };
});
```
- [DON'T]: Leave `console.log` in the hot path during load testing, which will artificially throttle the TP99 latency.
```javascript
// DON'T: Logging in hot path during benchmark
server.get('/data', async (req, reply) => {
    console.log(`worker request pid=${process.pid}`); // Will ruin benchmark results
    return { data: 'ok' };
});
```