@Domain
When the user requests assistance with modernizing legacy applications, migrating monolithic applications to microservices architecture (MSA), containerizing existing legacy code, moving legacy systems to cloud environments (public, private, hybrid, or edge/fog), or restructuring legacy data access and batch processing systems.

@Vocabulary
*   **Legacy Application:** Monolithic, massive, inflexible, and tightly coupled software systems, often running on mainframe servers and written in outdated languages.
*   **Microservices Architecture (MSA):** An architectural style where applications are structured as a collection of fine-grained, self-defined, autonomous, loosely coupled, and independently deployable services, each with its own data store and exposed via RESTful APIs.
*   **Containerization:** The process of wrapping application components in standardized containers (e.g., Docker) to remove infrastructure dependencies, ensuring portability across any platform or cloud environment.
*   **Refactoring:** Reorganizing a legacy application's source code to convert it into a microservice without changing its external functionality.
*   **Rewriting:** Rebuilding the application source code from scratch using modern programming languages (e.g., Ballerina) while guaranteeing the legacy application's functionality.
*   **Rearchitecting / Redesigning:** Changing the fundamental architecture of the legacy application using the latest styles (such as SOA, EDA) and modern middleware or NoSQL/NewSQL databases.
*   **Replatforming:** Deploying the legacy application onto newer platforms or infrastructures (like cloud environments) without necessarily changing the core architecture.
*   **Domain-Driven Design (DDD):** A methodology used during service extraction to partition legacy applications into distinct business domains (e.g., shopping cart, payment, shipping).
*   **Service Extraction:** The first phase of modernization, where distinct business functionalities are identified and separated out from the monolithic application.
*   **Service Composition:** The second phase of modernization, combining multiple microservices using orchestration or choreography to fulfill complex business processes.
*   **Service Migration:** The third phase of modernization, moving the refactored, composed microservices into cloud environments.
*   **Data Virtualization / Data Proxies:** Using proxies to transform data from different legacy databases into a standardized format for microservices, rather than completely transforming the underlying data structures.
*   **Function as a Service (FaaS) / Serverless Computing:** A cloud computing execution model where the cloud provider dynamically manages the allocation of machine resources, used for deploying code-level components (functions) but posing configuration management challenges compared to microservices.
*   **Stubs:** Mock implementations used during the modernization process to seamlessly connect newly refactored microservices with the remaining, non-refactored legacy application components for testing.
*   **Edge/Fog Clouds:** Decentralized computing infrastructure where data processing and storage are located closer to the ground-level IoT devices and sensors.

@Objectives
*   Dismantle monolithic legacy applications into modular, highly cohesive, and loosely coupled microservices.
*   Eliminate infrastructure dependencies by leveraging containerization (e.g., Docker) for every extracted microservice.
*   Establish independent data access for every microservice to ensure data encapsulation and eliminate shared legacy database bottlenecks.
*   Implement continuous integration and continuous deployment (DevOps/CI-CD) pipelines to facilitate agile, independent deployments of extracted services.
*   Overcome the shift from in-process communication (RPC/RMI) to network-based communication (RESTful APIs) by mitigating network latency and managing varying API versions and data formats.
*   Transition legacy batch-processing workloads into real-time, parallel, or concurrent processing models utilizing cloud-based platforms and multi-threading capabilities.

@Guidelines
*   **Modernization Strategy Selection:** When analyzing a legacy codebase, the AI MUST explicitly categorize the modernization strategy into Refactoring, Rewriting, Rearchitecting, or Replatforming, and justify the choice based on the code's state and business requirements.
*   **Prioritization of Components:** The AI MUST NOT attempt to modernize the entire monolith at once. The AI MUST prioritize components for extraction based on three factors: ease of extraction, product roadmap, and possible risks.
*   **Domain-Driven Extraction:** When extracting services, the AI MUST use Domain-Driven Design (DDD) to group related functionalities (e.g., inventory, payment) into single, isolated microservices.
*   **Data Access Separation:** The AI MUST isolate data logic from business logic. The AI MUST implement "data access as a service" using volume containers and NEVER allow multiple microservices to share a single legacy database directly.
*   **Data Virtualization over Transformation:** To integrate new microservices with existing legacy databases, the AI MUST implement data virtualization or data proxies to standardize formats, rather than attempting a risky, immediate structural transformation of the legacy database.
*   **Testing via Stubs:** When a microservice is extracted and refactored, the AI MUST generate stubs to simulate the legacy components it interacts with. The AI MUST verify that the newly formulated service mimics the old behavior seamlessly before proceeding to other components.
*   **Network Latency Mitigation:** Because in-process calls (RPC/RMI) are being replaced by network calls (REST APIs), the AI MUST design communication patterns to account for network latency, potential network congestions, and API version mismatches.
*   **Containerization Enforcement:** The AI MUST wrap every modernized microservice in its own container and configure multiple instances (redundancy) for high availability, protecting against the fickle nature of containers.
*   **FaaS vs Microservices Evaluation:** When considering Serverless (FaaS) as a modernization target, the AI MUST evaluate and warn the user about configuration management challenges (e.g., managing versions across a library of functions) compared to the self-contained reusability of microservices.
*   **Batch to Real-Time Conversion:** When analyzing legacy batch-processing logic, the AI MUST attempt to redesign the logic for real-time, parallel, or concurrent processing by leveraging multi-threading or cloud-based stream processing.

