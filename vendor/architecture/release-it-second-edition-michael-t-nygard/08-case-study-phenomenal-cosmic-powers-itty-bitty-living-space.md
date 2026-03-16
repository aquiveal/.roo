@Domain
Triggered when the AI is tasked with diagnosing production outages (specifically application hangs, high-latency, or low-CPU scenarios), configuring resource/connection pools, designing external integration points, writing system telemetry/monitoring scripts, or architecting incident remediation and dynamic configuration mechanisms.

@Vocabulary
- **Synthetic Transactions (e.g., SiteScope)**: Automated requests that simulate real customer behavior from the outside in to verify end-to-end site health and availability.
- **Request-Handling Instances (DRPs)**: Application server instances dedicated exclusively to serving user page requests or API calls.
- **Rolling Restart**: A mitigation strategy involving sequentially shutting down and rebooting servers across a cluster. Considered a slow, anti-pattern approach during acute crises compared to component-level restarts.
- **Thread Dump**: A complete snapshot of the state of all threads in a Java/application process, critical for identifying blocked threads, infinite waits, and resource exhaustion.
- **Lagging Indicator**: A metric, such as response time (page latency), that can only be calculated *after* a request completes. (If requests time out infinitely, the measured average latency may falsely appear healthy because failed requests are not averaged in).
- **Unbalanced Capacities**: A severe architectural mismatch where an upstream system can generate vastly more concurrent requests (e.g., 3,000 threads) than a downstream integration point can handle (e.g., 25 threads).
- **Recovery-Oriented Computing (ROC)**: An architectural philosophy that assumes failures are inevitable and prioritizes rapid, component-level recovery and survivability over attempting to build perfectly failure-proof systems.
- **Component-Level Restart**: The act of stopping and starting a specific internal application service or resource pool dynamically, without bringing down the entire host or application process.

@Objectives
- Diagnose catastrophic system hangs rapidly by correlating low system utilization (CPU) with high request concurrency and infinite latency.
- Prevent cascading failures by strictly enforcing timeouts and structurally segregating resource pools based on their specific downstream targets.
- Achieve sub-minute incident mitigation by designing components to be dynamically reconfigurable and restartable in isolation.
- Protect downstream bottlenecks by implementing upstream throttling and ensuring the user experience degrades gracefully when external integrations fail.
- Automate cluster-wide telemetry gathering and remediation actions via scriptable interfaces to eliminate reliance on slow, manual GUI operations.

@Guidelines
- **Diagnostic Rules:**
  - When observing a system state with high traffic, high latency (or timeouts), and abnormally **low CPU usage**, the AI MUST immediately suspect thread exhaustion caused by threads blocking on a downstream resource.
  - The AI MUST NOT rely solely on average response time metrics during an outage, as they are lagging indicators that ignore infinitely hanging requests.
  - The AI MUST utilize thread dumps across multiple tiers to trace the chain of failure. If front-end threads are blocked, the AI MUST check the middle-tier; if middle-tier threads are blocked, the AI MUST trace them to the external integration point.
- **Architectural Rules:**
  - The AI MUST NEVER configure a connection pool, socket, or resource pool without a strict, finite timeout. Infinite waits are strictly forbidden.
  - The AI MUST segregate connection pools by their specific destination service. Utilizing a single, shared connection pool for multiple distinct external integrations is forbidden.
  - The AI MUST architect systems according to Recovery-Oriented Computing (ROC) principles: components MUST expose lifecycle hooks (e.g., `stopService()`, `startService()`) and support dynamic property reloading (e.g., pool `max` size) without requiring a full JVM/process restart.
- **Remediation & Operations Rules:**
  - When a downstream system is overwhelmed (Unbalanced Capacities), the AI MUST throttle or completely disable the integration point at the upstream caller (e.g., setting pool max to 0) to shed load and free up request-handling threads.
  - When an integration point is throttled or disabled (e.g., the pool returns `null` instead of a connection), the AI MUST ensure the application logic catches this state and degrades gracefully, presenting a polite unavailability message to the user rather than throwing raw exceptions (e.g., `NullPointerException`) or crashing.
  - The AI MUST script and automate telemetry extraction and mitigation commands. Relying on HTML-based admin GUIs for large-scale cluster management or emergency remediation is strictly forbidden due to scaling limits and slow human interaction times.

