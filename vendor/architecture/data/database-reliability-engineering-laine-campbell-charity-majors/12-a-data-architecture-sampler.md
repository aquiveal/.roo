@Domain
These rules MUST be activated when the AI is tasked with designing, evaluating, or refactoring data architectures, database infrastructure pipelines, Data Access Layers (DAL), database proxy configurations, caching strategies, event/messaging system integrations, or distributed data processing patterns (such as Lambda, Kappa, Event Sourcing, or CQRS).

@Vocabulary
- **Frontend Datastore (OLTP):** The primary database serving real-time, highly concurrent, low-latency user transactions.
- **Data Access Layer (DAL):** The business logic tier abstraction that simplifies access to persistent datastores, hiding database complexity from software engineers.
- **Data Access Object (DAO):** A DAL implementation that maps application calls to the database, allowing for discrete testing and stubbing.
- **Object-Relational Mapper (ORM):** A DAL implementation that maps relational models to object models; prone to creating impedance, holding long transactions, and generating convoluted queries.
- **L4 Proxy:** A Layer 4 network transport proxy that distributes traffic based on IP addresses and ports without understanding database protocols.
- **L7 Proxy:** A Layer 7 application/HTTP proxy that understands database protocols, enabling query rewriting, caching, health checking, and lag-aware routing.
- **Load Shedding:** Using a proxy layer as a connection queue to hold a large number of connections while only allowing a safe threshold to do work in the database.
- **Thundering Herd:** A failure state where multiple cache servers simultaneously have frequently accessed data invalidated, causing a massive concurrent spike in read requests to the persistence datastore.
- **Doublewrite:** A caching strategy where data is written to both the cache and persistence store simultaneously; highly fragile without two-phase commits.
- **Write-through:** A caching strategy where data is written to the cache first and persisted to disk asynchronously.
- **Lambda Architecture:** A big data processing architecture utilizing three layers: batch processing (e.g., Hadoop), real-time processing (e.g., Storm/Spark), and a serving/query layer.
- **Kappa Architecture:** A simplified big data architecture that eliminates the batch layer in favor of a single stream-processing layer fed by an immutable append-only log (e.g., Kafka).
- **Event Sourcing:** A data modeling pattern where changes to entities are saved as a sequence of immutable state changes (events) in an event store, rather than using destructive mutations.
- **CQRS (Command-Query-Responsibility Segregation):** An architecture where the read/query models and write/command models are physically or logically separated, often utilizing different optimized datastores for each view.

@Objectives
- Guarantee low-latency writes and queries for frontend datastores while maintaining high availability (HA) and low Mean Time to Recover (MTTR).
- Decouple application logic from datastore complexity using robust Data Access Layers (DAL) while mitigating the risks of ORM impedance.
- Optimize database traffic and scalability using strictly evaluated L4 or L7 proxies, leveraging load shedding and query caching.
- Prevent data loss and processing duplication in event/messaging systems by enforcing idempotent consumers and data validation pipelines.
- Protect persistence datastores from cache invalidation spikes (Thundering Herds) using timeouts and proxy tiers.
- Select the appropriate large-scale data architecture (Lambda, Kappa, Event Sourcing, CQRS) strictly based on the system's tolerance for complexity, latency, and read/write optimization needs.

@Guidelines

### Frontend Datastores
- When designing primary transactional systems, the AI MUST configure the datastore to prioritize fast queries, high concurrency, and data integrity (OLTP patterns).
- When selecting a frontend datastore, the AI MUST ensure it supports low-latency writes/queries, high availability, low MTTR, and scales efficiently with application traffic.

### Data Access Layer (DAL)
- When structuring business logic, the AI MUST separate persistence logic into a dedicated Data Access Layer (DAL) to allow for discrete testing and database stubbing.
- When implementing a DAL, the AI SHOULD favor Data Access Objects (DAOs) using direct data access code (e.g., JDBC) to maintain granular control over query performance.
- When an ORM is mandated, the AI MUST explicitly design mitigations for ORM-specific risks: holding transactions too long, generating unnecessary/excessive queries, and obfuscating database constraints.

### Database Proxies
- When minimal latency is the absolute highest priority and simple algorithmic traffic distribution is sufficient, the AI MUST specify an L4 (Layer 4) proxy.
- When the architecture requires health checking, read/write splitting, query rewriting, result caching, or lag-aware routing, the AI MUST specify an L7 (Layer 7) proxy and explicitly document the latency trade-off.
- When protecting frontend datastores from connection exhaustion, the AI MUST implement load shedding at the proxy layer by queueing incoming connections and strictly limiting active backend database connections.

