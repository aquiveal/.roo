@Domain
These rules MUST trigger when the AI is tasked with designing, implementing, modifying, evaluating, or debugging multi-microservice workflows, distributed transactions (Sagas), or when deciding between/implementing Choreography versus Orchestration patterns in an event-driven architecture.

@Vocabulary
- **Workflow:** A specific set of actions composing a business process, including any logical branching and compensatory actions.
- **Choreography (Reactive Architecture):** A highly decoupled architecture where microservices react to input events independently, without centralized coordination, foreknowledge of downstream consumers, or upstream producers.
- **Orchestration:** An architecture where a central microservice (the orchestrator) maintains workflow state, issues commands to, and awaits responses from subordinate worker microservices.
- **Orchestrator:** The central microservice in the orchestration pattern responsible STRICTLY for workflow logic, tracking completion, and routing.
- **Worker Microservice:** The subordinate microservice in the orchestration pattern responsible STRICTLY for executing business logic and returning success/failure results.
- **Distributed Transaction (Saga):** A transaction spanning two or more microservices. Requires each participating microservice to process its portion of the transaction and provide logic to reverse/rollback that processing if the transaction is aborted.
- **Compensation Workflow:** A business-level remedial workflow (e.g., apologizing to a customer, issuing a refund) executed in response to a workflow failure, used as an alternative to strict technical transaction rollbacks.
- **God Service Anti-Pattern:** An improperly designed orchestrator that assumes the business fulfillment logic of its worker microservices, leading to poor encapsulation and tight coupling.
- **Event-Driven Orchestration:** Orchestrator and workers communicate asynchronously via durable event streams.
- **Direct-Call Orchestration:** Orchestrator and workers communicate synchronously via request-response APIs (e.g., HTTP/REST).

@Objectives
- Determine the correct architectural workflow pattern (Choreography vs. Orchestration) based on the specific business requirements for flexibility, monitoring, and complexity.
- Maintain strict boundaries of responsibility: workflow logic belongs to orchestrators; business logic belongs to worker services or independent choreographed services.
- Design safe, observable, and idempotent failure-handling mechanisms via Distributed Transactions (Sagas) or Compensation Workflows.
- Prevent the creation of brittle, tightly coupled dependencies that violate event-driven microservice tenets.

@Guidelines

**Workflow Pattern Selection**
- The AI MUST evaluate the workflow's propensity for change. If the workflow steps are highly likely to be reordered or have steps inserted in the middle, the AI MUST recommend Orchestration.
- The AI MUST recommend Choreography ONLY when cross-team decoupling is paramount, the workflow is relatively simple (linear), and future modifications will primarily involve appending new consumers to the end of the workflow.
- When an orchestration pattern is required, the AI MUST evaluate latency and durability needs:
  - Select **Event-Driven Orchestration** for robust workflows requiring built-in retries and isolation from intermittent failures.
  - Select **Direct-Call Orchestration** when very quick responses/real-time operations are strictly required (e.g., Function-as-a-Service workflows).

**Orchestration Constraints**
- The AI MUST NOT place business fulfillment logic inside the orchestrator. 
- The AI MUST restrict the orchestrator to handling ONLY workflow state transitions (e.g., sending commands, awaiting results, initiating rollbacks).
- The AI MUST delegate ALL retry, error handling, and intermittent failure management of a specific task to the worker microservice. The orchestrator MUST only care if the task completely succeeded or completely failed.

**Choreography Constraints**
- The AI MUST strictly respect bounded contexts. A choreographed service MUST NOT assume anything about its upstream or downstream peers.
- When modifying a choreographed workflow (e.g., changing A -> B -> C to A -> C -> B), the AI MUST explicitly check for and resolve breaking schema changes, and ensure all in-flight partial events are fully processed before swapping the topology.

**Monitoring Workflows**
- For Choreographed workflows, the AI MUST implement monitoring by independently tapping and materializing the specific output event streams relevant to the observer.
- For Orchestrated workflows, the AI MUST implement monitoring by querying the orchestrator's local materialized state, which tracks the exact status of every event in the workflow.

