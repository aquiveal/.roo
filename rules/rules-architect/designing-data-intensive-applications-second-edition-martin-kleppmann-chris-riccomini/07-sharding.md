@Domain
Database architecture design, distributed data systems engineering, scalability and horizontal scaling planning, Software-as-a-Service (SaaS) multitenancy implementation, secondary index design, and request routing configurations.

@Vocabulary
- **Sharding / Partitioning**: The process of breaking a large dataset into smaller, independent subsets distributed across multiple nodes.
- **Shard / Partition / Range / Region / Tablet / vnode / vBucket**: System-specific terms representing a single subset of sharded data (e.g., Kafka uses Partition, Cassandra uses vnode, Bigtable uses Tablet).
- **Horizontal Scaling (Scale-out)**: Increasing capacity by adding more machines rather than upgrading existing machine hardware.
- **Partition Key**: The attribute (or subset of attributes) of a record used to determine its assigned shard.
- **Skew**: An unfair or unbalanced distribution of data or query load across shards.
- **Hot Spot / Hot Shard**: A specific shard experiencing a disproportionately high load due to skew.
- **Hot Key**: A single partition key that receives an overwhelming volume of traffic (e.g., a celebrity user on a social network).
- **Key-Range Sharding**: Assigning a contiguous range of partition keys to each shard.
- **Hash-Range Sharding**: Applying a hash function to the partition key and assigning a contiguous range of the resulting hash values to each shard.
- **Consistent Hashing**: A hashing algorithm (e.g., Rendezvous hashing, Jump consistent hash) that maps keys to shards in a way that minimizes data movement when the number of shards changes.
- **Pre-splitting**: Configuring an initial set of shards on an empty database based on anticipated key distribution.
- **Resharding / Rebalancing**: The process of moving data or shards between nodes to adapt to changes in cluster size or workload.
- **Cell-Based Architecture**: Grouping services and storage for a specific set of multitenant users into a self-contained, isolated unit (cell) for fault isolation.
- **Request Routing / Routing Tier**: The system or component responsible for directing a client's read/write request to the specific node holding the required shard.
- **Local Secondary Index (Document-Partitioned)**: A secondary index where each shard maintains an index solely for the records stored within that specific shard.
- **Global Secondary Index (Term-Partitioned)**: A secondary index that covers data across all shards but is itself sharded based on the indexed term.
- **Scatter/Gather**: The process of querying all shards in parallel and combining the results, typically required when reading from a Local Secondary Index.
- **Tail Latency Amplification**: The degradation of overall response time caused by waiting for the slowest shard to respond in a Scatter/Gather query.

@Objectives
- Evaluate whether the data volume and write throughput genuinely require the complexity of sharding, defaulting to single-node scaling if sufficient.
- Select partition keys that ensure uniform distribution of data and query load across all available nodes.
- Prevent hot spots and hot keys through proactive architectural patterns (e.g., hashing, salting).
- Implement safe, predictable rebalancing operations that do not cause cascading failures.
- Architect multitenant systems that provide resource isolation, fault isolation, and regulatory compliance.
- Select the correct secondary index architecture (Local vs. Global) based on the strict ratio of read-to-write operations and tolerance for network overhead.

@Guidelines

**1. Database Sharding vs. Local Partitioning**
- The AI MUST distinguish between local partitioning (e.g., PostgreSQL table partitioning into multiple local files for fast deletion) and distributed sharding (splitting data across multiple physical machines).

**2. Sharding for Multitenancy**
- When designing multitenant SaaS architectures, the AI MUST evaluate sharding per tenant.
- The AI MUST list the exact benefits of this approach: Resource isolation, permission isolation, cell-based architecture (fault isolation), per-tenant backup/restore, data residency compliance (GDPR), and gradual schema rollout.
- The AI MUST warn against per-tenant sharding if there are millions of micro-tenants (requires grouping) or if cross-tenant joins are required.

**3. Key-Range Sharding Constraints**
- When utilizing Key-Range Sharding, the AI MUST NOT use monotonically increasing values (e.g., raw timestamps) as the primary partition key, as this guarantees a hot spot on the shard accepting current writes.
- The AI MUST enforce compound keys for time-series data (e.g., `[SensorID, Timestamp]`) to spread writes across multiple shards.

**4. Hash Sharding Constraints**
- The AI MUST NOT use the `hash(key) % N` (modulo number of nodes) algorithm for shard assignment. This causes catastrophic data movement when `N` changes.
- The AI MUST implement either a **Fixed Number of Shards** (creating many more shards than nodes, e.g., 1,000 shards for 10 nodes, moving entire shards when nodes are added) OR **Hash-Range Sharding** (using consistent hashing algorithms like Rendezvous or Jump consistent hash).
- The AI MUST NOT rely on language-built-in in-memory hash functions (e.g., Java `Object.hashCode()` or Ruby `Object#hash`) as they yield different values in different processes. Cryptographically weak but uniformly distributed hashes (e.g., Murmur3, MD5) MUST be explicitly defined.

