# @Domain
These rules MUST be triggered when the AI is tasked with designing, implementing, or refactoring the outermost layers of a Domain-Driven Design (DDD) application. This includes creating or modifying User Interfaces (UI), Application Services, Data Transfer Objects (DTOs), Domain Payload Objects (DPOs), Presentation Models, Command Objects, RESTful state representations, and Infrastructure configurations (such as dependency injection, transaction management, and security wiring).

# @Vocabulary
- **Application**: The finest set of components assembled to interact with and support a Core Domain model. This includes the domain model itself, the user interface, internally used Application Services, and infrastructural components.
- **Application Service**: A direct client of the domain model responsible for coordinating use case tasks, managing transactions, and enforcing security. It MUST NOT contain business domain logic.
- **Data Transfer Object (DTO)**: An object designed strictly to hold the entire number of attributes needed for a specific UI view, assembled by a DTO Assembler.
- **Domain Payload Object (DPO)**: A container object that holds references to whole Aggregate instances rather than individual attributes, used to transfer clusters of data within a single virtual machine architecture.
- **Domain Dependency Resolver (DDR)**: A strategy or mechanism used to force access to all lazy-loaded properties of an Aggregate before a transaction commits, preventing exceptions during view rendering.
- **Mediator (Double-Dispatch/Callback)**: An interface implemented by a client that the Aggregate double-dispatches to, publishing its internal state without exposing its shape or structure.
- **Presentation Model (View Model)**: An adapter that separates presentation from the view, providing properties and behaviors designed specifically for view needs (e.g., converting fluent domain methods to UI-required getters, deriving display logic, and tracking user edits).
- **Use Case Optimal Query**: A Repository finder method that dynamically places complex query results directly into a specifically designed Value Object to address the exact needs of a use case.
- **Command Object**: An object encapsulating a serialized method invocation request (input parameters) sent from the UI to an Application Service, mitigating long parameter lists.
- **Data Transformer**: An interface passed into an Application Service that dictates how the resulting domain data should be formatted (e.g., XML, JSON, CSV) via double-dispatch.

# @Objectives
- **Protect the Domain Model**: The AI MUST isolate the Domain Model from UI and infrastructure concerns. The Application Layer MUST act as a protective barrier.
- **Enforce Single Responsibility in Application Services**: The AI MUST ensure Application Services only handle task coordination, transaction boundaries, and security, delegating all domain logic to Aggregates or Domain Services.
- **Optimize UI Rendering**: The AI MUST select the most efficient and least coupling method to project Domain Model data to the UI, avoiding anemic data mapping where possible.
- **Invert Dependencies**: The AI MUST implement the Dependency Inversion Principle (DIP), ensuring infrastructure components depend on abstractions defined in the application or domain layers.

# @Guidelines

### User Interface & Rendering Domain Objects
- The AI MUST NOT map Aggregate states 1:1 to RESTful resources or UI views. Representations MUST be based on the use case.
- When the UI is NOT physically remote (i.e., operating in the same virtual machine), the AI SHOULD AVOID using DTOs to prevent accidental complexity.
- If avoiding DTOs, the AI MUST use one of the following alternatives:
  - **Domain Payload Object (DPO)**: Pass clusters of Aggregate references. The AI MUST ensure lazy-loaded relationships are resolved before the transaction closes using a Domain Dependency Resolver (DDR) or eager fetching.
  - **Mediator**: Pass an interest interface to the Aggregate. The Aggregate MUST push its internal state into the Mediator, preventing clients from navigating the Aggregate's internal structure.
  - **Use Case Optimal Query**: Query the repository for a custom Value Object specific to the use case. WARNING: If this is used excessively, the AI MUST evaluate if Aggregate boundaries are misaligned or if CQRS is required.

### Presentation Model & User Edits
- When dealing with UI frameworks that require JavaBean `get*` methods, the AI MUST NOT add these methods to the Domain Aggregates. Instead, the AI MUST use a Presentation Model.
- The Presentation Model MUST act as an adapter that exposes UI-friendly properties (e.g., converting `backlogItem.summary()` to `getSummary()`).
- The Presentation Model MUST track user edits and delegate to the Application Service to apply them. It MUST NOT perform the heavy lifting of the Application Service itself.

### Application Services
- The AI MUST keep Application Services thin. They MUST NOT contain business rules or domain logic.
- If an operation requires significant domain processing, the Application Service MUST delegate it to a Domain Service.
- The AI MUST use Command Objects (e.g., `ProvisionTenantCommand`) to encapsulate use case input when the parameter list becomes long. Command objects MAY use standard getters/setters to map easily from UI forms.
- **Decoupled Service Output**: To support disparate clients, the AI MAY design Application Services to return `void` and write their output to a standard output Port (Ports and Adapters style), or accept a `DataTransformer` parameter that double-dispatches the output format.
- **Composing Multiple Models**: If a single UI requires data from multiple Bounded Contexts, the AI MUST use a single Application Layer to compose the models. This layer acts as a new Bounded Context with a built-in Anticorruption Layer.

