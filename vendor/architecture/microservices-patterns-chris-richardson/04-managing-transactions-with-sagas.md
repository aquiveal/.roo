# @Domain
These rules MUST trigger when the AI is tasked with designing, architecting, refactoring, or implementing cross-service transactions, distributed data management, or multi-service data consistency in a microservice architecture. Activation is mandatory when user requests involve terms such as "distributed transaction", "Saga", "eventual consistency", "choreography", "orchestration", "compensating transaction", or "Eventuate Tram Saga framework".

# @Vocabulary
- **Saga**: A message-driven sequence of local transactions used to maintain data consistency across microservices.
- **Local Transaction**: An ACID transaction executed within the boundaries of a single microservice and its private database.
- **Compensating Transaction**: A transaction explicitly designed to undo the effects of a previously executed local transaction within a saga if a subsequent step fails.
- **Choreography**: A saga coordination strategy where there is no central controller; participants subscribe to each other's events and respond accordingly.
- **Orchestration**: A saga coordination strategy where a centralized controller (Saga Orchestrator) tells the saga participants what local transactions to execute using command/async-reply messages.
- **Saga Orchestrator**: A class or component modeled as a state machine that sequences the execution of a saga's transactions.
- **ACD**: Atomicity, Consistency, Durability. Sagas possess these traits but lack Isolation (the "I" in ACID).
- **Anomaly**: A data inconsistency caused by the lack of isolation between concurrently executing sagas (e.g., Lost Updates, Dirty Reads, Fuzzy/Nonrepeatable Reads).
- **Countermeasure**: A design technique used to prevent or reduce the business impact of concurrency anomalies caused by the lack of isolation.
- **Compensatable Transaction**: A transaction in a saga that can potentially be rolled back (using a compensating transaction) because a subsequent step might fail.
- **Pivot Transaction**: The go/no-go point in a saga. If the pivot transaction commits, the saga is guaranteed to run until completion. It is the last compensatable transaction or the first retriable transaction.
- **Retriable Transaction**: A transaction that follows the pivot transaction and is guaranteed to succeed.
- **Semantic Lock**: A countermeasure where a compensatable transaction sets a flag (e.g., a `_PENDING` state) in a record to indicate it is currently under modification by a saga.
- **Commutative Updates**: A countermeasure where update operations are designed to be executable in any order.
- **Pessimistic View**: A countermeasure that reorders the steps of a saga to minimize the business risk of dirty reads.
- **Reread Value**: A countermeasure (optimistic offline lock) where a saga rereads a record before updating it to prevent lost updates.
- **Version File**: A countermeasure that records the sequence of operations on a record so they can be reordered correctly.
- **By Value**: A countermeasure that dynamically selects the concurrency mechanism based on the business risk of the specific request.
- **Correlation ID**: A unique identifier included in messages/events to map received events back to the saga instance or local data.

# @Objectives
- The AI MUST ensure data consistency across multiple microservices without utilizing traditional, synchronous distributed transactions (e.g., 2PC, XA).
- The AI MUST decouple microservices during transaction execution by enforcing asynchronous messaging instead of synchronous interprocess communication (IPC).
- The AI MUST guarantee eventual consistency by implementing sagas with properly structured compensating transactions to handle business rule violations or failures.
- The AI MUST proactively mitigate the lack of isolation inherent in sagas (ACD model) by applying explicit design countermeasures to prevent data anomalies.

# @Guidelines

## Architectural Constraints and Anti-Patterns
- **No Distributed Transactions (2PC)**: The AI MUST NOT use two-phase commit (2PC) or XA transactions to span multiple microservices. 
- **No Synchronous Coupling in Sagas**: The AI MUST NOT implement saga coordination using synchronous protocols like REST or gRPC blocking calls, as this degrades availability and violates the CAP theorem's emphasis on availability/partition-tolerance.
- **No Shared Databases**: The AI MUST respect database-per-service boundaries. Sagas MUST be used whenever an operation spans multiple bounded contexts.

