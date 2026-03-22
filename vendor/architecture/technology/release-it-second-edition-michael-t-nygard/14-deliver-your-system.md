@Domain
Activation conditions: Trigger these rules when the user requests assistance with system deployment, continuous integration/continuous delivery (CI/CD) pipelines, database migrations (SQL or NoSQL), static asset serving, API versioning, API payload parsing, or system architecture refactoring aimed at zero-downtime releases.

@Vocabulary
*   **Build Pipeline / Funnel**: An automated sequence spanning development to operations that treats every step (tests, linting, integration) as a filter looking for reasons to reject the build.
*   **Convergence**: A deployment paradigm where configuration management tools (e.g., Chef, Puppet) apply scripts to transition long-lived, mutable machines from an unknown state to a desired state.
*   **Immutable Infrastructure**: A deployment paradigm where machines or containers are never patched; instead, entirely new images are built, deployed, and the old ones destroyed.
*   **Undeployed Code**: Considered a liability and unfinished inventory carrying unknown bugs and deployment risks.
*   **Expansion Phase**: The first step of a zero-downtime relational database migration. It safely adds structures (tables, columns, views, triggers) without impacting currently running code.
*   **Contraction / Cleanup Phase**: The final step of a zero-downtime relational database migration. It drops deprecated structures and applies strict constraints (e.g., `NOT NULL`, foreign keys) ONLY after all application instances have been updated.
*   **Shim**: A temporary database trigger or application-level bridge that synchronizes data between old and new schema structures during a rolling deployment.
*   **Trickle, then Batch**: A schemaless (NoSQL) migration strategy where documents are updated on-the-fly as they are read by the application ("trickle"), followed by a background job to update untouched documents ("batch").
*   **Postel's Robustness Principle**: "Be conservative in what you do, be liberal in what you accept from others." The foundation of non-breaking API changes.
*   **Covariant Requests / Contravariant Responses**: The Liskov substitution principle applied to APIs. You can accept more than before, but never less. You can return more than before, but never less.
*   **Contract Tests**: Isolated tests owned by the calling service that verify strict adherence to a specific provider contract without requiring full end-to-end integration environments.

@Objectives
*   Achieve zero-downtime deployments by treating deployment mechanics as a core application feature.
*   Eliminate the "planned downtime" fallacy; users must never be disrupted or aware of system upgrades.
*   Decouple provider deployments from consumer upgrades to ensure team-scale autonomy.
*   Transform massive, risky, coordinated "big bang" releases into frequent, automated, low-risk deployments.
*   Prevent API changes from breaking downstream consumers.

@Guidelines

**Automated Deployments & Rollout**
*   The AI MUST script all deployment tasks. Never recommend or create manual "playbooks."
*   The AI MUST structure the build process as a pipeline/funnel that strictly rejects builds on unit test failure, static analysis failure, or integration test failure.
*   The AI MUST decouple process lifetime from session lifetime. The AI MUST NOT rely on in-memory session data that would be lost during instance restarts.
*   When designing instance startup, the AI MUST implement a health-check endpoint that reports the instance as "unavailable" until caches are warmed, connections are established, and the instance is fully ready to accept load from the load balancer.
*   The AI MUST implement graceful draining. When an instance is marked for update, it must signal the load balancer to stop sending new traffic while allowing existing requests to finish within a defined time limit.

**Database Migrations (Zero-Downtime)**
*   The AI MUST NEVER generate a single SQL script that alters schemas and applies constraints simultaneously.
*   The AI MUST separate relational database changes into two phases:
    1.  *Expansion*: Add tables, nullable columns, views, and sync triggers (shims).
    2.  *Contraction*: Drop old columns/tables, apply `NOT NULL`, apply foreign key constraints.
*   The AI MUST apply the Contraction phase ONLY after the new codebase has been fully rolled out.
*   For NoSQL databases, the AI MUST NOT write blocking batch migration scripts that prevent application startup. The AI MUST implement "Trickle, then Batch" translation pipelines in the application code to migrate documents on-read.

**Static Asset Versioning**
*   The AI MUST configure static assets (images, CSS, JS) with far-future cache expiration headers (e.g., 10 years).
*   The AI MUST implement cache-busting by embedding the version hash directly in the URL path or filename (e.g., `/a5019c6f/styles/app.css`).
*   The AI MUST NOT use query strings for cache-busting (e.g., `app.css?v=hash`), as this breaks side-by-side asset hosting during rolling deployments.

**API Versioning & Compatibility**
*   The AI MUST evaluate all API changes against Postel's Robustness Principle.
*   The AI MUST classify a change as **SAFE (Non-breaking)** if it:
    *   Requires a subset of previously required parameters.
    *   Accepts a superset of previously accepted parameters.
    *   Returns a superset of previously returned values.
    *   Enforces a subset of previously required constraints.
