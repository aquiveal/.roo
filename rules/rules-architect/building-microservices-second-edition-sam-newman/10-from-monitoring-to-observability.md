# @Domain
These rules MUST trigger whenever the AI is tasked with designing, implementing, configuring, or reviewing telemetry, logging, metrics, tracing, alerting, or production testing within a microservice or distributed system architecture. This includes requests related to system health, incident response preparation, service-level definitions (SLAs/SLOs/SLIs), and infrastructure observability tooling.

# @Vocabulary
- **Observability**: A property of a system denoting the extent to which its internal state can be understood from its external outputs. It allows operators to ask questions they didn't know they needed to ask.
- **Monitoring**: An activity (something done to a system) typically involving predefined dashboards and alerts. Monitoring is a subset of observability.
- **MELT**: An overly reductive acronym (Metrics, Events, Logs, Traces). The AI MUST recognize these as overlapping implementation details of a broader concept: the unified event stream.
- **Correlation ID**: A unique identifier generated at the perimeter of a system and passed along to all downstream microservices to track a specific cascade of calls.
- **Clock Skew**: The inevitable desynchronization of system clocks across distributed machines, rendering timestamp-based chronological event ordering unreliable.
- **Cardinality**: The number of unique dimensions or queryable fields in a metric. High-cardinality data contains many tags (e.g., user ID, build number) and requires specialized storage (e.g., Honeycomb, Lightstep) compared to low-cardinality tools (e.g., Prometheus).
- **Span**: A record of local activity within a thread or microservice, serving as the building block of a distributed trace.
- **Service-Level Agreement (SLA)**: A high-level business contract defining the bare minimum acceptable service offering and associated penalties.
- **Service-Level Objective (SLO)**: A team-level agreement defining the target range for an acceptable system behavior.
- **Service-Level Indicator (SLI)**: A specific, measurable metric of how the software is behaving (e.g., response time, error rate) used to track against an SLO.
- **Error Budget**: The acceptable amount of system unreliability (e.g., allowed downtime per quarter). Used to dictate deployment velocity and risk tolerance.
- **Alert Fatigue**: A dangerous operational state where an overload of irrelevant or un-prioritized alerts causes operators to ignore critical system failures.
- **Semantic Monitoring**: Evaluating if a system is operating correctly from a business-value perspective (e.g., "Are we selling $20,000/hour?") rather than a technical perspective (e.g., "Is CPU < 90%?").
- **Synthetic Transactions**: Fake user interactions injected safely into a production system with known inputs and expected outputs to proactively detect failures.
- **MTBF**: Mean Time Between Failures.
- **MTTR**: Mean Time to Repair. In distributed systems, optimizing for fast MTTR is often more realistic and valuable than optimizing for infinite MTBF.

# @Objectives
- Shift the architectural focus from passive, static monitoring to active, interrogable observability.
- Ensure that every microservice emits standardized, highly contextual external outputs (events/logs/traces).
- Eliminate blind spots in distributed call chains by mandating Correlation IDs and Distributed Tracing.
- Prevent alert fatigue by establishing strict, context-rich, and actionable alerting criteria.
- Base system health evaluations on semantic business value (SLOs/SLIs) rather than binary technical thresholds.
- Implement safe, continuous "testing in production" to detect failures before users do.

# @Guidelines

## 1. Observability Mindset & Event Unification
- The AI MUST NOT treat logs, metrics, and traces as completely isolated silos. Instead, treat all external system outputs as generic "events" that can be indexed, aggregated into metrics, or stitched into traces.
- The AI MUST design observability systems as mission-critical, secure production systems. Do not expose PII in logs, and protect telemetry infrastructure against supply chain attacks.

## 2. Log Aggregation & Correlation (The Prerequisites)
- The AI MUST mandate log aggregation as a strict prerequisite before implementing any microservice architecture.
- **Standardization**: The AI MUST define a uniform log format (e.g., JSON or consistent column structures) across all microservices to enable centralized parsing and querying.
- **Avoid Agent Formatting**: The AI MUST NOT rely on log-forwarding agents (e.g., Fluentd, Logstash) to reformat logs, as this consumes excessive CPU. Formatting MUST be handled natively by the microservice prior to output.
- **Correlation IDs**: The AI MUST ensure a unique Correlation ID is generated at the system perimeter (e.g., API Gateway) and propagated as a parameter/header to *all* downstream calls. This ID MUST be logged in a consistent, standardized field in every log entry.
- **Clock Skew Mitigation**: The AI MUST NOT use log timestamps to determine exact chronological ordering or exact latency calculations for distributed calls. Distributed tracing MUST be utilized for accurate timing.

## 3. Metrics & Cardinality Management
- When selecting metrics storage, the AI MUST analyze the cardinality requirements.
- For low-cardinality requirements (e.g., simple CPU rates), the AI MAY recommend tools like Prometheus.
- For high-cardinality requirements (e.g., tracking requests by user ID, build number, and host OS simultaneously), the AI MUST explicitly recommend high-cardinality-capable tools (e.g., Honeycomb, Lightstep) to prevent database write explosions.
- The AI MUST implement standardization for metric naming conventions across all teams (e.g., `ResponseTime` instead of `RspTimeSecs`).

## 4. Distributed Tracing
- The AI MUST specify tracing architectures utilizing open standards (e.g., OpenTelemetry) to avoid vendor lock-in.
- The AI MUST define spans that capture start/end times, contextual logs, and key-value metadata (e.g., customer ID, endpoint).
- **Sampling Strategies**: The AI MUST implement sampling to prevent system overload. Recommend dynamic/smart sampling (e.g., sampling 100% of errors but 1% of successful requests) over blind random sampling where possible.

