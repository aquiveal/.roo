# @Domain
These rules apply to any tasks involving the design, configuration, or implementation of continuous integration/continuous deployment (CI/CD) pipelines, infrastructure as code (IaC), containerization, database migrations, web asset serving, and deployment automation scripts. The AI MUST activate these rules whenever a user requests help deploying software, building deployment architectures, managing schema changes for production, or configuring load-balanced rollouts.

# @Vocabulary
- **Machine**: A configurable operating system instance, which may be a physical host, a virtual machine (VM), or a container.
- **Service**: A callable interface for others to use, always composed of redundant copies of software running on multiple machines.
- **Build Pipeline**: A series of automated stages (a "funnel") that actively looks for reasons to reject a build (linting, unit tests, integration tests, trial deployment).
- **Convergence**: A configuration management strategy (e.g., Chef, Puppet) where a tool examines the current state of a mutable machine and applies scripts to match the desired state. Used primarily for "pets" or physical data centers.
- **Immutable Infrastructure**: A deployment strategy where existing machines are never patched or updated. Instead, a new image (container or AMI) is built from a known base, deployed, and the old machine is destroyed. Used primarily for "cattle" or cloud environments.
- **Canary Deployment**: The practice of rolling out a new release to a single instance or a very small subset of machines first, pausing to evaluate its health before continuing the rollout.
- **Microscopic Deployment Time**: The sequence and duration of updating a single instance: Prepare, Drain, Apply, and Warm-up.
- **Macroscopic Deployment Time**: The sequence and duration of the entire rollout across all clusters and machines.
- **Expansion Phase**: The first phase of a database migration that adds elements (tables, columns, views) in a strictly backward-compatible way.
- **Contraction (Cleanup) Phase**: The final phase of a database migration, executed *after* all code is updated, which removes old elements and applies strict constraints (e.g., `NOT NULL`, foreign keys).
- **Shim**: A temporary bridge (such as a database trigger) used during a rolling deployment to synchronize data between an old schema and a new schema while both application versions are running simultaneously.
- **Trickle, Then Batch**: A data migration strategy for schemaless databases where documents are up-converted dynamically upon being read by the application (trickle), followed later by a background process to update untouched documents (batch).
- **Cache-Busting**: The practice of forcing browsers and CDNs to fetch new static assets by embedding a version identifier in the asset's URL.

# @Objectives
- Achieve **Zero-Downtime Deployments** by treating deployment as a first-class feature of the software design.
- Eliminate the concept of "planned downtime"; deployments MUST be invisible to end users.
- Minimize the liability of undeployed code through continuous deployment and small, frequent releases.
- Ensure the application assists in its own deployment by maintaining backward compatibility during the rollout window.
- Automate the rejection of bad builds as early as possible in the pipeline.

# @Guidelines

## General Architecture & Infrastructure
- The AI MUST design deployment pipelines as funnels that actively attempt to reject builds through compilation, static analysis, unit testing, integration testing, and trial deployments.
- The AI MUST prefer Immutable Infrastructure patterns for cloud and container environments. Do not write scripts to patch running containers or cloud VMs.
- The AI MUST decouple session data from the application process lifetime (e.g., use an external Redis cache) to prevent data loss when an instance is killed during deployment.

## Rollout & Routing
- The AI MUST implement rolling updates in batches (e.g., Alpha, Bravo, Charlie).
- The AI MUST start every rollout with a Canary group and mandate a pause/evaluation step (automated or manual) before proceeding.
- The AI MUST configure load balancers to respect application health checks. 
- The AI MUST implement a "Drain" phase during deployment: toggle the health check to failing so the load balancer stops sending new requests, but allow existing requests to complete before terminating the process.
- The AI MUST account for application "Warm-up" time. An instance MUST NOT return a passing health check until caches are loaded, JIT is warmed up, and DB connections are established.

## Relational Database Schemata
- The AI MUST use a programmatic migrations framework (e.g., Liquibase, Flyway, Alembic) rather than raw SQL scripts executed manually.
- The AI MUST split schema changes into two distinct deployments: 
  1. **Expansion**: Add new tables, nullable columns, or views. This MUST be fully backward-compatible with the currently running application.
  2. **Contraction (Cleanup)**: Drop old tables/columns, add `NOT NULL` constraints, and add foreign key constraints. This MUST ONLY occur after the new application code is running on 100% of the instances.
- The AI MUST utilize Shims (e.g., database triggers) if data needs to be duplicated or kept in sync between old and new schema structures while both versions of the application are running simultaneously.
- The AI MUST mandate that schema changes be tested against a realistic, messy copy of production data, not just clean QA data.
- The AI MUST configure the CI/CD pipeline to parse schema changes as data and fail the build if mechanical errors are detected (e.g., failing to add an index on a newly created foreign key).

## Schemaless Database Migrations
- The AI MUST NOT implement synchronous, full-database batch migrations during deployment for schemaless databases, as this causes downtime.
- The AI MUST implement the **Trickle, Then Batch** pattern:
  1. Add conditional logic in the application to intercept old document versions upon read.
  2. Translate the old document to the new schema in memory, then write it back to the database.
  3. Provide a separate background batch script to migrate stale/untouched documents asynchronously after the deployment.
  4. Schedule a future cleanup task to remove the conditional translation logic.

