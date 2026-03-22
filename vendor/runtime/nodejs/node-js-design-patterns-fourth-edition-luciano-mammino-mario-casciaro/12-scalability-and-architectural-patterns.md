@Domain
This rule file MUST be triggered when the AI is tasked with designing, refactoring, or implementing application scaling, load balancing, high availability, clustering, containerization (Docker/Kubernetes), microservices architecture, and service integration strategies within a Node.js ecosystem.

@Vocabulary
- **Scale Cube**: A three-dimensional model for scalability defining X-axis (Cloning), Y-axis (Decomposing by service/functionality), and Z-axis (Splitting by data partition).
- **Vertical Scaling**: Upgrading the hardware of a single machine (CPU, RAM, Disk).
- **Horizontal Scaling**: Adding more instances of the application across multiple processes or machines.
- **Cluster Module (`node:cluster`)**: A core Node.js module used to fork the primary process into multiple worker processes to distribute load across CPU cores on a single machine.
- **Round-Robin Load Balancing**: The default algorithm used by `node:cluster` (except on Windows) and many reverse proxies to distribute incoming requests evenly across instances.
- **Zero-Downtime Restart**: A deployment technique where worker processes are sequentially stopped and replaced without interrupting the application's ability to serve requests.
- **Sticky Load Balancing (Sticky Sessions)**: A routing mechanism where a load balancer maps a user's session to a specific backend instance.
- **Reverse Proxy / Gateway**: An intermediary service (e.g., Nginx, HAProxy) that sits in front of backend instances to route and load-balance client requests.
- **Service Registry**: A central repository (e.g., Consul) that maintains an up-to-date view of available servers and network services for dynamic horizontal scaling.
- **Peer-to-Peer Load Balancing**: Client-side load balancing where the requesting service routes its own traffic directly to the instances of the target service, bypassing a central load balancer.
- **Data Ownership**: A microservices principle dictating that each service must manage and own its own isolated database.
- **API Proxy / API Gateway**: An integration pattern providing a single structural access point for multiple remote APIs.
- **API Orchestration Layer / API Orchestrator**: An abstraction layer that semantically integrates multiple services by coordinating requests and aggregating data.
- **Backend for Frontend (BFF)**: A specific type of API Orchestrator tailored for the exact needs of a specific client interface (e.g., mobile app, web app).
- **Message Broker**: An intermediary system used to decouple microservice communications using Publish/Subscribe patterns, preventing tight coupling and the "God object" anti-pattern.

@Objectives
- Ensure Node.js applications are designed for horizontal scalability from day one to compensate for its single-threaded nature.
- Implement robust, fault-tolerant systems using `node:cluster` or external orchestrators to guarantee high availability and self-healing.
- Eliminate shared in-memory state across instances to enable seamless load balancing and horizontal scaling.
- Decompose monolithic applications into highly cohesive, loosely coupled microservices strictly following the Data Ownership principle.
- Design resilient integration layers using the appropriate pattern (Proxy, Orchestrator, or Message Broker) based on coupling constraints.

@Guidelines

**Scaling Principles and the Scale Cube**
- The AI MUST apply the Scale Cube dimensions when evaluating scaling strategies:
  - Use **X-axis (Cloning)** for straightforward capacity increase (cloning instances).
  - Use **Y-axis (Decomposing)** to break monolithic complexity into microservices.
  - Use **Z-axis (Data Partitioning/Sharding)** for massive data volume distribution.
- The AI MUST default to Horizontal Scaling over Vertical Scaling to ensure fault tolerance and redundancy.

**Using the `node:cluster` Module**
- The AI MUST use `cluster.isPrimary` (or `cluster.isMaster` in older versions) to distinguish the orchestrating process from the workers.
- The AI MUST spawn a number of workers equal to the number of available logical CPU cores using `os.cpus().length`.
- The AI MUST implement resiliency by listening to the `exit` event on the primary process and spawning a replacement worker (`cluster.fork()`) if the crash was unintended (i.e., checking `code !== 0` and `!worker.exitedAfterDisconnect`).
- The AI MUST implement Zero-Downtime Restarts by listening to a signal (e.g., `SIGUSR2`), iterating over `Object.values(cluster.workers)`, gracefully stopping them using `worker.disconnect()`, waiting for the `exit` event, and subsequently calling `cluster.fork()`.
- The AI MUST be aware of `node:cluster` edge cases:
  - Invoking `server.listen({fd})` in a worker maps to different file descriptors than the primary.
  - Invoking `server.listen(handle)` bypasses the primary process delegation.
  - Invoking `server.listen(0)` generates the same "random" port for all workers after the first call.

**Stateful Communications and Load Balancing**
- The AI MUST NOT store user sessions or application state in the memory of the Node.js process.
- The AI MUST externalize state to a shared data store (e.g., Redis, Memcached) or use stateless authentication mechanisms (e.g., JWT).
- The AI MUST AVOID Sticky Load Balancing if possible, as it degrades redundancy, complicates failover, and ties user sessions to specific ephemeral instances.
- For multi-machine scaling, the AI MUST recommend a robust Reverse Proxy (e.g., Nginx, HAProxy) over native Node.js solutions for production environments.

**Dynamic Scaling and Service Registries**
- When infrastructure is dynamic, the AI MUST use a Service Registry pattern (e.g., using Consul) to allow application instances to register themselves on startup and deregister on exit.
- The AI MUST ensure graceful deregistration by binding deregistration logic to `SIGINT` and `uncaughtException` events.
- For internal service-to-service communication, the AI MUST consider Peer-to-Peer Load Balancing to reduce latency and eliminate the Reverse Proxy as a single point of failure.

