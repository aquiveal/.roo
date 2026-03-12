@Domain
These rules MUST be activated when the AI is tasked with diagnosing system bottlenecks, designing for high load, optimizing performance, implementing caching layers, configuring autoscaling policies, implementing CQRS/Event Sourcing, or deciding how to scale an existing microservice or monolithic architecture.

@Vocabulary
- **Vertical Scaling**: Scaling by allocating more powerful compute resources (CPU, memory, I/O) to an existing machine or instance.
- **Horizontal Duplication**: Scaling by deploying multiple identical instances of a service and distributing load among them (e.g., via load balancers or competing consumers).
- **Data Partitioning (Sharding)**: Scaling by dividing a workload or dataset into separate shards based on an attribute of the data (the partition key).
- **Functional Decomposition**: Scaling by extracting specific functionality into an independently deployable microservice to right-size its dedicated infrastructure.
- **CQRS (Command Query Responsibility Segregation)**: An architectural pattern that separates the data models used for reading from those used for writing.
- **Event Sourcing**: Projecting the current state of an entity by replaying a historical log of events.
- **Client-Side Caching**: Storing cached data within the consuming process to entirely avoid network round-trips to the origin.
- **Server-Side Caching**: Caching maintained by the origin microservice (e.g., reverse proxy, Redis, read replicas) to prevent expensive internal regeneration of data.
- **Request Caching**: Caching the exact final computed response for a specific request.
- **TTL (Time To Live)**: A cache invalidation strategy where data expires after a predefined time duration.
- **Conditional GET**: An HTTP caching mechanism utilizing `ETag` and `If-None-Match` headers to verify if a client's cached resource is still fresh, avoiding recalculation costs.
- **Notification-Based Invalidation**: An asynchronous invalidation strategy where the origin fires events (e.g., via a message broker) to inform consumers that cached data must be refreshed or evicted.
- **Write-Through Cache**: A caching strategy where the cache and the origin data are updated in the same transactional boundary.
- **Write-Behind Cache**: A caching strategy where data is written to the cache first and asynchronously synchronized to the origin (high risk of data loss).
- **Cache Poisoning**: A state where intermediate caches (ISPs, browsers, CDNs) permanently hold stale data due to misconfigured cache headers (e.g., `Expires: Never`).
- **Predictive Autoscaling**: Scaling resources based on known historical usage trends and time schedules.
- **Reactive Autoscaling**: Scaling resources dynamically based on real-time metrics (e.g., CPU load, failure rates).

@Objectives
- The AI MUST treat premature optimization as an anti-pattern; no scaling mechanism shall be proposed without an established baseline via automated load testing.
- The AI MUST progress through the four axes of scaling from least complex (Vertical/Horizontal) to most complex (Partitioning/Functional Decomposition).
- The AI MUST design microservices to be stateless to seamlessly support horizontal duplication without relying on sticky sessions.
- The AI MUST strictly limit the number of caching layers to prevent unpredictable data staleness and cache poisoning.
- The AI MUST encapsulate complex scaling patterns (like CQRS and Event Sourcing) strictly within the internal implementation of a microservice, completely hidden from external consumers.

@Guidelines

### 1. The Four Axes of Scaling Strategy
- **Vertical Scaling**: The AI MUST first evaluate if vertical scaling is sufficient before introducing distributed complexity. Note that vertical scaling requires multi-core optimized code to truly benefit from modern CPU upgrades.
- **Horizontal Duplication**: When implementing horizontal scaling, the AI MUST use a load balancer or a message broker (competing consumers). The AI MUST NOT use sticky sessions; services must be stateless.
- **Data Partitioning**: When partitioning data for write-heavy workloads, the AI MUST select a highly uniformly distributed partition key (e.g., unique customer UUIDs). The AI MUST NOT use attributes with natural skew (e.g., alphabetical names, geographic regions with vastly different user counts) for load-distribution partitioning.
- **Functional Decomposition**: The AI MUST treat functional decomposition (extracting a new microservice) as the most expensive scaling option. It MUST only be proposed when vertical scaling, horizontal duplication, and data partitioning have been exhausted, or when required for organizational autonomy.

### 2. Caching Implementation Rules
- **The Golden Rule of Caching**: The AI MUST minimize the number of caching layers between the origin and the client to exactly one whenever possible. The AI MUST explicitly flag nested caches as an architectural risk.
- **Selecting Cache Location**: 
  - Propose **Client-Side Caching** for maximum latency reduction and robustness (surviving origin outages). Note to user: this risks data inconsistency between different clients.
  - Propose **Server-Side Caching** when all consumers need a consistent view of the data, accepting the cost of a network round-trip.
- **Selecting Cache Invalidation**:
  - Use **TTL/Expires** for simple, low-criticality data.
  - Use **Conditional GETs (ETags)** when network bandwidth is cheap but server-side payload generation is computationally expensive.
  - Use **Notification-Based Invalidation** (pub/sub) when the window of staleness must be kept exceptionally small. Note to user: require heartbeat events to ensure the notification mechanism hasn't failed.
  - NEVER use **Write-Behind Caching** unless the user explicitly accepts the risk of data loss.
