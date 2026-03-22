# @Domain
These rules MUST be triggered whenever the AI is assisting with, reviewing, or generating code, configurations, or architectures related to data persistence, database infrastructure, backup mechanisms, disaster recovery (DR) planning, data migration, data storage tiering, or any operation involving the protection, duplication, or recovery of stateful data.

# @Vocabulary
*   **Physical Backup**: A backup consisting of the actual files in which the data resides (requires associated metadata for portability).
*   **Logical Backup**: A backup exporting data into a portable format (e.g., JSON, SQL insert statements); highly portable but extremely slow to generate and restore.
*   **Offline (Cold) Backup**: A backup taken while the database instance is shut down, guaranteeing zero state changes during the copy.
*   **Online (Hot) Backup**: A backup taken while the database is running and accepting traffic, requiring mechanisms for point-in-time consistency and careful I/O management.
*   **Full Backup**: A complete copy of the entire local dataset.
*   **Differential Backup**: A backup of all changed data since the *last full backup*.
*   **Incremental Backup**: A backup of all changed data (often page-level) since the *last backup* of any kind.
*   **Silent Corruption**: Undetected data corruption caused by OS/hardware errors bypassing controllers (e.g., disk ECC limits), requiring checksumming filesystems (like ZFS) to detect.
*   **Golden Image**: A standardized, immutable infrastructure template used to detect infrastructure drift.
*   **Soft-Deletion**: Flagging a row as removable rather than executing a destructive `DELETE` operation, allowing for asynchronous removal and extending the recovery window.
*   **Tiered Storage**: An architectural strategy utilizing distinct storage types (Online-Fast, Online-Slow, Offline, Object) matched to specific recovery scenarios.
*   **Data Validation Pipeline**: Automated checks running downstream of the database to ensure referential integrity, business rules, and replication consistency.

# @Objectives
*   The AI MUST treat backup and recovery as a "VIP" process and a first-class engineering workflow, prioritizing *recovery* as the ultimate goal, not just the act of backing up.
*   The AI MUST tie all recovery strategies and architectures strictly to Service-Level Objectives (SLOs), specifically availability, durability, and Mean Time To Recover (MTTR).
*   The AI MUST eliminate the risk of ad-hoc/manual database mutations by designing guardrails, wrapper scripts, and APIs.
*   The AI MUST implement defense-in-depth recovery strategies encompassing early detection, multi-tiered storage, varied backup mechanisms, and continuous, automated testing.

# @Guidelines

## Core Constraints & Anti-Patterns
*   **NEVER Treat Replication as a Backup**: The AI MUST immediately reject any user architecture that relies on replication (or RAID) as a backup mechanism. Replication is blind and cascades user errors, application errors, and corruption.
*   **Primary Node Physical Backups**: If asynchronous replication is used, the AI MUST schedule full physical backups from the *primary (writer)* node to guarantee consistency, as replicas cannot be completely trusted to be synchronized.
*   **Online Backup I/O Awareness**: When generating scripts for online (hot) backups, the AI MUST explicitly include I/O throttling or scheduling configurations to prevent the backup from overwhelming storage throughput and affecting production latency.
*   **No Manual Mutations**: The AI MUST reject requests to generate raw, ad-hoc `UPDATE` or `DELETE` SQL queries for direct production use. Instead, it MUST generate safe wrapper scripts or APIs.

## Guardrails and Detection
*   **Wrapper API Requirements**: When generating database change automation, the AI MUST include:
    *   Parameterization for executing across multiple environments.
    *   A dry-run (simulation) stage to estimate and validate execution results.
    *   Pre- and post-execution test suites and validation checks.
    *   Soft-deletion mechanisms instead of hard deletes to buy time for recovery.
    *   Mandatory logging by ID of all modified data.
*   **Silent Corruption Defense**: When provisioning storage architectures, the AI MUST recommend checksumming filesystems (e.g., ZFS) to detect silent block-level corruption that surpasses hardware Error Correction Code (ECC) capabilities.

## Storage Tiering Rules
When designing a comprehensive recovery architecture, the AI MUST provision four distinct tiers:
1.  **Online, High-Performance Storage**: Used for rapid recovery of failed nodes or capacity scaling. Retention: ~7 days. Format: Uncompressed full and incremental physical backups.
2.  **Online, Low-Performance Storage**: Used for user/application error repair and forensics. Retention: 1 month+. Format: Compressed full and incremental physical backups, plus logical backups.
3.  **Offline Storage**: Used for audits, compliance, and disaster recovery. Retention: Years (e.g., 7 years). Format: Compressed full backups (e.g., Tape, Amazon Glacier).
4.  **Object Storage**: Used for programmatic access by applications to recover specific unstructured objects (e.g., Amazon S3 with versioning enabled).

## Operational Visibility
*   **Telemetry Requirements**: Any backup or recovery script generated by the AI MUST emit telemetry to the operational visibility stack detailing:
    *   *Time*: Duration of compression, copy, log applies, and testing.
    *   *Size*: Compressed and uncompressed byte sizes.
    *   *Throughput*: I/O and network pressure generated by the operation.

