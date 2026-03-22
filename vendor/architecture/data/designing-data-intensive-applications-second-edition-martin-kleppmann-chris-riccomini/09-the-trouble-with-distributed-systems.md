### @Domain
Triggered when the user requests architecture design, code review, debugging, or implementation of distributed systems, microservices, network communication (RPC/REST APIs), data replication, or fault-tolerant infrastructure.

### @Vocabulary
- **Distributed System:** A system involving several machines (nodes) communicating via a network, inherently subject to network delays, interruptions, and partial failures.
- **Observability:** The practice of collecting and querying execution data (metrics and individual events) to diagnose problems in distributed systems.
- **Tracing Tools:** Infrastructure (e.g., OpenTelemetry, Zipkin, Jaeger) that tracks which client called which server for which operation, and how long each call took.
- **Location Transparency:** A flawed RPC abstraction that attempts to make a remote network request look identical to a local function call.
- **Metastable Failure:** A vicious cycle where a system remains in an overloaded state (e.g., due to a retry storm) even after the initial load spike is reduced, requiring a hard reset.
- **Exponential Backoff and Jitter:** A retry strategy that increases the delay between retries and adds randomization to prevent retry storms.
- **Circuit Breaker / Token Bucket:** Client-side algorithms used to temporarily halt requests to a service that has recently timed out or returned errors.
- **Load Shedding:** A server-side proactive measure to reject incoming requests when approaching overload.
- **Backpressure:** A mechanism where a server explicitly instructs clients to slow down their request rate.
- **Split Brain:** A dangerous state where two nodes independently believe they are the leader, risking data corruption if both accept writes.
- **Eventual Consistency:** A state in asynchronously replicated systems where a follower may temporarily serve stale data until it catches up with the leader.
- **Read-After-Write (Read-Your-Writes) Consistency:** A guarantee that users will always see their own recently submitted updates.
- **Monotonic Reads:** A guarantee that if a user makes successive reads, they will not observe time going backward (e.g., seeing older data after having seen newer data).
- **Consistent Prefix Reads:** A guarantee that causally related writes are observed in the exact order they were applied.
- **Version Vector / Logical Clock:** A collection of version numbers from all replicas used to capture causal dependencies and accurately detect concurrent writes, avoiding reliance on physical time.

### @Objectives
- Treat all network boundaries as unreliable, anticipating timeouts, dropped packets, and unpredictable latency.
- Prevent cascading failures and metastable states by enforcing strict overload protection (circuit breakers, load shedding, backpressure).
- Maintain system-wide observability through distributed tracing to ensure complex service interactions remain diagnosable.
- Ensure data consistency and prevent replication anomalies without relying on flawed abstractions like location transparency or synchronized real-time clocks.
- Prioritize data locality by moving computation to the data rather than transferring large data payloads across the network.

### @Guidelines
- **Network Call Abstraction:** The AI MUST NOT abstract network calls to look identically like local function calls (e.g., hiding them behind local getters/setters). Network boundaries MUST be explicit, exposing their asynchronous and fallible nature.
- **Timeout Handling:** The AI MUST treat a network timeout as an "unknown state." The AI MUST NOT assume the request failed to reach the server, nor assume it succeeded.
- **Retry Safety (Idempotence):** The AI MUST NOT implement automatic retries on network requests unless the target operation is explicitly idempotent or utilizes an application-level deduplication mechanism (e.g., an idempotency key).
- **Overload Mitigation (Client-Side):** When implementing clients that call external services, the AI MUST utilize exponential backoff with jitter for retries. The AI MUST implement a circuit breaker or token bucket algorithm to halt traffic to failing services.
- **Overload Mitigation (Server-Side):** When implementing server endpoints, the AI MUST include load shedding to drop requests when resources (CPU/memory/queue size) reach critical thresholds, and MUST return backpressure responses (e.g., HTTP 429) to throttle clients.
- **Observability Integration:** When generating code for microservices or distributed components, the AI MUST inject correlation IDs and distributed tracing spans (using OpenTelemetry, Zipkin, or Jaeger patterns) across all network boundaries.
- **Data Locality:** When operating on large volumes of data, the AI MUST design the architecture to bring the computation to the node that stores the data, rather than transferring the data across the network to a separate processing node.
- **Distributed Consistency:** The AI MUST NOT default to using distributed transactions across microservices, as they run counter to service independence. Consistency across services MUST be handled via asynchronous event streams, compensations (Sagas), or explicit application logic.
- **Replication Lag Anomalies:** When reading from asynchronous replicas, the AI MUST implement safeguards against replication lag:
  - For *Read-After-Write*, the AI MUST route a user's reads to the leader (or a synchronous follower) for a specified duration after they perform a write, or track the logical timestamp of the user's last write.
  - For *Monotonic Reads*, the AI MUST hash the user ID to ensure a specific user consistently reads from the same replica.
