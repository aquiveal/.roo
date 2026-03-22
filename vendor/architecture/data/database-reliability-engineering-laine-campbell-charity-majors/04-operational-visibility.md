# @Domain
These rules MUST trigger when the AI is tasked with designing, implementing, configuring, reviewing, or debugging operational visibility (OpViz), monitoring, logging, alerting, telemetry, distributed tracing, or performance metric collection for database systems, their host infrastructures, and the applications that interact with them.

# @Vocabulary
- **Operational Visibility (OpViz)**: The awareness of the working characteristics of a database service achieved through the regular measuring, collection, and analysis of data points across all system components.
- **Business Intelligence (BI) Platform**: The operational paradigm for OpViz. OpViz must be treated as a BI platform answering business/SLO questions, not just an IT collection utility.
- **Whitebox Monitoring**: Gathering real metrics by instrumenting the internals of the application and datastore (e.g., tracing a user flow).
- **Blackbox Monitoring**: Simulating a user by sending synthetic requests from the outside; primarily used for low-traffic periods or external edge validation.
- **Metric**: The measurement of a property observed periodically over a time-series. Stored as Counters, Gauges, Histograms, or Summaries.
- **Counter**: A cumulative metric representing the number of times a specific occurrence has happened.
- **Gauge**: A metric representing a current value that can fluctuate up or down (e.g., active locks, queue size).
- **Histogram**: Events broken into configured buckets to visualize the distribution of metrics (especially latency).
- **Summary**: Similar to histograms but focused on proving counts over sliding windows of time.
- **Event**: A discrete action occurring in the environment (e.g., code deployments, failovers, configuration changes).
- **Alert**: A human interrupt. Must ONLY be triggered when SLOs are in imminent danger of violation.
- **Ticket/Task**: Generated output for work that must be done but does not constitute an imminent disaster.
- **Notification**: Informational output sent to chat rooms/wikis to provide context without interrupting workflow.
- **Minimum Viable Monitoring Set (MVMS)**: The foundational monitoring requirements for a system: "Is the data safe?", "Is the service up?", and "Are the consumers in pain?".
- **USE Method**: Monitoring methodology focusing on Utilization, Saturation, and Errors for all system resources.
- **Steal Time**: CPU time a virtual machine spends waiting for a physical CPU (an indicator of a "noisy neighbor" in cloud environments).

# @Objectives
- Treat the OpViz stack as a mission-critical Business Intelligence (BI) system designed to answer "How is this impacting SLOs?" and "How is it broken, and why?".
- Shift monitoring aggregation away from static, individual hostnames toward dynamic, role-based aggregations (e.g., monitor the "master" role rather than `DB01`).
- Prevent data loss in metrics by capturing and storing high-resolution distributions and raw values rather than lossy averages.
- Reduce the signal-to-noise ratio by ruthlessly restricting human alerts to actual SLO-threatening events.
- Implement comprehensive end-to-end visibility stretching from the application codebase down to datastore disk flushes.

# @Guidelines

## Architecture and Data Storage Rules
- The AI MUST configure monitoring systems to store metrics based on architectural *roles* (e.g., "primary-writer", "read-replica") rather than ephemeral hostnames or IPs.
- The AI MUST define high-resolution sampling (1-second or lower) exclusively for metrics that exhibit high variability and directly impact SLOs (e.g., latency, CPU saturation, connection queues).
- The AI MUST define low-resolution sampling (1-minute or higher) for slow-moving metrics (e.g., overall disk capacity) to conserve monitoring resources.
- The AI MUST NEVER configure monitoring systems to store ONLY aggregated averages for latency; it MUST ensure the storage of actual values or histograms to allow visualization of distributions and outliers/long tails.
- The AI MUST restrict the monitoring architecture to a maximum of FIVE different sampling rates to maintain system simplicity.
- The AI MUST focus initial metric collection strictly on the critical path SLIs: Latency, Availability, Call Rates, and Utilization.

## Data Ingestion Rules
- The AI MUST prioritize Whitebox monitoring (instrumentation of application and DB internals) over Blackbox monitoring.
- When configuring Blackbox testing for latency/saturation, the AI MUST incorporate queueing theory using traffic volume to deduce system saturation.
- The AI MUST configure systems to log deployments, infrastructure changes, and database schema changes as discrete "Events" in the OpViz stack to allow correlation with performance spikes.

## Alerting and Data Output Rules
- The AI MUST restrict the generation of "Alerts" (human interrupts/pages) strictly to conditions where an SLO is in imminent danger of being violated.
- For threshold breaches that require action but do not threaten an SLO, the AI MUST configure the system to generate a "Ticket/Task" instead of an alert.
- For contextual changes (e.g., code deployments, config updates), the AI MUST configure the system to generate a "Notification" (e.g., to a Slack channel) rather than an alert or ticket.

