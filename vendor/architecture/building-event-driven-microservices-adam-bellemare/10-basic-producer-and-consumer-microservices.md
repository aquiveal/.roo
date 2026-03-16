@Domain
These rules are activated when the AI is tasked with architecting, developing, refactoring, or reviewing Basic Producer and Consumer (BPC) microservices. This includes tasks involving the integration of legacy systems into event-driven architectures, implementing simple stateless or stateful event processors outside of full-featured streaming frameworks, creating Sidecar data-sinking applications, or coordinating Hybrid BPC applications with external stream processors.

@Vocabulary
- **Basic Producer and Consumer (BPC) Microservice**: A simplified event-driven microservice that uses basic consumer and producer clients to ingest events, apply transformations or business logic, and emit output events, lacking advanced built-in features like event scheduling, watermarks, or changelogs.
- **Sidecar Pattern**: A deployment pattern where a BPC operates in its own container but alongside a legacy application within a single deployable unit, used to sink or source event data without modifying the legacy system's codebase.
- **Gating Pattern**: A stateful business logic pattern where an action is delayed until a specific set of required events (regardless of their arrival order) are all present in the system.
- **Hybrid BPC Application**: A microservice that combines a standard BPC implementation with an external heavyweight stream-processing framework to offload complex stream operations (like stream joins) while maintaining local API control.
- **External State Store**: A data storage system residing outside the microservice's container (e.g., remote database), which BPCs heavily rely upon to manage state, enabling horizontal scaling and recovery without complex internal state rematerialization.
- **Ghost Process**: An orphaned execution instance of an external stream-processing job that continues to run and consume resources because the initiating Hybrid BPC was terminated without triggering a clean shutdown of the external job.

@Objectives
- Implement lightweight, self-contained BPC microservices that strictly handle event ingestion, basic transformations, and event emission.
- Ensure stateful BPCs remain easily scalable and recoverable by offloading state management to External State Stores rather than attempting complex internal state reconstruction.
- Safely integrate legacy monoliths into the event-driven ecosystem without introducing risky codebase modifications by utilizing the Sidecar Pattern.
- Delegate complex data processing (e.g., full-text search, geospatial, Machine Learning) directly to the data layer to keep the BPC logic thin and focused on integration.
- Ensure proper lifecycle management of external resources in Hybrid BPC applications to prevent resource leaks and ghost processes.

@Guidelines

**BPC Feature Boundaries**
- When implementing a BPC, the AI MUST NOT attempt to build custom mechanisms for event scheduling, watermarks, internal changelogs, or complex local state horizontal scaling. If these are required, the AI MUST alert the user that a lightweight or heavyweight streaming framework is necessary.
- When transforming data statelessly within a BPC, the AI MUST isolate the transformation logic into easily testable, modular functions that process events individually.

**State Management**
- When a BPC requires stateful business logic, the AI MUST default to using an External State Store to maintain state. 
- When handling cyclic or variable loads, the AI MUST design the BPC so that processing instances can scale independently of the External State Store, ensuring state remains highly available even if processing instances scale down to one.

**Legacy Integration (Sidecar Pattern)**
- When integrating event streams with a legacy application that cannot or should not be modified, the AI MUST implement the Sidecar Pattern.
- When implementing a Sidecar, the AI MUST configure the BPC to sink required event streams directly into the legacy application's datastore.
- When deploying a Sidecar, the AI MUST configure the CMS to package the legacy application and the BPC container together as a single deployable unit.

**Gating Pattern Implementation**
- When business logic requires multiple discrete events to occur before proceeding, and the order of arrival is irrelevant, the AI MUST implement the Gating Pattern.
- When implementing the Gating Pattern, the AI MUST instruct the BPC to materialize incoming events into tables/state and upon every new event, query the other required tables to verify if all dependencies (including explicit human approvals) are fulfilled before emitting the final output event.

**Data Layer Delegation**
- When the event processing requires geospatial lookups, free-text search, or AI/ML evaluations, the AI MUST design the BPC as a thin integration mechanism that passes the event to a specialized underlying data layer for computation, rather than implementing the heavy logic in the BPC itself.

