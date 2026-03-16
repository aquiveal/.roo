**@Domain**
These rules activate when the AI is tasked with designing, architecting, optimizing, or refactoring distributed database systems, data storage layers, horizontally scalable systems, multi-tenant SaaS data stores, or when resolving database scalability, query routing, or partitioning challenges.

**@Vocabulary**
- **Sharding / Partitioning**: The process of splitting a large dataset into smaller, independent subsets where each piece of data belongs to exactly one subset.
- **Shard / Partition / Range / Region / Tablet / vnode / vBucket**: System-specific terms for a data subset.
- **Horizontal Scaling (Scale-out)**: Growing system capacity by adding more machines rather than upgrading a single machine.
- **Partition Key**: The specific attribute, field, or column used by the routing algorithm to determine which shard a record belongs to.
- **Skew**: An unfair or uneven distribution of data or query load across shards.
- **Hot Shard / Hot Spot**: A shard experiencing a disproportionately high load compared to others.
- **Hot Key**: A single partition key that receives an overwhelming amount of traffic (e.g., a celebrity user on a social network).
- **Key-Range Sharding**: Assigning a contiguous range of partition keys (from a minimum to a maximum) to a specific shard.
- **Hash-Range Sharding**: Applying a hash function to the partition key and assigning a contiguous range of the resulting hash values to a shard.
- **Consistent Hashing**: A hashing algorithm designed to minimize data movement when the number of shards or nodes changes.
- **Pre-splitting**: Configuring an initial set of shard boundaries on an empty database based on an anticipated key distribution.
- **Resharding / Rebalancing**: The process of moving data or entire shards between nodes to evenly distribute load when nodes are added or removed.
- **Local Secondary Index (Document-Partitioned)**: A secondary index maintained independently by each shard, indexing only the data present within that specific shard.
- **Global Secondary Index (Term-Partitioned)**: A secondary index that covers data across all shards but is itself sharded based on the indexed value (the term).
- **Scatter/Gather**: The process of querying all shards in parallel and combining the results, typically required when reading from a local secondary index without knowing the partition key.
- **Cell-Based Architecture**: Grouping services and storage for a specific set of tenants into a self-contained, isolated unit to limit fault blast radius.

**@Objectives**
- The AI MUST optimize for uniform distribution of data and query load across all available nodes.
- The AI MUST avoid architectural designs that result in data skew or hot spots.
- The AI MUST balance the trade-offs between write efficiency and read efficiency when designing secondary indexes.
- The AI MUST design rebalancing and routing mechanisms that minimize data movement and operational risk.
- The AI MUST only recommend sharding when single-node scaling is no longer feasible, acknowledging the inherent complexities of distributed transactions and joins.

**@Guidelines**

**1. Evaluation and Justification**
- The AI MUST NOT prematurely recommend sharding. If data volume and write throughput can be handled by a single machine, recommend single-node databases or read-scaling (replication) first.
- The AI MUST highlight that cross-shard operations require distributed transactions, which bottleneck performance or may be unsupported by the chosen database.

**2. Partition Key Selection & Hashing**
- When designing Key-Range Sharding, the AI MUST NOT use monotonically increasing values (like timestamps) as the primary partition key, as this directs all writes to a single hot shard.
- When prefixing a timestamp with another ID (e.g., `sensor_id + timestamp`), the AI MUST document that range queries across multiple IDs will require separate queries for each ID.
- When designing Hash Sharding, the AI MUST strictly enforce the use of stable, cross-process hash functions (e.g., MD5, Murmur3). The AI MUST explicitly forbid the use of in-memory or process-specific hash functions (like Java's `Object.hashCode()` or Ruby's `Object#hash`).
- The AI MUST strictly forbid the `hash(key) % N` (modulo number of nodes) routing approach, as changing `N` forces a massive, inefficient redistribution of data.

**3. Hot Spot Mitigation**
- If an application suffers from an extreme "Hot Key" (e.g., a viral social media post), the AI MUST implement "salting": appending a random number (e.g., a 2-digit decimal) to the hot key to distribute its writes across multiple shards.
- When implementing salting, the AI MUST include the corresponding read-side logic: the application must read all salted variations (e.g., 100 keys) and aggregate the results. Salting MUST ONLY be applied to known hot keys to avoid global overhead.

