# @Domain

These rules apply when the AI is tasked with designing system architecture, developing or modifying distributed systems, writing network-bound code (APIs, microservices, remote integrations), implementing database queries and connection pools, managing concurrency/multithreading, or creating deployment/automation scripts. Trigger these rules whenever reliability, production-readiness, error handling, scaling, or fault tolerance are discussed.

# @Vocabulary

*   **Transaction**: An abstract unit of work processed by the system (e.g., "customer places order"), which may encompass many database transactions and external integrations.
*   **Impulse**: A rapid, sudden shock to the system (e.g., a massive spike in concurrent traffic from a flash mob).
*   **Stress**: A persistent force applied to the system over an extended period (e.g., slow responses from a third-party dependency).
*   **Strain**: The resulting change in system shape/behavior caused by stress (e.g., higher RAM usage, blocked threads).
*   **Fault**: A condition that creates an incorrect internal state in the software (a latent bug or unchecked edge case).
*   **Error**: Visibly incorrect behavior resulting from a fault.
*   **Failure**: An unresponsive system.
*   **Integration Point**: Any connection to an external system, database, or API. The number-one killer of systems.
*   **Chain Reaction**: A failure in one horizontally scaled node causes load to redistribute to peers, triggering their failure in turn.
*   **Cascading Failure**: A crack in one layer (e.g., a database) triggers a crack in a calling layer (e.g., application servers) due to unchecked integration points or blocked threads.
*   **Dogpile**: A concentrated surge of demand/load occurring simultaneously (e.g., servers booting up with cold caches, cron jobs firing at the exact same second).
*   **Force Multiplier**: Automation tools that lack human judgment and can rapidly execute destructive actions across an entire environment (e.g., an autoscaler shutting down all instances).
*   **Circuit Breaker**: A software pattern that wraps dangerous operations, tracks failures, and trips to an "open" state to prevent further calls to a failing integration point, allowing it time to recover.
*   **Bulkhead**: Partitioning a system (e.g., physical redundancy, segregated thread pools) so a failure in one compartment does not sink the entire system.
*   **Steady State**: A system's ability to run indefinitely without human intervention (fiddling) by strictly managing data accumulation, logs, and caches.
*   **Governor**: A stateful, time-aware mechanism that limits the speed/rate of automated actions (especially destructive ones) to allow for human intervention.
*   **Back Pressure**: Blocking or slowing down producers when queues are full to prevent unbound memory consumption and communicate load limits upstream.

# @Objectives

*   Treat all software as "cynical": Expect bad things to happen, distrust external systems, and put up internal barriers to protect the system from unexpected failures.
*   Prevent faults from becoming errors, and prevent errors from propagating into total system failures.
*   Ensure the system has "longevity" by strictly preventing memory leaks, unmanaged data growth, and unbounded resource consumption.
*   Isolate failures using safe failure modes (crumple zones/crackstoppers) so that core functionality survives even if peripheral systems crash.

# @Guidelines

## Integration Points & Network Resiliency
*   When implementing any external connection (API call, database query, RPC, file I/O), the AI MUST explicitly configure both connection timeouts and read/write timeouts. NEVER rely on default infinite/blocking timeouts.
*   When handling idle connections (especially database connection pools), the AI MUST implement keep-alives, dead connection detection, or validation queries to prevent firewalls from silently dropping TCP connections (the "5 A.M. problem").
*   When consuming third-party or vendor API libraries, the AI MUST assume the library contains unsafe blocking calls. Wrap these calls in asynchronous futures, thread pools, or circuit breakers if the library does not provide native timeout controls.

## Resource Management & Blocked Threads
*   When writing resource cleanup code (e.g., closing database connections, statements, or streams), the AI MUST anticipate that the `close()` method itself may throw an exception (e.g., `SQLException`). The AI MUST catch and handle exceptions on closure to prevent resource leaks that exhaust connection pools.
*   When configuring resource pools (database, threads, sockets), the AI MUST bound the pool size and MUST specify a maximum wait time for thread checkout. Threads MUST NOT block forever waiting for a resource.
*   When dealing with stateful user sessions, the AI MUST minimize session data. To prevent memory exhaustion from session floods (e.g., caused by bots ignoring cookies), the AI MUST avoid caching large objects in sessions. If large objects must be stored, the AI MUST use weak/soft references or off-heap/off-host storage (e.g., Memcached, Redis).

## Database & Data Growth (Steady State)
*   When writing database queries, the AI MUST NEVER return an unbounded result set. The AI MUST append limits, pagination, or top-N clauses to prevent catastrophic memory exhaustion and CPU spikes.
*   When designing systems that accumulate data (logs, database rows, in-memory caches), the AI MUST implement a mechanism to drain or purge the data at an equal or greater rate (e.g., log rotation, size-bounded LRU caches, TTL expirations, application-level data purging routines).

## Demand Control & Dogpile Prevention
*   When scheduling periodic tasks (cron jobs, automated polling, retry loops), the AI MUST add randomized jitter (clock slew) and exponential backoff to distribute load and prevent synchronized dogpiles.
*   When processing inbound requests, the AI MUST implement "Fail Fast" logic: validate inputs, check resource availability, and verify circuit breaker states *before* executing expensive logic or acquiring database locks.
*   When a service is overloaded, the AI MUST shed load early by returning immediate HTTP 503 (Service Unavailable) responses, rather than accepting requests into an unbounded queue that results in slow responses. 