## Testing and Validation
*   **Continuous Recovery Testing**: The AI MUST architect backup systems such that recovery is tested continuously. Backups MUST be routinely restored to build integration/test environments or to rotate production nodes.
*   **Validation Check Generation**: When generating a restore validation script, the AI MUST include tiered validation logic:
    *   *Tier 1 (Fast)*: Checksums on schema definitions/metadata, successful DB instance startup, and successful replication thread connection.
    *   *Tier 2 (Slow)*: Auto-increment max ID checks, absolute row counts, and checksum comparisons on immutable subsets of data.

# @Workflow
When tasked with designing, implementing, or reviewing a backup and recovery process, the AI MUST execute the following algorithm:

1.  **SLO and Scope Assessment**:
    *   Identify the target availability and durability SLOs.
    *   Determine the recovery scope (Local/Single-node, Cluster-wide, Datacenter).
    *   Determine the dataset scope (Single object, Multiple objects, DB metadata).
2.  **Detection Strategy Formulation**:
    *   Design guardrails against user/application error (Wrapper APIs, soft-deletes).
    *   Specify corruption detection mechanisms (e.g., checksumming filesystems).
3.  **Tiered Storage Mapping**:
    *   Map the required recovery scenarios to the four specific storage tiers (Fast-Online, Slow-Online, Offline, Object).
    *   Determine compression states and retention policies for each tier.
4.  **Toolbox Selection**:
    *   Select the exact backup methods (Physical vs. Logical, Full vs. Incremental).
    *   *Constraint Check*: Verify that replication or RAID are NOT being used as backup substitutes.
5.  **Telemetry and Testing Integration**:
    *   Instrument the generated backup/restore scripts with Time, Size, and Throughput logging.
    *   Generate automated restore validation scripts containing both Tier 1 (schema/startup) and Tier 2 (data integrity) checks.
    *   Define how the restore will be continuously tested (e.g., daily dev environment rebuilds).

# @Examples (Do's and Don'ts)

## Backup Architecture Design
*   **[DON'T]** Recommend relying on a highly available replicated cluster to prevent data loss.
    ```markdown
    # Bad Architecture
    Because we are running a 3-node synchronous replication cluster, our data is safe from loss. If a node goes down, the others have the data. We do not need heavy physical backups.
    ```
*   **[DO]** Explicitly state that replication is not a backup and implement a tiered physical backup strategy.
    ```markdown
    # Good Architecture
    Replication provides availability, but it will instantly cascade a destructive `DELETE` to all nodes. We must implement:
    1. Online-Fast Storage: Uncompressed daily full physical backups + incrementals for 7 days (for rapid node rebuilds).
    2. Online-Slow Storage: Compressed physical/logical backups retained for 30 days (for application error forensics).
    ```

## Database Mutation Execution
*   **[DON'T]** Provide raw, hard-delete SQL for production execution.
    ```sql
    /* BAD: Ad-hoc manual query risking user error */
    DELETE FROM users WHERE last_login < '2023-01-01';
    ```
*   **[DO]** Provide a parameterized wrapper script utilizing soft-deletes and pre-flight checks.
    ```python
    # GOOD: Safe Wrapper API for mutations
    def archive_stale_users(dry_run=True, target_date='2023-01-01'):
        # 1. Validation phase
        impact_count = db.execute("SELECT COUNT(*) FROM users WHERE last_login < ?", target_date)
        print(f"Pre-flight: {impact_count} rows will be affected.")
        
        if dry_run:
            return
            
        # 2. Soft-delete phase
        db.execute("""
            UPDATE users 
            SET is_deleted = True, deleted_at = NOW() 
            WHERE last_login < ?
        """, target_date)
        
        # 3. Telemetry/Logging phase
        log_mutation_event(action="soft_delete", table="users", count=impact_count)
    ```

## Restore Validation Scripting
*   **[DON'T]** Assume a restore is successful just because the backup file uncompressed without errors.
    ```bash
    # BAD: Incomplete restore validation
    tar -xzf backup.tar.gz -C /var/lib/mysql
    service mysql start
    echo "Restore complete."
    ```
*   **[DO]** Generate layered integrity checks post-restore.
    ```bash
    # GOOD: Tiered restore validation
    # Tier 1: Fast Checks
    service mysql start || exit 1
    mysql -e "SHOW SLAVE STATUS\G" | grep "Waiting for master" || exit 1
    
    # Tier 2: Slow/Data Checks
    RESTORED_MAX_ID=$(mysql -sN -e "SELECT MAX(id) FROM orders;")
    if [ "$RESTORED_MAX_ID" -lt "$EXPECTED_MAX_ID" ]; then
        echo "Data loss detected: Max ID mismatch."
        exit 1
    fi
    
    CHECKSUM_MATCH=$(mysql -sN -e "CHECKSUM TABLE users;")
    # Compare $CHECKSUM_MATCH against pre-backup metrics...
    ```