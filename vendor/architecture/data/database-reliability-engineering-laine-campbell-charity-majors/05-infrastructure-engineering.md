@Domain
The rules in this file MUST be activated when the AI is engaged in tasks related to database infrastructure engineering, host selection, operating system and kernel tuning for databases, storage subsystem design, network configuration for data tiers, and the evaluation or deployment of virtualization, containers, or Database as a Service (DBaaS) platforms.

@Vocabulary
- **DBRE**: Database Reliability Engineer; a specialized engineer focused on applying repeatable software engineering principles to database operations.
- **SRE**: Software Reliability Engineer / Site Reliability Engineer.
- **Hypervisor / VMM**: Virtual Machine Monitor; software/firmware/hardware that creates and runs virtual machines (VMs).
- **NUMA (Non-Uniform Memory Access)**: A memory design where memory access time depends on the memory location relative to the processor.
- **OOM Killer**: Out of Memory Killer; a Linux kernel feature that terminates processes when the system is critically low on memory.
- **THP (Transparent Huge Pages)**: A Linux memory management system that uses larger memory pages (2 MB or 1 GB) to reduce TLB lookups.
- **TLB (Translation Lookaside Buffer)**: A memory cache that stores recent translations of virtual memory to physical addresses.
- **Swapping**: The process of storing and retrieving data that no longer fits in RAM to disk.
- **I/O Scheduler**: The method the OS uses to decide the order of block-level I/O operations (e.g., noop, deadline, cfq, anticipatory).
- **JBOD (Just a Bunch Of Disks)**: An architecture using multiple independent disks without RAID striping.
- **RAID 0 / 1 / 10**: Redundant Array of Independent Disks configurations (0 = striping, 1 = mirroring, 10 = striped mirrors).
- **fsync()**: An OS call that instructs the storage subsystem to flush in-memory write caches to physical disk.
- **NVRAM**: Non-Volatile Random Access Memory.
- **DBaaS**: Database as a Service (e.g., Amazon RDS).

@Objectives
- Architect database infrastructures that prioritize strict isolation, rapid recovery (MTTR), and horizontal scalability over monolithic, fragile uptime (MTBF).
- Enforce Linux kernel and OS optimizations specifically tailored for heavy, concurrent, low-latency database workloads.
- Design storage subsystems that carefully balance capacity, IOPS, latency, availability, and durability based on explicit dataset requirements.
- Mitigate the inherent risks and abstractions introduced by virtualization, containerization, and DBaaS platforms using rigorous automated failover and validation.

@Guidelines

**Kernel and Operating System Tuning**
- When configuring Linux memory for databases, the AI MUST recommend reserving a portion of physical memory (not allocating it to the DB) to prevent the kernel from entering unpredictable reclaim modes.
- When configuring database binaries, the AI MUST recommend using `jemalloc` or `tcmalloc` instead of the native `glibc` `malloc` to improve concurrency and reduce memory fragmentation.
- When encountering Transparent Huge Pages (THP) on database hosts, the AI MUST explicitly advise disabling defragmentation or disabling THP entirely, as defragmentation causes severe CPU thrashing in databases like Cassandra, Oracle, MySQL, and Hadoop.
- When addressing swap space on a database host, the AI MUST advocate for disabling swap entirely IF a rock-solid automated failover process is in place. The AI MUST prioritize allowing the OOM Killer to terminate the database (triggering failover) over allowing the database to survive in a high-latency, swapped state.
- If swap CANNOT be disabled, the AI MUST adjust OOM scores for database processes to reduce the chance of the kernel killing the database for other memory needs, and MUST configure the OS to avoid swapping out database memory for file cache.
- When configuring databases on NUMA architectures (e.g., MySQL, PostgreSQL, Cassandra, Redis), the AI MUST configure memory interleaving across all nodes (e.g., `numactl --interleave=all`), flush buffer caches right before startup (`sysctl -q -w vm.drop_caches=3`), and force immediate allocation (using `MAP_POPULATE` or `memset`) to prevent allocation imbalances and swap insanity.
- When configuring I/O schedulers for databases on SSDs, the AI MUST use the `noop` scheduler.
- When configuring I/O schedulers for highly concurrent multithreaded database loads on HDDs, the AI MUST use the `deadline` scheduler.
- When configuring OS resources, the AI MUST explicitly increase user resource limits for file descriptors, semaphores, and user processes, as databases exceed standard server defaults.

**Network Configuration**
- When designing network topologies for databases, the AI MUST isolate traffic into distinct channels: internode communications, application traffic, administrative traffic, and backup/recovery traffic (via physical NICs or partitions).
- When configuring TCP/IP for databases, the AI MUST expand available TCP/IP ports, reduce socket recycle times to avoid `TIME_WAIT` exhaustion, and increase the TCP backlog to tolerate connection saturation.

