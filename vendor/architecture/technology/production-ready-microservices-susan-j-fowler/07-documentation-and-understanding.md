@Domain
Trigger these rules when the user requests the creation, review, structuring, or updating of documentation for a microservice, system architecture, on-call runbook, onboarding guide, API specification, or when performing a production-readiness audit, architecture review, or creating a production-readiness roadmap.

@Vocabulary
- **The Onion Principle**: The philosophy of providing complete, selfless documentation that shares full knowledge of a service, preventing other developers from having to reverse-engineer or start from scratch.
- **Production-Ready Documentation**: A centralized, updated, and comprehensive repository of knowledge containing both bare facts and organizational context for a microservice.
- **Architecture Diagram**: A high-level visual representation abstracting the inner workings of a service to display components, endpoints, request flows, upstream/downstream dependencies, databases, and caches.
- **On-Call Runbook**: A comprehensive troubleshooting document containing general incident response procedures and explicit, step-by-step triage, mitigation, and resolution instructions for every single alert.
- **2 A.M. Rule**: The standard dictating that all on-call runbooks must be written so clearly and simply that a half-asleep developer can follow them flawlessly in the middle of the night.
- **Production-Readiness Audit**: A quantifiable checklist evaluation of a microservice against the eight standards (stability, reliability, scalability, fault tolerance, catastrophe-preparedness, performance, monitoring, and documentation).
- **Production-Readiness Roadmap**: A detailed, step-by-step plan mapping unfulfilled production-readiness requirements to technical details, linked tickets, and assigned developers.
- **Architecture Review**: A scheduled, collaborative evaluation of a microservice's architecture to discover scalability bottlenecks, single points of failure, and technical debt.
- **Microservice Understanding**: The organizational process and cultural standard ensuring that knowledge of a service's architecture, failure modes, and production-readiness status is aligned across individual developers, teams, and the overall organization.

@Objectives
- Centralize and standardize all microservice documentation to eliminate technical debt and organizational sprawl.
- Enforce the integration of documentation updates as a mandatory, blocking step in the standard development cycle (atomically linked to code changes).
- Translate complex microservice architectures into clear, jargon-free documentation accessible to developers, managers, and product managers alike.
- Eradicate the "black box" dependency problem by exhaustively documenting request flows, API endpoints, SLAs, and fallback mechanisms.
- Reduce Time to Mitigation (TTM) and Time to Resolution (TTR) by generating hyper-specific, actionable on-call runbooks tailored to the 2 A.M. Rule.
- Quantify and drive microservice quality by generating structured Production-Readiness Audits and Roadmaps.

@Guidelines
- **Documentation Location & Format Constraint**: The AI MUST structure documentation intended for a centralized, shared, and easily accessible internal website or wiki. README files and code comments MUST NOT be treated as the primary documentation source; they are supplementary only.
- **Development Cycle Integration Constraint**: When generating code changes, new features, or new alerts, the AI MUST simultaneously generate or prompt the user for the corresponding documentation updates. Documentation is NOT secondary to writing code.
- **Writing Style Constraint**: The AI MUST write clearly and concisely. Avoid heavy jargon unless explicitly defined. The documentation must be universally understandable by cross-functional roles.
- **Service Description Constraint**: Every documentation set MUST begin with a "Short Description" that is strictly limited to 1-2 sentences explaining what role the service plays in the overall ecosystem/business.
- **Architecture Diagram Constraint**: The AI MUST generate or define requirements for an Architecture Diagram that explicitly maps components, endpoints, request flows, dependencies (upstream/downstream), and datastores.
- **Contact & Links Constraint**: The AI MUST generate sections for Team Contact Info (members, roles, current on-call engineer) and Links (repository, dashboard, RFCs, architecture review slides).
- **Onboarding Guide Constraint**: The AI MUST include step-by-step technical details with concrete commands for checking out code, setting up the environment, starting the service, running tests, committing, and deploying via the pipeline.
- **API & Dependency Documentation Constraint**: For every API endpoint, the AI MUST document the name, description, request format, and response format. For every dependency, the AI MUST list the dependency name, endpoints used, expected SLA, and the fallback/caching mechanism in case of failure.
- **Runbook Constraint (2 A.M. Rule)**: For EVERY alert, the AI MUST document: Alert Name, Description, Problem Context, Severity/Scope, Communication Protocol, and exact step-by-step commands for Triage, Mitigation (reducing user impact), and Resolution (fixing root cause).
- **FAQ Constraint**: The AI MUST generate a Frequently Asked Questions section anticipating queries from both internal team members and external dependency consumers.
- **Audit & Roadmap Constraint**: When evaluating a service, the AI MUST generate a strict Yes/No audit against production-readiness standards, followed by a Roadmap mapping every "No" to a concrete technical task, ticket link, and assignee.
- **Automation Constraint**: The AI MUST advocate for and script automated checks for production-readiness requirements wherever possible to replace manual auditing.