### Infrastructure & Containers
- The AI MUST place Repository implementations, messaging adapters, and charting/UI generation tools in the Infrastructure Layer.
- The AI MUST configure infrastructure to implement interfaces defined by the Domain or Application layers (DIP).
- The AI MUST use an Enterprise Component Container (e.g., Spring) or equivalent Service Factory to inject Repository and Domain Service dependencies into Application Services.
- The AI MUST use declarative transaction management (e.g., `@Transactional`) at the Application Service method level.

# @Workflow
When tasked with developing or modifying the Application, UI, or Infrastructure components, the AI MUST follow this algorithmic process:

1. **Analyze the Use Case:** Identify the exact UI or external client requirement. Determine the input parameters and the required output format/view.
2. **Design the Input (Command Object):** If the input requires more than 3-4 primitive parameters, create a Command Object in the Application Layer to encapsulate the request.
3. **Implement the Application Service:**
   - Define the API method for the use case.
   - Apply transaction management (e.g., `@Transactional`) and security annotations (e.g., `@PreAuthorize`).
   - Look up the required Aggregate(s) via injected Repositories.
   - Delegate business logic to the Aggregate(s) or a Domain Service.
4. **Design the Output/Rendering Strategy:**
   - Decide between DTO, DPO, Mediator, Data Transformer, or a Use Case Optimal Query based on client locality and framework constraints.
   - If UI framework requires getters, build a Presentation Model mapping the fluent domain methods to standard JavaBean getters.
5. **Implement Infrastructure:** Ensure all persistence and messaging implementations reside in the Infrastructure package and are injected via the container (e.g., Spring XML/Annotations or equivalent registry).

# @Examples (Do's and Don'ts)

### Application Service Implementation
**[DO]** Use an Application Service to coordinate tasks, handle transactions, and use Command objects for input.
```java
public class TenantIdentityService {
    @Autowired
    private TenantProvisioningService tenantProvisioningService;

    @Transactional
    @PreAuthorize("hasRole('SubscriberRepresentative')")
    public String provisionTenant(ProvisionTenantCommand aCommand) {
        // App Service delegates business logic to the Domain Service
        Tenant tenant = this.tenantProvisioningService.provisionTenant(
            aCommand.getTenantName(),
            aCommand.getTenantDescription(),
            aCommand.isActive(),
            aCommand.getAdministratorName(),
            aCommand.getEmailAddress()
        );
        return tenant.tenantId().id();
    }
}
```

**[DON'T]** Put domain logic, Aggregate instantiation rules, or Event publishing directly into the Application Service.
```java
// INCORRECT: Domain logic leaked into Application Service
public class TenantIdentityService {
    @Transactional
    public String provisionTenant(ProvisionTenantCommand aCommand) {
        Tenant tenant = new Tenant(aCommand.getTenantName());
        tenant.setActive(aCommand.isActive());
        
        // App service shouldn't manually create admin roles and publish domain events!
        Role adminRole = new Role("Admin");
        adminRole.assignTo(tenant);
        DomainEventPublisher.instance().publish(new TenantProvisioned(tenant.id()));
        
        tenantRepository.save(tenant);
        return tenant.tenantId().id();
    }
}
```

### Decoupling Aggregate Internal State for the UI
**[DO]** Use a Mediator (Callback) to safely extract Aggregate state without exposing its internal structure, OR use a Presentation Model.
```java
// Aggregate Method
public void provideBacklogItemInterest(BacklogItemInterest anInterest) {
    anInterest.informTenantId(this.tenantId().id());
    anInterest.informStory(this.story());
    anInterest.informSummary(this.summary());
}

// Presentation Model adapting domain language to UI framework requirements
public class BacklogItemPresentationModel extends AbstractPresentationModel {
    private BacklogItem backlogItem;

    public BacklogItemPresentationModel(BacklogItem aBacklogItem) {
        this.backlogItem = aBacklogItem;
    }

    // Adapts fluent domain method "summary()" to framework required "getSummary()"
    public String getSummary() {
        return this.backlogItem.summary();
    }
}
```

**[DON'T]** Add JavaBean getters and setters to the Domain Aggregate just to satisfy UI rendering frameworks.
```java
// INCORRECT: Corrupting the Aggregate with UI-specific getters/setters
public class BacklogItem extends Entity {
    // Domain methods should be fluent (e.g., summary()), not getSummary()
    public String getSummary() { 
        return this.summary;
    }
    public void setSummary(String summary) { // Exposes state mutation unnecessarily
        this.summary = summary;
    }
}
```

### Handling Disparate Client Outputs
**[DO]** Use a Data Transformer to allow the Application Service to double-dispatch the required format for disparate clients.
```java
@Transactional(readOnly=true)
public CalendarWeekData calendarWeek(Date aDate, CalendarWeekDataTransformer aTransformer) {
    Calendar calendar = calendarRepository.calendarFor(aDate);
    // Double dispatch
    calendar.provideCalendarWeekInterest(aTransformer);
    return aTransformer.value(); 
}
```

**[DON'T]** Hardcode JSON, XML, or HTML generation directly inside the Application Service or Domain Model.