## Bootstrapping MVMS Rules
- When initializing monitoring for a new or unmonitored service, the AI MUST implement the Minimum Viable Monitoring Set (MVMS) before adding any granular metrics.
- To monitor "Is the data safe?", the AI MUST implement checks for: minimum of 3 live copies of data (if mission-critical), replication thread status, replication lag thresholds, and backup/restore success validation.
- To monitor "Is the service up?", the AI MUST implement end-to-end checks that fetch objects across all partitions/shards.
- The AI MUST NOT use complex database queries for simple load balancer aliveness checks. Load balancer checks must be completely isolated from DB resource consumption to prevent health-checking the database to death.
- The AI MUST configure off-premises/off-site health checks to monitor the primary monitoring service itself.

## Instrumentation Layers Rules
- **Application Layer**: 
  - The AI MUST ensure all external service calls (databases, search indexes, caches) are wrapped in distributed tracing (e.g., Zipkin/New Relic).
  - The AI MUST inject the codebase location (class/method/function) into SQL comments so database query logs map directly back to the application code.
- **Server/Instance Layer**: 
  - The AI MUST apply the USE method (Utilization, Saturation, Errors) aggregated across the pool of hosts performing a specific function.
  - The AI MUST include monitoring for `steal time` in virtualized/cloud environments to detect noisy neighbors.
  - The AI MUST monitor OS-level limits, including kernel mutexes, file descriptors, and task capacity.
- **Datastore Connection Layer**:
  - The AI MUST monitor connection upper bounds, active counts, and thread pool utilization.
  - The AI MUST monitor TCP connection backlogs and wait timeouts to identify saturation.
- **Internal Datastore Visibility**:
  - The AI MUST monitor background operations that impact latency: dirty buffers, checkpoint age, compaction tasks, and page evictions.
  - The AI MUST monitor replication for three fault states: lag/latency, broken threads, and replication drift (silent data divergence).
  - The AI MUST monitor memory structure hit ratios, churn, and concurrency serialization (mutexes/semaphores waits).
  - The AI MUST monitor the time spent waiting on locks, deadlocks, and rollbacks.

# @Workflow
When tasked with designing or implementing an Operational Visibility framework for a database system, the AI MUST follow this algorithmic process:

1. **SLO Alignment**: Identify the explicit Latency, Availability, and Throughput SLOs of the target system.
2. **Implement MVMS**:
   - Create automated validation for Data Safety (backup completion, replication health, minimum node counts).
   - Create Top-Level Health Checks (end-to-end partition reads).
   - Create Load Balancer Health Checks (simple, non-DB-intensive).
   - Create Customer Pain Checks (top-level error rates and latency).
3. **Application Instrumentation**:
   - Inject tracing contexts into all persistence calls.
   - Embed SQL comments indicating the origin file/function of the query.
4. **Infrastructure & Datastore Instrumentation**:
   - Configure Role-based grouping for all hosts (e.g., collect USE metrics for the role `app-db-replica`, not `host-123`).
   - Implement <1s high-resolution sampling for CPU queues, DB connection queues, and lock waits.
   - Implement low-resolution sampling for disk space and table sizes.
   - Enable internal DB metric collection (compaction/flush metrics, buffer hit rates, mutex spin waits).
5. **Output Routing**:
   - Map metric breaches that threaten the SLOs directly to the **Alerting** pipeline (PagerDuty/On-call).
   - Map non-imminent warnings to the **Ticketing** pipeline (Jira/GitHub issues).
   - Map state changes (deployments, config changes) to the **Notification** pipeline (Chatops).
6. **Data Retention Configuration**: Ensure latency metrics are stored as Histograms/raw distributions to prevent spike erosion caused by averaging.

# @Examples (Do's and Don'ts)

### Role-Based Aggregation
- [DO]: `SELECT avg(cpu_usage) FROM metrics WHERE role = 'payment-db-replica' GROUP BY time(1m)`
- [DON'T]: `SELECT avg(cpu_usage) FROM metrics WHERE hostname IN ('db-01', 'db-02', 'db-03') GROUP BY time(1m)`

### Latency Distributions
- [DO]: Store latency requests in buckets/histograms (e.g., `latency_bucket{le="0.05"}`, `latency_bucket{le="0.1"}`) to accurately visualize the 99th percentile and long-tail outliers.
- [DON'T]: Aggregate latency into a single 1-minute `average_response_time` metric, which hides critical micro-spikes and completely erodes the visibility of customer pain.

### Health Checks
- [DO]: Configure the load balancer to hit a static `/health` endpoint that returns `200 OK` from the application memory without touching the database connection pool.
- [DON'T]: Configure the load balancer health check to execute `SELECT 1 FROM users LIMIT 1;` every 5 seconds per proxy server, which will overwhelm the database as proxy servers scale up.

### Alerting Fatigue
- [DO]: Create a Pager alert: "5% of user requests to the API are experiencing latency > 100ms over a 3-minute window (Imminent SLO violation)."
- [DON'T]: Create a Pager alert: "CPU utilization on database replica 4 spiked to 90% for 30 seconds." (This should be silently handled by autoscaling or logged for capacity planning, not an alert).

### Application-to-DB Traceability
- [DO]: Inject code location into queries: `SELECT /* File: user_auth.py, Method: validate_login */ id, hash FROM users WHERE email = ?;`
- [DON'T]: Send opaque dynamic queries from an ORM without any meta-context, forcing the DBRE to manually search the entire codebase to find the source of an expensive query.