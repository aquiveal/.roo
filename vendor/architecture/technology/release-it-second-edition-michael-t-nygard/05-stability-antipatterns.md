@Domain
System Architecture, Backend Engineering, Service Integration, and Production Reliability. These rules trigger whenever the AI is designing, modifying, or reviewing distributed systems, network integrations, database queries, resource pooling, session management, or automation scripts.

@Vocabulary
*   **Technology Frontier**: The operational edge where systems exhibit both high interactive complexity and tight coupling, making them prone to rapid, catastrophic failures.
*   **Interactive Complexity**: A system state with enough hidden, internal dependencies that operator mental models are incomplete, leading to problem inflation and unexpected linkages.
*   **Tight Coupling**: The condition where a failure in one component instantly redistributes load, introduces delays, or propagates stress to other components, accelerating crack propagation.
*   **Integration Point**: Any socket, process, pipe, or remote procedure call connecting two systems (e.g., database connections, API calls, vendor libraries). The number one killer of systems.
*   **Fast Network Failure**: An immediate connection refusal (e.g., `Connection refused`) returning in milliseconds.
*   **Slow Network Failure**: A failure where packets are dropped (e.g., dropped ACK or silent firewall drops), causing threads to block for minutes waiting for a response or OS timeout.
*   **Chain Reaction**: A failure mode in horizontally scaled layers where the death of one node redistributes its load to surviving nodes, causing them to fail under the increased burden.
*   **Cascading Failure**: A failure mode where a crack jumps from one layer to another (e.g., a database slowdown causes application server thread pools to exhaust, bringing down the application).
*   **Self-Denial Attack**: A self-inflicted Distributed Denial of Service (DDoS), often caused by marketing mass-emails containing deep links, or rogue internal processes locking shared resources.
*   **Fight Club Bug**: A bug where increased front-end load causes exponentially increasing back-end processing.
*   **Scaling Effects**: Failures triggered by scaling relationships, such as O(n^2) connection limits in point-to-point architectures or shared resource bottlenecks.
*   **Unbalanced Capacities**: A mismatch in request-handling capacity between layers (e.g., a frontend with 3000 threads calling a backend with 75 threads), causing the backend to be crushed during traffic spikes.
*   **Dogpile**: A synchronized pulse of extreme load, caused by multiple servers booting simultaneously, hard-coded cron jobs firing at the top of the hour, or cache stampedes.
*   **Force Multiplier**: Control plane automation (e.g., autoscalers, configuration managers) that applies massive changes at high speed, lacking human judgment, and capable of amplifying outages if fed bad state data.
*   **Bogon**: A wandering network packet that arrives late, potentially interfering with newly re-opened sockets if TCP `TIME_WAIT` is not respected.
*   **Unbounded Result Set**: A database query or API call lacking explicit limits, which can unexpectedly return millions of rows and trigger OutOfMemory (OOM) crashes.

@Objectives
*   Assume the worst: Faults will happen. The AI must engineer systems to prevent faults from becoming errors, and errors from becoming system-wide failures.
*   Treat every integration point as hostile and likely to hang, crash, or return garbage.
*   Design for cynical software: Put up internal barriers, distrust external systems, and gracefully degrade functionality.
*   Prevent resource exhaustion by ensuring no thread, socket, or memory allocation can block or grow infinitely.

@Guidelines

**Integration Points**
*   When establishing an Integration Point, the AI MUST explicitly configure connection timeouts AND read/write timeouts. NEVER use default, infinite blocking calls.
*   When using long-lived TCP connections (e.g., JDBC connection pools), the AI MUST implement dead connection detection or application-level keepalives (e.g., heartbeat pings) to prevent firewalls from silently dropping idle connections.
*   When evaluating third-party or vendor API libraries, the AI MUST check for internal resource pooling, hidden synchronized blocks, or infinite socket reads. If present, the AI MUST wrap the library calls in a timeout mechanism or bounded worker pool.
*   When receiving HTTP responses, the AI MUST NOT blindly map responses to domain objects. Treat responses as untrusted data (maps/dictionaries) until semantically validated.

