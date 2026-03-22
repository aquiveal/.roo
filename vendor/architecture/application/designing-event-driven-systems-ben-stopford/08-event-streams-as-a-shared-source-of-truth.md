# @Domain
Trigger these rules when the user requests architectural design, system architecture planning, stream processing implementation, data integration strategies across distributed teams or services, designing Kafka-based multiteam systems, building materialized views, or implementing stateful stream processing. 

# @Vocabulary
- **Event Streaming as the Source of Truth**: The architectural pattern where a central, replayable messaging log retains historic datasets and serves as the single, immutable reference point for all organizational data.
- **Turning the Database Inside Out**: An analogy and architectural model where the traditional conflated components of a database (commit log, query engine, indexes, caching) are deconstructed and separated across a distributed system linked by an event log.
- **Unbundling**: The act of segregating the responsibility for data storage (the log) from the mechanism used to query it (the stream processing API or local database).
- **Pushing Data to Code**: The practice of streaming data directly into the application layer to create local tables, views, and indexes exactly where they are needed, rather than executing queries against a remote database.
- **Commit Log**: The central, immutable storage layer (e.g., Apache Kafka) acting as the definitive record of all business facts.
- **Views / Indexes**: Read-optimized, use-case-focused datasets (e.g., Redis, Solr, Kafka Streams state stores) derived from the central commit log and materialized privately within an application.

# @Objectives
- Establish the replayable event log as the definitive, shared source of truth for the entire organization's data.
- Decouple the responsibility of data storage from the mechanisms used for data querying.
- Treat the entire organization's systems and data flows as a single, distributed database.
- Maximize performance by making data local to the application ("Pushing Data to Code") rather than making remote database calls.
- Empower individual teams and services to move quickly by ensuring they maintain total, private control over their query functionality and local datasets.
- Decouple organizational data while keeping it strongly tied to a single shared source of truth.

# @Guidelines
- The AI MUST treat the central event log (Kafka) as the definitive source of truth; no single monolithic database may serve this role for inter-service communication.
- The AI MUST separate the system's commit log (storage) from its indexes and caches (query execution).
- The AI MUST implement queries by creating continuous stream processing jobs that materialize data locally, rather than issuing remote queries to a shared database.
- The AI MUST ensure that every consuming application or service derives its own specialized, private view from the central event stream.
- The AI MUST NOT design systems where multiple independent services share the same query functionality or share the same database instance.
- The AI MUST treat all downstream query-oriented systems (e.g., Redis, Solr, Hive) strictly as specialized index types derived from the central log, never as the source of truth.
- The AI MUST use stream processing systems (e.g., Kafka Streams, KSQL) as the trigger and view materialization mechanism for these indexes.
- The AI MUST maintain the simplest possible contract between services by limiting their integration exclusively to the sharing of central event streams.

# @Workflow
1. **Identify Central Facts**: Identify the core datasets and business facts required by multiple applications or departments across the organization.
2. **Establish the Log**: Define the central event streams (Kafka topics) that will store these datasets immutably and act as the organization's commit log.
3. **Analyze Consumer Needs**: For each consuming application, analyze the specific UI, geographic, or performance requirements (e.g., a fast, scrollable GUI grid requiring local caching).
4. **Design the Materialization Mechanism**: Design a stream processing job (using Kafka Streams or KSQL) that subscribes to the central log.
5. **Push Data to Code**: Configure the stream processor to push the exact required data into the application's local environment, materializing it into a highly optimized, private view (e.g., a local state store, an in-memory cache, or a specialized search index).
6. **Encapsulate the Query**: Implement the application to execute all reads and queries exclusively against this local, private view, completely isolated from other services.

# @Examples (Do's and Don'ts)

**Principle: Turning the Database Inside Out (Pushing Data to Code)**
- **[DO]**: Use a stream processor (Kafka Streams) to continuously read an `orders` topic and materialize a local, read-optimized state store directly inside a GUI application's backend so the frontend can query a scrollable grid with zero network latency.
- **[DON'T]**: Program the GUI application to periodically poll a remote, centralized Oracle database every time the user scrolls the grid, relying on a bolt-on caching layer to manage latency.

**Principle: Unbundling Storage and Querying**
- **[DO]**: Store the single source of truth for `payments` in a Kafka topic, and allow Team A to pipe it into Redis for fast key/value lookups while Team B pipes the exact same topic into Solr for free-text search.
- **[DON'T]**: Force Team A and Team B to share a single massive Elasticsearch cluster acting as both the system of record and the query engine for `payments`, coupling both teams to the same operational uptime and query schemas.

**Principle: Private Query Functionality**
- **[DO]**: Ensure that a service's local materialized view is completely private; if another service needs similar data, it must derive its own view from the central Kafka log.
- **[DON'T]**: Expose the underlying materialized view of Service A via an API just so Service B can skip building its own view from the central log.