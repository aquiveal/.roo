# @Domain
These rules MUST trigger when the AI is tasked with generating, refactoring, or analyzing the directory structure, module organization, system architecture, or dependency flow of a codebase. This includes any request involving Layered Architecture, Ports & Adapters (Hexagonal/Clean Architecture), Command-Query Responsibility Segregation (CQRS), or the wiring of business logic to infrastructural concerns (UI, databases, message brokers).

# @Vocabulary
- **Layered Architecture**: An organizational pattern dividing the codebase into horizontal layers (Presentation, Business Logic, Data Access), enforcing a strict top-down dependency model.
- **Presentation Layer (PL) / User Interface Layer**: The system's public interface, encompassing GUIs, CLIs, APIs, and message brokers used to receive input and communicate output.
- **Business Logic Layer (BLL) / Domain Layer**: The layer encapsulating business decisions and logic (Transaction Script, Active Record, Domain Model). The heart of the software.
- **Data Access Layer (DAL) / Infrastructure Layer**: The layer providing access to persistence mechanisms (databases, cloud storage, external APIs).
- **Service Layer / Application Layer**: A logical boundary acting as an intermediary facade between the PL and BLL, responsible for orchestrating business logic, managing transactions, and handling errors.
- **Tier**: A physical boundary representing an independently deployable service or server (distinct from a logical *Layer*).
- **Ports & Adapters (Hexagonal/Clean/Onion Architecture)**: An architectural pattern that decouples business logic from infrastructure using the Dependency Inversion Principle.
- **Dependency Inversion Principle (DIP)**: A principle dictating that high-level modules (business logic) must not depend on low-level modules (infrastructure). 
- **Port**: An interface defined within the Business Logic Layer that specifies how it interacts with external components.
- **Adapter**: A concrete implementation of a Port, residing in the Infrastructure Layer.
- **Command-Query Responsibility Segregation (CQRS)**: A pattern that segregates the responsibilities of a system's models into a Command Execution Model (for state modifications) and Read Models (for querying).
- **Command Execution Model**: The strongly consistent source of truth used to validate rules, enforce invariants, and execute operations that modify state.
- **Read Model (Projection)**: A pre-cached, read-only projection of data optimized for specific queries, residing in durable databases, flat files, or memory.
- **Synchronous Projection**: A projection strategy using a catch-up subscription model (e.g., via checkpoints or row versions) to fetch updated data from the execution model.
- **Asynchronous Projection**: A projection strategy using a message bus (pub/sub) to update read models.
- **Architectural Slices**: Vertical partitioning within a Bounded Context that defines logical boundaries for distinct subdomains, allowing each to use a different architectural pattern.

# @Objectives
- To prevent the diffusion of business logic into presentation or data access components by establishing strict architectural boundaries.
- To enforce the correct dependency flow based on the chosen architectural pattern (Top-Down for Layered, Inward/DIP for Ports & Adapters).
- To pair the correct architectural pattern with the corresponding business logic implementation pattern (e.g., Active Record with Layered Architecture; Domain Model with Ports & Adapters).
- To support polyglot modeling and event-sourced systems through the accurate implementation of CQRS.
- To localize architectural decisions to specific subdomains (Architectural Slices) rather than forcing a uniform architecture across an entire multifaceted Bounded Context.

# @Guidelines
- **Matching Architecture to Business Logic**: 
  - The AI MUST use a strict Layered Architecture (3 layers) when the business logic uses the Transaction Script pattern.
  - The AI MUST use a Layered Architecture with an added Service/Application Layer when the business logic uses the Active Record pattern.
  - The AI MUST use Ports & Adapters when the business logic uses the Domain Model pattern.
  - The AI MUST use CQRS (usually in conjunction with Ports & Adapters) when the business logic uses the Event-Sourced Domain Model pattern, or when polyglot persistence is required.
