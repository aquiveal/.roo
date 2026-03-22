# @Domain
These rules MUST trigger when the AI engages in tasks, evaluates files, or receives user requests related to:
- Database architecture, provisioning, and deployment (e.g., Terraform, CloudFormation, Ansible, Chef, Puppet applied to datastores).
- Database schema changes, migrations, and change-set tooling.
- Operational visibility, monitoring, metrics, and alerting configurations for datastores.
- Backup, restore, failover, and disaster recovery scripting or planning.
- CI/CD pipeline integration for database objects and configuration.
- Any request involving the roles of Database Administrator (DBA), Database Reliability Engineer (DBRE), or Site Reliability Engineer (SRE) managing stateful systems.

# @Vocabulary
- **DBRE (Database Reliability Engineer)**: An engineer who applies software engineering principles, repeatable processes, and automation to design, build, and operate data stores, acting as a substitute for traditional manual database administration.
- **SRE (Site Reliability Engineer)**: Fundamentally doing work historically done by ops teams, but using engineers with software expertise predisposed to substituting automation for human labor.
- **Toil**: Manual, repetitive, automatable, tactical work devoid of enduring value that scales linearly as a service grows.
- **Ephemeral Storage**: Storage that is lost if the compute instance fails or is shut down; used for consistent throughput/low latency, requiring robust automated network-based backup/recovery and application resilience.
- **Pets vs. Cattle**: The metaphor defining infrastructure design. "Pets" are named, uniquely customized servers nurtured back to health. "Cattle" are numbered, identical, replaceable components culled and replaced when sick. Databases MUST be treated as cattle.
- **Impedance Mismatch**: The organizational and cultural barrier between software engineering (SWE) and operations/DBA, resulting from different tooling, goals, and deployment methodologies.
- **Change-sets**: Packaged database changes (modifications to tables, indexes, data) evaluated and applied programmatically.
- **Guardrails**: Tooling and automated checks (e.g., Etsy's "Schemanator") that empower developers to safely apply their own database changes without fear, incorporating heuristic reviews, preflight checks, and safe fallback.
- **Maslow's Hierarchy of Database Needs**: A prioritized framework for database infrastructure maturity comprising:
  1. **Survival and Safety**: Backups, replication, failover, basic availability.
  2. **Love and Belonging (DevOps Needs)**: CI/CD integration, code review, breaking down silos, eliminating root cowboy commands, building guardrails.
  3. **Esteem**: Observability, instrumentation, correlation, alert tuning (reducing pager fatigue), and degradation knobs.
  4. **Self-Actualization**: Self-remediation, seamless scaling, empowering developers, and focusing on future product building.
- **Degradation Knobs**: Configurations or flags allowing a system to selectively degrade quality of service (e.g., read-only mode, queuing writes, blacklisting) instead of experiencing a complete outage.
- **Cowboy Commands**: Ad-hoc, manual commands executed directly in production environments (often as root), strictly prohibited in a DBRE culture.

# @Objectives
- The AI MUST approach all database tasks as an engineer building software, utilizing repeatable, automatable processes rather than manual administrative tasks.
- The AI MUST eliminate "snowflake" configurations; all database infrastructure MUST be designed as replaceable, version-controlled "cattle".
- The AI MUST bridge the gap between software development and operations by applying the Software Development Life Cycle (SDLC) to all database scripts, configurations, and schemas.
- The AI MUST design self-service platforms and guardrails that empower non-DBA teams to safely deploy database changes independently.
- The AI MUST fulfill the Hierarchy of Database Needs in strict sequential order, never prioritizing advanced scaling or complex monitoring before fundamental survival (backups/failover) is guaranteed.

# @Guidelines

## 1. Protect the Data via Engineering, Not Gatekeeping
- The AI MUST NOT implement strict, human-dependent separation of duties as a security measure if it restricts innovation or velocity.
- The AI MUST implement data protection via automated provisioning, automated deployment, redundancy, and well-practiced automated recovery procedures.
- When designing systems on Ephemeral Storage, the AI MUST implement full network-based database copies for restoration and engineer the application to tolerate node rebuilding.

## 2. Implement Self-Service for Scale
- The AI MUST output solutions that empower cross-functional teams rather than forcing them to serialize on a DBRE.
- The AI MUST generate self-service tooling, such as metric plugins, backup utilities, approved reference architectures, and safe deployment methods.

## 3. Elimination of Toil
- When a user requests a script or process for a manual database change, the AI MUST propose a fully automated, reusable tool to eliminate the repetitive human labor (e.g., rolling schema change automation utilities).

## 4. Databases Are Not Special Snowflakes (Pets vs. Cattle)
- The AI MUST NOT generate configurations that rely on specific hostnames, unique hardware, or manual server nurturing (e.g., "Patty" or "Selma" servers).
- The AI MUST design database cluster nodes to be strictly identical and effortlessly replaceable.

## 5. Eliminate Barriers Between Software and Operations
- The AI MUST treat all infrastructure, configurations, data models, and scripts as software.
- The AI MUST apply standard SDLC practices (code, test, integrate, build, deploy) to all database objects.

## 6. Fulfill the Hierarchy of Database Needs
- **Survival and Safety**: The AI MUST explicitly verify that backups, restores, replication, and failovers are configured before generating code for scaling or sharding.
- **Love and Belonging**: The AI MUST NOT generate instructions directing the user to log in as root to manually execute SQL. The AI MUST generate Guardrails (see below).
- **Esteem**: The AI MUST configure services to inherently expose state. The AI MUST NOT generate "monitor everything" alerting rules that cause pager fatigue; alerts MUST be tied to actionable signal, not noise. The AI MUST define Degradation Knobs (e.g., site read-only mode, feature toggles, write-queuing).
- **Self-Actualization**: The AI MUST aim for configurations that allow common operational pains to remediate themselves automatically.

## 7. Build Guardrails
When generating tools for schema or data changes, the AI MUST incorporate:
- Change-set heuristic reviews (validating standards in schema definitions).
- Pre-deployment test scripts.
- Preflight checks to display current cluster status to the developer.
- Rolling change mechanisms to apply impact on "out of service" databases.
- Workflows broken into subtasks to allow safe cancellation/fallback.

# @Workflow
When tasked with designing, deploying, or managing database systems, the AI MUST execute the following algorithm:

1. **Hierarchy Level 1 Verification (Survival)**
   - Assess the current request for backup, replication, and failover capabilities.
   - If generating an architecture, ensure automated backup and network-based restore mechanisms are explicitly defined first.

2. **Cattle-ification (Snowflake Elimination)**
   - Ensure all requested resources are abstracted.
   - Remove any hardcoded identifiers; replace with version-controlled, declarative infrastructure code (e.g., Terraform/Ansible).

3. **SDLC Integration (Love and Belonging)**
   - Wrap the database change in a CI/CD-compatible format.
   - Inject Guardrails: Add scripts for preflight checks, heuristic validation, and subtask cancellation.

4. **Instrumentation and Control (Esteem)**
   - Define metric outputs that allow the application to self-report its state (up/down/error rates).
   - Inject Degradation Knobs: Add specific configuration flags allowing the database/service to selectively degrade (e.g., queue writes, drop non-critical traffic) during stress.

5. **Toil Mitigation Check**
   - Review the final output. If the solution requires a human to execute it more than once for future changes, refactor the output into a self-service automation script.

# @Examples (Do's and Don'ts)

### Principle: Databases Are Not Special Snowflakes (Pets vs. Cattle)
- **[DO]**: Use declarative, parameterized code for database clusters where any node can be culled and rebuilt automatically.
  ```hcl
  resource "aws_autoscaling_group" "db_cluster" {
    name_prefix = "db-node-cattle-"
    min_size    = 3
    max_size    = 5
    # Nodes are replaced automatically if unhealthy
  }
  ```
- **[DON'T]**: Create customized, named instances that require manual care.
  ```hcl
  resource "aws_instance" "db_patty" {
    name = "patty-the-primary-db"
    # Requires human login to fix if broken
  }
  ```

### Principle: Eliminate Barriers Between Software and Operations (Guardrails)
- **[DO]**: Provide a CI/CD script that programmatically tests and safely applies changes with preflight checks.
  ```yaml
  deploy_db_changes:
    script:
      - ./db_tools/preflight_check.sh --cluster main
      - ./db_tools/heuristic_review.sh schemas/updates.sql
      - ./db_tools/rolling_apply.sh schemas/updates.sql --allow-cancel
  ```
- **[DON'T]**: Provide instructions for manual, cowboy-style root execution.
  ```text
  SSH into the primary database server using root.
  Run `mysql -u root -p < updates.sql`.
  Watch the graphs to make sure it doesn't crash.
  ```

### Principle: Esteem (Observability and Degradation Knobs)
- **[DO]**: Implement specific flags to gracefully degrade service and alert only on actionable end-user impact.
  ```python
  if db_latency > threshold:
      enable_degradation_knob(feature="read_only_mode")
      queue_writes_for_later()
      alert_oncall("Write queue active, database degraded but responsive")
  ```
- **[DON'T]**: Monitor every possible metric and hard-fail the system without fallback.
  ```python
  if cpu_usage > 80%:
      page_oncall_engineer() # Pager fatigue: CPU spikes might be normal
      throw SystemError("Database overloaded") # No degradation, site goes down
  ```

### Principle: Survival on Ephemeral Storage
- **[DO]**: Rely on network-based cluster recovery and redundancy.
  ```bash
  # Restore process for ephemeral storage
  fetch_latest_full_backup_from_s3()
  stream_transaction_logs_over_network()
  rejoin_cluster_and_sync()
  ```
- **[DON'T]**: Rely on local volume snapshots for databases running on ephemeral instance types.
  ```bash
  # Anti-pattern: Assuming local disk state persists
  aws ec2 create-snapshot --volume-id ephemeral_vol_123 
  ```