# @Domain
These rules MUST be triggered whenever the AI is requested to design, architect, refactor, or implement domain (business) logic in an enterprise application. This includes tasks involving the structuring of business rules, validation, calculations, system transaction boundaries, and the interface between the presentation layer and data access layer.

# @Vocabulary
- **Domain Logic (Business Logic)**: The core validations, calculations, and derivations based on application inputs and stored data.
- **Application Logic (Workflow Logic)**: Logic related to application responsibilities and use case coordination, such as notifying users or integrated applications, distinct from pure problem-domain logic.
- **Transaction Script**: A procedural organization of business logic where each procedure (or script) handles a single request from the presentation layer.
- **Domain Model**: An object-oriented model of the domain that seamlessly incorporates both behavior and data, often featuring complex webs of interconnected objects, inheritance, and strategies.
- **Table Module**: A domain logic pattern where a single class instance handles the business logic for all rows in a database table or view, designed to work directly with a Record Set.
- **Service Layer**: A boundary layer that defines available operations, coordinates application logic (workflow), and controls transactions, delegating pure domain logic to underlying objects.
- **Record Set**: A generic, tabular data structure (e.g., ADO.NET DataSet) representing the result of a database query.
- **POJO (Plain Old Java Object)**: A standard, unencumbered object not tied to an external framework (like EJB), highly recommended for implementing Domain Models.
- **Domain Facade**: A Service Layer implementation variation consisting of thin facades over a Domain Model, where the Domain Model contains all business logic.
- **Operation Script**: A Service Layer implementation variation consisting of thicker classes that directly implement application logic but delegate to encapsulated domain objects for domain logic.
- **Command Pattern**: An object-oriented design pattern used in Transaction Scripts to encapsulate each script within its own distinct class.

# @Objectives
- **Match Architecture to Complexity**: The AI MUST select the appropriate domain logic pattern (Transaction Script, Domain Model, or Table Module) strictly based on the complexity of the business rules and the target platform's tooling.
- **Enforce Separation of Concerns**: The AI MUST isolate domain logic from presentation and data source mechanics. Domain objects MUST NOT depend on or call presentation logic.
- **Maximize Cohesion**: The AI MUST keep behavior and the data it acts upon together.
- **Optimize Distribution**: The AI MUST minimize object distribution and remote calls, preferring colocated, locally invocable Service Layers over premature remote distributions.

# @Guidelines

## General Domain Logic Rules
- The AI MUST evaluate the complexity of the domain before selecting a pattern.
- The AI MUST NOT leak presentation concepts (e.g., HTML, UI widgets, HttpRequest objects) into any domain logic pattern.
- The AI MUST NOT separate usage-specific behavior from domain objects simply to prevent "bloat." Place behavior in the object that is the natural fit, and refactor for bloat only if it becomes an actual problem.

## Transaction Script Constraints
- **Usage**: Use ONLY for simple business logic (e.g., straightforward CRUD operations, simple validations).
- **Structure**: Organize as either a single class containing several related scripts (grouped by subject area) or one class per Transaction Script (using the Command Pattern).
- **Dependencies**: The script MUST NOT contain any calls to presentation logic.
- **Data Access**: The script should interact with the database directly or via a thin wrapper (like Table Data Gateway or Row Data Gateway).

## Domain Model Constraints
- **Usage**: Use for complex, volatile business logic requiring validations, calculations, derivations, inheritance, and strategy patterns.
- **Behavior & Data**: EVERY class in the Domain Model MUST contain both data and the behavior that operates on that data.
- **Rich vs. Simple**: 
  - For simple models isomorphic to the database, use the Active Record pattern. 
  - For rich models with divergent database schemas, use the Data Mapper pattern to ensure complete isolation from the database.
- **Framework Independence**: The AI MUST prefer POJOs (or equivalent plain objects in other languages) over heavy framework-bound objects (like Entity Beans) to allow testing outside of a container and to support re-entrancy.

## Table Module Constraints
- **Usage**: Use predominantly in environments with strong `Record Set` tooling (e.g., .NET, ADO.NET, COM). 
- **Structure**: Create exactly ONE class per database table (or view). Create exactly ONE instance of this class to handle all rows in a given Record Set.
- **Identity**: The Table Module MUST NOT have a notion of individual object identity. All methods acting on a specific record MUST accept an identity reference (e.g., a primary key) as a parameter.
- **Data Passing**: The Table Module MUST accept a Record Set as an argument, perform business logic on it, and pass the modified Record Set to the presentation or data source layers.

## Service Layer Constraints
- **Usage**: Use when the application has multiple kinds of clients (e.g., UI and integration gateways) or when use cases involve coordinating multiple transactional resources.
- **Logic Segregation**: The Service Layer MUST contain ONLY application/workflow logic. Pure domain logic MUST be delegated to the Domain Model or Table Module.
- **API Design**: Define the Service Layer operations around the system's use cases (e.g., a 1:1 correspondence with CRUD use cases + coordination).
- **Locality**: The Service Layer MUST be designed for local invocation using domain objects in its method signatures by default. DO NOT introduce Remote Facades or Data Transfer Objects (DTOs) unless distribution is explicitly required.

# @Workflow
When tasked with creating or refactoring business logic, the AI MUST follow this exact sequence:

1. **Complexity & Environment Assessment**:
   - IF the platform heavily utilizes Record Sets (e.g., .NET) AND logic is moderate: Select **Table Module**.
   - IF the business rules are simple, sequential, and procedural: Select **Transaction Script**.
   - IF the business rules are highly complex, varying, or require OO concepts (inheritance/polymorphism): Select **Domain Model**.

2. **Layering & Boundaries Definition**:
   - Extract any UI/presentation parsing out of the domain logic.
   - IF the application requires coordinating multiple transactional resources (e.g., DB update + Email + Message Queue) OR has multiple client types: Create a **Service Layer** to act as the boundary.

3. **Implementation**:
   - **For Transaction Script**: Group procedures by subject area. Ensure SQL access is handled via Gateways.
   - **For Domain Model**: Create fine-grained objects combining data and behavior. Apply Strategy patterns for conditional branching. Do NOT add database connection code directly in the domain objects unless using Active Record for a simple model.
   - **For Table Module**: Define the class around the tabular data structure. Implement methods that accept a RecordSet and an ID.
   - **For Service Layer**: Implement an Operation Script or Domain Facade. Ensure transaction boundaries are opened and closed within the Service Layer methods.

4. **Review**:
   - Verify NO presentation logic exists in the domain.
   - Verify NO usage-specific logic has been prematurely separated from a Domain Model.
   - Verify the Service Layer operates locally by default.

# @Examples (Do's and Don'ts)

## 1. Separation of Presentation and Domain Logic
**[DON'T]** Leak presentation artifacts into a Transaction Script or Domain Model.
```java
public class RevenueRecognitionScript {
    // BAD: Depending on HttpServletRequest in the domain logic
    public void calculateRevenue(HttpServletRequest request) {
        String contractId = request.getParameter("contractId");
        // ... business logic ...
    }
}
```

**[DO]** Pass only extracted, pure data into the domain logic.
```java
public class RevenueRecognitionScript {
    // GOOD: Pure domain logic signature
    public Money recognizedRevenue(long contractNumber, MfDate asOf) {
        Money result = Money.dollars(0);
        ResultSet rs = db.findRecognitionsFor(contractNumber, asOf);
        while (rs.next()) {
            result = result.add(Money.dollars(rs.getBigDecimal("amount")));
        }
        return result;
    }
}
```

## 2. Domain Model Data and Behavior Cohesion
**[DON'T]** Create anemic domain models where data is separate from behavior, or rely entirely on external procedural scripts to modify domain data.
```java
public class RevenueRecognition {
    private Money amount;
    private MfDate date;
    // BAD: Only getters/setters, no behavior
}

public class RecognitionCalculator {
    // BAD: Logic separated from the data it operates on
    public boolean isRecognizableBy(RevenueRecognition rr, MfDate asOf) {
        return asOf.after(rr.getDate()) || asOf.equals(rr.getDate());
    }
}
```

**[DO]** Combine data and behavior within the Domain Model objects.
```java
public class RevenueRecognition {
    private Money amount;
    private MfDate date;
    
    public RevenueRecognition(Money amount, MfDate date) {
        this.amount = amount;
        this.date = date;
    }

    // GOOD: Behavior lives with the data
    boolean isRecognizableBy(MfDate asOf) {
        return asOf.after(date) || asOf.equals(date);
    }
}
```

## 3. Table Module Implementation
**[DON'T]** Manage individual object identity as instance state in a Table Module.
```csharp
class Contract : TableModule {
    private long currentContractId; // BAD: Table Module should not hold specific identity state
    
    public void CalculateRecognitions() {
        DataRow contractRow = this[currentContractId];
        // ...
    }
}
```

**[DO]** Pass identity into the methods while holding the Record Set (DataSet) at the instance level.
```csharp
class Contract : TableModule {
    public Contract (DataSet ds) : base (ds, "Contracts") {}

    // GOOD: Identity is passed as a parameter to the method
    public void CalculateRecognitions (long contractID) {
        DataRow contractRow = this[contractID];
        Decimal amount = (Decimal)contractRow["amount"];
        // ... apply business logic to Record Set ...
    }
}
```

## 4. Service Layer Coordination
**[DON'T]** Put application logic (workflow, external notifications) directly into pure Domain Model objects.
```java
class Contract {
    public void calculateRecognitions() {
        product.calculateRevenueRecognitions(this);
        // BAD: Domain object knows about email and integration gateways
        EmailGateway.sendEmail(...);
    }
}
```

**[DO]** Use a Service Layer to coordinate the transaction and application logic, delegating pure business rules to the Domain Model.
```java
public class RecognitionService extends ApplicationService {
    // GOOD: Service Layer acts as boundary, handles transactions and application workflow
    public void calculateRevenueRecognitions(long contractNumber) {
        Contract contract = Contract.readForUpdate(contractNumber);
        
        // Delegate domain logic to Domain Model
        contract.calculateRecognitions(); 
        
        // Handle application logic/workflow
        getEmailGateway().sendEmailMessage(
            contract.getAdministratorEmailAddress(),
            "RE: Contract #" + contractNumber,
            "Revenue recognitions calculated.");
            
        getIntegrationGateway().publishRevenueRecognitionCalculation(contract);
    }
}
```