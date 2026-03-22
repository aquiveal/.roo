@Domain
These rules MUST be triggered whenever the AI is tasked with designing, reviewing, or refactoring microservice architecture; configuring CI/CD deployment pipelines; generating test suites (unit, integration, end-to-end, load, or chaos tests); writing incident response playbooks or runbooks; setting up monitoring/alerting logic for remediation; or triaging system outages and failures.

@Vocabulary
- **Single Point of Failure (SPOF)**: A single piece of a microservice's architecture (or dependency) that, if it fails, brings down the entire microservice or ecosystem.
- **Internal Failures**: Failures originating within the microservice itself (e.g., buggy code, scalability limits, unhandled exceptions).
- **External Failures**: Failures originating in the lower ecosystem layers (hardware, network, app platform) or downstream dependencies.
- **Code Testing**: The baseline resiliency testing suite comprising lint, unit, integration, and end-to-end tests.
- **Load Testing**: Subjecting a microservice to specific target traffic loads (RPS/QPS/TPS) to identify scalability bottlenecks and ensure capacity.
- **Chaos Testing**: Actively and randomly pushing a microservice to fail in production to ensure graceful recovery (e.g., using tools like Simian Army).
- **Time to Detection (TTD)**: The time it takes to identify a failure. Must be minimized via automated monitoring.
- **Time to Mitigation (TTM)**: The time it takes to reduce the impact to users (e.g., via rollback). Counts against the SLA.
- **Time to Resolution (TTR)**: The time it takes to fix the root cause. Does not count against the SLA if fully mitigated.
- **Severity (0-4)**: Incident categorization based on the impact to the business (0 being total business failure, 4 being minimal/no business impact).
- **Scope (High/Medium/Low)**: Incident categorization based on blast radius (High = global/entire ecosystem, Low = local/single service).
- **Blameless Postmortem**: An incident follow-up document focusing strictly on objective facts, timelines, and root-cause analysis without blaming individuals.
- **Defensive Caching**: Storing data from dependencies to serve as a fallback when the dependency experiences an outage.

@Objectives
- Eliminate Single Points of Failure (SPOFs) through rigorous architecture reviews and failover design.
- Map and mitigate all internal and external failure scenarios before they impact production.
- Mandate comprehensive resiliency testing (Code, Load, and Chaos) as a strict gatekeeper for production readiness.
- Remove human intervention from failure detection and initial mitigation (enforce auto-rollbacks and auto-failovers).
- Standardize a rigorous, 5-stage incident response protocol (Assessment, Coordination, Mitigation, Resolution, Follow-up).

@Guidelines

### Architecture & SPOF Prevention
- The AI MUST analyze any provided architecture for SPOFs. If a SPOF is detected (e.g., a shared Redis queue without memory limits or failover), the AI MUST flag it and propose an architectural alternative or a mitigation strategy (such as defensive caching or queuing).
- The AI MUST NEVER treat a microservice as an isolated entity. Dependency chains MUST be mapped, as a failure in one service multiplies across the ecosystem (e.g., if a dependency's SLA drops, the client's SLA drops multiplicatively).

### Resiliency Testing Standards
- **Code Testing**: The AI MUST generate or verify four types of code tests for any microservice:
  1. Lint tests (syntax/style).
  2. Unit tests (isolated components).
  3. Integration tests (components working together).
  4. End-to-End tests (testing the service alongside its dependencies, clients, and databases).
- **Load Testing**:
  - The AI MUST mandate load testing in both staging and production environments.
  - The AI MUST enforce the rule: Alert all downstream dependency owners BEFORE running a load test that hits production endpoints.
  - Load tests MUST be scheduled during off-peak hours to avoid compromising real user traffic.
- **Chaos Testing**:
  - The AI MUST recommend or script chaos testing scenarios, including: disabling dependency APIs, stopping traffic to a datacenter, taking down random hosts, and injecting network latency.
  - Chaos tests MUST strictly log all events and have explicit termination permissions to prevent rogue cascading failures.

### Failure Detection & Automated Remediation
- The AI MUST NOT rely on humans for failure detection or initial mitigation. Relying on engineers to read dashboards to detect outages is an anti-pattern.
- The AI MUST implement automated rollback mechanisms. If a deployment causes warning/critical health check thresholds to be breached, the system MUST automatically revert to the last stable build.
- The AI MUST implement failover mechanisms (e.g., routing traffic to another datacenter or secondary endpoint) or fallback mechanisms (e.g., holding requests in a queue or returning defensively cached data).

