@Domain
These rules MUST be triggered whenever the AI is tasked with generating, reviewing, or modifying database schemas, database migration scripts, data access layer (DAL) code, database continuous integration/continuous deployment (CI/CD) pipelines, rollback scripts, or architectural design documentation relating to database changes.

@Vocabulary
- **DBRE (Database Reliability Engineer):** An engineering role focused on database reliability, serving as an educator, collaborator, and enabler for software engineers rather than a deployment gatekeeper.
- **SWE:** Software Engineer.
- **VCS (Version Control System):** The single source of truth where ALL database artifacts must be checked in (e.g., Git).
- **Migration:** An incremental, coded database change (e.g., altering a table, adding metadata) mapped to a specific sequence or version number.
- **DAO (Data Access Object):** A centralized abstraction layer encapsulating database access code to simplify testing and integration.
- **Soft Delete:** Flagging a row as delete-able rather than issuing an immediate, resource-intensive `DELETE` statement.
- **Rolling Migration:** Incrementally applying database changes across each node in a cluster (taking a node out of service, applying the change, and returning it to service).
- **Online Schema Change:** Applying schema changes without locking the table for read/write access (e.g., via triggers and table renames, such as Percona Toolkit).

@Objectives
- Transform the database change process from a manual, gatekept bottleneck into an automated, developer-empowered pipeline.
- Ensure all database changes, configurations, and test datasets are fully version-controlled, tested, and idempotent.
- Prevent production downtime, object locking, resource saturation, and replication stalls during database migrations.
- Facilitate cross-functional education by providing context, architectural history, and best-practice rationales alongside any database code modifications.

@Guidelines

**Collaboration and Education**
- The AI MUST provide architectural context and explanations ("the why") when proposing database changes to foster SWE autonomy.
- The AI MUST format database design documents using the exact following sections: Executive summary, Goals and anti-goals, Background, Design, Constraints, Alternatives, and Launch Details.
- The AI MUST recommend standardized tooling (e.g., Etsy's Schemanator, Percona Toolkit, SQL tuning suites) when appropriate.

**Version Control and Integration Prerequisites**
- The AI MUST ensure ALL database components are version-controlled. This includes DDL, triggers, stored procedures, views, configurations, sample test datasets, and data cleanup scripts.
- The AI MUST sequence all database migrations using incrementing integers or clear version numbers.
- The AI MUST generate or define three distinct tiers of test data for CI pipelines:
  1. Metadata (lookup tables, IDs).
  2. Functional data (small datasets for quick integration tests).
  3. Large, production-like datasets (scrubbed/anonymized to prevent PII exposure).

**Development and Testing Practices**
- The AI MUST flag and reject the use of `SELECT *` to prevent network packet overfilling and code breakage upon schema evolution. Explicit column selection is mandatory.
- The AI MUST encourage encapsulating database queries within DAOs or APIs to simplify testing primitives.
- The AI MUST formulate tests spanning four categories for database CI:
  1. **Post-Commit Tests:** Quick, automated feedback using minimal datasets.
  2. **Full Dataset Tests:** Asynchronous tests against scrubbed production data to check load, execution plans, and latency impact.
  3. **Downstream Tests:** Validating event workflows, ETL jobs, and batch jobs dependent on the database.
  4. **Operational Tests:** Validating backup/recovery, failover, cluster configurations, and security.

**Pre-Build Validation Rules**
- The AI MUST perform heuristic analysis on proposed migrations and FLAG the following as unsafe for automated deployment:
  - `UPDATE` or `DELETE` statements lacking a `WHERE` clause.
  - Large numbers of rows impacted by a single statement.
  - `ALTER` statements on massive or highly active tables.
  - New columns containing `DEFAULT` values (which lock the table to update all existing rows).
  - Foreign keys lacking corresponding indexes.
  - Structural changes to sensitive/PII tables.

**Deployment and Migration Patterns**
- **Locking Operations:** For adding columns or modifying structures, the AI MUST recommend adding an empty column and using lazy updating in application code, OR using online schema change tools (e.g., Percona Toolkit), OR utilizing rolling migrations.
- **High Resource Operations:** For massive data modifications, the AI MUST throttle/batch the updates. For massive deletions, the AI MUST recommend soft deletes processed asynchronously or table/partition dropping to avoid massive undo I/O.
- **Rollbacks:** The AI MUST ALWAYS generate a corresponding rollback script for every migration. Rollback scripts MUST NOT use `DROP TABLE` (which permanently destroys data); instead, they MUST use `RENAME TABLE` to preserve data for potential recovery.

@Workflow
When tasked with creating or reviewing a database migration or access code, the AI MUST follow this exact algorithm:

1. **Impact Analysis & Heuristic Check:** Scan the provided SQL/code against the Pre-Build Validation Rules. Check for `SELECT *`, missing `WHERE` clauses, and potential locking operations.
2. **Pattern Selection:** Based on the impact, select the appropriate Migration Pattern (e.g., Throttled Batching, Soft Deletion, Online Schema Change, Rolling Migration).
3. **Artifact Generation:** 
   - Generate the strictly-versioned Forward Migration script.
   - Generate the safe Rollback script (using `RENAME` instead of `DROP`).
4. **Test Strategy Formulation:** Output the required test steps covering Post-Commit, Full Dataset, Downstream, and Operational tests. Ensure the test data requirements (Metadata, Functional, Scrubbed) are defined.
5. **Educational Context:** Output a brief "DBRE Architectural Context" block explaining *why* the specific pattern was chosen to educate the SWE.

@Examples (Do's and Don'ts)

**Example 1: Adding a Column with a Default Value (Locking Operation)**
- [DO]: Create a migration that adds an empty column without a default. Update the application to write the default value on new inserts, and lazily update existing rows via a background script. Alternatively, generate a script utilizing Percona Toolkit's `pt-online-schema-change`.
- [DON'T]: `ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT true;` (This locks the entire table to rewrite every single row, causing production downtime).

**Example 2: Mass Deletion of Expired Data (High Resource Operation)**
- [DO]: Add an `is_deleted` boolean or `deleted_at` timestamp (Soft Delete) and filter out these rows in the DAO. Run a throttled, batched background job to physically delete the rows during off-peak hours, or drop an entire time-based partition.
- [DON'T]: `DELETE FROM sessions WHERE last_active < '2023-01-01';` (This saturates disk I/O, floods the transaction log, and causes replication stalls).

**Example 3: Query Efficiency**
- [DO]: `SELECT id, username, email FROM users WHERE status = 'active';`
- [DON'T]: `SELECT * FROM users WHERE status = 'active';` (This wastes TCP bandwidth and breaks application mappings if a new column is added).

**Example 4: Generating Rollback Scripts**
- [DO]: `ALTER TABLE new_feature_table RENAME TO deprecated_new_feature_table;`
- [DON'T]: `DROP TABLE new_feature_table;` (This destroys any data that might have been written during the failed deployment, making forensic recovery impossible).

**Example 5: Updating Data**
- [DO]: `UPDATE inventory SET stock = stock - 1 WHERE item_id = 12345;`
- [DON'T]: `UPDATE inventory SET stock = stock - 1;` (The AI must strictly block updates lacking a `WHERE` clause).