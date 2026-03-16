# @Domain
These rules MUST be triggered whenever the AI is tasked with generating, reviewing, or updating documentation for a microservice, when a user adds a new feature (API endpoint, dependency, or alert) that requires documentation updates, or when the AI is asked to perform an architecture review, production-readiness audit, or generate an on-call runbook. 

# @Vocabulary
*   **The Onion Principle**: Derived from a literary metaphor; the fundamental rule that developers must always provide helpful context and documentation to other developers and teams.
*   **Centralized Documentation**: A single, shared, and easily accessible location (usually an internal website or dedicated documentation repository) containing all knowledge about a microservice, separate from standard code repositories.
*   **Architecture Diagram**: A visual abstraction (which the AI will represent via Mermaid or PlantUML) detailing components, endpoints, request flows, dependencies, and databases.
*   **Onboarding and Development Guide**: A step-by-step manual allowing new developers to set up, develop, test, and deploy the service from scratch.
*   **On-Call Runbook**: A specific set of step-by-step instructions detailing how to triage, mitigate, and resolve every known alert, written simply enough for a sleepy developer to understand at 2 A.M.
*   **Architecture Review**: A scheduled evaluation where developers whiteboard and evaluate a service's architecture to find bottlenecks, points of failure, and outdated technologies.
*   **Production-Readiness Audit**: A process of quantifying a microservice's stability, reliability, scalability, fault tolerance, performance, monitoring, and documentation against a strict checklist.
*   **Production-Readiness Roadmap**: A step-by-step project plan detailing how to bring a service to a production-ready state, containing technical details, linked tickets, and assigned developers.

# @Objectives
*   Create and maintain a centralized repository of knowledge containing both hard facts and organizational understanding for every microservice.
*   Eliminate the technical debt caused by "black box" microservices by making documentation a mandatory, inseparable part of the development cycle.
*   Ensure that every microservice conforms to a strict 8-part documentation structure.
*   Facilitate microservice understanding at the developer, team, and organizational levels through standardized audits, reviews, and roadmaps.
*   Drive the automation of production-readiness checks to replace manual checklists.

# @Guidelines

## General Documentation Rules
*   The AI MUST NOT consider `README.md` files or inline code comments as sufficient microservice documentation. True documentation MUST be centralized.
*   The AI MUST automatically prompt the user to update the centralized documentation whenever a significant code change is made (e.g., adding an API endpoint, adding a dependency, or creating a new alert).
*   The AI MUST avoid jargon-heavy or overly technical language that obscures the basic function of the service. Documentation MUST be understandable by any developer, manager, or product manager.

## The 8 Mandatory Documentation Components
When generating or reviewing microservice documentation, the AI MUST ensure the presence of the following eight sections:
1.  **Description**: A 1-2 sentence summary of the service's role in the overall ecosystem.
2.  **Architecture Diagram**: A representation of the service, its endpoints, request flows, dependencies (upstream and downstream), and datastores.
3.  **Contact and On-Call Information**: Names, roles, and contact info for the team, plus exactly how to find the currently on-call engineer.
4.  **Links**: Direct URLs to the codebase repository, monitoring dashboards, the original RFC, and recent architecture review slides.
5.  **Onboarding and Development Guide**: Exact CLI commands and steps for checking out code, setting up the environment, starting the service, running tests (lint, unit, integration, end-to-end), and the deployment pipeline process.
6.  **Request Flows, Endpoints, and Dependencies**: A bulleted list of API endpoints (inputs/outputs), descriptions of request flows, and a list of dependencies with their SLAs and fallback mechanisms.
7.  **On-Call Runbooks**: Step-by-step triage, mitigation, and resolution steps for *every* alert, plus a general troubleshooting section.
8.  **FAQ**: Answers to common questions from client teams and internal team members.

## Runbook Constraints (The "2 A.M. Rule")
*   The AI MUST write on-call runbook instructions using simple, direct, imperative language.
*   The AI MUST structure every alert entry with four explicit sub-sections: `Alert Name/Description`, `Triage Steps`, `Mitigation Steps` (reducing impact), and `Resolution Steps` (fixing root cause).