## Saga Coordination Selection
- **Evaluate Complexity**: The AI MUST choose between Choreography and Orchestration based on saga complexity.
- **When to Use Choreography**: The AI MUST use Choreography ONLY for simple, short sagas (e.g., 2-3 steps) where a centralized orchestrator is overkill.
- **When to Use Orchestration**: The AI MUST use Orchestration for complex sagas to avoid cyclic dependencies between services and to keep saga coordination logic centralized and understandable.

## Designing Choreography-Based Sagas
- **Event Exchange**: The AI MUST implement Choreography by having participants publish domain events upon completing local transactions, which in turn trigger subsequent participants' event handlers.
- **Transactional Messaging**: The AI MUST ensure that updating the local database and publishing the event occur atomically using Transactional Messaging (e.g., Transactional Outbox pattern).
- **Correlation IDs**: The AI MUST include Correlation IDs in all published events so downstream participants can map events to their respective local data/aggregates.

## Designing Orchestration-Based Sagas
- **State Machine Modeling**: The AI MUST model Saga Orchestrators as state machines, explicitly defining states, transitions, and the events/replies that trigger those transitions.
- **Command/Async-Reply**: The AI MUST implement Orchestrator communication using asynchronous request/response. The orchestrator sends command messages to participant channels and listens for reply messages on a dedicated orchestrator reply channel.
- **Participant Proxy Classes**: The AI MUST define Proxy classes for saga participants (e.g., `KitchenServiceProxy`) to establish statically typed messaging endpoints (channels, command types, expected reply types) instead of hardcoding channels in the orchestrator.
- **Dumb Participants, Smart Orchestrator**: The AI MUST localize coordination logic within the orchestrator. Domain objects/participants MUST NOT possess knowledge of the saga orchestrator.

## Structuring the Saga and Compensating Transactions
- **Categorize Transactions**: For every saga, the AI MUST explicitly categorize all steps into:
  1. Compensatable transactions
  2. Pivot transaction
  3. Retriable transactions
- **Reverse Execution for Compensation**: If step N fails, the AI MUST orchestrate compensating transactions for steps N-1 down to 1 in reverse order (C_n-1 ... C_1).
- **Read-Only Exclusions**: The AI MUST NOT generate compensating transactions for read-only steps or for retriable transactions.

## Implementing Isolation Countermeasures
- **Identify Anomalies**: The AI MUST analyze the saga for potential Lost Updates, Dirty Reads, and Fuzzy Reads.
- **Apply Semantic Locks**: The AI MUST apply the Semantic Lock countermeasure to compensatable transactions by introducing `_PENDING` states (e.g., `APPROVAL_PENDING`, `CREATE_PENDING`) to domain entities.
- **Handle Locked Records**: When a client requests an operation on a record in a `_PENDING` state, the AI MUST decide whether to fail fast (returning an error to the client) or block the request until the semantic lock is cleared by the saga's completion or compensation.
- **Apply Reread Value**: To prevent lost updates, the AI MUST implement optimistic offline locking (Reread Value), re-checking entity versions before committing the final retriable transaction of a saga.

# @Workflow
When tasked with designing or implementing a transaction that spans multiple microservices, the AI MUST adhere to the following rigid algorithm:

1. **Operation Identification**: Identify the system command/operation that requires updates across multiple bounded contexts (services).
2. **Saga Step Mapping**: Break the operation down into a linear sequence of local ACID transactions, mapping each transaction to its respective microservice.
3. **Transaction Classification**:
   - Identify the point of no return: mark this as the *Pivot Transaction*.
   - Mark all preceding steps as *Compensatable Transactions*.
   - Mark all subsequent steps as *Retriable Transactions*.
4. **Compensation Mapping**: For every Compensatable Transaction, define the exact *Compensating Transaction* required to logically undo it.
5. **Coordination Strategy Selection**:
   - Assess saga length and risk of cyclic dependencies.
   - Select *Orchestration* unless the saga is exceptionally simple, then select *Choreography*.
6. **Countermeasure Application**:
   - Evaluate the risk of concurrent access to the involved aggregates.
   - Implement the *Semantic Lock* countermeasure by adding `_PENDING` states to the initial aggregates modified in the compensatable transactions.
   - Apply *Reread Value* (optimistic locking) to final state updates.
