# @Domain
These rules are triggered whenever the AI is tasked with designing, architecting, refactoring, or writing business/domain logic for an enterprise application. This includes creating application services, implementing business rules, handling validations and calculations, structuring data processing modules, or establishing the boundary between presentation, domain, and data source layers.

# @Vocabulary
*   **Domain Logic / Business Logic**: The rules, validations, calculations, and conditions that dictate how an application operates within its specific problem domain.
*   **Transaction Script**: A procedural architectural pattern that organizes business logic as a single procedure (or script) for each action or business transaction requested by a user.
*   **Domain Model**: An object-oriented architectural pattern that builds a rich model of the domain, organized primarily around the nouns of the domain, combining both state and complex behavior (calculations, validations) into individual objects.
*   **Table Module**: An architectural pattern where a single class instance handles the business logic for all rows in a database table or view, designed to work directly with a Record Set.
*   **Record Set**: A generic tabular data structure (like a SQL result set or .NET DataSet) used heavily by the Table Module pattern to pass data between layers.
*   **Service Layer**: A layer placed over a Domain Model or Table Module that provides a clear API, handles transaction control, and enforces security. 
*   **Controller-Entity Style**: A design approach where logic specific to a single use-case/transaction is placed in procedural services ("use-case controllers") while shared behavior resides in domain objects ("entities").
*   **Data Mapper**: A complex data source mapping layer required to persist a rich Domain Model without coupling the domain to the database schema.
*   **Row Data Gateway / Table Data Gateway**: Simple data source layers that map well to Transaction Scripts and Table Modules.

# @Objectives
*   Assess the complexity of the domain logic to select the most appropriate architectural pattern (Transaction Script, Table Module, or Domain Model).
*   Prevent code duplication and unmanageable webs of conditional logic by refactoring to object-oriented patterns when complexity increases.
*   Maintain strict boundaries between domain logic and presentation/data source layers.
*   Apply Service Layers judiciously to handle use-case workflows, transaction boundaries, and security without draining the underlying domain objects of their core business logic.

# @Guidelines

### Pattern Selection & Complexity Assessment
*   When evaluating a new feature or application, the AI MUST estimate the complexity of the domain logic to choose the architecture. 
*   When the domain logic is simple (e.g., basic order capturing, simple pricing, straightforward CRUD), the AI MUST use the **Transaction Script** pattern.
*   When the development environment features rich tooling for tabular data (e.g., .NET DataSets) and logic is moderately complex, the AI MUST consider the **Table Module** pattern.
*   When the business rules are highly complex, arbitrary, and feature numerous special cases or variations (exceeding the subjective complexity threshold of "7.42"), the AI MUST use the **Domain Model** pattern.
*   The AI MUST recognize that these patterns are not mutually exclusive; the AI MAY mix them within a single application (e.g., using Transaction Scripts for simple read-only use cases and a Domain Model for complex processing).

### Implementing Transaction Script
*   When implementing a Transaction Script, the AI MUST encapsulate all logic for a specific user action (validations, calculations, database saves, system invocations) within a single procedure or command object.
*   The AI MUST set clear transaction boundaries within the script (opening a transaction at the start and closing it at the end).
*   The AI MUST pair Transaction Scripts with simple data source layers, specifically Row Data Gateway or Table Data Gateway.
*   The AI MUST actively monitor Transaction Scripts for duplicated code across different transactions and factor common code into shared subroutines.

### Implementing Domain Model
*   When implementing a Domain Model, the AI MUST organize the logic primarily around the nouns of the domain (e.g., Lease, Asset, Product).
*   The AI MUST delegate specific parts of a calculation or validation to the object that owns the relevant data (e.g., a `Product` object contains the strategy for calculating its own revenue recognition).
*   The AI MUST account for the cost of data source complexity. When a rich Domain Model is used, the AI MUST isolate it from the database schema using the Data Mapper pattern.

### Implementing Table Module
*   When implementing a Table Module, the AI MUST create exactly *one* instance of the class to handle the logic for *all* instances of that domain entity (e.g., one `Contract` Table Module class to handle all contracts).
*   The AI MUST pass a Record Set as an argument to the Table Module's constructor or methods.
*   The AI MUST require clients to pass an ID (primary key) when invoking methods on the Table Module that apply to a specific individual record.

