# @Domain
This rule file activates when the AI is tasked with designing system architectures, defining nonfunctional requirements (NFRs), reviewing system performance metrics, implementing network request logic (retries, timeouts), writing incident postmortems, or evaluating the scalability, reliability, and maintainability of data-intensive backends.

# @Vocabulary
- **Functional Requirements**: What the application must do (features, screens, operations).
- **Nonfunctional Requirements**: System qualities such as performance, reliability, security, scalability, and maintainability.
- **Fan-out**: The factor by which a single initial request multiplies into several downstream requests (e.g., delivering one social media post to millions of followers).
- **Materialization (Materialized View)**: The process of precomputing and storing the results of a query (e.g., a home timeline) to serve future reads quickly from a cache rather than recomputing them.
- **Throughput**: The number of requests per second, or data volume per second, a system processes.
- **Response Time**: The elapsed time a client sees from making a request to receiving the answer (includes network and queueing delays).
- **Service Time**: The duration the server actually spends processing a request (excludes queueing and network delays).
- **Latency**: The duration a request spends latent (waiting to be handled) without being actively processed.
- **Head-of-line Blocking**: A performance issue where a small number of slow requests hold up the processing of subsequent, faster requests.
- **Tail Latency Amplification**: A phenomenon where a single slow backend call slows down an entire end-user request that relies on multiple parallel backend calls.
- **Metastable Failure**: A vicious cycle where an overloaded system worsens its own state (e.g., through retry storms) and cannot recover even when original load drops.
- **Fault**: A particular component of a system stopping working correctly (e.g., a disk crash).
- **Failure**: The system as a whole stops providing the required service to the user (failing its SLO).
- **Single Point of Failure (SPOF)**: A component whose individual fault escalates to cause a system-wide failure.
- **Chaos Engineering / Fault Injection**: Deliberately triggering faults in a system to continuously test and validate fault-tolerance mechanisms.
- **Shared-Nothing Architecture**: Horizontal scaling (scaling out) using multiple independent nodes, coordinating at the software level.
- **Operability**: The ease with which an operations team can keep a system running smoothly (via telemetry, predictability, and automation).
- **Simplicity**: Managing complexity by using clean abstractions to hide implementation details and avoid "big balls of mud".
- **Evolvability**: Designing systems to easily accommodate future changes, primarily by minimizing irreversible actions.

# @Objectives
- Evaluate and enforce strict, percentile-based performance measurement standards.
- Design resilient architectures that gracefully degrade under load using backpressure, load shedding, and smart retry strategies.
- Architect scalable systems that separate read and write paths optimally (e.g., using materialization and controlling fan-out).
- Cultivate system reliability through redundancy, decoupling of software faults, and blameless sociotechnical evaluations.
- Ensure systems are maintainable by prioritizing operability, leveraging strong abstractions for simplicity, and avoiding irreversible architectural decisions.

# @Guidelines

### Performance and Metrics
- The AI MUST NEVER use or recommend the arithmetic mean (average) to describe typical system response times.
- The AI MUST utilize percentiles (p50/median for typical load; p95, p99, p999 for outliers and tail latencies) when defining Service Level Objectives (SLOs) or analyzing response times.
- When aggregating response time data across multiple nodes or time windows, the AI MUST NOT average percentiles. It MUST specify adding the raw histograms together.
- The AI MUST advocate for client-side measurement of response times, as server-side metrics fail to capture network and queueing delays.

### Architecture and Scalability
- When designing timeline, feed, or notification systems, the AI MUST explicitly calculate the **fan-out** factor.
- For high fan-out scenarios, the AI MUST recommend **materialized views** (precomputing data on write) rather than executing expensive join queries on read.
- The AI MUST handle extreme fan-out outliers (e.g., "celebrity" accounts) as architectural exceptions: storing their data separately and merging it at read-time to prevent write-path overload.
- The AI MUST strongly warn against premature optimization for scale; it MUST propose architectures designed to handle current load plus exactly one order of magnitude of growth.
- The AI MUST prefer **Shared-Nothing (scale-out)** architectures over Shared-Memory or Shared-Disk setups for distributed systems requiring high horizontal scalability.

### Network Resiliency and Overload Prevention
- When implementing HTTP clients, RPCs, or inter-service communication, the AI MUST mandate the use of **exponential backoff** and **randomized jitter** for retries.
- The AI MUST implement or recommend **circuit breakers** or **token buckets** to halt requests to failing downstream services and prevent retry storms.
- To prevent metastable failures on the server side, the AI MUST require the implementation of **load shedding** (proactively rejecting requests when near capacity limit) and **backpressure** (signaling clients to slow down).