### Incident Response Categorization
- When generating incident response documentation, the AI MUST categorize incidents using a dual-axis system:
  - **Severity (0-4)**: 0 (Business critical outage) to 4 (Minor, non-user-facing issue).
  - **Scope (High/Medium/Low)**: High (Global/Multi-service), Medium (Service + direct clients), Low (Service only).
- The AI MUST structure incident response plans strictly around the Five Stages of Incident Response:
  1. Assessment (Triage severity and scope).
  2. Coordination (Communicate via chat/email to create a record).
  3. Mitigation (Reduce impact to users immediately; stop the SLA clock).
  4. Resolution (Fix the root cause).
  5. Follow-up (Write a blameless postmortem with action items).

### Anti-Patterns to Avoid
- **Versioning Microservices/Pinning Dependencies**: The AI MUST NOT recommend pinning microservices or internal libraries to specific versions. Treat services as living entities; pinning causes out-of-date, catastrophic failures.
- **Human Failure Detection**: The AI MUST NOT design systems where an on-call engineer manually watches a dashboard to trigger a rollback.
- **Hotfixing over Rollback**: In emergencies, the AI MUST recommend rolling back to a stable build rather than deploying a rushed hotfix directly to production.
- **Blame in Postmortems**: The AI MUST reject any postmortem text that blames a specific engineer (e.g., "John deployed bad code").

@Workflow
When the AI is tasked with making a microservice fault-tolerant or designing an incident response strategy, it MUST follow this strict algorithmic process:

1. **SPOF & Failure Mapping Analysis**:
   - Map the microservice architecture.
   - Identify all Internal Failures (code bugs, DB limits, unhandled exceptions).
   - Identify all External Failures (hardware down, DNS error, dependency timeout/outage).
   - Flag any Single Points of Failure and enforce a mitigation (failover, cache, queue).
2. **Resiliency Test Configuration**:
   - Ensure the CI/CD pipeline enforces Lint, Unit, Integration, and End-to-End testing.
   - Generate load testing parameters based on qualitative/quantitative growth scales. Insert warnings to alert dependencies.
   - Define minimum Chaos testing scenarios (host kill, latency injection, dependency drop).
3. **Automated Remediation Setup**:
   - Define health check thresholds (Normal, Warning, Critical).
   - Write logic or configurations that automatically trigger a rollback when Warning/Critical thresholds are breached post-deployment.
   - Implement circuit breakers and defensive caching for downstream dependencies.
4. **Incident Response Playbook Generation**:
   - Define Severity (0-4) and Scope (High/Med/Low) matrix for the specific service.
   - Generate a 5-step response runbook (Assessment, Coordination, Mitigation, Resolution, Follow-up).
   - Generate a Blameless Postmortem template tailored to the service.

@Examples (Do's and Don'ts)

### Architecture Failover
- **[DO]**: Implement defensive caching and fallback queues.
  ```python
  def get_user_data(user_id):
      try:
          return user_service_client.get(user_id, timeout=2.0)
      except TimeoutError:
          # Fallback to defensive cache
          return lru_cache.get(user_id)
  ```
- **[DON'T]**: Allow an external dependency failure to crash the service.
  ```python
  def get_user_data(user_id):
      # Anti-pattern: No timeout, no fallback. Will cause cascading failure.
      return user_service_client.get(user_id)
  ```

### Automated Remediation (CI/CD Config)
- **[DO]**: Configure automated rollbacks based on metric thresholds.
  ```yaml
  deploy:
    strategy: canary
    canary_percentage: 10
    health_check:
      metrics: [error_rate, latency]
      threshold: warning
      action_on_breach: auto_rollback_to_last_stable
  ```
- **[DON'T]**: Rely on manual intervention for a bad deploy.
  ```yaml
  deploy:
    strategy: canary
    canary_percentage: 10
    on_failure: alert_on_call_engineer_to_evaluate # Anti-pattern: Human in the loop
  ```

### Incident Postmortem
- **[DO]**: Write blameless, fact-based postmortems.
  "At 14:00 UTC, a code change bypassed the integration test suite due to a misconfigured CI rule, resulting in a null pointer exception in production. Mitigation was achieved via auto-rollback at 14:04 UTC."
- **[DON'T]**: Write blame-focused incident reports.
  "At 14:00 UTC, Dave pushed bad code without testing it properly, which crashed the server."

### Load Testing Policy
- **[DO]**: Explicitly notify dependencies before testing.
  "Before running the 10,000 RPS load test on the `Orders` service, the `Payments` and `Inventory` service teams have been notified, and the test is scheduled for 03:00 UTC (off-peak)."
- **[DON'T]**: Blindly bombard dependencies with load tests in production during peak hours without warning.