## Architectural Patterns
*   When integrating with remote services, the AI MUST implement the **Circuit Breaker** pattern to track failures, open the circuit when thresholds are breached, and provide fallback responses, thereby preventing cascading failures and blocked threads.
*   When defining thread pools or service architectures, the AI MUST apply the **Bulkhead** pattern: separate critical workloads into dedicated thread pools or instance groups so that exhaustion in one workflow does not starve another.
*   When dealing with cross-system workflows, the AI MUST prefer **Decoupling Middleware** (async message queues, pub/sub) over synchronous request/reply integrations to achieve temporal and spatial isolation.
*   When designing automation or scaling scripts, the AI MUST implement a **Governor**: enforce hard limits or manual checkpoints on destructive actions (e.g., "Do not shut down more than 10% of instances automatically").

## Testing & Automation
*   When generating integration tests, the AI MUST generate **Test Harnesses** that explicitly simulate real-world hostility: dropped connections, extreme latency, garbage responses, and connection refusals. Do not merely mock the "happy path."

# @Workflow

1.  **Identify Integration Points**: Scan the requested code/architecture for any network boundaries, database connections, or file system accesses.
2.  **Enforce Timeouts**: For every integration point identified, explicitly configure connection, read, and write timeouts.
3.  **Apply Circuit Breakers & Bulkheads**: Wrap integration point calls in a Circuit Breaker. Allocate dedicated, bounded thread/connection pools (Bulkheads) for distinct external calls.
4.  **Secure Resource Cleanup**: Inspect `finally` blocks or resource destructors. Ensure that the failure of one `close()` operation does not skip the closure of subsequent resources.
5.  **Enforce Result Limits**: Inspect all database queries and API list endpoints. Inject strict pagination or `LIMIT` clauses.
6.  **Implement Demand Control**: Verify that cron jobs and retries utilize random jitter. Ensure the service performs early input/resource validation to Fail Fast.
7.  **Verify Steady State**: Check caching mechanisms for maximum size constraints/TTLs. Ensure file logging includes rotation policies.

# @Examples (Do's and Don'ts)

## Resource Cleanup
**[DON'T]** Leave cleanup vulnerable to exceptions thrown by `close()`, which leaks the connection.
```java
Connection conn = null;
Statement stmt = null;
try {
    conn = connectionPool.getConnection();
    stmt = conn.createStatement();
    // Do work
} finally {
    if (stmt != null) { stmt.close(); } // If this throws SQLException...
    if (conn != null) { conn.close(); } // ...this is never reached. Leak!
}
```

**[DO]** Handle exceptions independently during cleanup, or use modern language features (like try-with-resources) that guarantee cleanup.
```java
// Modern Java approach ensuring reliable cleanup
try (Connection conn = connectionPool.getConnection();
     Statement stmt = conn.createStatement()) {
    // Do work
} catch (SQLException e) {
    // Handle exception
}

// Or manually:
finally {
    if (stmt != null) {
        try { stmt.close(); } catch (SQLException e) { log.warn("Failed to close statement", e); }
    }
    if (conn != null) {
        try { conn.close(); } catch (SQLException e) { log.warn("Failed to close connection", e); }
    }
}
```

## Database Querying
**[DON'T]** Fetch unbounded results that can grow massively over time and cause OutOfMemory errors.
```sql
-- Anti-pattern: Unbounded result set
SELECT id, status, payload FROM transactions WHERE status = 'PENDING';
```

**[DO]** Always apply limits to queries, forcing the application to process data in safe chunks.
```sql
-- Pattern: Bounded result set
SELECT id, status, payload FROM transactions WHERE status = 'PENDING' LIMIT 100;
```

## Retry Logic & Dogpiles
**[DON'T]** Use fixed retries that synchronize failing clients into a dogpile.
```python
def fetch_data():
    for attempt in range(3):
        try:
            return make_network_call()
        except NetworkError:
            time.sleep(5) # Fixed sleep creates a dogpile effect
    raise Exception("Failed")
```

**[DO]** Implement exponential backoff with random jitter.
```python
import time
import random

def fetch_data():
    base_sleep = 1
    for attempt in range(3):
        try:
            return make_network_call()
        except NetworkError:
            # Exponential backoff with random jitter
            sleep_time = (base_sleep * (2 ** attempt)) + random.uniform(0, 1)
            time.sleep(sleep_time)
    raise Exception("Failed")
```

## Timeouts on Integration Points
**[DON'T]** Open network requests without specifying timeouts, leading to blocked threads if the server hangs.
```python
import requests

def get_external_data():
    # Anti-pattern: Missing timeout. Thread blocks indefinitely if server hangs.
    response = requests.get('https://api.thirdparty.com/data')
    return response.json()
```

**[DO]** Explicitly declare both connection and read timeouts.
```python
import requests

def get_external_data():
    # Pattern: Explicit connection (3.0s) and read (10.0s) timeouts
    response = requests.get('https://api.thirdparty.com/data', timeout=(3.0, 10.0))
    return response.json()
```