**5. Hot Key Mitigation (Skew Handling)**
- For highly skewed workloads where a single key receives massive write traffic (the "celebrity problem"), the AI MUST implement key salting: append a random integer (e.g., 0-99) to the hot key.
- The AI MUST implement the corresponding read logic: queries for the hot key must perform a read across all 100 split keys and combine the results.
- The AI MUST restrict this salting ONLY to known hot keys to avoid unnecessary read amplification for standard keys.

**6. Rebalancing Operations**
- The AI MUST advocate for "Human-in-the-loop" (manual or administrator-approved) rebalancing over fully automatic rebalancing.
- The AI MUST warn that automatic rebalancing coupled with automatic failure detection can trigger cascading failures (e.g., moving load away from a temporarily slow node, thereby crushing the remaining healthy nodes).

**7. Request Routing Architecture**
- The AI MUST explicitly define the routing tier architecture using one of three models:
  1. Any-node routing (nodes use a Gossip protocol to forward requests, e.g., Cassandra/Riak).
  2. Routing Tier / Load Balancer (relies on a consensus coordinator like ZooKeeper/etcd to track shard-to-node mapping, e.g., HBase, SolrCloud, MongoDB).
  3. Shard-aware clients (clients subscribe to ZooKeeper/etcd and connect directly).

**8. Secondary Index Selection**
- The AI MUST mandate **Local Secondary Indexes (Document-Partitioned)** for write-heavy workloads. The AI MUST design the read path to utilize a Scatter/Gather query pattern and account for Tail Latency Amplification.
- The AI MUST mandate **Global Secondary Indexes (Term-Partitioned)** for read-heavy workloads. The AI MUST design the write path to handle multi-shard updates, utilizing distributed transactions or asynchronous updates (e.g., DynamoDB global indexes).

@Workflow

1. **Assess Scale and Necessity**: Determine if write throughput and data volume exceed single-node capabilities. If not, explicitly advise against sharding to avoid distributed transaction overhead.
2. **Evaluate Multitenancy**: If the application is SaaS, define tenant boundaries. Decide between one-shard-per-tenant, grouped-tenant shards, or cell-based architecture based on tenant size and data residency requirements.
3. **Select Partition Key**:
   - For range queries: Choose Key-Range Sharding. Define a compound key (e.g., `EntityID + Timestamp`) to prevent hot spots.
   - For uniform distribution without range queries: Choose Hash Sharding.
4. **Define Hashing and Assignment Strategy**: Implement a fixed number of shards (larger than the node count) or hash-range boundaries. Select a stable hash function (e.g., Murmur3).
5. **Design Hot-Key Mitigation**: Identify potential celebrity/viral keys. Implement a random prefix/suffix salting mechanism for writes and a scatter/gather aggregation mechanism for reads of those specific keys.
6. **Architect Secondary Indexes**:
   - Analyze Read/Write ratio.
   - Write-Heavy -> Design Local Indexes + Scatter/Gather read layer.
   - Read-Heavy -> Design Global Indexes + Distributed transaction/async write layer.
7. **Design Request Routing**: Introduce a routing tier using a coordinator (ZooKeeper/etcd/Raft) or a gossip protocol to manage the state of the cluster and direct client requests.
8. **Define Rebalancing Protocol**: Document the operational procedure for adding/removing nodes, explicitly requiring manual triggers or strict threshold limits to prevent automated cascading failures.

@Examples (Do's and Don'ts)

**Principle: Hash Sharding Assignment**
- [DO]: Pre-allocate 1,024 logical shards for a 10-node cluster. Hash the partition key, assign it to one of the 1,024 shards, and maintain a mapping table of logical shards to physical nodes.
- [DON'T]: Route requests using `Murmur3(key) % ActiveNodeCount`.

**Principle: Key-Range Sharding for Time-Series**
- [DO]: Define the partition key as `Concat(Hash(DeviceID), Timestamp)`. This groups data for a specific device close together in time, while spreading concurrent writes across multiple devices to different shards.
- [DON'T]: Define the partition key as `Timestamp`. All current inserts will hit the exact same node, melting the hardware while other nodes sit idle.

**Principle: Hot Key Mitigation**
- [DO]: Detect that `User_Celebrity_123` is experiencing viral write load. Change the write logic to insert into `User_Celebrity_123_00` through `User_Celebrity_123_99` by appending a random number. Update the read logic for this user to query all 100 keys and aggregate.
- [DON'T]: Allow all traffic for a viral entity to hit a single partition, accepting timeouts and node failure.

**Principle: Secondary Indexes**
- [DO]: Use a Global Secondary Index for a "User Email" lookup in an e-commerce database, because reads are frequent (login) and writes are rare (email change). The query hits exactly one shard.
- [DON'T]: Use a Local Secondary Index for "User Email" lookups, forcing the login service to perform a scatter/gather query across 50 shards every time a user logs in, amplifying tail latency.

**Principle: Rebalancing**
- [DO]: Configure alerts for when a shard exceeds 10GB or 10,000 IOPS. Require a DevOps engineer to click "Approve" to split the shard and migrate it to a newly provisioned node.
- [DON'T]: Configure the system to automatically detach and migrate a shard the moment node CPU spikes to 90%, which immediately overwhelms the network and crashes the receiving node.