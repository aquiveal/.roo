# @Domain
This rule file MUST be activated when the AI is tasked with designing system architecture, writing or refactoring integration code, configuring resource pools, establishing network communications, designing error-handling strategies, or writing load and longevity tests for distributed systems.

# @Vocabulary
*   **Cynical Software:** Software that expects bad events to happen, does not trust its own internal state, builds internal barriers to protect itself from failures, and refuses to become intimately coupled with other systems.
*   **Transaction:** An abstract unit of work processed by the system (not exclusively a database transaction, but the reason the system exists, e.g., "customer places order").
*   **Dedicated System:** A system that processes just one type of transaction.
*   **Mixed Workload:** A system that processes a combination of different transaction types.
*   **System:** The complete, interdependent set of hardware, applications, and services required to process transactions for users.
*   **Robust System:** A system that continues processing transactions even when transient impulses, persistent stresses, or component failures disrupt normal processing.
*   **Impulse:** A rapid, sudden shock to the system (e.g., a massive spike in concurrent traffic within a single minute).
*   **Stress:** A force applied to the system over an extended period (e.g., slow responses from a third-party dependency).
*   **Strain:** The alteration in system behavior or shape produced by stress (e.g., high RAM usage, excess I/O rates).
*   **Longevity:** The ability of a system to keep processing transactions for an extended duration, typically defined as the time between code deployments.
*   **Cracks in the System:** Small, initial component failures that, under stress, propagate rapidly and explosively break the rest of the system.
*   **Failure Mode:** The combination of the original trigger, the pathway the crack spreads to the rest of the system, and the resulting damage.
*   **Crackstoppers (Crumple Zones):** Safe, deliberately designed failure modes engineered to contain damage, absorb impacts, and protect indispensable system features by failing first.
*   **Fault:** A condition that creates an incorrect internal state in the software (e.g., a latent bug or an unchecked boundary condition).
*   **Error:** Visibly incorrect behavior resulting from a triggered fault.
*   **Failure:** An unresponsive system resulting from unmitigated errors.
*   **Chain of Failure:** The sequential propagation pathway where a Fault becomes an Error, and an Error provokes a Failure.

# @Objectives
*   Design and implement "cynical" software that survives the real world rather than just passing Quality Assurance (QA) tests.
*   Anticipate and absorb both sudden impulses and prolonged stresses without allowing strain to fracture the entire system.
*   Ensure system longevity by actively defending against memory leaks and data growth over extended timeframes.
*   Design explicit, contained failure modes (crackstoppers) so that when components fail, they do not propagate cracks to dependent layers.
*   Break the Chain of Failure by preventing internal Faults from escalating into visible Errors, and Errors from escalating into systemic Failures.

# @Guidelines
*   **Implement Cynical Architectures:** The AI MUST NOT assume external calls will succeed, respond quickly, or behave logically. The AI MUST erect internal defensive barriers around all external integrations.
*   **Define Safe Failure Modes:** The AI MUST proactively design what a component will do when it fails. If a failure mode is not designed, the system will default to an unpredictable and dangerous failure mode.
*   **Bounded Resource Pools:** When configuring connection pools, thread pools, or any constrained resource, the AI MUST configure the pool to either dynamically create more resources or block requesting callers for a strictly limited time. The AI MUST NOT configure resource pools to block indefinitely.
*   **Network Call Defenses:** The AI MUST explicitly configure timeouts for all sockets, RMI, RPC, and HTTP calls. The AI MUST NOT rely on default networking behaviors that block forever waiting for a response.
*   **Thread Isolation:** The AI MUST write integration code such that blocked threads can be jettisoned or isolated. The AI MUST NOT allow a blocked external call to consume and exhaust primary request-handling threads.
*   **Architectural Shock Absorbers:** To prevent crack propagation, the AI MUST favor decoupled architectures. The AI MUST evaluate substituting tightly coupled synchronous calls with request/reply message queues, tuple spaces, or loosely coupled service groups.
*   **Partition Service Groups:** The AI MUST separate dependent services into multiple partitions so that an error in one group does not immediately consume the resources of all other consumers.
*   **The "What Can Go Wrong?" Checklist:** For every external call, I/O operation, and resource allocation, the AI MUST explicitly account for the following scenarios in the code:
    *   What if the system cannot make the initial connection?
    *   What if it takes 10 minutes to make the connection?
    *   What if the connection is made but gets disconnected immediately?
    *   What if the connection is made but no response is ever sent?
    *   What if the response takes 2 minutes to arrive?
    *   What if 10,000 requests arrive at the exact same time?
    *   What if the disk is full when attempting to log the resulting error?
*   **Address Longevity Threats:** The AI MUST implement resource cleanup (e.g., `try/finally` blocks) to prevent the accumulation of memory leaks and unbounded data growth over time.
*   **Design Longevity Tests:** When generating test suites, the AI MUST NOT rely solely on short-burst load tests. The AI MUST script longevity tests (using tools like JMeter or Marathon) that drive continuous, moderate requests over days.
*   **Simulate Idle Periods in Testing:** The AI MUST program longevity test scripts to include explicit "slack" periods (several hours of idle time) to simulate midnight traffic lulls. This specifically tests for connection pool exhaustion and firewall connection dropping upon resumption of traffic.
*   **Fault Strategy Selection:** The AI MUST explicitly implement either a "fault-tolerant" strategy (catching exceptions, checking error codes, recovering state) or a "let it crash" strategy (terminating and restarting from a known good state). The AI MUST document which strategy is being applied to prevent Faults from becoming Errors.

