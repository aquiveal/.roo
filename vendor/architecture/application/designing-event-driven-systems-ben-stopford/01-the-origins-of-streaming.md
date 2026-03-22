@Domain
This rule file is activated whenever the AI is tasked with designing, implementing, or reviewing real-time data ingestion pipelines, stream processing architectures, Kafka Streams applications, KSQL scripts, or transitioning traditional batch/RPC-based analytics into continuous, event-driven streaming systems.

@Vocabulary
- **Stream Processing Layer:** A clustered application layer (using Kafka Streams Java DSL or KSQL) that computes continuous queries over incoming data streams.
- **Serving Layer:** The destination for processed streams, allowing end-users or systems to query the results (e.g., Cassandra, HDFS, or Kafka Streams Interactive Queries).
- **Continuous Computation:** The execution model where a query is recomputed instantaneously every time a new input arrives, emitting a result if the value has changed.
- **State:** Data required by a stream processor (such as running counts within a window) to compute aggregations, joins, or recover from crashes/restarts.
- **Changelog Topic:** A Kafka topic used to back up the internal state of a stream processor, ensuring durability and recovery.
- **Pipeline:** A sequence of stream processing queries chained together over multiple stages (e.g., combining two independent aggregation streams into a final ratio stream).
- **Local State Store:** An embedded storage mechanism within the stream processor node that holds state or tables locally, enabling fast, message-at-a-time queries without crossing the network.
- **Interactive Queries:** A feature of Kafka Streams allowing external applications to query the local state stores directly without pushing data to an external serving layer.

@Objectives
- Architect systems based on continuous, real-time computation rather than scheduled batch processing.
- Eliminate per-message network latency by internalizing reference data and running computations against local state stores.
- Guarantee fault-tolerance and infinite horizontal scalability by designing processors as clustered, stateless-acting nodes backed by Kafka changelogs.
- Construct modular, chained processing pipelines instead of monolithic, overly complex stream queries.

@Guidelines
- **Network and Ingestion Sizing:** The AI MUST calculate Kafka ingestion capabilities by factoring in replication overhead. The AI MUST divide raw network speed by three (e.g., a 10 GbE cluster yields ~1 GB/s actual ingestion) when evaluating throughput limits.
- **Continuous Query Execution:** The AI MUST NOT design scheduled polling mechanisms for data processing. All queries MUST be implemented as continuous computations (using Kafka Streams Java DSL or KSQL) that react to every arriving message.
- **State Management:** When an operation requires historical context (e.g., counts, aggregations, windows), the AI MUST explicitly define local state storage.
- **State Durability:** The AI MUST ensure that every local state store is backed by a Kafka changelog topic to permit seamless recovery and continuation upon node crash or restart.
- **Zero-Network Processing:** The AI MUST strongly prohibit message-at-a-time network calls to external databases for enrichments or lookups. Instead, the AI MUST route reference data into Kafka and materialize it into local state stores for in-memory or local-disk querying.
- **Pipeline Modularity:** The AI MUST break complex stream computations into multiple chained stages. If calculating a derived metric (e.g., stability ratio from crashes and usage), the AI MUST compute the base metrics in independent early stages and join them in a subsequent stage.
- **Fault-Tolerant Clustering:** The AI MUST NOT design stream processors that rely on a single-node execution environment or local, non-replicated disk states. The architecture MUST support dynamic scaling where work and state automatically reroute to new or surviving nodes.
- **Serving Layer Abstraction:** The AI MUST explicitly define how computed results are queried by specifying a serving layer, choosing between pushing results to external datastores (Cassandra, HDFS) or exposing them via Interactive Queries.

@Workflow
1. **Ingestion Modeling:** Define the source data streams (e.g., JSON payloads from mobile devices). Calculate required bandwidth, strictly applying the 1/3 replication overhead rule to ensure the Kafka ingestion cluster is correctly sized.
2. **Compute Paradigm Selection:** Choose the appropriate stream processing engine (Kafka Streams Java DSL for programmatic logic, KSQL for SQL-like analytical queries) based on the application's ecosystem.
3. **Pipeline Staging:** Deconstruct the required business logic into atomic queries. Chain these queries by directing the output of Stage 1 streams into the input of Stage 2 streams.
4. **State and Storage Definition:** Identify all operations requiring state (windowed aggregations, joins, historical counts). Configure local state stores for these operations and explicitly declare their associated changelog topics for durability.
5. **Enrichment Localization:** If the stream requires external reference data, design a pipeline to ingest that database into Kafka and load it into the stream processor's local state, completely eliminating remote network calls during processing.
6. **Serving Layer Integration:** Define the output destination for the final processed stream, configuring either a connector to an external database (Cassandra/HDFS) or configuring Kafka Streams Interactive Queries for direct access.

@Examples (Do's and Don'ts)

**Pipeline Chaining and Continuous Computation**
- [DO] Create modular KSQL pipelines that react continuously:
  ```sql
  CREATE STREAM apps_opened AS SELECT app_id, count(*) FROM raw_events WHERE type='OPEN' WINDOW TUMBLING (SIZE 1 DAY) GROUP BY app_id;
  CREATE STREAM apps_crashed AS SELECT app_id, count(*) FROM raw_events WHERE type='CRASH' WINDOW TUMBLING (SIZE 1 DAY) GROUP BY app_id;
  CREATE STREAM app_stability AS SELECT o.app_id, (c.count / o.count) AS crash_ratio FROM apps_opened o JOIN apps_crashed c ON o.app_id = c.app_id;
  ```
- [DON'T] Write a cron job that runs once a day to query an event database and calculate crash ratios in batch.

**State Management and Enrichments**
- [DO] Internalize reference data to enrich streams using local state stores:
  ```java
  KTable<String, User> usersTable = builder.table("users-topic");
  KStream<String, Event> events = builder.stream("events-topic");
  events.join(usersTable, (event, user) -> new EnrichedEvent(event, user));
  ```
- [DON'T] Perform an HTTP REST call or JDBC SQL query inside the stream processing `map` or `foreach` function for every arriving event.

**Throughput Calculation**
- [DO] State: "Given a 30 GbE network environment, the maximum safe Kafka ingestion rate is calculated at 10 GbE (approx 1 GB/s) due to the mandatory 3x replication factor overhead."
- [DON'T] Assume a 10 GbE network card equates to 10 GbE of application-level Kafka ingestion throughput.