@Domain
These rules MUST be triggered whenever the AI is tasked with designing system architecture, evaluating or implementing performance metrics, defining Service Level Objectives (SLOs) or Service Level Agreements (SLAs), planning system capacity and scalability, designing fault-tolerance mechanisms, writing system incident reports, or defining nonfunctional requirements for a software application.

@Vocabulary
- **Nonfunctional Requirements**: System properties including performance, reliability, security, compliance, and maintainability, distinct from functional features.
- **Response Time**: The elapsed time from when a client makes a request to when they receive the response (includes network latency, queueing, and service time).
- **Service Time**: The exact duration a server is actively processing a request.
- **Latency**: The time a request is waiting (latent) and not being actively processed, including network delay and queueing.
- **Queueing Delay**: Time spent waiting for CPU or resources before processing begins.
- **Head-of-line Blocking**: When a small number of slow requests hold up the processing of subsequent faster requests.
- **Percentiles (p50, p95, p99, p999)**: Metrics used to define the distribution of response times. p50 is the median; higher percentiles represent the slowest outlier requests (tail latencies).
- **Tail Latency Amplification**: The effect where a single end-user request requires multiple backend calls, making the overall request slow even if only one backend call hits a high percentile delay.
- **SLO (Service Level Objective)**: A target performance metric (e.g., p99 response time < 1s).
- **SLA (Service Level Agreement)**: A contract defining penalties if an SLO is not met.
- **Throughput**: The number of requests per second or data volume per second a system can process.
- **Metastable Failure**: A vicious cycle where an overloaded system becomes less efficient and cannot recover even when load is reduced.
- **Retry Storm**: When increased response times cause clients to time out and retry, further overloading the system.
- **Fan-out**: The factor by which one initial request results in multiple downstream requests or writes (e.g., delivering a post to all followers).
- **Materialization**: Precomputing and updating query results (e.g., a timeline cache) to optimize read performance.
- **Fault**: A specific part of a system stopping working correctly (e.g., a disk failure, network drop).
- **Failure**: The entire system stopping providing the required service to the user (i.e., missing the SLO).
- **Fault Tolerance**: The ability of a system to prevent faults from escalating into failures.
- **SPOF (Single Point of Failure)**: A component whose fault inevitably causes a system failure.
- **Chaos Engineering / Fault Injection**: Deliberately triggering faults in a system to test and increase confidence in fault-tolerance machinery.
- **Rolling Upgrade**: Upgrading a multi-node system one node at a time without downtime.
- **Cascading Failure**: A problem in one component causing another to overload, bringing down successive components.
- **Blameless Postmortem**: An incident investigation culture focusing on systemic and sociotechnical flaws rather than punishing individuals.
- **Scalability**: A system's ability to cope with increased load by adding computing resources.
- **Load Parameters**: Metrics defining the current load on a system (e.g., requests/sec, read/write ratio, concurrent users).
- **Shared-Memory Architecture (Scale Up)**: Increasing resources (CPU, RAM) on a single machine.
- **Shared-Disk Architecture**: Multiple CPUs/RAM accessing a shared storage array via a fast network (NAS/SAN).
- **Shared-Nothing Architecture (Scale Out / Horizontal Scaling)**: A distributed system of independent nodes, coordinating via a conventional network.
- **Maintainability**: The ease of keeping a system running, adapting it, and fixing it over time.
- **Operability**: Making a system easy for operations teams to keep running smoothly (observability, automation, good defaults).
- **Simplicity**: Managing complexity through abstraction and avoiding "big ball of mud" architectures.
- **Evolvability (Agility)**: Making it easy for engineers to make changes and minimizing irreversible decisions.

@Objectives
- Explicitly define and address nonfunctional requirements (performance, reliability, scalability, maintainability) in all architectural designs.
- Prevent component faults from escalating into system-wide failures through redundancy, isolation, and controlled degradation.
- Measure and describe performance accurately using percentiles and distribution models, completely avoiding arithmetic means for user experience metrics.
- Design systems that scale horizontally by breaking tasks down into independent, decoupled components.
- Prioritize maintainability by designing for operability (easy monitoring and deployment), simplicity (strong abstractions), and evolvability (reversible decisions).

@Guidelines
- **Describing Performance**:
  - The AI MUST describe typical performance using the median (p50) and outlier performance using higher percentiles (p95, p99, p999).
  - The AI MUST NOT use the arithmetic mean (average) to describe typical user response times, as it masks outliers.
  - The AI MUST differentiate between "Latency" (waiting time) and "Service Time" (processing time).
  - The AI MUST aggregate percentiles correctly by adding histograms, NEVER by averaging percentiles.
- **Handling Load and Overload**:
  - When designing request workflows, the AI MUST implement protections against retry storms.
  - The AI MUST mandate client-side protections: exponential backoff with jitter and circuit breakers.
  - The AI MUST mandate server-side protections: load shedding and backpressure mechanisms.
