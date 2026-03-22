@Domain
Trigger these rules when designing, implementing, configuring, or debugging Function-as-a-Service (FaaS) solutions, serverless event-driven microservices, cloud functions (e.g., AWS Lambda, Google Cloud Functions, Azure Functions), open-source serverless frameworks (e.g., OpenFaaS, OpenWhisk, Kubeless, Pulsar FaaS), or function-to-function communication topologies within an event-driven architecture.

@Vocabulary
- **Function-as-a-Service (FaaS)**: A serverless compute paradigm where short-lived code executes in response to triggering conditions, running to completion and terminating.
- **Cold Start**: The initial state of a function where a container must be provisioned, code loaded, and client connections (e.g., to event brokers or state stores) established.
- **Warm Start**: The state where a previously executed, suspended function instance is reused, retaining its established connections to minimize latency.
- **Event-Stream Listener**: A triggering mechanism where a function is automatically invoked by the arrival of a new event in a subscribed stream, often passing an array (batch) of events.
- **Consumer Group Lag**: A triggering mechanism based on the delta between the current consumer offset and the head offset of a stream, often used to scale function instances dynamically.
- **Batch Size**: The maximum number of events dispatched to a function for processing in a single invocation.
- **Batch Window**: The maximum amount of time a framework waits to accumulate events before triggering the function.
- **External State Store**: A database or storage mechanism existing outside the function's execution environment, required for stateful FaaS due to the ephemeral nature of functions.
- **Internal Event Stream**: An event stream used strictly for function-to-function communication within a single bounded context, concealed from external consumers.
- **Hysteresis Loop**: A tolerance threshold in scaling policies designed to prevent rapid, endless scaling up and down (thrashing) of function instances.
- **Static Partition Assignment**: Pre-assigning specific partitions to functions to eliminate consumer group rebalancing overhead.

@Objectives
- Architect FaaS solutions that strictly adhere to bounded contexts, avoiding fragmented logic and ambiguous ownership.
- Ensure at-least-once processing guarantees and prevent data loss by strictly managing offset commits.
- Maintain deterministic processing and event ordering, especially when invoking subsequent functions or dealing with asynchronous code.
- Optimize FaaS resource utilization, execution timeouts, and lifecycle hooks to balance cost and latency.
- Implement robust state management using external data stores, adhering to the "no local state" constraint of serverless environments.

@Guidelines

- **Bounded Context Enforcement**
  - The AI MUST ensure functions and internal event streams strictly belong to a single bounded context.
  - The AI MUST enforce a 1:1 or n:1 mapping of functions to a specific product/context.
  - The AI MUST restrict access to FaaS data stores and internal streams from any external contexts.
  - The AI MUST group function code within a repository mapped directly to the bounded context.

- **Offset Committal Strategy**
  - The AI MUST commit consumer offsets ONLY after the function has fully and successfully completed processing the event or batch of events.
  - The AI MUST NOT commit offsets at the start of the function invocation. (Doing so risks data loss if the function fails or times out).

- **Function Granularity ("Less Is More")**
  - The AI MUST favor fewer, comprehensive functions over a highly fragmented architecture of many granular, hyper-specific functions.
  - The AI MUST NOT reuse the exact same function across multiple different services if it blurs ownership or bounded context boundaries.

- **State Management**
  - The AI MUST NOT rely on local container memory or local disk for durable state between invocations (unless explicitly using specialized features like Azure Durable Functions).
  - The AI MUST implement state management using External State Stores.
  - The AI MUST persist and retrieve state explicitly via database/API connections within the function code.
  - The AI MUST apply strict access permissions to the function's external state, blocking all access outside its bounded context.

- **Functions Calling Other Functions**
  - The AI MUST prefer **Event-Driven Communication** (producing to an internal event stream to trigger the next function) over direct invocation. This allows independent offset management and zero data loss on failures.
  - If using **Direct-Call Asynchronous (Choreography)**: The AI MUST NOT update consumer offsets until all asynchronous tasks are confirmed successful. The AI MUST prevent out-of-order execution race conditions (do not trigger async calls blindly in a loop without managing event completion order).
  - If using **Direct-Call Synchronous (Orchestration)**: The AI MUST process each event completely through the workflow (Function A -> Function B -> Output) sequentially before beginning the next event to respect offset ordering.

- **Lifecycle and Termination Management**
  - The AI MUST evaluate the invocation frequency of the function to determine connection cleanup logic.
  - For intermittently running functions: The AI MUST explicitly close event broker connections, close DB connections, and relinquish partition assignments before termination to prevent processing delays and ghost partition claims.
  - For continuously/heavily running functions: The AI MUST leave connections open to take advantage of Warm Starts.

