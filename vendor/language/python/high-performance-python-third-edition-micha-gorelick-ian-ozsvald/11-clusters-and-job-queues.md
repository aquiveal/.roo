# @Domain
Tasks involving the design, implementation, debugging, or deployment of distributed computing solutions, clustered Python applications, task queues, message brokers (Pub/Sub or Queues), IPython Parallel setups, or Docker containerization for horizontal scaling.

# @Vocabulary
*   **Cluster**: A collection of computers (nodes) working together to solve a common task, viewed externally as a single system.
*   **Beowulf Cluster**: A cluster of commodity PCs on a local area network used for clustered processing.
*   **Dynamic Scaling**: The practice of activating additional servers/nodes in response to increased demand at specific times.
*   **Message Broker**: A system (like RabbitMQ, Kafka, ActiveMQ, ZeroMQ) that facilitates communication between multiple actors via a message bus, decoupling message creators from consumers.
*   **Queue**: A buffer for messages used when there is an imbalance between data production and consumption, allowing horizontal scaling of data consumers.
*   **Pub/Sub (Publisher/Subscriber)**: A collection of queues where publishers push data to a topic, and all subscribers to that topic receive an identical copy.
*   **Consumer**: A logical grouping of tasks/processes that react to messages within a subscription group.
*   **IPython Parallel**: An extension of the IPython kernel for parallel computing consisting of Engines (synchronous Python interpreters), Controllers (work distributors/schedulers), and Hubs.
*   **ZeroMQ**: A low-level, high-performance messaging library used as middleware (powers IPython Parallel and Jupyter), providing no security by default.
*   **Technical Debt**: Stale or obsolete code/flags that, if left in a distributed system, can cause catastrophic financial or operational failures during upgrades (e.g., the Knight Capital incident).
*   **Hardware Virtualization**: Running software on "fake" hardware (e.g., VMware, VirtualBox), introducing resource overhead.
*   **OS-level Virtualization**: Running on the native hardware but a "fake" operating system (e.g., Docker via `cgroups`), resulting in near-zero CPU/memory performance degradation on Linux.
*   **Dead Man's Switch**: A monitoring backup that triggers an alert in the absence of an expected event.

# @Objectives
*   Ensure that single-machine vertical scaling and code optimizations (profiling, compiling, memory reduction) are fully exhausted before introducing the complexity of a cluster.
*   Prioritize system resilience, ease of debugging, and fault tolerance over raw execution speed in distributed environments.
*   Design clusters to handle network latency, hardware failures, and asynchronous data arrival gracefully.
*   Implement containerization (Docker) optimally to guarantee reproducible, easily deployable runtime environments without sacrificing build speed.

# @Guidelines

## Cluster Pre-requisites and Strategy
*   The AI MUST verify that the user has profiled their system, exploited compiler solutions (Numba/Cython), and maximized local multicore usage (multiprocessing/Joblib) before recommending a clustered solution.
*   The AI MUST advocate for a simple software architecture (e.g., independent Queues) over complex Interprocess Communication (IPC) across machines, unless latency control is the absolute highest priority (e.g., MPI).

## Resilience, Monitoring, and Failure Handling
*   The AI MUST design distributed systems with the assumption that machines will fail, networks will partition, and queues will back up.
*   The AI MUST recommend implementing deliberate failure testing (e.g., `kill -9`, dividing by zero, pulling power) on single-node setups to validate robustness before scaling up.
*   The AI MUST prioritize human-readable message formats (like JSON text) over low-level compressed binary protocols for message passing. Debugging a partially failed cluster is time-critical, and human-readable text saves engineering time during outages.
*   The AI MUST implement "Positive Reporting" (e.g., daily cluster health emails) and "Dead Man's Switches" alongside standard monitoring (e.g., Graphite, Ganglia, Pingdom) so that the *absence* of a signal triggers an alert.
*   The AI MUST ensure there is a documented, tested "Cold Restart Plan" for the cluster to avoid extended downtime when all systems fail simultaneously.

## Safe Deployments and Upgrades
*   To prevent catastrophic deployment failures (referencing the $462M Knight Capital loss), the AI MUST explicitly remove obsolete code/feature flags rather than repurposing them.
*   The AI MUST mandate automated, reproducible deployment environments using system images (AMI, .deb, .rpm) or configuration management (Docker, Ansible, Salt, Puppet).
*   The AI MUST recommend heterogeneous software environments (different OS versions/platforms) where applicable to prevent network-wide crashes triggered by a single client bug (referencing the Skype 24-hour outage).