**Chain Reactions & Cascading Failures**
*   When designing horizontally scaled infrastructure, the AI MUST ensure that the application handles increased load safely without leaking memory or triggering race conditions.
*   When configuring resource pools (e.g., DB connections, thread pools), the AI MUST limit the time a thread can wait to check out a resource. Queues MUST be bounded.
*   When a remote provider fails, the AI MUST NOT implement immediate, aggressive speculative retries. Retries MUST use exponential backoff to avoid hammering a struggling downstream system.

**User and Session Management**
*   When handling per-user sessions, the AI MUST minimize in-memory session footprint. Cache only what is strictly necessary.
*   When storing large or expensive objects in memory, the AI MUST use `WeakReference` or `SoftReference` (or language equivalent) so the garbage collector can reclaim memory under pressure before throwing an OutOfMemoryError.
*   When building stateless or heavily scaled web services, the AI MUST consider off-heap or off-host memory (e.g., Redis, Memcached) instead of in-process session state.
*   When dealing with high connection volumes, the AI MUST evaluate OS-level TCP constraints, such as port exhaustion, and configure `TIME_WAIT` recycling safely within private networks.
*   When handling user requests, the AI MUST NOT rely exclusively on `robots.txt` for scraper mitigation. Use application-level or network-level circuit breakers/rate limiters to block abusive IPs or missing session cookies.
*   When creating deep links for email campaigns, the AI MUST route users to static landing zones or CDN-cached pages first, avoiding direct hits to origin application servers with un-cached parameters.

**Blocked Threads**
*   When implementing concurrent code, the AI MUST NOT synchronize on domain objects. The AI MUST use immutable domain objects and Command Query Responsibility Segregation (CQRS) to avoid locks.
*   When using locks, the AI MUST use modern concurrency primitives with timeouts (e.g., `tryLock(timeout)`) instead of unbounded wait/synchronized blocks.
*   When modifying inherited classes, the AI MUST NOT violate the Liskov Substitution Principle by quietly introducing synchronized blocks or blocking network calls where the base interface implies fast, local execution.

**Scaling Effects & Capacities**
*   When connecting multiple instances of a service, the AI MUST NOT use point-to-point communication if the scale exceeds a few nodes, as connections scale at O(n^2). The AI MUST implement UDP/TCP multicast, pub/sub, or message queues.
*   When designing interactions between tiers, the AI MUST account for Unbalanced Capacities. The AI MUST limit the concurrent outbound calls from the frontend to match the safe threshold of the backend.
*   When a service experiences high load, the AI MUST apply Backpressure or Shed Load (fail fast) rather than queuing requests infinitely.

**Dogpiles & Force Multipliers**
*   When scheduling cron jobs or system events, the AI MUST add randomized clock slew/jitter to prevent synchronized execution across multiple nodes.
*   When initializing caches or database connections on application boot, the AI MUST stagger startup or pre-warm caches progressively to avoid slamming the database.
*   When writing automation or control plane scripts (e.g., autoscalers, deployment scripts), the AI MUST implement "Governors" (safeguards) that pause and demand human confirmation if the script attempts to shut down a dangerously high percentage of instances or detects a massive state disparity.

**Slow Responses & Unbounded Result Sets**
*   When a service calculates its own average response time and finds it exceeds the SLA, the AI MUST trigger a Fail Fast mechanism to return immediate errors rather than hanging clients.
*   When writing database queries or API fetches, the AI MUST append strict limits (e.g., `LIMIT`, `TOP`, `rownum`) to prevent Unbounded Result Sets.
*   When exposing API endpoints, the AI MUST require pagination parameters (first item, count) and never allow the client to demand infinite data.
*   When processing relationship traversals (e.g., ORM lazy loading), the AI MUST safeguard against relationships that accumulate unlimited children (e.g., audit trails, clickstreams).