**Hybrid BPC Applications**
- When business requirements demand complex stream operations (such as joining large event streams) but the application must remain a BPC, the AI MUST implement a Hybrid BPC Application.
- When designing a Hybrid BPC, the AI MUST construct a client within the BPC to dispatch the heavy stream-processing instructions to an external stream-processing framework.
- When receiving data in a Hybrid BPC, the AI MUST configure the external stream processor to write its results to an intermediate output event stream, which the BPC then consumes.
- When managing the lifecycle of a Hybrid BPC, the AI MUST implement shutdown hooks in the BPC to explicitly send termination commands to the external stream-processing framework to prevent Ghost Processes.

@Workflow
1. **Requirement Assessment**: Analyze the event processing requirements. Verify that the task does not require strict deterministic event scheduling or complex internal state materialization. If it does, halt and recommend a full streaming framework.
2. **Determine State and Scaling Strategy**: If state is required, provision an External State Store. Decouple the scaling metrics of the BPC container from the data layer to allow dynamic scaling based on event volume.
3. **Select Integration Pattern**:
   - If augmenting a legacy monolith: Apply the *Sidecar Pattern*.
   - If waiting for multiple unordered prerequisites: Apply the *Gating Pattern*.
   - If heavy search/ML is needed: Apply *Data Layer Delegation*.
   - If complex stream joins are needed: Apply the *Hybrid BPC Pattern*.
4. **Implement Client Logic**: Write the code using standard producer and consumer clients for the target language. Ensure a clear loop for ingestion, business logic application, and emission.
5. **Configure Lifecycle hooks (Hybrid specific)**: If using an external framework, bind the termination of the external cluster job to the graceful shutdown phase of the BPC microservice.

@Examples (Do's and Don'ts)

**Legacy Integration (Sidecar Pattern)**
[DO]
```yaml
# docker-compose.yml demonstrating single-deployable sidecar
version: '3.8'
services:
  legacy-frontend:
    image: legacy-app:v1
    depends_on:
      - legacy-db
  legacy-db:
    image: postgres:13
  bpc-sidecar-updater:
    image: bpc-event-consumer:latest
    environment:
      - KAFKA_BROKERS=kafka:9092
      - INPUT_STREAM=product-updates
      - DB_CONNECTION=jdbc:postgresql://legacy-db:5432/legacy
    depends_on:
      - legacy-db
```

[DON'T]
```python
# Anti-pattern: Modifying the legacy application codebase to consume events directly when it is risky to do so.
class LegacyMonolith:
    def __init__(self):
        self.kafka_consumer = KafkaConsumer('product-updates') # Do not embed in untouched legacy code
```

**Hybrid BPC Lifecycle Management**
[DO]
```java
// BPC coordinating with an external stream processing framework
public class HybridBPC {
    private ExternalStreamClient externalClient;
    private String jobId;

    public void start() {
        // Start heavy join job on external cluster
        jobId = externalClient.submitJoinJob("streamA", "streamB", "joinedOutput");
        
        // Register shutdown hook to prevent ghost processes
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Terminating external stream job...");
            externalClient.terminateJob(jobId);
        }));
        
        // Consume from the intermediate output stream
        consumeLocal("joinedOutput");
    }
}
```

[DON'T]
```java
// Anti-pattern: Failing to terminate the external job when the BPC shuts down
public class HybridBPC {
    public void start() {
        ExternalStreamClient externalClient = new ExternalStreamClient();
        externalClient.submitJoinJob("streamA", "streamB", "joinedOutput");
        // MISSING: No shutdown hook or reference to the jobId. 
        // If this BPC restarts, it will create a duplicate ghost process.
        consumeLocal("joinedOutput");
    }
}
```

**Gating Pattern**
[DO]
```javascript
// BPC executing the Gating Pattern using an external state store
async function processEvent(event) {
    // 1. Save the new piece of the puzzle
    await externalDb.save(event.bookId, event.type, event.data);
    
    // 2. Check if all conditions are met
    const bookState = await externalDb.get(event.bookId);
    if (bookState.hasContents && bookState.hasCoverArt && bookState.hasPricing) {
        // 3. Emit the final event ONLY when all unordered prerequisites are present
        await producer.emit('ready-for-publishing', bookState);
    }
}
```

[DON'T]
```javascript
// Anti-pattern: Attempting to rely on strict event ordering in a BPC
async function processEvent(event) {
    // Assuming cover art always comes last - this will break if pricing arrives last
    if (event.type === 'COVER_ART') {
        await producer.emit('ready-for-publishing', event.bookId); 
    }
}
```