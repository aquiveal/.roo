# @Domain
These rules MUST be triggered when the AI is tasked with analyzing software architecture risk, evaluating architectural diagrams or proposals for vulnerabilities, assessing Agile project/story risk, conducting risk storming sessions, evaluating new technology choices, or generating risk assessment reports.

# @Vocabulary
*   **Risk Matrix**: A two-dimensional tool for calculating risk, determined by multiplying the *Impact* of the risk (1=Low, 2=Medium, 3=High) by the *Likelihood* of the risk occurring (1=Low, 2=Medium, 3=High), yielding a score from 1 to 9.
*   **Risk Categories**: 
    *   **Low Risk (Green)**: Matrix scores of 1 or 2.
    *   **Medium Risk (Yellow)**: Matrix scores of 3 or 4.
    *   **High Risk (Red)**: Matrix scores of 6 or 9.
*   **Risk Assessment**: A summarized report accumulating overall risk based on specific contextual criteria (e.g., Data Integrity, Availability) and domain areas/services.
*   **Direction of Risk**: A visual indicator showing whether a specific risk is improving, worsening, or remaining stable over time. Denoted by `+` (improving/green), `-` (worsening/red), or directional arrows with target numbers.
*   **Risk Storming**: A collaborative, three-part exercise (Identification, Consensus, Mitigation) used to determine architectural risk within a specific dimension.
*   **Risk Dimension**: A specific area of focus for a risk storming session (e.g., Availability, Scalability, Performance, Data Loss, Security).
*   **Identification Phase**: The noncollaborative first step of Risk Storming where individuals independently assign risk scores to architecture components to avoid influencing one another.
*   **Consensus Phase**: The collaborative second step of Risk Storming where divergent risk ratings are discussed to agree upon a single, unified risk matrix score for each component.
*   **Mitigation Phase**: The collaborative third step of Risk Storming focused on identifying architectural modifications to reduce or eliminate agreed-upon risks, weighing cost against risk reduction.
*   **SLA (Service-Level Agreement)**: A legally binding contractual agreement regarding system availability/performance used to calculate risk likelihood for third-party dependencies.
*   **SLO (Service-Level Objective)**: A non-legally binding goal for system availability/performance.
*   **Ambulance Pattern**: A prioritization routing pattern (using separate messaging channels) to prioritize critical system traffic over standard traffic during elasticity spikes.

# @Objectives
*   Eliminate subjectivity in architecture risk analysis by strictly applying the two-dimensional Impact × Likelihood Risk Matrix.
*   Produce highly actionable, filtered Risk Assessment reports that highlight critical vulnerabilities and their trajectory (Direction of Risk).
*   Simulate and facilitate structured Risk Storming exercises that accurately model the Identification, Consensus, and Mitigation phases.
*   Generate pragmatic risk mitigation strategies that balance ideal technical architecture with business constraints (e.g., cost, time).
*   Extend architectural risk modeling to Agile project management by evaluating the impact and likelihood of user story non-completion.

# @Guidelines
*   **Risk Matrix Calculation Rules**:
    *   The AI MUST ALWAYS calculate the **Impact** dimension first, followed by the **Likelihood** dimension.
    *   The AI MUST explicitly show the math: `Impact (1-3) × Likelihood (1-3) = Score (1-9)`.
*   **The Unproven Technology Rule**:
    *   If the architecture utilizes an unproven, unknown, or completely new technology to the team, the AI MUST automatically assign it the highest risk rating (Impact 3 × Likelihood 3 = 9). The Risk Matrix cannot be accurately applied to unknowns.
*   **Risk Assessment Formatting Constraints**:
    *   The AI MUST accumulate risk both by *Risk Criteria* (e.g., Availability, Security) and by *Domain Area* (e.g., Customer Registration, Order Fulfillment).
    *   When presenting risk to stakeholders or summarizing findings, the AI MUST use *Filtering* to increase the signal-to-noise ratio by exclusively displaying High Risk (6-9) areas, unless explicitly asked for a full report.
    *   The AI MUST include the *Direction of Risk* for every tracked metric using `[+]` for improving/decreasing risk, `[-]` for worsening/increasing risk, or noting "Stable" if unchanged.
*   **Risk Storming Constraints**:
    *   The AI MUST strictly isolate Risk Storming efforts to a **Single Dimension** (e.g., only Security, or only Elasticity) per analysis pass to avoid confusion.
    *   If evaluating a holistic system, the AI MUST use a comprehensive architecture diagram/model. If evaluating a specific feature, the AI MUST use a contextual diagram/model.
    *   When acting as a facilitator for Risk Storming, the AI MUST simulate the *Identification Phase* by generating multiple hypothetical developer/architect perspectives, explicitly generating divergent scores to force a *Consensus Phase* resolution.