- **Performance Tuning**
  - The AI MUST configure the `maximum execution time` of the function to be higher than the expected time required to process the configured `batch size`.
  - When handling function timeouts, the AI MUST resolve them by either increasing the maximum execution time OR decreasing the maximum batch size.

- **Scaling and Rebalancing**
  - The AI MUST implement scaling policies using a step-based approach or a hysteresis loop to prevent a virtual deadlock of constant consumer group rebalancing.
  - The AI MUST restrict auto-scaling frequency (e.g., max once every few minutes) to avoid thrashing.
  - For highly sensitive latency requirements where rebalancing is unacceptable, the AI MUST use Static Partition Assignments.

@Workflow
When tasked with creating or modifying a FaaS-based microservice, the AI MUST follow this exact sequence:

1. **Context Validation**: Define the bounded context. Validate that the workload is appropriate for FaaS (highly variable load, stateless, or simple stateful using an external DB).
2. **Component Definition**: Define the 4 core components: The Function Code, the Input Event Stream, the Triggering Logic, and the Error/Scaling Policies.
3. **Trigger Selection**: Select the appropriate trigger (Event-Stream Listener for standard reactive processing, Consumer Group Lag for custom scaling/polling, Schedule for periodic batching, or Webhook/Resource for external integrations).
4. **Parameter Tuning**: Calculate expected processing time per event. Set the `Batch Size` and `Batch Window`. Set the `Max Execution Time` to comfortably accommodate the batch size.
5. **State Integration**: If state is required, configure connections to an External State Store. Ensure connection creation logic handles both Cold Starts (initialize) and Warm Starts (reuse).
6. **Processing Implementation**: Write the processing loop. Ensure events are processed sequentially if ordering matters.
7. **Offset Management**: Place the offset committal logic at the absolute end of the processing block, executing only on success. Implement dead-letter queue routing for unprocessable events if retries are exhausted.
8. **Termination Logic**: Implement a shutdown hook to clean up connections if the function runs sporadically.
9. **Scaling Policy**: Define the scale-up/scale-down metrics (e.g., lag-based) and apply a hysteresis loop to prevent rapid rebalancing.

@Examples (Do's and Don'ts)

**Principle: Offset Committing**
[DO]
```java
public int processEvents(Event[] events, Context context) {
    for(Event event: events) {
        applyBusinessLogic(event);
    }
    // Commit only after all events in the batch are successfully processed
    context.success(); 
    return 0;
}
```
[DON'T]
```java
public int processEvents(Event[] events, Context context) {
    // ANTI-PATTERN: Acknowledging success before processing finishes
    context.success(); 
    for(Event event: events) {
        applyBusinessLogic(event); // If this fails, data is permanently lost
    }
    return 0;
}
```

**Principle: Direct-Call Asynchronous Execution (Ordering)**
[DO]
```java
public int functionA(Event[] events, Context context) {
    for(Event event: events) {
        // Orchestrated, sequential execution respects offset ordering
        Result resultA = processLocally(event);
        Result resultB = invokeFunctionBSynchronously(event, resultA);
        producer.produce("Output_Stream", resultB);
    }
    context.success();
    return 0;
}
```
[DON'T]
```java
public int functionA(Event[] events, Context context) {
    for(Event event: events) {
        // ANTI-PATTERN: Fire-and-forget async calls inside a loop
        // Causes race conditions, out-of-order processing, and lost errors
        asyncFunctionB(event); 
    }
    context.success(); // Commits offsets even if asyncFunctionB fails later
    return 0;
}
```

**Principle: Termination and Connection Management (Intermittent Functions)**
[DO]
```java
public void onShutdown(Context context) {
    // Relinquishing resources ensures other instances can claim partitions immediately
    eventBrokerClient.closeConnections();
    eventBrokerClient.relinquishPartitionAssignments();
    databaseClient.close();
}
```
[DON'T]
```java
public void onShutdown(Context context) {
    // ANTI-PATTERN: Doing nothing on shutdown for an intermittent function.
    // The consumer group will block partition reassignment until a timeout occurs, stalling processing.
}
```

**Principle: Handling Function Timeouts**
[DO]
When encountering frequent `FunctionExecutionTimeout` errors, configure the FaaS framework to automatically halve the batch size on failure and re-execute, OR permanently decrease the `max_batch_size` parameter in the trigger configuration to ensure the batch finishes within the execution window.
[DON'T]
Ignore timeouts or implement internal retry loops within the function that further extend the processing time beyond the FaaS provider's hard limits, leading to forced container kills and infinite uncommitted offset loops.