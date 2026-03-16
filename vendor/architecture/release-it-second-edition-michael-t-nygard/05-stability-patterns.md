# @Domain
These rules activate whenever the AI is designing, writing, reviewing, or debugging code for distributed systems, networking applications, microservices, APIs, or any production-bound software infrastructure. They apply particularly to tasks involving system architecture, integration points, concurrency, connection management, or fault tolerance.

# @Vocabulary
*   **Impulse**: A rapid, sudden shock to the system (e.g., a traffic spike).
*   **Stress**: A continuous force applied to the system over an extended period (e.g., a slow database).
*   **Crack Propagation**: The process by which a localized fault cascades into a systemic failure.
*   **Circuit Breaker**: A mechanism that monitors failures and opens a circuit to prevent calls to a failing remote system, providing a fallback instead.
*   **Bulkhead**: Partitions within a system that isolate failures so one broken component does not sink the entire system.
*   **Steady State**: A system's ability to run indefinitely without human intervention by continually recycling accumulated resources (data, logs, memory).
*   **Fail Fast**: The practice of validating resources and parameters immediately and returning an error before executing expensive operations.
*   **Let It Crash**: An error-handling philosophy where localized components are terminated and restarted to a clean state rather than attempting complex, unreliable state recovery.
*   **Supervision Tree**: A hierarchy in the Let It Crash model where a supervisor (which is NOT the consumer of the service) monitors and restarts child processes.
*   **Handshaking**: A cooperative protocol where a server signals its readiness or unreadiness to receive requests, allowing it to throttle its own workload.
*   **Test Harness**: A malicious, devious mock server designed specifically to simulate chaotic, out-of-spec network and protocol failures.
*   **Decoupling Middleware**: Message queues or publish/subscribe systems that separate producers and consumers in space and time.
*   **Load Shedding**: Refusing new requests at the system edge when the system exceeds its SLA or capacity.
*   **Back Pressure**: Blocking or slowing producers within a system boundary when a bounded queue is full.
*   **Governor**: A stateful, time-aware mechanism that slows down the execution rate of automated, unsafe actions to allow for human intervention.

# @Objectives
*   Prioritize resilience, recovery, and fault isolation over nominal-path execution.
*   Prevent cracks (faults) from propagating across system layers to avoid cascading failures.
*   Assume all external systems, networks, and integrations will fail, hang, or behave maliciously.
*   Maintain partial system functionality and self-protection mechanisms even when dependent services collapse.
*   Abstract error handling and timeout management into reusable structural primitives.

# @Guidelines

## Timeouts
*   The AI MUST apply configurable timeouts to ALL remote network calls, resource pool checkouts, socket operations, and thread synchronizations/mutexes.
*   The AI MUST NOT implement or recommend infinite blocking calls.
*   The AI MUST abstract long-running operations into structural primitives (e.g., Query Objects or Generic Gateways) to centralize timeout and error handling.
*   The AI MUST NOT recommend immediate retries upon timeout. The AI MUST implement delayed, store-and-forward retries or queueing to allow the remote system time to recover.
*   The AI MUST return a fallback result or failure to the client quickly rather than exhausting the client's own timeout window with repeated internal retries.

## Circuit Breaker
*   The AI MUST wrap risky external integration points in a Circuit Breaker.
*   The AI MUST implement three states: Closed (normal), Open (calls fail immediately without attempting execution), and Half-Open (a trial call is allowed after a timeout to test recovery).
*   The AI MUST track fault *density* (e.g., using a Leaky Bucket algorithm) rather than raw absolute fault counts.
*   The AI MUST track different failure types separately (e.g., Connection Refused vs. Timeout).
*   The AI MUST ensure Circuit Breaker state is scoped to a single process. The AI MUST NOT share Circuit Breaker state across multiple processes via out-of-process communication, which introduces new failure modes.
*   The AI MUST specify a clear fallback strategy (return last good response, cached value, generic answer, or failover to secondary service).
*   The AI MUST ensure Circuit Breaker state changes are logged, exposed for monitoring, and capable of manual override.

## Bulkheads
*   The AI MUST segregate resources (e.g., thread pools, memory, processes) to ensure a failure in one partition does not exhaust resources in another.
*   The AI MUST NOT share a single thread pool or connection pool for entirely different downstream integrations.
*   The AI MUST reserve a dedicated, isolated thread pool specifically for administrative/diagnostic requests.

## Steady State
*   The AI MUST implement data purging logic strictly within the application code to maintain referential and logical integrity, rather than relying on DBA scripts.
*   The AI MUST implement log rotation based on size, NOT time, and ensure logs are shipped off individual hosts to a centralized collector.
*   The AI MUST strictly bound all in-memory caches. The AI MUST use Least Recently Used (LRU) eviction or weak/soft references to allow garbage collectors to reclaim memory under pressure. The AI MUST implement an invalidation strategy.

## Fail Fast
*   The AI MUST validate user inputs, parameters, and structural integrity immediately upon request reception.
*   The AI MUST execute a "software mise en place": pre-verify that required resources (DB connections, open Circuit Breakers) are available BEFORE starting expensive processing.
*   The AI MUST report system failures (resource exhaustion) distinctly from application failures (bad user input) so upstream callers do not accidentally trip their own Circuit Breakers due to user typos.

