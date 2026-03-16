# @Domain
These rules MUST be activated when the AI is designing, architecting, refactoring, or writing code for distributed systems, web services, APIs, microservices, database integrations, network communications, or when addressing issues related to system capacity, performance, stability, scaling, or production-readiness.

# @Vocabulary
- **Integration Point**: Any connection, socket, process, pipe, or remote procedure call linking the system to an external or internal service, database, or API.
- **Listen Queue**: A finite operating system queue for a network port that holds pending TCP connections (SYN received, awaiting application `accept()`). 
- **Bogon**: A wandering, delayed network packet from a closed connection that arrives late and can corrupt a reused socket if `TIME_WAIT` is circumvented.
- **Chain Reaction**: A load-related failure mode in horizontally scaled clusters where the death of one node redistributes its load to surviving nodes, causing them to overload and fail sequentially.
- **Cascading Failure**: A failure that jumps across layer boundaries (e.g., from database to app server), typically caused by exhausted resource pools or blocked threads waiting on a failing lower-layer dependency.
- **Weak/Soft Reference**: A programmatic mechanism to hold an object in memory until the garbage collector encounters low memory conditions, at which point the payload is automatically reclaimed to prevent OutOfMemory errors.
- **Shared-Nothing Architecture**: A horizontal scaling ideal where each server operates independently without requiring coordination or calls to centralized shared resources (like lock managers).
- **Self-Denial Attack**: A scenario where the system, the organization, or legitimate users unintentionally generate a synchronized surge of traffic that overloads the system (e.g., email marketing blasts with deep links).
- **Dogpile**: A sudden, concentrated burst of demand caused by synchronized events, such as all servers booting at once, a cron job firing exactly at midnight, or threads simultaneously refreshing an expired cache.
- **Force Multiplier**: Automation (like autoscalers, service discovery, or configuration management) that executes large-scale actions rapidly, which can amplify minor configuration faults into total system outages.
- **Unbounded Result Set**: A database query or service call that returns an unpredictable, limitless number of records, exhausting heap memory and crashing the application.
- **Slow Response**: A state where a system processes requests at a severely degraded pace. Considered worse than a fast failure because it ties up threads, memory, and connections in both the provider and the caller.

# @Objectives
- The AI MUST design "cynical" software that assumes all external systems, networks, users, and libraries will eventually fail, hang, or misbehave.
- The AI MUST prioritize the preservation of partial functionality and system survival over flawless execution of every individual request.
- The AI MUST actively prevent faults from becoming errors, and errors from becoming cascading systemic failures.
- The AI MUST ensure capacity limits, timeouts, and resource boundaries are strictly enforced on all integration points and queries.

# @Guidelines

### Integration Points & Network Protocols
- The AI MUST explicitly configure read, write, and connection timeouts on every network socket, HTTP client, database connection, and remote procedure call.
- The AI MUST NOT rely on default infinite blocking behaviors for any network I/O.
- The AI MUST NOT map HTTP responses directly into domain objects without first verifying the response format, status code, and content type (to avoid parsing errors from unexpected HTML/text payloads like generic 404 pages or ISP redirects).
- The AI MUST implement keep-alive pings (e.g., dead connection detection) for long-running idle connections passing through firewalls to prevent silent connection drops resulting in infinite blocking.

### Chain Reactions & Cascading Failures
- The AI MUST protect request-handling threads by ensuring that failing integration points trip a Circuit Breaker, immediately returning failures rather than blocking threads.
- The AI MUST limit the time a thread can wait to check out a resource from a pool.
- The AI MUST NOT implement aggressive or infinite speculative retries on failed external calls. Retries MUST utilize exponential backoff and jitter.
- The AI MUST partition capacity (e.g., thread pools, processes) using the Bulkhead pattern so that a failure in one subsystem does not drain the resources of the entire application.

