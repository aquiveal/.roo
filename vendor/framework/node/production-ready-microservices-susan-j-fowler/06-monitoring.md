# @Domain

This rule file is activated whenever the AI is tasked with designing, implementing, configuring, reviewing, or debugging observability, logging, dashboarding, alerting, or on-call runbook systems for microservices. It applies to tasks involving application code instrumentation, infrastructure-as-code for monitoring tools (e.g., Prometheus, Grafana, ELK stack, Datadog), log formatting, alert rule definitions, and the creation of operational documentation.

# @Vocabulary

- **Key Metrics**: The specific, quantifiable properties of a microservice that are necessary and sufficient for describing its behavior, health, and status.
- **Host and Infrastructure Metrics**: Key metrics pertaining to the servers and underlying infrastructure on which the microservice runs (e.g., CPU, RAM, threads, file descriptors, database connections).
- **Microservice Metrics**: Key metrics unique to the individual microservice's application layer (e.g., SLA, latency, endpoint success rates, handled/unhandled exceptions).
- **Test Tenancy**: The practice of marking data written by staging environments as test data so it can be easily identified and cleared.
- **Actionable Alert**: An alert that requires immediate, specific human intervention from an on-call developer to triage, mitigate, or resolve an issue. 
- **Nonactionable Alert**: An alert that is triggered but requires no action, is ignored, or cannot be resolved by the on-call developer. (Considered a strict anti-pattern).
- **Normal Threshold**: The appropriate upper and lower bounds of a key metric during standard operation, which MUST NOT trigger an alert.
- **Warning Threshold**: A deviation from the norm that could lead to a problem; MUST trigger an alert to allow mitigation *before* an outage occurs.
- **Critical Threshold**: A severe deviation indicating that an outage is occurring or the service's availability is actively being harmed.
- **On-Call Runbook**: A centralized document containing step-by-step instructions detailing how to triage, mitigate, and resolve specific alerts.
- **Time to Detection (TTD) / Time to Mitigation (TTM) / Time to Resolution (TTR)**: Metrics tracking the lifecycle of an outage; TTD and TTM count against a service's SLA, whereas TTR generally does not if the user impact has been mitigated.

# @Objectives

- **Total Visibility**: Ensure the exact state of the microservice can be reconstructed at any point in the past or present solely through its logs and metrics, mitigating the lack of strict microservice versioning.
- **Proactive Mitigation**: Design alerting thresholds (Warning and Critical) that allow developers to detect and mitigate issues *before* they escalate into full outages or impact the SLA.
- **Actionability**: Guarantee that 100% of triggered alerts require specific, documented human action, while automating away any recurring alerts that have standard, predictable resolutions.
- **Simplicity and Clarity**: Create dashboards that allow any external engineer to determine the exact health of the microservice at a single glance, free of clutter or non-key metrics.
- **Sustainable Operations**: Prevent on-call burnout by enforcing strict alerting hygiene, comprehensive runbooks, and appropriate team rotation schedules.

# @Guidelines

## Key Metrics Selection & Tracking
- The AI MUST categorize and track monitoring data into two distinct groups: Host/Infrastructure Metrics and Microservice Metrics.
- The AI MUST ensure Host/Infrastructure Metrics include: CPU utilization (per host and aggregate), RAM utilization, available threads, open file descriptors (FD), and active database connections.
- The AI MUST ensure Microservice Metrics include: Language-specific task processing metrics (e.g., uwsgi workers for Python), Availability, SLA adherence, Latency (service-wide and per-endpoint), Endpoint success rates, Endpoint responses and average response times, Originating clients, Errors and exceptions (both handled and unhandled), and the health/status of all downstream dependencies.
- The AI MUST ensure all key metrics are monitored across EVERY stage of the deployment pipeline (Staging, Canary, Production).