# @Workflow
1.  **Dependency Mapping:** Identify every integration point, shared resource, database connection, and external API call within the target code.
2.  **Vulnerability Assessment:** Apply the "What Can Go Wrong?" checklist to every mapped dependency. Document the expected system strain for each scenario (e.g., "If this API hangs, 40 request threads will block").
3.  **Crackstopper Injection:** Modify the code to inject boundary defenses. Add strict timeouts to all network calls and maximum wait times to all resource pool checkouts.
4.  **Decoupling Evaluation:** Analyze the architecture to determine if a synchronous call can be replaced with an asynchronous shock absorber (e.g., a message queue). If yes, refactor the communication layer.
5.  **Failure Mode Definition:** Write explicit fallback logic (e.g., return a degraded response, drop the request, or restart the component) detailing exactly how the component behaves when the crackstopper is triggered.
6.  **Longevity Test Generation:** Write automated test scripts designed to run continuously. Embed programmatic pauses (slack periods of several hours) within the test execution loop to validate that resources gracefully recover from idle states.
7.  **Final Review:** Verify that the code is "cynical"—confirming that no external inputs or dependencies are trusted, and that a failure in this specific component cannot trigger a Chain of Failure across the entire system.

# @Examples (Do's and Don'ts)

### Resource Pool Configuration
**[DO]** Configure resource pools to fail fast when exhausted, returning control to the caller so they can degrade gracefully.
```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/db");
// A crackstopper: Block for a limited time, then throw an exception
config.setConnectionTimeout(5000); 
config.setMaximumPoolSize(20);
HikariDataSource ds = new HikariDataSource(config);
```

**[DON'T]** Leave resource pool wait times unconfigured or set to infinite, allowing a slow database to exhaust all application threads.
```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/db");
config.setMaximumPoolSize(20);
// ANTI-PATTERN: Connection timeout is infinite/unbounded by default in some older pools,
// creating a Failure Mode where all 40 frontend threads will block waiting for a connection.
HikariDataSource ds = new HikariDataSource(config);
```

### Network Communication Timeouts
**[DO]** Apply explicit timeouts to all stages of a network connection to prevent slow responses from becoming a system-wide stress.
```python
import requests
from requests.exceptions import Timeout

def fetch_external_data():
    try:
        # DO: Explicitly bound the connection time (3.0s) and the read time (5.0s)
        response = requests.get("https://api.example.com/data", timeout=(3.0, 5.0))
        return response.json()
    except Timeout:
        # Crackstopper: Handle the fault locally before it becomes an error
        return {"status": "degraded", "data": []}
```

**[DON'T]** Trust the network or the remote server to respond promptly.
```python
import requests

def fetch_external_data():
    # ANTI-PATTERN: No timeout. If the remote API accepts the connection but never 
    # sends data, the calling thread blocks forever. The crack propagates.
    response = requests.get("https://api.example.com/data")
    return response.json()
```

### Longevity Testing Scripts
**[DO]** Create test scenarios that simulate long-term real-world stresses, including periods of absolute inactivity to test network/firewall behavior.
```xml
<!-- DO: JMeter setup including a Timer to simulate mid-night slack periods -->
<ThreadGroup>
    <stringProp name="ThreadGroup.num_threads">10</stringProp>
    <stringProp name="ThreadGroup.ramp_time">60</stringProp>
    <boolProp name="ThreadGroup.scheduler">true</boolProp>
    <stringProp name="ThreadGroup.duration">604800</stringProp> <!-- 7 days -->
</ThreadGroup>
<!-- Use Throughput Shaping Timer to drop load to near 0 for hours 02:00-05:00 -->
<kg.apc.jmeter.timers.VariableThroughputTimer>
    <collectionProp name="load_profile">
        <collectionProp name="active_hours">
            <stringProp name="start_rps">100</stringProp>
            <stringProp name="end_rps">100</stringProp>
            <stringProp name="duration_sec">72000</stringProp> <!-- 20 hours active -->
        </collectionProp>
        <collectionProp name="slack_period">
            <stringProp name="start_rps">1</stringProp>
            <stringProp name="end_rps">1</stringProp>
            <stringProp name="duration_sec">14400</stringProp> <!-- 4 hours slack -->
        </collectionProp>
    </collectionProp>
</kg.apc.jmeter.timers.VariableThroughputTimer>
```

**[DON'T]** Rely solely on short, intense load tests that recycle environments daily, hiding long-term sludge buildup and idle connection drops.
```xml
<!-- ANTI-PATTERN: Testing only for immediate QA passage -->
<ThreadGroup>
    <stringProp name="ThreadGroup.num_threads">5000</stringProp>
    <stringProp name="ThreadGroup.duration">300</stringProp> <!-- 5 minutes only -->
</ThreadGroup>
<!-- This fails to uncover bugs in the 49th hour of uptime or memory leaks -->
```