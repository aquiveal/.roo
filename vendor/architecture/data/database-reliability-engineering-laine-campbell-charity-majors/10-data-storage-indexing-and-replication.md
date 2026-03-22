# @Domain
These rules MUST trigger when the user requests assistance with designing, configuring, optimizing, evaluating, or troubleshooting database storage engines, data structures, indexing mechanisms, or distributed data replication topologies.

# @Vocabulary
- **Block/Page**: The finest level of granularity for storing records; a fixed byte size on disk.
- **Extent**: A larger container organizing data blocks, used as the allocation unit within a tablespace.
- **B-tree (Binary Tree)**: A self-balancing data structure keeping data sorted, optimized for block-level reading and writing, utilizing root, internal, and leaf nodes.
- **SSTable (Sorted-String Table)**: A file containing a set of sorted key-value pairs, stored opaquely as arbitrary BLOBs, heavily utilized in LSM tree architectures.
- **LSM Tree (Log-Structured Merge Tree)**: An algorithm combining in-memory tables (Memtables), batch flushing to immutable SSTables, and periodic compaction.
- **Memtable**: An in-memory data structure that absorbs writes before they are sorted and flushed to disk as SSTables.
- **Tombstone**: A logical marker in an LSM tree indicating that a record has been deleted.
- **Bloom Filter**: A probabilistic data structure used to rapidly evaluate whether a record key is present in an SSTable, reducing unnecessary disk reads.
- **Hash Index**: An index mapping hashes to record locations, strictly for single-key lookups.
- **Bitmap Index**: An index storing data as bit arrays, highly optimized for low-cardinality values.
- **Clustered Index**: An index that dictates the physical storage order of table records on disk.
- **WAL (Write-Ahead Log) / Redo Log**: A sequential log recording transactions before they are applied to data files, ensuring atomicity and durability during crashes.
- **Single-Leader Replication**: A topology where one node (leader) accepts writes and propagates them to other nodes (followers/replicas).
- **Multi-Leader Replication**: A topology where multiple nodes accept writes, necessitating conflict resolution mechanisms.
- **Leaderless (Write-Anywhere) Replication**: A Dynamo-based topology where any node accepts writes and reads, typically relying on eventual consistency.
- **CDC (Change Data Capture) / Row-Based Replication**: A replication method that ships actual row modifications rather than raw SQL statements or underlying physical block changes.
- **Statement-Based Replication**: A replication method that ships the actual SQL query executed.
- **Quorum**: The minimum number of nodes required to acknowledge a read (R) or write (W) to guarantee consistency in a distributed system. 
- **Sloppy Quorum**: A configuration allowing writes to succeed even if the target nodes are unreachable, routing the data temporarily to healthy nodes.
- **Hinted Handoff**: The process of delivering temporarily stored writes (from a sloppy quorum) to their rightful node once it returns online.
- **Anti-Entropy**: A background synchronization process (often using Merkle trees) that repairs inconsistencies in eventually consistent datasets.
- **Merkle Tree**: A balanced tree of object hashes used to rapidly identify and repair divergent data across distributed nodes.
- **CRDT (Conflict-Free Replicated Datatype)**: A data structure mathematically guaranteed to merge concurrent modifications without conflicts.

# @Objectives
- The AI MUST optimize local data storage architectures by selecting the appropriate storage engine (B-tree vs. LSM) based on read/write latency requirements and workload patterns.
- The AI MUST define accurate and highly performant indexing strategies tailored to data cardinality and query behavior.
- The AI MUST architect resilient and consistent replication topologies that strictly align with the user's availability, scalability, locality, and disaster recovery requirements.
- The AI MUST enforce safety protocols around replication lag, failovers, and split-brain scenarios by defining appropriate consistency trade-offs.

# @Guidelines

## Data Structure & Storage Engine Selection
- When a workload is read-heavy or requires optimal range-based queries, the AI MUST recommend B-tree-based storage engines.
- When configuring B-trees on Solid-State Drives (SSDs), the AI MUST evaluate and recommend smaller database block sizes to mitigate the 30% to 40% latency penalty associated with large blocks on SSDs.
- When configuring database block sizes, the AI MUST ensure they align perfectly with the underlying filesystem block size to prevent wasted I/O.
- When a workload is write-heavy, the AI MUST recommend LSM Tree/SSTable-based storage engines (e.g., Cassandra, RocksDB).
- When operating LSM storage, the AI MUST account for I/O and disk space spikes during SSTable compaction processes resulting from tombstone consolidation.
- When optimizing read performance in LSM systems, the AI MUST allocate sufficient memory to Bloom Filters to minimize false-positive disk seeks.

## Indexing Architecture
- When single-key lookup speed is paramount and the index fits entirely in memory, the AI MUST implement Hash Indexes. Range scans MUST NOT be attempted on Hash Indexes.
- When indexing low-cardinality fields (e.g., boolean flags, status codes), the AI MUST use Bitmap Indexes.
- When indexing high-cardinality fields, the AI MUST use B-tree indexes and STRICTLY AVOID Bitmap Indexes.
- When physical disk layout optimization is required for primary access patterns, the AI MUST define a Clustered Index.

