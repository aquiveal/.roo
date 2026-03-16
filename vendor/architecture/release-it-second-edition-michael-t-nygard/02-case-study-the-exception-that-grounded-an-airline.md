# @Domain
Activation conditions: The AI MUST activate these rules when handling user requests, tasks, or files related to distributed systems architecture, high-availability cluster design, database failover orchestration, Java thread dump analysis, JDBC connection management, resource pooling, remote method invocation (RMI)/synchronous network calls, incident postmortems, or system outage diagnostics.

# @Vocabulary
- **Core Facilities (CF):** A centralized service-oriented architecture (SOA) application responsible for common services (e.g., flight searches), demonstrating high interactive complexity and tight coupling with client systems.
- **Failover:** The process of migrating an active database or service from one host to a redundant host using orchestration tools (e.g., Veritas Cluster Server) to allow maintenance or recovery.
- **Virtual IP Address:** An IP address managed by a cluster server that masks physical host identities from applications, allowing transparent failover between redundant nodes.
- **Severity 1 (Sev 1):** A critical system outage requiring immediate, prioritized intervention to restore service.
- **Service Level Agreement (SLA):** A defined time limit for resolving system outages (e.g., a one-hour SLA limit).
- **Thread Dump:** A snapshot of the state of every thread in a JVM at a specific point in time, used to diagnose hung applications without source code access.
- **Remote Method Invocation (RMI):** A remote procedure call mechanism used by Enterprise JavaBeans (EJBs) that, by default, lacks network timeouts, causing callers to block indefinitely if the remote server hangs.
- **Symptom vs. Disease:** The operational principle that individual system symptoms (e.g., an unresponsive IVR system) are often manifestations of a deeper shared dependency disease (e.g., exhausted DB connections in CF), rather than the root cause itself.
- **Postmortem:** An investigative, forensic process conducted after an outage is resolved to determine root causes, evaluate configurations, and implement preventative measures, likened to a "murder mystery without a corpse."
- **Post Hoc, Ergo Propter Hoc:** "You touched it last." A diagnostic heuristic in operations where recent system changes (e.g., a planned failover) are the primary suspects for subsequent unexpected outages.

# @Objectives
- **Prioritize Restoration Over Investigation:** The AI MUST prioritize actions and recommendations that restore system service immediately during an active outage, deferring root-cause investigation to the postmortem phase.
- **Enforce Cynical Resource Management:** The AI MUST assume that any external dependency or internal resource closure (e.g., `Statement.close()`) can and will fail, and MUST design code to isolate and survive these inevitable failures.
- **Eliminate Infinite Blocking:** The AI MUST eradicate default, indefinite blocking behaviors in all network calls, remote method invocations, and resource pool acquisitions.
- **Automate Forensic Data Collection:** The AI MUST prescribe automated scripts to gather diagnostic data (thread dumps, DB snapshots) without prolonging system outages.
- **Prevent Chain Reactions:** The AI MUST identify and sever tight coupling where a single localized defect (e.g., an unhandled `SQLException`) can propagate into a global, cross-system cascading failure.

# @Guidelines

### 1. Incident Response & Diagnostics
- **Automated Data Capture:** When designing operations protocols, the AI MUST require pre-existing automated scripts for capturing thread dumps and database snapshots. Improvised data collection during a Sev 1 incident is forbidden.
- **Service Restoration First:** When advising on active outages, the AI MUST recommend restarting suspected locked layers (e.g., restarting application servers) to restore SLAs before attempting live debugging.
- **Dependency Mapping for Triage:** When facing multiple simultaneously hung applications, the AI MUST identify the single common downstream dependency (the "disease") rather than treating individual applications (the "symptoms").

### 2. Thread Dump Analysis
- **Triggering:** The AI MUST utilize appropriate signals to trigger thread dumps: `kill -3 <pid>` (UNIX), `Ctrl+Break` (Windows), or `jcmd <pid> Thread.print` for detached JVMs.
- **Deduction from Stacks:** The AI MUST read thread dumps to deduce application architecture, specifically identifying: third-party libraries in use, thread pool configurations, thread counts, background processes, and active network protocols based on stack trace class names.
- **Identifying Bottlenecks:** The AI MUST scan thread dumps for threads trapped in `Object.wait()`, blocked on resource pool checkouts (e.g., `connectionPool.getConnection`), or blocked in native network libraries (e.g., `SocketInputStream.socketRead0`).

### 3. Resource & Connection Management
- **The `close()` Exception Risk:** The AI MUST operate under the architectural assumption that methods closing resources (e.g., JDBC `Statement.close()`) will throw exceptions (e.g., `SQLException` due to IOExceptions from dead TCP connections following a DB failover).
- **Isolated Cleanup:** When writing cleanup blocks (`finally`), the AI MUST isolate each resource closure. A failure to close one resource MUST NEVER prevent the closure of subsequent resources. Failure to isolate closures is categorized as a critical resource leak.
- **Resource Pool Exhaustion:** The AI MUST evaluate connection pools to ensure they do not block indefinitely when exhausted. Infinite waiting for checked-out connections MUST be replaced with bounded waits and timeouts.