## 5. System Health, SLOs, and Error Budgets
- The AI MUST NOT define system health as a binary "Up/Down" state.
- The AI MUST define Service-Level Indicators (SLIs) that measure exact user-facing behaviors.
- The AI MUST define Service-Level Objectives (SLOs) built upon those SLIs.
- The AI MUST calculate and enforce Error Budgets. If a system exceeds its error budget, the AI MUST recommend halting feature deployments in favor of reliability improvements.

## 6. Alerting and Alert Fatigue Prevention
- The AI MUST NOT create alerts for every minor technical anomaly. Ask: "Should this wake someone up at 3 A.M.?"
- The AI MUST evaluate all proposed alerts against the EEMUA guidelines:
  1. **Relevant**: The alert provides actual value.
  2. **Unique**: The alert does not duplicate another alert.
  3. **Timely**: The alert arrives quickly enough to act upon.
  4. **Prioritized**: The operator knows what to fix first.
  5. **Understandable**: The message is clear and readable.
  6. **Diagnostic**: It is immediately clear what is broken.
  7. **Advisory**: The alert tells the operator what action to take.
  8. **Focusing**: It draws attention to the most critical issue.

## 7. Semantic Monitoring & Testing in Production
- The AI MUST prioritize MTTR (Mean Time To Repair) via fast rollbacks and excellent telemetry over impossible MTBF (Mean Time Between Failures) goals.
- **Semantic Monitoring**: The AI MUST define monitoring checks based on business value (e.g., "Are orders processing?") using Real User Monitoring or Synthetic Transactions.
- **Synthetic Transactions**: The AI MUST script automated, safe fake user interactions with known inputs and expected outputs to run continuously against the production environment.
- The AI MUST ensure that Synthetic Transactions are isolated safely so they do not corrupt actual production data (e.g., do not actually ship physical products for fake test orders).

## 8. Tool Selection Criteria
- The AI MUST recommend tools that are "Democratic" (usable by all developers, not just a segregated ops team).
- The AI MUST ensure tools provide four types of context:
  1. **Temporal**: Compared to past states.
  2. **Relative**: Compared to other components.
  3. **Relational**: Dependency impacts.
  4. **Proportional**: Scope of the blast radius.

# @Workflow
When tasked with designing or auditing an observability or monitoring strategy, the AI MUST follow this exact sequence:

1. **Establish the Log Aggregation Baseline**:
   - Define the standardized log format (e.g., JSON schema).
   - Implement perimeter generation and downstream propagation of Correlation IDs.
   - Restrict PII from being logged (Data Frugality).
2. **Define Business Health & SLOs**:
   - Identify the core business semantic behaviors (e.g., "Customer places order").
   - Define SLIs for these behaviors.
   - Establish SLOs and calculate the permissible Error Budget.
3. **Design the Telemetry Pipeline**:
   - Select metric tools based on cardinality requirements.
   - Implement OpenTelemetry-compliant Distributed Tracing with defined spans and dynamic sampling rules.
4. **Configure Actionable Alerting**:
   - Audit all alerts against the EEMUA 8-point checklist.
   - Delete/downgrade non-critical alerts to dashboard-only visibility to prevent alert fatigue.
5. **Implement Testing in Production**:
   - Design Synthetic Transactions that continuously execute against production endpoints.
   - Ensure safety boundaries for fake data injection.

# @Examples (Do's and Don'ts)

**[DO] Standardized Logging with Correlation IDs**
```json
{
  "timestamp": "2023-10-15T16:01:03Z",
  "service": "PaymentService",
  "level": "ERROR",
  "correlation_id": "abc-12345-xyz",
  "message": "Payment validation failed",
  "action": "ValidatePayment",
  "duration_ms": 142
}
```

**[DON'T] Unstructured, Uncorrelated Logging**
```text
15-10-2023 16:01:03 Error validating the payment. Connection timeout.
```
*(Why: No correlation ID to trace the upstream request, unstructured text requires expensive regex parsing, missing service context).*

**[DO] EEMUA-Compliant Alerting**
```text
ALERT: SEV-1 - Checkout Flow Failing
Context: The OrderService is returning 503s for 15% of requests over the last 2 minutes.
Diagnostic: Connections to the Primary Database are exhausting the pool.
Advisory: Scale up the Database Connection Pool OR trigger a rollback of OrderService to v1.4.2.
Link to Runbook: https://wiki.internal/runbooks/db-pool-exhaustion
```

**[DON'T] Lazy/Fatigue-Inducing Alerting**
```text
ALERT: CPU Usage High
Host: 10.0.4.52 is at 95% CPU.
```
*(Why: Not diagnostic, not advisory, lacks proportional context. Is this a background batch job or a user-facing outage? This wakes an operator up at 3 AM with no clear next steps).*

**[DO] Semantic Monitoring (Synthetic Transactions)**
*Configure a cron job that executes a test script every 1 minute in production:*
1. Create a user with a specific `is_test_user: true` flag.
2. Add a test item to the cart.
3. Execute checkout using a sandbox payment gateway credential.
4. Verify the system returns a `200 OK` and an Order ID.
5. Alert immediately if this flow fails.

**[DON'T] Purely Technical Monitoring for Business Health**
*Assuming the business is healthy solely because all microservices are reporting CPU < 50% and Memory < 60%.*
*(Why: A misconfigured routing rule or expired API key could mean 0 traffic is reaching the services. The servers are technically healthy, but the business is making zero money).*