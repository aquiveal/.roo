# @Domain

These rules MUST be triggered when the AI is tasked with any of the following:
- Designing database architectures, selecting datastores, or defining storage tier classifications.
- Writing or reviewing database migrations, schema changes, and deployment pipelines.
- Creating self-service tooling, checklists, or guardrails for Software Engineers (SWEs) interacting with databases.
- Drafting infrastructure-as-code (IaC), configuration management, or operational playbooks for database clusters.
- Defining service level metrics, Service-Level Objectives (SLOs), or Key Performance Indicators (KPIs) for database reliability and team collaboration.
- Implementing data validation pipelines, recovery APIs, or defining data-driven decision-making processes (Deming Cycle).
- Writing organizational or cultural documentation regarding database operations, cross-functional engineering, or incident post-mortems.

# @Vocabulary

- **DBRE (Database Reliability Engineer)**: A discipline focusing on database reliability, shifting from isolated database administration (DBA) to active cross-functional partnership and engineering enablement.
- **SRE (Site Reliability Engineer)**: An operational role focused on software engineering applied to operations; a partner to the DBRE in managing infrastructure and on-call shifts.
- **Self-Service Catalog**: A curated, approved list of tested storage architectures available for SWEs to deploy, categorized by tiers.
- **Tier 1 Storage**: Core services tested in production. Requires self-service patterns. Comes with strict Service-Level Agreements (SLAs), highly guaranteed SLOs (availability, latency, throughput, durability), and a 15-minute Sev1 response SLA.
- **Tier 2 Storage**: Non-critical services tested in production. Uses self-service patterns. Comes with reduced SLOs and a 30-minute Sev1 response SLA.
- **Tier 3 Storage**: Untested in production. Operates on a "best effort" escalation basis with no guaranteed SLOs. Fully supported by the SWE teams.
- **Heuristics**: Defined rules and checklists used to flag database changes/migrations as safe for automated deployment versus dangerous/ambiguous (requiring DBRE review).
- **Migration Patterns**: A documented, living database of safe execution methods for database changes, allowing SWEs to safely deploy updates.
- **Guardrails**: Implementations and constraints built into the deployment pipeline that prevent unsafe actions based on defined heuristics and patterns.
- **Deming Cycle**: The Plan-Do-Check-Act (PDCA) feedback loop requiring clear metrics, baselines, and skeptical analysis to drive data-driven decision making.
- **Data Validation Pipeline**: Automated processes designed and funded by SWEs to verify data integrity programmatically.
- **Recovery API**: Programmatic interfaces built by SWEs to automate the recovery of data, reducing reliance on manual DBRE intervention.
- **Blameless Post-mortem**: A culturally necessary review of incidents or migrations (successful and unsuccessful) focused on systemic improvements rather than human error.

# @Objectives

- Shift the paradigm of database management from isolated gatekeeping (legacy DBA) to cross-functional enablement and automation (DBRE).
- Architect datastores strictly according to predefined Tier classifications (Tier 1, 2, or 3) with explicit SLAs, SLOs, and operational expectations.
- Empower SWEs with self-service tooling, migration patterns, and heuristics to safely manage their own database changes without becoming bottlenecked by DBREs.
- Enforce strict, metric-backed, data-driven decision-making using the Deming Cycle for all database changes and architectural shifts.
- Embed data integrity and recoverability directly into application code bases via validation pipelines and recovery APIs, distributing the responsibility across the engineering organization.
- Measure the success of the DBRE culture using explicitly tracked metrics (e.g., pairing hours, non-DBRE on-call shifts, migration success rates).

# @Guidelines

## Architectural Process & Datastore Selection
- The AI MUST NOT propose a datastore architecture without explicitly classifying it as Tier 1, Tier 2, or Tier 3 Storage.
- For every proposed datastore, the AI MUST define the operational SLA, the Sev1 response SLA (15-min for Tier 1, 30-min for Tier 2, Best Effort for Tier 3), and the expected SLOs (Availability, Latency, Throughput, Durability).
- The AI MUST generate architectural design documents that detail best practices, trade-offs, and operational patterns for any chosen datastore to build organizational mindshare.
- The AI MUST define post-mortem metrics for architecture, specifically:
  - Number of projects using DBRE approved templates.
  - Storage engines used and deployed.
  - Hours of DBRE work per phase.
  - Availability, throughput, and latency metrics grouped by storage tier.

## Database Development & SWE Enablement
- The AI MUST generate checklists for SWEs covering data models, query optimization, and feature usage. These checklists MUST be designed to automatically flag user stories that require manual DBRE review.
- When generating application-to-database integration code, the AI MUST design the code to be safely deployable using predefined migration patterns.
- The AI MUST define team integration metrics, including:
  - Development pairing hours between SWEs and DBREs.
  - Feature metrics (latency/durability) mapped to DBRE involvement.
  - Count of on-call shifts pairing SWEs with SREs.

## Production Migrations & Guardrails
- The AI MUST classify every database migration using strict heuristics. Changes MUST be categorized as either "Safe for Automation" (matches a known Migration Pattern) or "Requires DBRE Review" (ambiguous, high-risk, or lacks a pattern).
- The AI MUST provide explicit fallback plans and rollback scripts for every database change.
- The AI MUST design review board processes into migration workflows, enabling post-mortems of both successful and unsuccessful changes to iterate on heuristics.
- The AI MUST output migration tracking metrics, including:
  - Count of migrations requiring DBRE intervention vs. automated migrations.
  - Failure/success rates and the corresponding organizational impact.

