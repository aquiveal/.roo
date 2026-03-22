# @Domain

These rules MUST be activated when the AI is tasked with evaluating, selecting, designing, configuring, or interacting with databases, datastores, persistence tiers, Object-Relational Mappers (ORMs), or distributed data architectures. This includes architectural reviews, schema design, database migrations, connection layer configurations, and debugging data consistency or latency issues.

# @Vocabulary

- **Relational Model**: A data model representing data as relationships based on unique keys, utilizing strict normalization, schemas, and joins. Examples: Oracle, MySQL, PostgreSQL, DB2, SQL Server, Google Spanner, Amazon RedShift, NuoDB.
- **Key-Value Model**: A data model storing objects as opaque blobs inside dictionaries/hashes, without relationship mappings. Examples: Dynamo, Aerospike, Cassandra, Riak, Voldemort, Redis.
- **Document Model**: A subset of Key-Value where the database maintains metadata about the document structure (e.g., JSON), allowing secondary indexing without joins, but requiring denormalization and external data governance. Example: MongoDB.
- **Navigational/Graph Model**: A data model using nodes (data), edges (relationships), and properties to represent connected data, optimized for following links rather than traditional queries. Example: Neo4J.
- **ORM (Object-Relational Mapper)**: A data access layer abstracting the database. Often causes impedance mismatches, unnecessary queries, and obfuscated logic.
- **ACID**: Atomicity, Consistency, Isolation, Durability.
- **Atomicity**: The guarantee that an entire transaction is committed to the datastore, or completely rolled back (no partial writes).
- **Consistency (ACID)**: The guarantee that a transaction brings the database from one valid state to another, enforcing defined rules, constraints, and triggers.
- **Isolation**: The guarantee that concurrent execution of transactions results in a state identical to serial, sequential execution.
- **Dirty Read**: Reading uncommitted data that is being written by another concurrent transaction.
- **Nonrepeatable Read**: Reading the same data twice within a single transaction and getting different results due to another transaction committing updates.
- **Phantom Read**: Executing the same range query twice within a transaction and receiving a different set of rows (more or fewer) because another transaction inserted or deleted rows.
- **MVCC (Multiversion Concurrency Control)**: Snapshot isolation maintaining multiple versions of data to prevent read locks from blocking writes, and vice versa.
- **Write Skew**: An isolation anomaly in MVCC where two concurrent transactions read the same data and make disjoint updates, resulting in an inconsistent combination of both.
- **2PL (2-Phase Locking)**: A strict serialization mechanism using shared (read) and exclusive (write) locks.
- **SSI (Serial Snapshot Isolation)**: An optimistic serialization approach that waits until commit to check for write collisions, rolling back if serializability is violated.
- **Durability**: The guarantee that committed transactions survive power loss or crashes, typically utilizing a Write-Ahead Log (WAL).
- **BASE**: Basically Available, Soft state, Eventual consistency. A non-transactional distributed model favoring write throughput and availability over strict consistency.
- **CAP Theorem**: The principle that a distributed datastore can provide at most two of three guarantees: Consistency, Availability, and Partition Tolerance. Since Partitions are inevitable, systems must trade off C vs. A.
- **Consistency (CAP) / Linearizability**: The guarantee that a set of operations on an object occurs in real-time order and appears instantaneous to all users.
- **Yield**: The ability of a distributed system to successfully return an answer to a query.
- **Harvest**: The completeness of the dataset returned by a distributed system query.

# @Objectives

- The AI MUST perfectly align datastore architectural choices with the application's specific requirements for data models, transactional guarantees (ACID vs. BASE), and distributed system trade-offs (CAP).
- The AI MUST rigorously evaluate and mitigate the performance and abstraction penalties introduced by ORMs.
- The AI MUST enforce explicit decisions regarding database isolation levels based on the application's tolerance for read anomalies (dirty, nonrepeatable, phantom, write skew).
- The AI MUST consciously navigate the CAP theorem, explicitly defining whether a system favors Consistency or Availability during a network partition, while exposing all hidden latency trade-offs.
- The AI MUST evaluate degraded state behavior by explicitly balancing Yield (uptime/response) against Harvest (data completeness).

# @Guidelines

## Data Model Selection
- When asked to select or design a datastore, the AI MUST explicitly match the data model to the application's read/write patterns:
  - Select **Relational** for strict schema governance, complex relationships, and ACID compliance.
  - Select **Key-Value** for high-throughput, low-latency, schema-less blob storage where relationships are unnecessary.
  - Select **Document** when the object structure is hierarchical, joins are expensive, and denormalization is acceptable, BUT explicitly warn the user about data bloat and the need for application-layer data governance.
  - Select **Graph** when the primary query pattern involves deep relationship traversal (edges) rather than set-based aggregations.

## ORM Mitigation
- When evaluating or generating Data Access Layer (DAL) code utilizing an ORM, the AI MUST proactively inspect and mitigate the four critical ORM anti-patterns:
  1. Tying reads and writes strictly to tables (preventing independent scaling).
  2. Holding transactions open longer than necessary (wasting finite connection/snapshot resources).
  3. Generating a huge number of unnecessary queries (N+1 query problem).
  4. Generating convoluted, poorly performing SQL.
