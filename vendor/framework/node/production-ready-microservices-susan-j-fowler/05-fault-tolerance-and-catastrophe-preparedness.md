@Domain
These rules activate whenever the AI is tasked with designing system architecture, reviewing or writing microservice code, configuring deployment pipelines, building testing suites (unit, integration, end-to-end, load, chaos), setting up monitoring/remediation automation, or generating incident response documentation/postmortems.

@Vocabulary
- **Single Point of Failure (SPOF)**: A piece of a microservice's architecture that, if it fails, will bring down the entire microservice or dependency chain.
- **Internal Failures**: Failures originating within the microservice itself (e.g., code bugs, unhandled exceptions, local DB failures, scalability limits).
- **External Failures**: Failures originating in the lower three layers of the ecosystem (Hardware, Communication/Platform) or from downstream dependencies.
- **Resiliency Testing**: The practice of actively, repeatedly, and randomly pushing a microservice to fail in production to ensure graceful recovery.
- **Code Testing**: The combination of lint, unit, integration, and end-to-end (E2E) testing.
- **Load Testing**: Running target traffic loads against a microservice to evaluate scalability and behavior.
- **Chaos Testing**: Actively injecting failures (e.g., latency, host death, dependency outages) into production environments.
- **Time to Detection (TTD)**: The duration between a failure occurring and the alert/detection system identifying it.
- **Time to Mitigation (TTM)**: The duration between detection and the moment the impact on users/SLAs is halted (e.g., via failover or rollback).
- **Time to Resolution (TTR)**: The duration required to fix the root cause of the issue (does not count against SLA if mitigated).
- **Incident Scope**: Categorized as High (global/entire business), Medium (local and clients), or Low (only the individual service).
- **Incident Severity**: Categorized on a 0-4 scale based on the business impact.
- **Blameless Postmortem**: A follow-up document focusing strictly on facts, timelines, and systemic improvements without assigning personal blame to developers.

@Objectives
- Architect away Single Points of Failure (SPOFs) at both the microservice and ecosystem levels.
- Anticipate and mitigate all classes of failure (Hardware, Communication/Platform, Dependency, Internal).
- Validate fault tolerance through exhaustive, automated Resiliency Testing (Code, Load, Chaos).
- Eliminate human intervention in known failure scenarios by fully automating failure detection and remediation (rollbacks and failovers).
- Standardize incident response using a strict five-stage procedural framework to minimize TTD and TTM.

@Guidelines

**Architecture & SPOF Mitigation**
- The AI MUST analyze any provided architecture or request flow to identify Single Points of Failure (SPOFs). If a SPOF is found, the AI MUST propose a mitigation strategy (e.g., defensive caching, message queues, dynamic routing) or architect it away.
- The AI MUST configure separate communication channels for health checks and standard RPC data to prevent network clogging from causing false negative health checks.
- The AI MUST NOT implement or encourage version pinning for internal microservices or internal libraries; dependencies must be treated as living, changing entities.

