# @Domain
These rules MUST be triggered whenever the AI is tasked with designing, implementing, evaluating, or refactoring business processes, state changes, or data modifications that span multiple microservices, distinct database boundaries, or distributed systems.

# @Vocabulary
*   **ACID**: Atomicity, Consistency, Isolation, and Durability. The properties of a reliable local database transaction. In microservices, ACID applies only within the boundary of a single microservice, not across them.
*   **Distributed Transaction**: An attempt to apply ACID properties across multiple independent processes/databases, typically using algorithms like Two-Phase Commit (2PC).
*   **Two-Phase Commit (2PC)**: A distributed transaction algorithm consisting of a voting phase and a commit phase, requiring long-lived locks across multiple workers.
*   **Saga**: An algorithm/pattern that coordinates multiple state changes across distributed services without requiring long-lived locks, by breaking a Long-Lived Transaction (LLT) into a sequence of discrete, independent local transactions.
*   **Long-Lived Transaction (LLT)**: A transaction that takes a significant amount of time (minutes, hours, days) where holding traditional database locks is unfeasible.
*   **Backward Recovery**: A saga failure mode strategy that reverts failures and cleans up previous steps (rollback).
*   **Forward Recovery**: A saga failure mode strategy that pauses or retries a process from the point of failure until it succeeds.
*   **Compensating Transaction (Semantic Rollback)**: An explicitly modeled operation that undoes or mitigates the effects of a previously committed local transaction within a saga (e.g., sending a cancellation email because the original email cannot be "un-sent").
*   **Orchestrated Saga**: A command-and-control saga implementation where a central coordinator (Orchestrator) explicitly directs other microservices on what to do and tracks the saga state.
*   **Choreographed Saga**: A trust-but-verify saga implementation where responsibility is distributed. Microservices react to domain events independently without a central coordinator.
*   **Correlation ID**: A unique identifier injected into logs, requests, and events used to trace a distributed workflow across multiple microservice boundaries.

# @Objectives
*   Eliminate the use of distributed database transactions and synchronous multi-service locks.
*   Model complex, multi-service business processes explicitly using the Saga pattern.
*   Ensure distributed systems can safely and predictably recover from business-logic failures using explicit forward or backward recovery mechanisms.
*   Prevent microservices from becoming "anemic" entities stripped of business logic by overly aggressive centralized orchestrators.
*   Maintain loose coupling between microservices by defaulting to choreographed, event-driven workflows where multiple teams are involved.

# @Guidelines
### Distributed Transactions & Locks
*   The AI MUST NEVER propose, design, or implement distributed transactions (such as Two-Phase Commits) to coordinate state changes across microservices.
*   The AI MUST ensure that ACID transactions are strictly scoped to the local database of a single microservice.

### Saga Design
*   The AI MUST use the Saga pattern whenever a business process requires state changes across multiple microservices.
*   The AI MUST differentiate between business failures (e.g., insufficient funds) and technical failures (e.g., network timeout) when designing recovery strategies. Sagas handle business failures; technical failures require resiliency patterns (retries, circuit breakers).
*   The AI MUST define Compensating Transactions for every step in a saga that can be semantically rolled back.
*   The AI MUST analyze the workflow steps and proactively reorder them to push operations that are difficult or impossible to roll back (e.g., sending physical mail, transferring real money) to the very end of the saga.

### Orchestration vs. Choreography
*   The AI MUST recommend **Orchestrated Sagas** ONLY when the entire workflow is owned by a single stream-aligned team, to manage the inherent domain coupling it introduces.
*   The AI MUST actively prevent the creation of "anemic" microservices. An orchestrator must NOT absorb the internal business logic or state-machine rules of the downstream services it coordinates. Downstream services MUST retain the right to reject invalid requests.
*   The AI MUST recommend **Choreographed Sagas** (event-driven) when a workflow spans multiple teams, to enforce loose coupling and preserve team autonomy.
*   The AI MUST NOT use or recommend visual Business Process Modeling (BPM) tools to abstract saga logic away from developers. Sagas MUST be modeled explicitly in code.