- **Cache Poisoning Prevention**: The AI MUST NEVER output HTTP headers that dictate infinite caching (e.g., `Expires: Never`). Cache control headers MUST have explicit, finite lifetimes.

### 3. Architectural Patterns & Complexity
- **CQRS and Event Sourcing**: If the AI implements CQRS or Event Sourcing to scale read/write models independently, these patterns MUST NOT leak into the microservice's external API contract. They are strictly internal implementation details. The AI MUST recommend simpler approaches (like database read replicas) before proposing full CQRS.
- **Premature Optimization**: The AI MUST prompt the user to create automated performance/load tests to prove a bottleneck exists before implementing caching, sharding, or functional decomposition.

### 4. Autoscaling Configurations
- **Scaling Triggers**: The AI MUST configure autoscaling to react to both load (e.g., CPU spikes) and failure (e.g., replacing dead instances to maintain a minimum threshold).
- **Scale Down Caution**: The AI MUST configure autoscaling policies to scale up aggressively (fast) but scale down cautiously (slow/delayed) to prevent capacity flapping and accommodate slow instance spin-up times.

@Workflow
When tasked with resolving a system bottleneck or scaling a microservice, the AI MUST follow this exact sequence:

1. **Establish the Baseline**: Query the user for existing performance metrics or instruct them to write and execute an automated load test to quantify the current limit (e.g., latency vs. throughput).
2. **Evaluate the Constraints**: Determine if the system is CPU-bound, memory-bound, read-heavy, or write-heavy.
3. **Traverse the Scaling Axes**:
   - *Step 3a*: Propose **Vertical Scaling** (easiest fix). If rejected/maxed out, proceed to 3b.
   - *Step 3b*: Propose **Horizontal Duplication** (adding instances + load balancer/queue). If the workload requires strict session state or is database-write-constrained, proceed to 3c.
   - *Step 3c*: Propose **Data Partitioning**. Define a uniformly distributed partition key (e.g., UUID). If the bottleneck is due to conflicting operational types, proceed to 3d.
   - *Step 3d*: Propose **Functional Decomposition** or CQRS. Extract the bottlenecked functionality into its own deployable unit.
4. **Design Caching Strategy** (If read-latency is the constraint):
   - Choose ONE caching location (Client-side OR Server-side).
   - Define the explicit invalidation mechanism (TTL, ETag, Notification).
5. **Configure Autoscaling**: Generate infrastructure code (e.g., Terraform, Kubernetes HPA) to scale the duplicated/partitioned resources dynamically, enforcing rapid scale-up and delayed scale-down policies.

@Examples (Do's and Don'ts)

### Data Partitioning Keys
- [DO]: Partition data based on a highly unique, evenly distributed identifier to prevent hot spots.
```python
// DO: Good partition key
def get_database_shard(customer_uuid):
    shard_count = 4
    return hash(customer_uuid) % shard_count
```
- [DON'T]: Partition data based on naturally skewed attributes.
```python
// DON'T: Bad partition key (Alphabetical names are unevenly distributed)
def get_database_shard(customer_last_name):
    if customer_last_name[0].upper() < 'N':
        return 1
    return 2
```

### Horizontal Duplication
- [DO]: Use stateless endpoints that allow any instance to serve any request.
```nginx
# DO: Stateless load balancing
upstream order_service {
    server instance1.example.com;
    server instance2.example.com;
}
```
- [DON'T]: Rely on sticky sessions, which destroy the ability to horizontally distribute load effectively.
```nginx
# DON'T: Sticky sessions couple clients to specific instances
upstream order_service {
    ip_hash; # Anti-pattern for microservices
    server instance1.example.com;
    server instance2.example.com;
}
```

### Caching Headers
- [DO]: Provide specific, finite lifetimes and utilize ETags for conditional fetching.
```http
// DO: Finite caching with validation
HTTP/1.1 200 OK
Cache-Control: max-age=300, must-revalidate
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```
- [DON'T]: Emit infinite cache headers that can permanently poison intermediate caches.
```http
// DON'T: Infinite caching leads to cache poisoning
HTTP/1.1 200 OK
Expires: Thu, 31 Dec 2099 23:59:59 GMT
Cache-Control: max-age=315360000
```

### Autoscaling
- [DO]: Scale up fast, scale down slow.
```yaml
# DO: Kubernetes HPA with cautious scale-down
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300 # Wait 5 minutes before scaling down
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60
  scaleUp:
    stabilizationWindowSeconds: 0 # Scale up immediately
```
- [DON'T]: Scale down aggressively, causing capacity flapping.
```yaml
# DON'T: Immediate scale down causes flapping
behavior:
  scaleDown:
    stabilizationWindowSeconds: 0 
```