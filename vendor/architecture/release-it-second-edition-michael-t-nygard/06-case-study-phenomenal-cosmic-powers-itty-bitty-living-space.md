# @Domain
Trigger these rules when the user requests assistance with system architecture, production operations, incident triage, performance diagnostics, distributed system design, or component lifecycle management. Activation is strictly bound to scenarios involving high-load events, system hangs, thread exhaustion, integration point failures, or the design of dynamically reconfigurable application components.

# @Vocabulary
- **Page Latency (Lagging Indicator)**: A measurement of response time that only factors in completed requests. It is a lagging indicator because requests that time out or hang infinitely are not averaged in until (or unless) they finish.
- **Rolling Restart**: The operational procedure of taking down and restarting servers one by one or in small batches to maintain availability. Under severe systemic load/deadlock, this procedure often fails as restarted servers are immediately crushed by the backlog.
- **Thread Dump**: A snapshot of the exact state of all threads executing in a process, used to definitively diagnose blocked threads, deadlocks, and resource pool exhaustion.
- **Resource Pool Exhaustion**: A state where all available connections/threads in a pool are checked out, causing subsequent requesting threads to block.
- **Conway's Law (Architectural Benefit)**: The principle that system design mimics organizational communication structures. In this context, it results in the beneficial segregation of components (e.g., a dedicated connection pool for a specific department's service), which can be independently disabled.
- **Recovery-Oriented Computing (ROC)**: A design philosophy based on three principles: 1) Failures in hardware and software are inevitable; 2) A priori prediction of all failure modes is impossible; 3) Human action is a major source of system failures. ROC prioritizes the ability to rapidly recover from failures over the futile attempt to prevent all failures.
- **Component-Level Restart**: The ability to stop, reconfigure, and restart a specific software component (like a connection pool) at runtime without rebooting the entire host server or application process.

# @Objectives
- Diagnose system hangs by ignoring misleading "healthy" metrics (like low CPU) and directly analyzing thread states and lagging indicators.
- Prevent cascading failures by strictly enforcing boundaries, timeouts, and throttling mechanisms on all external integration points.
- Architect systems according to Recovery-Oriented Computing (ROC) principles, ensuring that components can be reconfigured and rebooted independently of the main application process.
- Automate repetitive operational tasks and recovery procedures to eliminate human error during high-stress incidents.
- Protect the core business function (e.g., order capture) at the expense of non-critical subsystems (e.g., delivery scheduling) during extreme load.

# @Guidelines
- **Baseline Observation**: The AI MUST establish or require baselines for normal operational metrics (session counts, request-handling threads, heap memory, latency) before attempting to diagnose anomalous high-load events.
- **Interpreting Low CPU**: When encountering a system with high traffic, high latency, failing synthetic transactions, but abnormally LOW CPU usage, the AI MUST immediately diagnose the issue as a blocked-thread/resource-starvation anomaly.
- **Thread Dump Analysis**: The AI MUST mandate the generation and analysis of thread dumps to identify exactly which external call or resource pool is holding the request-handling threads hostage.
- **Timeout Enforcement**: The AI MUST strictly prohibit the design or implementation of resource pools or connection pools that lack explicit timeout values. Infinite blocking is an unacceptable anti-pattern.
- **Unbalanced Capacities**: When designing integrations between systems of different scales (e.g., a 100-server front-end calling a 1-server back-end), the AI MUST implement localized connection pools and throttles on the front-end to prevent overwhelming the back-end.
- **Dynamic Reconfiguration**: The AI MUST design application components to read configuration dynamically. Changes to properties like `max_connections` MUST NOT require a full JVM/server reboot to take effect.
- **Component Lifecycle Management**: The AI MUST implement `startService()` and `stopService()` lifecycle hooks on all integration components, allowing operators to disable or reset malfunctioning integrations on the fly.
- **Feature Throttling over Failure**: When an external integration fails, the AI MUST design the system to degrade gracefully (e.g., return a polite "scheduling unavailable" message) rather than failing the entire primary transaction.
- **Scripting Recovery**: The AI MUST mandate that multi-step recovery actions (e.g., setting a property, stopping a service, starting a service) be automated into a single executable script for operations teams to use under stress.
- **Evaluating Latency**: The AI MUST evaluate page latency with the understanding that it is a lagging indicator; if requests are hanging infinitely, the true latency is masked.

