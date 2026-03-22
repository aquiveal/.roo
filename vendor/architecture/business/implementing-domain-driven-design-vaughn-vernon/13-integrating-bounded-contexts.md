# @Domain
Trigger these rules when executing tasks involving system integration, cross-system communication, developing Application Programming Interfaces (APIs), publishing or consuming message queues, creating RESTful resources, designing distributed systems, or integrating multiple Bounded Contexts.

# @Vocabulary
*   **Bounded Context**: A conceptual boundary around a system or application where a specific Ubiquitous Language and domain model apply.
*   **Context Map**: The concrete implementation (code) and visual representation of the relationships between integrating Bounded Contexts.
*   **RPC (Remote Procedure Call)**: A system-level integration approach that relies on executing procedures across network boundaries (e.g., SOAP). Known for creating tight temporal coupling.
*   **RESTful HTTP**: A method of exchanging and modifying uniquely identified resources (URIs) using HTTP verbs (GET, PUT, POST, DELETE).
*   **Publish-Subscribe**: A messaging mechanism where a publisher broadcasts Domain Events to one or more asynchronous subscribers.
*   **Published Language**: A well-documented, shared language (often a custom media type/JSON) used to express domain information as a common medium of communication between contexts, preventing the need to share class binaries.
*   **Open Host Service (OHS)**: A protocol/API defined to give access to a subsystem as a set of services, expanding to handle new integration requirements based on use cases.
*   **Shared Kernel / Conformist**: Undesirable integration relationships where consumers slavishly adhere to the upstream model or directly share domain model code, causing tight coupling.
*   **Anticorruption Layer (ACL)**: A defensive translation layer created by a downstream client consisting of a Service, an Adapter, and a Translator. It isolates the local domain model from foreign concepts.
*   **Domain Event**: A record of a discrete occurrence in the domain, used to synchronize remote contexts.
*   **Long-Running Process (Saga)**: An event-driven, distributed parallel processing pattern used to manage multi-step integrations across contexts without atomic transactions.
*   **TimeConstrainedProcessTracker**: A technical Subdomain concept used to manage timeouts, retries, and failures for Long-Running Processes.
*   **Idempotency**: The property of an operation whereby it can be applied multiple times without changing the result beyond the initial application.

# @Objectives
*   Integrate Bounded Contexts securely, reliably, and autonomously while assuming the network is inherently hostile and unreliable.
*   Prevent domain model pollution by isolating foreign concepts using Anticorruption Layers.
*   Expose Bounded Contexts to the enterprise using use-case-driven Open Host Services and standard Published Languages.
*   Achieve high availability and eventual consistency through messaging and Domain Events rather than synchronous RPC calls or two-phase commits.
*   Minimize or completely eliminate duplicated information (state) across Bounded Contexts.
*   Ensure that all distributed operations gracefully handle out-of-order deliveries, network latency, and duplicate messages.

# @Guidelines
*   **Distributed Computing Principles**: The AI MUST design all integration points assuming the network is unreliable, latency exists, bandwidth is finite, topology changes, and the network is not secure. Never treat a remote call as an in-process call.
*   **Avoid Database Integration**: The AI MUST NOT integrate systems using shared databases or raw file-based integration.
*   **RESTful HTTP Constraints**: 
    *   When implementing RESTful services (Open Host Service), the AI MUST expose representations based on *client use cases*, NOT by dumping raw, one-to-one domain model Aggregate states.
    *   The AI MUST use standard HTTP methods semantically (GET for queries, PUT/POST for commands, DELETE for removal).
    *   To increase consumer autonomy when using REST, the AI MUST decouple the request using local timers or background polling mechanisms so that the client does not crash if the upstream REST service is temporarily unavailable.
