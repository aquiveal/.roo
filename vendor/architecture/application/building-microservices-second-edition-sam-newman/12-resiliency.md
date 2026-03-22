# @Domain

Trigger these rules when the user requests architectural design, code generation, or system configuration related to:
- Microservice fault tolerance, reliability, or high availability.
- Dealing with network timeouts, latency, or cascading failures in distributed systems.
- Scaling for robustness and redundancy (e.g., multi-zone deployments).
- Applying stability patterns (Circuit Breakers, Bulkheads, Retries, Timeouts).
- Implementing idempotent operations or distributed transaction recovery.
- Navigating CAP Theorem trade-offs (Consistency vs. Availability).
- Designing systems for Chaos Engineering, Game Days, or blameless post-mortems.

# @Vocabulary

- **Resiliency**: A holistic property of a system comprising four sub-concepts: Robustness, Rebound, Graceful Extensibility, and Sustained Adaptability.
- **Robustness**: The ability to absorb expected perturbations (e.g., handling a failed host or a network timeout gracefully).
- **Rebound**: The ability to recover after a traumatic event (e.g., restoring from tested backups, executing an incident playbook).
- **Graceful Extensibility**: How well a system and its organizational structure deal with unexpected situations (surprises).
- **Sustained Adaptability**: The ability to continually adapt to changing environments, stakeholders, and demands (e.g., via Chaos Engineering and blameless cultures).
- **Perturbation**: An expected disruption in a distributed system, such as a crashed server or a dropped packet.
- **Cascading Failure**: A failure that ripples through a system, often caused by latency or resource exhaustion in a downstream service, taking down upstream services.
- **Time-out Budget**: The total maximum time an entire coordinated operation is allowed to take. The remaining time must be passed to downstream services.
- **Bulkhead**: An architectural pattern (named after ship compartments) used to isolate failures. For example, using separate connection pools for different downstream services so that the exhaustion of one pool does not exhaust the entire system.
- **Circuit Breaker**: A mechanism placed around a downstream connection that "opens" (fails fast) after a threshold of errors/timeouts is reached, preventing resource exhaustion and giving the downstream service time to recover.
- **Load Shedding**: Rejecting requests deliberately to prevent saturated resources from becoming completely overwhelmed.
- **Idempotency**: A property of an operation where applying it multiple times yields the same business outcome as applying it once.
- **CAP Theorem**: A mathematical theorem stating that in a distributed system experiencing a network partition (P), you must choose between Consistency (C) and Availability (A).
- **AP System**: A system that sacrifices consistency for availability during a partition (Eventual Consistency).
- **CP System**: A system that sacrifices availability to ensure strict consistency during a partition.
- **Chaos Engineering**: The discipline of experimenting on a system in order to build confidence in its capability to withstand turbulent conditions in production.
- **Game Day**: A planned exercise to simulate outages and test people, processes, and systems.
- **Blameless Post-Mortem**: An incident review process focused on systemic causes and learning rather than punishing human error.

# @Objectives

- **Assume Inevitable Failure**: Design the system under the absolute assumption that hardware will fail, networks will partition, and downstream services will become latent or crash.
- **Prevent Cascading Failures**: Ensure that a slow or failing downstream microservice cannot exhaust the resources of upstream microservices. Latency kills.
- **Degrade Gracefully**: Determine the business context of an outage and provide a degraded user experience (e.g., hiding a shopping cart but still showing the catalog) rather than a hard failure.
- **Implement Explicit Stability Patterns**: Universally apply Time-Outs, Retries, Bulkheads, and Circuit Breakers on all out-of-process network calls.
- **Design for Safe Retries**: Ensure all inter-service operations are idempotent to safely handle retries on transient network failures.
- **Embrace the CAP Theorem**: Consciously decide per microservice (or per operation) whether to favor Availability (AP) or Consistency (CP). Default to AP where real-world business logic allows.
- **Foster a Resilient Culture**: Prioritize Mean Time To Repair (MTTR), tested backups, observability, and blameless continuous learning over attempting to achieve infinite Mean Time Between Failures (MTBF).

# @Guidelines

## General Architecture and Cross-Functional Requirements (CFRs)
- MUST elicit and explicitly define CFRs (Response time/latency percentiles, Availability guarantees, Durability of data).
- MUST translate CFRs into explicit Service-Level Objectives (SLOs) to guide scaling and robustness decisions.
- MUST implement graceful degradation logic for every customer-facing interface that aggregates multiple microservices. If one service is down, the others MUST continue to render their portions of the interface.

