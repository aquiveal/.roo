# @Domain
Trigger these rules when tasked with designing, auditing, reviewing, or implementing the architecture, infrastructure, operational procedures, or lifecycle of a microservice. This includes tasks related to service-level agreements (SLAs), deployment pipelines, system scaling, failure mitigation, observability (monitoring/logging), and microservice documentation.

# @Vocabulary
- **Production-Ready**: A microservice that can be trusted to serve production traffic reliably, exhibiting high availability and meeting all eight standardization principles.
- **Availability**: The primary goal of microservice standardization; an emergent property of a production-ready system. Calculated as `Uptime / (Uptime + Downtime)`.
- **Nines Notation**: The measurement of availability expressed as a percentage (e.g., 99.99% is "four-nines"). Corresponds to a strict mathematical allowance of downtime per year, month, week, and day.
- **Stability**: The principle of mitigating negative side effects accompanying continuous evolution and change (development, deployment, deprecation).
- **Reliability**: The principle of establishing trust between a microservice, its clients, and its dependencies, ensuring it behaves as expected and protects its SLA.
- **Defensive Caching**: A reliability technique used to protect a microservice's availability against the failures of its downstream dependencies.
- **Scalability**: The ability to handle a large number of tasks simultaneously and adapt to growth, measured by both qualitative and quantitative growth scales.
- **Qualitative Growth Scale**: Scalability metrics tied to high-level business functions (e.g., scaling with "page views" or "customer orders").
- **Quantitative Growth Scale**: Scalability metrics tied to measurable technical throughput (e.g., requests per second).
- **Fault Tolerance & Catastrophe-Preparedness**: The ability of a microservice to withstand internal (self-inflicted) and external (infrastructure/ecosystem) failures, validated through resiliency testing.
- **Resiliency Testing**: A testing strategy encompassing code testing, load testing, and chaos testing (forcing failures in production).
- **Performance**: The measure of how quickly and efficiently a microservice handles requests and utilizes hardware resources.
- **Actionable Alert**: A monitoring alert that clearly indicates a real problem and requires a specific, documented response from an engineer.
- **Runbook**: Step-by-step mitigation strategies accompanying every actionable alert.
- **Production-Readiness Audit**: A quantifiable checklist evaluating whether a service meets the eight production-readiness requirements.
- **Roadmap**: A step-by-step guide detailing the work needed to bring an audited microservice up to a production-ready state.

# @Objectives
- Treat microservice availability as the ultimate overarching goal, recognizing that availability is an emergent property of applying the eight production-readiness standards.
- Eliminate ad-hoc, per-team operational rules by enforcing universal, quantifiable standardization across the entire microservice ecosystem.
- Ensure that the freedom and developer velocity inherent in microservice architecture do not compromise ecosystem stability.
- Frame all architectural and operational constraints as liberating mechanisms ("form is liberating") that prevent outages and increase developer velocity.
- Transform abstract availability targets into concrete allowable downtime budgets.

# @Guidelines
- **Availability Calculations**: The AI MUST calculate and state explicit downtime allowances when discussing SLAs. (e.g., 99.99% = 52.56 min/year, 4.38 min/month, 1.01 min/week, 8.66 sec/day).
- **Stability Enforcement**: The AI MUST mandate stable introduction and deprecation procedures. Deployments MUST follow a rigid pipeline: Staging -> Canary (2%-5% of production hosts) -> Production. 
- **Reliability Enforcement**: The AI MUST design microservices to expect and handle dependency failures. Defensive caching, fallback routing, and reliable discovery MUST be integrated into architecture proposals.
- **Scalability Definitions**: The AI MUST require both a Qualitative Growth Scale (business metric) and a Quantitative Growth Scale (RPS/QPS) when planning capacity or traffic management.
- **Performance Optimization**: The AI MUST flag inefficient resource utilization. The AI MUST prevent the use of synchronous, blocking processes for task handling where asynchronous processing is viable, and MUST minimize expensive network calls.
- **Fault Tolerance Mandates**: The AI MUST identify and eliminate Single Points of Failure (SPOFs). The AI MUST prescribe comprehensive resiliency testing, explicitly requiring code tests, load tests, and chaos tests (forcing failures in production).
- **Monitoring & Alerting Strictness**: 
  - The AI MUST NOT allow non-actionable alerts. Every alert MUST represent a real deviation requiring human intervention.
  - The AI MUST require a Runbook for every configured alert.
  - The AI MUST ensure logging provides enough state context to debug issues across an ecosystem that is constantly changing and deploying.
