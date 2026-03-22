@Domain
Triggered when architecting, designing, implementing, reviewing, or testing distributed software systems, enterprise integrations, backend web services, database connection management, socket communications, resource pools, and system stability/longevity mechanisms.

@Vocabulary
- **Transaction**: An abstract unit of work processed by the system (e.g., "customer places order"), potentially spanning multiple database transactions and external integrations.
- **Dedicated System**: A system that processes just one type of transaction.
- **Mixed Workload**: A system that processes a combination of different transaction types.
- **System**: The complete, interdependent set of hardware, applications, and services required to process transactions for users.
- **Robust System**: A system that continues processing transactions despite transient impulses, persistent stresses, or component failures.
- **Impulse**: A rapid shock to the system (e.g., a flash mob, suddenly dumping millions of messages into a queue).
- **Stress**: A force applied to the system over an extended period (e.g., slow responses from a third-party credit card processor).
- **Strain**: The change in shape or behavior produced by stress (e.g., higher RAM usage, excess I/O rates, odd downstream effects).
- **Longevity**: A system's ability to keep processing transactions for a long time (operationally defined as at least the time between scheduled code deployments).
- **Cracks in the system**: Microscopic points of failure that, under stress, propagate faster and faster until catastrophic systemic failure occurs.
- **Failure Mode**: The combination of the original trigger, the way the crack spreads to the rest of the system, and the ultimate result of the damage.
- **Crackstoppers**: Intentionally designed safe failure modes (analogous to crumple zones in cars) that contain damage and protect indispensable system features.
- **Fault**: A condition that creates an incorrect internal state in the software (e.g., a triggered latent bug, an unchecked boundary condition).
- **Error**: Visibly incorrect behavior resulting from a fault.
- **Failure**: An unresponsive system resulting from an unmitigated error.

@Objectives
- Treat production stability and real-world hostility as primary architectural concerns, rather than merely aiming to pass Quality Assurance (QA) tests.
- Develop "cynical software" that inherently expects bad things to happen, puts up internal barriers, and refuses to intimately trust other systems.
- Stop the propagation of cracks (the progression of Fault -> Error -> Failure) by explicitly designing intentional, safe failure modes (crackstoppers).
- Maximize system longevity by relentlessly preventing memory leaks, halting unbounded data growth, and mandating longevity testing.
- Relieve systemic strain by replacing tight coupling with shock-absorbing, less-coupled architectures.

@Guidelines
- **Mandate Cynical Software:** The AI MUST NOT assume external calls, I/O operations, or resource allocations will succeed. The AI MUST proactively wrap all external integrations with protective barriers.
- **Implement Crackstoppers:** The AI MUST configure all resource pools (e.g., database connection pools, thread pools) to either block for a strictly limited time or dynamically create more connections. The AI MUST NEVER configure a pool to block requesting threads indefinitely.
- **Enforce Timeouts:** The AI MUST explicitly set both connection and read timeouts on all socket connections, RMI calls, and remote procedure calls. Default infinite timeouts MUST be overridden.
- **Isolate via Partitioning:** When designing infrastructure or service deployment, the AI MUST partition servers/services into multiple distinct service groups to prevent a single problem from taking down all users.
- **De-couple Architectures:** When designing inter-system communications, the AI MUST recommend decoupled mechanisms (e.g., request/reply message queues, tuple spaces) to act as shock absorbers instead of tightly coupled, blocking synchronous calls.
- **Exhaustive I/O Interrogation:** For every external call, I/O operation, resource use, and expected outcome, the AI MUST analyze and explicitly handle the following failure permutations:
  - What if the initial connection fails?
  - What if it takes excessive time (e.g., 10 minutes) to make the connection?
  - What if the connection succeeds but subsequently disconnects?
  - What if the connection succeeds but receives no response from the other end?
  - What if the query/response takes excessive time (e.g., 2 minutes)?
  - What if a massive impulse of concurrent requests (e.g., 10,000) arrives at once?
  - What if the local disk is full when attempting to log the resulting error?
- **Longevity Threat Mitigation:** The AI MUST actively audit and reject code patterns that cause memory leaks or unbounded data accumulation, as these are the primary threats to system longevity.
- **Fault Strategy Election:** The AI MUST explicitly state whether a component uses a "fault-tolerant" approach (catching exceptions, checking error codes, recovering) or a "let it crash" approach (failing fast and restarting from a known good state). Regardless of the choice, the AI MUST ensure faults are trapped before they become systemic errors.

@Workflow
1. **Boundary Analysis:** Identify all system boundaries, integration points, socket layers, and external dependencies in the proposed code or architecture.
2. **Impulse & Stress Mapping:** For each boundary, document what constitutes a rapid "impulse" and a prolonged "stress". 
3. **Crackstopper Implementation:** Apply explicit constraints (timeouts, bounded wait times, fail-fast validations) to every identified boundary to serve as "crumple zones".
4. **Decoupling Review:** Evaluate whether synchronous/tightly-coupled calls can be safely replaced with asynchronous message queues or tuple spaces to absorb network strain.
5. **Longevity Test Generation:** Create or specify longevity testing strategies (using tools like JMeter or Marathon). The AI MUST explicitly instruct these tests to run continuously for days and MUST include idle/slack periods to accurately simulate slow night periods, ensuring connection pool and firewall timeouts are caught.

@Examples

**[DO]**
```java
// Implementing a Crackstopper with Cynical Software principles
public List<Flight> lookupByCity(String city) throws LookupException {
    Connection conn = null;
    PreparedStatement stmt = null;
    try {
        // Pool is explicitly configured to timeout after 3000ms, not block forever
        conn = connectionPool.getConnection(3000); 
        
        // Sockets underlying the connection have explicit network timeouts configured
        stmt = conn.prepareStatement(QUERY);
        stmt.setQueryTimeout(5); // 5 second timeout on the query execution
        
        // Process results...
    } catch (SQLException | SocketTimeoutException e) {
        // Fault is caught and contained before it becomes a systemic Error/Failure
        throw new LookupException("Service temporarily degraded", e);
    } finally {
        // Safely releasing resources, aware that close() itself can throw exceptions
        closeQuietly(stmt);
        closeQuietly(conn);
    }
}
```

**[DON'T]**
```java
// Anti-pattern: Un-cynical software, infinite blocking, and unhandled failure modes
public List<Flight> lookupByCity(String city) throws Exception {
    // Blocks indefinitely if pool is exhausted, tying up request-handling threads
    Connection conn = connectionPool.getConnection(); 
    
    Statement stmt = conn.createStatement();
    // No query timeout set. A stressed DB will cause this thread to hang forever.
    ResultSet rs = stmt.executeQuery("SELECT * FROM flights WHERE city = '" + city + "'");
    
    // If the database failed over, closing the statement might throw an exception,
    // bypassing the conn.close() and leaking the connection permanently.
    stmt.close(); 
    conn.close(); 
    
    return results;
}
```

**[DO]**
```markdown
# Longevity Test Plan
Use JMeter to drive continuous, moderate traffic against the production-candidate environment for 7 days. 
Crucially, script a 3-hour "slack period" every night where traffic drops to 0. This idle period is explicitly designed to test if stateful firewalls drop TCP connections and whether the application's connection pool properly validates stale connections upon resumption of traffic.
```

**[DON'T]**
```markdown
# Longevity Test Plan
Run the automated QA test suite. Once it passes, run a 1-hour load test at 200% expected capacity to prove the system doesn't crash under load, then sign off for production deployment.
```