## Stability Patterns Implementation
- **Time-Outs**: 
  - MUST set a default time-out on EVERY out-of-process call. Never use infinite blocking waits.
  - MUST base time-out thresholds on "normal" healthy response times.
  - MUST calculate and pass a "time-out budget" across downstream calls. If an overall operation is allowed 1000ms, and 300ms has elapsed, downstream calls MUST NOT be allowed more than 700ms combined.
- **Retries**: 
  - MUST only retry on transient, recoverable errors (e.g., HTTP 503 Service Unavailable, 504 Gateway Timeout).
  - MUST NOT retry on deterministic client errors (e.g., HTTP 404 Not Found, 400 Bad Request).
  - MUST implement a delay/backoff between retries to prevent bombarding a struggling downstream service.
  - MUST count retry time against the overall operation time-out budget. Stop retrying if the budget is exhausted.
- **Bulkheads**:
  - MUST allocate separate connection pools/thread pools for distinct downstream services.
  - MUST NOT share a single global HTTP connection pool across multiple differing outbound integration points.
- **Circuit Breakers**:
  - MUST wrap all synchronous downstream calls in a Circuit Breaker.
  - MUST configure the Circuit Breaker to "open" (fail fast) after a defined threshold of consecutive timeouts or 5xx errors.
  - MUST configure the Circuit Breaker to periodically send probe requests (half-open state) to detect when the downstream service has recovered.
  - MAY manually "open" circuit breakers during planned maintenance to safely take a downstream microservice offline.
- **Idempotency**:
  - MUST design API contracts and event payloads to be idempotent.
  - MUST include unique contextual identifiers (e.g., Transaction ID, Order ID) in payloads so the receiving service can detect and ignore duplicate processing.
  - MUST note that idempotency applies to the business operation; logging the duplicate call and updating monitoring metrics MUST still occur.

## Data and State (CAP Theorem)
- MUST identify whether an operation requires CP (Consistency) or AP (Availability) during a network partition.
- MUST favor AP (Eventual Consistency) for real-world modeled data where possible, as absolute consistency is often an illusion in physical logistics.
- MUST NOT build custom distributed consistent data stores or custom distributed locking mechanisms. If CP is strictly required, use proven off-the-shelf CP systems (e.g., Consul for configuration, Spanner for relational data).
- MUST explicitly design for the reconciliation of eventually consistent data.

## Redundancy and Isolation
- MUST deploy multiple instances of any microservice running in production to handle host failures.
- MUST distribute instances across multiple physical fault domains (e.g., AWS Availability Zones).
- MUST isolate microservices logically and physically (e.g., separate containers, separate databases, independent compute resources) to prevent "noisy neighbor" resource exhaustion.

## Recovery and Culture (Rebound & Adaptability)
- MUST treat backups as non-existent ("Schrödinger's backup") until they are actively and routinely tested via restoration.
- MUST script infrastructure as code (IaC) to allow rapid, automated recreation of microservice instances from scratch following a compromise or failure.
- MUST build systemic hooks for Chaos Engineering (e.g., terminating instances randomly) to continuously validate robustness.
- MUST prioritize logging, correlation IDs, and tracing to assist humans in diagnosing unexpected failures quickly.
- MUST design alerts to be actionable and prioritized, avoiding alert fatigue.

# @Workflow

When architecting or writing code for a distributed microservice operation, the AI MUST execute the following algorithmic process:

1. **Analyze the Distributed Operation**:
   - Identify the initiating trigger (user request, event).
   - Trace the synchronous and asynchronous downstream dependencies required to fulfill the operation.

2. **Define CFRs and Budgets**:
   - Establish the latency target for the overall operation.
   - Assign a Time-out Budget.
   - Determine the data durability and availability requirements.

3. **Design the Degradation Strategy**:
   - Evaluate: "What happens if downstream Service X is down or latent?"
   - Define the fallback behavior (e.g., return cached data, return partial UI, queue for later, or fail the entire operation gracefully).

4. **Apply Stability Patterns (Code Generation)**:
   - *Isolate*: Assign a dedicated Bulkhead (connection pool) for the downstream call.
   - *Protect*: Wrap the call in a Circuit Breaker.
   - *Bound*: Apply a strict Time-out to the HTTP/RPC client, subtracting elapsed time from the overall Time-out Budget.
   - *Retry*: Add a conditional retry loop with backoff exclusively for 503/504/Timeout errors.
   - *Idempotent*: Ensure the request payload includes a unique idempotency key.