## Microservice Understanding & Auditing
*   When conducting an Architecture Review, the AI MUST actively search for and highlight single points of failure (SPOFs), scalability bottlenecks, and missing fallback mechanisms.
*   When conducting a Production-Readiness Audit, the AI MUST output a definitive "Yes", "No", or "Partial" for every requirement.
*   The AI MUST translate any "No" or "Partial" audit results directly into a Production-Readiness Roadmap, formatting them as actionable tasks with placeholders for an assigned developer and a ticketing system link.

# @Workflow

## Workflow 1: Microservice Documentation Generation
1.  **Initialize**: Request the service's basic context (name, business purpose, team members, dependencies, API endpoints, alerts).
2.  **Draft Description**: Write a concise 1-2 sentence description.
3.  **Generate Architecture**: Create a Mermaid diagram showing clients -> the microservice -> datastores and downstream dependencies.
4.  **Populate Contact & Links**: Create placeholder sections for team contacts, on-call schedules, repo links, and dashboard links.
5.  **Build Onboarding Guide**: Write explicit setup, test, and deploy instructions based on the service's language/framework.
6.  **Document APIs & Dependencies**: List all endpoints with descriptions. List all dependencies and their fallback behaviors.
7.  **Draft Runbook**: For every provided alert, generate the Triage, Mitigate, and Resolve steps.
8.  **Draft FAQ**: Provide a template for Frequently Asked Questions.
9.  **Review**: Verify that all 8 mandatory sections are present and clearly formatted.

## Workflow 2: Updating Documentation During Code Changes
1.  **Detect Change**: Identify if the user has added an endpoint, dependency, or alert.
2.  **Prompt Update**: Alert the user: "Significant change detected. The Onion Principle requires documentation updates."
3.  **Execute Update**: Automatically append the new endpoint to the API list, the new dependency (and its fallback) to the Dependency list, or the new alert to the On-Call Runbook.

## Workflow 3: Production-Readiness Audit & Roadmap Creation
1.  **Audit Execution**: Evaluate the service against the 8 production-readiness standards (Stability, Reliability, Scalability, Fault Tolerance, Performance, Monitoring, Documentation, Understanding).
2.  **Gap Analysis**: Identify every requirement that is not fully met.
3.  **Roadmap Generation**: For each unmet requirement, generate a markdown task containing:
    *   **Unmet Requirement**: Describe what is missing.
    *   **Technical Details**: How to implement the fix.
    *   **Related Outages**: Placeholder for linked incident reports.
    *   **Ticket Link**: Placeholder for Jira/Linear link.
    *   **Assignee**: Placeholder for developer name.

# @Examples (Do's and Don'ts)

## Microservice Description
**[DO]**
**Description:**
After a customer places an order, `receipt-sender` sends a receipt to the customer via email.

**[DON'T]**
**Description:**
This service is a highly scalable Node.js application that consumes Kafka events, processes JSON payloads using a custom middleware, and pushes SMTP packets over an encrypted tunnel. *(Violates the rule against jargon-heavy descriptions; obscures the basic business function).*

## On-Call Runbook
**[DO]**
### Alert: High CPU Utilization on Redis Broker
**Description:** Redis message broker CPU has exceeded 85% for 5 minutes.
**Organizational Impact:** Severity 2. Delays in asynchronous task processing.
**Triage:**
1. Run `top` on the Redis host.
2. Check the `celery-worker` dashboard to see if worker nodes are down, causing the queue to back up.
**Mitigate:**
1. If Celery workers are down, scale the worker cluster up by 5 nodes using `kubectl scale deployment celery-worker --replicas=10`.
**Resolve:**
1. Investigate recent deployments to the worker code that may have introduced infinite loops or memory leaks.

**[DON'T]**
### Alert: Redis CPU High
If Redis gets too high, it might be because of Celery. Check the workers and fix the code so the queue drains. *(Violates the "2 A.M. rule"; lacks step-by-step CLI commands and clear separation of triage, mitigation, and resolution).*

## Documentation Storage
**[DO]**
AI Action: "I have updated the centralized documentation repository at `docs.internal.company.com/services/receipt-sender.md` to reflect the new API endpoint."

**[DON'T]**
AI Action: "I have added comments to `app.js` and updated the local `README.md`. Documentation is complete." *(Violates the rule that READMEs and inline comments are not sufficient for microservice documentation).*