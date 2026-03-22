@Domain
Trigger these rules when tasks involve designing, configuring, or modifying infrastructure management systems, deployment pipelines, CI/CD environments, monitoring and telemetry frameworks, configuration services, autoscaling logic, or administrative command-and-control interfaces.

@Vocabulary
- **Control Plane**: The collection of software and services that manage, orchestrate, and observe the infrastructure and applications, distinct from the systems processing direct production user data.
- **Governor**: A programmatic safeguard built into automation tools to limit the speed, scope, or scale of destructive actions (e.g., terminating instances) to allow for human intervention.
- **Platform Team**: A group that provides self-service APIs, infrastructure, and tools for application developers to use, rather than executing operational tasks on their behalf.
- **Real-User Monitoring (RUM)**: The direct measurement of the actual user experience in production, as opposed to relying solely on server-side health checks.
- **Push-based Deployment**: A deployment model where a central server reaches out (e.g., via SSH) to target machines to apply configurations or code. Best for long-lived VMs/physical hosts.
- **Pull-based Deployment**: A deployment model where instances reach out to a configuration service to pull their own configurations. Best for ephemeral/elastically scaled instances.
- **Canary Deployment**: A deployment strategy where new code is rolled out to a small subset of instances first, evaluated for health, and then rolled out to the rest.
- **Dogpile**: A cascading system failure caused when multiple instances perform a heavy operation simultaneously (e.g., flushing a cache, or responding to a global command queue message), overwhelming shared resources.

@Objectives
- Maximize system resilience by preventing automation from executing unbounded destructive actions.
- Shift the operational mindset from "doing the work" to "providing self-service APIs" (Platform as a Service).
- Treat all CI/CD, development, and QA infrastructure with the same SLA and rigor as production systems.
- Establish system-wide transparency centered on economic value and user experience, rather than binary "up/down" server statuses.
- Implement robust, resilient configuration services that do not act as single points of failure for application startup or operation.
- Provide scriptable, CLI-first command and control interfaces; avoid reliance on operational GUIs.

@Guidelines

**1. Automation and Governors**
- The AI MUST treat "human error" as a system failure. If a script or tool allows a user to destroy the system via a typo, the tool is at fault.
- The AI MUST implement Governors on all automation that removes capacity or modifies state.
- The AI MUST cap the maximum percentage of capacity that automation can remove at one time (e.g., < 50%). Exceeding this threshold MUST require explicit human confirmation.
- The AI MUST build deceleration zones into automation to account for momentum (e.g., delay further scaling actions while waiting for recent scaling actions to take effect).

**2. Platform and Ecosystem Design**
- The AI MUST design platform tools (monitoring, DB provisioning, deployments) as self-service APIs for developers to consume.
- The AI MUST NOT design workflows where the platform/operations team is a manual gatekeeper or ticket-processor for application configurations.
- The AI MUST embrace third-party platforms (e.g., Kubernetes, Mesos, CloudFoundry) natively; DO NOT build abstract wrappers around their APIs.

**3. Development Is Production**
- The AI MUST configure development, CI/CD, and QA environments using the exact same automation, topologies, and SLA standards as production environments.
- The AI MUST secure the build server. CI/CD plugins MUST be treated as critical attack vectors and audited for provenance.
- The AI MUST enforce that production deployments ONLY originate from the CI/CD pipeline, NEVER from a developer's local machine.

**4. System-Wide Transparency**
- The AI MUST instrument systems to answer two questions: "Are users receiving a good experience?" and "Is the system creating economic value?"
- The AI MUST expose metrics across the following categories:
  - *Traffic*: Page requests, transaction counts, concurrent sessions.
  - *Business*: Transactions processed/aborted, conversion rates, dollar values, queue depths.
  - *Users*: Usage patterns, error encounter rates, successful/unsuccessful logins.
  - *Resource Pools*: Total resources, high-water marks, blocked threads, creation/destruction rates.
  - *Databases*: Exceptions thrown, query counts, average response times.
  - *Integration Points*: Circuit breaker states, timeouts, protocol/network errors, concurrent requests.
  - *Caches*: Hit rates, memory footprint, eviction counts, creation times.
