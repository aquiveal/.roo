@Domain
These rules MUST trigger when the AI is tasked with designing, configuring, or implementing Apache Kafka broker infrastructure, defining topic configurations, scaling Kafka clusters, setting producer/consumer properties for durability and ordering, implementing long-term storage or compacted topics, or establishing Kafka security, tenant segregation, and quotas.

@Vocabulary
- **Partitioned Log**: The underlying hardware-sympathetic abstraction of Kafka; a set of append-only files spread over multiple machines enabling O(1) sequential reads/writes.
- **Zero-Copy**: An efficiency mechanism where data is copied directly from the disk buffer to the network buffer without entering the JVM.
- **Partitioner**: The producer component that determines which partition a message is routed to, typically using either round-robin or a hash of a provided message key.
- **Consumer Group**: A load-balanced collection of consumers that share reading the partitions of a topic, guaranteeing that a single partition is assigned to only one consumer instance at a time.
- **Quotas**: Bandwidth segregation controls used to allocate specific throughput bounds to services or consumer groups, preventing multitenant noisy-neighbor issues.
- **Compacted Topics**: A specialized topic type that acts like a log-structured merge-tree, asynchronously removing superseded messages sharing the same key to retain only the most recent event.
- **Latest-Versioned Pattern**: An architectural pattern combining both a retention-based topic (for history) and a compacted topic (for footprint reduction), linked together by a Kafka Streams job.

@Objectives
- Design Kafka deployments as high-throughput, horizontally scalable distributed storage systems rather than traditional ephemeral message brokers.
- Maximize performance by adhering to log-structured, sequential disk access patterns and zero-copy principles.
- Guarantee strict message ordering and data durability in business-critical architectures.
- Ensure multiservice ecosystem stability by strictly enforcing quotas and multitenant load segregation.
- Optimize topic configurations for specific data access patterns (e.g., compacted topics for keyed data tables vs. retention topics for event sourcing).

@Guidelines
- **Broker Paradigm vs. Traditional Messaging**: The AI MUST NOT apply traditional messaging patterns (like JMS message selectors, index structures, or B-trees) to Kafka designs. Instead, the AI MUST leverage append-only logs and sequential access.
- **Performance & Zero-Copy**: The AI MUST design consumption patterns that allow Kafka to transfer data directly from disk buffer to network buffer, minimizing unnecessary JVM processing on the broker.
- **Strict Ordering Guarantees**: 
  - When relative ordering is required (e.g., updates to the same customer), the AI MUST instruct the producer to apply a consistent hashing key to the messages.
  - When global ordering is strictly required across an entire dataset (e.g., legacy system migrations), the AI MUST configure the topic with a single partition, and explicitly document the resulting single-machine throughput bottleneck.
- **Producer Durability & Retries**:
  - The AI MUST explicitly enable retries in producer configurations.
  - To prevent message reordering during retries, the AI MUST configure producers to send batches one at a time per destination machine (e.g., setting `max.in.flight.requests.per.connection=1` or enabling idempotence).
  - For sensitive datasets, the AI MUST set the replication factor to 3 and configure the producer to wait for full replication before acknowledging (`acks=all`).
- **Disk Flushing Protocol**: The AI MUST AVOID configuring synchronous disk flushing. If an extreme edge case (e.g., single-machine deployment) demands synchronous flushing, the AI MUST significantly increase the producer batch size to mitigate the severe throughput penalty.
- **High Availability & Load Balancing**: The AI MUST deploy event-driven services in a Highly Available (HA) configuration (multiple instances) and explicitly use Kafka's consumer group functionality to ensure partitions are automatically load-balanced and safely reassigned during failure.
- **Multitenant Protection (Quotas)**: In multiservice ecosystems, the AI MUST define and apply Kafka Quotas to individual service instances or consumer groups to strictly enforce SLAs and prevent accidental Denial-of-Service (DoS) attacks.
- **Topic Type Selection**:
  - The AI MUST use standard retention-based topics for audit logs, Event Sourcing, and general notification flows.
  - The AI MUST use Compacted Topics for keyed datasets (e.g., product catalogs, database tables) to slow dataset growth and accelerate stateful stream processing loads.
  - The AI MUST implement the "Latest-Versioned Pattern" when both a full historical audit and an optimized latest-state cache are simultaneously required.
- **Data Deletion**: To delete data in a compacted topic, the AI MUST instruct the producer to send a new message with the target key and a `null` value (tombstone).
- **Security Enforcement**: The AI MUST enforce enterprise-grade security by implementing authentication (Kerberos or TLS client certificates), authorization (Unix-like ACLs), and network encryption (TLS). The AI MUST also require authentication for communication between Kafka brokers and ZooKeeper.

@Workflow
1. **Analyze the Data Profile**: Determine if the dataset represents a stream of immutable historical facts (requires retention-based topic) or an evolving table of current states (requires a compacted topic).
2. **Determine Partitioning & Ordering Strategy**: 
   - Assign a consistent message key if relative ordering is required.
   - Use round-robin (no key) if ordering does not matter and throughput is the sole priority.
   - Restrict to 1 partition ONLY if global ordering is an absolute architectural requirement.
3. **Configure the Producer for Durability**: Enable retries, restrict in-flight requests to 1 (or use idempotent producers) to prevent reordering on failure, and require full replica acknowledgment (`acks=all`).
4. **Implement Service Resiliency**: Assign consuming applications to a consumer group and provision at least two instances to inherit native load balancing and partition-failover semantics.
5. **Protect the Cluster**: Apply network security (TLS, Kerberos, ACLs) and configure bandwidth quotas to sandbox the service's throughput.

@Examples (Do's and Don'ts)

- **Ordering and Retries**
  - [DO]: Configure the producer with `retries=Integer.MAX_VALUE` and `max.in.flight.requests.per.connection=1` (or `enable.idempotence=true`) to guarantee both delivery and strict ordering during transient network failures.
  - [DON'T]: Enable retries while leaving `max.in.flight.requests.per.connection` at its default (>1), which explicitly risks interleaving batches and destroying message order upon a failure and retry.

- **Topic Configuration for Reference Data**
  - [DO]: Create a Compacted Topic for a "Customer Database" replication stream so that superseded customer records are purged and the footprint remains optimal for fast service startup.
  - [DON'T]: Use a standard time-based retention topic for an active database table replication stream, as the service will be forced to replay the entire history of every row change just to build the current state.

- **Global Ordering**
  - [DO]: Use a single partition topic if the legacy consumer requires absolute global ordering, while explicitly accepting that throughput is permanently capped to a single machine's disk/network capacity.
  - [DON'T]: Attempt to maintain global ordering across a topic with multiple partitions by writing complex client-side reassembly logic.

- **Cluster Protection**
  - [DO]: Assign a specific Quota limit (e.g., 50 MB/s) to a new microservice before deploying it to the shared production Kafka cluster.
  - [DON'T]: Deploy new services to a shared cluster without quotas, risking a badly configured loop or aggressive historical replay bringing down the entire company's central nervous system.

- **Handling State Deletion**
  - [DO]: Publish a message with the key `CustomerId: 123` and a `null` payload to physically remove a record from a compacted topic during a GDPR "Right to be Forgotten" request.
  - [DON'T]: Attempt to issue a generic delete command or drop the entire topic to remove a single keyed record.