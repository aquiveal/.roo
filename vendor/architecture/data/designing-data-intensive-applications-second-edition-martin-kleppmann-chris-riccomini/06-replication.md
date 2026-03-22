# @Domain
These rules activate whenever the AI is tasked with designing, analyzing, configuring, or troubleshooting distributed data systems, database architectures, state synchronization, multi-region deployments, offline-first applications, collaborative software, or any system requiring data to be copied and maintained across multiple network-connected nodes.

# @Vocabulary
- **Replication**: Keeping a copy of the same data on multiple machines connected via a network to decrease latency, increase availability, or scale read throughput.
- **Replica**: A node that stores a copy of the database.
- **Single-Leader Replication (Primary-Backup / Active-Passive)**: A topology where one replica is designated as the leader (accepts writes) and others are followers (apply the leader's replication log and serve reads).
- **Synchronous Replication**: The leader waits for a follower to confirm it has received the write before reporting success to the client.
- **Asynchronous Replication**: The leader sends the write to followers but does not wait for a response before reporting success.
- **Semi-Synchronous Replication**: A configuration where one follower is synchronous and the others are asynchronous, ensuring at least two up-to-date nodes.
- **Failover**: The process of promoting a follower to be the new leader when the existing leader fails.
- **Split Brain**: A dangerous fault scenario where two nodes simultaneously believe they are the leader, potentially leading to data corruption.
- **STONITH (Fencing)**: "Shoot The Other Node In The Head", a mechanism to forcibly shut down an old leader to prevent split brain.
- **Logical (Row-Based) Log**: A replication log format decoupled from storage engine internals, recording changes at the row granularity.
- **Eventual Consistency**: A guarantee that if writes stop, all followers will eventually catch up and be consistent with the leader.
- **Replication Lag**: The delay between a write happening on the leader and being reflected on a follower.
- **Read-After-Write (Read-Your-Writes) Consistency**: A guarantee that if a user reloads a page, they will always see any updates they submitted themselves.
- **Monotonic Reads**: A guarantee that a user will not observe time going backward (i.e., reading stale data after previously reading newer data).
- **Consistent Prefix Reads**: A guarantee that anyone reading a sequence of causally related writes will see them appear in the same order.
- **Multi-Leader (Active-Active) Replication**: A topology where more than one node can accept writes, and each leader acts as a follower to other leaders.
- **Sync Engine / Local-First**: Software architectures where local databases act as leaders on user devices, replicating asynchronously with a backend and other devices.
- **Last Write Wins (LWW)**: A conflict resolution strategy that randomly or arbitrarily (usually via timestamp) picks one concurrent write and discards the others.
- **CRDT (Conflict-Free Replicated Datatypes)**: Data structures that automatically resolve concurrent modifications without data loss (e.g., keeping track of character IDs for text insertion).
- **Operational Transformation (OT)**: A conflict resolution algorithm (used in Google Docs) that transforms operation indexes to account for concurrent edits.
- **Leaderless Replication (Dynamo-style)**: A topology where any replica can accept writes directly from clients, and reads/writes are sent to multiple nodes in parallel.
- **Read Repair**: A mechanism in leaderless systems where clients detect stale data during a read and write the newer value back to the stale replica.
- **Hinted Handoff**: A mechanism where a replica temporarily stores writes on behalf of an offline replica, delivering them when the node recovers.
- **Anti-Entropy**: A background process that periodically compares replicas and copies missing data to resolve inconsistencies.
- **Quorum**: The minimum number of votes required for a read ($r$) or write ($w$) to be valid. The strict quorum condition is $w + r > n$.
- **Sloppy Quorum**: Allowing writes to succeed on any reachable node in the network, even if they aren't the designated replicas for that key, to maintain high availability during network partitions.
- **Happens-Before Relation**: The causal dependency between operations; operation A happens before B if B knows about A, depends on A, or builds upon A.
- **Version Vector**: A collection of version numbers from all replicas used to track causal dependencies and detect concurrent writes across multiple nodes.

# @Objectives
- Architect replication systems that precisely balance the trade-offs between availability, durability, latency, and consistency based on explicit business requirements.
- Prevent data loss, data corruption, and anomalous user experiences (like seeing time move backward or losing own writes) caused by replication lag and network faults.
- Guide the implementation of robust conflict resolution mechanisms in multi-leader and leaderless topologies, actively avoiding data-loss strategies like LWW when data preservation is critical.
- Ensure disaster recovery and high availability mechanisms (like failover) do not inadvertently cause catastrophic system failures (e.g., split brain).

# @Guidelines

## Single-Leader Replication
- The AI MUST recommend Single-Leader replication by default for workloads requiring strong consistency, simple conflict avoidance, and centralized write ordering.
- When configuring replication synchronization, the AI MUST explicitly advise against making all followers synchronous, as any single node failure will halt all writes.
- The AI MUST recommend Semi-Synchronous replication (one sync follower, remainder async) to guarantee durability on at least two nodes without sacrificing overall availability.
- When designing failover protocols, the AI MUST explicitly require a mechanism (e.g., STONITH/fencing) to prevent Split Brain. 
- The AI MUST warn that promoting an asynchronous follower during failover can lead to lost writes, and MUST advise checking application compatibility with discarded transactions (especially if interacting with external systems like Redis or email servers).
- For replication logs, the AI MUST recommend Logical (Row-Based) Logs over Write-Ahead Logs (WAL) if the system requires zero-downtime rolling upgrades, heterogenous database versions, or Change Data Capture (CDC) integrations. The AI MUST NOT use Statement-Based replication unless the application strictly avoids non-deterministic functions (e.g., `NOW()`, `RAND()`).

## Mitigating Replication Lag (Eventual Consistency)
- When a system uses read-scaling (reading from async followers), the AI MUST proactively identify the risk of replication lag anomalies.
- **Read-After-Write**: If a user modifies data, the AI MUST enforce a routing rule that reads the user's own modified data from the leader (or a guaranteed up-to-date replica). For non-user-owned data, the AI may allow reading from followers. If the entire dataset is editable by the user, the AI MUST suggest time-based routing (read from leader for X seconds after a write) or client-timestamp tracking.
- **Monotonic Reads**: To prevent time from moving backward across multiple requests, the AI MUST mandate that a specific user's reads are consistently routed to the same replica (e.g., via hash of User ID), rather than randomly load-balancing across all replicas.
- **Consistent Prefix Reads**: In sharded or independently replicated systems, the AI MUST ensure that causally related writes are routed to the same partition, or require the use of algorithms that track causal dependencies.

## Multi-Leader Replication
- The AI MUST restrict recommendations of Multi-Leader replication to specific use cases: Geo-distributed operations across multiple datacenters, offline-first/local-first clients, and real-time collaborative editing.
- When implementing Multi-Leader, the AI MUST highlight **Conflict Resolution** as the primary architectural challenge.
- The AI MUST attempt to use **Conflict Avoidance** (routing all writes for a specific record to a specific leader) as the first line of defense.
- If conflicts are unavoidable, the AI MUST explicitly warn that Last Write Wins (LWW) causes data loss. LWW MUST ONLY be recommended if losing concurrent updates is strictly acceptable to the business.
- For collaborative data, the AI MUST recommend Automatic Conflict Resolution using CRDTs (for offline/peer-to-peer flexibility) or Operational Transformation (for centralized collaborative processing).
- When evaluating replication topologies (All-to-All, Star, Circular), the AI MUST warn about causal dependency violations (writes overtaking each other) in All-to-All networks and mandate the use of Version Vectors to order events correctly.

## Leaderless Replication (Dynamo-Style)
- The AI MUST configure leaderless systems using Quorum math: $w + r > n$. 
- For read-heavy workloads, the AI MUST suggest decreasing $r$ and increasing $w$ (while maintaining $w + r > n$), but MUST warn that if $w = n$, a single node failure halts all writes.
- The AI MUST explicitly state that $w + r > n$ does *not* guarantee strict linearizability. The AI MUST warn about edge cases: sloppy quorums, failed writes not rolling back, and concurrent write timing issues.
- To ensure leaderless nodes catch up on missed data, the AI MUST implement both Read Repair (for frequently accessed data) and Anti-Entropy background processes (for rarely accessed data).
- For high-availability under severe network partitions, the AI may suggest Sloppy Quorums and Hinted Handoff, but MUST explicitly warn that $w + r > n$ is broken during this state, and reads will be stale until the partition heals.
- The AI MUST NOT use wall-clock timestamps to detect concurrent writes in a leaderless system. It MUST mandate the use of Version Vectors (or Dotted Version Vectors) to capture the happens-before relationship and detect true concurrency.

# @Workflow
1. **Analyze Topology Needs**: Determine if the system requires cross-region writes, offline client support, or extreme write availability (points to Multi-Leader or Leaderless). If write centralization and strong consistency are paramount, select Single-Leader.
2. **Define Synchrony & Quorums**: 
   - For Single-Leader: Configure one synchronous replica and N asynchronous replicas.
   - For Leaderless: Define $n$ (total replicas), $w$ (write quorum), and $r$ (read quorum) ensuring $w + r > n$.
3. **Design the Log / Sync Mechanism**: Select logical row-based logs for single-leader to ensure upgrade paths. For leaderless, configure anti-entropy and read repair.
4. **Implement Lag Mitigations**: Map out the user journey. Apply Read-Your-Writes routing for user-edited data. Apply replica-pinning for Monotonic Reads.
5. **Design Conflict Resolution**: If Multi-Leader or Leaderless, identify all concurrent write vectors. Select CRDTs, OT, or deterministic manual sibling merging. Avoid LWW unless explicitly authorized to discard data.
6. **Architect Fault Recovery**: Define the failover timeout. Implement STONITH/fencing. Define the process for a recovered node to catch up (LSN syncing or hinted handoff).

# @Examples (Do's and Don'ts)

### Single-Leader and Replication Lag
- **[DO]**: `if (request.userId == profile.ownerId) { routeTo(LEADER); } else { routeTo(FOLLOWER); }`
- **[DON'T]**: Route a user's profile update to the leader, and then immediately redirect their page reload to a round-robin load balancer across all asynchronous followers, causing their update to seemingly disappear.

### Failover and Split Brain
- **[DO]**: Use a distributed consensus system (like ZooKeeper/etcd) with node fencing (shutting off the power port of the old leader) before promoting a new leader.
- **[DON'T]**: Rely solely on a 5-second network ping timeout to promote a new leader without isolating the old leader, leading to two nodes accepting writes simultaneously.

### Log Formats
- **[DO]**: Use logical (row-based) replication logs so that followers can run Database Version 2.0 while the leader runs Database Version 1.0, enabling zero-downtime upgrades.
- **[DON'T]**: Use statement-based replication for queries like `INSERT INTO users (id, created_at) VALUES (uuid(), NOW())`, which will generate different IDs and timestamps on every replica.

### Multi-Leader Conflict Resolution
- **[DO]**: Use a CRDT for a collaborative text editor so that concurrent character insertions by two offline users are merged deterministically without data loss.
- **[DON'T]**: Use Last Write Wins (LWW) for an e-commerce shopping cart, where User A adding "Shoes" and User B adding "Hat" results in one of the items being permanently deleted based on network arrival time.

### Leaderless Concurrency
- **[DO]**: Use Version Vectors (e.g., `[ReplicaA: 2, ReplicaB: 1, ReplicaC: 3]`) returned to the client on read, which the client must pass back on write, allowing the database to accurately determine if a write is an overwrite or a concurrent conflict.
- **[DON'T]**: Use a standard Unix timestamp to resolve conflicts across leaderless nodes, as NTP clock drift will inevitably cause a causally later write to be discarded because its node had a slightly slower clock.