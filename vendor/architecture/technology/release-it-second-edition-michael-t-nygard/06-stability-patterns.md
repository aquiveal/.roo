@Domain
These rules are triggered whenever the AI is tasked with designing, architecting, developing, or refactoring distributed systems, microservices, backend applications, network integration points, system administration scripts, or deployment automation tools. They apply to any request involving high availability, system resilience, fault tolerance, resource pooling, network communication, or system state management.

@Vocabulary
- **Transaction**: An abstract unit of work processed by the system (not strictly a database transaction).
- **System**: The complete, interdependent set of hardware, applications, and services required to process transactions.
- **Impulse**: A rapid, transient shock to the system (e.g., a massive traffic spike).
- **Stress**: A persistent force applied to the system over an extended period (e.g., slow responses from a third-party API).
- **Strain**: The resulting deformation or odd effect within the system caused by stress.
- **Fault**: A condition that creates an incorrect internal state in the software.
- **Error**: Visibly incorrect behavior originating from a fault.
- **Failure**: An unresponsive system.
- **Crack**: A fault that begins to propagate through the system, eventually leading to full failure if unstopped.
- **Crackstopper**: A design pattern (like a crumple zone) that contains damage and prevents crack propagation.
- **Timeouts**: Fault isolation mechanisms that abandon blocked operations rather than waiting indefinitely.
- **Circuit Breaker**: A pattern that wraps dangerous operations, tracks failures, and prevents subsequent calls when a failure threshold is reached.
- **Bulkheads**: System partitions that isolate failures to a single compartment, preventing total ship (system) loss.
- **Steady State**: The principle of avoiding human "fiddling" by ensuring no resource (logs, data, memory) accumulates without a corresponding automated recycling/purging mechanism.
- **Fail Fast**: The practice of aborting an operation immediately if required resources or preconditions are unmet, rather than wasting cycles.
- **Let It Crash**: An architectural philosophy of terminating a faulty component and restarting it to a known clean state rather than attempting complex error recovery.
- **Handshaking**: Cooperative demand control where a receiver signals its readiness (or lack thereof) to accept data from a sender.
- **Test Harness**: A devious, customized simulator used during testing to intentionally inflict network, protocol, and application-level failures on a calling service.
- **Decoupling Middleware**: Message-oriented, asynchronous communication that isolates endpoints in space and time to prevent cascading failures.
- **Shed Load**: Refusing incoming requests at the system edge when demand exceeds the service's SLA or capacity.
- **Back Pressure**: Throttling producers inside a system boundary by blocking or dropping items when a bounded queue is full.
- **Governor**: A stateful limiter applied to automation that restricts the speed or volume of destructive/unsafe actions to allow human intervention.

@Objectives
- Assume the worst: the network will fail, dependencies will hang, humans will make unforced errors, and users will act unpredictably.
- Prevent faults from becoming errors, and errors from becoming complete system failures.
- Stop crack propagation: isolate failures so they do not cascade across integration points or exhaust system resources.
- Create cynical software that expects external components to fail and proactively protects its own request-handling threads and memory.
- Design systems that can operate indefinitely without human intervention (fiddling) to clean up accumulated state (sludge).

@Guidelines
- **Timeouts**
  - The AI MUST configure explicit timeouts for EVERY network call, socket connection, read/write operation, and resource pool checkout. Infinite blocking is strictly forbidden.
  - The AI MUST group long-running interactions into a single abstraction (e.g., a Query Object or Gateway) to enforce timeouts consistently.
  - When an operation times out, the AI MUST return a designated response or queue the work for later. The AI MUST NOT immediately retry a timed-out remote connection, as fast retries exacerbate external failures.
- **Circuit Breaker**
  - The AI MUST wrap all external integration points with a Circuit Breaker.
  - The AI MUST configure the Circuit Breaker to track fault *density* (e.g., using a Leaky Bucket pattern) rather than absolute fault counts.
  - When the circuit is "Open", the AI MUST provide a fallback strategy (e.g., return a cached value, return a generic response, or fail immediately).
  - The AI MUST scope the Circuit Breaker state to the individual process. It MUST NOT share Circuit Breaker state across multiple processes to avoid introducing a new distributed point of failure.
  - The AI MUST expose Circuit Breaker state changes to operations via logs and metrics.
- **Bulkheads**
  - The AI MUST logically or physically partition resources (e.g., server instances, CPUs, thread pools) to contain failures.
  - The AI MUST dedicate separate thread pools for administrative/health-check endpoints versus standard request-handling to ensure the system remains observable even under heavy load.
  - If a specific background process is prone to runaway CPU usage, the AI MUST bind that process to specific CPU cores to prevent host-wide starvation.
- **Steady State**
  - The AI MUST implement automated application-level data purging for databases. It MUST NOT rely on external DBA scripts if using an ORM, as logical integrity requires application context.
  - The AI MUST implement size-based log file rotation and ensure logs are forwarded off the host to prevent filesystem exhaustion.
  - The AI MUST implement strict memory limits and cache-eviction policies (e.g., LRU, time-based, or weak references) for all in-memory caching. Unbounded caches are strictly forbidden.
- **Fail Fast**
  - The AI MUST validate all required parameters and check the availability of required external resources (e.g., connection pools, Circuit Breakers) *before* beginning heavy processing.
  - If resources are unavailable, the AI MUST immediately return an error (e.g., HTTP 503) to free up the calling thread.
  - The AI MUST distinguish between system failures (e.g., HTTP 503) and user/input errors (e.g., HTTP 400). Generic errors MUST NOT be used, to prevent upstream Circuit Breakers from tripping due to user input mistakes.