### Reliability and Fault Tolerance
- The AI MUST clearly distinguish between "faults" (component level) and "failures" (system level) in documentation and design.
- The AI MUST identify and eliminate Single Points of Failure (SPOFs) by mandating redundancy at the hardware, zone, and data levels.
- The AI MUST recommend the practice of **Chaos Engineering** (deliberate fault injection) to continuously exercise and validate fault-tolerance mechanisms.
- The AI MUST design stateful systems to support **rolling upgrades** (restarting one node at a time) to prevent downtime during patching.

### Maintainability and Human Factors
- When drafting post-incident reports or analyzing outages, the AI MUST NOT cite "human error" as the root cause. It MUST conduct a **blameless postmortem** focusing on the sociotechnical system, emergent behaviors, and interface design flaws.
- The AI MUST ensure **Operability** by mandating built-in observability (OpenTelemetry, tracing), health checks, predictable default behaviors, and safe rollback mechanisms.
- The AI MUST prioritize **Simplicity** by hiding complex, low-level implementations behind clean, generalized abstractions.
- To ensure **Evolvability**, the AI MUST actively identify and advise against technically irreversible decisions that lock the architecture into rigid patterns.

# @Workflow
When tasked with designing a system, defining NFRs, or reviewing backend architecture, the AI MUST follow this rigid algorithm:

1. **Quantify the Load (Scalability Assessment)**
   - Define exact throughput metrics (requests/sec, data volume/sec).
   - Identify the statistical distribution of the load (e.g., read/write ratios, peak concurrent users).
   - Check for heavy skew or extreme outliers (e.g., celebrity fan-out).
2. **Define the Measurement Standard (Performance Assessment)**
   - Establish p50, p95, and p99 response time targets based on client-side observation.
   - Select appropriate histogram/sketching algorithms (e.g., t-digest, DDSketch) for metric aggregation.
3. **Map the Data Flow (Architectural Assessment)**
   - Determine if the read path requires materialization to meet latency targets.
   - Implement hybrid materialization if fan-out skew exists (write-heavy for normal users, read-heavy for outliers).
4. **Harden the Boundaries (Resiliency Assessment)**
   - Audit all network boundaries. Inject exponential backoff, jitter, circuit breakers, and load shedding.
   - Identify SPOFs and enforce redundancy schemas.
5. **Evaluate the Lifecycle (Maintainability Assessment)**
   - Verify that the system allows rolling upgrades.
   - Confirm telemetry, logging, and tracing are integrated (Operability).
   - Validate that components are isolated via clean abstractions (Simplicity).

# @Examples (Do's and Don'ts)

### 1. Performance Measurement
- **[DO]**: "The service must maintain a p50 response time of < 200ms and a p99 response time of < 1s, measured at the client. Aggregate metrics across nodes by merging the t-digest histograms."
- **[DON'T]**: "The service must maintain an average (mean) response time of 300ms. To get the global average, we will average the percentiles from all servers."

### 2. Handling System Overload
- **[DO]**:
  ```python
  import random
  import time

  def make_request_with_retry(attempt=1, max_attempts=5):
      try:
          return http_client.get("/resource")
      except ServiceUnavailableError:
          if attempt >= max_attempts:
              raise
          # Exponential backoff with random jitter
          sleep_time = (2 ** attempt) + random.uniform(0, 1)
          time.sleep(sleep_time)
          return make_request_with_retry(attempt + 1, max_attempts)
  ```
- **[DON'T]**:
  ```python
  def make_request_with_retry(attempt=1, max_attempts=5):
      try:
          return http_client.get("/resource")
      except ServiceUnavailableError:
          if attempt >= max_attempts:
              raise
          # Naive retry storm generator
          return make_request_with_retry(attempt + 1, max_attempts)
  ```

### 3. Architecture for High Fan-Out (Social Timelines)
- **[DO]**: "For standard users, precompute home timelines by fanning out writes to followers' cache boxes (Materialized Views). For celebrity users (>100k followers), bypass write fan-out; instead, merge their posts into the follower's timeline dynamically at read time."
- **[DON'T]**: "Execute a SQL `JOIN` on the `posts` and `follows` tables every time a user refreshes their timeline, regardless of the user's follower count."

### 4. Incident Reporting
- **[DO]**: "The outage occurred because the deployment interface allowed a malformed configuration to be applied without validation. The sociotechnical system lacked safety guards for this specific operation. Action items: implement configuration syntax validation and automated fast-rollbacks."
- **[DON'T]**: "The outage occurred because Bob made a human error and deployed the wrong configuration file. Action items: tell Bob to be more careful next time."

### 5. Architecture Selection
- **[DO]**: "Since our current load is 500 requests per second and easily fits on a single machine, we will utilize a simple single-node PostgreSQL database to minimize accidental complexity. We will rethink the architecture if load approaches 5,000 requests per second."
- **[DON'T]**: "We expect to be the next Twitter, so we must immediately implement a massively distributed, microservices-based shared-nothing architecture using Kubernetes and a sharded NoSQL database, even though we only have 100 users."