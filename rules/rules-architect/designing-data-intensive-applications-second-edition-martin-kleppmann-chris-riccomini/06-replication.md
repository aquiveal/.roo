# @Domain
This rule file is triggered when the AI is tasked with designing, implementing, configuring, or debugging distributed data systems, database replication strategies, high availability architectures, sync engines (offline-first/local-first software), multi-datacenter deployments, state conflict resolution algorithms, or mitigating data anomalies resulting from replication lag and network partitions.

# @Vocabulary
- **Replication**: Keeping a copy of the same data on multiple machines connected via a network to decrease latency, increase availability, and scale read throughput.
- **Replica**: A node that stores a copy of the database.
- **Single-Leader (Primary-Backup / Active-Passive)**: A topology where one replica (the leader) accepts all writes, and streams data changes to other replicas (followers/read replicas).
- **Synchronous Replication**: The leader waits for a follower to confirm it received a write before reporting success to the client.
- **Asynchronous Replication**: The leader sends the write to the follower but does not wait for a response.
- **Semi-Synchronous Replication**: A configuration where exactly one follower is synchronous and the others are asynchronous, ensuring at least two up-to-date nodes.
- **Failover**: The process of promoting a follower to leader, reconfiguring clients, and redirecting followers after a leader failure.
- **Split Brain**: A dangerous scenario where two nodes simultaneously believe they are the leader, potentially leading to data corruption.
- **Fencing / STONITH**: Mechanisms used to shut down an old leader to prevent split-brain scenarios.
- **Statement-Based Replication**: Replicating raw SQL queries (e.g., `INSERT`, `UPDATE`). Prone to nondeterminism issues (e.g., `NOW()`).
- **Write-Ahead Log (WAL) Shipping**: Replicating low-level byte changes in disk blocks. Tightly couples the replica to the specific storage engine version.
- **Logical (Row-Based) Replication**: Replicating the decoupled, granular data changes (inserted/deleted/updated rows), allowing version mismatches between leader and follower.
- **Change Data Capture (CDC)**: Parsing a logical log to send database contents to external systems (e.g., data warehouses).
- **Eventual Consistency**: The temporary state where followers lag behind the leader, but will eventually catch up if writes stop.
- **Replication Lag**: The delay between a write happening on the leader and reflecting on a follower.
- **Read-After-Write (Read-Your-Writes) Consistency**: A guarantee that a user reloading a page will always see the updates they just submitted.
- **Monotonic Reads**: A guarantee that a user will not see time move backward (i.e., reading stale data after having previously read newer data).
- **Consistent Prefix Reads**: A guarantee that observers will see causally related writes in the correct, logical order.
- **Availability Zones / Regions**: A region is a geographic location containing multiple availability zones (independent datacenters).
- **Multi-Leader (Active-Active) Replication**: A setup where multiple nodes can accept writes and asynchronously replicate them to each other. Used for geo-distribution and local-first software.
- **Sync Engine**: Software coordinating asynchronous multi-leader replication between end-user devices (local-first/offline-first) and a server.
- **Conflict Resolution**: The algorithmic or manual process of merging concurrent, diverging writes on different leaders.
- **Last Write Wins (LWW)**: A conflict resolution strategy that resolves conflicts by keeping the write with the highest timestamp and discarding others. Prone to data loss.
- **CRDT (Conflict-Free Replicated Datatype)**: A data structure that automatically resolves conflicts using commutative operations or unique identifiers instead of indexes.
- **Operational Transformation (OT)**: A conflict resolution algorithm heavily used in collaborative text editing that transforms operation indexes based on concurrent edits.
- **Leaderless (Dynamo-style) Replication**: A topology where any replica accepts writes directly from clients or via a coordinator, without enforcing a strict write order.
- **Quorum Reads/Writes**: A configuration where $w$ (write nodes) + $r$ (read nodes) > $n$ (total replicas), guaranteeing that at least one read node possesses the most recent write.
- **Read Repair**: A leaderless mechanism where a client detecting stale data during a read immediately writes the newer data back to the stale replica.
- **Hinted Handoff**: A leaderless mechanism where a functioning node temporarily stores writes intended for an offline node, delivering them when it recovers.
- **Anti-Entropy**: A background process in leaderless databases that continually compares replicas and copies missing data.
- **Sloppy Quorum**: Allowing writes to succeed on *any* reachable nodes (even those not officially designated for the key) during a network partition.
- **Request Hedging**: Sending read requests to multiple replicas in parallel and using the fastest response to mitigate tail latency and gray failures.
- **Happens-Before Relation**: The defining characteristic of causality; operation A happens before B if B knows about, depends on, or builds upon A.
- **Concurrent Writes**: Two writes where neither knows about the other (neither happens-before the other), regardless of exact physical time.
- **Version Vector**: A collection of version numbers (one per replica) used to capture causality and detect concurrent writes accurately without relying on physical clocks.
- **Zero-Disk Architecture (ZDA)**: A system design where nodes have no persistent state, utilizing object storage for all persistence and local disks purely for caching.