### Implementing Service Layer
*   When exposing a Domain Model or Table Module to a presentation layer, the AI MUST evaluate the need for a **Service Layer**.
*   The AI MUST use the Service Layer to define the application's API, manage database transaction boundaries, and enforce security checks.
*   The AI MUST default to creating the *thinnest possible* Service Layer (a facade) that merely forwards calls to the underlying Domain Model or Table Module.
*   If employing the "controller-entity" style, the AI MUST strictly place only use-case-specific logic in the Service Layer (as Transaction Scripts) while leaving all shared, multi-use-case logic in the underlying domain entities.

### Refactoring Rules
*   If a design starts with Transaction Script and the conditional logic becomes a tangled web or duplication becomes unmanageable, the AI MUST immediately refactor toward a Domain Model.
*   The AI MUST NOT refactor from a Domain Model down to a Transaction Script unless the data source layer complexity (Data Mapper) proves entirely unjustified by the domain logic.

# @Workflow
1.  **Analyze Request**: Identify the business rules, validations, and calculations required for the task.
2.  **Determine Architecture**:
    *   If logic is simple procedural steps -> Select **Transaction Script**.
    *   If environment is Record-Set-centric -> Select **Table Module**.
    *   If logic requires complex OO techniques (strategies, inheritance, rich behavior) -> Select **Domain Model**.
3.  **Structure the Logic**:
    *   *Transaction Script*: Write one method/class per business action. Factor out shared subroutines.
    *   *Table Module*: Create a single class representing the database table. Pass the Record Set into it. Add methods that manipulate the Record Set using passed-in IDs.
    *   *Domain Model*: Create granular noun-based objects. Distribute behavior so objects act on their own data. Connect via associations.
4.  **Establish Data Source Coupling**:
    *   Pair Transaction Script / Table Module with Gateways.
    *   Pair Domain Model with Data Mapper.
5.  **Apply Service Layer (Optional)**:
    *   Wrap the domain logic in a Service Layer to provide a clean API to the presentation.
    *   Inject transaction start/commit and security checks into the Service Layer methods.
    *   Delegate business decisions directly to the domain objects.

# @Examples (Do's and Don'ts)

### Transaction Script
*   **[DO]** Create a distinct procedure for a user action that orchestrates the entire flow:
    ```java
    public void calculateRevenueRecognitions(long contractNumber) {
        ResultSet contracts = db.findContract(contractNumber);
        // ... simple procedural logic to calculate and insert records ...
        db.insertRecognition(contractNumber, amount, date);
    }
    ```
*   **[DON'T]** Disperse the steps of a single transaction across multiple UI event handlers or leave transaction boundaries unmanaged.

### Domain Model
*   **[DO]** Distribute logic into the objects themselves, using OO principles like inheritance and strategy:
    ```java
    class Contract {
        private Product product;
        public void calculateRecognitions() {
            product.calculateRevenueRecognitions(this);
        }
    }
    class Product {
        private RecognitionStrategy strategy;
        public void calculateRevenueRecognitions(Contract contract) {
            strategy.calculateRevenueRecognitions(contract);
        }
    }
    ```
*   **[DON'T]** Create "anemic" domain objects that only have getters/setters and place all the business logic in a massive central manager class.

### Table Module
*   **[DO]** Instantiate one module passing in a Record Set, and pass IDs to operate on specific rows:
    ```csharp
    class Contract : TableModule {
        public Contract(DataSet ds) : base(ds, "Contracts") {}
        
        public void CalculateRecognitions(long contractID) {
            DataRow row = this[contractID];
            Decimal amount = (Decimal)row["amount"];
            // ... logic applied to the specific row in the DataSet ...
        }
    }
    ```
*   **[DON'T]** Create a new `Contract` instance for every row in the database when using this pattern.

### Service Layer
*   **[DO]** Use the Service Layer to handle transactions and delegate to the Domain Model:
    ```java
    class RecognitionService {
        @Transactional
        public void calculateRevenueRecognitions(long contractNumber) {
            Contract contract = Contract.readForUpdate(contractNumber);
            contract.calculateRecognitions(); // Delegation to Domain Model
            emailGateway.sendEmailMessage(...);
        }
    }
    ```
*   **[DON'T]** Strip the domain objects of their core logic and build a thick Service Layer that performs all the domain calculations directly, creating duplicated code across different services.