**Distributed Transactions (Sagas) & Failure Handling**
- The AI MUST avoid implementing distributed transactions unless absolutely necessary to reduce risk/complexity.
- If a distributed transaction is required, the AI MUST ensure that EVERY participating microservice provides an idempotent reversal/rollback action.
- In Choreographed Sagas, the AI MUST ensure consumers listening for transaction status are configured to listen to ALL potential failure output streams (e.g., success is output of C, failure is output of A).
- In Orchestrated Sagas, the AI MUST design the orchestrator to issue explicit rollback commands to previously successful workers upon receiving a failure response from a downstream worker.
- The AI MUST prioritize Compensation Workflows over strict Distributed Transactions when dealing with customer-facing products where strict rollback provides a poor user experience (e.g., oversold inventory).

@Workflow
When tasked with designing or modifying a multi-microservice workflow, the AI MUST follow this exact sequence:

1. **Analyze Requirements:** Evaluate the workflow for complexity, likelihood of order changes, latency requirements, and observability needs.
2. **Select Architecture:**
   - Choose *Choreography* if the process is simple, linear, and highly decoupled.
   - Choose *Orchestration* if the process is complex, requires centralized monitoring, or has a high likelihood of future step re-ordering.
3. **Define Communication Strategy (If Orchestration):** Choose *Event-Driven* (via broker) for durability/retries or *Direct-Call* (via REST/RPC) for ultra-low latency.
4. **Design Bounded Contexts:** 
   - Define the inputs and outputs.
   - If Orchestration, strictly separate the orchestrator code (workflow logic) from the worker code (business logic).
5. **Design Monitoring Strategy:** Define how the workflow's progress will be tracked (materialized state in orchestrator vs. stream-tapping in choreography).
6. **Define Failure/Transaction Handling:** 
   - Determine if the business requirement allows for a *Compensation Workflow* (e.g., email apology).
   - If a strict technical rollback is required, design the *Saga*. Map out the exact failure points and the corresponding idempotent rollback commands/events for each participating microservice.
7. **Validate Independence:** Ensure worker microservices are responsible for their own local state consistency and retry policies during both processing and rollback.

@Examples (Do's and Don'ts)

**Pattern Selection & Modification**
- [DO] Use Choreography when multiple unrelated teams need to react to a core domain event (e.g., "UserCreated") without affecting the producer.
- [DON'T] Use Choreography for a 10-step order fulfillment process where steps frequently change order. Inserting a step in the middle of a choreographed chain forces breaking schema changes and risky topology swaps.

**Orchestrator Bounded Contexts (God Service Anti-Pattern)**
- [DO] Design an orchestrator that sends a "ProcessPayment" event and waits for a "PaymentSuccess" or "PaymentFailed" event. The payment microservice handles its own 3 internal retry attempts.
- [DON'T] Design an orchestrator that executes "PaymentAttempt1", evaluates the error, waits 5 seconds, and executes "PaymentAttempt2". This violates bounded contexts by pulling business logic into the orchestrator.

**Distributed Transactions (Sagas)**
- [DO] Design a choreographed saga where Service C fails, emits a "ServiceCFailed" event, which Service B consumes to trigger its internal `revertServiceB_State()` logic, which then emits "ServiceBReverted".
- [DON'T] Assume you can monitor a choreographed saga by only looking at the final output stream. The AI must implement monitoring that listens to the failure streams of Service A, B, and C to get an accurate view of aborted transactions.
- [DO] Design an orchestrated saga where the orchestrator receives a failure from Service B, and sequentially issues a "RollbackServiceA" command to Service A, awaiting a "ServiceARolledBack" confirmation.

**Rollbacks vs. Compensation Workflows**
- [DO] Implement a Compensation Workflow for an airline ticketing system that oversells a flight: issue a "SendDiscountAndApology" event.
- [DON'T] Implement a strict Distributed Transaction Saga that forcefully yanks the ticket out of the user's account and silently refunds their card, providing a confusing and poor customer experience.