@Workflow
1. **Vital Sign Analysis:** Check core metrics (session counts, network bandwidth, page latency, CPU usage). If the system shows infinite/high latency and low CPU utilization, identify the state as thread exhaustion and proceed to step 2.
2. **Thread Dump Execution:** Trigger and analyze thread dumps on the affected front-end application servers to identify exactly which resource pool or method the request-handling threads are blocked on.
3. **Dependency Tracing:** Follow the blocked threads to their target integration point. If the target is an internal middle-tier (e.g., Order Management), execute thread dumps on that middle-tier to find the ultimate external bottleneck (e.g., 3rd-party Scheduling Service).
4. **Capacity Assessment:** Compare the inbound request volume (upstream threads) to the maximum concurrent capacity of the downstream bottleneck. If a severe imbalance exists, proceed to mitigation.
5. **Component Isolation and Throttling:** Locate the specific, segregated resource pool connecting to the bottleneck. Dynamically update its configuration (e.g., setting maximum connections to 0 or a severely throttled number).
6. **Component Restart (ROC):** Invoke the specific component's `stop` and `start` lifecycle methods via an automated script to apply the new limits and instantly flush the previously blocked threads. DO NOT execute a rolling restart of the entire server cluster.
7. **Graceful Degradation Verification:** Verify that the application safely handles the restricted pool (e.g., checking for `null` connection objects) and routes the user to a graceful degradation UI flow.
8. **Remediation Automation:** Write a parameterized script encapsulating Steps 5 and 6, allowing operators to instantly dial the integration point's capacity up or down across the entire cluster based on real-time downstream health.

@Examples

[DO] Segregate connection pools by integration point to isolate failures.
```java
// Correct: Dedicated pools for different services prevent one slow service from consuming all threads.
DataSource inventoryPool = new DataSource("jdbc:inventory...", 5000); // 5s timeout
DataSource schedulingPool = new DataSource("jdbc:scheduling...", 5000); // 5s timeout

public DeliverySchedule getSchedule() {
    Connection conn = null;
    try {
        conn = schedulingPool.getConnection();
        if (conn == null) {
            // Graceful degradation when pool is administratively throttled to 0
            return DeliverySchedule.UNAVAILABLE_POLITE_MESSAGE;
        }
        // process request...
    } catch (TimeoutException e) {
        return DeliverySchedule.UNAVAILABLE_POLITE_MESSAGE;
    }
}
```

[DON'T] Use a single, shared connection pool without timeouts for multiple distinct services, risking total thread starvation.
```java
// Anti-pattern: Shared pool. If the scheduling database hangs, the inventory lookups will also fail because all threads are stuck waiting here forever.
DataSource sharedEnterprisePool = new DataSource("jdbc:enterprise_router..."); // No timeout

public DeliverySchedule getSchedule() {
    // Threads will block here infinitely if the downstream service hangs.
    Connection conn = sharedEnterprisePool.getConnection(); 
    // process request...
}
```

[DO] Implement component-level lifecycle hooks for rapid, dynamic recovery without process reboots.
```bash
# Correct: Scripted mitigation interacting with specific component lifecycle hooks via API
curl -X POST http://admin:8080/api/components/schedulingPool/config -d '{"maxConnections": 0}'
curl -X POST http://admin:8080/api/components/schedulingPool/stop
curl -X POST http://admin:8080/api/components/schedulingPool/start
```

[DON'T] Rely on rolling server restarts to clear blocked threads during an acute outage.
```bash
# Anti-pattern: Rebooting the world takes hours across a large cluster and does not fix the underlying downstream bottleneck.
for server in $ALL_SERVERS; do
    ssh $server "service application restart"
    sleep 600 # Waiting for caches to warm up, prolonging the outage
done
```