# @Domain

These rules MUST trigger when the AI is tasked with designing, refactoring, or implementing communication flows between different system components, bounded contexts, or aggregates. This includes integrating APIs, publishing domain events, orchestrating asynchronous messaging, implementing model translations (Anti-Corruption Layers/Open-Host Services), or managing long-running, multi-step business transactions.

# @Vocabulary

- **Model Translation**: The process of mapping a source bounded context's model to a target bounded context's model to prevent strong coupling.
- **Stateless Model Translation**: On-the-fly translation of requests/messages using proxies or API Gateways without requiring a persistent database for the translation logic.
- **Stateful Model Translation**: Translation logic that requires persistent storage to track, aggregate, or batch incoming data before processing or forwarding.
- **Message Proxy**: An intermediary component that subscribes to asynchronous messages from a source, translates the model, filters noise, and forwards the result to a target.
- **Interchange Context**: A dedicated bounded context (often an API Gateway) whose sole responsibility is translating models for consumption by multiple downstream contexts.
- **Backend-for-Frontend (BFF)**: A stateful translation pattern where a user interface component combines and aggregates data originating from multiple services.
- **Outbox Pattern**: A reliable messaging pattern where updated aggregate state and outgoing domain events are saved together in the same atomic database transaction, later to be published by a relay.
- **Message Relay**: A background process that fetches unpublished events from the database (via polling or transaction log tailing) and publishes them to the message broker.
- **Saga**: A stateful or stateless pattern managing a long-running business process across multiple transactions/components by matching observed events to corresponding commands and issuing compensating actions upon failure.
- **Compensating Action**: A command issued by a Saga or Process Manager to revert or compensate for a partially completed process when a subsequent step fails.
- **Process Manager**: A central processing unit that explicitly maintains the state of a complex business sequence, uses conditional routing (if/else) to determine next steps, and must be explicitly initialized.

# @Objectives

- Ensure strict decoupling between bounded contexts by preventing internal implementation details (e.g., internal domain events) from leaking across component boundaries.
- Guarantee at-least-once, reliable delivery of domain events without risking inconsistent states caused by dual-write failures (e.g., database commits succeeding while message publishing fails).
- Orchestrate cross-aggregate and cross-context business workflows safely using eventual consistency, avoiding distributed or multi-aggregate atomic transactions.
- Choose the appropriate integration pattern (Saga vs. Process Manager) based on the complexity, routing requirements, and initialization triggers of the business workflow.

# @Guidelines

## Model Translation
- The AI MUST implement **Stateless Model Translation** via a Proxy or API Gateway for synchronous cross-context communication where the downstream cannot conform to the upstream model.
- The AI MUST implement a **Message Proxy** for asynchronous communication to intercept internal domain events, translate them into a Published Language, and filter out internal noise before exposing them to external bounded contexts.
- The AI MUST implement **Stateful Model Translation** using persistent storage, stream-processing platforms, or batching solutions when translation requires aggregating incoming data, processing in batches, or unifying multiple fine-grained messages into a single message.
- The AI MUST utilize the **Backend-for-Frontend (BFF)** or a dedicated **Anti-Corruption Layer (ACL)** to aggregate and unify data when a single context must consume and process data from multiple upstream bounded contexts.

## Reliable Event Publishing (Outbox Pattern)
- The AI MUST NOT publish domain events directly from an aggregate's business logic methods.
- The AI MUST NOT publish domain events sequentially in the application layer after committing a database transaction (this risks a state where the DB is updated but events are lost if the process crashes).
- The AI MUST implement the **Outbox Pattern** for publishing events. The aggregate's state update and the generated domain events MUST be persisted within a single, atomic database transaction.
- When using relational databases, the AI MUST store outgoing events in a dedicated Outbox table within the same transaction.
- When using NoSQL databases lacking multi-document transactions, the AI MUST embed the outgoing domain events directly inside the aggregate's document (e.g., as an `outbox` array property).
- The AI MUST implement a **Message Relay** using either a Pull-based (Polling Publisher) or Push-based (Transaction Log Tailing) mechanism to read the Outbox table/array, publish the messages to the broker, and subsequently mark them as published or delete them.

## Orchestrating Cross-Component Workflows (Sagas)
- The AI MUST implement a **Saga** when handling linear, multi-aggregate business processes that react to events and trigger predefined commands.
- The AI MUST implement **Compensating Actions** within the Saga to revert previously committed transactions if a downstream step in the process fails.
- The AI MUST NOT use Sagas to compensate for poorly designed aggregate boundaries. If two entities strictly require strong consistency, they MUST be redesigned as a single aggregate rather than orchestrated via a Saga.
- If a Saga requires state tracking to issue compensating actions, the AI MUST persist the Saga's state and use the Outbox pattern to dispatch its commands (e.g., by saving a `CommandIssuedEvent` to the database instead of executing the command synchronously).

