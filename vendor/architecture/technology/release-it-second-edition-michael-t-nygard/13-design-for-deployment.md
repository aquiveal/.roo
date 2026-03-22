# @Domain
These rules MUST activate whenever the AI is performing tasks related to software deployment, continuous integration/continuous deployment (CI/CD) pipelines, database schema migrations, application state management, web asset delivery, or infrastructure configuration (e.g., Docker, Terraform, Chef, Ansible, Kubernetes). These rules govern the architectural design and coding standards required to achieve zero-downtime, continuous deployments.

# @Vocabulary
- **Deployment as a Feature**: The architectural principle that deployment is an integral system state ("during") that must be designed for, not just a transition between "before" and "after".
- **Convergence (Mutable Infrastructure)**: A deployment strategy where configuration management tools (e.g., Chef, Puppet) alter the state of long-lived, running machines to match a desired configuration.
- **Immutable Infrastructure**: A deployment strategy where machines or containers are never modified after creation. New versions are deployed by building a new image and discarding the old one.
- **Build Pipeline**: A series of automated stages spanning development and operations that acts as a funnel to reject bad builds (compilation, static analysis, automated testing, staging) before production rollout.
- **Microscopic Time Scale**: The sequence of events required to update a single machine/instance: Prepare, Drain Activity, Apply Changes, and Warm-up.
- **Macroscopic Time Scale**: The sequence of events required to roll out a release across an entire fleet of instances (e.g., Canary group, then sequential batches).
- **Expansion Phase**: The first stage of a database schema migration consisting strictly of additive, non-breaking changes (adding tables, views, nullable columns).
- **Shims**: Database triggers or intermediate application code that bridges old and new data structures, keeping both synchronized while old and new application versions run simultaneously.
- **Contraction (Cleanup) Phase**: The final stage of a database schema migration, executing destructive changes and strict validations (dropping tables, applying NOT NULL or foreign key constraints) ONLY after all instances are running the new application code.
- **Trickle, Then Batch**: A schemaless database migration strategy where application code handles and updates old document formats on-read (trickle), followed by a scheduled background migration for untouched documents (batch).
- **Cache Busting**: Techniques to force browsers and proxies to fetch new versions of static web assets (images, CSS, JS) by altering the asset's URL or filename.
- **Canary Deploy**: Pushing new code to a small, isolated subset of instances and monitoring their health/metrics before continuing the rollout to the rest of the fleet.

# @Objectives
- The AI MUST design all systems to support zero-downtime, continuous deployments.
- The AI MUST treat the act of deployment as a supported operational state where multiple versions of the application and database schema will coexist.
- The AI MUST prevent the introduction of breaking database schema changes during application rollouts.
- The AI MUST enforce immutable infrastructure paradigms wherever applicable to ensure repeatable, pristine deployment states.
- The AI MUST structure web asset delivery to prevent version mismatch errors when user traffic spans mixed-version backend instances.

# @Guidelines

## Infrastructure and Build Pipelines
- **Immutable Preference**: When scaffolding infrastructure, the AI MUST default to immutable infrastructure patterns (e.g., building new Docker images or AMIs) rather than writing convergence scripts for mutable instances, unless explicitly directed otherwise.
- **Fail the Build**: The AI MUST implement strict checks in the CI/CD pipeline definition that reject builds for mechanical errors. Specifically, the AI MUST configure pipelines to statically analyze database migrations (e.g., rejecting any migration that adds a foreign key without a corresponding index).
- **Decoupled Session State**: The AI MUST NEVER store critical session data in-memory on the application instance. Session state MUST be stored in external caches (e.g., Redis) so instances can be destroyed and recreated without data loss.

## Relational Database Migrations
- **Phase Separation**: The AI MUST separate schema modifications into distinct Expansion and Contraction migration files.
- **Safe Expansions**: During the Expansion phase, the AI MUST ONLY generate migrations that add tables, add views, add nullable columns, or add triggers.
- **No Early Constraints**: The AI MUST NEVER add `NOT NULL` constraints, unique constraints, or foreign key constraints to active tables during the Expansion phase. These MUST be deferred to the Contraction phase after the new code is fully deployed.
- **Shim Generation**: If a table is split or fundamentally altered, the AI MUST generate database triggers (Shims) to automatically synchronize inserts/updates between the old and new tables to support instances running the old codebase.
- **Code-Based Migrations**: The AI MUST define migrations using a programmatic DSL/framework (e.g., Liquibase, ActiveRecord, Alembic) rather than raw SQL DDL, to allow pipeline analysis and automated rollbacks.

## Schemaless/NoSQL Migrations
- **Trickle Migrations**: The AI MUST implement backwards-compatible read/write logic in the application code. When fetching a document, the code MUST detect the schema version, translate/migrate the document in memory, and save the updated version back to the database.
- **Pipeline Translation**: If supporting multiple historical versions, the AI MUST structure the document reading code as a translation pipeline that upgrades documents step-by-step through historical versions.

