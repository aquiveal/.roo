@Domain
When designing, analyzing, or implementing inter-service communication, distributed systems, event-driven architectures, microservice integrations, or cross-team data sharing mechanisms.

@Vocabulary
- **Command**: An action or request for an operation to be performed by another service. It executes synchronously, expects a completion status (and potentially a result), and changes system state.
- **Event**: A record of a past fact and a notification that something happened in the real world. It has no expectation of future action (fire-and-forget) and travels in only one direction.
- **Query**: A synchronous request to look up data. It is free of side effects and leaves the system state unchanged.
- **Loose Coupling**: The reduction of assumptions two parties make about each other (Leymann); specifically, minimizing the impact a change in one component will have on another (connascence).
- **Receiver-Driven Routing**: A publish-subscribe paradigm where the routing logic is defined by the subscriber (receiver) rather than the sender, flipping the burden of responsibility and maximizing pluggability.
- **Event-Carried State Transfer (Replication Hat)**: The use of an event stream to replicate data from a source service to a consuming service, allowing the consumer to query the data locally and autonomously.
- **Event Notification (Notification Hat)**: The use of an event solely to trigger a downstream service into action without carrying full state payloads.
- **Event Collaboration**: A choreographed pattern where multiple independent services collaborate around a single business workflow. Each service owns a subset of state transitions and plugs together through a chain of events without centralized control.
- **Bounded Context**: A cohesive group of closely related components or services (often within a single team or department) that share a domain model and deployment boundaries.
- **Choreography**: Decentralized workflow management (e.g., Event Collaboration) where no single service owns the entire process.
- **Orchestration**: Centralized workflow management using command-and-control logic, typically via a process manager.
- **Stateless Stream Processing**: Processing events purely for notification, executing logic one message at a time without external data lookups.
- **Stateful Stream Processing**: Processing events by replicating a required dataset (e.g., a Customers table) directly into the stream processor to perform local joins and enrichments.

@Objectives
- Eliminate brittle, synchronous dependencies between independent services to prevent cascading failures.
- Invert service dependencies using receiver-driven routing to enable the seamless plugging and unplugging of services without modifying upstream systems.
- Classify and enforce the correct use of Commands, Events, and Queries across system boundaries.
- Implement Event Collaboration to build decentralized, choreographed business workflows.
- Blend request-driven and event-driven protocols strategically, isolating synchronous coupling to within bounded contexts while strictly enforcing asynchronous decoupling between them.

@Guidelines
- **Communication Classification**: The AI MUST categorize every network interaction as a Command, Event, or Query.
- **Constraint on Commands**: The AI MUST restrict the use of Commands (RPC/HTTP POST) to strictly synchronous operations within a single Bounded Context, or when explicitly implementing a centralized process manager.
- **Constraint on Queries**: The AI MUST use Queries (REST GET/gRPC) only for lightweight data retrieval across service boundaries, or heavyweight retrieval strictly within a service boundary.
- **Enforcing Receiver-Driven Routing**: When an upstream service completes an action, the AI MUST NOT program it to call downstream services. It MUST emit an Event (e.g., `OrderCreated`) and allow downstream services to subscribe.
- **Event-Carried State Transfer**: When a service frequently queries an external service for data (e.g., a Shipping service querying a Customer service), the AI MUST design the consumer to subscribe to data mutation events, replicate the dataset locally, and query its own local storage to maximize autonomy and execution speed.
- **Event Collaboration over Orchestration**: When designing multi-step business processes, the AI MUST prefer Choreography over Orchestration. No single service should own the entire workflow. Each service MUST react to an event, perform its subset of logic, and emit a new event to push the workflow forward.
- **Mixing Protocols Architecture**: The AI MUST design user-facing APIs using synchronous request-response (REST/RPC), but immediately journal the state change to an event stream (Kafka) to trigger backend processing asynchronously.
- **Bounded Context Rules**: The AI MUST permit synchronous interactions (Commands/Queries) inside a Bounded Context (e.g., within a specific team's application). The AI MUST STRICTLY ENFORCE asynchronous Event messaging between different Bounded Contexts (e.g., between departments).
- **Essential Data Coupling**: The AI MUST recognize that core data coupling is unavoidable. Instead of creating shared databases (Integration Database anti-pattern) or relying on chatty RPC queries, the AI MUST use events to push data into the application boundaries of the consumers.
- **Stateful vs. Stateless Evaluation**: The AI MUST evaluate if a consumer needs reference data. If yes, the AI MUST design a Stateful Stream Processing architecture where reference data is replicated into local tables. If no, the AI MUST use Stateless Stream Processing (Notification).

@Workflow
1. **Analyze the Topology**: Identify all services, actors, and data domains in the proposed system.
2. **Define Bounded Contexts**: Group services into Bounded Contexts based on team ownership, shared domain models, and deployment boundaries.
3. **Map the Interactions**: For every edge between two services, classify the interaction as a Command, Query, or Event.
4. **Refactor Cross-Boundary RPC**: Locate any Command or Query that crosses a Bounded Context. Replace it with an Event. 
    - If it was a Command notifying a service to act, replace with a Notification Event.
    - If it was a Query fetching external data, replace with Event-Carried State Transfer (data replication).
5. **Design the UI/Edge Layer**: Implement standard synchronous REST/RPC interfaces for the frontend, ending the synchronous chain by writing an Event to the broker.
6. **Implement Event Collaboration**: Map out the business workflow chronologically. Assign responsibility for each specific state transition to a distinct service. Define the exact input Event and output Event for each service in the chain.

@Examples (Do's and Don'ts)

- **Interaction Design & Coupling**
  - [DO]: Design the `OrderService` to process an order and publish an `OrderCreated` event to a topic. Allow the `ShippingService` and `RepricingService` to independently subscribe to that topic.
  - [DON'T]: Design the `OrderService` to sequentially call `shippingService.ship(order)` and `repricingService.updatePrice(order)` via HTTP REST.

- **Data Lookups Across Boundaries**
  - [DO]: Have the `ShippingService` listen to `CustomerDetailsUpdated` events, building a local read-optimized database of customer addresses. When an order arrives, query the local database for the address.
  - [DON'T]: Have the `ShippingService` pause processing upon receiving an order to make a synchronous REST GET call to the `CustomerService` to fetch the shipping address.

- **Workflow Architecture (Event Collaboration)**
  - [DO]: Model workflows chronologically: `OrderService` emits `OrderValidated` -> `PaymentService` consumes it and emits `PaymentProcessed` -> `ShippingService` consumes it and emits `OrderShipped`.
  - [DON'T]: Build a god-service `OrderOrchestrator` that sends a command to validate, waits for the response, sends a command to pay, waits for the response, and sends a command to ship.

- **Naming Conventions**
  - [DO]: Name Events in the past tense to reflect irrevocable facts (e.g., `PaymentProcessed`, `OrderCreated`).
  - [DON'T]: Name Events as imperative commands or future requests (e.g., `ProcessPaymentEvent`, `CreateOrder`).

- **Bounded Contexts**
  - [DO]: Use synchronous HTTP calls between a `FrontendBFF` (Backend-for-Frontend) and the `UserAuthService` because they live in the same bounded context.
  - [DON'T]: Use synchronous HTTP calls between the `LogisticsDepartment` and the `BillingDepartment`. Use asynchronous event streams exclusively.