- **Layered Architecture Constraints**:
  - The AI MUST enforce a strict top-down dependency graph: Presentation -> Service (optional) -> Business Logic -> Data Access.
  - The AI MUST NOT allow the Business Logic Layer to reference the Presentation Layer.
  - The AI MUST NOT allow the Data Access Layer to reference the Business Logic Layer in a standard Layered Architecture.
  - The AI MUST clearly distinguish between *Layers* (logical code organization) and *Tiers* (physical deployment units); do not extract code into separate services just to create a "Layer".
- **Service Layer Constraints**:
  - The AI MUST implement the Service Layer as an orchestration facade. It must instantiate transaction scopes, load data, invoke business logic, commit/rollback transactions, and return an `OperationResult`.
  - The AI MUST NOT duplicate Transaction Script logic into a Service Layer. If the business logic *is* a Transaction Script, the BLL and Service Layer are functionally the same.
- **Ports & Adapters Constraints**:
  - The AI MUST combine Presentation and Data Access concerns into a single "Infrastructure Layer".
  - The AI MUST invert dependencies: The Infrastructure Layer MUST depend on the Business Logic Layer. The Business Logic Layer MUST NOT depend on the Infrastructure Layer.
  - The AI MUST define all interfaces (Ports) required for external integration (e.g., `IMessageBus`, `IRepository`) strictly within the Business Logic Layer.
  - The AI MUST implement the concrete classes (Adapters) strictly within the Infrastructure Layer.
- **CQRS Constraints**:
  - The AI MUST separate state-modifying operations (Commands) from read-only operations (Queries).
  - The AI MUST allow Commands to return data (e.g., execution results, validation errors, generated IDs, or updated state), provided the returned data originates EXCLUSIVELY from the strongly consistent Command Execution Model. Do not force Commands to return `void` if the caller needs immediate feedback.
  - The AI MUST NOT allow Queries to modify state or interact with the Command Execution Model; Queries must target the eventually consistent Read Models.
  - The AI MUST prioritize Synchronous Projections (catch-up subscriptions via checkpoints/rowversions) over Asynchronous Projections (pub/sub) to avoid distributed computing challenges (out-of-order delivery, duplication), unless specifically instructed otherwise.
- **Scope and Architectural Slices**:
  - The AI MUST NOT force a single architectural pattern across an entire Bounded Context if it contains multiple subdomains of varying complexity.
  - The AI MUST define vertical logical boundaries (Architectural Slices) per subdomain, allowing each module/namespace to utilize the architecture that fits its specific business logic pattern.

# @Workflow
1. **Analyze the Subdomain & Business Logic**: Determine the complexity of the specific business subdomain and its underlying business logic pattern (Transaction Script, Active Record, Domain Model, Event-Sourced Domain Model).
2. **Determine Architectural Scope**: Identify if the codebase spans multiple subdomains. If yes, partition the directory structure vertically into Architectural Slices (e.g., `/SubdomainA`, `/SubdomainB`) before applying horizontal architectural patterns.
3. **Select Architectural Pattern**:
   - Assign Layered Architecture for Transaction Script / Active Record.
   - Assign Ports & Adapters for Domain Model.
   - Assign CQRS for Event-Sourced Domain Model or high-scale read/write asymmetry.
4. **Scaffold the Structure**: Generate the directory and file structure corresponding to the selected pattern.
   - *Layered*: `/Presentation`, `/Application` (Service), `/Domain` (BLL), `/Infrastructure` (DAL).
   - *Ports & Adapters*: `/Core` (Domain + Ports), `/Application` (Use Cases), `/Infrastructure` (Adapters + UI).
   - *CQRS*: `/Commands`, `/Queries`, `/Projections`.
5. **Implement Dependency Rules**: Write code and module imports that strictly adhere to the dependency constraints of the chosen architecture (Top-Down vs. Dependency Inversion).
6. **Implement Integration logic**: Wire the application layer or service layer to handle transaction orchestration, port/adapter resolution, or CQRS command/query routing.

# @Examples (Do's and Don'ts)