@Workflow
1.  **Assess and Prioritize:** Analyze the monolithic legacy application. Evaluate business functions based on ease of extraction, roadmap alignment, and potential risk. Select a single, low-risk, high-value component to modernize first.
2.  **Service Extraction (Phase 1):** Apply Domain-Driven Design (DDD) to separate the chosen business functionality from the monolith. Determine whether to *Refactor* (reorganize existing code) or *Rewrite* (use a modern language like Ballerina) the component into a microservice.
3.  **Decouple Data Access:** Build "data access as a service" for the extracted component. Implement data virtualization/proxies to map the microservice's data needs to the legacy database without altering the legacy database structure.
4.  **Containerize:** Package the newly created microservice and its data access layer into individual containers (e.g., Docker application containers and volume containers). Configure for deployment across multiple instances to ensure redundancy.
5.  **Integration Testing with Stubs:** Generate stubs to bridge the new containerized microservice with the remaining legacy application. Test exhaustively to ensure the new service exactly mimics the legacy behavior and handles network latency correctly.
6.  **Service Composition (Phase 2):** Define the interaction between the new microservice and other services. Choose an orchestration (centralized hub) or choreography (decentralized event-driven) pattern to manage the business process flow.
7.  **Service Migration (Phase 3) and CI/CD:** Commit the validated microservice code to a centralized repository. Configure the CI/CD pipeline (e.g., Jenkins) to automate testing and deploy the container image to the target cloud environment (public, private, hybrid, or edge/fog).
8.  **Iterate:** Repeat steps 1-7 for the next prioritized legacy component until the monolithic application is fully modernized.

@Examples

**[DO]** Extracting a business function and using stubs to test integration with the legacy monolith.
```java
// DO: Isolate domain logic into a new RESTful microservice and use a proxy for legacy data.
@RestController
@RequestMapping("/api/v1/inventory")
public class ModernInventoryController {
    
    private final LegacyDataProxy dataProxy;

    public ModernInventoryController(LegacyDataProxy dataProxy) {
        this.dataProxy = dataProxy;
    }

    @GetMapping("/{itemId}")
    public ResponseEntity<InventoryItem> getItem(@PathVariable String itemId) {
        // Calls a proxy that safely formats legacy data into a modern standardized JSON object
        InventoryItem item = dataProxy.fetchAndStandardizeLegacyItem(itemId);
        return ResponseEntity.ok(item);
    }
}

// DO: Use a stub for the remaining legacy system to test the new microservice
public class LegacyBillingSystemStub implements BillingService {
    @Override
    public boolean chargeAccount(String accountId, double amount) {
        // Stub mimics the legacy behavior for testing the new Inventory microservice
        return true; 
    }
}
```

**[DON'T]** Attempting to share the legacy database directly without a proxy, or performing a massive structural change to the legacy DB during initial extraction.
```java
// DON'T: Tightly couple the new microservice directly to the raw, unstandardized legacy database schema.
@RestController
public class BadInventoryController {
    
    @Autowired
    private JdbcTemplate legacyDatabaseConnection; // Antipattern: Direct raw legacy DB access

    @GetMapping("/inventory/{itemId}")
    public Map<String, Object> getItem(@PathVariable String itemId) {
        // Antipattern: Exposing raw legacy table structures (e.g., AS400 column names) directly to the modern API
        return legacyDatabaseConnection.queryForMap("SELECT ITEM_NUM_X12, QTY_ON_HND FROM LEGACY_INV_TBL WHERE ITEM_NUM_X12 = ?", itemId);
    }
}
```

**[DO]** Shifting from legacy sequential batch processing to modern parallel processing.
```java
// DO: Utilize concurrent processing (multi-threading/streams) to replace legacy single-threaded batch processing.
public void processOrdersConcurrently(List<Order> orders) {
    orders.parallelStream().forEach(order -> {
        modernOrderProcessingService.process(order);
    });
}
```

**[DON'T]** Preserving single-threaded batch processing in a newly modernized cloud microservice.
```java
// DON'T: Porting over legacy single-threaded batch loops into a modern containerized application.
public void processOrdersLegacyStyle(List<Order> orders) {
    // Antipattern: Fails to utilize modern multi-core/cloud infrastructure capabilities
    for (Order order : orders) {
        legacyBatchProcessor.process(order);
    }
}
```