# @Objectives
- Architect replication systems that balance high availability, latency, and consistency based on the specific application requirements.
- Select the appropriate replication topology (Single-Leader, Multi-Leader, Leaderless) using deliberate, heavily weighted trade-off analysis.
- Prevent data loss and corruption during node failures, network partitions, and failovers.
- Mitigate UX degradation caused by replication lag by implementing strict consistency guarantees (Read-Your-Writes, Monotonic Reads, Consistent Prefix Reads) where appropriate.
- Systematically manage distributed write conflicts using deterministic algorithms (CRDTs, OT, Version Vectors) rather than relying on flawed physical clock comparisons (LWW).

# @Guidelines
- **Replication Topology Selection**:
  - The AI MUST use Single-Leader replication for general-purpose workloads requiring strong consistency and serializable transactions.
  - The AI MUST use Multi-Leader replication *only* when required by multi-datacenter (geo-distributed) latency constraints, high tolerance to regional outages, or local-first/offline-first synchronization engines.
  - The AI MUST use Leaderless replication for workloads requiring ultra-high availability, tolerance to gray failures/latency spikes, and where eventual consistency is fully acceptable.
- **Synchrony vs. Asynchrony**:
  - The AI MUST NOT recommend fully synchronous replication across all nodes (as one failure stalls the entire system).
  - The AI MUST recommend Semi-Synchronous replication (one synchronous follower, the rest asynchronous) to guarantee durability without sacrificing total availability.
  - The AI MUST explicitly state the durability risks (data loss on leader failure) when configuring fully asynchronous replication.
- **New Follower Setup**:
  - The AI MUST NOT suggest copying raw data files of an active database.
  - The AI MUST define a process of taking a consistent snapshot, copying the snapshot, and connecting to the leader using the exact log sequence number / binlog coordinate of that snapshot to catch up.
- **Handling Failover (Single-Leader)**:
  - The AI MUST account for the risks of automatic failover: split-brain scenarios, discarding asynchronous writes, and cascading failures due to aggressive timeouts.
  - The AI MUST recommend STONITH (fencing) mechanisms if automatic failover is configured.
  - The AI MUST ensure that the promoted follower is the most up-to-date replica to minimize data loss.
- **Replication Log Implementation**:
  - The AI MUST recommend Logical (row-based) logging over Statement-based (due to non-determinism) and WAL shipping (due to storage engine version coupling).
  - The AI MUST utilize Logical logs when configuring Change Data Capture (CDC).
- **Mitigating Replication Lag Anomalies**:
  - **Read-Your-Writes**: The AI MUST route reads for a user's *own* mutable data directly to the leader (or a synchronous follower). Alternatively, use logical timestamps to pause reads until the follower catches up.
  - **Monotonic Reads**: The AI MUST route all of a single user's reads to the *same* replica (e.g., using a hash of the user ID) to prevent time from appearing to move backward.
  - **Consistent Prefix Reads**: The AI MUST ensure causally related writes are routed to the same shard or tracked explicitly, preventing users from seeing a response before the corresponding question.
- **Multi-Leader Topologies & Routing**:
  - The AI MUST warn against circular and star topologies due to single points of failure.
  - The AI MUST favor all-to-all topologies while actively mitigating causal ordering issues (messages overtaking each other).
  - The AI MUST ensure messages are tagged with node identifiers to prevent infinite replication loops.
- **Conflict Resolution (Multi-Leader/Leaderless)**:
  - The AI MUST attempt to avoid conflicts entirely by routing writes for a specific record to a dedicated leader based on user/tenant ID.
  - The AI MUST strongly warn against Last Write Wins (LWW) if data loss (dropped concurrent writes) is unacceptable.
  - The AI MUST implement or recommend CRDTs or Operational Transformation (OT) for automatic, lossless merging of concurrent writes.
  - The AI MUST explicitly define how sibling values will be surfaced to and merged by the application layer if manual resolution is chosen.
