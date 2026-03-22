# @Domain
This rule file is activated when the AI is tasked with migrating, refactoring, or modernizing an existing monolithic application into a microservice architecture. It applies to user requests involving extracting services from a legacy codebase, implementing new features alongside an existing monolith, designing interprocess communication (IPC) between a monolith and microservices, or solving data consistency and security challenges during a phased migration.

# @Vocabulary
- **Monolithic Hell**: A state where an application has outgrown its architecture, resulting in slow delivery, buggy software releases, and poor scalability due to complexity and tightly coupled modules.
- **Big Bang Rewrite**: An anti-pattern involving rewriting an entire application from scratch in a new architecture. Highly risky and strongly discouraged.
- **Strangler Application Pattern**: An application modernization strategy where a new microservices-based application is incrementally built around the legacy monolithic application, gradually replacing it over time.
- **Integration Glue**: A set of adapters in both the extracted service and the monolith that enables them to collaborate via IPC (REST, messaging, domain events) while the system is transitioning.
- **Anti-Corruption Layer (ACL)**: A layer of code within the Integration Glue that translates between the legacy monolith's domain model and the new service's pristine domain model, preventing legacy concepts from polluting the new service.
- **Vertical Slice**: A complete segment of functionality targeted for extraction, comprising inbound adapters (API), domain logic, outbound adapters (database access), and the database schema.
- **Semantic Lock**: A countermeasure (e.g., an `APPROVAL_PENDING` state) used in sagas to indicate a record is in the process of being updated.
- **Compensatable Transaction**: A transaction in a saga that can be rolled back using a compensating transaction if a subsequent step fails.
- **Pivot Transaction**: The "go/no-go" point in a saga. If it commits, the saga will run to completion.
- **Retriable Transaction**: A transaction in a saga that follows the pivot transaction and is guaranteed to succeed.

# @Objectives
- Escape monolithic hell safely by adhering strictly to incremental refactoring rather than massive rewrites.
- Demonstrate business value early and often by prioritizing the extraction or implementation of high-value capabilities.
- Minimize widespread, risky, and time-consuming changes to the legacy monolithic codebase during the extraction process.
- Ensure strict data consistency and seamless security (authentication/authorization) bridging between the legacy monolith and the new microservices.

# @Guidelines

## General Refactoring Philosophy
- **Verify the Root Cause**: Before initiating a migration, the AI MUST verify that the software delivery problems (slow delivery, bugs) are caused by the architecture and not by poor software development processes (e.g., lack of automated testing).
- **Avoid Big Bang Rewrites**: The AI MUST NEVER recommend or attempt to rewrite the entire legacy application from scratch. All refactoring MUST use the Strangler Application Pattern.
- **Defer Infrastructure Decisions**: Do not over-invest in sophisticated deployment infrastructure (e.g., Kubernetes, service meshes) up front. The AI MUST prioritize establishing a deployment pipeline with automated testing before provisioning heavy microservice infrastructure.

## Strategies for Strangling the Monolith
- **Stop Digging (Implement New Features as Services)**: When asked to add a new feature to a bloated monolith, the AI MUST implement it as a standalone microservice unless the feature is too small to be a meaningful service or is fundamentally too tightly coupled to the monolith's code.
- **Split Presentation from Backend**: To gain independent deployability and rapid UI iteration, the AI SHOULD consider splitting the presentation tier (web UI) from the business logic and data access layers as an initial, partial modernization step.
- **Extract Business Capabilities**: The AI MUST break apart the monolith by extracting functionality as complete "Vertical Slices" (API, logic, data).
- **Prioritize Extractions Strategically**: The AI MUST NOT extract services blindly. Extractions must be prioritized based on business benefit: accelerating active development, solving performance/scaling bottlenecks, or unblocking the extraction of other services.

## Designing the Integration Glue and IPC
- **Encapsulate IPC**: The integration glue MUST be encapsulated behind interfaces (e.g., a Repository interface for queries, or a Service interface for updates) so the business logic remains agnostic to the IPC mechanism.
- **Querying Data**: When a service needs monolith data (or vice versa), the AI MUST evaluate two options:
  1. Invoke a query API (e.g., REST/gRPC) for simple, low-volume lookups.
  2. Maintain a data replica (CQRS view) synchronized via domain events for complex or high-volume querying.
- **Anti-Corruption Layer (ACL)**: The AI MUST ALWAYS implement an ACL in the integration glue to translate data formats, class names, and attributes between the monolith's legacy domain model and the microservice's domain model.
- **Event Publishing from the Monolith**: To allow services to subscribe to monolith changes without massive code alterations, the AI SHOULD utilize transaction log tailing or database polling to publish events from the monolith.

## Splitting Domain Models and Databases
- **Eliminate Cross-Service Object References**: When splitting a domain model, the AI MUST replace object references that span process boundaries with primary key IDs, adhering to DDD Aggregate rules.
- **Replicate Data to Minimize Monolith Changes**: To avoid updating every instance of a moved field within the legacy codebase, the AI SHOULD replicate the extracted data from the new service back to the monolith's database during the transition period. Make the legacy fields read-only and synchronize them via events from the new service.