## Dependency Inversion in Ports & Adapters
- **[DO]** Define the Port (Interface) in the Domain Layer and the Adapter (Implementation) in the Infrastructure Layer.
```csharp
// Domain Layer (Core)
namespace App.BusinessLogicLayer {
    public interface IMessaging {
        void Publish(Message payload);
    }
}

// Infrastructure Layer
namespace App.Infrastructure.Adapters {
    using App.BusinessLogicLayer;
    public class SQSBus : IMessaging {
        public void Publish(Message payload) { /* AWS SQS specific code */ }
    }
}
```
- **[DON'T]** Reference infrastructure-specific libraries or concrete implementations directly inside the Domain Layer.
```csharp
// DON'T do this: Domain Layer directly depending on Infrastructure
namespace App.BusinessLogicLayer {
    using Amazon.SQS; // VIOLATION: Infrastructure concern bleeding into Domain
    public class NotificationService {
        public void Publish(Message payload) {
            var client = new AmazonSQSClient();
            client.SendMessageAsync(...);
        }
    }
}
```

## Service Layer Orchestration
- **[DO]** Use the Service Layer to orchestrate transactions and handle errors, keeping the Presentation Layer clean.
```csharp
namespace ServiceLayer {
    public class UserService {
        public OperationResult Create(ContactDetails contactDetails) {
            try {
                _db.StartTransaction();
                var user = new User();
                user.SetContactDetails(contactDetails);
                user.Save();
                _db.Commit();
                return OperationResult.Success;
            } catch (Exception ex) {
                _db.Rollback();
                return OperationResult.Exception(ex);
            }
        }
    }
}

namespace PresentationLayer.Controllers {
    public class UserController : Controller {
        [HttpPost]
        public ActionResult Create(ContactDetails contactDetails) {
            var result = _userService.Create(contactDetails);
            return View(result);
        }
    }
}
```
- **[DON'T]** Mix transaction management and domain logic directly inside the Presentation Layer controller.
```csharp
// DON'T do this: Controller managing transactions and active records
namespace PresentationLayer.Controllers {
    public class UserController : Controller {
        [HttpPost]
        public ActionResult Create(ContactDetails contactDetails) {
            try {
                _db.StartTransaction(); // VIOLATION: Controller shouldn't manage DB transactions
                var user = new User();
                user.SetContactDetails(contactDetails);
                user.Save();
                _db.Commit();
                return View("Success");
            } catch {
                _db.Rollback();
                return View("Error");
            }
        }
    }
}
```

## CQRS Command Return Values
- **[DO]** Allow commands to return execution results or newly generated data from the strongly consistent model.
```csharp
public ExecutionResult EscalateTicket(TicketId id, EscalationReason reason) {
    try {
        var ticket = _ticketRepository.Load(id);
        var cmd = new Escalate(reason);
        ticket.Execute(cmd);
        _ticketRepository.Save(ticket);
        // Returning data from the strongly consistent execution model
        return ExecutionResult.Success(new { NewStatus = ticket.Status, UpdatedAt = ticket.LastModified });
    } catch (ConcurrencyException ex) {
        return ExecutionResult.Error(ex);
    }
}
```
- **[DON'T]** Force commands to return `void` and force the UI to blindly poll eventually consistent read models for the result of the exact action just taken.
```csharp
// DON'T do this: Returning void and hiding failure/success context from the caller
public void EscalateTicket(TicketId id, EscalationReason reason) {
    var ticket = _ticketRepository.Load(id);
    ticket.Execute(new Escalate(reason));
    _ticketRepository.Save(ticket);
    // VIOLATION: Caller has no idea if this succeeded, failed, or hit a concurrency exception.
}
```

## Architectural Slices
- **[DO]** Partition a Bounded Context vertically if it contains subdomains of varying complexity.
```text
/BoundedContext
  /Promotions (Supporting Subdomain)
    /Controllers
    /ActiveRecords
    /Views
  /Optimization (Core Subdomain)
    /Core (Domain Model)
    /Application (Use Cases)
    /Infrastructure (Adapters)
```
- **[DON'T]** Force a single, monolithic folder structure (e.g., forcing everything into a strict Ports & Adapters shape) across subdomains that require simple Transaction Scripts.