### Traceability and State Management
*   The AI MUST ensure that a **Correlation ID** is generated at the start of any saga and passed through all subsequent synchronous requests and asynchronous events.
*   When designing Choreographed Sagas, the AI MUST propose a mechanism (such as an event-consuming projection service) to track and visualize the overall state of the saga, mitigating the lack of a central orchestrator.

# @Workflow
When tasked with designing or refactoring a multi-service business process, the AI MUST strictly follow this algorithmic sequence:

1.  **Decompose the Workflow:** Break the overall long-lived business process down into discrete steps, mapping each step to a specific local microservice and its local ACID database transaction.
2.  **Optimize Step Ordering:** Review the sequence of local transactions. Push actions that are difficult to undo or highly likely to fail toward the end of the sequence to minimize the required rollback surface area.
3.  **Define Failure & Recovery Modes:** For each step, determine if a failure requires Backward Recovery (rollback) or Forward Recovery (retry/human intervention).
4.  **Design Compensating Transactions:** For every step requiring Backward Recovery, define the exact semantic rollback operation (e.g., if step 1 is "Reserve Stock", the compensating transaction is "Release Stock").
5.  **Determine Implementation Style:**
    *   Assess team ownership. If multiple teams own the services involved, select **Choreography**.
    *   If a single team owns the process and centralized tracking is paramount, select **Orchestration**.
    *   *Optional:* Mix styles (e.g., choreographed across major boundaries, orchestrated within a specific microservice's internal domain).
6.  **Implement Traceability:** Inject Correlation IDs into all API definitions, event payloads, and logging outputs associated with the saga.
7.  **Validate against Anemic Domain:** If using Orchestration, verify that the downstream services still control their own local state machine rules and validate inbound requests.

# @Examples (Do's and Don'ts)

### Distributed State Management
*   **[DON'T]** Use Two-Phase Commit (2PC) or distributed locks to update an Order database and a Customer database simultaneously.
*   **[DO]** Use a Saga. Commit the Order locally (Status: PENDING), emit an `OrderCreated` event, and let the Customer service consume it and update its own local database.

### Saga Recovery
*   **[DON'T]** Attempt to execute a standard database `ROLLBACK` command across a network connection when a multi-service workflow fails.
*   **[DO]** Execute a Compensating Transaction. Example: If `PaymentService` successfully charged the user, but `WarehouseService` reports `OutOfStock`, the orchestrator or event listener MUST trigger a `RefundPayment` command to the `PaymentService`.

### Optimizing Step Ordering
*   **[DON'T]** Send a "Welcome and Order Confirmed" email as step 1 of an order saga, before payment and inventory checks are completed. (You cannot un-send an email).
*   **[DO]** Process the payment (Step 1), reserve the inventory (Step 2), and ONLY trigger the Welcome Email (Step 3) once the previous steps are successfully committed.

### Orchestration Design
*   **[DON'T]** Build an `OrderOrchestrator` that calculates the inventory math, directly updates the `Inventory` table via CRUD wrappers, and forces the inventory status to change.
*   **[DO]** Build an `OrderOrchestrator` that sends a `ReserveStockRequest` to the `InventoryService`. The `InventoryService` evaluates its own state machine, performs the math, updates its local DB, and returns a `StockReserved` or `ReservationFailed` response.

### Choreography and Traceability
*   **[DON'T]** Fire isolated events (`PaymentTaken`, `ItemPackaged`) without linking data, making it impossible to know the status of an overarching user order.
*   **[DO]** Generate a `Correlation ID` (e.g., `saga_id: 998877`) at the point of order creation. Include this ID in the `OrderPlaced` event, the `PaymentTaken` event, and the `ItemPackaged` event. Build a read-model projection that consumes these events, grouping them by `Correlation ID` to provide a real-time view of the saga's state.