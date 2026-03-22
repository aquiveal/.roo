@Domain
These rules MUST be activated when the user requests assistance with scaling systems, handling increased architectural load, improving system performance or latency, implementing caching strategies, designing database partitioning (sharding), adding read replicas, configuring autoscaling, or evaluating the Command Query Responsibility Segregation (CQRS) and Event Sourcing patterns. 

@Vocabulary
- **Vertical Scaling**: Scaling by provisioning a larger, more powerful machine (more CPU, memory, I/O). 
- **Horizontal Duplication**: Scaling by deploying multiple instances of the same service or data store to distribute load (e.g., using a load balancer, read replicas, or the competing consumer pattern).
- **Data Partitioning (Sharding)**: Scaling by dividing workload or data across multiple isolated nodes based on a specific attribute of the data (the partition key).
- **Functional Decomposition**: Scaling by extracting specific functionality into independent microservices to allow targeted, independent scaling of that specific workload.
- **The Scale Cube**: A mental model comprising Functional Decomposition, Horizontal Duplication, and Data Partitioning (augmented with Vertical Scaling as a fourth axis).
- **CQRS (Command Query Responsibility Segregation)**: An architectural pattern where responsibilities for reading (queries) and writing (commands) data are separated into different models and processes.
- **Event Sourcing**: A pattern where the state of an entity is projected by replaying a history of immutable events related to that entity.
- **Client-Side Caching**: Storing cached data inside or alongside the consuming microservice to avoid network calls to the origin.
- **Server-Side Caching**: Storing cached data inside the boundary of the origin microservice, transparent to the consumer.
- **Request Cache**: Caching the exact, specific response to a distinct request to avoid all recalculation and downstream lookups.
- **TTL (Time to Live)**: A mechanism for cache invalidation where data is considered stale after a fixed period of time.
- **Conditional GET**: An HTTP caching mechanism using ETags where a client requests a resource only if it has changed (`If-None-Match`).
- **Notification-Based Invalidation**: An event-driven caching strategy where the origin broadcasts events when data changes to proactively invalidate subscriber caches.
- **Write-Through Cache**: A caching pattern where the cache and the origin data store are updated simultaneously.
- **Write-Behind Cache**: A caching pattern where the cache is updated first, and the origin data store is updated asynchronously later.
- **Predictive Autoscaling**: Scaling resources based on known, historical time-based trends (e.g., time of day).
- **Reactive Autoscaling**: Scaling resources dynamically in response to immediate load metrics or instance failures.

@Objectives
- Base all scaling decisions on identified constraints: prioritize scaling mechanisms that directly address the specific bottleneck (e.g., read vs. write load, CPU vs. network latency).
- Prioritize simple, low-risk scaling methods (Vertical, Horizontal) before recommending complex methods (Partitioning, CQRS, Microservice Decomposition).
- Prevent premature optimization by mandating baseline load testing and experimentation before architectural changes.
- Implement caching judiciously as a targeted performance/robustness optimization, minimizing the number of cache layers to preserve data freshness and system reasoning.
- Ensure autoscaling rules prioritize system availability and handle scale-down actions conservatively.

@Guidelines

### 1. Scaling Axis Selection
- The AI MUST evaluate scaling solutions in order of increasing complexity: Vertical Scaling -> Horizontal Duplication -> Data Partitioning -> Functional Decomposition.
- **Vertical Scaling**:
  - Recommend for immediate, short-term relief without code changes.
  - The AI MUST warn the user that moving to a larger machine often yields more CPU *cores*, not faster clock speeds. If the application is CPU-bound, warn that code MUST be capable of concurrent/multi-threaded execution to benefit.
  - Warn that vertical scaling does NOT improve robustness/redundancy.
- **Horizontal Duplication**:
  - Recommend for read-heavy workloads (e.g., database read replicas) and stateless application nodes.
  - The AI MUST advise avoiding "sticky session" load balancing, as it introduces scaling and robustness complications.
- **Data Partitioning**:
  - Recommend for write-constrained transactional workloads.
  - The AI MUST require a highly considered partition key that guarantees an even distribution of load (e.g., unique customer IDs, geographic regions). The AI MUST explicitly reject arbitrary or imbalanced keys (e.g., alphabetical sorting by surname).
  - The AI MUST warn that queries spanning multiple partitions are complex and may require asynchronous map/reduce jobs or separate read stores.
- **Functional Decomposition**:
  - Recommend when specific, isolated workloads have wildly different scaling requirements or infrastructural costs than the rest of the monolith.
  - The AI MUST remind the user that this drastically increases architectural complexity.

### 2. CQRS and Event Sourcing
- The AI MUST treat CQRS and Event Sourcing as advanced, highly complex scaling patterns.
- If the user proposes CQRS, the AI MUST first suggest simpler alternatives (e.g., read replicas) unless the user's requirements explicitly mandate divergent read/write data models.
- **Encapsulation**: If CQRS or Event Sourcing is implemented, the AI MUST ensure these patterns remain internal implementation details of the microservice. Consumers MUST NOT be aware of the separated read/write models.