@Workflow
1. **Context Extraction**: Analyze the provided microservice code, configuration, or user prompt to identify the service's purpose, endpoints, dependencies, and operational metrics.
2. **Generate Core Description**: Draft a 1-2 sentence high-level description of the microservice's business function.
3. **Map Architecture & Flows**: Document the architecture diagram structure, detailing all internal components, external dependencies, data stores, and the exact path of request flows.
4. **Compile Operational Metadata**: Create the Contact/On-Call and Links sections with placeholders for specific team members, repository URLs, and dashboard URLs.
5. **Draft Onboarding & Dev Guide**: Write a sequential list of exact terminal commands required to clone, build, test, and deploy the service.
6. **Detail APIs and Dependencies**: Create a comprehensive matrix of all exposed endpoints and all consumed upstream dependencies, explicitly noting SLAs and fallback behaviors.
7. **Construct the 2 A.M. Runbook**: Identify all known alerts. For each, generate foolproof, step-by-step triage, mitigation, and resolution instructions requiring zero guesswork.
8. **Populate FAQs**: Generate 3-5 anticipated questions regarding the service's behavior, setup, or troubleshooting.
9. **Perform Readiness Audit**: Evaluate the gathered documentation against the production-readiness standards.
10. **Generate Roadmap**: Output a structured roadmap for any missing documentation or architectural gaps identified in the audit.

@Examples

**[DO]** Write a clear, concise service description:
> **Description:** After a customer places an order, the `receipt-sender` service processes the transaction payload and sends a formatted receipt to the customer via email.

**[DON'T]** Write a jargon-heavy, overly technical description:
> **Description:** `receipt-sender` is a Node.js async microservice utilizing Kafka pub/sub to consume raw binary buffers from the order-gateway topic, serializing them into JSON, mapping the AST, and pushing through SendGrid's REST API while handling backpressure.

**[DO]** Write a 2 A.M. Rule compliant On-Call Runbook entry:
> **Alert:** High CPU Utilization (>85%)
> **Description:** The service is consuming excessive CPU, risking a drop in request processing speed.
> **Severity/Scope:** Severity 2 / Scope Medium
> **Triage:**
> 1. Run `kubectl top pods -n receipt-sender` to identify the specific pod spiking.
> 2. Check the Kibana dashboard to see if an abnormal spike in incoming order traffic correlates with the CPU spike.
> **Mitigation:**
> 1. Immediately scale the deployment to distribute load: `kubectl scale deployment receipt-sender --replicas=10`
> **Resolution:**
> 1. Once mitigated, pull the CPU profile for the offending pod: `go tool pprof http://<pod-ip>:8080/debug/pprof/profile`
> 2. Analyze for memory leaks or infinite loops and roll back to the previous stable build if introduced by a recent deploy.

**[DON'T]** Write a vague runbook entry:
> **Alert:** CPU is high
> **Steps:** Check the logs to see what is causing the CPU to spike. Restart the pods if it looks bad. Contact the DB team if you think it's a database issue.

**[DO]** Document an upstream dependency explicitly:
> **Dependency:** `user-profile-service`
> **Endpoint Used:** `GET /v1/users/{id}/preferences`
> **SLA:** 99.99% availability, <50ms latency.
> **Fallback/Mitigation:** If `user-profile-service` times out or returns 5xx, the service falls back to a local LRU Redis cache. If cache misses, default to standard email preferences and queue a sync task.

**[DON'T]** Document an upstream dependency vaguely:
> **Dependency:** User Service. We make calls to it to get user info. If it goes down, our service might fail so make sure to check if they are having an outage.

**[DO]** Integrate documentation into the dev cycle:
> "I have added the new `/v2/receipts` endpoint to the code. I have also updated the Central Wiki API specifications, added the new dependencies to the Architecture Diagram, and added the specific `v2_timeout` alert to the On-Call Runbook."

**[DON'T]** Treat documentation as a secondary chore:
> "I've deployed the new `/v2/receipts` endpoint to production. I left some comments in the code explaining how it works. I'll update the main wiki documentation next sprint if I have time."