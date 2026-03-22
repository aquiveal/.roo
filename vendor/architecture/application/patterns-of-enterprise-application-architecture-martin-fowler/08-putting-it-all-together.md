# @Domain

These rules MUST be triggered whenever the AI is tasked with designing, refactoring, or implementing the high-level architecture of an enterprise application. Activation conditions include:
- Establishing or modifying the primary layering scheme (Presentation, Domain, Data Source) of a system.
- Deciding how to organize and structure business/domain logic.
- Selecting the object-relational mapping strategy to connect domain logic to a database.
- Designing the presentation layer (Web interfaces, controllers, and views).
- Defining distribution boundaries, remote interfaces, or Web Services within an application.
- Making architectural decisions specific to enterprise platforms (Java/J2EE, .NET).

# @Vocabulary

- **Transaction Script**: A procedural organization of business logic where each procedure handles a single request from the presentation.
- **Domain Model**: An object model of the domain that incorporates both behavior and data, representing complex business logic.
- **Table Module**: A domain logic pattern where a single instance handles the business logic for all rows in a database table or view, designed to work with a Record Set.
- **Record Set**: An in-memory representation of tabular data (e.g., ADO.NET Data Set, JDBC RowSet).
- **Row Data Gateway**: An object that acts as a gateway to a single record in a data source.
- **Table Data Gateway**: An object that acts as a gateway to a database table, handling all SQL for that table.
- **Active Record**: An object that wraps a row in a database table, encapsulates database access, and adds domain logic on that data.
- **Data Mapper**: A layer of mappers that moves data between objects and a database while keeping them independent of each other.
- **Unit of Work**: A pattern that maintains a list of objects affected by a business transaction and coordinates writing out changes to resolve concurrency problems.
- **Optimistic Offline Lock**: A concurrency pattern used for transactions spanning multiple requests to prevent conflicts without locking database records.
- **Page Controller**: An object that handles a request for a specific page or action on a Web site.
- **Front Controller**: A single controller that handles all requests for a Web site.
- **Template View**: A view pattern that renders information into HTML by embedding markers in an HTML page (e.g., JSP, ASP).
- **Transform View**: A view pattern that processes domain data element by element and transforms it into HTML (e.g., XSLT).
- **Two Step View**: A view pattern that turns domain data into HTML in two steps: forming a logical page, then rendering it into HTML.
- **Remote Facade**: A coarse-grained facade over fine-grained objects to improve efficiency over a network.
- **Data Transfer Object (DTO)**: An object that carries data between processes to reduce the number of method calls.
- **POJO**: Plain Old Java Object, used to describe standard Java objects unencumbered by platform-specific frameworks like EJB.
- **Mediating Layers**: Optional architectural layers such as Application Controller (between Presentation and Domain) and Data Mapper (between Domain and Data Source).

# @Objectives

- The AI MUST structure enterprise applications into three primary decoupled layers: Presentation, Domain, and Data Source.
- The AI MUST select the appropriate domain logic pattern strictly based on the complexity of the business rules and the target platform's tooling.
- The AI MUST perfectly align the Data Source mapping pattern with the chosen Domain logic pattern.
- The AI MUST enforce the principle of local execution by default, introducing distribution (Remote Facades and DTOs) only when strict physical process boundaries are required.
- The AI MUST apply platform-specific idioms (Java/J2EE vs. .NET) exactly as prescribed to maximize tool synergy and performance.
- The AI MUST implement Test-Driven Development (TDD), Continuous Integration (CI), and refactoring principles to ensure architectural decisions remain adaptable.

# @Guidelines

## Domain Layer Selection
- When encountering simple domain logic (e.g., basic catalog routing, simple pricing), the AI MUST use **Transaction Script**.
- When encountering moderate domain logic or working in an environment heavily geared toward Record Sets (e.g., .NET), the AI MUST use **Table Module**.
- When encountering highly complex, volatile, or intricate business rules, the AI MUST use **Domain Model**.

