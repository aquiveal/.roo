# @Domain
These rules MUST be activated when the AI is tasked with designing, configuring, reviewing, or deploying database infrastructure, data access layers, database queries, security policies, authentication mechanisms, data encryption implementations, or database logging and monitoring systems. This includes any review of infrastructure-as-code (IaC) related to datastores, SQL query generation, ORM configuration, or secret management.

# @Vocabulary
*   **DBRE**: Database Reliability Engineer.
*   **DB-DoS**: Database Denial of Service. An attack that exhausts database resources (connections, CPU, memory, disk, replication) through legitimate or illegitimate traffic spikes, rendering dependent services unavailable.
*   **STRIDE**: A threat modeling classification framework evaluating: Spoofing identity, Tampering with data, Repudiation, Information disclosure, Denial of service, and Elevation of privilege.
*   **DREAD**: A risk prioritization framework computing risk based on: Damage potential, Reproducibility, Exploitability, Affected users, and Discoverability.
*   **CVE**: Common Vulnerabilities and Exposures.
*   **PFS (Perfect Forward Secrecy)**: A cryptographic property ensuring that a compromise of the server's long-term signing key does not compromise the confidentiality of past sessions (e.g., using Ephemeral Diffie-Hellman `ECDHE` or `DHE`).
*   **Cipher Suite**: A negotiated security setting for TLS connections consisting of a Key Exchange Algorithm (e.g., `ECDHE`), Signature Algorithm (e.g., `RSA`), Cipher and Mode (e.g., `AES128-GCM`), and MAC function (e.g., `SHA256`).
*   **HMAC (Hash-based Message Authentication Code)**: A cryptographic hash used to allow equality searches on encrypted database fields without disclosing plaintext values.
*   **Ephemeral Database Users**: Dynamically generated, short-lived database credentials mapped to specific application hosts via a secure secret management service.
*   **Gold Standard**: Pre-approved, automated, self-service infrastructure patterns that enforce baseline database security out-of-the-box.

# @Objectives
*   **Defense in Depth**: The AI MUST apply security controls at every layer (Application, Database, OS, Network, and Filesystem) rather than relying on a single perimeter.
*   **Eliminate Defaults**: The AI MUST systematically identify and strip away default vendor configurations, accounts, and exposed ports.
*   **Secure Data Across States**: The AI MUST enforce cryptographic protections for data in transit (flight), data in the database (use), and data in the filesystem (rest).
*   **Prevent Exploits**: The AI MUST proactively neutralize SQL Injection (SQLi) and DB-DoS vulnerabilities through strict architectural patterns and code review.
*   **Comprehensive Visibility**: The AI MUST ensure all access, configuration mutations, and syntax errors are aggressively logged and monitored to detect intruders, insiders, and accidental damage.

# @Guidelines

## 1. Infrastructure and Gold Standards
*   **No Defaults**: When generating infrastructure code for databases, the AI MUST explicitly disable or remove default accounts, default passwords, and default listening interfaces (e.g., never bind to `0.0.0.0` without strict authentication and firewalling).
*   **Least Privilege**: The AI MUST lock down unnecessary ports, restrict access lists to explicit hostgroups, and remove database features that allow OS filesystem or network exploits.
*   **Self-Service Code**: The AI MUST encapsulate security best practices (SSL/TLS generation, password policy enforcement, audit log forwarding) within reusable IaC modules.

## 2. Threat Modeling
*   When evaluating database architecture, the AI MUST use the **STRIDE** model to classify potential threats.
*   The AI MUST prioritize risks using the **DREAD** algorithm, ranking threats based on Damage, Reproducibility, Exploitability, Affected users, and Discoverability.

## 3. Operational Visibility and Logging
*   **Application Layer**: The AI MUST ensure the application logs all failed and successful SQL statements, logs SQL syntax errors (as they are leading indicators of SQLi attacks), and tracks any interaction with PII/critical data via metadata-flagged API endpoints.
*   **Database Layer**: The AI MUST configure the datastore to audit and push to centralized logging: configuration changes (file or memory), user/privilege changes, DML on audit tables (SELECT/INSERT/UPDATE/DELETE), new database objects (functions, triggers, views), logins (failed and successful), and binary patching.
*   **OS Layer**: The AI MUST ensure monitoring of OS configuration changes, new software/scripts, OS logins, and kernel/binary patches.

## 4. DB-DoS Mitigation
*   The AI MUST review database queries for potential resource exhaustion vectors (e.g., unbound UNIONs, huge sorts, missing indexes, empty search inputs).
*   To mitigate DB-DoS, the AI MUST recommend implementing:
    *   Client-side throttling and exponential backoff.
    *   Quality of Service (QoS) quotas prioritizing critical traffic over expensive queries.
    *   Graceful degradation of results during high load (e.g., reducing rows scanned).
    *   Query killers or performance profiles to terminate runaway transactions.

## 5. SQL Injection Prevention
*   The AI MUST absolutely forbid dynamic SQL generation using string concatenation.
*   The AI MUST enforce the use of **Prepared Statements (Parameterized Queries)** for all data access code.
*   When table names or sort directions (`ASC`/`DESC`) must be dynamic, the AI MUST enforce strict **Input Validation** against a predefined whitelist.
*   The AI MUST recommend harm reduction strategies: patching database binaries, removing unused stored procedures, and creating discrete database users for each application rather than a shared superuser.

