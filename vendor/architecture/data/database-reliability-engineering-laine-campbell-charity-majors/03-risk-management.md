@Domain
This rule file is triggered when the AI is tasked with designing system architecture, evaluating operational reliability, proposing infrastructure changes, performing risk assessments, conducting incident post-mortems, or establishing Service-Level Objectives (SLOs) and data recovery strategies.

@Vocabulary
*   **Kaizen**: Continuous, iterative improvement. Applied to risk assessment as an ongoing, cyclic process rather than a one-time event.
*   **Reductive Bias**: The human tendency to oversimplify complex concepts, hindering advanced problem-solving in distributed systems.
*   **Inaction Syndrome**: Choosing inaction due to the perceived risk of change being greater than the risk of the status quo. 
*   **Pager Fatigue**: Operator exhaustion caused by excessive or unnecessary alerting (e.g., false positives, alerting on trends instead of imminent failures).
*   **Group Polarization (Risky Shift)**: The tendency for groups to make more extreme decisions (highly risk-tolerant or highly risk-averse) than individual members would independently.
*   **Risk Transfer**: Groups demonstrating higher risk tolerance by shifting the responsibility of that risk to another group (e.g., Ops shifting risk to DBAs).
*   **Decision Transfer**: Overestimating risk to force decision-making responsibility up the management hierarchy.
*   **Bootstrapping**: The initial, pragmatic framing of a risk management process, focusing only on the most likely or highest-impact scenarios rather than attempting an exhaustive, quixotic list.
*   **Framing**: Creating a limited, pragmatic scope to bound risk assessment work.
*   **MTTR (Mean Time To Recover)**: The time it takes to resume service after a failure. Prioritized heavily over MTBF.
*   **MTBF (Mean Time Between Failures)**: The time between system failures. Maximizing this creates brittle, untested systems.
*   **Risk**: Likelihood multiplied by Impact (Consequence).
*   **Avoidance**: Finding a way to eliminate a risk entirely.
*   **Reduction**: Lessening the impact or likelihood of a risk when it occurs.
*   **Acceptance**: Labeling a risk as tolerable and planning for it to happen.

@Objectives
*   Embed risk assessment and mitigation natively into all architectural and operational workflows.
*   Prioritize system resiliency and rapid recovery (MTTR) over the elimination of all failures (MTBF).
*   Utilize "downtime budgets" to take intelligent risks for the sake of feature innovation and system improvement.
*   Eliminate cognitive and group biases from risk-related decision making.
*   Ensure the cost of mitigation resources is always less than the calculated cost of inaction.

@Guidelines
*   **Calculate Risk Quantitatively**: The AI MUST define risk strictly as `Likelihood * Impact`. 
*   **Apply Standardized Likelihoods**: The AI MUST categorize probability over a defined period (e.g., one week) using the following scale:
    *   *Almost Certain*: >50%
    *   *Likely*: 26–50%
    *   *Possible*: 11–25%
    *   *Unlikely*: 5–10%
    *   *Rare*: <5%
*   **Apply Standardized Impacts**: The AI MUST categorize impacts based strictly on SLO budgets:
    *   *Severe*: Degraded >100ms for ≥10 minutes for ≥5% of users; privacy breach; unauthorized access; data corruption. (Immediate SLO violation).
    *   *Major*: Degraded >100ms for 3–5 minutes for ≥5% of users; system capacity degraded to 100% of needed (vs 200% target). (Imminent SLO violation).
    *   *Moderate*: Degraded >100ms for 1–3 minutes for ≥5% of users; system capacity degraded to 125% of needed. (Contributes to SLO violation).
    *   *Minor*: Degraded >100ms for ≤1 minute for ≥5% of users; system capacity degraded to 150% of needed.
*   **Embrace Failure**: The AI MUST NOT attempt to eliminate all risks. Systems without stressors become brittle. The AI MUST recommend designing systems that experience regular, controlled stressors to build operational muscle memory.
*   **Mitigate Human/Group Bias**: The AI MUST explicitly evaluate its own proposed architectures for human/group factors:
    *   Are we ignoring familiar hazards (e.g., disk full) in favor of exotic ones?
    *   Are we assuming operators are perfectly rested? (AI MUST assume operators executing manual remediation are fatigued).
    *   Are we transferring risk or decision-making inappropriately?