7. **Implementation Definition**:
   - *If Orchestration*: Define the State Machine (states, transitions, actions). Define Participant Proxy classes. Define Command and Reply messages.
   - *If Choreography*: Define the Domain Events published by each service and the corresponding Event Handlers in downstream services.
8. **Failure Path Verification**: Trace the failure of the Pivot Transaction and every Compensatable Transaction to ensure the compensating transactions reverse the state back to a consistent baseline (e.g., transitioning from `APPROVAL_PENDING` to `REJECTED`).

# @Examples (Do's and Don'ts)

## Saga Coordination
- **[DON'T]** Use REST calls synchronously to update multiple services.
```java
// ANTI-PATTERN: Synchronous Distributed Transaction using REST
@Transactional
public void createOrder(OrderDetails details) {
    Order order = orderRepository.save(new Order(details));
    // Blocking HTTP call to Kitchen Service
    kitchenServiceClient.createTicket(order.getId(), details);
    // Blocking HTTP call to Accounting Service
    accountingServiceClient.authorize(order.getConsumerId());
}
```

- **[DO]** Use an Orchestrator with asynchronous messaging to coordinate local transactions.
```java
// CORRECT: Creating a Saga Orchestrator to handle the transaction asynchronously
@Transactional
public Order createOrder(OrderDetails orderDetails) {
    Order order = Order.createOrder(orderDetails);
    orderRepository.save(order);
    
    CreateOrderSagaState data = new CreateOrderSagaState(order.getId(), orderDetails);
    // Persists the saga state and asynchronously sends the first command message
    createOrderSagaManager.create(data, Order.class, order.getId());
    
    return order;
}
```

## Isolation Countermeasures (Semantic Lock)
- **[DON'T]** Immediately transition a domain entity to an active/approved state when the cross-service transaction is not yet complete.
```java
// ANTI-PATTERN: No isolation. Entity is "APPROVED" before payment is verified.
public Order(OrderDetails orderDetails) {
    this.state = OrderState.APPROVED; // Vulnerable to dirty reads!
}
```

- **[DO]** Implement a Semantic Lock using a `_PENDING` state until the Saga finishes.
```java
// CORRECT: Semantic Lock countermeasure applied
public Order(OrderDetails orderDetails) {
    // Lock the record conceptually. Other sagas/clients know it is incomplete.
    this.state = OrderState.APPROVAL_PENDING; 
}

public void noteApproved() {
    if (this.state == OrderState.APPROVAL_PENDING) {
        this.state = OrderState.APPROVED; // Clears the lock (Retriable transaction)
    }
}

public void noteRejected() {
    if (this.state == OrderState.APPROVAL_PENDING) {
        this.state = OrderState.REJECTED; // Clears the lock (Compensating transaction)
    }
}
```

## Orchestration State Machine Definitions
- **[DON'T]** Hardcode message channels and JSON strings directly in the orchestrator logic.
- **[DO]** Use a typed DSL and Participant Proxy classes to define the Saga routing and compensation logic.
```java
// CORRECT: Saga Definition using a State Machine DSL and Proxy classes
public class CreateOrderSaga implements SimpleSaga<CreateOrderSagaState> {
    private SagaDefinition<CreateOrderSagaState> sagaDefinition;

    public CreateOrderSaga(KitchenServiceProxy kitchenService, AccountingServiceProxy accountingService) {
        this.sagaDefinition = step()
            .withCompensation(orderService.reject, CreateOrderSagaState::makeRejectOrderCommand)
            .step()
            // Forward transaction (Compensatable)
            .invokeParticipant(kitchenService.create, CreateOrderSagaState::makeCreateTicketCommand)
            .onReply(CreateTicketReply.class, CreateOrderSagaState::handleCreateTicketReply)
            // Compensating transaction mapping
            .withCompensation(kitchenService.cancel, CreateOrderSagaState::makeCancelCreateTicketCommand)
            .step()
            // Pivot transaction
            .invokeParticipant(accountingService.authorize, CreateOrderSagaState::makeAuthorizeCommand)
            .build();
    }
}
```