5. **Determine CAP Theorem Trade-off**:
   - Evaluate if the state mutation requires strict multi-node Consistency (CP) or if Eventual Consistency (AP) is acceptable.
   - If CP is required, select an appropriate consensus-backed data store and accept reduced availability.
   - If AP is chosen, design the asynchronous reconciliation or background sync logic.

6. **Establish Redundancy & Rebound**:
   - Ensure the deployment configuration (e.g., Kubernetes Deployment/Helm) specifies multiple replicas spread across multi-AZ node pools.
   - Ensure data stores are configured for automated backups with documented restore testing procedures.

# @Examples (Do's and Don'ts)

## 1. Time-outs and Budgets
- **[DO]**: Pass the remaining time budget to downstream services and use strict local timeouts.
  ```python
  def fetch_user_data(user_id, remaining_budget_ms):
      start_time = time.time()
      timeout_for_this_call = min(remaining_budget_ms, MAX_LOCAL_TIMEOUT_MS)
      
      try:
          response = http_client.get(f"/users/{user_id}", timeout=timeout_for_this_call)
          return response.json()
      except TimeoutException:
          return get_fallback_user_data(user_id)
  ```
- **[DON'T]**: Use default HTTP clients without timeouts, or wait infinitely for a slow downstream service, which causes thread exhaustion.
  ```python
  # Anti-pattern: No timeout, blocks infinitely if downstream is latent
  response = requests.get(f"http://legacy-ad-system.local/ads") 
  ```

## 2. Bulkheads
- **[DO]**: Configure separate connection pools for different downstream services.
  ```java
  // Good: Isolated thread pools prevent one slow service from consuming all threads
  @HystrixCommand(fallbackMethod = "fallbackAds", 
                 threadPoolKey = "AdServicePool", 
                 threadPoolProperties = { @HystrixProperty(name = "coreSize", value = "10") })
  public AdResponse fetchAds() {
      return adClient.getAds();
  }
  ```
- **[DON'T]**: Share a single global HTTP client/thread pool for the entire application, allowing a slow, low-priority service (e.g., the "turnip ad system") to take down the critical purchase flow.

## 3. Circuit Breakers and Retries
- **[DO]**: Retry only on transient errors with backoff, and open the circuit breaker if the service is truly unhealthy.
  ```javascript
  // Good: Retries specifically on 503/504, uses backoff, wrapped in a circuit breaker
  const breaker = new CircuitBreaker({ failureThreshold: 5, resetTimeout: 10000 });
  
  async function callInventory(itemId) {
      return breaker.fire(async () => {
          for (let attempt = 1; attempt <= 3; attempt++) {
              let res = await fetch(`/inventory/${itemId}`, { timeout: 1000 });
              if (res.ok) return res.json();
              if (res.status !== 503 && res.status !== 504) throw new Error("Deterministic error");
              await sleep(attempt * 500); // Backoff
          }
          throw new Error("Retries exhausted");
      });
  }
  ```
- **[DON'T]**: Blindly retry on 404s or 400s, or retry instantly without delays in a tight loop, effectively accidentally DDoSing the downstream service.

## 4. Idempotency
- **[DO]**: Use unique transaction/action IDs to ensure a retry does not duplicate a business operation.
  ```json
  // Good: Includes a specific context/reason to make the point credit idempotent
  {
    "credit": {
      "amount": 100,
      "forAccount": "1234",
      "reason": {
        "forPurchaseId": "ORDER-4567"
      }
    }
  }
  ```
- **[DON'T]**: Send contextless mutations that result in double-processing if the network times out but the original request succeeded.
  ```json
  // Anti-pattern: Non-idempotent. If retried, user gets 200 points.
  {
    "credit": 100,
    "accountId": "1234"
  }
  ```

## 5. CAP Theorem
- **[DO]**: Accept Eventual Consistency (AP) for operations involving physical reality, knowing out-of-sync data can be rectified asynchronously (e.g., apologizing to a user if an inventory item is later found to be broken in the physical warehouse).
- **[DON'T]**: Attempt to build custom distributed locking over multiple microservice databases to force CP, leading to massive latency, deadlocks, and total systemic failure during network partitions.