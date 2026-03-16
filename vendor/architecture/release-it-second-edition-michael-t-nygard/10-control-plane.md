# @Domain
Trigger these rules when the user requests assistance with infrastructure automation, deployment pipeline design, monitoring and observability setup, platform engineering, orchestration, configuration management, or designing administrative command-and-control interfaces for applications.

# @Vocabulary
*   **Control Plane:** The collection of software and services that run in the background to manage, schedule, and orchestrate other software, ensuring production load is successful.
*   **Mechanical Advantage:** The multiplier on human effort provided by automation, which allows massive systemic changes but can rapidly amplify errors if unchecked.
*   **Platform Team:** A team that provides self-service capabilities, APIs, and infrastructure to application developers, treating them as customers rather than acting as a manual operational chokepoint.
*   **System Failure:** An outage or issue resulting from tools, playbooks, or interfaces that permit or amplify human mistakes, contrasting with the blame-oriented "human error."
*   **Real-User Monitoring (RUM):** Direct measurement of the user's experience and latency from the client side, providing true indicators of system health.
*   **Top Line / Bottom Line Metrics:** Economic value indicators; top line refers to revenue generation (e.g., successful transactions, queue depths), while bottom line refers to operational and infrastructure costs.
*   **Configuration Service:** A distributed database (e.g., ZooKeeper, etcd) used for dynamic configuration, orchestration, and leader election.
*   **Canary Deployment:** A deployment strategy where new code is routed to a small subset of instances first, acting as an early warning system to reject bad builds before they reach all users.
*   **Command Queue:** A shared message queue or pub/sub bus used to broadcast administrative commands to multiple instances simultaneously.

# @Objectives
*   Design platform automation that maximizes mechanical advantage for routine tasks while preserving human judgment for destructive or large-scale actions.
*   Shift operational responsibilities from manual intervention by a centralized team to self-service APIs consumed by autonomous development teams.
*   Establish system-wide transparency that unifies technical metrics with economic value and user experience.
*   Implement command and control mechanisms that fail safely, degrade gracefully, and are immune to rapid, unchecked automation failures.

# @Guidelines

### Automation and Safeguards
*   When configuring automation (e.g., autoscalers, orchestrators), the AI MUST implement "governors" (rate limits and safety boundaries) to prevent the system from removing too much capacity or executing destructive actions too quickly.
*   The AI MUST ensure automation pauses and requires human confirmation before executing scale-in or deletion operations that cross safe operational thresholds (e.g., terminating more than a defined percentage of instances).

### Postmortems and Incident Review
*   When generating postmortem templates or incident reports, the AI MUST frame issues as "System Failures" rather than "Human Error." The AI MUST focus on how the tooling allowed the error to occur.
*   The AI MUST include analysis of "near misses" and successful operations in review processes to learn from anomalies that did not result in outages.

### Platform Engineering
*   When defining platform team deliverables, the AI MUST design self-service interfaces and APIs that application teams consume, rather than defining manual request queues or ticket-based workflows.
*   When designing database administration workflows, the AI MUST separate infrastructure management from application data modeling, enforcing machine-readable migration formats (XML, JSON, YAML) for automated deployments.

### Development Environments
*   When designing CI/CD and development infrastructure, the AI MUST treat development and QA environments as production systems for the engineering team, applying production-level SLAs, monitoring, and automated provisioning to them.

### Transparency and Metrics
*   When designing observability, the AI MUST integrate Real-User Monitoring (RUM) to accurately gauge user experience, as internal instance metrics are insufficient.
*   The AI MUST configure unified dashboards that correlate technical performance with Economic Value metrics, explicitly monitoring top-line indicators (business transaction completion rates, queue depths) and bottom-line indicators (infrastructure utilization, operational cost).
*   The AI MUST configure metric aggregation over time to allow for long-term historical analysis without exhausting storage.
*   The AI MUST define nominal alerting ranges based on standard deviations (e.g., mean +/- two standard deviations) correlated to specific cyclical business periods (e.g., hour of the week).

### Required Instance Metrics
*   When instrumenting an application, the AI MUST expose the following categories:
    *   **Traffic:** Page requests, transaction counts, concurrent sessions.
    *   **Business Transactions:** Processed, aborted, conversion rates, dollar value.
    *   **Users:** Demographics, errors encountered, login success/failure rates.
    *   **Resource Pools:** Enabled state, total/checked-out resources, blocked threads, wait times.
    *   **Database:** SQLException counts, query counts, average response times.
    *   **Integration Points:** Circuit breaker states, timeout counts, network/protocol errors, concurrent requests.
    *   **Caches:** Hit rates, memory used, items flushed, time spent creating items.

### Configuration Services
*   When integrating tools like ZooKeeper or etcd, the AI MUST architect the application so that instances can successfully start up even if the configuration service is temporarily unreachable.
*   The AI MUST ensure that network partitions isolating a configuration node do not trigger global shutdown commands to the rest of the application.

