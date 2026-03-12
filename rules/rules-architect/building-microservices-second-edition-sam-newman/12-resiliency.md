# @Domain
These rules MUST trigger when the AI is engaged in tasks involving the architecture, design, implementation, code review, or troubleshooting of distributed systems, microservices, network communication protocols, incident response, post-mortem analysis, or system scaling and infrastructure provisioning.

# @Vocabulary
- **Resiliency**: A holistic system property comprising Robustness, Rebound, Graceful Extensibility, and Sustained Adaptability.
- **Robustness**: The ability of a system to absorb expected perturbations (e.g., host failures, network timeouts) via mechanisms put in place using foresight or hindsight.
- **Rebound**: The ability of a system and its people to recover after a traumatic event or outage (e.g., via backups, playbooks, disaster recovery plans).
- **Graceful Extensibility**: The ability of a system and its organization to handle unexpected situations (surprises), typically relying on distributed responsibility rather than rigid automation.
- **Sustained Adaptability**: The continuous investment in adapting to changing environments, stakeholders, and demands to prevent future fragility.
- **Cross-Functional Requirements (CFRs)**: System properties often termed "non-functional requirements", including response time/latency percentiles, availability guarantees, and data durability.
- **Degrading Functionality**: The practice of allowing a system to partially function (e.g., hiding a UI element or using default data) when a downstream dependency fails, rather than bringing down the entire operation.
- **Cascading Failure**: A failure state where one malfunctioning component (especially one acting slowly) exhausts shared resources, causing upstream systems to fail sequentially.
- **Time-Out Budget**: The maximum total time allocated for an overarching operation, which must be passed down and respected across a chain of synchronous service calls.
- **Bulkhead**: An architectural pattern that isolates failures into separate compartments (e.g., separate connection pools for different downstream services) to prevent a localized failure from sinking the entire system.
- **Load Shedding**: The act of intentionally rejecting requests to protect a system's core resources from becoming completely saturated.
- **Circuit Breaker**: An automated mechanism that wraps downstream calls; it "opens" (trips) after a threshold of failures or timeouts is reached, failing fast on subsequent calls to protect the downstream service and free up upstream resources.
- **Idempotency**: The property of an operation where applying it multiple times yields the exact same outcome as applying it once. Essential for safe retries.
- **CAP Theorem**: The principle that a distributed system can only provide two of three guarantees: Consistency (C), Availability (A), and Partition Tolerance (P). In distributed networks, P is mandatory, leaving a choice between AP and CP.
- **AP System**: A distributed system that sacrifices strong consistency in favor of availability and partition tolerance, yielding Eventual Consistency.
- **CP System**: A distributed system that sacrifices availability to guarantee strong consistency across partitions, typically refusing to respond if nodes cannot synchronize.
- **Chaos Engineering**: The discipline of running experiments (e.g., randomly terminating instances) on a production system to build confidence in its capability to withstand turbulent conditions.
- **Game Days**: Planned organizational exercises simulating disaster scenarios to test human and technical rebound capabilities.
- **Blameless Post-Mortem**: An incident review process that explicitly avoids assigning human blame, focusing instead on systemic flaws and fostering a culture of psychological safety and learning.

# @Objectives
- **Assume Failure**: The AI must treat all hardware, networks, and downstream services as inherently unreliable and prone to failure or severe latency.
- **Prevent Cascading Failures**: The AI must prioritize system stability over absolute feature completeness by isolating faults and failing fast.
- **Enforce State Safety**: The AI must ensure that network operations can be safely retried without corrupting system state.
- **Explicit Trade-offs**: The AI must force explicit architectural decisions regarding Consistency versus Availability (CAP Theorem) based on specific business capabilities.
- **Promote Human-Centric Resilience**: The AI must design systems that aid human operators during crises, avoiding alert fatigue and eliminating blame-focused root cause analysis.

# @Guidelines

## General Resiliency & Failure Assumptions
- The AI MUST design all microservice interactions under the assumption that the network will fail, packets will be lost, and downstream instances will disappear without warning.
- The AI MUST evaluate scaling and architecture proposals against all four resiliency axes: Robustness, Rebound, Graceful Extensibility, and Sustained Adaptability.
- The AI MUST NOT treat system health as a binary "up or down" state, but as a spectrum requiring nuanced degradation strategies.

## Cross-Functional Requirements (CFRs)
- When proposing an architecture, the AI MUST request or define explicit CFRs, specifically: Response time/latency (measured in percentiles, e.g., 90th percentile), Availability (uptime requirements), and Durability of data (acceptable data loss and retention periods).

## Degrading Functionality
- For any user-facing feature relying on multiple microservices, the AI MUST explicitly define the fallback behavior if any single dependency is unavailable.
- The AI MUST prefer returning cached data, default values, or hiding UI elements over failing the entire user request (e.g., throwing a 500 error for the whole page).

## Time-Outs
- The AI MUST apply time-outs to ALL out-of-process (network) calls.
- The AI MUST define a default time-out strategy and adjust it based on the expected "normal" healthy response time of the downstream service.
- The AI MUST track an overarching Time-Out Budget for chained synchronous calls. If the global budget is exceeded, the AI MUST abort the operation rather than initiating further downstream calls.

## Retries
- The AI MUST limit retries to transient errors (e.g., HTTP 503 Service Unavailable, 504 Gateway Timeout, or network drops).
- The AI MUST NOT initiate retries for client errors (e.g., HTTP 400, 404).
- The AI MUST enforce a delay (backoff) between retries to avoid bombarding a struggling downstream service.
- The AI MUST factor retry delays into the overall Time-Out Budget.