**4. Rebalancing & Shard Sizing**
- For hash sharding, the AI MUST recommend creating a fixed number of shards that is significantly higher than the number of nodes (e.g., 1,000 shards for 10 nodes) to allow whole shards to move without splitting data when nodes are added.
- The AI MUST advise against fully automated rebalancing without human oversight. The AI MUST warn that automated rebalancing during temporary node slowdowns can cause cascading cluster failures.

**5. Secondary Indexes**
- If the workload is write-heavy, the AI MUST recommend Local Secondary Indexes to keep writes within a single shard, warning the user about the scatter/gather penalty for reads.
- If the workload is read-heavy, the AI MUST recommend Global Secondary Indexes to allow efficient, single-shard reads, warning the user about the complexity of distributed transactions during writes.

**6. Request Routing**
- The AI MUST design a routing tier using a consensus-based coordination service (e.g., ZooKeeper, etcd) or a built-in gossip protocol to maintain authoritative shard-to-node mappings.
- Clients or routing tiers MUST subscribe to the coordination service to detect when shards change ownership.

**7. Multi-Tenancy**
- When sharding by tenant, the AI MUST ensure that resource isolation, fault isolation (cell-based architecture), and GDPR-compliant data deletion are factored into the design.
- The AI MUST account for tenant size variance, acknowledging that massive tenants may require further internal sharding.

**@Workflow**
When tasked with designing or auditing a sharded data architecture, the AI MUST follow this algorithmic process:
1. **Analyze the Workload**: Determine if the bottleneck is write throughput, data volume, or read throughput. (If only read throughput, suggest replication instead).
2. **Select Sharding Strategy**: 
   - Choose *Key-Range Sharding* if the application heavily relies on scanning contiguous records (e.g., time-series bounded by an entity ID).
   - Choose *Hash Sharding* if uniform distribution is critical and range scans are rare.
3. **Define Partition Key**: Select a key that guarantees even distribution. If using a hash, specify the cryptographic/stable hash function.
4. **Identify Hot Spots**: Ask the user if extreme outliers exist in the dataset. If yes, implement a salting/random-prefixing strategy exclusively for those keys.
5. **Design Secondary Indexes**: Map out all required queries. If queries rarely include the partition key, define a Global Secondary Index. If queries usually include the partition key or writes are the primary bottleneck, define a Local Secondary Index.
6. **Define Routing and Rebalancing**: Specify whether a routing tier, a coordination service (ZooKeeper/etcd), or smart clients will handle request routing. Specify a fixed-shard strategy or dynamic splitting strategy for rebalancing.

**@Examples (Do's and Don'ts)**

**Partition Key Selection**
- **[DO]** Prefix monotonically increasing keys with an entity ID: `partition_key = concat(sensor_id, "-", timestamp)`. This distributes write load across multiple sensor shards while preserving local time-range scans.
- **[DON'T]** Use raw timestamps for key-range sharding: `partition_key = timestamp`. This creates a single hot shard that receives 100% of current write traffic while all older shards sit idle.

**Hash Routing**
- **[DO]** Use a fixed number of logical shards assigned to physical nodes: `shard_id = hash(key) % 1000`; look up `shard_id` in a ZooKeeper routing table to find the physical node IP.
- **[DON'T]** Modulo the physical nodes directly: `node_ip = nodes[hash(key) % nodes.length]`. This will cause massive data invalidation and movement if `nodes.length` changes.

**Hash Functions**
- **[DO]** Use a stable hash function: `hashed_key = murmur3_32(user_id)`.
- **[DON'T]** Use language-specific memory-address hashes: `hashed_key = user_id.hashCode()`.

**Hot Key Mitigation (Salting)**
- **[DO]** Distribute a viral key's writes and aggregate on read:
  ```python
  # Write
  random_salt = random.randint(0, 99)
  db.write(f"post_12345_likes_{random_salt}", "+1")
  
  # Read
  total_likes = sum([db.read(f"post_12345_likes_{i}") for i in range(100)])
  ```
- **[DON'T]** Route all updates for a viral object to a single key, which will overwhelm the single CPU/node responsible for that shard.

**Secondary Indexing**
- **[DO]** Use a Global Secondary Index when you frequently search by a term (e.g., `color="red"`) but do not know the primary partition keys (e.g., `user_id`). Route the query to the single shard responsible for the term `red`.
- **[DON'T]** Use a Local Secondary Index for a highly specific query lacking the partition key, which forces a scatter/gather query to ping hundreds of shards just to find a single matching record.