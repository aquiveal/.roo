# @Domain

These rules MUST trigger when the AI is tasked with designing, configuring, evaluating, or refactoring Service-Level Agreements (SLAs), Service-Level Objectives (SLOs), Service-Level Indicators (SLIs), system monitoring architectures, alerting rules, metric collection strategies, or reliability reporting for databases and distributed services.

# @Vocabulary

*   **Service-Level Agreement (SLA):** The comprehensive contract including enumerated lists of requirements, remedies, business impacts, and penalties.
*   **Service-Level Objective (SLO):** The internal commitments and targets set by architects and operators that guide the design and operation of the system to meet expected requirements.
*   **Service-Level Indicator (SLI):** A finite, specific metric used to measure compliance with an SLO.
*   **Latency:** The total round-trip time of a request, from client initiation to payload delivery. (Distinct from Response Time).
*   **Response Time:** The time it takes a server/system to service a request internally.
*   **Availability:** The ability of a system to return an expected, well-formed response to a requesting client, expressed as a percentage of overall time.
*   **Throughput:** The rate of successful requests in a specific period of time, typically measured on a per-second basis (e.g., QPS).
*   **Durability:** The successful persistence of a write operation to storage so it can be retrieved later.
*   **Cost/Efficiency:** The overall resource and human cost required to operate a service, ideally expressed as cost per business-driving action.
*   **Five 9's:** Shorthand for 99.999% availability.
*   **Lossy Process:** The anti-pattern of aggregating or averaging metrics (specifically latency) prior to storage, destroying outlier data and hiding true workload characteristics.
*   **MTBF (Mean Time Between Failures):** The traditional, robustness-focused measurement of time between system outages.
*   **MTTR (Mean Time To Recover):** The resiliency-focused measurement of how long it takes to resume service after a failure occurs.
*   **Resiliency:** A system state characterized by low MTTR, low impact during failures, and automated remediation, where failure is treated as a normal operational scenario.
*   **Robustness:** A system state focused heavily on avoiding failure (increasing MTBF), which often results in brittle, fragile architectures.
*   **RUM (Real User Monitoring):** Metric collection based strictly on actual user requests and error rates.
*   **Synthetic Monitoring:** Artificial tests and probes designed to ensure consistent, thorough coverage of code paths and geographical regions, regardless of active user traffic.
*   **Decaying Function:** An analytical method prioritizing recent datasets over older datasets to predict future SLO violations in rapidly changing release environments.

# @Objectives

*   Design Customer-Centric SLOs: The AI MUST build SLOs based entirely on the experience and requirements of the customer/user, not strictly on internal component metrics.
*   Prioritize Resiliency over Robustness: The AI MUST design systems and metrics that optimize for low MTTR (Mean Time To Recover) and graceful degradation rather than attempting to achieve zero failures.
*   Ensure Preemptive Visibility: The AI MUST design monitoring systems intended to identify and remediate potential impacts *before* an SLO is violated, never relying on monitoring merely to confirm a violation has already occurred.
*   Preserve Data Fidelity: The AI MUST strictly avoid metric averaging or aggregation mechanisms that obscure latency distribution outliers.

# @Guidelines

### 1. SLO/SLI Definition Rules
*   **Limit Indicators:** The AI MUST define a maximum of three (3) primary indicators per service. Exceeding three indicates the inclusion of symptoms rather than primary customer-centric metrics.
*   **Customer-Centric Scope:** The AI MUST define objectives based on end-to-end user experience (e.g., full page rendering, end-to-end API response) rather than isolated component health.

### 2. Latency Measurement Constraints
*   **Never Average Latency:** The AI MUST NOT use arithmetic averages, medians, or standard deviations to define or monitor latency SLOs. Latency distributions are multimodal and non-gaussian. Averaging is a lossy process that hides outliers.
*   **Use Percentiles:** The AI MUST express latency SLOs using percentiles (e.g., 99th or 99.9th percentile) to explicitly state the acceptable percentage of outliers.
*   **Define Ranges:** The AI MUST specify latency targets as a range (e.g., `between 25ms and 100ms`) rather than a single upper limit (`< 100ms`). Leaving the lower bound at 0 seconds incentivizes wasteful performance engineering efforts that exceed the network capacities of client devices.
*   **Separate Stages:** If measuring complex interactions (e.g., web page loads), the AI MUST split latency into distinct operational stages (e.g., initial response vs. final rendering).

### 3. Availability Definition Constraints
*   **Avoid Naive Percentages:** The AI MUST NOT define availability as a simple flat percentage (e.g., "99.9% uptime").
*   **Define the Time Window:** The AI MUST bind the availability percentage to a specific rolling time window (e.g., "averaged over one week").
*   **Set Degradation Thresholds:** The AI MUST define exactly what constitutes "downtime" by setting a threshold of affected users (e.g., "Downtime is called if > 5% of users are affected").
*   **Set Incident Boundaries:** The AI MUST define the maximum acceptable duration for a single continuous incident.
*   **Accommodate Maintenance:** The AI MUST explicitly codify allowable planned downtime parameters (frequency, duration, communication lead time, and max user impact).

### 4. Throughput & Durability Guidelines
*   **Tie Throughput to Latency:** The AI MUST pair throughput indicators with latency objectives to identify bottlenecks that constrain overall capacity without technically violating latency thresholds.
*   **Durability Windows:** For storage systems, the AI MUST define durability strictly as a maximum acceptable window of data loss during a failure (e.g., "No more than the past two seconds of data lost").