## Single-Leader Replication Protocols
- The AI MUST choose the appropriate replication synchronicity:
  - **Asynchronous**: When low write latency is prioritized over absolute zero-data-loss durability.
  - **Synchronous**: When zero data loss is strictly required, accepting increased write latency.
  - **Semi-Synchronous**: To balance latency and durability by requiring acknowledgment from at least one replica.
- When configuring replication log formats across bandwidth-constrained networks, the AI MUST consider Statement-Based Logs.
- If Statement-Based Logs are used, the AI MUST audit queries for non-deterministic functions (e.g., `NOW()`, `RAND()`, or specific triggers/stored procedures) which will cause data drift.
- To avoid non-deterministic SQL issues, the AI MUST recommend Row-Based Replication (CDC) or Write-Ahead Log (WAL) shipping.
- When configuring replication, the AI MUST explicitly establish monitoring for replication lag (delay between leader commit and replica apply) and replica availability.

## Multi-Leader Replication Protocols
- When configuring Multi-Leader topologies, the AI MUST implement conflict resolution strategies.
- The AI MUST attempt to avoid conflicts entirely by using affinity routing (tying specific users/regions to specific leaders) or assigning discrete primary key namespaces (e.g., odd/even IDs) to different leaders.
- When conflicts cannot be avoided, the AI MUST define a resolution algorithm.
- The AI MUST explicitly warn against using Last Write Wins (LWW) based on wall-clock timestamps unless system clocks and NTP are strictly synchronized and leap-second behaviors are accounted for.
- For complex merging, the AI MUST recommend Conflict-Free Replicated Datatypes (CRDTs) where supported by the datastore (e.g., Riak).

## Leaderless (Write-Anywhere) Replication Protocols
- When configuring Dynamo-based leaderless systems, the AI MUST calculate and enforce strict Quorums using the formula `R + W > N` (where R = read nodes, W = write nodes, N = total replicas) to guarantee consistency.
- When extreme availability is required during node outages, the AI MUST enable Sloppy Quorums and configure Hinted Handoffs.
- The AI MUST define Anti-Entropy processes (Merkle tree synchronization) to repair cold data inconsistencies that escape read repair or hinted handoffs.

# @Workflow
1. **Analyze Storage Engine Requirements**: Evaluate the workload to determine if it is read-heavy (select B-tree) or write-heavy (select LSM/SSTables). 
2. **Align Hardware and Software Block Sizes**: Validate that database block sizes map cleanly to SSD/HDD filesystem block boundaries.
3. **Design the Indexing Strategy**: Map query patterns to specific index types (Hash for memory key-value, Bitmap for low cardinality, B-tree for ranges/high cardinality).
4. **Determine Replication Topology**: 
   - Use Single-Leader for standard scale-out and strong consistency.
   - Use Multi-Leader for multi-datacenter active/active disaster recovery.
   - Use Leaderless for high-availability eventual consistency.
5. **Configure Replication Internals**: 
   - Single-Leader: Select log format (Row/Statement/WAL) and timing (Sync/Async).
   - Multi-Leader: Define the exact conflict resolution strategy (CRDT, Namespace isolation, LWW).
   - Leaderless: Calculate `R + W > N` values and configure anti-entropy/hinted handoff mechanisms.
6. **Implement Replication Monitoring**: Define health checks for replication lag (using heartbeat rows), quorum availability, and checksum-based data consistency audits.

# @Examples (Do's and Don'ts)

## Storage Engine Alignment
- **[DO]**: Ensure the database block/page size is equal to or a multiple of the OS filesystem block size (e.g., formatting an ext4 filesystem with 4K blocks to match InnoDB's 16K pages) to prevent partial reads/writes.
- **[DON'T]**: Use 64K database block sizes on an SSD without benchmarking, as B-tree traversal with large block sizes incurs severe read latency penalties on solid-state drives.

## Index Selection
- **[DO]**: Use a Bitmap Index on a `user_status` column that only contains 'ACTIVE', 'SUSPENDED', or 'DELETED'.
- **[DON'T]**: Use a Hash Index to optimize a query containing `WHERE timestamp > '2023-01-01'`.

## Replication Log Formatting
- **[DO]**: Utilize Row-Based Replication (CDC) when the application frequently uses `UPDATE users SET last_login = NOW() WHERE id = 123`.
- **[DON'T]**: Rely on Statement-Based Replication when utilizing non-deterministic stored procedures, as replicas will calculate different values than the leader resulting in silent data drift.

## Multi-Leader Conflict Resolution
- **[DO]**: Resolve multi-leader collision risks by configuring Leader A to generate auto-incrementing IDs starting at 1 with a step of 2 (1,3,5), and Leader B to start at 2 with a step of 2 (2,4,6).
- **[DON'T]**: blindly trust Last Write Wins (LWW) conflict resolution across global data centers without implementing strict NTP monitoring, as clock skew will cause legitimate updates to be discarded.

## Leaderless Quorum Configuration
- **[DO]**: In a 5-node cluster (N=5), configure Write Quorum (W) to 3 and Read Quorum (R) to 3, ensuring `3 + 3 > 5`, guaranteeing a read will fetch the latest write.
- **[DON'T]**: Set W=2 and R=2 in a 5-node cluster, as `2 + 2 <= 5`, which violates linearizability and guarantees stale reads.