- The AI MUST aggregate logs off-host to a centralized indexing/search system (e.g., ELK, Splunk) via push (containers) or pull (long-lived VMs) mechanisms.

**5. Configuration Services (ZooKeeper, etcd, Consul)**
- The AI MUST design applications to successfully start up even if the configuration service is unreachable.
- The AI MUST design applications to continue serving traffic using cached/stale configuration if the configuration service partitions or goes offline.
- The AI MUST ensure that a partitioned configuration node cannot erroneously instruct the autoscaler to shut down the world.

**6. Command and Control**
- The AI MUST design administrative interfaces for the CLI/scripting. GUIs MUST NOT be the primary method for executing operational playbooks.
- The AI MUST expose admin APIs over HTTP on a dedicated, internal-only port that is strictly inaccessible to public traffic.
- The AI MUST NOT expose a "flush cache" command in production, as this causes immediate database dogpiles.
- The AI MUST NOT expose database schema updates or "wipe data" functions via live control APIs. Schema changes MUST occur via the deployment pipeline.
- If using a Command Queue (pub/sub) to broadcast admin commands to instances, the AI MUST inject randomized delays (jitter) or use wave-based execution in the instance handlers to prevent dogpiling the underlying resources.

@Workflow
When requested to design, build, or modify control plane architecture, the AI MUST adhere to the following strict algorithm:

1. **Evaluate Scale and Cost**: Determine if the organizational scale justifies running complex distributed tools (e.g., ZooKeeper, Consul) or if simpler injected configurations (e.g., environment variables) suffice.
2. **Establish Transparency First**: Before building control mechanisms, define the metric/log collection pipelines. Map business top-line (revenue/conversion) and bottom-line (resource/ops cost) metrics to technical instrumentation.
3. **Secure the Build Pipeline**: Ensure the CI/CD system is defined as the sole source of truth for production artifacts. Implement Canary deployment stages in the pipeline.
4. **Implement Governors**: Identify any destructive or scaling automation. Wrap these in rate-limiters, percentage thresholds, and manual override tripwires.
5. **Design the Control Interface**: Expose necessary live-control toggles (circuit breaker resets, connection pool sizing, feature toggles) via secure, CLI-accessible REST APIs or jitter-enabled command queues. Validate that dangerous controls (cache flush, schema wipe) are omitted.
6. **Validate Failure Modes**: Review the architecture to explicitly confirm that the failure of the control plane (monitoring down, config service down, deploy server down) WILL NOT impact the running data plane (user traffic).

@Examples (Do's and Don'ts)

**Principle: Automation Governors**
- [DO]: `if (instancesToRemove > totalInstances * 0.10) { alertHumanForApproval(); return; } else { executeTermination(); }`
- [DON'T]: `autoscaler.getDesiredState().then(state => scaleTo(state.instanceCount));` (Blindly trusting the config without limits).

**Principle: Command and Control Interfaces**
- [DO]: Provide a REST API on a private port (e.g., 9090) with an endpoint `POST /admin/circuit-breakers/reset`. Provide a bash script wrapping `curl` for operators to iterate over instances.
- [DON'T]: Build a heavy web GUI that requires an operator to manually click "Reset" on 50 different instances during an active Sev-1 incident.

**Principle: Handling Command Queues**
- [DO]: `onReceive('RELOAD_CONFIG', () => { setTimeout(reload, Math.random() * 30000); });` (Spreads the load over 30 seconds).
- [DON'T]: `onReceive('RELOAD_CONFIG', () => { database.fetchConfig(); });` (Causes an immediate synchronized dogpile on the database).

**Principle: Configuration Service Resilience**
- [DO]: `try { config = etcd.fetch(); cache.save(config); } catch (e) { config = cache.load() || default; log.warn("Using stale config"); }`
- [DON'T]: `let config = etcd.fetchSync(); if (!config) process.exit(1);` (Creates a hard dependency on the control plane).

**Principle: Safe Live Controls**
- [DO]: Expose controls to adjust connection pool maximums, trigger graceful shutdown draining, or flip feature toggles.
- [DON'T]: Expose `POST /admin/flush-cache` or `POST /admin/drop-tables`. Ensure schema migrations are purely handled by the deployment pipeline.