## Orchestrating Complex Workflows (Process Managers)
- The AI MUST implement a **Process Manager** (instead of a Saga) if the business workflow requires complex logic, conditional routing (if-else statements), and explicit instantiation.
- The AI MUST NOT implicitly bind a Process Manager to a single source event. Process Managers MUST expose explicit initialization methods/commands.
- The AI MUST implement Process Managers as state-based or event-sourced aggregates that maintain sequence state and determine the next processing steps.
- The AI MUST isolate command execution from the Process Manager's state transitions using the Outbox pattern (saving intents to execute commands to be picked up by a relay).

# @Workflow

When designing or implementing communication and integration between components, the AI MUST follow this algorithmic process:

1. **Analyze Integration Coupling:**
   - Determine if the communication is cross-context or intra-context.
   - If cross-context, determine if the upstream model can be consumed directly. If not, design a Translation Layer (Stateless Proxy/Message Proxy for 1:1, or Stateful BFF/ACL for 1:N or batching).
2. **Design Event Publishing:**
   - Verify the database technology in use (SQL vs. NoSQL).
   - Scaffold the Outbox persistence mechanism (Dedicated table for SQL, embedded array for NoSQL).
   - Implement the atomic commit of both aggregate state and outgoing events.
   - Scaffold the background Message Relay to poll/tail the outbox and push to the message broker.
3. **Evaluate Cross-Component Workflows:**
   - Identify if a business transaction spans multiple aggregates.
   - If the flow is strictly linear, event-to-command matching, implicitly triggered by an event: Scaffold a **Saga**.
   - If the flow has complex branching (if-else), requires explicit initialization, and maintains central sequence state: Scaffold a **Process Manager**.
4. **Implement Workflow Resilience:**
   - Define the failure scenarios for the Saga or Process Manager.
   - Define and map Compensating Actions for every potential failure point.
   - Ensure the Saga/Process Manager does not execute commands synchronously, but instead appends `CommandIssuedEvent` records to an Outbox for asynchronous, reliable execution.

# @Examples (Do's and Don'ts)

## Event Publishing

- **[DON'T]** Publish events directly from the aggregate or sequentially in the application layer without transactional guarantees.
```csharp
// ANTI-PATTERN: Prone to dual-write failures
public void DeactivateCampaign(CampaignId id, string reason) {
    var campaign = repository.Load(id);
    campaign.Deactivate(reason);
    _repository.CommitChanges(campaign); // DB transaction commits
    
    // If server crashes here, events are lost forever!
    foreach (var e in campaign.GetUnpublishedEvents()) {
        _messageBus.Publish(e); 
    }
}
```

- **[DO]** Use the Outbox Pattern to guarantee at-least-once delivery.
```csharp
// CORRECT PATTERN: Outbox
public void DeactivateCampaign(CampaignId id, string reason) {
    var campaign = repository.Load(id);
    campaign.Deactivate(reason);
    // CommitChanges atomically saves the updated state AND the events into an Outbox table
    _repository.CommitChanges(campaign, campaign.GetUnpublishedEvents()); 
}
// A separate Relay process fetches from the Outbox table and safely calls _messageBus.Publish()
```

## Outbox Pattern in NoSQL

- **[DON'T]** Try to use multi-table transactions in NoSQL databases that do not support them.
- **[DO]** Embed the outbox array inside the aggregate document.
```json
{
  "campaign-id": "364b33c3-2171-446d",
  "state": { "publishing-state": "DEACTIVATED" },
  "outbox": [
    { "type": "campaign-deactivated", "reason": "Goals met", "published": false }
  ]
}
```

## Sagas & Process Managers Command Dispatch

- **[DON'T]** Execute HTTP calls or synchronous commands directly inside a Saga or Process Manager's event handler.
```csharp
// ANTI-PATTERN: Fails if external service is down, losing the state transition
public void Process(CampaignActivated @event) {
    var campaign = _repository.Load(@event.CampaignId);
    // Unsafe synchronous external call
    _publishingService.SubmitAdvertisement(@event.CampaignId); 
}
```

- **[DO]** Append command execution intents to the Outbox for reliable dispatch.
```csharp
// CORRECT PATTERN: Reliable Command Dispatch
public void Process(CampaignActivated activated) {
    var campaign = _repository.Load(activated.CampaignId);
    
    // Create an intent to execute a command
    var commandIssuedEvent = new CommandIssuedEvent(
        target: Target.PublishingService,
        command: new SubmitAdvertisementCommand(activated.CampaignId)
    );
    
    _events.Append(activated); // Transition internal state
    _events.Append(commandIssuedEvent); // Save intent via Outbox
    
    _repository.CommitChanges(this, _events);
}
```