## Infrastructure Design & Deployment
- The AI MUST define all database deployments, configuration files, and scripts using version-controlled Infrastructure as Code (IaC).
- The AI MUST construct operational playbooks that are simple, tested, and reliable enough to be executed by non-DBREs (Ops/SWEs) during on-call shifts.
- The AI MUST ensure infrastructure test suites cover configuration correctness, security, load, and data integrity/replication.
- The AI MUST define infrastructure operational metrics, including:
  - Count of components managed via configuration management/orchestration.
  - Count of successful/failed provisions.
  - Mean Time to Restore (MTTR) managed by non-DBREs.
  - Escalation counts to DBREs.

## Data-Driven Decision Making & Data Integrity
- The AI MUST apply the Deming Cycle (Plan, Do, Check, Act) to all proposed changes. Every change MUST define baseline metrics to be gathered prior to the change, and the criteria for post-change analysis.
- The AI MUST NOT rely solely on manual DBRE effort for data integrity. The AI MUST design and propose Data Validation Pipelines to automatically verify data constraints and consistency.
- The AI MUST design Recovery APIs that allow automated or SWE-triggered data recovery, tracking any manual recovery efforts to justify the investment in these APIs.

# @Workflow

When executing a task related to database engineering, deployment, or organizational design, the AI MUST follow this exact algorithmic process:

1. **Phase 1: Tier and Architecture Definition**
   - Identify the datastore being utilized or proposed.
   - Categorize the datastore into Tier 1, Tier 2, or Tier 3.
   - Explicitly output the SLA, Sev1 response time, and SLO guarantees based on the selected tier.

2. **Phase 2: SWE Enablement & Heuristics Creation**
   - Analyze the proposed database change or application logic.
   - Generate a checklist for the SWE to validate the data model and queries.
   - Apply heuristics to the change: determine if it matches a known "Migration Pattern" (Safe) or if it requires human "DBRE Review" (Ambiguous/Dangerous).

3. **Phase 3: Infrastructure and Guardrail Implementation**
   - Write the necessary Infrastructure as Code (IaC) to deploy or modify the datastore.
   - Embed guardrails into the deployment pipeline to block changes that fail the heuristics check.
   - Generate an operational playbook designed for a non-DBRE (SRE/Ops) to execute safely during an on-call shift.

4. **Phase 4: Deming Cycle & Measurement Setup**
   - Define the **Plan**: State the goal of the change.
   - Define the **Do**: Detail the execution steps.
   - Define the **Check**: Output the exact baseline metrics to capture before the change and what metrics to monitor post-change (e.g., latency, throughput, pairing hours, escalation counts).
   - Define the **Act**: Specify the rollback or adjustment plan if the "Check" phase fails.

5. **Phase 5: Data Integrity & Recovery Strategy**
   - Design a Data Validation Pipeline step to continuously verify the integrity of the data affected by the task.
   - Outline a Recovery API endpoint or automated script that SWEs can trigger to restore this data without escalating to a DBRE.

# @Examples (Do's and Don'ts)

### Architecture Classification
- **[DO]** "Deploying PostgreSQL for the core payment service. Classification: Tier 1 Storage. SLA: 15-minute Sev1 response. SLOs: 99.99% Availability, <10ms Latency. Requires strict self-service migration patterns."
- **[DON'T]** "Deploying PostgreSQL for the payment service. Ensure it has plenty of RAM and is backed up nightly." (Fails to use Tier classifications, SLAs, and SLO tracking).

### Migration Heuristics & Guardrails
- **[DO]** "Migration: Adding a new nullable column. Heuristic Check: Safe. Matches Migration Pattern #4 (Non-blocking schema addition). Guardrail: Auto-approve for CI/CD pipeline. Rollback script provided."
- **[DON'T]** "Migration: Altering table to change column types. Run this SQL command against production." (Fails to apply heuristics, fails to evaluate if it requires DBRE review, lacks rollback).

### Data-Driven Decision Making (Deming Cycle)
- **[DO]** "Applying index optimization. Plan: Reduce read latency on the orders table. Do: Deploy concurrent index build via IaC. Check: Gather baseline latency; post-deployment, verify P99 latency drops below 50ms without degrading write throughput. Act: If write latency spikes >100ms, execute the provided index drop script."
- **[DON'T]** "Adding an index to make the query faster. It should improve performance." (Fails to establish the Deming Cycle, lacks baselines, and lacks a rollback plan).

### Data Integrity & Recovery
- **[DO]** "To protect against application-level logical corruption, implementing a scheduled Data Validation Pipeline that compares foreign key referential states against the event log. Exposing a `/api/v1/admin/recover_order` endpoint for SWEs to trigger programmatic state reconstruction."
- **[DON'T]** "If the application accidentally deletes user data, page the DBRE to manually restore the rows from the nightly backup." (Fails to shift recovery responsibility to SWEs via Recovery APIs and validation pipelines).

### Defining Organizational Metrics
- **[DO]** "To measure the success of this DBRE initiative, we will track: 1. DBRE/SWE pairing hours per week. 2. Percentage of database migrations executed automatically vs. those requiring manual DBRE review. 3. Number of on-call incidents resolved by non-DBREs."
- **[DON'T]** "We will track database uptime and query speed to see if the DBREs are doing a good job." (Fails to track cross-functional organizational enablement metrics).