### 3. Caching Strategies
- **The Golden Rule of Caching**: The AI MUST strive to implement caching in as *few* places as possible (ideally zero, unless proven necessary). The AI MUST actively prevent nested caching architectures (e.g., client-side cache reading from a server-side cache), which obscure data freshness.
- **Location Selection**:
  - *Client-Side*: Recommend for maximum latency reduction and origin-failure robustness. If data inconsistency across multiple clients is unacceptable, recommend a *Shared Client-Side Cache* (e.g., Redis).
  - *Server-Side*: Recommend for transparently speeding up origin queries for all consumers, acknowledging it does not eliminate the network hop.
  - *Request Cache*: Recommend for highly expensive, easily cacheable aggregate calculations (e.g., "Top 10 Best Sellers").
- **Invalidation Strategy**:
  - *TTL*: Recommend for simple, blunt invalidation. Base TTL durations on data volatility (e.g., short TTL for fast-moving stock, long TTL for slow-moving stock).
  - *Conditional GETs*: Recommend when network hops are acceptable, but server-side resource generation is expensive. Enforce the use of ETags and `If-None-Match` HTTP headers.
  - *Notification-Based*: Recommend when the tolerance for stale data is near zero. The AI MUST enforce the inclusion of "heartbeat" events to detect silent failures in the notification stream.
  - *Write-Behind*: The AI MUST warn against write-behind caches in microservices unless the user explicitly accepts the high risk of data loss before origin persistence.
- **Cache Poisoning**: The AI MUST NOT set `Expires: Never` or infinite TTLs on HTTP resources, especially when intermediate proxies, CDNs, or browser caches are involved.

### 4. Autoscaling
- The AI MUST recommend mixing *Predictive Scaling* (for known traffic cycles) and *Reactive Scaling* (for unexpected spikes and node failures).
- The AI MUST verify that application spin-up time (cold starts) is sufficiently fast to handle reactive scaling. If spin-up is slow, the AI MUST recommend maintaining excess idle capacity.
- The AI MUST enforce conservative scale-down rules to prevent thrashing and ensure sufficient capacity during fluctuating traffic.

### 5. Architectural Evolution
- The AI MUST NOT attempt to build a system for "massive scale" upfront. Systems MUST be designed to solve current problems while remaining malleable enough to evolve. 

@Workflow
When tasked with resolving a scaling, load, or performance issue, the AI MUST follow this exact sequence:

1. **Analyze the Constraint**: Identify the specific bottleneck. Is it read-heavy database contention? Write-heavy contention? Network latency? Compute exhaustion?
2. **Establish the Baseline**: Query the user on whether load testing and performance metrics exist. If not, the AI MUST instruct the user to build automated load tests and monitor baselines before applying architectural changes.
3. **Evaluate Simple Scaling Axes**:
   - Assess Vertical Scaling (Can we just rent a bigger/memory-optimized cloud instance?).
   - Assess Horizontal Duplication (Can we add a load balancer and more instances? Can we add a read replica?).
4. **Evaluate Advanced Scaling Axes** (If simple scaling is insufficient):
   - For write constraints, evaluate Data Partitioning. Propose a balanced partition key.
   - For isolated expensive features, evaluate Functional Decomposition.
5. **Evaluate Caching** (If latency or read-heavy load is the core issue):
   - Propose the cache location (Client, Server, Shared, Request).
   - Define the exact cache invalidation mechanism (TTL, ETag, Events).
6. **Formulate the Solution**: Present the recommended architectural shift, explicitly noting the new complexities (e.g., cross-shard querying, cache staleness, multi-core refactoring) the user must manage.

@Examples (Do's and Don'ts)

- **[DO]** Use high-cardinality, evenly distributed identifiers for data partitioning. 
  *Example:* Partitioning a customer database using a randomly generated internal `customer_uuid`.
- **[DON'T]** Use arbitrary or unbalanced human identifiers for partitioning.
  *Example:* Partitioning based on the first letter of a customer's surname (A-M vs N-Z), as this will cause extreme data and load skew.

- **[DO]** Hide CQRS implementation details behind a unified microservice API.
  *Example:* A `Sales` microservice routes `POST /orders` to its internal write-model, and `GET /orders` to its internal read-model, exposing a single REST interface to the outside world.
- **[DON'T]** Force consumers to understand your CQRS architecture.
  *Example:* Exposing two separate microservices, `Sales-Read-Service` and `Sales-Write-Service`, to all upstream consumers.

- **[DO]** Use HTTP `ETag` and `If-None-Match` headers for Conditional GETs.
  *Example:* The client sends `If-None-Match: "o5t6fkd2sa"`. The microservice evaluates if the resource hash has changed. If not, it returns `304 Not Modified` to save processing time and bandwidth.
- **[DON'T]** Nest caches without a clear understanding of cumulative data staleness.
  *Example:* A client-side cache with a 5-minute TTL reading from a server-side cache with a 5-minute TTL, resulting in data that is up to 10 minutes out of date.

- **[DO]** Implement heartbeat events in notification-based cache invalidation.
  *Example:* An `Inventory` service emits a `Stock_Unchanged_Heartbeat` every 60 seconds over the message broker. If the `Recommendation` service misses three heartbeats, it disables its client-side cache to prevent serving permanently stale data.
- **[DON'T]** Implement Write-Behind caches for critical business data without accepting data loss risk.
  *Example:* Writing financial transactions to an in-memory Write-Behind cache before persisting to the database. If the cache node crashes, the financial data is permanently lost.