@Domain
Triggers for these rules:
- Writing or reviewing resource management, cleanup, or connection pooling code.
- Implementing network protocols, remote procedure calls (RPC), or socket-based communications.
- Diagnosing application hangs, unresponsive services, or cascading failures.
- Analyzing thread dumps or stack traces to determine the root cause of an outage.
- Planning or executing postmortem investigations and service restoration procedures.

@Vocabulary
- **Post Hoc, Ergo Propter Hoc**: Latin for "after this, therefore because of this" (or "you touched it last"). A starting heuristic for postmortems indicating that the most recent system change is a primary suspect for a subsequent failure.
- **Thread Dump**: A snapshot of the state of all threads in a process (e.g., JVM) used to deduce third-party library usage, thread pool sizes, background processing, and protocol usage.
- **Cascading Failure**: A failure mode where a defect in one isolated system (e.g., a database connection leak) exhausts shared resources (e.g., thread pools, socket readers), propagating the failure to upstream dependencies (e.g., Kiosks, IVR).
- **RMI (Remote Method Invocation)**: A remote procedure call transport that, by default, can block indefinitely because calls cannot be made to time out, leaving the caller vulnerable to remote server hangs.
- **Failover**: The process of migrating an active resource (like a database) from one host to another. Network topology changes during failover can invalidate existing TCP connections, leading to delayed I/O exceptions in application pools.
- **Automated Data Collection**: Scripts configured to automatically take thread dumps and database snapshots during an incident without prolonging the outage.

@Objectives
- Prevent single, localized exceptions from causing systemic resource exhaustion and grounding entire enterprise architectures.
- Ensure resource cleanup code (e.g., `try...finally` blocks) is resilient to failures within the cleanup phase itself.
- Eliminate infinite blocking scenarios in remote calls and socket reads.
- Prioritize rapid service restoration during an outage while simultaneously capturing volatile state data (thread dumps/logs) for postmortem analysis.
- Transition the engineering mindset from "preventing every bug" (which is fantasy) to "preventing bugs in one system from affecting everything else."

@Guidelines
- **Resource Cleanup Resilience**: When the AI generates or reviews resource cleanup logic (especially within `finally` blocks), it MUST ensure that exceptions thrown by one cleanup operation do not abort the execution of subsequent cleanup operations. Each disposable resource MUST be closed in its own isolated error-handling scope.
- **Timeout Enforcement**: The AI MUST NEVER implement remote network calls, RMI, or socket reads that block indefinitely. Every network dependency MUST be wrapped with an explicit timeout.
- **Incident Response Prioritization**: If simulating or assisting in an active outage scenario, the AI MUST recommend restoring service (e.g., restarting application servers) as the absolute first priority, ahead of deep root-cause investigation.
- **State Capture**: The AI MUST recommend using automated scripts to capture process thread dumps and database snapshots *before* restarting unresponsive services, as the evidence ("the corpse") vanishes once the server is rebooted.
- **Thread Dump Analysis**: When provided with a thread dump, the AI MUST analyze it to deduce the application's internal state, specifically hunting for threads blocked in `SocketInputStream.socketRead0`, `Object.wait()`, or connection pool `getConnection()` methods.
- **Defensive Pool Configuration**: The AI MUST verify that connection pools handle stale connections (e.g., connections surviving a database failover) gracefully without leaking the connection if a subsequent `close()` operation fails.
- **Failover Awareness**: The AI MUST assume that network state does not inherently survive IP failovers. It must anticipate that socket writes on pre-failover TCP connections will eventually throw IOExceptions, and must handle these exceptions without leaking resources.
- **Testing for the Unexpected**: The AI MUST advise that standard testing profiles ("aiming for QA") are insufficient for finding edge-case resource leaks. It should recommend stress tests that explicitly simulate backend failovers or timeouts.

@Workflow
**Process for Diagnosing System Hangs & Analyzing Postmortems:**
1. **Identify the Trigger**: Check for recent maintenance windows or changes ("post hoc, ergo propter hoc") such as database failovers.
2. **Collect Volatile Data**: Acquire thread dumps and application logs from the unresponsive servers before issuing restart commands.
3. **Restore Service**: Recommend targeted restarts of the affected application servers to clear blocked threads and restore SLAs.
4. **Analyze Thread Dumps**:
   - Count the total number of request-handling threads.
   - Identify the exact line of code where the threads are blocked (e.g., waiting for a database connection or waiting on a socket read).
   - Look for commonalities across nodes (e.g., 40 out of 40 threads blocked on `FlightSearch.lookupByCity`).
5. **Trace the Dependency**: If upstream threads are blocked on a remote call, acquire thread dumps from the downstream service being called.
6. **Identify the Smoking Gun**: Cross-reference blocked threads in the downstream service (e.g., blocked at `connectionPool.getConnection()`) with the source code handling those resources.
7. **Fix the Leak/Block**: Rewrite the offending resource handling code to isolate cleanup exceptions and enforce timeouts on remote integrations.

@Examples (Do's and Don'ts)

[DO] Implement resource cleanup where every closable resource is isolated in its own `try/catch` block within the `finally` clause, preventing one exception from leaking other resources.
```java
public List lookupByCity(...) throws RemoteException {
    Connection conn = null;
    Statement stmt = null;
    try {
        conn = connectionPool.getConnection();
        stmt = conn.createStatement();
        // Do the lookup logic
        // return a list of results
    } finally {
        if (stmt != null) {
            try {
                stmt.close();
            } catch (SQLException e) {
                // Log exception, but do not allow it to abort conn.close()
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
}
```

[DON'T] Group multiple `.close()` calls in a single `finally` block without independent exception handling. If `stmt.close()` throws an exception (e.g., due to a severed TCP connection from a failover), `conn.close()` is bypassed, leaking the connection and permanently exhausting the pool.
```java
public List lookupByCity(...) throws SQLException, RemoteException {
    Connection conn = null;
    Statement stmt = null;
    try {
        conn = connectionPool.getConnection();
        stmt = conn.createStatement();
        // Do the lookup logic
        // return a list of results
    } finally {
        // ANTI-PATTERN: If stmt.close() throws, conn is never closed!
        if (stmt != null) {
            stmt.close(); 
        }
        if (conn != null) {
            conn.close();
        }
    }
}
```

[DO] Configure RMI, Web Service, or Socket clients to explicitly enforce timeouts to prevent threads from blocking endlessly when a downstream dependency hangs.
```java
// Example of applying a timeout to a socket connection
Socket socket = new Socket();
socket.connect(new InetSocketAddress("api.corefacilities.com", 8080), 5000); // 5 second connection timeout
socket.setSoTimeout(10000); // 10 second read timeout
```

[DON'T] Rely on default RMI or Socket behaviors which wait indefinitely for a response, allowing a downstream resource exhaustion to trigger a cascading failure that halts upstream Kiosk and IVR applications.