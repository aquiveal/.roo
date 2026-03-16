- **@Domain**
Activation conditions: Triggers when the AI encounters tasks, architectural designs, or file modifications involving distributed systems coordination, leader election, distributed locking, distributed transactions, strict ordering of operations, cross-node consistency models, or the resolution of split-brain and network partition scenarios.

- **@Vocabulary**
  - **Linearizability (Strong/Atomic Consistency)**: A consistency guarantee making a system appear as if there were only one copy of the data, where every operation takes effect atomically at a specific point in time.
  - **Causality**: The "happens-before" relationship defining the dependency of events in a distributed system. Weaker than linearizability but avoids coordination bottlenecks.
  - **Total Order Broadcast**: A protocol ensuring that all nodes receive the exact same messages in the exact same sequence.
  - **Two-Phase Commit (2PC)**: A distributed transaction algorithm consisting of a prepare phase and a commit phase, managed by a coordinator.
  - **Coordinator**: The node responsible for managing a distributed transaction or consensus process across cohorts (participants).
  - **Consensus**: A fault-tolerant agreement problem where multiple nodes must agree on a single value or decision (e.g., electing a leader) and cannot change their minds once decided.
  - **Split-Brain**: A catastrophic failure mode where two or more nodes simultaneously believe they are the leader, risking data corruption.
  - **Fencing Token**: A monotonically increasing number granted by a lock service every time a lock is acquired, used by storage systems to reject writes from deposed, out-of-sync leaders.
  - **Epoch / Term Number**: A monotonically increasing integer used in consensus algorithms to distinguish newer leader elections from older ones, guaranteeing that the newest leader’s decisions take precedence.
  - **CAP Theorem**: The principle that a distributed system can only provide two out of three guarantees when a network Partition occurs: Consistency (Linearizability) or Availability.

- **@Objectives**
  - Architect distributed systems that correctly balance consistency requirements (e.g., linearizability vs. causality) against performance and availability trade-offs.
  - Ensure absolute protection against split-brain scenarios and data corruption using proven consensus algorithms and fencing mechanisms.
  - Implement distributed transactions safely, accounting for partial failures, coordinator crashes, and network partitions.
  - Translate abstract consistency requirements into concrete, logically sound distributed coordination implementations without relying on unproven proprietary protocols.

- **@Guidelines**
  - When encountering distributed locking mechanisms, the AI MUST implement a **Fencing Token** architecture to prevent stalled or paused clients from erroneously writing data after their lock has expired.
  - The AI MUST NOT rely on local system clocks or time-of-day timestamps for ordering distributed events; it MUST use logical clocks, sequence numbers, or vector clocks to establish **Causality**.
  - When a system requires operations to appear instantaneous and strictly ordered, the AI MUST mandate **Linearizability**, but MUST warn the user about the latency overhead and availability risks during network partitions (as dictated by the **CAP Theorem**).
  - The AI MUST explicitly differentiate between **Serializability** (an isolation guarantee for transactions) and **Linearizability** (a recency guarantee for individual objects).
  - When designing distributed transactions across multiple databases or partitions, the AI MUST use **Two-Phase Commit (2PC)** while explicitly handling the edge case of a coordinator crash (blocking state).
  - The AI MUST NOT attempt to build custom consensus protocols. Whenever leader election, service discovery, or distributed state agreement is required, the AI MUST integrate established consensus systems (e.g., ZooKeeper, etcd, Consul) utilizing Raft or Paxos.
  - When reviewing code for consensus-based leader election, the AI MUST verify that all state-changing requests include an **Epoch/Term Number** to invalidate requests from ghost leaders.
  - For systems needing high availability that cannot afford linearizability delays, the AI MUST design around **Causal Consistency** using version vectors or totally ordered broadcast.

- **@Workflow**
  1. **Analyze Consistency Needs**: Determine if the requested data flow requires Linearizability (single-source-of-truth illusion) or Causal Consistency (preservation of happens-before relationships). 
  2. **Assess Network Constraints (CAP)**: Evaluate the system's tolerance for network partitions. If Availability is critical, downgrade from Linearizability to Causal/Eventual consistency.
  3. **Establish Ordering**: Define the mechanism for event ordering. Use a single-leader sequence generator for Total Order Broadcast, or version vectors for decentralized causal ordering.
  4. **Design the Consensus Layer**: For leader election or distributed agreement, implement a standard consensus tool (e.g., ZooKeeper, etcd). Assign strictly increasing Epoch/Term numbers to every new leader.
  5. **Secure Distributed Locks**: Whenever distributed locks are requested, immediately generate a Fencing Token mechanism. Update the target storage layer to reject writes containing token numbers lower than the highest seen token.
  6. **Handle Multi-Node Transactions**: If data spans multiple partitions/databases, implement 2PC. Define the Coordinator node, code the Prepare phase (ensuring all cohorts write to stable storage), and code the Commit/Abort phase. Add recovery logic for Coordinator failure.
  7. **Failure Scenario Validation**: Audit the design against partial failures (e.g., message drops, process pauses). Ensure no split-brain writes can bypass the Fencing Token or Epoch Number validation.

- **@Examples (Do's and Don'ts)**
  - **[DO]** Use a fencing token passed to the database to ensure a delayed process cannot overwrite data after losing a distributed lock.
    ```python
    # Acquiring the lock returns a monotonically increasing fencing token
    lock_token = coordination_service.acquire_lock("resource_x")
    
    # The storage layer rejects any write if it has seen a higher token
    db.execute("UPDATE table SET val = %s WHERE id = %s AND last_token <= %s", 
               (new_val, resource_id, lock_token))
    ```
  - **[DON'T]** Rely solely on a time-based lease or heartbeat timeout for distributed locks without a fencing mechanism, as a garbage collection pause can cause the lease to expire silently.
    ```python
    # INCORRECT: The process might pause here, lose the lock, wake up, and blindly write.
    if coordination_service.has_lock("resource_x"):
        db.execute("UPDATE table SET val = %s", (new_val,))
    ```
  - **[DO]** Use an established consensus system like ZooKeeper or etcd (which implement Raft/ZAB) to handle leader election and consensus tasks.
  - **[DON'T]** Build a custom heartbeat-based ping system in application code to dynamically elect a leader, as it will inevitably fail to handle asynchronous network delays and result in a split-brain.
  - **[DO]** Design Two-Phase Commit (2PC) operations to hold transaction locks on cohorts until the coordinator explicitly sends the final commit or abort signal.
  - **[DON'T]** Confuse replication (like asynchronous single-leader replication) with consensus; replication does not guarantee agreement if the leader crashes before propagating the log.