- **Documentation Requirements**: The AI MUST enforce strict documentation standards. Documentation MUST include: Architecture diagrams, onboarding/development guides, request flows, API endpoints, and on-call runbooks.
- **Organizational Understanding**: The AI MUST advocate for scheduled architecture reviews (whiteboarding the service) and quantifiable production-readiness audits that yield actionable roadmaps.
- **SRE Alignment**: The AI MUST align its recommendations with Site Reliability Engineering (SRE) practices, prioritizing quantifiable, measurable results over theoretical architecture.

# @Workflow
1. **SLA & Availability Assessment**: Identify the target availability (Nines). Calculate the exact allowable downtime per month/day. Use this strict budget to justify the subsequent architectural constraints.
2. **Standardization Audit - Stability & Reliability**: Evaluate the deployment pipeline. Ensure staging and canary phases exist. Review all dependencies and enforce defensive caching and fallback routing.
3. **Standardization Audit - Scalability & Performance**: Define the qualitative and quantitative growth scales. Map these scales to capacity planning, traffic management, and data storage scalability. Ensure resource utilization is highly efficient.
4. **Standardization Audit - Fault Tolerance**: Scan the architecture for SPOFs. Define catastrophe scenarios (internal and external) and map out the required resiliency tests (Code, Load, Chaos) to validate recovery.
5. **Standardization Audit - Monitoring**: Review the observability stack. Verify that dashboards reflect ecosystem health, logs capture system state accurately, and all alerts are strictly actionable and tied to a runbook.
6. **Standardization Audit - Documentation & Understanding**: Generate or verify the existence of the required documentation (Architecture diagram, request flows, runbooks). Recommend an architecture review and a production-readiness audit.
7. **Roadmap Generation**: Compile any missing standards into a step-by-step roadmap, assigning concrete tasks to bring the microservice to a fully production-ready state.

# @Examples (Do's and Don'ts)

**Availability and SLAs**
- [DO]: "The target SLA is four-nines (99.99%). This permits exactly 4.38 minutes of downtime per month. We must implement defensive caching so a downstream failure does not consume this budget."
- [DON'T]: "Make sure the microservice is highly available so it doesn't go down often."

**Deployment Pipelines (Stability)**
- [DO]: "Deployments must pass through Staging, proceed to a Canary pool serving 2% of production traffic, and only roll out to Production if key metrics remain stable."
- [DON'T]: "Deploy the new feature directly to production to maintain high developer velocity."

**Scalability Context**
- [DO]: "Growth Scale defined: Qualitatively, the service scales with 'customer orders'. Quantitatively, it must handle 500 RPS. Capacity planning will be based on projected quarterly customer order volume."
- [DON'T]: "Scale the service to handle 500 requests per second." (Ignores the qualitative business metric).

**Alerting and Monitoring**
- [DO]: "Alert: `High_Exception_Rate_Payment_API`. Threshold: > 5% error rate over 3 minutes. Actionable: Yes. Runbook: Link to mitigation steps for payment gateway timeouts."
- [DON'T]: "Alert: `CPU_Spike`. Threshold: > 60%." (Non-actionable, lacks context, lacks runbook).

**Fault Tolerance (Chaos Testing)**
- [DO]: "To ensure catastrophe-preparedness, we will implement chaos testing that randomly terminates production instances and severs database connections to validate the failover logic."
- [DON'T]: "We wrote unit and integration tests, so the service is fully fault-tolerant."

**Documentation**
- [DO]: "The repository must contain an architecture diagram, detailed request flows, a developer onboarding guide, and a complete on-call runbook detailing mitigation strategies for every alert."
- [DON'T]: "Just read the code to understand how the microservice handles data."