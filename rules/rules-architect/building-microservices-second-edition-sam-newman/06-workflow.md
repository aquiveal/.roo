# @Domain
These rules MUST trigger whenever the AI is tasked with designing, architecting, or implementing a business process, state change, or workflow that spans multiple microservices, requires coordination across multiple databases, or handles Long Lived Transactions (LLTs).

# @Vocabulary
- **ACID**: Atomicity, Consistency, Isolation, and Durability. Properties of local database transactions. In microservices, these properties apply locally but are lost at the global/cross-service level.
- **Distributed Transaction / 2PC (Two-Phase Commit)**: An algorithm that attempts to provide transactional safety across multiple distinct processes using a voting phase and a commit phase. Highly prone to blocking and fragility.
- **Saga**: An algorithm for coordinating multiple changes in state across a distributed system without locking resources for long periods. Breaks a long-lived transaction into a sequence of independent local transactions.
- **LLT (Long Lived Transaction)**: A transaction that might take minutes, hours, or days to complete, making standard database locking mechanisms unviable. 
- **Backward Recovery**: Reverting a failure and cleaning up afterward (rolling back).
- **Forward Recovery**: Picking up from the point where a failure occurred and keeping processing (retrying).
- **Compensating Transaction**: An operation that undoes a previously committed local transaction within a Saga (a semantic rollback).
- **Semantic Rollback**: A compensating action that addresses a past transaction in a business sense (e.g., sending a cancellation email rather than "unsending" the original email).
- **Orchestrated Saga**: A centralized command-and-control approach where a central coordinator (orchestrator) directs collaborating services on what to do and tracks the workflow's state.
- **Choreographed Saga**: A decentralized trust-but-verify approach where responsibility is distributed. Services react to broadcasted events without a central coordinator.
- **Correlation ID**: A unique identifier attached to a workflow and passed along all subsequent calls and events to allow tracing of the Saga's state across multiple services.
- **BPM (Business Process Modeling) Tools**: Visual drag-and-drop tools for defining process flows. Often incompatible with developer workflows and version control.

# @Objectives
- Coordinate state changes across multiple microservices without utilizing global resource locks.
- Replace fragile, blocking distributed transactions with explicit, asynchronous Saga patterns.
- Ensure that business processes are explicitly modeled and capable of recovering from business failures gracefully.
- Maintain independent deployability and autonomy of services by strictly limiting domain coupling in workflows.

# @Guidelines
- **Reject Distributed Transactions**: The AI MUST NOT recommend, design, or implement distributed transactions (such as Two-Phase Commits/2PC) across microservices. 
- **Adopt Sagas for Workflows**: The AI MUST use Sagas to handle state changes that span multiple services.
- **Differentiate Business vs. Technical Failures**: Sagas MUST be used to recover from business failures (e.g., "insufficient funds"). Technical failures (e.g., "500 Internal Server Error" or network timeouts) MUST be handled via technical reliability patterns (retries, circuit breakers) rather than Saga rollbacks.
- **Design Compensating Transactions**: For any step in a Saga that modifies state, the AI MUST define a semantic compensating transaction if backward recovery is required.
- **Optimize Step Ordering**: The AI SHOULD sequence workflow steps to defer operations that are difficult or impossible to compensate (e.g., dispatching physical goods, sending emails) to the end of the Saga.
- **Mix Recovery Modes**: The AI MAY mix fail-backward (compensating) and fail-forward (retrying) recovery mechanisms within the same Saga based on the business context.
- **Choose the Right Saga Style**:
  - The AI MUST prefer **Choreographed Sagas** (event-driven) when the workflow spans multiple teams to ensure loose coupling and autonomy.
  - The AI MAY use **Orchestrated Sagas** (request/response driven by a central service) if the entire workflow and all participating microservices are owned by a single team.