### Event and Message Systems
- When transactions require downstream processing (e.g., analytics, fraud detection, CDN uploads), the AI MUST decouple these workloads from the frontend datastore using event/messaging systems (e.g., Kafka, RabbitMQ).
- When designing event consumers, the AI MUST enforce idempotency to ensure that duplicated message deliveries do not corrupt downstream state.
- When data loss is unacceptable in an event pipeline, the AI MUST design an audit consumer that writes validation copies back to the bus to compare against original messages.

### Caches and Memory Stores
- When implementing a caching tier, the AI MUST explicitly define the population strategy and its mitigations:
  1. **Post-write caching:** Use for static data; AI MUST account for the risk of stale data.
  2. **Doublewrite caching:** Write to both DB and cache; AI MUST implement post-write validation or two-phase commits to prevent fractured state.
  3. **Write-through caching:** Write to cache first; AI MUST implement event logging to reconstruct writes if the cache crashes before asynchronous disk persistence.
- When designing cache expiration, the AI MUST mitigate "Thundering Herd" scenarios by applying randomized/offset time-outs to cache entries or by placing a proxy cache layer in front of the persistence datastore.

### Lambda vs. Kappa Architectures
- When a system requires both long-running historical computation and "good enough" real-time views, and the organization can afford maintaining two separate codebases, the AI MUST implement a Lambda architecture.
- When a system requires streamlined infrastructure and single-codebase maintainability, the AI MUST implement a Kappa architecture utilizing an append-only immutable log (e.g., Kafka) and a unified stream processing layer.

### Event Sourcing and CQRS
- When designing an Event Sourced system, the AI MUST log all entity mutations as a sequence of state changes rather than destructive updates (overwrites).
- When using Event Sourcing, the AI MUST implement mechanisms to manage schema evolution, as new schemas can invalidate previously stored historical events.
- When a system's read and write workloads require vastly different performance optimizations (e.g., search indexing vs. append-only logs), the AI MUST implement CQRS (Command-Query-Responsibility Segregation).
- When implementing CQRS, the AI MUST ensure that write commands return sufficient data (e.g., success/failure, errors, and version numbers) so the application can accurately query the newly generated read model.
- When evaluating CQRS, the AI MUST NOT apply it globally to simple CRUD applications; it MUST explicitly segregate only the domains that strictly require multiple views to avoid unnecessary architectural complexity.

@Workflow
1. **Analyze Frontend Requirements:** Evaluate the primary application traffic to define the Frontend Datastore constraints (OLTP, concurrency, latency limits).
2. **Define the Data Access Layer (DAL):** Isolate database interactions into DAOs. If an ORM is required, explicitly generate rules to monitor and kill long-running transactions and optimize generated queries.
3. **Select and Configure Proxy Routing:** Evaluate OSI layer needs. Choose L4 for raw speed or L7 for protocol-aware routing (read/write splits, caching). Implement connection queueing (load shedding).
4. **Architect Asynchronous Eventing:** Map all post-transaction workflows (analytics, emails) to an event bus (e.g., Kafka). Validate that all consumer logic is idempotent.
5. **Formulate Caching Strategy:** Determine the cache population method (post-write, doublewrite, write-through). Apply jitter/offsets to TTLs to completely prevent Thundering Herds.
6. **Evaluate Advanced Data Patterns:** Determine if the data volume and view requirements necessitate big data pipelines (Lambda/Kappa) or multi-model views (Event Sourcing/CQRS). Apply only to specific domains requiring them.

@Examples

### Data Access Layer (DAL)
- **[DO]** Use Data Access Objects (DAOs) that explicitly declare required columns, ensuring queries are highly optimized and easily testable via stubs.
- **[DON'T]** Use an ORM configuration that blindly issues `SELECT *` across multiple joined tables and holds the transaction open while the application processes the business logic.

### Database Proxies
- **[DO]** Deploy an L7 proxy to intercept read-only queries and route them exclusively to replicas that have zero replication lag.
- **[DON'T]** Point application servers directly to a database cluster without a proxy layer, risking connection exhaustion under heavy load.

### Caching and Thundering Herds
- **[DO]** Add randomized offsets (jitter) to cache expiration times (TTLs) so that concurrent cache misses are staggered, protecting the persistence database.
- **[DON'T]** Set a hard, synchronized expiration time for highly accessed cache keys, allowing thousands of application servers to query the backend database at the exact same millisecond.

### Event Consumers
- **[DO]** Design message consumers to check a local datastore for a `message_id` before processing, ensuring that at-least-once delivery does not result in duplicate state changes.
- **[DON'T]** Assume message buses provide strictly exactly-once delivery without building idempotent application-level consumer logic.

### CQRS (Command-Query-Responsibility Segregation)
- **[DO]** Use CQRS to push user profile updates to an append-only log, while asynchronously generating an ElasticSearch read-model specifically optimized for complex text searching.
- **[DON'T]** Implement CQRS and Event Sourcing for a simple settings-toggle table, introducing massive distributed system complexity where a standard relational table would suffice.