## Maintaining Data Consistency (Sagas)
- **Sequence Extractions Carefully**: The AI MUST actively plan the extraction sequence to simplify saga implementation. 
- **Avoid Monolith Compensating Transactions**: Modifying the monolith to support compensatable transactions (which require widespread additions of Semantic Locks like `PENDING` states) is risky and expensive. The AI MUST sequence extractions and design sagas such that the monolith's local transactions act ONLY as *Pivot Transactions* or *Retriable Transactions*.

## Handling Authentication and Authorization
- **Bridge Legacy and Modern Security**: The AI MUST support both the monolith's session-based security and the microservices' token-based (JWT) security simultaneously.
- **The USERINFO Cookie Strategy**: To achieve this without rewriting monolith security, the AI MUST enhance the monolith's login handler to output an additional cookie (e.g., `USERINFO`) containing the user's JWT (identity and roles).
- **API Gateway Translation**: The API Gateway MUST be configured to extract the `USERINFO` cookie from incoming requests and map it to the `Authorization` HTTP header when proxying requests to the new microservices.

# @Workflow
When tasked with refactoring a monolithic application or adding functionality to a legacy system, the AI MUST follow this algorithmic process:

1. **Assess the Problem**: Confirm that the requested feature or extraction addresses architectural limitations rather than process deficiencies.
2. **Time-Boxed Architecture Definition**: Perform a brief mapping of the target microservice architecture to establish a destination model.
3. **Evaluate as New Service**: If implementing a new feature, evaluate if it can be built as a standalone service (Stop Digging). If yes, proceed to step 6.
4. **Rank Extractions**: If extracting existing code, rank the modules by business benefit (development velocity, scaling, unblocking dependencies).
5. **Define the Vertical Slice**: Identify the inbound adapters, domain logic, outbound adapters, and database tables to be extracted. Break god classes into specific aggregates.
6. **Design the Domain Split**: Replace cross-service object references with primary keys. 
7. **Design the Integration Glue**: Define the APIs (Repository/Service interfaces) for collaboration between the monolith and the new service. 
8. **Implement the Anti-Corruption Layer**: Write translation logic between the legacy model and the new microservice model.
9. **Implement Data Consistency (Sagas)**: Design the sequence of local transactions. Ensure the monolith steps are isolated as pivot or retriable transactions. Replicate data back to the monolith if it prevents widespread legacy code refactoring.
10. **Implement Security Bridging**: Ensure the API gateway routes the `USERINFO` cookie to the `Authorization` header for the newly extracted service.
11. **Deploy behind a Feature Toggle**: Deploy the new service and use a dynamic feature toggle within the monolith's integration glue to route traffic between the legacy implementation and the new service.

# @Examples (Do's and Don'ts)

### Strangling the Monolith
- **[DO]** Implement a brand-new feature (e.g., Delayed Order Notifications) as a completely new standalone microservice that queries the monolith via REST and listens to monolith database events.
- **[DON'T]** Attempt to pause all feature development for 12 months to rewrite the entire legacy application into a microservice architecture from scratch.

### Splitting Domain Models
- **[DO]** Refactor an `Order` class being extracted to a new service by removing the `Restaurant` object reference and replacing it with a `Long restaurantId`.
- **[DON'T]** Maintain foreign key constraints or object references in ORM configurations that point to tables/classes that now live in a separate deployable service.

### Minimizing Monolith Changes via Data Replication
- **[DO]** When extracting a `Delivery` service from the monolith, leave the `delivery_time` column in the monolith's database. Make it read-only in the monolith, and update it asynchronously by subscribing to `DeliveryScheduleUpdated` events emitted by the new Delivery Service.
- **[DON'T]** Hunt down and rewrite 500 different legacy SQL queries in the monolith that read `delivery_time` to make them perform synchronous REST calls to the new Delivery Service.

### Designing Sagas for Extractions
- **[DO]** Sequence extractions so that the step executed by the legacy monolith is the "Pivot" step (e.g., `Monolith: Authorize Credit Card`), which cannot fail due to downstream business rules, followed by `Service: Change state to APPROVED`.
- **[DON'T]** Design a saga where the monolith executes step 1, the microservice executes step 2, and step 2 can fail, forcing the monolith to implement complex compensating transactions and widespread `PENDING` states.

### Integration Glue & Anti-Corruption Layer
- **[DO]** Create an interface `CustomerContactInfoRepository` inside the new service that returns a pristine `CustomerContactInfo` object, and implement it with a proxy class that fetches legacy data and translates it from the monolith's messy `TblUserRecord` schema.
- **[DON'T]** Allow legacy names, status codes, or bloated God-class definitions from the monolith to leak into the new microservice's domain model.

### Security Migration
- **[DO]** Update the monolith's LoginHandler to return a standard `JSESSIONID` cookie AND a `USERINFO` cookie containing a JWT. Configure the API Gateway to convert the `USERINFO` cookie into an `Authorization: Bearer <JWT>` header for the microservices.
- **[DON'T]** Attempt to force the new stateless microservices to connect to the monolith's centralized in-memory session store (e.g., Tomcat HttpSession) to authenticate users.