## Application Health and Draining
- **Robust Health Checks**: The AI MUST implement a dedicated health check endpoint (e.g., `/health`) that returns the application version, runtime version, host IP, and the status of connection pools, caches, and circuit breakers.
- **Load Balancer Toggles**: The AI MUST allow the health check to be administratively toggled to `false` (returning HTTP 503) so the load balancer stops sending new requests, allowing the instance to gracefully drain existing activity before shutdown.
- **Warm-up Awareness**: The AI MUST configure applications to report as "unavailable" to the load balancer until all caches are warmed up and database connection pools are fully established.

## Web Asset Delivery
- **Far-Future Caching**: The AI MUST configure static assets to be served with far-future `Cache-Control` headers (e.g., 10 years).
- **Structural Cache Busting**: The AI MUST embed version identifiers (e.g., Git commit SHA) directly into the directory path or filename of static assets.
- **No Query-String Versioning**: The AI MUST NEVER use query strings for cache busting static assets, as intermediate proxies frequently ignore query strings when caching.
- **Asset Coexistence**: The AI MUST ensure that both old and new web assets are available on the server simultaneously during deployment to prevent 404 errors for users interacting with an older instance of the application.

# @Workflow
When tasked with creating a feature that requires infrastructure, application, and database schema changes, the AI MUST execute the following deployment-safe algorithm:

1. **Design the Expansion Phase Migration**:
   - Analyze the required data changes.
   - Generate a migration script that adds new tables, columns (nullable), and views.
   - Generate database triggers (Shims) to sync data from the old schema structure to the new structure, and vice versa.
2. **Implement Application Logic (Trickle Phase)**:
   - Write application code that reads from/writes to the new schema structure.
   - If using NoSQL, write application-level translation pipelines to detect old document formats and upgrade them on-read.
   - Update the `/health` endpoint to reflect the status of any new dependencies.
3. **Configure Web Assets**:
   - Inject the current build version/SHA into the file path of any new static assets.
   - Ensure the build pipeline outputs these assets alongside, not overwriting, previous assets.
4. **Define the Rollout Strategy (Micro/Macro)**:
   - Provide configurations for the load balancer to target a Canary group.
   - Define the drain procedure (toggle health check to fail, wait for active threads to complete).
   - Define the warm-up procedure (load caches before passing health checks).
5. **Design the Contraction/Cleanup Phase Migration**:
   - Generate a separate, subsequent migration script to drop the Shims (triggers).
   - Drop deprecated tables/columns.
   - Apply `NOT NULL` constraints and foreign key constraints to the new columns.
   - Explicitly instruct the user that this cleanup migration MUST ONLY run after the new application code is 100% deployed and stable.

# @Examples (Do's and Don'ts)

## Relational Database Schema Changes
- **[DO]** Split a column change into multiple deployments. Deployment 1: Add new nullable column `first_name` and a database trigger to populate it from `full_name`. Deployment 2 (Application): Deploy code that writes to both columns but reads from `first_name`. Deployment 3 (Cleanup): Add `NOT NULL` to `first_name` and drop `full_name`.
- **[DON'T]** Execute `ALTER TABLE users RENAME COLUMN full_name TO first_name;` in a single migration. (This will immediately break all running instances of the old application code during the rollout window).

## Web Asset Cache Busting
- **[DO]** Structure asset URLs by embedding the version hash into the path: `<link rel="stylesheet" href="/a5019c6f/styles/app.css" />`
- **[DON'T]** Append version hashes to the query string, which may be ignored by proxies: `<link rel="stylesheet" href="/styles/app.css?v=a5019c6f" />`
- **[DON'T]** Use server-side rewrite rules that strip the version portion to point to a single `app.css` file, as this overwrites the old asset while old application instances are still attempting to serve it.

## Schemaless Database Migrations
- **[DO]** Implement a translation layer in the data access code: `if doc.version == 1 { doc = upgrade_to_v2(doc); save(doc); }`
- **[DON'T]** Write a batch script to migrate millions of NoSQL documents during the deployment window, causing extended planned downtime.

## Build Pipeline CI/CD Checks
- **[DO]** Configure CI tools to statically analyze schema migrations for missing foreign-key indexes before allowing the build to pass.
- **[DON'T]** Rely solely on manual DBA reviews to catch mechanical schema performance issues.

## Instance Draining
- **[DO]** Configure the application to intercept a `SIGTERM`, set an internal `is_shutting_down = true` flag (causing `/health` to return 503), and wait for active request threads to finish before exiting.
- **[DON'T]** Terminate instances abruptly without removing them from the load balancer pool or waiting for in-flight requests to complete.