*   The AI MUST classify a change as **BREAKING** if it:
    *   Rejects previously accepted input.
    *   Adds required fields to the request.
    *   Removes guaranteed information from the response.
    *   Requires an increased level of authorization.
*   When a breaking API change is unavoidable, the AI MUST introduce a version discriminator in the URL (e.g., `/v2/applications`). The AI MUST NOT rely on generic media types or hidden headers unless strictly required by the user's framework.
*   The AI MUST maintain both old and new API versions side-by-side during the rollout. The AI MUST handle translation between old and new domain models at the controller layer to minimize business-logic duplication.
*   The AI MUST assume that an API's actual implementation—including bugs and edge-case acceptances—becomes the de facto specification once live. The AI MUST NOT "tighten" validation on existing public endpoints if it causes previously accepted requests to fail.

**Testing**
*   The AI MUST split external integration testing into two isolated Contract Tests:
    1.  *Outbound*: Ensure the client code generates requests that strictly match the provider's specification.
    2.  *Inbound*: Ensure the client code gracefully handles all valid responses (and errors) the provider is allowed to send.
*   The AI MUST generate test payloads that include missing optional fields and extra unknown fields to verify the application does not crash on unexpected inputs.

@Workflow
When tasked with creating a deployment strategy, database migration, or API update, the AI MUST follow this exact algorithm:

1.  **Analyze the Change Scope**:
    *   Identify if the task modifies application code, database schema, static assets, or API contracts.
2.  **Asset Cache-Busting Setup** (If assets modified):
    *   Rewrite asset references in the code to include commit SHAs or version hashes in the file path.
3.  **Database Migration Split** (If schema modified):
    *   Step 3a: Generate the Expansion migration (CREATE, ADD COLUMN, CREATE TRIGGER).
    *   Step 3b: Implement application-level shims/translators to handle read/writes across old and new formats.
    *   Step 3c: Generate the Contraction migration (DROP, ALTER COLUMN SET NOT NULL, ADD CONSTRAINT) to be run explicitly post-deployment.
4.  **API Compatibility Check** (If API modified):
    *   Evaluate against the "SAFE vs BREAKING" constraints.
    *   If BREAKING: Generate a new URL route (e.g., `/v2/`), route it to a new controller method, write adapter logic to translate old requests to the new domain model, and leave the `/v1/` route intact.
5.  **Rollout Orchestration Definition**:
    *   Ensure application exposes a `/health` endpoint reflecting internal readiness (caches, DB connections).
    *   Define the rolling batch update strategy (Canary -> Batch 1 -> Batch N).
6.  **Contract Test Generation**:
    *   Generate inbound and outbound contract tests for any modified API boundaries using randomized/generative payloads.

@Examples (Do's and Don'ts)

**Database Migrations**
*   [DO]: Add a nullable column `email_address` in Migration V1. Deploy the code that writes to both `email` and `email_address`. Wait for rollout. Run Migration V2 to drop `email` and make `email_address` NOT NULL.
*   [DON'T]: Create a single migration script that adds `email_address`, copies data, drops `email`, and applies `NOT NULL`. This will instantly break all running instances of the old codebase.

**Static Asset Versioning**
*   [DO]: `<link rel="stylesheet" href="/a5019c6f/styles/app.css" />` (Allows old and new CSS files to exist in separate directories simultaneously while old instances are still serving traffic).
*   [DON'T]: `<link rel="stylesheet" href="/styles/app.css?v=a5019c6f" />` (Overwrites the physical file; old instances will serve the old HTML pointing to the new CSS, breaking the layout).

**API Versioning**
*   [DO]: Create `/v2/borrower`. Keep `/v1/borrower` active. In the v1 controller, receive the old JSON, map it to the new `Borrower` internal object, call the business logic, and map the result back to the v1 JSON format.
*   [DON'T]: Add a required `creditScore` field to the existing `/borrower` endpoint. This breaks Postel's Robustness Principle and will instantly crash all downstream consumers who have not yet updated.

**API Payload Parsing**
*   [DO]: Parse incoming JSON gracefully, ignoring undocumented or extra fields sent by the consumer, and substitute sensible defaults for missing optional fields.
*   [DON'T]: Use strict deserializers that throw HTTP 500/400 errors if the consumer sends an unexpected payload field (e.g., Jackson's `FAIL_ON_UNKNOWN_PROPERTIES`).

**Integration Testing**
*   [DO]: Write a test that asserts: "Given the OpenAPI spec for Provider X, my client correctly serializes this edge-case data into a valid request."
*   [DON'T]: Write a test that spins up the entire application and Provider X's application, sends a request, and asserts against the database state of Provider X.