*   **Published Language Implementation**: 
    *   The AI MUST NOT share compiled interfaces and class binaries between integrating systems to exchange data.
    *   The AI MUST define a custom media type or standard intermediate format (JSON, XML, Protocol Buffers) to represent the Published Language.
    *   The AI MUST use a generic reader (e.g., `NotificationReader` with XPath-like or dot-separated navigation) on the consumer side to parse only the needed data fields from the serialization.
*   **Anticorruption Layer (ACL) Architecture**: 
    *   When consuming a foreign service, the AI MUST implement an ACL consisting of a `Service` (facade interface in the domain), an `Adapter` (infrastructure class handling the network/HTTP request), and a `Translator` (mapping the foreign JSON/XML to a local object).
    *   The AI MUST translate foreign concepts into local *Value Objects*, not Entities, whenever possible to minimize the responsibility of maintaining lifecycle changes.
*   **Messaging and Eventual Consistency**:
    *   The AI MUST use asynchronous messaging and Domain Events to synchronize state across Bounded Contexts.
    *   The AI MUST ensure that the message sender limits the Domain Event payload to essential data (e.g., identities, occurredOn timestamps, and basic strings).
*   **Handling Information Duplication**:
    *   The AI MUST attempt to minimize information duplication across Contexts. Only immutable identity references should be duplicated by default.
    *   If duplication of mutable state is strictly required by an SLA, the AI MUST implement a `ChangeTracker` inside the local Aggregate. 
    *   The AI MUST use the `occurredOn` date from the Domain Event to discard out-of-order messages (e.g., an "unassigned" event arriving before an "assigned" event).
*   **Idempotency & De-duplication**: 
    *   The AI MUST design message handlers and API endpoints to be idempotent.
    *   If business logic cannot be made naturally idempotent, the AI MUST explicitly track processed message IDs in the subscriber's database and silently ignore/acknowledge duplicates.
*   **Long-Running Processes (Sagas)**:
    *   For multi-step integrations across Contexts, the AI MUST NOT use global/XA transactions.
    *   The AI MUST implement a Process state machine or `TimeConstrainedProcessTracker` to monitor completion.
    *   The AI MUST configure explicit retry limits, timeout thresholds, and exponential back-off delays.
    *   Upon a full timeout exhaustion, the AI MUST dispatch a compensation command or alert a human administrator via an event.

# @Workflow
When tasked with integrating two systems or Bounded Contexts, the AI MUST follow this exact sequence:

1.  **Assess the Relationship**: Determine the Context Map relationship (e.g., Upstream/Downstream, Open Host Service to Anticorruption Layer).
2.  **Select the Integration Style**: 
    *   Choose RESTful HTTP for fan-out, pull-based integrations where consumers need to query current/archived logs.
    *   Choose Messaging (Publish-Subscribe) for push-based, autonomous, eventually consistent integrations.
3.  **Define the Published Language**: Define the JSON/media-type payload. Ensure it contains `notificationId`, `occurredOn`, and specific string/primitive properties. Do not expose internal Domain objects.
4.  **Implement the Upstream Service (OHS)**:
    *   Create an Application Service to coordinate the transaction.
    *   Create the REST Controller/Adapter or Message Publisher to serialize the data and dispatch it.
5.  **Implement the Downstream Consumer (ACL)**:
    *   Create the specific `ExchangeListener` or HTTP Poller.
    *   Create an `Adapter` to receive the raw string payload.
    *   Create a `Translator` to parse the payload (using a generic reader) and instantiate a local **Value Object**.
    *   Create a `Service` to invoke the local Domain Model with the translated object.
6.  **Implement Resilience Mechanics**:
    *   Add idempotency checks in the consumer using the message ID.
    *   Add temporal version checking (`occurredOn`) to ignore out-of-order updates.
    *   Implement a `TimeConstrainedProcessTracker` if the integration spans multiple asynchronous steps.

# @Examples (Do's and Don'ts)