## Bulkheads
- The AI MUST NOT use a single, shared connection pool for all outbound network requests in a service.
- The AI MUST isolate resources by implementing separate connection pools (Bulkheads) for each downstream dependency.
- The AI MUST utilize Bulkheads to implement Load Shedding, aggressively rejecting inbound requests when a compartment reaches capacity.

## Circuit Breakers
- The AI MUST wrap all synchronous downstream network calls in a Circuit Breaker.
- The AI MUST configure Circuit Breakers to "open" (blow) upon reaching a threshold of timeouts or 5XX errors, instantly failing subsequent calls.
- When a Circuit Breaker is open, the AI MUST define whether to queue the request for later (if asynchronous) or fail fast and degrade the UI gracefully.

## Idempotency
- The AI MUST design all state-mutating endpoints and event consumers to be idempotent.
- The AI MUST use unique transaction identifiers, request IDs, or correlation IDs to detect and ignore duplicate requests safely.

## CAP Theorem & Data Consistency
- The AI MUST NOT attempt to invent or implement custom CP (Consistent/Partition Tolerant) distributed data stores or distributed locking algorithms. It MUST rely on proven off-the-shelf solutions (e.g., Consul, ZooKeeper) if strict CP is required.
- The AI MUST explicitly decide whether a service/operation requires AP (Availability) or CP (Consistency) and document the business justification.
- The AI MUST default to AP (Eventual Consistency) for high-scale, distributed microservices unless strict transactional consistency (e.g., financial ledger balances) is a hard business requirement.

## Isolation & Redundancy
- The AI MUST NOT place multiple instances of the same microservice on the same physical host, underlying VM, or single point of failure.
- The AI MUST configure deployments to span multiple availability zones or data centers to protect against facility-level outages.

## Chaos Engineering & Blameless Culture
- When drafting incident response plans or post-mortems, the AI MUST use blameless language, focusing exclusively on systemic vulnerabilities, lack of guardrails, and process failures rather than "human error."
- The AI MUST recommend Chaos Engineering practices (e.g., Game Days, Chaos Monkey) to validate Robustness and test Rebound strategies in production environments.

# @Workflow
When tasked with designing a new distributed workflow, integrating a microservice, or analyzing a system failure, the AI must follow this rigid algorithmic process:

1. **Identify Dependencies:** Map every out-of-process network call (databases, message brokers, downstream microservices) involved in the workflow.
2. **Define CFRs:** Establish the acceptable latency percentiles, availability targets, and overarching time-out budget for the entire operation.
3. **Apply Stability Patterns (Per Dependency):**
   - Assign a specific time-out value based on expected normal behavior.
   - Wrap the call in a dedicated Bulkhead (isolated connection pool/thread pool).
   - Wrap the call in a Circuit Breaker configured to trip on timeouts/5XX errors.
   - Define the retry policy (which HTTP codes trigger a retry, backoff duration, maximum attempts).
4. **Enforce Idempotency:** Ensure the receiving service utilizes a unique key to process retried requests safely without duplicating state mutations.
5. **Determine Degradation Strategy:** For each dependency, explicitly define what the primary service returns or does if the circuit breaker is open or the call fails (e.g., return stale cache, hide UI component, queue for later).
6. **Evaluate Data Consistency (CAP):** Categorize the data storage interaction as AP or CP. If AP, design the compensation/eventual consistency mechanism. If CP, select the appropriate off-the-shelf consensus tool.
7. **Review Redundancy:** Ensure the architectural topology explicitly mandates deployment across multiple availability zones.
8. **Document Failure Modes:** Output a matrix of expected failure modes and the system's automated response (Robustness) and human response (Rebound) to each.

# @Examples (Do's and Don'ts)

## Timeouts and Budgets
- **[DO]**: Pass a `remaining_timeout_ms` header to downstream services. Check `if (remaining_timeout_ms <= 0) abort();` before initiating an expensive database query.
- **[DON'T]**: Hardcode a 30-second timeout on a downstream HTTP call for a user-facing web request, causing the thread to block while the user repeatedly refreshes the page.

## Bulkheads and Connection Pools
- **[DO]**: Configure three separate HTTP client instances with independent thread pools for `ServiceA`, `ServiceB`, and `ServiceC`.
- **[DON'T]**: Use a single global `HttpClient` or connection pool where a slow response from `ServiceC` exhausts all threads, preventing calls to `ServiceA` and `ServiceB`.

## Idempotency
- **[DO]**: Accept a POST request containing a `transaction_id`. Check the database for `transaction_id`; if it exists, return `200 OK` with the existing result. If not, process the mutation.
- **[DON'T]**: Blindly increment a user's loyalty points by 100 every time the `POST /loyalty/credit` endpoint is hit, causing duplicated points if the network drops and the client retries.

## Circuit Breakers & Degradation
- **[DO]**: When the Recommendation service trips its circuit breaker, catch the `CircuitBreakerOpenException` and return an empty list `[]`, allowing the UI to render the shopping cart without recommendations.
- **[DON'T]**: Allow the exception from the Recommendation service to bubble up to the global error handler, resulting in a 500 error page that prevents the user from checking out.

## Post-Mortem Analysis
- **[DO]**: "The incident occurred because the database deployment script lacked a confirmation prompt and the system allowed destructive actions without a secondary verification."
- **[DON'T]**: "The outage was caused by human error when Bob accidentally ran the wrong script and deleted the production tables."