## Data Source Layer Alignment
- When implementing **Transaction Script**, the AI MUST separate database logic from the script by using either **Row Data Gateway** or **Table Data Gateway**. 
  - IF the system processes requests that span a read and a save, the AI MUST use **Optimistic Offline Lock**.
- When implementing **Table Module**, the AI MUST use **Table Data Gateway** to generate the Record Sets. The AI SHOULD leverage the Record Set's built-in concurrency controls as a **Unit of Work**.
- When implementing **Domain Model**:
  - IF the domain model is simple and isomorphic to the database schema, the AI MUST use **Active Record** (or Table/Row Data Gateway).
  - IF the domain model is complex and diverges from the database schema, the AI MUST use **Data Mapper**.
  - Whenever Data Mapper is used, the AI MUST implement a **Unit of Work** to handle concurrency and database writes.

## Presentation Layer Architecture
- When building HTML interfaces, the AI MUST separate the controller from the view (**Model View Controller**).
- For document-oriented sites with static/dynamic mixes, the AI MUST use **Page Controller**.
- For applications with complex navigation and heavy UI routing, the AI MUST use **Front Controller**.
- For view rendering, the AI MUST choose between **Template View** (if using server pages/HTML editors) or **Transform View** (if using XSLT/XML).
- IF the application requires a global, consistent layout or multiple distinct appearances for the same data, the AI MUST use **Two Step View**.

## Distribution Strategies
- The AI MUST NOT distribute objects by default. Processes MUST run locally in a single process wherever possible.
- When crossing a mandatory process boundary, the AI MUST NOT expose fine-grained domain objects.
- To communicate across boundaries, the AI MUST wrap the domain layer with a **Remote Facade** exposing coarse-grained methods.
- The AI MUST pass data across the remote boundary exclusively using **Data Transfer Objects (DTOs)**.

## Technology-Specific Implementation
- **Java/J2EE**:
  - For Transaction Scripts, the AI MAY use Session Beans acting upon Entity Beans (used strictly as Row Data Gateways) OR POJOs with Data Gateways.
  - For complex Domain Models, the AI MUST use POJOs for the domain logic and Data Mappers. The AI MUST NOT use Entity Beans for complex domain models.
  - The AI MUST NOT expose Entity Beans via remote interfaces.
  - IF distributing a POJO domain model, the AI MUST wrap it with Session Beans acting as Remote Facades.
- **.NET**:
  - The AI MUST default to **Table Module** interacting with ADO.NET Data Sets.
  - The AI MUST NOT use Transaction Scripts unless they are trivial procedures returning Data Sets.
  - The AI MUST NOT use Web Services for internal inter-layer communication within the same application.
- **Stored Procedures**:
  - The AI MUST NOT place domain or business logic inside stored procedures unless specifically requested for a severe performance bottleneck.
  - IF used, stored procedures MUST be encapsulated behind a **Table Data Gateway**.
- **Web Services**:
  - The AI MUST use Web Services exclusively for application integration, not internal application construction.
  - Web Services MUST be treated architecturally as **Remote Facades**.
  - The AI SHOULD design Web Services for asynchronous, message-based communication whenever possible.

## Alternative Layering Schemes
- When evaluating or integrating alternative layering schemes (e.g., Brown, Core J2EE, Microsoft DNA, Marinescu), the AI MUST map their components back to the primary Presentation-Domain-DataSource model.
- The AI MUST treat mediating layers (Application Controller, Data Mapper, Service Layer) as optional additions to the base three-layer architecture, utilized only when specific complexities arise.

# @Workflow

1. **Evaluate Domain Complexity**: Analyze the user request to determine the complexity of the business logic.
   - Assign the classification: Simple, Moderate/Tabular, or Complex.
2. **Select Domain Pattern**:
   - Simple -> Instantiate Transaction Script.
   - Moderate/Tabular (.NET) -> Instantiate Table Module.
   - Complex -> Instantiate Domain Model.
3. **Select Data Source Pattern**:
   - If Transaction Script -> Implement Row Data Gateway or Table Data Gateway.
   - If Table Module -> Implement Table Data Gateway returning Record Sets.
   - If Domain Model -> Implement Active Record (if simple/isomorphic) OR Data Mapper + Unit of Work (if complex).