### 5. Cost & Efficiency Tracking
*   **Unit of Cost:** The AI MUST track cost based on business-value actions (e.g., cost per page view, cost per transaction, cost per subscription).
*   **Human Cost Integration:** The AI MUST include estimated operations, engineering, and on-call staff time in efficiency and cost measurements.

### 6. Monitoring & Alerting Architecture
*   **Raw Data Storage:** The AI MUST ensure logging architectures store raw success/error rates and exact latency values at high resolution (1-second sampling rates for critical paths) without pre-aggregation.
*   **Hybrid Monitoring:** The AI MUST implement both Real User Monitoring (RUM) for actual error rates and Synthetic Monitoring to prevent regional or time-based blind spots.
*   **Predictive Alerting:** The AI MUST design alerts that use decaying functions and historical comparisons to predict SLO violations *before* the error budget is exhausted. Alerts MUST trigger when the burn rate indicates a future violation.

# @Workflow

When tasked with designing or implementing an SLM (Service-Level Management) strategy for a service or database, the AI MUST follow this exact algorithmic sequence:

1.  **Identify the Customer Action:** Determine the exact end-to-end action the customer is trying to perform (e.g., "Sign up for an account", "Query order history").
2.  **Select Indicators (Max 3):** Choose the most critical SLIs from the core list: Latency, Availability, Throughput, Durability, Cost/Efficiency.
3.  **Draft Latency Objective:**
    *   Establish a realistic lower bound (fastest useful response).
    *   Establish the upper bound.
    *   Assign the percentile (e.g., 99%).
    *   *Resulting format:* "99% request latency over 1 minute must be between [Lower] and [Upper]."
4.  **Draft Availability Objective:**
    *   Assign the overall target percentage.
    *   Define the rolling time window.
    *   Set the maximum allowable duration for a single incident.
    *   Set the user-impact percentage that triggers an official "downtime" state.
    *   Define planned maintenance windows.
5.  **Draft Supporting Objectives (Throughput/Durability/Cost):**
    *   Set peak throughput bounds.
    *   Set time-based data-loss thresholds.
    *   Define the business unit action for cost tracking.
6.  **Design the Telemetry Pipeline:**
    *   Ensure 1-second sampling intervals for SLO-bound metrics.
    *   Verify raw metric storage is utilized rather than aggregated averages.
    *   Define Synthetic probes for edge cases/regions.
7.  **Configure Predictive Alerting:**
    *   Establish the total allowed error budget (e.g., 10.08 minutes of downtime per week).
    *   Calculate the current burn rate based on real user errors.
    *   Generate alert thresholds that trigger ticket creation *only* when the trajectory exceeds the allowed budget.

# @Examples (Do's and Don'ts)

### Defining Latency SLOs

**[DON'T]**
```yaml
# Anti-pattern: Uses a single upper bound, uses "average", lacks percentiles.
service_slo:
  latency:
    target: "< 100ms"
    measurement: "1-minute average"
```

**[DO]**
```yaml
# Correct: Uses a range to prevent over-engineering, uses percentiles, uses explicit time bounds.
service_slo:
  latency:
    target_range: "25ms - 100ms"
    percentile: 99
    evaluation_window: "1 minute"
```

### Defining Availability SLOs

**[DON'T]**
```text
# Anti-pattern: Naive flat percentage, no operational context, incentivizes brittleness.
The database must maintain 99.99% availability at all times.
```

**[DO]**
```text
# Correct: Granular, actionable, defines downtime bounds, accommodates maintenance.
Availability SLO:
- 99.9% availability averaged over one week.
- No single incident greater than 10.08 minutes.
- Downtime state is triggered ONLY if more than 5% of global users are affected.
- One annual 4-hour planned downtime allowed if communicated 2 weeks prior and affects < 10% of users concurrently.
```

### Monitoring Dashboard Configurations (Latency)

**[DON'T]**
```javascript
// Anti-pattern: Storing and graphing only the average latency per minute.
function calculateMetrics(requestLogs) {
  let totalLatency = sum(requestLogs.latency);
  let averageLatency = totalLatency / requestLogs.length;
  storeToDatabase(averageLatency); // LOSSY PROCESS! Outliers destroyed.
}
```

**[DO]**
```javascript
// Correct: Storing raw events, filtering the top 1% (to monitor the 99th percentile), and allowing min/max overlay visualization.
function evaluateLatencySLO(requestLogs_1_second_window) {
  // Store all raw values for accurate historical percentiles
  storeRawValuesToTimeSeriesDB(requestLogs_1_second_window);
  
  let sortedLogs = sortByLatency(requestLogs_1_second_window);
  let p99Logs = removeTopOnePercent(sortedLogs);
  
  if (p99Logs.some(log => log.latency > 100 || log.latency < 25)) {
      triggerBurnRateAlert("Latency SLO violation detected in current 1s window");
  }
}
```

### Alerting Posture

**[DON'T]**
*   Paging a human operator immediately every time a single web request fails or times out.
*   Generating alerts based on internal component CPU usage reaching 80% without correlating to actual user latency or throughput drops.

**[DO]**
*   Paging a human operator when a predictive decaying function identifies that the current error burn rate will exhaust the weekly 10-minute downtime budget within the next 4 hours.
*   Creating a non-paging ticket when garbage collection events consume 30% of the allowed latency budget by Tuesday.