## Message Brokering (Queues and Pub/Sub)
*   The AI MUST use a **Queue** when there is an imbalance between message production and consumption, allowing tasks to buffer until a worker is available.
*   The AI MUST use a **Pub/Sub** architecture when a single event needs to trigger multiple disparate transformations or be consumed by decoupled systems.
*   When configuring message brokers, the AI MUST explicitly address and define:
    *   Message delivery guarantees (at-least-once, at-most-once).
    *   Consumer acknowledgment requirements (what happens if a consumer dies mid-processing).
    *   Message expiration policies.
    *   Queue overflow behavior (what happens when memory runs out).

## IPython Parallel (For Research/Ad-Hoc Clusters)
*   The AI MUST use the `sync_imports()` context manager or the `@require` decorator to ensure that modules imported locally are also imported on remote engines.
*   The AI MUST use `push()` to send data/variables to the global namespace of remote engines and `pull()` to retrieve them.
*   The AI MUST warn that underlying ZeroMQ instances lack built-in security, requiring SSH tunneling if used outside a trusted local network.

## Docker Optimization
*   The AI MUST leverage Docker's build cache by copying dependency files (e.g., `COPY requirements.txt .`) and running installations (`RUN pip install`) *BEFORE* copying the rest of the application code (`COPY . .`).
*   The AI MUST utilize a `.dockerignore` file to prevent large, unnecessary files in the build context from slowing down the `docker build` process.
*   The AI MUST format the `CMD` instruction as a JSON array (e.g., `CMD ["python", "./script.py"]`) to ensure system signals (like `SIGINT` or `SIGKILL`) are handled correctly.
*   The AI MUST tag images with both a descriptive version tag and the `latest` tag for registry sharing.

# @Workflow
When tasked with designing or implementing a clustered or queued architecture, the AI MUST follow this exact sequence:
1.  **Justification Check**: Confirm with the user that single-machine optimizations (compilation, multiprocessing, memory reduction) have been exhausted or that dynamic scaling/reliability explicitly requires a cluster.
2.  **Architecture Selection**: Select the appropriate broker pattern. Use Queues for workload distribution and load balancing; use Pub/Sub for data fan-out. Use IPython Parallel strictly for interactive research environments.
3.  **Single-Node Prototyping**: Implement the job server and exactly one job processor on a single machine.
4.  **Resilience Testing**: Inject artificial faults (exceptions, crashes) into the single-node prototype to verify that the queue retains messages and the processor recovers.
5.  **Horizontal Scaling**: Add a second job processor on the same machine, verify 2x speedup. Then, introduce a secondary machine to test network latency and state synchronization.
6.  **Containerization**: Wrap the verified worker/server in a Dockerfile, strictly separating the `requirements.txt` copy/install steps from the source code copy step to maximize caching.
7.  **Monitoring & Documentation**: Output instructions for positive reporting monitors and draft a step-by-step cold-restart procedure for the cluster.

# @Examples (Do's and Don'ts)

## Message Serialization
*   **[DO]** Use human-readable text for message payloads to ensure rapid debugging during a crisis.
    ```python
    import json
    # DO: Easy to inspect if a queue stalls
    payload = json.dumps({"task_id": 105, "action": "resize", "user": "admin"})
    queue.put(payload)
    ```
*   **[DON'T]** Use low-level compressed binary protocols for task queues unless strictly bounded by network I/O, as it obscures data during emergency recovery.

## Docker Build Caching
*   **[DO]** Copy requirements and install them before copying the rest of the codebase to utilize Docker layer caching.
    ```dockerfile
    FROM python:3.12-slim
    WORKDIR /usr/src/app
    # DO: Copy requirements first to cache the pip install step
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    # Copy the rest of the code only after dependencies are installed
    COPY . .
    CMD ["python", "./worker.py"]
    ```
*   **[DON'T]** Copy the entire directory before installing dependencies, which invalidates the cache every time a line of source code changes.
    ```dockerfile
    FROM python:3.12-slim
    WORKDIR /usr/src/app
    # DON'T: This ruins layer caching if any file in the repo changes
    COPY . .
    RUN pip install -r requirements.txt
    ```

## IPython Parallel Imports
*   **[DO]** Ensure remote engines have the required modules imported using `sync_imports()`.
    ```python
    import ipyparallel as ipp
    c = ipp.Client()
    dview = c[:]
    # DO: Sync imports across all remote engines
    with dview.sync_imports():
        import os
    dview.apply_sync(lambda: os.getpid())
    ```
*   **[DON'T]** Assume that because a module is imported in the local script, the remote IPython engine knows about it.

## Feature Flags and Upgrades
*   **[DO]** Completely remove obsolete feature flags and code paths from the codebase before upgrading cluster software.
*   **[DON'T]** Repurpose an old, unused feature flag for a new feature (this directly caused Knight Capital's $462M loss due to a single un-upgraded machine executing the old, stale code path).