### Managing Users & Sessions
- The AI MUST minimize the amount of data stored in in-memory user sessions. The session MUST NOT be used to cache large result sets, pagination data, or shopping carts in their entirety.
- The AI MUST use Weak References or Soft References for caching large/expensive objects in memory, allowing the Garbage Collector to reclaim them during high-traffic memory pressure.
- The AI MUST consider off-heap memory (e.g., Redis, Memcached) for session storage to decouple memory constraints from the application process.
- The AI MUST NOT use URL rewriting to track sessions; session IDs MUST be transmitted exclusively via cookies to prevent bot/scraper traffic from creating a new session in memory for every single HTTP request.
- The AI MUST lower TCP `TIME_WAIT` settings for internal data center traffic to rapidly free ephemeral ports during high connection volume.

### Blocked Threads & Libraries
- The AI MUST NOT synchronize methods on domain objects. Instead, the AI MUST use immutable domain objects and Command objects for state mutation.
- The AI MUST NOT violate the Liskov Substitution Principle by adding `synchronized` (or equivalent locking semantics) to a subclass method override if the superclass/interface method is not synchronized.
- The AI MUST treat all third-party and vendor API libraries as inherently dangerous. If a vendor library lacks timeout controls, the AI MUST isolate its execution in a separate worker thread pool wrapped with a Future and a strict timeout.
- The AI MUST NOT roll custom connection pools. The AI MUST use proven, battle-tested concurrency primitives and connection pool libraries.

### Scaling Effects & Shared Resources
- The AI MUST avoid designing systems that rely on $O(n^2)$ point-to-point communications between instances. For systems expected to scale beyond a few nodes, the AI MUST utilize UDP broadcast, multicast, publish/subscribe, or message queues.
- The AI MUST ruthlessly stress-test any shared resource (e.g., lock managers, cluster managers) and design fallback modes (e.g., optimistic locking) if the shared resource becomes a bottleneck or fails.

### Unbalanced Capacities & Flow Control
- The AI MUST design back-end systems to survive tsunamis of requests from higher-capacity front-end systems using Handshaking and Backpressure to throttle inbound traffic.
- The AI MUST implement Load Shedding at the edge (e.g., returning HTTP 503) when internal queues fill up or when average response time exceeds the SLA.

### Dogpiles & Force Multipliers
- The AI MUST NOT configure scheduled tasks, cron jobs, or batch processes to fire at exact round hours (e.g., exactly at midnight). The AI MUST apply a randomized clock slew/jitter to distribute the load.
- The AI MUST implement Governors on all automation and control plane scripts. Automation that destroys, shuts down, or modifies instances MUST include rate limiters, hysteresis (start fast, shut down slowly), and hard deceleration thresholds (e.g., pausing for human confirmation if attempting to terminate >20% of a cluster).

### Unbounded Result Sets
- The AI MUST NOT execute queries without a deterministic upper bound.
- The AI MUST enforce pagination and strict `LIMIT` clauses on all database queries and service requests returning collections.
- The AI MUST design APIs to require result-size parameters from clients.

# @Workflow
When developing, modifying, or reviewing a system component, the AI MUST strictly execute the following algorithm:

1. **Identify Integration Points**: Catalog every external API, database, and library the component interacts with.
2. **Apply Timeouts & Circuit Breakers**: For every identified integration point, enforce strict connection, read, and execution timeouts. Wrap risky integrations in Circuit Breakers.
3. **Analyze Result Sets**: Verify that all database queries and external requests explicitly limit the size of the returned data. Implement pagination or hard caps.
4. **Evaluate Resource Pools**: Ensure no thread can block infinitely waiting for a connection, lock, or thread pool slot. Set maximum wait times for all pools.
5. **Mitigate Dogpiles**: Audit any scheduled tasks, retries, or cache-miss logic. Inject randomized jitter into execution times and backoff calculations.
6. **Enforce Memory Hygiene**: Audit session data and in-memory caches. Evict large objects from sessions. Wrap cache payloads in Weak/Soft references.
7. **Simulate Hostile Input (Cynical Review)**: Review the logic under the assumption that the external service hangs, returns a completely different data type (e.g., HTML instead of JSON), or returns a dataset 1000x larger than expected. Add defensive guards.

