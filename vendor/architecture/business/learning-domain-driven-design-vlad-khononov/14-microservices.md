# @Domain
These rules trigger when the AI is tasked with designing, architecting, evaluating, or refactoring microservices, distributed systems, service boundaries, or APIs. This includes requests to break down a monolith, define service granularity, design inter-service communication, or map domain-driven design (DDD) concepts (Aggregates, Bounded Contexts, Subdomains) to physical services.

# @Vocabulary
- **Service**: A mechanism that enables access to one or more capabilities using a prescribed public interface (the "front door").
- **Microservice**: A service with a micro-public interface that encapsulates its database and balances local and global complexity.
- **Local Complexity**: The complexity of an individual microservice's internal implementation.
- **Global Complexity**: The complexity of the overall system structure, defined by the degree of association, interactions, and interdependence among services.
- **Deep Module/Service**: A service where a simple, narrow public interface encapsulates complex internal business logic.
- **Shallow Module/Service**: A service where the public interface is almost as complex as its internal logic (e.g., a service exposing a single method). This increases global complexity.
- **Distributed Big Ball of Mud**: An anti-pattern resulting from over-decomposing a system into overly fine-grained, shallow services that require massive integration overhead to function together.
- **Bounded Context (in relation to Microservices)**: The widest valid physical boundary for a system. All microservices are bounded contexts, but not all bounded contexts are microservices.
- **Subdomain**: A fine-grained business capability representing a set of coherent use cases. The safest heuristic for defining microservice boundaries.
- **Open-Host Service (OHS)**: A pattern that decouples a service's implementation model from its integration model (published language) to compress the public interface.
- **Anticorruption Layer (ACL)**: A pattern (sometimes deployed as a standalone service) that reduces the complexity of integrating with upstream services by translating foreign models into the consumer's model.

# @Objectives
- The AI MUST design microservices as "deep services" with minimal public interfaces that encapsulate rich internal complexity.
- The AI MUST balance local complexity (within the service) and global complexity (between services).
- The AI MUST align microservice boundaries with business subdomains, rejecting both overly broad monoliths and overly narrow, single-method/single-aggregate services.
- The AI MUST prevent the creation of "distributed big balls of mud" by minimizing integration complexity and inter-service chatter.
- The AI MUST ensure absolute database encapsulation within every designed microservice.

# @Guidelines
- **Define by Interface, Not Size:** The AI MUST define a microservice by the small size of its public interface ("micro-front door"), NOT by lines of code, team size, or ease of rewriting.
- **Database Encapsulation:** The AI MUST ensure that every microservice encapsulates its database. Data MUST ONLY be accessed via the service's integration-oriented public interface.
- **Avoid Naïve Decomposition (Shallow Services):** The AI MUST NOT decompose services to the level of single methods or individual aggregates if doing so creates "shallow modules" that force heavy integration overhead.
- **Optimize System Complexity:** The AI MUST balance global and local complexity. If reducing local complexity (making a service smaller) exponentially increases global complexity (inter-service communication), the AI MUST revert to a coarser-grained boundary.
- **Align with Subdomains:** The AI MUST use business *Subdomains* (coherent sets of use cases operating on related data) as the primary heuristic for drawing microservice boundaries, as they naturally form deep modules.
- **Reject Aggregate-Based Services:** The AI MUST NOT default to exposing individual DDD Aggregates as microservices. Aggregates are transactional boundaries, and making them physical services usually results in highly coupled, chatty systems.
- **Understand Bounded Context Asymmetry:** The AI MUST recognize that while a microservice is a bounded context (a model boundary owned by one team), a bounded context can safely encompass multiple subdomains and does not automatically need to be split into microservices unless justified by non-functional requirements.
- **Compress Public Interfaces:** The AI MUST use the Open-Host Service pattern to expose a simplified "published language" rather than the internal implementation model.
- **Isolate Integration Complexity:** The AI MUST utilize Anticorruption Layers (as internal layers or standalone services) to strip away integration complexity from the consuming service's business logic, thereby compressing its interface.

# @Workflow
1. **Analyze System Functionality:** When asked to design or decompose a system, first identify the overarching business problem and group the functionality into coherent use cases (Subdomains).
2. **Define Boundaries:** Map physical microservice boundaries to the identified Subdomains. Refuse requests to break services down to the level of individual methods or standalone Aggregates.
3. **Design the "Front Door":** Define the public interface for the microservice. Ensure it is "deep"—the API surface area must be vastly smaller and simpler than the internal logic it abstracts.
4. **Encapsulate State:** Assign an isolated database/data-store to the microservice. Remove any external dependencies that attempt to read from or write to this database directly.
5. **Evaluate Global vs. Local Complexity:** Review the integration points between the proposed services. If completing a standard business transaction requires excessive "chatter" between services, merge the excessively coupled services into a deeper, single microservice.
6. **Apply Interface Compression:** Introduce an Open-Host Service (published language) for outgoing integrations, ensuring internal implementation details are not leaked. Introduce an Anticorruption Layer for incoming integrations to shield the new service from upstream complexity.

# @Examples (Do's and Don'ts)

- **[DO] Aligning Microservices with Subdomains (Deep Module)**
  ```csharp
  // The service acts as a deep module aligned with the "Backlog Management" subdomain.
  // It encapsulates complex logic (prioritization, routing, state management) behind a simple interface.
  public interface IBacklogManagementService
  {
      TicketId CreateTicket(TicketDetails details);
      void AssignTicket(TicketId ticketId, UserId agentId);
      void ResolveTicket(TicketId ticketId, Resolution details);
  }
  ```

- **[DON'T] Aligning Microservices with Single Methods or Aggregates (Shallow Module)**
  ```csharp
  // Anti-pattern: Naive decomposition into shallow services.
  // This creates a "Distributed Big Ball of Mud" with massive global complexity.
  public interface ICreateTicketService 
  {
      TicketId Execute(TicketDetails details);
  }

  public interface IAssignTicketService 
  {
      // Requires deep database integration with ICreateTicketService's data
      void Execute(TicketId ticketId, UserId agentId); 
  }
  ```

- **[DO] Compressing Interfaces with Open-Host Service**
  ```csharp
  // Internal aggregate model is rich and complex
  internal class CampaignAggregate { ... }

  // Public interface exposes only a compressed, integration-oriented "Published Language"
  public interface ICampaignService
  {
      CampaignDto GetCampaignSummary(CampaignId id); // CampaignDto is the published language
  }
  ```

- **[DON'T] Leaking Implementation Details into the Public Interface**
  ```csharp
  // Anti-pattern: Exposing the internal database or aggregate structure directly.
  // This inflates the "front door" and tightly couples consumers to implementation details.
  public interface ICampaignService
  {
      DbResultSet<CampaignDataRow> GetCampaignsBySql(string sqlQuery);
  }
  ```