### Provisioning and Deployment
*   When designing deployment pipelines, the AI MUST strictly separate build and run stages, utilizing a secure artifact repository that prevents direct deployment from developer workstations.
*   The AI MUST implement Canary Deployments within the pipeline to automatically reject bad builds based on anomaly detection (e.g., error spikes, latency) before widespread rollout.

### Command and Control
*   For applications with slow startup times (e.g., JVMs, large caches), the AI MUST implement live control mechanisms via an administrative API.
*   The AI MUST bind the administrative API to a separate, private network port inaccessible from the public internet.
*   The AI MUST support the following live controls: reset circuit breakers, adjust connection pools/timeouts, disable outbound integrations, reload configuration, start/stop accepting load, and feature toggles.
*   The AI MUST NOT implement "flush cache" endpoints in production, as this causes severe performance degradation and database dogpiles.
*   The AI MUST NOT implement database schema update or data-wipe commands in the production application code.
*   When using Command Queues for fleet-wide administration, the AI MUST introduce randomized delays (jitter) or wave-based execution in the workers to prevent synchronized dogpiles on shared resources.
*   When designing operator interfaces, the AI MUST prioritize scriptable Command Line Interfaces (CLIs) and HTTP APIs over Graphical User Interfaces (GUIs) to enable reliable automation and avoid manual clicking errors.

### Platform Players
*   When utilizing prefab platforms (e.g., Kubernetes, Mesos), the AI MUST embrace native platform constructs and declarations fully, and MUST NOT build custom wrappers or abstraction scripts around their APIs.

# @Workflow
1.  **Assess Scale and ROI:** Determine if the operational complexity of a full control plane is justified by the scale of the system and rate of deployment. If small, default to simplified, stateless deployments without heavy coordination services.
2.  **Establish the Pipeline:** Architect the CI/CD pipeline ensuring isolated builds, artifact repositories, and environments (Dev/QA) governed by production-level SLAs.
3.  **Implement Transparency:** Instrument the application to emit the required comprehensive metric categories (Traffic, Business, Resources, Caches, Integrations). Route logs to a centralized indexer and correlate metrics to economic value.
4.  **Integrate Configuration & Discovery:** Introduce dynamic configuration services (if at scale), ensuring applications degrade gracefully and boot successfully during configuration service outages.
5.  **Build Command and Control:** Expose scriptable, private-port administrative APIs for live tuning of long-running instances. Ensure destructive commands (cache flushing, schema drops) are strictly omitted.
6.  **Apply Automation Governors:** Audit all autoscaling and orchestration scripts. Inject rate-limits, blast-radius constraints, and human-in-the-loop approvals for large-scale destructive actions.

# @Examples (Do's and Don'ts)

### Command and Control Interfaces
**[DO]** Expose administrative controls on a dedicated, private port for safe, scriptable operations.
```python
# Application traffic on port 8080, Admin traffic on port 9090
app = Flask("public_app")
admin_app = Flask("admin_app")

@admin_app.route("/admin/circuit-breaker/reset", methods=["POST"])
def reset_breaker():
    circuit_breaker.reset()
    return jsonify({"status": "reset_successful"})

if __name__ == "__main__":
    # Run admin API on private interface only
    Thread(target=lambda: admin_app.run(host="10.0.0.5", port=9090)).start()
    app.run(host="0.0.0.0", port=8080)
```

**[DON'T]** Mix admin controls on the public port, or implement dangerous "flush cache" operations.
```python
app = Flask("app")

# ANTI-PATTERN: Admin command on public port
# ANTI-PATTERN: Implementing a catastrophic cache flush in prod
@app.route("/api/v1/admin/flush-all-caches", methods=["GET"])
def flush_caches():
    global_cache.clear_all() # Will cause a database dogpile immediately
    return "Caches cleared"
```

### Automation Governors
**[DO]** Limit the rate and percentage of instances an autoscaler can terminate to prevent runaway scale-in.
```yaml
# Kubernetes HorizontalPodAutoscaler with scale-down stabilization
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60 # Governor: Max 10% capacity removed per minute
```

**[DON'T]** Allow automation to terminate unlimited instances based solely on a potentially faulty metric.
```yaml
# ANTI-PATTERN: No scale-down limits. If metrics fail, all pods could be terminated.
behavior:
  scaleDown:
    policies:
    - type: Percent
      value: 100 # Can terminate everything instantly
```

### Configuration Service Dependency
**[DO]** Allow the application to start using cached or default configuration if the configuration service is unavailable.
```java
public AppConfig loadConfig() {
    try {
        return etcdClient.get("app/config", timeout=2000);
    } catch (TimeoutException | ConnectionException e) {
        log.warn("Config service unreachable. Falling back to local cache.");
        return LocalCache.getLastKnownConfig();
    }
}
```

**[DON'T]** Force the application to crash on startup if the configuration service is down.
```java
public AppConfig loadConfig() {
    // ANTI-PATTERN: Hard dependency prevents recovery if etcd is partitioned
    return etcdClient.get("app/config"); 
}
```