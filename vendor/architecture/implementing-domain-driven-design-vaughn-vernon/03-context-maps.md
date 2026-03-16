# @Domain

This rule file is activated whenever the AI is requested to design, analyze, or implement integrations between multiple software systems, subsystems, or Bounded Contexts. It applies to tasks involving cross-team technical dependencies, API consumption, message-based system integration, translation layers between different models, and the creation of integration diagrams or documentation representing the relationships between distinct software models.

# @Vocabulary

- **Context Map:** A visual diagram and corresponding source code implementation that captures the existing terrain of Bounded Contexts and the integration relationships between them.
- **Bounded Context:** An explicit linguistic boundary within which a specific domain model and Ubiquitous Language apply.
- **Upstream (U):** The Bounded Context that provides information or services. Its actions and changes influence the downstream context.
- **Downstream (D):** The Bounded Context that consumes information or services from the upstream context. It is dependent on the upstream context.
- **Partnership:** An integration relationship where two teams succeed or fail together, requiring coordinated planning, joint management, and synchronized releases.
- **Shared Kernel:** An explicit, carefully restricted subset of the domain model and associated code shared intimately between two teams. 
- **Customer-Supplier Development:** A relationship where the upstream team (Supplier) accommodates the priorities and requirements of the downstream team (Customer).
- **Conformist:** A relationship where the downstream team slavishly adheres to the upstream team's model because the upstream team has no motivation to accommodate the downstream team's needs.
- **Anticorruption Layer (ACL):** A defensive translation layer created by a downstream client to isolate its own domain model from the upstream system's model and functionality.
- **Open Host Service (OHS):** A protocol defined by an upstream subsystem to give access to its services, open to all who need to integrate with it.
- **Published Language (PL):** A well-documented shared language (often XML or JSON schemas) used as a common medium of communication between models, typically combined with OHS.
- **Separate Ways:** A deliberate decision to cut two sets of functionality completely loose from each other due to the high cost and low benefit of integration.
- **Big Ball of Mud:** A messy, mixed model with inconsistent boundaries. A boundary is drawn around it to prevent it from sprawling into and corrupting other contexts.
- **Translation Map:** The specific logic/code that maps a representational state (e.g., a JSON payload from an OHS) into a valid object (usually a Value Object) in the local downstream model.
- **Autonomous Service:** A service that limits direct real-time dependencies (like RPC) on other systems, often utilizing asynchronous messaging and eventual consistency to remain operational even if dependencies fail.

# @Objectives

- The AI MUST map the *current*, existing landscape of systems and integrations, not an idealized future state.
- The AI MUST use Context Maps to explicitly define organizational relationships and inter-team communication contracts.
- The AI MUST protect the purity of downstream domain models by isolating them from upstream changes using appropriate translation mechanisms.
- The AI MUST favor system autonomy by decoupling Bounded Contexts temporally and technically wherever possible.
- The AI MUST treat the Context Map as both a communication tool (diagram/discussion) and a concrete code implementation.

# @Guidelines

- **Map the Present:** The AI MUST document and implement Context Maps based on the current existing terrain of the project. Future integrations should only be mapped when their implementation begins.
- **Avoid Enterprise Architecture Diagrams:** The AI MUST NOT treat Context Maps as system topology or enterprise architecture diagrams. Context Maps MUST focus strictly on interacting models, linguistic boundaries, and DDD organizational patterns.
- **Explicit Upstream/Downstream (U/D) Labeling:** The AI MUST explicitly label integrating contexts as Upstream (U) or Downstream (D) to clearly indicate the direction of influence and dependency.
- **Protect Downstream Models (ACL):** When integrating a downstream context with an upstream context that it does not control, the AI MUST implement an Anticorruption Layer (ACL) to translate upstream representations into local downstream concepts.
- **Translate to Value Objects:** When consuming data through an ACL, the AI MUST attempt to translate the remote representation into local, immutable Value Objects rather than deeply coupled Entities, adhering to the integration principle of minimalism.
- **Expose Services Safely (OHS/PL):** When acting as an upstream provider for multiple consumers, the AI MUST define an Open Host Service (OHS) combined with a Published Language (PL) (e.g., RESTful resources using custom media types) rather than exposing the raw domain model or database schemas directly.
- **Isolate the Mess (Big Ball of Mud):** When encountering a legacy system with inconsistent models, the AI MUST explicitly designate it as a Big Ball of Mud, restrict sophisticated modeling within it, and forcefully isolate other contexts from it using an ACL.
- **Avoid RPC for Autonomy:** To achieve autonomous services, the AI MUST favor asynchronous, event-driven integrations (Domain Events via messaging) over synchronous Remote Procedure Calls (RPC), accepting eventual consistency as a standard practice.
- **Explicitly Model Remote Unavailability:** When a local Bounded Context depends on the creation of a resource in a remote Bounded Context, the AI MUST explicitly model the availability states of that resource (e.g., `ADD_ON_NOT_ENABLED`, `NOT_REQUESTED`, `REQUESTED`, `READY`) to gracefully handle eventual consistency and asynchronous delays.
- **Avoid Ceremonious Documentation:** The AI MUST keep Context Map documentation informal and communicative, avoiding heavy, rigid diagramming ceremonies that stifle team agility.