## Logging Constraints
- The AI MUST embed logging deep within the microservice codebase to capture all information essential to describing the exact state of the service at any given time.
- The AI MUST NOT rely on microservice versioning to debug past errors; logs must be robust enough to recreate the state of rapid, continuous deployments.
- **CRITICAL**: The AI MUST NEVER log identifying information (PII, customer names, Social Security numbers), passwords, access keys, secrets, or unencrypted user IDs.
- The AI MUST implement end-to-end request tracing throughout the entire client and dependency chain to measure total stack latency and availability.
- The AI MUST enforce per-service logging quotas and retention limits to ensure logging storage remains scalable and cost-effective.
- **ANTI-PATTERN**: The AI MUST NOT include debugging logs in code destined for production. Debug logs must be strictly isolated to local or development environments.

## Dashboard Design Rules
- The AI MUST configure dashboards to display ONLY the defined Key Metrics.
- **ANTI-PATTERN**: The AI MUST NOT include non-key metrics on the dashboard (which causes clutter), nor omit any metric that is actively alerted on (which reflects poor monitoring coverage).
- The AI MUST configure dashboards to overlay or visually indicate exact deployment times on all metric graphs to quickly correlate metric anomalies with new code releases.
- The AI MUST ensure dashboards are highly visual and intuitive, allowing an outsider to immediately understand service health.
- **ANTI-PATTERN**: The AI MUST explicitly discourage the practice of "dashboard watching" for outage detection. Dashboards are for anomaly visualization and threshold tuning; outage detection MUST be driven by automated Alerting.