## 6. Securing Data In Transit
*   The AI MUST enforce **TLS 1.1 or 1.2** (strongly preferring TLS 1.2 or higher). It MUST explicitly reject TLS 1.0 and SSL 3.0.
*   The AI MUST enforce the use of strong cipher suites using **PFS (Perfect Forward Secrecy)**. Key exchanges MUST use `ECDHE` or `DHE`. Signatures MUST prefer `RSA` over `DSA`/`DSS`. Ciphers MUST use `AES` (128, 192, or 256) in `GCM` mode. MAC functions MUST use `SHA2` (e.g., SHA256, SHA384).
*   The AI MUST specify that inter-network and internet-to-load-balancer traffic be encrypted via VPN/IPSec or SSL/TLS.
*   **Secrets Management**: The AI MUST NOT store database credentials or encryption keys in plaintext filesystems or source code. The AI MUST recommend integrating secure secret managers (e.g., Hashicorp Vault, AWS KMS).
*   **Dynamic Users**: Where possible, the AI MUST design authentication flows using dynamically built, ephemeral database users mapped to specific application hosts.

## 7. Securing Data at Rest and In Use
*   **Application-Level Security**: For highly sensitive fields (PII, Financial), the AI MUST prefer application-level encryption (e.g., Bouncy Castle, OpenSSL) before insertion to ensure DB portability and prevent DBA exposure.
*   **Searchable Encrypted Data**: Because B-Tree indexes fail on encrypted strings, the AI MUST design schema searches using an `HMAC` of the plaintext field. The AI MUST suggest adding obfuscation (dummy data, batched inserts) to prevent frequency/cardinality inference attacks on the HMAC index.
*   **Filesystem Encryption**: The AI MUST specify filesystem encryption (Stacked like eCryptfs/EncFs, or Block-level like Loop-AES/dm-crypt) for database logs, temporary files, and metadata files.

# @Workflow
When generating, reviewing, or securing database-related code or architecture, the AI MUST follow this rigid step-by-step process:

1.  **Data Classification**: Determine the type of data being handled (Financial, Health, PII, Gov, Business Secret) to establish the necessary encryption and compliance baseline.
2.  **Threat Modeling (STRIDE/DREAD)**: Evaluate the proposed architecture or query against spoofing, tampering, repudiation, information disclosure, DoS, and privilege escalation.
3.  **Connection & Identity Security**: Enforce TLS 1.2+ and PFS cipher suites. Extract any hardcoded credentials and replace them with calls to a Key Management Service (Vault/KMS) or dynamic ephemeral credentials.
4.  **Query Hardening**: Scan all SQL/DAL code for string concatenation. Replace with prepared statements. Implement input validation whitelists for structural SQL elements (table names, ASC/DESC). Evaluate queries for DB-DoS vulnerabilities (missing limits, Cartesian joins) and enforce throttling/timeouts.
5.  **Encryption Strategy Application**: Apply Application-Level encryption to sensitive columns. Append an HMAC column if equality search is required. Ensure filesystem encryption is specified for underlying storage instances.
6.  **Telemetry Injection**: Inject logging triggers for successful/failed queries, syntax errors, and configuration mutations to satisfy comprehensive visibility requirements.

# @Examples (Do's and Don'ts)

## Prepared Statements (SQL Injection Prevention)
*   **[DO]**: Use parameterized queries where the database driver handles variable binding.
    ```java
    String query = "SELECT ip, os FROM servers WHERE host_name = ?";
    PreparedStatement pstmt = connection.prepareStatement(query);
    pstmt.setString(1, hostName);
    ResultSet results = pstmt.executeQuery();
    ```
*   **[DON'T]**: Concatenate strings to build SQL queries, which allows attackers to modify the query structure.
    ```java
    String query = "SELECT ip, os FROM servers WHERE host_name = '" + hostName + "'";
    Statement stmt = connection.createStatement();
    ResultSet results = stmt.executeQuery(query); // Vulnerable to SQLi
    ```

## TLS Cipher Suite Configuration
*   **[DO]**: Specify modern cipher suites that provide Perfect Forward Secrecy and authenticated encryption.
    ```nginx
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;
    ```
*   **[DON'T]**: Allow outdated SSL/TLS versions or weak ciphers that lack PFS.
    ```nginx
    ssl_protocols SSLv3 TLSv1; # Vulnerable to downgrade attacks
    ssl_ciphers HIGH:!aNULL:!MD5; # Too broad, might select non-PFS ciphers
    ```

## Database Listener Binding
*   **[DO]**: Bind database listeners to private interfaces or localhost, utilizing firewalls to restrict access.
    ```ini
    bind_ip = 127.0.0.1, 10.0.5.15
    security:
      authorization: enabled
    ```
*   **[DON'T]**: Bind to all interfaces without authentication enabled (the default MongoDB anti-pattern).
    ```ini
    bind_ip = 0.0.0.0 # Exposed to the public internet
    # authorization is disabled by default
    ```

## Searching Encrypted Data
*   **[DO]**: Store ciphertext and a salted HMAC of the plaintext. Query against the HMAC for exact matches.
    ```sql
    -- Application hashes "user@email.com" using a secure key to produce the HMAC
    SELECT user_id, encrypted_email FROM users WHERE email_hmac = 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3';
    ```
*   **[DON'T]**: Attempt to index ciphertext using a standard B-Tree, or decrypt the entire table into memory to perform a search.
    ```sql
    -- Cannot use B-Tree index on AES-encrypted blobs effectively
    SELECT user_id FROM users WHERE pgp_sym_decrypt(encrypted_email, 'secret') = 'user@email.com';
    ```

## Application Log Visibility
*   **[DO]**: Log syntax errors explicitly to detect automated SQL injection probing.
    ```javascript
    try {
        await db.query(sql, params);
    } catch (err) {
        if (err.code === 'ER_SYNTAX_ERROR') {
            securityLogger.warn({ event: 'SQL_SYNTAX_ERROR', user: req.user, query: sql, ip: req.ip });
        }
    }
    ```
*   **[DON'T]**: Swallow database errors or return raw stack traces to the end user.