# @Workflow

When instructed to integrate two or more systems or map their relationships, the AI MUST follow this algorithmic process:

1. **Identify the Bounded Contexts:** Determine the distinct models involved in the integration request.
2. **Determine the Integration Direction:** Identify which system provides the data/behavior (Upstream) and which consumes it (Downstream).
3. **Assess the Organizational Relationship:** Determine the team dynamics (e.g., Customer-Supplier, Conformist, Partnership) to select the correct technical integration pattern.
4. **Select the Integration Patterns:**
   - If Upstream exposing to many: Apply Open Host Service (OHS) and Published Language (PL).
   - If Downstream needing protection: Apply Anticorruption Layer (ACL).
   - If integrating with a messy legacy system: Apply Big Ball of Mud boundary and ACL.
5. **Design the Published Language (Upstream):** If acting as Upstream, define the exact payload representations (e.g., JSON schemas) that will be shared via the OHS.
6. **Design the Translation Map (Downstream):** If acting as Downstream, map the exact fields from the upstream PL payload to a specifically crafted, localized Value Object in the downstream domain model.
7. **Implement State Management for Async Operations:** If the integration relies on asynchronous messaging/Domain Events, implement explicit state tracking (e.g., `REQUESTED`, `READY`) in the local model to represent the pending status of the remote integration.

# @Examples (Do's and Don'ts)

### [DO] Implement an Anticorruption Layer (ACL) Translating Upstream Data to a Local Value Object

**Scenario:** A downstream Collaboration Context needs user information from an upstream Identity Context.

```java
// Inside the Downstream Collaboration Context's Infrastructure Layer

public class UserInRoleAdapter {
    public Author toCollaborator(Tenant aTenant, String anIdentity, String aRoleName) {
        // 1. Fetch from Upstream Open Host Service (OHS)
        ClientResponse<String> response = restClient.get(aTenant, anIdentity, aRoleName);
        
        // 2. Translate using a Translation Map
        if (response.getStatus() == 200) {
            return new CollaboratorTranslator().toAuthorFromRepresentation(response.getEntity());
        }
        throw new IllegalStateException("Upstream user not found or not in role.");
    }
}

public class CollaboratorTranslator {
    public Author toAuthorFromRepresentation(String aUserInRoleRepresentation) {
        // Parse Published Language (PL) JSON
        RepresentationReader reader = new RepresentationReader(aUserInRoleRepresentation);
        String username = reader.stringValue("username");
        String firstName = reader.stringValue("firstName");
        String lastName = reader.stringValue("lastName");
        String emailAddress = reader.stringValue("emailAddress");

        // Instantiate local Downstream Value Object
        return new Author(username, (firstName + " " + lastName).trim(), emailAddress);
    }
}
```

### [DON'T] Expose the Internal Domain Model as the Integration API (Accidental Conformist / Shared Kernel)

**Scenario:** An upstream system needs to provide data to downstream consumers.

```java
// ANTI-PATTERN: Returning internal Domain Entities directly over the network API.
// This forces downstream consumers to understand the upstream internal model, 
// creating brittle, tightly coupled "Conformist" relationships.

@Path("/tenants/{tenantId}/users")
public class UserResource {
    
    @GET
    @Path("{username}")
    public User getUser(@PathParam("tenantId") String tenantId, @PathParam("username") String username) {
        // DON'T return the actual Aggregate/Entity directly. 
        // This leaks database structure and domain behavior to consumers.
        return userRepository.findByUsername(tenantId, username);
    }
}
```

### [DO] Explicitly Model Remote Unavailability for Eventual Consistency

**Scenario:** The local Agile PM context requests the creation of a Discussion in the remote Collaboration context asynchronously.

```java
// Local Downstream Model Explicitly tracking the remote state

public enum DiscussionAvailability {
    ADD_ON_NOT_ENABLED, 
    NOT_REQUESTED, 
    REQUESTED, // Waiting for remote system to process the Domain Event
    READY;     // Remote system confirmed creation
}

public final class ProductDiscussion {
    private DiscussionAvailability availability;
    private DiscussionDescriptor descriptor; // Contains remote ID once READY

    public ProductDiscussion(DiscussionDescriptor descriptor, DiscussionAvailability availability) {
        this.descriptor = descriptor;
        this.availability = availability;
    }
    
    public boolean isReady() {
        return this.availability == DiscussionAvailability.READY;
    }
    
    public ProductDiscussion nowReady(DiscussionDescriptor aDescriptor) {
        if (this.isReady()) {
            throw new IllegalStateException("Already ready.");
        }
        return new ProductDiscussion(aDescriptor, DiscussionAvailability.READY);
    }
}
```

### [DON'T] Treat Context Maps as System Topology Diagrams

**Scenario:** Creating a visual or textual Context Map.

```text
// ANTI-PATTERN: Focusing on infrastructure rather than linguistic boundaries and team relationships.

[DON'T DO THIS]
Load Balancer -> Web Server -> App Server (Tomcat) -> Oracle Database

[DO THIS INSTEAD]
[Identity & Access Context] (Upstream, OHS, PL) ---> (ACL, Downstream) [Collaboration Context]
```