## Alerting Standards
- The AI MUST configure alerts for every single Key Metric identified for the microservice.
- The AI MUST configure an alert to fire when a Key Metric is *missing* or *not seen*.
- The AI MUST define three levels of thresholds for key metrics: Normal, Warning, and Critical.
- The AI MUST ensure thresholds are high enough to avoid noise, but low enough to catch real problems before they impact the SLA.
- The AI MUST ensure 100% of alerts are Actionable. 
- **ANTI-PATTERN**: The AI MUST NOT configure nonactionable alerts. If an alert requires no action, the AI MUST remove it, reassign it, or alter the threshold.
- When configuring alerts on downstream dependencies, the AI MUST NOT trigger an alert unless the client service requires specific mitigation actions (e.g., manual failover, contacting the dependency's team).

## Incident Response & Runbook Requirements
- The AI MUST generate a corresponding On-Call Runbook entry for EVERY configured alert.
- The runbook entry MUST include: Alert name, description of the alert, description of the underlying problem, severity/scope, and step-by-step instructions on how to triage, mitigate, and resolve the issue.
- The AI MUST ensure runbook instructions are written simply and clearly enough to be understood by a fatigued developer at 2:00 AM.
- The AI MUST mandate two types of runbooks: Shared organizational runbooks for infrastructure/host-level alerts, and service-specific runbooks for microservice application alerts.
- The AI MUST identify recurring, easily mitigated alerts and provide code/scripts to automate their resolution directly within the microservice.

# @Workflow

When tasked with instrumenting monitoring for a microservice, the AI MUST adhere to the following strict algorithmic process:

1. **Metric Identification Phase**:
   - Enumerate all necessary Host/Infrastructure metrics based on the deployment environment.
   - Enumerate all necessary Microservice metrics (Latency, SLA, Endpoints, Errors, Language-specific limits).
   - Document these as the authoritative Key Metrics list.

2. **Logging Implementation Phase**:
   - Inject structured logging into the codebase to capture state transitions, request flows, and handled/unhandled exceptions.
   - Scan and strip any logging commands that capture PII, secrets, or unencrypted IDs.
   - Strip any debug-level logging from production-bound configurations.
   - Implement trace IDs for end-to-end request tracking.

3. **Dashboard Construction Phase**:
   - Generate dashboard configuration files (e.g., Grafana JSON).
   - Map every identified Key Metric to a visual graph.
   - Integrate deployment event markers into the graphs.
   - Audit the dashboard to ensure zero non-key metrics are present.

4. **Alerting Configuration Phase**:
   - For each Key Metric, define Normal, Warning, and Critical thresholds based on load-testing data or historical bounds.
   - Create an alert for the absence of each metric.
   - Validate every alert against the "Actionability" test. Remove or adjust any alert that does not require human intervention.

5. **Runbook Generation Phase**:
   - Create a markdown/wiki-style Runbook document.
   - For every alert defined in Phase 4, write a step-by-step triage, mitigation, and resolution guide.
   - Include general troubleshooting and debugging tips for unprecedented failures.

# @Examples (Do's and Don'ts)

## Logging

- **[DO]**: Log structured data representing the exact state and request flow, using trace IDs and hashed user identifiers.
  ```json
  {
    "timestamp": "2023-10-12T14:32:01Z",
    "level": "INFO",
    "trace_id": "req-987654321",
    "event": "order_processed",
    "endpoint": "/v1/process",
    "hashed_user_id": "a9f8b7c6d5",
    "response_time_ms": 45,
    "status": "success"
  }
  ```
- **[DON'T]**: Log PII, secrets, or temporary debug statements in production code.
  ```json
  {
    "timestamp": "2023-10-12T14:32:01Z",
    "level": "DEBUG",
    "message": "User John Doe (SSN: 000-11-2222) logged in with password 'hunter2'. Variable x is currently 4."
  }
  ```

## Dashboarding

- **[DO]**: Create a clean dashboard showing only Key Metrics with vertical lines indicating when a new deployment occurred.
  ```text
  [ Graph: CPU Utilization ] | [ Graph: API Latency (ms) ]
  --|-- (Deploy v1.2)        | --|-- (Deploy v1.2)
    |---                     |   |--
  ```
- **[DON'T]**: Clutter the dashboard with vanity metrics (e.g., "Total lines of code", "Number of Twitter followers") or require engineers to actively stare at the dashboard to catch outages instead of relying on PagerDuty/Alerts.

## Alerting

- **[DO]**: Define distinct, actionable thresholds mapped directly to a runbook.
  ```yaml
  alert: HighLatency
  expr: http_request_duration_seconds{job="receipt-sender"} > 0.5
  labels:
    severity: warning
  annotations:
    summary: "API latency is above 500ms"
    runbook_url: "https://wiki.internal/runbooks/receipt-sender#HighLatency"
    action_required: "Check dependency 'customer-service' health. If degraded, enable defensive caching fallback."
  ```
- **[DON'T]**: Create nonactionable, noisy alerts with no runbook or mitigation path.
  ```yaml
  alert: DependencyDown
  expr: up{job="third-party-weather-api"} == 0
  annotations:
    summary: "Weather API is down"
    action_required: "None. Just wait for them to fix it. Do not wake up."
  ```

## On-Call Runbooks

- **[DO]**: Write explicitly clear, step-by-step instructions for a 2:00 AM scenario.
  ```markdown
  ### Alert: HighDatabaseConnections
  **Severity**: Critical (0)
  **Scope**: Local Service
  **Problem**: The microservice is exhausting the maximum allowed connection pool to PostgreSQL.
  
  **Triage**:
  1. Check the Dashboard (Link) to confirm the connection count graph is pinned at 100%.
  
  **Mitigate**:
  1. Immediately restart the microservice instances to flush zombie connections:
     `kubectl rollout restart deployment receipt-sender`
  
  **Resolve**:
  1. Check logs for unhandled exceptions causing connection leaks.
  2. Revert the last deployment if it occurred within the last 2 hours.
  ```
- **[DON'T]**: Write vague, unhelpful runbooks that force the engineer to figure it out from scratch.
  ```markdown
  ### Alert: DB Error
  Something is wrong with the database. Log into the server and figure out why it's crashing. Try Googling the error code. Good luck.
  ```