- **Concurrent Write Resolution:** The AI MUST NOT use real-time system clocks (e.g., `System.currentTimeMillis()`) to resolve distributed concurrent writes (Last-Write-Wins), as clock skew will lead to silent data loss. The AI MUST use Version Vectors, logical clocks, or Conflict-Free Replicated Data Types (CRDTs) to detect and resolve concurrency.

### @Workflow
1. **Boundary Identification:** Identify all network boundaries in the requested architecture or code. Mark them as highly susceptible to variable latency and partial failure.
2. **Failure Mode Definition:** For each network boundary, define the timeout threshold. Explicitly write the fallback or error-handling logic for the "timeout (unknown)" state.
3. **Idempotence & Retry Engineering:** If retries are required, generate the idempotency mechanism (e.g., passing a unique request ID). Wrap the network call in an exponential backoff + jitter loop, protected by a circuit breaker.
4. **Overload Protection:** Implement server-side constraints. Add queue size limits, load shedding checks, and backpressure HTTP status codes.
5. **Observability Injection:** Add tracing context headers to the outbound request and extract them on the inbound server side. Wrap the execution in an observability span.
6. **State & Consistency Validation:** Evaluate the replication model. If operating in a multi-leader or leaderless, distributed context, replace physical timestamps with logical Version Vectors for conflict resolution. If using asynchronous single-leader replication, apply Read-Your-Writes routing logic for the client.

### @Examples (Do's and Don'ts)

**[DO]** Explicitly handle network failures with idempotency, exponential backoff, jitter, and circuit breakers.
```python
import time
import random
import requests
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
def call_distributed_service(payload, idempotency_key):
    max_retries = 3
    base_delay = 0.5

    for attempt in range(max_retries):
        try:
            # Observability: passing trace context and idempotency key
            headers = {
                "X-Idempotency-Key": idempotency_key,
                "X-Trace-Id": get_current_trace_id()
            }
            response = requests.post("https://api.internal/v1/resource", json=payload, headers=headers, timeout=2.0)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                # Timeout means unknown state; do not assume failure or success
                raise UnknownNetworkStateException("Service unreachable or timed out.") from e
            
            # Exponential backoff with jitter
            delay = (base_delay * (2 ** attempt)) + random.uniform(0, 0.1)
            time.sleep(delay)
```

**[DON'T]** Use location transparency (flawed RPC) that mimics local function calls and assumes timeouts equal failure.
```python
# ANTI-PATTERN: Hides network reality, no idempotency, instant retry storm
def update_user_profile(user_id, data):
    while True:
        try:
            # Looks like a local call, but makes a network request under the hood
            UserRPCClient.update(user_id, data) 
            break # Success
        except TimeoutError:
            # DANGEROUS: Assumes timeout means it didn't execute.
            # DANGEROUS: Immediate retry without backoff causes metastable failures.
            continue 
```

**[DO]** Use Version Vectors / Logical Clocks to detect concurrent writes in distributed systems.
```json
// Example of a data payload using Version Vectors to track causality
{
  "key": "shopping_cart_123",
  "value": ["milk", "eggs"],
  "version_vector": {
    "replica_A": 4,
    "replica_B": 1,
    "replica_C": 2
  }
}
```

**[DON'T]** Use physical system clocks for conflict resolution (Last-Write-Wins) across distributed nodes.
```json
// ANTI-PATTERN: Vulnerable to clock skew. A slower clock on a node will cause its writes to be silently discarded.
{
  "key": "shopping_cart_123",
  "value": ["milk", "eggs"],
  "last_updated_system_time": 1698345123999 
}
```