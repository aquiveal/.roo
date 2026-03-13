# @Domain
Activates when the AI is tasked with architecting, implementing, evaluating, or debugging distributed systems features related to "Consistency and Consensus". *(Note: Because the specific Chapter 10 "Consistency and Consensus" is marked as unavailable in the source text, these rules are exhaustively extracted from the foundational principles of consistency, replication lag, quorums, ACID guarantees, and consensus algorithms detailed across the provided Chapters 6, 7, and 8).*

# @Vocabulary
- **Eventual Consistency**: The temporary state of inconsistency between replicas; given no new writes, all followers will eventually catch up to the leader's state.
- **Read-After-Write (Read-Your-Writes) Consistency**: A guarantee that if a user reloads a page or queries the system, they will always see the updates they submitted themselves.
- **Monotonic Reads**: A consistency guarantee preventing users from seeing time move backward (i.e., reading an older state after previously reading a newer state).
- **Consistent Prefix Reads**: A guarantee that readers will observe causally related writes in the exact order they occurred.
- **Quorum Consistency ($w + r > n$)**: A configuration in leaderless systems where the sum of required write ($w$) and read ($r$) acknowledgments exceeds the total number of replicas ($n$), ensuring the read and write node sets overlap.
- **Sloppy Quorum**: A configuration allowing any reachable replica to accept writes during a network interruption, even if it is not the designated replica for that key.
- **ACID Consistency**: An application-specific requirement that data must always satisfy certain invariants (e.g., credits and debits must balance), transitioning the database from one valid state to another.
- **Consensus**: The process of distributed nodes agreeing on a state or value, such as electing a new leader or managing shard assignments (implemented via algorithms like Raft, Multi-Paxos, or tools like ZooKeeper/etcd).
- **Split Brain**: A dangerous fault state where two nodes independently believe they are the leader, risking data loss and corruption.
- **Fencing / STONITH (Shoot The Other Node In The Head)**: Mechanisms to forcefully isolate or shut down an outdated leader to prevent a split-brain scenario.

# @Objectives
- Safeguard data integrity and state validity across distributed network replicas.
- Select and enforce the precise consistency model (Eventual, Read-After-Write, Monotonic, Consistent Prefix, or Strong/Serializable) tailored to the application's tolerance for stale data.
- Architect robust failover and shard-routing mechanisms using proven consensus protocols to eliminate split-brain vulnerabilities.
- Ensure application-level ACID consistency by strictly defining database constraints or utilizing atomic multi-object transactions.

# @Guidelines
- **Replication Lag Mitigation**:
  - Do not pretend asynchronous replication is synchronous. Expose and handle eventual consistency anomalies at the application layer.
  - Enforce *Read-After-Write* consistency for user-owned data. Implementation options include: reading the user's own profile exclusively from the leader, tracking the timestamp of the last update to force leader reads for a time window, or tracking the client's logical clock/timestamp and forcing replicas to wait until they catch up.
  - For cross-device *Read-After-Write* consistency, centralize the metadata tracking the user's last update timestamp, and route all of a user's devices to the same datacenter region.
  - Enforce *Monotonic Reads* by consistently routing a specific user's reads to the same replica (e.g., via user ID hashing) rather than random load balancing.
  - Enforce *Consistent Prefix Reads* by ensuring causally related writes are explicitly tracked or directed to the same partition/shard.
- **Quorum Configuration Constraints**:
  - Do not assume a quorum ($w + r > n$) provides absolute strong consistency. Account for edge cases: failed node restorations from old backups, concurrent writes, and partial write failures that are not rolled back.
  - Set $w = r = (n+1)/2$ for standard quorum balance, or $w=n, r=1$ for read-heavy workloads (understanding the tradeoff of heavily degraded write availability).
- **Consensus & Leader Election**:
  - Use established consensus systems (ZooKeeper, etcd, Raft, Multi-Paxos) for leader election, shard routing, and configuration management.
  - Never implement ad-hoc, timeout-based automated failover without strict fencing/STONITH to prevent split-brain.
- **ACID Consistency Enforcement**:
  - Explicitly map application invariants to database constraints (foreign keys, uniqueness, check constraints, triggers, materialized views).
  - If constraints cannot model the invariant, the application logic MUST define the transaction boundaries correctly to preserve consistency; the database cannot protect against bad data if invariants are unstated.

# @Workflow
1. **Analyze Consistency Tolerance**: Determine if the specific data access path can tolerate eventual consistency. If users or downstream systems will break due to stale data, proceed to stronger guarantees.
2. **Select the Consistency Level**:
   - For user-submitted modifications: Apply *Read-After-Write* mechanisms.
   - For sequential viewing/refreshing: Apply *Monotonic Reads*.
   - For causally linked events (e.g., questions and answers): Apply *Consistent Prefix Reads*.
3. **Configure Quorums (If Leaderless)**: Define $n, w, r$ based on the read/write latency and availability targets. Add read-repair and anti-entropy processes to handle missed writes.
4. **Design Consensus and Coordination**: If implementing automated failover or dynamic shard assignment, integrate a consensus layer (Raft/ZooKeeper/etcd) to act as the source of truth for the cluster.
5. **Implement Fencing**: Add STONITH procedures to immediately revoke write access from any node that is falsely acting as a leader during a network partition.
6. **Enforce Invariants**: Translate domain consistency requirements into schema constraints or encapsulate them fully within ACID transactions.

# @Examples (Do's and Don'ts)
- **[DO]** Route all of a user's read requests to the same replica using a hash of their user ID to ensure Monotonic Reads.
- **[DON'T]** Load-balance a user's read requests randomly across asynchronous followers, which can cause data to suddenly disappear (time moving backward) if one replica lags behind another.
- **[DO]** Pass the timestamp of the client's most recent write in subsequent read requests so the replica can block until it has caught up to that timestamp, guaranteeing Read-After-Write consistency.
- **[DON'T]** Rely solely on $w + r > n$ quorums to prevent dirty or stale reads without accounting for the fact that concurrent writes and non-rolled-back partial writes can break the quorum guarantee.
- **[DO]** Utilize a consensus-backed coordination service (like ZooKeeper or etcd) to maintain the authoritative mapping of shards to nodes to prevent conflicting coordinators.
- **[DON'T]** Use a simple ping timeout to automatically promote a new leader without a fencing mechanism, as a temporary network glitch will easily result in a split-brain data corruption.
- **[DO]** Define database-level uniqueness, check, and foreign-key constraints to guarantee ACID consistency for strict application invariants.