## Web Assets
- The AI MUST apply far-future expiration headers (e.g., 10 years) to all static web assets.
- The AI MUST implement cache-busting by embedding the version identifier (e.g., Git commit SHA) directly into the URL path or filename (e.g., `/a5019c6f/styles/app.css`).
- The AI MUST NOT use query strings for cache-busting (e.g., `app.css?v=123`), as this is less reliable across various proxies and prevents clean directory separation of versions.
- The AI MUST ensure static assets are served from a separate cluster/CDN, OR ensure session affinity is used, OR pre-deploy all assets to all hosts before rolling out the new HTML templates that reference them.

# @Workflow
When tasked with designing a deployment process or writing deployment code, the AI MUST follow this algorithmic process:

1. **Pipeline Construction**:
   - Define the CI stages: lint, unit test, compile/build.
   - Define the CD stages: trial deployment, integration tests.
   - Designate the artifact as an immutable image (Docker/AMI) or a convergent script package.
2. **Schema Separation**:
   - Analyze required database changes.
   - Separate changes into an `Expansion` migration script (safe to run before code deployment) and a `Contraction` migration script (safe to run only after full code deployment).
   - Generate application code to handle both database states if necessary.
3. **Asset Management**:
   - Ensure the build process injects a unique SHA/hash into the file paths of all static assets.
   - Configure the web server/CDN to serve these assets with far-future cache headers.
4. **Microscopic Deployment Sequencing**:
   - Script the shutdown sequence: toggle health check -> wait for connection drain -> terminate process.
   - Script the startup sequence: boot process -> warm up cache/connections -> toggle health check to passing.
5. **Macroscopic Rollout Sequencing**:
   - Define the Canary batch deployment.
   - Define the rolling batch deployments for the rest of the cluster.
6. **Cleanup**:
   - Script the execution of the `Contraction` database migrations.
   - Identify and remove old feature toggles and temporary data shims.

# @Examples (Do's and Don'ts)

## Relational Database Migrations
**[DO]** Split a column renaming or splitting operation into two backward-compatible phases.
```sql
-- Deployment 1: Expansion (Run BEFORE code rollout)
ALTER TABLE users ADD COLUMN first_name VARCHAR(255);
ALTER TABLE users ADD COLUMN last_name VARCHAR(255);
-- Shim to keep data in sync while old code writes to 'full_name'
CREATE TRIGGER sync_names BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION split_full_name();

-- ... Code Rollout Happens Here (Old and New code running simultaneously) ...

-- Deployment 2: Contraction (Run AFTER code rollout is 100% complete)
DROP TRIGGER sync_names ON users;
ALTER TABLE users DROP COLUMN full_name;
ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
```

**[DON'T]** Apply breaking schema changes in a single synchronous migration during deployment.
```sql
-- ANTI-PATTERN: Causes downtime. Old application instances will crash immediately.
ALTER TABLE users RENAME COLUMN full_name TO first_name;
ALTER TABLE users ADD COLUMN last_name VARCHAR(255) NOT NULL;
```

## Schemaless Database Migrations (Trickle, Then Batch)
**[DO]** Handle document upgrades lazily within the application read path.
```javascript
// Good Approach: Trickle migration on read
async function getUserProfile(userId) {
  let profile = await db.collection('profiles').findOne({ _id: userId });
  
  if (profile.schemaVersion === 1) {
    // Up-convert on the fly
    profile = translateV1toV2(profile);
    // Write back to DB so it doesn't need conversion next time
    await db.collection('profiles').updateOne({ _id: userId }, { $set: profile });
  }
  
  return profile;
}
```

**[DON'T]** Run a massive blocking map-reduce migration script before starting the application.
```javascript
// ANTI-PATTERN: Locks the deployment until millions of records are updated.
await db.collection('profiles').updateMany(
  { schemaVersion: 1 },
  { $set: { "new_structure": true } } // Blocks startup
);
```

## Web Asset Cache-Busting
**[DO]** Bake the version hash into the file path.
```html
<!-- Good Approach: Version in the path, easily hosted in parallel directories -->
<link rel="stylesheet" href="/assets/a5019c6f/css/app.css" />
<script src="/assets/a5019c6f/js/main.js"></script>
```

**[DON'T]** Use query parameters for cache busting.
```html
<!-- ANTI-PATTERN: Proxies may strip query strings; mixes old and new files in one directory -->
<link rel="stylesheet" href="/assets/css/app.css?v=a5019c6f" />
<script src="/assets/js/main.js?v=a5019c6f"></script>
```

## Instance Draining
**[DO]** Expose a health endpoint that can be toggled to drain traffic before shutdown.
```javascript
// Good Approach: Graceful drain
let isShuttingDown = false;

app.get('/health', (req, res) => {
  if (isShuttingDown) {
    return res.status(503).send('Draining'); // Load balancer stops sending traffic
  }
  return res.status(200).send('OK');
});

process.on('SIGTERM', () => {
  isShuttingDown = true;
  // Wait for existing requests to finish (e.g., 30 seconds) before closing server
  setTimeout(() => server.close(), 30000); 
});
```

**[DON'T]** Force-kill the process immediately.
```javascript
// ANTI-PATTERN: Drops active user connections immediately
process.on('SIGTERM', () => {
  process.exit(0); 
});
```