### 4. Network & Remote Calls
- **RMI and EJB Hazards:** The AI MUST explicitly flag RMI and EJB remote calls as high-risk due to their lack of default socket timeouts.
- **Enforced Timeouts:** The AI MUST mandate strict timeouts on all synchronous remote calls, sockets, and API integrations to prevent caller threads from blocking indefinitely when remote servers hang or TCP connections silently drop.

### 5. Configuration Auditing
- **Backup Comparisons:** During postmortems, the AI MUST recommend comparing current configuration files against nightly backups made prior to the outage to detect unauthorized or undocumented mid-incident changes.

# @Workflow
When analyzing an architectural failure, outage scenario, or writing distributed resource management code, the AI MUST follow this rigid step-by-step process:

1. **Service Restoration Check:** Determine if the system is currently down. If down, immediately recommend execution of automated diagnostic scripts (thread dumps/snapshots) followed by targeted layer restarts based on dependency diagrams to restore service.
2. **Data Gathering (Postmortem):** Request or locate the automated forensic artifacts: application server logs, thread dumps, configuration files, database configurations, cluster server configurations, and backup configurations.
3. **Correlation & "Post Hoc" Analysis:** Identify any scheduled or unscheduled changes (e.g., failovers, deployments) that occurred immediately prior to the outage window. Formulate a primary hypothesis around these changes.
4. **Thread Dump Autopsy:**
    - Parse the dumps for threads in a "runnable" vs. "blocked" state.
    - Identify groups of threads blocking at the exact same method signature (e.g., `SocketInputStream.socketRead0` or `connectionPool.getConnection()`).
    - Trace the stack upward to identify the specific domain class/method initiating the block (e.g., `FlightSearch.lookupByCity`).
5. **Code Isolation (Decompilation if necessary):** Locate the exact source code for the blocking method. If source is unavailable, explicitly recommend decompiling the production binaries.
6. **Vulnerability Identification:** Scan the identified code strictly for:
    - Missing timeouts on network/RMI calls.
    - Flawed `try-catch-finally` blocks where a single exception halts the execution of subsequent cleanup code.
    - Resource pools configured to block indefinitely upon exhaustion.
7. **Remediation Design:** Refactor the offending code to use isolated resource closures (e.g., `try-with-resources`), inject explicit timeouts on all remote sockets, and configure resource pools with maximum block times.

# @Examples (Do's and Don'ts)

### Resource Cleanup in `finally` Blocks
**[DON'T]** Use sequential `close()` calls in a single `finally` block where an exception skips subsequent closures, causing connection pool exhaustion:
```java
// ANTI-PATTERN: If stmt.close() throws a SQLException, conn.close() is skipped.
public List lookupByCity(...) throws SQLException, RemoteException {
    Connection conn = null;
    Statement stmt = null;
    try {
        conn = connectionPool.getConnection();
        stmt = conn.createStatement();
        // Do the lookup logic
    } finally {
        if (stmt != null) {
            stmt.close(); // Throws exception if DB failover killed the TCP state
        }
        if (conn != null) {
            conn.close(); // Never executes, connection is leaked!
        }
    }
}
```

**[DO]** Use Java 7+ `try-with-resources` to guarantee isolated closure of all resources regardless of individual exceptions:
```java
// CORRECT: try-with-resources ensures all resources are closed independently.
public List lookupByCity(...) throws SQLException, RemoteException {
    // The connection and statement will both be closed automatically and safely.
    try (Connection conn = connectionPool.getConnection();
         Statement stmt = conn.createStatement()) {
        // Do the lookup logic
    } 
    // No explicit finally block needed for closures.
}
```

**[DO]** If constrained to legacy Java versions (pre-Java 7), isolate each `close()` call in its own `try-catch` block:
```java
// CORRECT LEGACY PATTERN: Isolated closures guarantee execution.
    } finally {
        if (stmt != null) {
            try {
                stmt.close();
            } catch (SQLException e) {
                log.warn("Failed to close statement", e);
            }
        }
        if (conn != null) {
            try {
                conn.close();
            } catch (SQLException e) {
                log.warn("Failed to close connection", e);
            }
        }
    }
```

### Remote Method Invocation / Network Calls
**[DON'T]** Rely on default RMI transports or default socket factories without configuring strict timeouts, risking total thread pool exhaustion.
```java
// ANTI-PATTERN: Default RMI calls can block forever waiting for a response.
InitialContext ctx = new InitialContext();
FlightSearch search = (FlightSearch) ctx.lookup("FlightSearchEJB");
// If CF is hung, this call blocks indefinitely, hanging the calling application.
search.lookupByCity("NYC");
```

**[DO]** Configure custom socket factories or client settings that enforce timeouts on all outgoing connections and reads.
```java
// CORRECT: Enforce timeouts at the socket level to fail fast.
Socket socket = new Socket();
socket.connect(new InetSocketAddress(host, port), 5000); // 5-second connection timeout
socket.setSoTimeout(10000); // 10-second read timeout
// Now, if the remote system hangs, this system throws a SocketTimeoutException and survives.
```