# @Examples (Do's and Don'ts)

### Database Queries and Unbounded Result Sets
[DON'T]: Execute an open-ended query assuming the table is small.
```sql
-- Anti-pattern: Vulnerable to Unbounded Result Sets
SELECT id, name, status FROM transactions WHERE status = 'PENDING';
```
[DO]: Enforce strict limits and pagination.
```sql
-- Safe: Bounded Result Set
SELECT id, name, status FROM transactions WHERE status = 'PENDING' LIMIT 100 OFFSET 0;
```

### Network Timeouts
[DON'T]: Use default client configurations which often block infinitely.
```python
# Anti-pattern: Default requests.get can hang forever if the server accepts the connection but sends no data.
import requests
response = requests.get('https://api.vendor.com/data')
```
[DO]: Explicitly define connect and read timeouts.
```python
# Safe: Explicit timeouts for connect (3.0s) and read (10.0s).
import requests
try:
    response = requests.get('https://api.vendor.com/data', timeout=(3.0, 10.0))
except requests.exceptions.Timeout:
    # Handle timeout gracefully (e.g., fallback, fail fast)
    pass
```

### Liskov Substitution Principle and Thread Blocking
[DON'T]: Add `synchronized` to a subclass method implementing an interface that doesn't define it, causing hidden thread bottlenecks.
```java
// Anti-pattern: Hidden synchronization blocking all calling threads under load
public class RemoteAvailabilityCache implements GlobalObjectCache {
    @Override
    public synchronized Object get(String id) {
        // If this remote call hangs, ALL threads calling get() are blocked forever.
        return fetchFromRemote(id); 
    }
}
```
[DO]: Avoid global synchronization; use localized concurrency controls, timeouts, or immutable objects.
```java
// Safe: Non-blocking, isolated concurrency with timeouts
public class RemoteAvailabilityCache implements GlobalObjectCache {
    private final ConcurrentHashMap<String, Future<Object>> cache = new ConcurrentHashMap<>();

    @Override
    public Object get(String id) {
        try {
            return cache.computeIfAbsent(id, this::fetchAsync).get(2, TimeUnit.SECONDS);
        } catch (TimeoutException e) {
            return fallbackAvailability(id); // Fail fast
        }
    }
}
```

### Retry Logic and Dogpiles
[DON'T]: Use fixed-interval retries that cause synchronized traffic pulses.
```javascript
// Anti-pattern: Fixed retry creates a dogpile effect
async function fetchWithRetry() {
    try {
        return await fetchData();
    } catch (e) {
        setTimeout(fetchWithRetry, 5000); // Everyone retries exactly 5 seconds later
    }
}
```
[DO]: Use exponential backoff with randomized jitter.
```javascript
// Safe: Exponential backoff with jitter diffuses demand
async function fetchWithRetry(attempt = 1) {
    try {
        return await fetchData();
    } catch (e) {
        const baseDelay = Math.pow(2, attempt) * 1000;
        const jitter = Math.random() * 1000;
        setTimeout(() => fetchWithRetry(attempt + 1), baseDelay + jitter);
    }
}
```

### Response Parsing
[DON'T]: Blindly parse responses without checking content types.
```javascript
// Anti-pattern: Assumes the response is always JSON. A generic 503 HTML page will crash the parser.
const response = await fetch('https://api.example.com/data');
const data = await response.json(); 
```
[DO]: Verify the format before parsing.
```javascript
// Safe: Cynical parsing
const response = await fetch('https://api.example.com/data');
const contentType = response.headers.get("content-type");
if (contentType && contentType.includes("application/json")) {
    const data = await response.json();
} else {
    throw new Error("Invalid response format");
}
```