## Let It Crash
*   For components with microsecond/millisecond startup times (e.g., actors, isolated microservices), the AI MUST favor crashing and restarting over complex, error-prone state cleanup.
*   The AI MUST isolate crashing components to prevent cascading failures.
*   The AI MUST implement a Supervisor Hierarchy. The supervisor MUST NOT be the consumer of the crashed service.
*   The AI MUST track the density/frequency of child crashes. If child restarts are too frequent, the supervisor MUST crash itself to bubble the failure up.
*   The AI MUST ensure crashed and restarted components reintegrate automatically into load balancers/service discovery pools.
*   The AI MUST NOT apply Let It Crash to monoliths or components with slow (minutes-long) initialization times.

## Handshaking
*   The AI MUST implement cooperative demand control by exposing specific health check endpoints.
*   The AI MUST ensure health checks return error statuses (e.g., HTTP 503) when the service is overwhelmed, enabling load balancers to immediately route traffic elsewhere.
*   If implementing custom socket protocols, the AI MUST build in signaling to let endpoints inform each other when they cannot accept more work.

## Test Harnesses
*   When generating integration tests, the AI MUST design or recommend a malicious Test Harness server instead of simple, compliant mock objects.
*   The AI MUST configure the Test Harness to simulate out-of-spec behaviors: refusing connections, black-holing requests (accepting but never replying), returning garbage data, returning massive payloads, and exhibiting extreme latency.

## Decoupling Middleware
*   The AI MUST favor asynchronous, message-oriented middleware (queues, pub/sub) over synchronous request/reply architectures (HTTP/RPC) for inter-system communication to decouple systems in space and time.

## Demand Control (Shed Load & Back Pressure)
*   **Shed Load (At System Edges):** The AI MUST configure the system to drop requests immediately (e.g., HTTP 503) when response times exceed the SLA or resources are saturated.
*   **Back Pressure (Within System Boundaries):** The AI MUST use strictly bounded queues for internal producer/consumer handoffs. 
*   When a bounded queue is full, the AI MUST dictate whether the system drops the item, refuses the work, or blocks the producer.
*   If blocking the producer, the AI MUST ensure the block has a strict timeout. The AI MUST separate outbound call threads from request-handling threads so the request-handler can time out and return a 503 rather than freezing.

## Governor
*   For any automation that manipulates infrastructure (autoscaling, data deletion, node termination), the AI MUST implement a Governor.
*   The AI MUST make the Governor asymmetric: it MUST allow rapid action in safe directions (adding capacity) but apply increasing resistance/slowness in unsafe directions (removing capacity).
*   The AI MUST pause automated destruction and require human intervention if changes exceed safe operational variance thresholds.

# @Workflow
1.  **Analyze External Dependencies:** Map every integration point, database, and remote service the code interacts with.
2.  **Apply Defensive Wrappers:** Enforce Timeouts and Circuit Breakers on all identified external dependencies. Abstract these into generic gateways.
3.  **Enforce Entry Constraints:** Implement Fail Fast validation and allocate requests to designated Bulkheads.
4.  **Validate Steady State Mechanics:** Ensure all caches are bounded, logs are size-rotated, and data purging routines are present.
5.  **Establish Demand Control:** Configure Handshaking (health checks), Load Shedding (at edges), and Back Pressure (bounded queues internally).
6.  **Define Recovery Models:** Apply "Let It Crash" with Supervisors for fast-restarting actors, and implement Governors for automated infrastructure actions.
7.  **Design Chaotic Testing:** Generate Test Harnesses that actively assault the application with latency, garbage data, and protocol violations.

# @Examples (Do's and Don'ts)

### Timeouts
*   [DO] Use explicitly configured timeouts for HTTP clients, e.g., `client = &http.Client{Timeout: 10 * time.Second}`. Implement fallback logic or queue the request for later if the timeout triggers.
*   [DON'T] Use default clients that block indefinitely, e.g., `http.Get("url")`, which can hang the thread forever if the remote server drops the ACK.

### Circuit Breaker
*   [DO] Wrap network calls in a Circuit Breaker object that tracks error rates. If errors exceed 10 in 10 seconds, open the circuit and immediately return a cached or default value for subsequent calls.
*   [DON'T] Catch a timeout exception, log it, and simply retry the exact same failing downstream call synchronously, thereby exhausting the local thread pool.

### Bulkheads
*   [DO] Create separate `ExecutorService` thread pools for `PaymentProcessing` and `EmailNotifications`. If the email server hangs, payment processing remains unaffected.
*   [DON'T] Rely on a single global thread pool or database connection pool for the entire monolithic application.

### Steady State
*   [DO] Use an in-memory cache configured with a maximum size limit of 1000 items and an LRU eviction policy.
*   [DON'T] Use a standard dictionary/hash map to cache results where items are continually added but never explicitly removed, resulting in an inevitable `OutOfMemoryError`.

### Fail Fast
*   [DO] In the first lines of a controller, check if the Circuit Breaker for the required backend system is OPEN. If it is, immediately return `503 Service Unavailable`.
*   [DON'T] Parse a massive JSON payload, allocate domain objects, and perform heavy computation, only to fail at the very end because the database connection pool is exhausted.

### Back Pressure
*   [DO] Pass jobs between internal components using a bounded queue of size 500. If full, the producer thread times out after 50ms and returns a "System Busy" error to the client.
*   [DON'T] Use an unbounded `LinkedBlockingQueue` that quietly absorbs millions of messages until the JVM crashes under traffic spikes.

### Governor
*   [DO] Write an autoscaler script that limits termination to a maximum of 5% of the total fleet per hour, requiring manual admin approval to exceed that rate.
*   [DON'T] Allow a script to unilaterally terminate 90% of production instances because a partially-failed service discovery tool falsely reported them as idle.