- **Leaderless Quorums & Resilience**:
  - The AI MUST enforce the quorum condition $w + r > n$ to ensure reads overlap with the most recent write.
  - The AI MUST NOT treat $w + r > n$ as an absolute guarantee of strong consistency (accounting for node restores, concurrent write/reads, and partial write failures).
  - The AI MUST recommend Request Hedging (sending reads to multiple replicas and accepting the fastest) to mitigate tail latency and gray failures.
  - The AI MUST utilize Read Repair (client-driven) and Anti-Entropy (background process) to maintain eventual consistency.
- **Detecting Concurrency**:
  - The AI MUST NOT use physical timestamps to definitively determine causality or concurrency.
  - The AI MUST use Version Vectors (or dotted version vectors) to track causal histories per replica and key, accurately differentiating between overwrites and concurrent conflicting siblings.

# @Workflow
1. **Analyze Requirements**: Evaluate the specific needs for read/write scaling, geographic distribution, latency constraints, and offline availability.
2. **Select Topology**: Choose Single-Leader (default/consistency), Multi-Leader (geo/offline), or Leaderless (high availability/latency tolerance).
3. **Configure Synchrony/Quorum**:
   - *If Single-Leader*: Configure Semi-Synchronous replication to balance durability and write availability.
   - *If Leaderless*: Define $n$, $w$, and $r$ values based on the read/write load ratio, ensuring $w + r > n$ for standard quorum consistency.
4. **Design Failover & Recovery**: Establish snapshot-based bootstrapping for new followers. Define timeout thresholds, split-brain fencing (STONITH), and promotion logic for leader failures.
5. **Mitigate Lag Anomalies**: Implement routing logic to satisfy Read-Your-Writes (e.g., read own data from leader) and Monotonic Reads (e.g., hash-based replica pinning).
6. **Implement Conflict Management**:
   - Map out the Happens-Before relationships using Version Vectors.
   - Define a deterministic conflict resolution strategy (CRDTs, OT, or explicit application-level sibling merging). Explicitly reject LWW unless intentional data loss is approved.
7. **Ensure Compatibility**: Decouple storage formats using Logical (row-based) replication logs to allow rolling upgrades and CDC.

# @Examples (Do's and Don'ts)

**Principle: Replication Logging**
- [DO]: Configure logical (row-based) replication to allow zero-downtime upgrades and decouple the log from the storage engine implementation.
- [DON'T]: Use statement-based replication (e.g., raw SQL) without strict determinism guarantees, as functions like `NOW()` or `RAND()` will cause replicas to diverge.

**Principle: Read-Your-Own-Writes Consistency**
- [DO]: Track the logical timestamp of a user's latest write and ensure the load balancer only routes their read requests to followers that have processed up to that exact timestamp.
- [DON'T]: Route a user's post-write redirect randomly across a pool of fully asynchronous followers, which will sporadically result in the user thinking their data was deleted.

**Principle: Monotonic Reads**
- [DO]: Use a consistent hashing mechanism based on the `user_id` to route all read queries from a specific user to the exact same follower replica during their session.
- [DON'T]: Round-robin read queries across all replicas for a single user's session, which risks them reading a fresh replica followed immediately by a stale replica.

**Principle: Conflict Resolution**
- [DO]: Use a Version Vector (tracking the version per replica per key) to detect concurrent writes, and implement a CRDT to deterministically merge the divergent states.
- [DON'T]: Default to Last Write Wins (LWW) using physical system clocks to resolve concurrent shopping cart updates, resulting in dropped items and lost revenue.

**Principle: Failover Configuration**
- [DO]: Require manual intervention or implement strict fencing (STONITH) mechanisms before automatically promoting a follower to leader, to guarantee the old leader is completely offline.
- [DON'T]: Configure an aggressively short timeout for automatic failover without fencing, risking a split-brain scenario if the leader is merely experiencing a temporary garbage collection pause or network latency spike.

**Principle: Quorum Configuration (Leaderless)**
- [DO]: Set $n=5$, $w=3$, $r=3$ to ensure strict quorum overlap ($w+r > n$) while tolerating up to two concurrent node failures.
- [DON'T]: Set $n=5$, $w=2$, $r=2$ and expect to always read the latest data, as the read and write nodes may not overlap.