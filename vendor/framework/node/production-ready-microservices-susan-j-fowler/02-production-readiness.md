# @Domain

Trigger these rules when tasked with designing, architecting, auditing, or evaluating a microservice, particularly when the user requests a review of system architecture, deployment processes, infrastructure requirements, or overall "production-readiness" before a service handles live production traffic.

# @Vocabulary

- **Production-Ready**: A state in which an application or microservice can be trusted to serve production traffic by behaving reasonably, performing reliably, and maintaining high availability.
- **Availability**: The primary goal and emergent property of production-readiness, measured by dividing uptime by the total time a service was operational (uptime + downtime).
- **Service-Level Agreement (SLA)**: An agreement defining the expected availability of a service (e.g., 99.99% availability).
- **Nines Notation**: The percentage of time a service is available, expressed in "nines" (e.g., 99% is "two-nines", 99.99% is "four-nines").
- **Stability**: The principle of responsibly handling changes (development, deployment, deprecation) without causing instability within the larger ecosystem.
- **Reliability**: The principle that a microservice can be trusted by its clients, dependencies, and ecosystem, functioning correctly and routing/discovering reliably.
- **Scalability**: The ability of a microservice to handle a large and growing number of tasks/requests simultaneously. 
- **Qualitative Growth Scale**: Scalability tied to high-level business metrics (e.g., users, orders).
- **Quantitative Growth Scale**: Scalability tied to measurable quantities (e.g., requests per second).
- **Fault Tolerance**: The ability of a microservice to withstand both internal (code bugs) and external (datacenter outages) failures.
- **Catastrophe-Preparedness**: The state of having identified, planned for, and tested extreme failure scenarios.
- **Performance**: The measure of how well a microservice handles requests, processes tasks, and utilizes resources efficiently.
- **Monitoring**: The combination of logging, graphical dashboards, and actionable alerting to determine microservice health.
- **Runbook**: Step-by-step instructions accompanying actionable alerts, detailing mitigation strategies.
- **Site Reliability Engineer (SRE)**: Engineers primarily responsible for driving, enforcing, and implementing production-readiness standards across an organization.

# @Objectives

- Ensure that every microservice architecture design or audit prioritizes **Availability** as the ultimate goal.
- Evaluate microservices against the eight production-readiness principles: Stability, Reliability, Scalability, Fault Tolerance, Catastrophe-Preparedness, Performance, Monitoring, and Documentation.
- Transform abstract availability goals into quantifiable, actionable, and measurable engineering requirements.
- Identify and eliminate single points of failure, inefficient resource utilization, and undocumented dependencies.
- Enforce strict standardization to mitigate the dangers of high developer velocity and ecosystem evolution.

# @Guidelines

- **Availability Calculation Constraints**:
  - When evaluating SLAs, the AI MUST calculate allowed downtime accurately using "nines notation":
    - Two-nines (99%): 3.65 days/year, 14.4 minutes/day.
    - Three-nines (99.9%): 8.76 hours/year, 1.44 minutes/day.
    - Four-nines (99.99%): 52.56 minutes/year, 8.66 seconds/day.
    - Five-nines (99.999%): 5.26 minutes/year, 864.3 milliseconds/day.
- **Stability Requirements Enforcement**:
  - The AI MUST require a stable development cycle.
  - The AI MUST ensure the deployment process includes proper staging, canary (2%-5% of production hosts), and production rollouts.
  - The AI MUST check for stable introduction and deprecation procedures for new technologies or old microservices.
- **Reliability Requirements Enforcement**:
  - The AI MUST mandate integration tests and successful staging/canary phases to prevent compromising clients/dependencies.
  - The AI MUST require defensive caching and fallback plans to protect the microservice's SLA from dependency failures.
  - The AI MUST ensure routing, discovery, health checks, and error handling are explicitly defined and reliable.
- **Scalability Requirements Enforcement**:
  - The AI MUST define both Quantitative and Qualitative growth scales for the service.
  - The AI MUST identify hardware resource bottlenecks and enforce capacity planning.
  - The AI MUST explicitly require scalable traffic handling (e.g., preparing for traffic bursts).
  - The AI MUST evaluate the dependency chain to ensure dependencies can scale concurrently with the microservice.
  - The AI MUST ensure data storage solutions are architected for scale.
- **Fault Tolerance and Catastrophe-Preparedness Enforcement**:
  - The AI MUST explicitly identify potential internal and external single points of failure.
  - The AI MUST require a defined failure detection and remediation strategy.
  - The AI MUST mandate three types of resiliency testing: code testing, load testing, and chaos testing (scheduled and random failure injection).
  - The AI MUST ensure incidents and outages are wrapped into carefully executed, standardized procedures.