- The AI MUST default to requesting or generating raw SQL logs from the ORM to validate query efficiency.

## ACID and Isolation Configuration
- When defining transactional logic, the AI MUST declare the intended isolation level and map it to the prevented anomalies:
  - **Read Uncommitted**: ALLOWS dirty reads, nonrepeatable reads, phantom reads. Use only when exact precision is entirely irrelevant.
  - **Read Committed**: PREVENTS dirty reads. ALLOWS nonrepeatable reads and phantom reads.
  - **Repeatable Read**: PREVENTS dirty and nonrepeatable reads. ALLOWS phantom reads and Write Skew (in MVCC).
  - **Serializable**: PREVENTS all read anomalies via 2PL or SSI. The AI MUST warn the user about severe latency impacts and deadlocks (2PL) or frequent rollback retries (SSI) when using this level.

## Durability Tuning
- The AI MUST evaluate if 100% Durability (fsync on every commit) is necessary. If performance is critical and slight data loss upon OS crash is acceptable, the AI MUST suggest relaxing the Write-Ahead Log (WAL) flush interval.

## CAP Theorem and Latency Trade-offs
- The AI MUST explicitly reject the notion that CAP is strictly binary. It MUST evaluate the hidden variable: **Latency**.
- When designing for **Consistency (Linearizability)**, the AI MUST warn about and configure for:
  - *Ordering-latency trade-off*: Slower writes due to coordinator processes (e.g., Paxos).
  - *Primary timeout retry trade-off*: Increased latency when a primary node times out and proxies retry against alternative nodes.
  - *Reader time-out retry trade-off*: Latency spikes when readers retry to avoid stale data.
  - *Synchronous replication-latency trade-off*: Network hops required for all nodes to acknowledge a write before committing.

## Yield vs. Harvest Strategy
- When designing failover or degraded states for distributed datastores, the AI MUST prompt the user to define the Yield vs. Harvest tolerance.
- If high availability is paramount, the AI MUST configure the system to prioritize Yield (returning a response) even if Harvest is degraded (returning 75% of search results because 25% of nodes are down).

# @Workflow

1. **Requirement Parsing**: Analyze the user's data storage request and immediately classify the primary workload type (OLTP, OLAP, High-throughput blob, deep relation traversal).
2. **Taxonomy Mapping**: Select the appropriate data model (Relational, KV, Document, Graph) and justify the choice based on normalization needs and relationship complexity.
3. **Transaction Profiling**: Determine if the system requires strict ACID compliance or if a BASE (Eventual Consistency) model is acceptable.
4. **Isolation Definition**: If ACID is selected, evaluate the risk of dirty, nonrepeatable, and phantom reads. Explicitly set and document the minimum required ANSI isolation level.
5. **CAP & Latency Declaration**: Identify the system's behavior during a network partition. Explicitly document whether Availability or Consistency is dropped, and list the specific latency trade-offs incurred during normal operations.
6. **Degraded State Rules**: Define the Yield vs. Harvest ruleset. Instruct the application how to handle partial data availability (e.g., return partial results, or throw an error).
7. **ORM / Access Review**: If an ORM is used, output a mandatory review checklist enforcing raw SQL logging, connection duration limits, and avoidance of N+1 query loops.

# @Examples (Do's and Don'ts)

## Datastore Selection
- **[DO]**: "Because your application requires deep traversal of user social connections and recommendations based on friends-of-friends, I recommend a Navigational/Graph datastore like Neo4J, as traditional relational joins will be prohibitively expensive."
- **[DON'T]**: "You should use MongoDB for everything because JSON is easy to work with and schemas are annoying." (Anti-pattern: Failing to warn about denormalization bloat and missing data governance).

## ORM Usage
- **[DO]**: "I have generated the SQLAlchemy ORM queries. However, I have explicitly eager-loaded the `children` relationship to prevent the N+1 query problem, and I have kept the transaction scope limited strictly to the `commit()` block to prevent holding snapshot resources unnecessarily."
- **[DON'T]**: "Just use `user.orders.items` in your loop, the ORM will figure out how to fetch the data." (Anti-pattern: Obfuscating logic and generating unnecessary queries).

## Transaction Isolation
- **[DO]**: "To calculate the final financial ledger, I am setting the transaction isolation level to `SERIALIZABLE` to prevent phantom reads. Note: We must wrap this in a retry block because the SSI (Serial Snapshot Isolation) implementation may throw serialization failures under high concurrency."
- **[DON'T]**: "Let's use `REPEATABLE READ` for the financial ledger." (Anti-pattern: Failing to warn about Write Skew or phantom reads which can corrupt financial data).

## Yield vs. Harvest
- **[DO]**: "In the event of a Cassandra node failure, I have configured the application to reduce Harvest to maintain Yield. The search API will return the available 66% of results instantly rather than timing out and failing the entire request."
- **[DON'T]**: "If a node goes down, the database query will just hang until it comes back." (Anti-pattern: Ignoring the Yield vs. Harvest distributed systems trade-off).