@Workflow
1.  **Identify Boundaries**: Map all Integration Points in the provided code or architecture. Identify databases, third-party APIs, vendor libraries, and inter-service calls.
2.  **Apply Timeouts & Bounds**: For every identified boundary, inject explicit connection timeouts, read timeouts, and bounded resource pool waits.
3.  **Audit Memory & Threads**: Review object caching, session state, and concurrency locks. Replace hard references to large objects with soft/weak references. Replace unbounded locks with timed locks.
4.  **Enforce Limits**: Review all SQL queries, ORM fetches, and API endpoints. Inject `LIMIT` clauses and pagination enforcement.
5.  **Inject Jitter**: Locate any scheduled tasks, retries, or startup routines. Add random slew/jitter to distribute load temporally.
6.  **Implement Shedding/Fail Fast**: Review the service's load handling. Add logic to reject incoming requests (e.g., HTTP 503) if internal queues or thread pools are exhausted, avoiding slow responses.
7.  **Review Automation Limits**: If modifying deployment or scaling scripts, add threshold checks (Governors) to abort operations if they affect >X% of the fleet.

@Examples (Do's and Don'ts)

**Integration Points & Timeouts**
*   [DO]: Configure HTTP clients with strict connection and read timeouts.
    `HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(2)).build();`
*   [DON'T]: Use default socket configurations that can block indefinitely.
    `new Socket("api.example.com", 80); // Anti-pattern: no timeout`

**Unbounded Result Sets**
*   [DO]: Always explicitly limit the maximum rows returned by a query.
    `SELECT id, name FROM users WHERE status = 'ACTIVE' LIMIT 100;`
*   [DON'T]: Trust the data producer or assume the table will stay small.
    `SELECT * FROM audit_logs WHERE user_id = 123; // Anti-pattern: can return millions of rows`

**Session & Heap Memory**
*   [DO]: Wrap expensive, easily re-computable objects in weak/soft references when caching in memory.
    `session.setAttribute("expensive_report", new SoftReference<>(reportData));`
*   [DON'T]: Store large collections or unlimited search results directly in the HTTP session.
    `session.setAttribute("search_results", listOfTenThousandItems); // Anti-pattern: rapid OOM risk`

**Blocked Threads**
*   [DO]: Use concurrency utilities with explicit timeouts.
    `if (lock.tryLock(5, TimeUnit.SECONDS)) { try { /* ... */ } finally { lock.unlock(); } }`
*   [DON'T]: Use unbounded synchronization blocks over network I/O or external libraries.
    `synchronized(this) { vendorApi.fetchData(); } // Anti-pattern: ties up threads indefinitely`

**Dogpiles**
*   [DO]: Add random jitter to scheduled tasks.
    `sleep(random.nextInt(5000)); executeNightlyBatch();`
*   [DON'T]: Hardcode exact execution times for hundreds of instances.
    `if (time == "00:00:00") executeNightlyBatch(); // Anti-pattern: causes database dogpile`

**Cascading Failures & Resource Pools**
*   [DO]: Configure connection pools to throw an exception quickly if a connection cannot be acquired.
    `HikariConfig config = new HikariConfig(); config.setConnectionTimeout(3000);`
*   [DON'T]: Allow thread pools to block indefinitely waiting for a downed database.
    `pool.setBlockWhenExhausted(true); pool.setMaxWaitMillis(-1); // Anti-pattern: guarantees system hang`

**Force Multiplier Automation**
*   [DO]: Add safety boundaries to operational scripts.
    `if (nodesToTerminate.size() > totalNodes * 0.20) { abort("Governor triggered: Too many nodes!"); }`
*   [DON'T]: Blindly apply desired state without checking the magnitude of the destructive action.
    `aws ec2 terminate-instances --instance-ids ${ALL_MISMATCHED_NODES} // Anti-pattern: could delete the whole fleet`