**Containerization and Kubernetes**
- The AI MUST package Node.js applications using minimal OCI-compliant base images (e.g., `FROM node:24-slim`).
- The AI MUST enforce strict statelessness when designing applications for Kubernetes, as pods are disposable and can be terminated at any time.
- The AI MUST delegate scaling, rollouts, and process restart responsibilities to Kubernetes rather than implementing `node:cluster` inside a container, unless specific per-pod CPU utilization metrics demand internal clustering.

**Microservices and Decomposition**
- The AI MUST enforce the Data Ownership principle: each microservice MUST have its own independent database. The AI MUST NOT allow multiple microservices to connect to the same shared database.
- The AI MUST ensure that inter-service communication occurs via remote interfaces (APIs, Message Brokers) rather than direct data access.

**Integration Patterns**
- The AI MUST use an **API Proxy/Gateway** when structural integration is needed (simply routing requests to the correct service).
- The AI MUST use an **API Orchestrator** or **BFF** when semantic integration is needed (composing multiple service calls into a single response, or aggregating data for a specific frontend).
- The AI MUST NOT use an API Orchestrator if it creates a "God object" (an entity that knows too much about the system and forces high coupling).
- The AI MUST use a **Message Broker (Publish/Subscribe)** to propagate side-effects or state changes across the system. Services MUST emit events to the broker without knowing the identities of the subscribers.

@Workflow
1. **Analyze Requirements**: Determine the specific scaling bottleneck (CPU-bound, memory-bound, network-bound, or team/codebase complexity).
2. **Apply Scale Cube**:
   - If CPU/Traffic bound -> Apply X-axis scaling.
   - If Codebase/Domain bound -> Apply Y-axis scaling.
   - If Database/Storage bound -> Apply Z-axis scaling.
3. **Select Infrastructure Strategy**:
   - For a single machine: Implement `node:cluster` with crash recovery and zero-downtime restart logic.
   - For multi-machine: Implement a Reverse Proxy (Nginx) and configure statelessness (Redis/JWT).
   - For dynamic/cloud-native: Implement Dockerfiles, Service Registry integrations, or Kubernetes deployment manifests.
4. **Enforce Statelessness**: Audit the codebase for in-memory state (e.g., `const sessions = {}`). Refactor to external shared stores.
5. **Architect Microservices (if applicable)**: Define strict service boundaries. Assign isolated databases to each service.
6. **Define Integration Layer**: Route requests via an API Gateway, aggregate complex queries via an Orchestrator/BFF, and distribute state changes via an asynchronous Message Broker.

@Examples (Do's and Don'ts)

[DO] Implement a resilient `node:cluster` architecture with automatic worker replacement.
```javascript
import cluster from 'node:cluster';
import { cpus } from 'node:os';
import { createServer } from 'node:http';

if (cluster.isPrimary) {
  const availableCpus = cpus();
  for (const _ of availableCpus) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code) => {
    if (code !== 0 && !worker.exitedAfterDisconnect) {
      console.log(`Worker ${worker.process.pid} crashed. Starting a new worker`);
      cluster.fork();
    }
  });
} else {
  const server = createServer((req, res) => {
    res.end(`Hello from ${process.pid}\n`);
  });
  server.listen(8080);
}
```

[DON'T] Leave a clustered application vulnerable to permanent downtime by failing to listen to the `exit` event.
```javascript
import cluster from 'node:cluster';
import { cpus } from 'node:os';

// ANTI-PATTERN: If workers crash, they are never replaced. The app will die.
if (cluster.isPrimary) {
  cpus().forEach(() => cluster.fork());
} else {
  // worker logic
}
```

[DO] Implement zero-downtime restarts by gracefully disconnecting workers one by one.
```javascript
process.on('SIGUSR2', async () => {
  const workers = Object.values(cluster.workers);
  for (const worker of workers) {
    worker.disconnect();
    await once(worker, 'exit');
    if (!worker.exitedAfterDisconnect) continue;
    
    const newWorker = cluster.fork();
    await once(newWorker, 'listening');
  }
});
```

[DON'T] Restart workers abruptly, dropping active client connections.
```javascript
// ANTI-PATTERN: Kills all workers immediately, causing downtime and lost requests.
process.on('SIGUSR2', () => {
  Object.values(cluster.workers).forEach(w => w.process.kill());
});
```

[DO] Store session data in a shared data store (e.g., Redis) when scaling horizontally.
```javascript
import Redis from 'ioredis';
const redisClient = new Redis();

export async function setSession(sessionId, data) {
  await redisClient.set(sessionId, JSON.stringify(data));
}
```

[DON'T] Store session data in local process memory when building a scalable application.
```javascript
// ANTI-PATTERN: This will fail in a load-balanced environment because 
// subsequent requests might hit a different instance.
const localSessions = new Map();

export function setSession(sessionId, data) {
  localSessions.set(sessionId, data);
}
```

[DO] Enforce Data Ownership in microservices by assigning isolated databases to each service.
```javascript
// Product Service connects to the Product DB
const productDb = new DbClient('product_db');

// Cart Service connects to the Cart DB
const cartDb = new DbClient('cart_db');
```

[DON'T] Share a single database across multiple microservices.
```javascript
// ANTI-PATTERN: High coupling. The Checkout Service directly alters Product data.
// Instead, Checkout Service should publish a 'purchase_completed' event to a message broker.
export async function completeCheckout(db, cartId) {
  await db.query('UPDATE products SET availability = availability - 1');
}
```