# @Workflow
1. **Pulse Assessment**: Verify the current state of system metrics against known baselines (Traffic, Sessions, Latency, CPU, Thread Utilization).
2. **Symptom Triage**: If the system is unresponsive but CPU/Network limits are not saturated, instantly pivot investigation to thread synchronization and resource pool blocking.
3. **Trace the Blockage**: Analyze thread dumps on the failing tier. If threads are blocked waiting for a downstream service, move to the downstream service and analyze its thread dumps to find the ultimate bottleneck.
4. **Identify the Capacity Mismatch**: Determine the capacity delta between the caller (e.g., 3,000 threads) and the provider (e.g., 25 threads). 
5. **Isolate and Throttle**: Locate the specific connection pool or component bridging the mismatch. 
6. **Execute Component Restart**: Apply configuration changes (e.g., setting `max` to 0 to disable) and execute a component-level restart (`stopService` -> `startService`) to immediately free upstream request-handling threads.
7. **Automate the Mitigation**: Write a consolidated script encapsulating the reconfiguration and component restart so operators can easily toggle the throttle based on real-time load.

# @Examples (Do's and Don'ts)

**[DO]** Design connection pools with strict timeouts and runtime lifecycle hooks.
```java
public class SchedulingConnectionPool implements LifecycleComponent {
    private int maxConnections;
    private int checkoutTimeoutMs;
    private boolean isRunning;

    public void setMaxConnections(int max) {
        this.maxConnections = max;
    }

    public synchronized void stopService() {
        this.isRunning = false;
        // Drain existing connections, abort waiting threads
    }

    public synchronized void startService() {
        // Initialize pool with current maxConnections
        this.isRunning = true;
    }

    public Connection getConnection() throws TimeoutException {
        if (!isRunning || maxConnections == 0) {
            throw new ComponentDisabledException("Service temporarily disabled.");
        }
        // Attempt checkout with strict checkoutTimeoutMs
    }
}
```

**[DON'T]** Rely on a full server reboot to apply critical integration configuration changes, as it prolongs outages and exacerbates load issues.
```java
// ANTI-PATTERN: Configuration read only on static initialization
public class SchedulingConnectionPool {
    private static final int MAX_CONN = Integer.parseInt(System.getProperty("max.conn"));
    
    public Connection getConnection() {
        // Infinite block if pool is exhausted
        return pool.take(); 
    }
}
```

**[DO]** Handle isolated integration failures by degrading gracefully and protecting the core transaction.
```java
try {
    DeliverySchedule schedule = schedulingPool.getSchedule(orderId);
    order.setSchedule(schedule);
} catch (ComponentDisabledException | TimeoutException e) {
    // Core transaction (Order) succeeds. Degrade specific feature gracefully.
    order.setScheduleStatus("Scheduling currently unavailable. We will contact you shortly.");
}
```

**[DON'T]** Allow a non-critical external integration to hold the primary request-handling thread open indefinitely, masking true latency and crashing the site.
```java
// ANTI-PATTERN: No timeout, no catch block. 
// A failure in getSchedule() will hang the main checkout thread, 
// eventually causing all 3,000 front-end threads to block and the site to crash.
DeliverySchedule schedule = legacySchedulingSystem.getSchedule(orderId);
order.setSchedule(schedule);
```

**[DO]** Write consolidated automation scripts for operations to use during an incident, abstracting away the multi-step component lifecycle.
```bash
#!/bin/bash
# toggle_scheduling.sh
# Usage: ./toggle_scheduling.sh [0 for disable, >0 for capacity]

NEW_MAX=$1
echo "Setting scheduling pool max to $NEW_MAX..."
set_property "schedulingPool.max" "$NEW_MAX"
echo "Restarting scheduling pool component..."
invoke_method "schedulingPool.stopService"
invoke_method "schedulingPool.startService"
echo "Component restarted successfully."
```

**[DON'T]** Perform rolling restarts of the entire application cluster when the root cause is a downstream bottleneck; the restarted servers will just immediately exhaust their threads again.