*   **Alerting Rules**: The AI MUST recommend warnings for trends and reserve actual alerts (interrupts) ONLY for imminent SLO violations to prevent Pager Fatigue.
*   **Control Selection**: For every identified risk, the AI MUST explicitly provide options for Avoidance, Reduction, and Acceptance, evaluating the trade-off cost of each against the cost of downtime.
*   **Automate Recovery**: The AI MUST mandate automated remediation over manual remediation if the SLO downtime budget (e.g., 10 minutes) is shorter than human response time.

@Workflow
When tasked with assessing a system, proposing an architecture, or creating a reliability plan, the AI MUST follow this exact 7-step algorithmic process:

1.  **Service Risk Evaluation**
    *   Define the Availability and Latency SLOs.
    *   Calculate the business cost of downtime (Revenue lost per minute, customer lifetime value lost, data loss impact).
    *   Identify the peak value loss per minute.
2.  **Architectural Inventory**
    *   List all datacenters, components/tiers, roles, communication pathways, and background jobs.
3.  **Risk Prioritization (Bootstrapping & Framing)**
    *   Identify the most probable hazards and worst-case scenarios. Do NOT attempt an exhaustive list.
    *   Map each hazard using the strict Likelihood and Impact scales.
    *   Calculate Risk Level (Unacceptable, High, Moderate, Acceptable).
    *   Filter the list to focus exclusively on Unacceptable and High risks first.
4.  **Control Identification & Selection**
    *   For each prioritized risk, generate specific controls under three categories: Avoidance, Reduction, and Acceptance.
    *   Compare the implementation cost of the control against the cost of downtime calculated in Step 1.
    *   Select controls that prioritize lowering MTTR (e.g., automated failover) over increasing MTBF.
5.  **Phased Implementation & Testing**
    *   Define a phased rollout for the selected controls: Test environment (no traffic) -> Test environment (simulated traffic) -> Production (closely monitored).
    *   Define specific metrics to record during testing (e.g., time to failover, latency impacts, data corruption checks).
6.  **Operational Incorporation**
    *   Embed the control into normal, day-to-day operations (e.g., using failover processes for routine rolling deployments) to ensure it is constantly practiced and free of bugs.
7.  **Iterative Review (Kaizen)**
    *   Define the triggers for revisiting this assessment: Service delivery reviews (business shifts), Incident management (post-mortems), and Architectural pipeline changes.

@Examples (Do's and Don'ts)

*   **Principle: MTTR over MTBF**
    *   [DO]: "To handle database primary failure, implement an automated failover mechanism like MHA that triggers within 30 seconds. Incorporate this failover into standard weekly deployments to ensure the operations team practices it regularly and the automation remains tested."
    *   [DON'T]: "To handle database primary failure, procure highly expensive, fault-tolerant hardware to ensure the database never goes down, and require manual DBA intervention for any failover to ensure safety."

*   **Principle: Quantitative Risk Prioritization**
    *   [DO]: "Component: Web Server. Likelihood: Likely (26-50% chance of instance failure this week). Impact: Major (Takes 3-5 mins to replace manually, degrading service for >5% users). Risk: High. Control: Implement auto-scaling groups to replace instances in 5 seconds, reducing Impact to Minor and Risk to Moderate."
    *   [DON'T]: "Web servers might fail, which is bad for the users. We should try to monitor them closely and have someone restart them if they break."

*   **Principle: Alerting and Pager Fatigue**
    *   [DO]: "Configure an alert to page the on-call engineer ONLY when the latency SLO budget drops below 30% remaining. For disk space increasing at a predictable rate, generate a warning ticket in the queue for daytime resolution rather than a page."
    *   [DON'T]: "Configure a pager alert to fire anytime disk space exceeds 80% or if CPU usage spikes above 90% for one minute."

*   **Principle: Human Factors Assessment**
    *   [DO]: "While evaluating this manual disaster recovery runbook, we must account for Overoptimism and Fatigue. An operator executing this at 3:00 AM will likely make a mistake. We must wrap these steps in an idempotent script to reduce cognitive load."
    *   [DON'T]: "This 40-step manual recovery document is comprehensive and will guarantee safe recovery as long as the operator follows it carefully."