4. **Select Presentation Pattern**:
   - Determine routing needs -> Select Page Controller or Front Controller.
   - Determine rendering needs -> Select Template View, Transform View, or Two Step View.
5. **Define Distribution Strategy**:
   - Attempt to consolidate all layers into a single process.
   - IF remote communication is strictly required -> Implement Remote Facade and construct DTOs for data transit.
6. **Apply Platform-Specific Adjustments**: Refine the design using POJOs (Java) or Data Sets (.NET) strictly adhering to the technology guidelines.
7. **Ensure Refactorability**: Output the architectural skeleton with clear unit testing boundaries (TDD) to allow safe future refactoring.

# @Examples (Do's and Don'ts)

- **[DO]** Use POJOs for complex Domain Models in Java to ensure they are decoupled from the EJB container.
```java
// Domain model using POJOs, decoupled from database and framework
public class Contract {
    private Product product;
    private Money revenue;
    private MfDate whenSigned;

    public Contract(Product product, Money revenue, MfDate whenSigned) {
        this.product = product;
        this.revenue = revenue;
        this.whenSigned = whenSigned;
    }
    public void calculateRecognitions() {
        product.calculateRevenueRecognitions(this);
    }
}
```

- **[DON'T]** Distribute fine-grained domain objects across a network boundary or expose Entity Beans remotely.
```java
// ANTI-PATTERN: Fine-grained remote calls (Causes severe network latency)
public interface Customer extends EJBObject { // Remote interface
    public String getFirstName() throws RemoteException;
    public void setFirstName(String name) throws RemoteException;
    public String getLastName() throws RemoteException;
    public void setLastName(String name) throws RemoteException;
}
```

- **[DO]** Wrap domain logic behind a Remote Facade and use a DTO for remote communication.
```java
// Remote Facade returning a coarse-grained DTO
public class AlbumServiceBean implements SessionBean {
    public AlbumDTO getAlbum(String id) throws RemoteException {
        return new AlbumAssembler().writeDTO(Registry.findAlbum(id));
    }
    public void updateAlbum(String id, AlbumDTO dto) throws RemoteException {
        new AlbumAssembler().updateAlbum(id, dto);
    }
}
```

- **[DON'T]** Put domain or business logic inside a Remote Facade.
```java
// ANTI-PATTERN: Remote Facade containing domain logic
public class AlbumServiceBean implements SessionBean {
    public void updateAlbum(String id, AlbumDTO dto) throws RemoteException {
        // Business logic mixed into facade
        if (dto.getPrice() < 10.00 && dto.getGenre().equals("Classical")) {
             dto.setDiscountApplied(true);
        }
        new AlbumAssembler().updateAlbum(id, dto);
    }
}
```

- **[DO]** Use Table Module and Table Data Gateway when working in a .NET Record Set-centric environment.
```csharp
// Table Module interacting with ADO.NET DataSet
class Contract : TableModule {
    public Contract (DataSet ds) : base (ds, "Contracts") {}

    public void CalculateRecognitions (long contractID) {
        DataRow contractRow = this[contractID];
        Decimal amount = (Decimal)contractRow["amount"];
        // Business logic acting on the DataRow...
    }
}
```

- **[DON'T]** Put complex business rules or HTML markup directly into a server page (Template View).
```html
<!-- ANTI-PATTERN: Scriptlets containing domain logic in a JSP -->
<%
    Order order = Order.find(request.getParameter("id"));
    if (order.getTotal() > 1000) {
        order.setDiscount(0.10);
    }
    order.save();
%>
```

- **[DO]** Use a Helper object or Controller to process logic, leaving the Template View strictly for display.
```html
<!-- Controller/Helper handles the logic, Template View handles display -->
<jsp:useBean id="helper" class="actionController.AlbumConHelper"/>
<% helper.init(request, response); %>
<B><jsp:getProperty name="helper" property="title"/></B>
```