**Handling Dependencies & External Failures**
- The AI MUST calculate and warn about composite SLA risks (e.g., Service A's SLA is mathematically bound by the SLA of its downstream Dependency B).
- The AI MUST implement failover mechanisms for dependency failures: re-routing to alternative endpoints, queueing requests, or fetching from an LRU (Least Recently Used) defensive cache.
- The AI MUST flag unhandled exceptions and improper exception catching, enforcing strict error handling at all architectural boundaries.

**Resiliency Testing Protocols**
- **Code Testing**: The AI MUST enforce the generation of 4 distinct test types: Lint, Unit (individual components), Integration (component interaction), and E2E (hitting clients, self, dependencies, and DBs).
- **Load Testing**: The AI MUST design load tests based on established quantitative (RPS/QPS) and qualitative (business metric) growth scales.
- **Load Testing Safety**: The AI MUST implement automated kill-switches in load testing scripts and MUST include steps/code to alert downstream dependencies before executing production load tests.
- **Chaos Testing**: The AI MUST define chaos testing scenarios utilizing centralized tools (like Simian Army) that simulate: disabled dependency endpoints, stopped traffic to a dependency, introduced latency, datacenter traffic halts, and random host shutdowns.

**Automated Remediation**
- The AI MUST automate failovers and rollbacks based on monitoring thresholds. Human beings MUST NOT be relied upon for failure detection or manual remediation of known alerts.
- The AI MUST treat configuration files like code. Any configuration deployment script MUST include automated rollback logic triggered by health check failures.

**Incident Response & Postmortems**
- The AI MUST structure incident response procedures according to the 5 Stages: Assessment, Coordination, Mitigation, Resolution, and Follow-up.
- The AI MUST prioritize Mitigation (reducing impact to users) over Resolution (fixing the root cause).
- The AI MUST generate postmortem documentation that is strictly blameless. The AI MUST NOT use developer names or assign personal fault, focusing instead on system gaps, TTD/TTM metrics, timelines, root-cause analysis, and action items.

@Workflow
When tasked with designing a fault-tolerant microservice, implementing testing, or writing incident response materials, the AI MUST follow this algorithmic process:

1. **Failure Scenario Mapping & SPOF Elimination**:
   - Analyze the microservice's architecture against the four failure categories (Hardware, Communication/Platform, Dependency, Internal).
   - Identify SPOFs. If a SPOF cannot be removed (e.g., mandated organizational tool), implement defensive caching or queuing as mitigation.
2. **Resiliency Testing Implementation**:
   - Generate Code Tests (Lint, Unit, Integration, E2E) to be run in the CI pipeline.
   - Design Load Tests targeting staging and production. Inject dependency notification steps and kill-switches.
   - Define Chaos Testing scenarios targeting the mapped failure scenarios.
3. **Automated Remediation Configuration**:
   - Map key metrics to warning/critical thresholds.
   - Write scripts/configurations that automatically trigger a rollback to the last known stable build (code or config) when critical thresholds are breached.
   - Configure dynamic routing for datacenter failovers or dependency circuit-breaking.
4. **Incident Response Standardization**:
   - Categorize the microservice's business criticality (Severity 0-4) and Scope (High/Medium/Low).
   - Draft runbooks outlining the 5 stages of incident response.
   - Create a blameless postmortem template pre-filled with the service's specific SLA, TTD, and TTM tracking metrics.

@Examples (Do's and Don'ts)

**Architecture & Dependency Handling**
- [DO]: Implement circuit breakers and fallback queues for downstream RPC calls.
  ```python
  @circuit(failure_threshold=5, recovery_timeout=30)
  def fetch_customer_data(user_id):
      try:
          return make_rpc_call("customer_service", user_id)
      except Exception:
          return lru_cache.get(user_id) # Defensive caching fallback
  ```
- [DON'T]: Hardcode specific versions of internal microservices (version pinning), as they change rapidly and will cause breaking failures.
  ```json
  "dependencies": {
      "internal-auth-service": "v1.0.4" // ANTI-PATTERN
  }
  ```

**Load Testing Execution**
- [DO]: Include a dependency notification payload and a latency-based kill-switch in a load test script.
  ```bash
  # Notify dependencies
  curl -X POST http://alert-system/notify -d '{"message": "Starting prod load test on Service X"}'
  # Run load test with auto-abort if latency exceeds 500ms
  run_load_test --target=prod --rps=5000 --abort-on-latency=500ms
  ```
- [DON'T]: Execute a massive load test directly against production without alerting downstream dependencies, as this mimics a DDoS attack and causes cascading outages.

**Automated Remediation**
- [DO]: Automate a rollback immediately if a deployment causes health checks to fail.
  ```yaml
  deploy:
    strategy: canary
    steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - analyze:
          metrics: [error_rate, latency]
          thresholds: {error_rate: "< 1%", latency: "< 200ms"}
          onFailure: AUTOMATIC_ROLLBACK # Human intervention removed
  ```
- [DON'T]: Trigger an alert that simply tells an on-call engineer to manually SSH into a server to revert a config file.

**Incident Response (Postmortem)**
- [DO]: Write a blameless postmortem focusing on systemic facts.
  *"Timeline: At 14:02, a configuration change was merged bypassing the automated validation script. The error rate spiked to 15%. TTD was 2 minutes. TTM was 5 minutes via automated rollback. Action Item: Mandate CI validation on all config repos."*
- [DON'T]: Write a postmortem assigning blame to a human.
  *"Timeline: At 14:02, John pushed a bad config file because he didn't review his code. Action Item: Tell John to be more careful."*