*   **Mitigation & Negotiation Guidelines**:
    *   The AI MUST NOT propose a single, excessively expensive mitigation strategy as the only solution. 
    *   The AI MUST provide tiered mitigation options (e.g., an expensive ideal solution like clustering, and a pragmatic cheaper solution like database splitting) to facilitate stakeholder negotiation.
    *   When mitigating third-party dependency risks, the AI MUST rely on published SLAs or SLOs to accurately determine the *Likelihood* of failure.
    *   When mitigating elasticity/throughput risks, the AI MUST consider queueing (back-pressure), caching, and the Ambulance Pattern (priority routing).
*   **Agile Story Risk Evaluation**:
    *   When asked to evaluate Agile iterations, the AI MUST apply the Risk Matrix to user stories: `Impact if not completed` × `Likelihood of not completing`.

# @Workflow
When the AI is tasked with analyzing architecture risk or conducting a Risk Storming session, it MUST follow this rigid algorithm:

1.  **Define the Scope and Dimension**:
    *   Identify the architecture topology or components to be analyzed.
    *   Select ONE specific Risk Dimension (e.g., Availability, Scalability, Security).
2.  **Simulate Identification (Individual Assessment)**:
    *   List all major components in the target architecture.
    *   Generate 2 to 3 independent, simulated "participant" ratings for each component using the Risk Matrix (Impact × Likelihood). 
    *   *Enforce the Unproven Technology Rule* (assign 9) for any unfamiliar tools.
3.  **Drive Consensus (Collaborative Resolution)**:
    *   Identify components where simulated participants generated divergent scores.
    *   Provide architectural justification to resolve the divergence (e.g., "Participant A rated ELB a 6 due to high impact, but Participant B argued likelihood is 1 due to AWS redundancy. Consensus reached at 3 (Medium)").
    *   Establish a final, agreed-upon Risk Score for every component.
4.  **Formulate Mitigation Strategies**:
    *   Filter the consensus list to isolate High Risk (6-9) components.
    *   For each High Risk component, propose concrete architecture modifications (e.g., adding an API Gateway, separating databases, implementing back-pressure queues).
    *   Provide a cost/effort trade-off analysis for the proposed mitigations.
5.  **Generate the Risk Assessment Report**:
    *   Output a structured summary grouping the final risks by Domain Area and Risk Criteria.
    *   Apply Direction of Risk indicators (`[+]`, `[-]`, `[Stable]`).
    *   Present the "Before Mitigation" and "After Mitigation" architectural state.

# @Examples (Do's and Don'ts)

**Risk Matrix Calculation**
*   [DO]: "Database Availability Risk: Impact is High (3) because the call router fails without it. Likelihood is Low (1) because it is highly clustered. Score: 3 × 1 = 3 (Medium Risk)."
*   [DON'T]: "The database is probably a high risk because databases usually go down and cause big problems." *(Anti-pattern: Subjective guessing without using the Impact × Likelihood formula).*

**Handling Unknown Technologies**
*   [DO]: "The team has no experience with Redis Cache. Applying the Unproven Technology Rule: Impact (3) × Likelihood (3) = 9 (High Risk)."
*   [DON'T]: "The team doesn't know Redis, but Redis is generally reliable in the industry, so Likelihood is 1. Score = 3." *(Anti-pattern: Ignoring the specific team's risk of implementing unknown tech).*

**Risk Assessment Filtering and Direction**
*   [DO]: 
    ```text
    Filtered High Risk Assessment (Dimension: Elasticity)
    - Diagnostics Engine Interface: Score 9 [-] (Worsening under current seasonal load)
    - Legacy Monolith DB: Score 6 [Stable]
    ```
*   [DON'T]: 
    ```text
    Risk Assessment:
    - Diagnostics: 9 (getting worse)
    - Web Server 1: 2
    - Web Server 2: 2
    - Web Server 3: 2
    ``` *(Anti-pattern: Failing to use standard direction indicators (+/-) and failing to filter out noise/low-risk items in summary views).*

**Mitigation and Trade-offs**
*   [DO]: "To mitigate the High Risk (6) database availability issue, Option A is Database Clustering (Cost: High, mitigates 100% of target risk). If the stakeholder rejects this cost, Option B is Logical Database Splitting to isolate the failure domain (Cost: Low, mitigates 80% of target risk)."
*   [DON'T]: "The database is High Risk. You must implement a multi-region Active-Active cluster." *(Anti-pattern: Forcing the most expensive/complex technical ideal without offering pragmatic, tiered negotiation options).*

**Elasticity Mitigation**
*   [DO]: "To mitigate the Elasticity risk (9) on the Diagnostics Engine, we will implement an Ambulance Pattern using two message queues to prioritize Nurse traffic over Self-Service traffic, while adding an Outbreak Cache to deflect read-heavy bursts."
*   [DON'T]: "To mitigate Elasticity risk, just switch the REST calls to asynchronous messaging." *(Anti-pattern: Messaging provides back-pressure, but does not solve the timeout issue for prioritized users without the Ambulance Pattern and Caching).*