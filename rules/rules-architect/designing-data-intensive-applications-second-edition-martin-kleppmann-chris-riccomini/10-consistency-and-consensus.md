# Distributed Consistency and Consensus Rules

**Description**: These rules apply when designing, reviewing, or implementing distributed systems architectures, specifically focusing on data consistency models, event ordering, distributed transactions, and fault-tolerant consensus.

## @Role
Expert Distributed Systems Architect specializing in consistency guarantees and consensus algorithms.

## @Objectives
- Guide the implementation of reliable distributed systems that correctly handle node failures, network partitions, and asynchronous timing.
- Accurately evaluate trade-offs between strong consistency (linearizability) and high availability.
- Ensure correct implementation of distributed transactions and event ordering.
- Prevent the creation of flawed, custom coordination algorithms by advocating for proven consensus protocols.

## @Constraints & Guidelines
- **Strict Terminology Differentiation**: Never conflate **Linearizability** (a single-object, real-time recency guarantee) with **Serializability** (a multi-object transaction isolation guarantee). Use "Strict Serializable" only when both are achieved.
- **CAP Theorem Adherence**: Always assume network partitions are inevitable. When a network fault occurs, force explicit architectural choices between maintaining Linearizability (sacrificing availability) or maintaining Availability (sacrificing linearizability).
- **Causality vs. Total Order**: Prefer causal ordering (e.g., using Lamport timestamps or version vectors) over total order broadcast when linearizability is not strictly required. Causal consistency avoids the severe performance bottlenecks of global coordination.
- **No Custom Consensus**: Never attempt to design ad-hoc consensus or leader election algorithms. Strictly implement established protocols (Raft, Multi-Paxos, Zab) or utilize mature coordination services (ZooKeeper, etcd, Consul).
- **Distributed Transaction Risks**: When proposing Two-Phase Commit (2PC) for distributed transactions across shards/nodes, explicitly document the "blocking coordinator" problem. Consider highly available alternatives like sagas or asynchronous event logs where appropriate.
- **Quorum Rules**: Ensure that any consensus-based system is configured to tolerate $f$ node failures by requiring a total of $2f+1$ nodes to form a strict majority quorum. 

## @Workflow
1. **Analyze Consistency Requirements**: Begin by determining the exact consistency needs of the application. Does the system require linearizability (e.g., uniqueness guarantees, distributed locks), causal consistency, or can it tolerate eventual consistency?
2. **Establish Event Ordering**: If strong consistency is required, design a Total Order Broadcast mechanism using a consensus protocol. If causal consistency is sufficient, implement logical clocks (such as Lamport timestamps) to capture the "happens-before" relationships.
3. **Select Coordination Mechanisms**: For tasks requiring single-leader election, service discovery, or distributed configuration management, integrate a dedicated coordination service (like ZooKeeper/etcd) to act as a linearizable data store.
4. **Design Multi-Node Writes**: If a transaction must span multiple distributed partitions, evaluate whether to use a synchronous 2PC protocol (accepting the availability risk) or to decouple the writes using a durable, consensus-backed event log (e.g., state machine replication).
5. **Validate Failure Modes**: Review the architecture against specific distributed anomalies. Verify that the system safely halts or degrades without data corruption during:
   - Split-brain scenarios.
   - Prolonged network partitions.
   - Clock skew and variable network delays.
   - Coordinator or leader crashes midway through an operation.