**Storage Architecture**
- When defining database block sizes, the AI MUST ensure they align perfectly with the underlying disk block sizes or filesystem block sizes to prevent wasted I/O operations.
- When configuring storage for SSDs, the AI MUST evaluate smaller database block sizes to optimize B-tree traversal performance.
- When configuring databases for latency-sensitive workloads, the AI MUST configure the database to use direct IO (e.g., `O_DIRECT`) to bypass the OS page cache and avoid multi-millisecond latency impacts.
- When selecting filesystems, the AI MUST specify journaling filesystems (e.g., XFS or EXT4) to reduce corruption risks during crash events.
- When addressing storage durability, the AI MUST verify whether the underlying hardware honors `fsync()` calls. If using a write cache, the AI MUST verify it is battery-backed (NVRAM) before allowing the database to skip `fsync()` flushing.
- When designing storage capacity, the AI MUST NOT design monolithic, massive datastores (e.g., a single 10 TB volume). The AI MUST break datasets into smaller databases to ensure backup, restore, and rebuild times remain within acceptable Service Level Objectives (SLOs).
- When selecting RAID levels, the AI MUST specify RAID 1 or RAID 10 for single-disk failure tolerance, JBOD for distributed systems that handle redundancy at the software layer, and MUST explicitly warn against RAID 0 due to extreme vulnerability to data loss.

**Virtualization and Cloud Environments**
- When deploying databases on hypervisors/VMs, the AI MUST assume relaxed durability (hypervisors often ignore `fsync` calls for performance) and MUST treat data loss on single nodes as an inevitability.
- When sizing databases in virtualized environments, the AI MUST design for horizontal scaling and minimize concurrency per node, as hypervisors have lower concurrency boundaries than bare metal.
- When utilizing persistent block storage in the cloud, the AI MUST account for network dependency and plan for latency instability caused by network congestion.

**Containers**
- When evaluating containers (e.g., Docker) for database workloads, the AI MUST recommend them for rapid spin-up in test/development environments.
- When evaluating containers for production databases, the AI MUST warn against them if the workload is heavily I/O bound, requires kernel-level customizations, or is susceptible to network congestion on a shared OS/host model.

**Database as a Service (DBaaS)**
- When implementing a DBaaS platform (e.g., Amazon RDS), the AI MUST NOT treat it as a replacement for database expertise. The AI MUST enforce DBRE involvement in engine selection, data modeling, access frameworks, and security.
- When operating DBaaS, the AI MUST account for the lack of OS/network visibility by relying on database-native metrics (e.g., MySQL performance schema).
- When configuring DBaaS or any clustered database, the AI MUST ensure strict Network Time Protocol (NTP) synchronization across all nodes to prevent inexplicable replication lag.
- When adopting DBaaS, the AI MUST design a migration path and disaster recovery plan back to self-hosted/raw infrastructure to prevent vendor lock-in and retain ultimate control over data.

@Workflow
1.  **Platform & Architecture Selection**: Assess the deployment target (Bare Metal, VM, Container, or DBaaS). Apply the specific constraints for that target (e.g., horizontal scaling for VMs, visibility workarounds for DBaaS).
2.  **OS & Kernel Optimization**: Configure memory allocators (`jemalloc`/`tcmalloc`), disable/adjust SWAP behavior in tandem with OOM Killer settings, configure NUMA interleaving, disable THP defragmentation, and set appropriate resource limits.
3.  **Storage Subsystem Design**: Select the appropriate disk type (SSD/HDD), map the correct I/O scheduler (`noop` or `deadline`), align block sizes, implement `O_DIRECT`, and configure RAID/JBOD topologies based on MTTR requirements.
4.  **Network Tuning**: Isolate traffic streams and tune TCP/IP settings for high-concurrency connections.
5.  **Durability & Failover Validation**: Validate `fsync` behavior through the entire storage stack. Ensure that any relaxation of durability (e.g., disabling swap, ephemeral cloud storage) is strictly paired with tested, automated failover mechanisms.

@Examples (Do's and Don'ts)

- **[DO]**: Use `noop` as the I/O scheduler when the database is backed by an array of SSDs with an optimizing controller.
- **[DON'T]**: Use the default elevator algorithm (`cfq` or `anticipatory`) for database storage on SSDs, as it unnecessarily attempts to minimize seek times on media where seek times are stable.

- **[DO]**: Disable OS swap completely IF you have an automated, rapid failover mechanism, allowing the OOM Killer to cull the database instantly so traffic routes to a healthy replica.
- **[DON'T]**: Allow a database to swap heavily to disk to "stay alive," as the resulting latency spikes will violate SLOs and cause application-wide cascading failures.

- **[DO]**: Address NUMA imbalances by interleaving memory allocation, flushing the buffer cache before startup, and forcing the OS to allocate the database buffer pool immediately.
- **[DON'T]**: Allow the Linux kernel to assign memory to a single preferred NUMA node for a large database buffer pool, as this will result in localized memory exhaustion and swapping while the rest of the machine has free RAM.

- **[DO]**: Break a required 10 TB storage need into multiple smaller database instances or shards to ensure that backup and recovery processes can execute quickly.
- **[DON'T]**: Create a single 10 TB RAID 0 striped volume for a database, creating a massive single point of failure with an unacceptably long rebuild time.

- **[DO]**: Use `jemalloc` or `tcmalloc` as the memory allocation library for database binaries to reduce fragmentation.
- **[DON'T]**: Enable Transparent Huge Pages (THP) defragmentation on database hosts, as it will cause severe CPU thrashing.

- **[DO]**: Ensure precise NTP synchronization across all instances when using a DBaaS provider.
- **[DON'T]**: Rely blindly on the DBaaS provider's defaults without auditing time synchronization, as clock drift will cause severe replication lag and troubleshooting nightmares.