### [DO] Expose a RESTful resource based on a specific integration use case
```java
@Path("/tenants/{tenantId}/users")
public class UserResource {
    @GET
    @Path("{username}/inRole/{role}")
    @Produces({ OvationsMediaType.ID_OVATION_TYPE })
    public Response getUserInRole(
            @PathParam("tenantId") String aTenantId,
            @PathParam("username") String aUsername,
            @PathParam("role") String aRoleName) {
        
        User user = this.accessService().userInRole(aTenantId, aUsername, aRoleName);
        if (user != null) {
            return this.userInRoleResponse(user, aRoleName); // Returns Published Language JSON
        } else {
            return Response.noContent().build();
        }
    }
}
```

### [DON'T] Directly expose the raw Domain Model Aggregate through REST
```java
// ANTI-PATTERN: Exposing the internal Domain Model directly causes Shared Kernel/Conformist coupling
@GET
@Path("{username}")
public User getRawUser(@PathParam("username") String aUsername) {
    // This forces the client to understand the internal structure of 'User'
    return userRepository.findByUsername(aUsername); 
}
```

### [DO] Translate foreign payloads to local Value Objects using an Anticorruption Layer (ACL)
```java
public class CollaboratorTranslator {
    public <T extends Collaborator> T toCollaboratorFromRepresentation(
            String aUserInRoleRepresentation, Class<T> aCollaboratorClass) throws Exception {
        
        // Parse the Published Language using a generic reader
        RepresentationReader reader = new RepresentationReader(aUserInRoleRepresentation);
        String username = reader.stringValue("username");
        String firstName = reader.stringValue("firstName");
        String lastName = reader.stringValue("lastName");
        String emailAddress = reader.stringValue("emailAddress");

        // Instantiate a LOCAL Value Object
        Constructor<T> ctor = aCollaboratorClass.getConstructor(String.class, String.class, String.class);
        return ctor.newInstance(username, (firstName + " " + lastName).trim(), emailAddress);
    }
}
```

### [DON'T] Share compiled class binaries between Bounded Contexts
```java
// ANTI-PATTERN: Depending on a class from another Bounded Context
import com.foreigncontext.domain.User; 

public class LocalService {
    public void processForeignUser(User foreignUser) {
        // Tight coupling to the foreign domain model
    }
}
```

### [DO] Protect against out-of-order messages when duplicating state
```java
public abstract class Member extends Entity {
    private MemberChangeTracker changeTracker;

    public void disable(Date asOfDate) {
        // Check if this event occurred AFTER the last known state change
        if (this.changeTracker().canToggleEnabling(asOfDate)) {
            this.setEnabled(false);
            this.setChangeTracker(this.changeTracker().enablingOn(asOfDate));
        }
        // If it occurred before, silently ignore the out-of-order message
    }
}
```

### [DON'T] blindly update state without idempotency or temporal checks
```java
// ANTI-PATTERN: Assumes perfect network reliability and strict message ordering
public void handleUserDisabledEvent(UserDisabledEvent event) {
    Member member = repository.find(event.getMemberId());
    member.setEnabled(false); // Fails if an 'Enabled' event was sent after this but arrived first
    repository.save(member);
}
```

### [DO] Use a TimeConstrainedProcessTracker for Long-Running Processes
```java
@Transactional
public void startDiscussionInitiation(StartDiscussionInitiationCommand aCommand) {
    Product product = productRepository.productOfId(aCommand.getTenantId(), aCommand.getProductId());
    
    // Create a tracker to monitor the asynchronous cross-context request
    TimeConstrainedProcessTracker tracker = new TimeConstrainedProcessTracker(
            product.tenantId().id(),
            ProcessId.newProcessId(),
            "Create discussion for product: " + product.name(),
            new Date(),
            5L * 60L * 1000L, // retries every 5 minutes
            3,                // 3 total retries
            ProductDiscussionRequestTimedOut.class.getName());

    processTrackerRepository.add(tracker);
    product.setDiscussionInitiationId(tracker.processId().id());
    
    // Message is then published to messaging infrastructure...
}
```