- **Avoid BPM Tools for Code**: The AI MUST NOT implement orchestrated sagas using visual BPM tools; workflows MUST be implemented in code using developer-friendly tooling and version control.
- **Prevent Anemic Services in Orchestration**: When using Orchestration, the AI MUST ensure that local business logic and state machine management remain within the downstream services, not entirely centralized in the orchestrator.
- **Mandate Correlation IDs**: The AI MUST include Correlation IDs in all requests, events, and logs associated with a choreographed or orchestrated Saga to enable state tracking and debugging.

# @Workflow
When tasked with implementing a cross-service workflow or state change, the AI MUST follow this exact algorithmic process:

1. **Identify the LLT**: Map out the entire end-to-end business process (the Long Lived Transaction).
2. **Decompose into Local Transactions**: Break the LLT down into a sequence of discrete steps, where each step represents a local ACID transaction within a single microservice.
3. **Sequence Optimization**: Reorder the steps. Move steps that are likely to fail to the beginning. Move steps that are difficult or impossible to roll back to the end.
4. **Define Failure Modes**: For each step, determine if a failure requires Backward Recovery (rollback) or Forward Recovery (retry).
5. **Design Compensating Actions**: For every step requiring Backward Recovery, define the exact semantic rollback action (Compensating Transaction) that will revert the business state.
6. **Select Implementation Style**: 
   - Ask or determine if the participating services span multiple organizational teams.
   - If multiple teams: Design a **Choreographed Saga** using event publication and subscriptions.
   - If a single team: Design an **Orchestrated Saga** using a central coordinator service.
7. **Embed Traceability**: Inject a Correlation ID generation step at the workflow's initiation and pass it through all subsequent API calls and event payloads.

# @Examples (Do's and Don'ts)

**[DO] Choreographed Saga with Compensating Transactions**
```javascript
// Service A: Order Service
function handleOrderPlacement(orderRequest) {
    const correlationId = generateCorrelationId();
    const order = createPendingOrder(orderRequest);
    
    // Broadcast event for other services to react to (Choreography)
    eventBroker.publish('OrderPlaced', {
        correlationId: correlationId,
        orderId: order.id,
        customerId: order.customerId,
        amount: order.amount
    });
}

// Service B: Loyalty Service (Reacting to Event)
eventBroker.subscribe('OrderPlaced', async (event) => {
    try {
        await awardPoints(event.customerId, event.amount);
        eventBroker.publish('PointsAwarded', { correlationId: event.correlationId, orderId: event.orderId });
    } catch (error) {
        // Business failure triggers a compensating event
        eventBroker.publish('PointsAwardFailed', { correlationId: event.correlationId, orderId: event.orderId, reason: error.message });
    }
});

// Service A: Order Service (Handling the rollback semantically)
eventBroker.subscribe('PointsAwardFailed', async (event) => {
    // Compensating Transaction: Mark order as aborted instead of a DB rollback
    await abortOrder(event.orderId, event.reason);
    notifyCustomerOfCancellation(event.orderId);
});
```

**[DON'T] Distributed Transactions (2PC)**
```javascript
// ANTI-PATTERN: Attempting to lock resources across multiple services using a distributed transaction
async function processOrderDistributed(orderRequest) {
    const globalTx = new DistributedTransactionManager();
    
    try {
        globalTx.begin();
        // Locking DB rows over network calls is strictly forbidden!
        await orderService.createOrderWithLock(globalTx, orderRequest);
        await warehouseService.reserveStockWithLock(globalTx, orderRequest.itemId);
        await paymentService.deductFundsWithLock(globalTx, orderRequest.customerId);
        
        globalTx.commit(); // High latency, blocks resources globally
    } catch (e) {
        globalTx.rollback();
    }
}
```

**[DO] Optimizing Saga Step Ordering**
```text
// CORRECT STEP ORDERING
1. Check/Reserve Stock (High likelihood of failure, easy to compensate)
2. Take Payment (Medium likelihood of failure, moderate to compensate via refund)
3. Dispatch physical goods (Low likelihood of failure, extremely difficult to compensate/un-ship)
```

**[DON'T] Poor Saga Step Ordering**
```text
// ANTI-PATTERN: Dispatching goods before taking payment
1. Dispatch physical goods
2. Take Payment (If this fails, compensating the shipped physical goods is impossible)
```