- **Architecting for Fan-out**:
  - When designing high-read systems (like social feeds), the AI MUST evaluate materialization (precomputing views/caches) over expensive on-the-fly multi-way joins.
  - The AI MUST separate normal users from "celebrity" nodes (outliers with massive fan-out) to prevent bottlenecks during materialization processes.
- **Reliability and Faults**:
  - The AI MUST design systems to be fault-tolerant, expecting hardware and software faults as a normal operating condition.
  - The AI MUST eliminate Single Points of Failure (SPOFs) through redundancy (e.g., multi-zone replication, RAID, software-level failover).
  - The AI MUST prefer rolling upgrades over planned downtime, designing state and data schemas to support mixed-version deployments.
  - When diagnosing outages, the AI MUST NOT conclude with "human error." The AI MUST analyze the sociotechnical system, identifying systemic lack of safeguards, bad interfaces, or misaligned priorities (Blameless Postmortem approach).
- **Scalability**:
  - The AI MUST NOT state "System X is scalable" without defining specific load parameters (e.g., active users, read/write ratio, data volume).
  - The AI MUST design scalability in orders of magnitude; architectures should be re-evaluated when load increases by 10x.
  - The AI MUST default to shared-nothing (horizontal scaling) architectures for high-scale needs, utilizing explicit sharding or microservices.
  - The AI MUST explicitly reject "magic scaling sauce" generalizations; scalability solutions must be uniquely tailored to the application's specific load parameters.
- **Maintainability**:
  - The AI MUST enforce Operability by ensuring systems have high observability, expose health metrics, behave predictably, and allow manual overrides of automated processes.
  - The AI MUST enforce Simplicity by aggressively abstracting implementation details and minimizing accidental complexity.
  - The AI MUST enforce Evolvability by decoupling services, avoiding rigid schemas where inappropriate, and minimizing irreversible architectural choices.

@Workflow
1. **Identify Nonfunctional Categories**: Explicitly separate requirements into Performance, Reliability, Scalability, and Maintainability.
2. **Define Load Parameters**: Identify the specific metrics that characterize the system's workload (e.g., 10k requests/sec, 100:1 read/write ratio, 50GB new data/day).
3. **Establish Performance Metrics**: Define SLOs using percentiles (e.g., p50 < 200ms, p99 < 1s). Account for tail latency amplification in microservices.
4. **Determine Fault Tolerance**: Identify potential faults (disk failure, node crash, network split, rogue process). Map out redundancy, circuit breakers, and isolation strategies to prevent these from becoming failures.
5. **Formulate Scalability Strategy**: Choose between vertical scaling (for simplicity at low scale) and horizontal/shared-nothing scaling (for high scale). Determine if read-scaling (caches/materialization) or write-scaling (sharding) is required.
6. **Design for Maintainability**: Specify the abstractions to be used, the telemetry/observability required for operations, and the deployment strategies (e.g., rolling upgrades) to ensure evolvability.

@Examples (Do's and Don'ts)

**Performance Metrics**
- [DO]: "The service must maintain a p50 response time of <100ms and a p99 response time of <500ms under a load of 5,000 requests per second."
- [DON'T]: "The service should have an average response time of 150ms." (Averages hide terrible experiences for tail-end users).

**Handling Overload and Retries**
- [DO]: "Clients will implement exponential backoff with jitter for retries, and the server will utilize a token bucket rate limiter to shed load when nearing metastable failure."
- [DON'T]: "If the request fails or times out, the client should immediately retry in a tight loop." (This creates a retry storm and metastable failure).

**Social Feed / High-Read Data Architecture**
- [DO]: "Use a push-based materialized view for standard users to compute home timelines on write. For celebrity accounts with >100k followers, use a pull-based merge-on-read approach to avoid massive fan-out latency."
- [DON'T]: "Run a SQL query with a JOIN across the users, follows, and posts tables every time a user refreshes their timeline." (This will collapse under high read load).

**Incident Reporting (Postmortems)**
- [DO]: "The incident was triggered when an operator deployed a configuration change. The root cause is that the deployment tooling lacks automated syntax validation and phased rollouts, allowing a malformed config to instantly propagate globally."
- [DON'T]: "The system went down because Bob made a typo in the config file. Bob has been reprimanded and told to be more careful." (Blaming human error ignores the sociotechnical system flaws).

**Scalability Terminology**
- [DO]: "To accommodate a 10x growth in active users, we will adopt a shared-nothing architecture, sharding the user database by `tenant_id` across multiple commodity nodes."
- [DON'T]: "We will use a NoSQL database because it is inherently scalable." (Scalability requires defining the specific load parameter and architecture, not just a database label).