- **Let It Crash**
  - For small, granular, fast-starting components (e.g., actors, microservices, containers), the AI MUST implement supervisor trees that terminate and restart faulty components rather than attempting deep state recovery.
  - The AI MUST ensure that supervised restarts are tracked. If restart density is too high, the supervisor MUST recursively crash itself.
  - The AI MUST NOT apply "Let It Crash" to slow-starting monoliths or systems that require long cache warm-ups.
- **Handshaking**
  - The AI MUST implement health-check endpoints that assess the true capability of the instance to process work (e.g., database connectivity, thread pool saturation).
  - If the instance cannot process work in a timely manner, the health check MUST signal the load balancer to stop sending traffic (e.g., by returning an HTTP 503).
- **Test Harnesses**
  - When writing integration tests, the AI MUST NOT test solely against a "happy path" mock.
  - The AI MUST recommend or implement test harnesses that deliberately simulate slow responses, dropped connections, half-open sockets, and garbage payloads (e.g., mapping different misbehaviors to different ports).
- **Decoupling Middleware**
  - Where business requirements permit, the AI MUST prefer asynchronous, message-oriented middleware (queues, pub/sub) over tightly coupled synchronous RPC/HTTP calls to completely decouple endpoints in time and space.
- **Shed Load**
  - For services exposed to unbounded external demand (the Internet), the AI MUST implement self-monitoring against the SLA. If response times exceed the SLA, the system MUST shed load by rejecting new requests (HTTP 503) until it catches up.
- **Create Back Pressure**
  - Inside a system boundary, the AI MUST use bounded (finite) queues. Unbounded queues are strictly forbidden.
  - When a queue is full, the AI MUST explicitly define the back-pressure behavior: drop the item, refuse the work, or block the producer (with a timeout).
  - The AI MUST accept network calls on one thread pool and issue internal/outbound queued calls on a secondary thread pool so that back-pressure blocking does not consume the primary listener threads.
- **Governor**
  - When writing automation, scaling, or provisioning scripts, the AI MUST implement a Governor to limit the rate of unsafe actions (e.g., shutting down instances, deleting data).
  - The Governor MUST apply a response curve: actions within a safe threshold execute normally; actions outside the threshold encounter increasing resistance or require human confirmation.

@Workflow
1. **Integration Point Hardening**: Identify all network and cross-process calls. Wrap every call in a Circuit Breaker and enforce a strict Timeout.
2. **Capacity & Resource Protection**: Analyze resource contention points. Implement Bulkheads (separate thread pools), establish finite queues with Back Pressure, and implement Fail Fast validation at the entry points.
3. **State & Sludge Management**: Review all stateful operations. Apply the Steady State pattern by ensuring logs rotate, caches evict, and database rows are purged via automated lifecycle policies.
4. **Demand Control**: Define the system's acceptable SLA. Implement Health Checks (Handshaking) and Load Shedding for external traffic, and Let It Crash supervisors for internal component failures.
5. **Automation Safety**: For any control-plane or operational script generated, insert a Governor pattern to hard-limit the velocity of destructive actions.
6. **Cynical Testing**: Design Test Harness specifications that deliberately feed the system malformed data, infinitely slow responses, and abrupt disconnects to prove the above mechanisms work.

@Examples (Do's and Don'ts)

- **Timeouts**
  - [DO]: `response = httpClient.get("https://api.example.com/data", timeout=5.0)`
  - [DON'T]: `response = httpClient.get("https://api.example.com/data") // Default infinite wait`

- **Circuit Breaker**
  - [DO]: Wrap the database call in a breaker. `if (breaker.isOpen()) { return CachedData.get(); } else { try { result = db.query(); breaker.recordSuccess(); return result; } catch(TimeoutException e) { breaker.recordFailure(); throw e; } }`
  - [DON'T]: Blindly catch a timeout and immediately execute a `while(true)` retry loop against the failing database.

- **Steady State (Caching)**
  - [DO]: `Cache cache = CacheBuilder.newBuilder().maximumSize(10000).expireAfterWrite(10, TimeUnit.MINUTES).build();`
  - [DON'T]: `Map<String, UserSession> cache = new HashMap<>(); // Grows infinitely until OutOfMemoryError`

- **Fail Fast**
  - [DO]: `if (!dbPool.hasAvailableConnections() || circuitBreaker.isOpen()) { return HTTP_503_UNAVAILABLE; } processHeavyRequest();`
  - [DON'T]: Execute 90% of the complex business logic, perform 5 calculations, and *then* request a DB connection, only to fail and throw an exception because the pool is empty.

- **Back Pressure (Queues)**
  - [DO]: `BlockingQueue<Task> queue = new ArrayBlockingQueue<>(500); // Finite queue`
  - [DON'T]: `BlockingQueue<Task> queue = new LinkedBlockingQueue<>(); // Unbounded queue leading to memory exhaustion`

- **Governor (Automation)**
  - [DO]: `def scale_down(target_count): if current_count - target_count > MAX_SAFE_KILL_QUOTA: alert_human(); return MAX_SAFE_KILL_QUOTA; else: execute_kill(target_count)`
  - [DON'T]: `def scale_down(target_count): for instance in instances_to_kill: instance.terminate() // Kills 99% of infrastructure due to a bad config read`