- **Performance Requirements Enforcement**:
  - The AI MUST flag synchronous/blocking architectures where asynchronous (nonblocking) task processing would increase performance.
  - The AI MUST identify and warn against expensive network calls.
  - The AI MUST mandate efficient hardware/resource utilization without over-provisioning (which wastes money) or under-provisioning (which harms availability).
- **Monitoring Requirements Enforcement**:
  - The AI MUST ensure microservice-level logging captures request and response data sufficient to reconstruct the system state at the time of failure without relying on static code versioning.
  - The AI MUST require a real-time, easily understood dashboard for key metrics.
  - The AI MUST mandate that ALL alerts are actionable and tied to specific, signal-providing thresholds (normal, warning, critical).
  - The AI MUST require a runbook for every actionable alert.
- **Documentation and Understanding Enforcement**:
  - The AI MUST require an architecture diagram detailing endpoints, request flows, and dependencies.
  - The AI MUST require an onboarding/development guide and an on-call runbook.
  - The AI MUST encourage the practice of whiteboarding/auditing architecture regularly to ensure organizational understanding.

# @Workflow

1. **Calculate Availability Baseline**:
   - Query or identify the target SLA for the microservice.
   - Output the exact allowed downtime per year, month, week, and day to establish strict constraints.
2. **Audit Stability and Reliability**:
   - Assess the deployment pipeline. Demand staging and canary configurations.
   - Map all dependencies and require a documented fallback or caching mechanism for each.
3. **Audit Scalability and Performance**:
   - Define the Qualitative growth scale (e.g., scales with "user logins").
   - Define the Quantitative growth scale (e.g., scales with "1,000 requests per second").
   - Evaluate resource allocation, ensuring efficient task processing (async vs. sync).
4. **Audit Fault Tolerance**:
   - Scan the architecture for single points of failure.
   - Prescribe specific resiliency tests: Code, Load, and Chaos testing methodologies.
5. **Audit Monitoring and Documentation**:
   - Verify the presence of a logging strategy that survives high deployment velocity.
   - Ensure the definition of normal, warning, and critical thresholds for alerts.
   - Check that a runbook is outlined for every alert.
   - Compile a checklist of missing documentation (architecture diagrams, onboarding guides).
6. **Generate Production-Readiness Roadmap**:
   - Output a step-by-step roadmap detailing exactly which of the 8 production-readiness requirements the service currently fails to meet, and prescribe concrete engineering tasks to remediate them.

# @Examples (Do's and Don'ts)

- **[DO]** Define availability quantitatively.
  *Example*: "The service requires four-nines availability (99.99%). This limits downtime to 52.56 minutes per year, or 8.66 seconds per day. We must implement defensive caching to ensure upstream dependency failures do not consume this downtime budget."
- **[DON'T]** Use availability as a vague goal without actionable steps.
  *Example*: "We need to make this microservice highly available so it doesn't go down." (Violation: Provides no concrete requirements).

- **[DO]** Mandate a phased deployment pipeline.
  *Example*: "To satisfy the Stability requirement, the deployment pipeline must push code to a staging environment, followed by a canary pool of 2% of production hosts, before a full production rollout."
- **[DON'T]** Allow direct-to-production deployments in high-velocity environments.
  *Example*: "Deploy the hotfix straight to the production servers to resolve the bug quickly." (Violation: Bypasses stability controls, risking broader ecosystem outages).

- **[DO]** Pair alerts with runbooks.
  *Example*: "Configure a critical threshold alert for CPU utilization > 85%. This alert must link to a runbook detailing the exact mitigation steps the on-call engineer must take."
- **[DON'T]** Create non-actionable alerts.
  *Example*: "Send an email alert every time a request times out so the team is aware." (Violation: Alerts must be actionable and accompanied by mitigation instructions, otherwise they create noise).

- **[DO]** Define scalability using both qualitative and quantitative scales.
  *Example*: "The service scales qualitatively with active shopping carts, and quantitatively at 500 database transactions per second."
- **[DON'T]** Define scalability using only current traffic metrics.
  *Example*: "The service currently handles 100 RPS, so it is scalable." (Violation: Ignores qualitative business metrics and fails to plan for capacity growth).

- **[DO]** Enforce chaos testing for fault tolerance.
  *Example*: "To meet Catastrophe-Preparedness requirements, implement chaos testing to randomly terminate database connections in production to verify that the fallback queue operates correctly."
- **[DON'T]** Assume architectural isolation prevents cascading failures.
  *Example*: "The microservice is isolated, so if its dependency fails, it will just return a 500 error." (Violation: Fails the Reliability standard; services must protect their own SLAs via caching or fallbacks rather than propagating failures).